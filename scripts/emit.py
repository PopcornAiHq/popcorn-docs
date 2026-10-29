#!/usr/bin/env python3
"""One pass over `content/`, every machine-readable output.

Deliberately one script rather than one per artifact. Sites that grew a second
transform for their LLM exports ended up with the two disagreeing, and the
fix was always to collapse them back into a single walk of the source. So
`chunks.json`, `llms.txt`, `llms-full.txt`, `search.json` and the per-page
Markdown all come out of the same read here, and the next output belongs in
this file too.

Outputs, under `build/`:

    chunks.json      one record per concept — what the MCP server serves
    llms.txt         the index: id, title, summary. The whole corpus, cheaply.
    llms-full.txt    every written page's body concatenated, for a reader that
                     wants it all. A generated reference page contributes its
                     title, summary and URL but not its body: those pages are
                     looked up one entry at a time, and inlined they would
                     outweigh everything written by hand
    <part>/<kind>/<id>.md  the plain-Markdown twin of each page, at the
                     path its llms.txt entry advertises: the page's `part`,
                     then concepts or guides. The glossary and the
                     references have no part, and sit at <kind>/<id>.md
    <part>/<kind>/<id>.html  the same page for a person with a browser
    index.html       the Overview, rendered from `content/_overview.md`
    index.md         that source as written, the Overview's Markdown twin
    404.html         what a missing path is answered with, in the site's own
                     chrome, so a stale link still leaves the reader somewhere
                     they can navigate from
    fonts/           the self-hosted typefaces, copied from `assets/fonts/`
    robots.txt       allow everything. Without one the bucket answers 403 for
                     the missing key, and a crawler that reads a 403 robots.txt
                     as "disallow all" refuses every page on the site. It
                     names the sitemap
    sitemap.xml      every HTML page, for search engines. Some agents — Gemini's
                     browsing among them — open a URL only when it was pasted
                     or a search returned it, never by following a link, so a
                     page a search engine has not indexed is out of their reach
    search.json      what the site's own search reads: per page its title, URL,
                     section, summary and every heading or lookup entry with
                     its anchor. No bodies — chunks.json carries those, and
                     the browser fetches this whole on a reader's first search

`llms.txt` is the file most likely to be fetched by something we do not
control, so it carries summaries and not bodies. A reader that wants
everything asks for `llms-full.txt` and knows what it is paying for — and
what it pays for is prose. The reference pages stay in `chunks.json` and at
their own URLs, which is where an agent that needs one argument name should
get it.

Pages are written under their section, mirroring the URL in the index, so
that the link an agent follows is the file that was emitted. They were once
flattened into a single `md/` directory while the index advertised
`<section>/<id>`, and every link in the index 404ed. `check-links.py` is
what now holds the two together.

The `.md` suffix is load-bearing: it is what makes S3 serve the page as
text/markdown without the upload having to name a content type per object.

The HTML twin sits beside the Markdown one rather than replacing it, and
`llms.txt` keeps pointing at the `.md`. An agent asking for a page should get
prose, not a document it has to strip tags out of first; a person following
the same path in a browser gets the `.html`. Neither has to content-negotiate
and neither URL moves when the other changes.
"""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import sys

import render

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OVERVIEW = CONTENT / "_overview.md"
DIAGRAM = ROOT / "assets" / "routine.svg"
BUILD = ROOT / "build"
FONTS = ROOT / "assets" / "fonts"
SITE = render.SITE

_DOC = re.compile(r"^---\n(?P<fm>.*?)\n---\n(?P<body>.*)$", re.S)
_SCALAR = re.compile(r"^(?P<key>[a-z_]+):\s*(?P<val>.*)$")


def parse(path: pathlib.Path) -> dict:
    """Frontmatter and body. A deliberately small YAML subset.

    Only the shapes `content/_frontmatter.md` documents: plain scalars, folded
    blocks (`key: >`), and flow sequences (`key: [a, b]`). Anything else is a
    file that does not follow the contract, and the contract checker is what
    should say so — not a silent reinterpretation here.
    """
    doc = _DOC.match(path.read_text())
    if not doc:
        raise SystemExit(f"✖  {path.relative_to(ROOT)}: no frontmatter")

    meta: dict = {}
    key: str | None = None
    folded: list[str] = []

    for line in doc.group("fm").splitlines():
        if key and (line.startswith("  ") or line.startswith("\t")):
            folded.append(line.strip())
            continue
        if key:
            meta[key] = " ".join(folded).strip()
            key, folded = None, []

        found = _SCALAR.match(line)
        if not found:
            continue
        name, value = found.group("key"), found.group("val").strip()
        if value == ">":
            key = name
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[name] = [v.strip() for v in inner.split(",") if v.strip()]
        else:
            meta[name] = value

    if key:
        meta[key] = " ".join(folded).strip()

    # A number, not the string the scalar parse gives: sorted as text, 10
    # would come before 2. check-content.py rejects anything that is not one.
    if "order" in meta:
        meta["order"] = int(meta["order"])
    meta["body"] = doc.group("body").strip()
    # The content directory the page lives in. Its URL is no longer that
    # directory: see `page_dir`.
    meta["source_dir"] = path.parent.name
    return meta


# The two parts of the site, Using Popcorn first: (frontmatter value, label).
# A page's part is the first segment of its URL and a heading of the sidebar;
# the pages with no part follow both, under Look it up. Popcorn is used
# headless, so a user's assistant is the first reader, and Using Popcorn leads.
PARTS = [
    ("use", "Using Popcorn"),
    ("build", "Building Routine Templates"),
]

# The kinds of page: (kind, label). The sidebar lists topics, not kinds, so
# the label is seen in a page's eyebrow and in search. A kind not listed here
# still publishes, after these, under its own name.
SECTIONS = [
    ("concepts", "Concepts"),
    ("guides", "Guides"),
    ("glossary", "Glossary"),
    ("reference", "Reference"),
]

# The sections whose pages a generator writes. llms-full.txt names them
# without inlining them; see the module docstring.
GENERATED = {"reference"}

_KNOWN = [name for name, *_ in SECTIONS]
_PARTS = [name for name, *_ in PARTS]

# Kinds that serve both parts and belong to neither. Their pages have no
# `part:`, sit at /<kind>/<id>, and are listed once, after both parts.
SHARED = {"glossary", "reference"}

def check_part(page: dict) -> None:
    """Stop the build, naming the page, when its `part` does not fit its kind.

    check-content.py reports the same with the rest of the contract; this is
    for a build run on its own, which would otherwise fail on a KeyError or
    put a shared page under one part."""
    part, kind = page.get("part"), nav_section(page)
    if kind in SHARED and part:
        sys.exit(f"✖  {page['id']}: a {kind} page has no part:, but this one says '{part}'")
    if kind not in SHARED and part not in _PARTS:
        sys.exit(f"✖  {page['id']}: part: must be one of {', '.join(_PARTS)}, not {part!r}")


# Pages listed under a kind other than their directory's. The glossary lives
# in content/concepts/ but is looked up rather than read through. An id never
# changes meaning, which is what makes naming one here safe.
NAV_SECTION = {"glossary": "glossary"}


def nav_section(page: dict) -> str:
    return NAV_SECTION.get(page["id"], page["source_dir"])


def page_dir(page: dict) -> str:
    """The page's directory on the site: its part, when it has one, then its kind."""
    part = page.get("part")
    return f"{part}/{nav_section(page)}" if part else nav_section(page)


def href(page: dict, suffix: str = ".html") -> str:
    return f"/{page_dir(page)}/{page['id']}{suffix}"


def url(page: dict | None) -> str:
    """A page's canonical address — the one the sitemap lists. None is the home page."""
    return f"{SITE}/" if page is None else f"{SITE}{href(page)}"


def section_label(section: str) -> str:
    return dict(SECTIONS).get(section, section.title())


def part_label(part: str) -> str:
    return dict(PARTS).get(part, part.title())


def reading_order(page: dict) -> tuple:
    """Part first, then the page's `order:`, then its kind, then its title.

    `order:` numbers a part's pages in one sequence, concepts and guides
    together, so a guide sits beside the concepts it puts to work. Filenames
    sort alphabetically, which put an advanced guide ahead of the one it
    builds on. A page with no `order:` goes after the ordered ones in its part.
    """
    part = page.get("part")
    part_rank = _PARTS.index(part) if part in _PARTS else len(_PARTS)
    section = nav_section(page)
    rank = _KNOWN.index(section) if section in _KNOWN else len(_KNOWN)
    order = page.get("order")
    return (part_rank, order is None, order or 0, rank, section, page["title"].lower())


def by_topic(pages: list[dict]) -> list[dict]:
    """The pages in the sidebar's order: each part's groups, then the rest.

    A group sits where its first page does in reading order, so groups need
    no order of their own; a later page in the same group joins it there.
    The pager walks this order too, so Next is always the link below.
    """
    topics: dict[tuple, list[dict]] = {}
    for page in pages:
        key = (page.get("part") or "", page.get("group", "") if page.get("part") else "")
        topics.setdefault(key, []).append(page)
    return [page for group in topics.values() for page in group]


def sidebar(pages: list[dict], current: str | None) -> str:
    """The site sidebar: each part's `group:`s, then Look it up.

    A part lists topics, not kinds: a group holds concepts and guides alike,
    so neither heading repeats under both parts. Pages without a group sit
    directly under their part.
    """
    parts: dict[str, dict[str, list]] = {}
    # The glossary and the references serve both parts, so they are listed
    # once, after them, under one heading rather than one each.
    shared: list = []
    for page in by_topic(pages):
        link = (render.inline(page["title"]), href(page), page["id"] == current)
        if not page.get("part"):
            shared.append(link)
            continue
        parts.setdefault(page["part"], {}).setdefault(page.get("group", ""), []).append(link)
    # The home page leads the sidebar, current when no page is — `current`
    # is None only when the landing page is the one being built.
    out: list = [(None, [("", [("Overview", "/", current is None)])])]
    for part, groups in parts.items():
        out.append((part_label(part), None))
        out.append(("", list(groups.items())))
    if shared:
        out.append((LOOK_UP, None))
        out.append((None, [("", shared)]))
    return render.site_nav(out)


# The sidebar's heading for the kinds that belong to neither part.
LOOK_UP = "Look it up"


_DIAGRAM_BLOCK = re.compile(r"^```diagram\n.*?^```\n", re.M | re.S)


def overview() -> tuple[str, str]:
    """The Overview's lede and body, from `content/_overview.md`.

    The source opens with `# Overview` and one paragraph, which is the page's
    summary: styled as one on the site, and the blockquote `llms.txt` opens
    with, as the llms.txt format asks."""
    text = OVERVIEW.read_text().split("\n", 1)[1].strip()
    lede, rest = text.split("\n\n", 1)
    return " ".join(lede.split()), rest


def landing(pages: list[dict]) -> str:
    """The home page, rendered from `content/_overview.md`.

    The page is hand-written rather than assembled from the sidebar's parts
    and kinds: a first-time reader needs a first action and a picture of a
    Routine, which no listing of pages gives them. Its source is also served
    as `/index.md`, so an agent can read it like any other page.
    """
    lede, rest = overview()
    # The ```diagram block is a text drawing, which is what an agent reading
    # /index.md should get. A person gets the drawing in assets/, inlined
    # rather than linked so it takes the page's colours in either theme.
    rest = _DIAGRAM_BLOCK.sub("\x00diagram\x00\n", rest, count=1)
    figure = f'<figure class="diagram">{DIAGRAM.read_text().strip()}</figure>'
    return render.document(
        "Overview — Popcorn docs",
        f'<h1>Overview</h1>\n<p class="summary">{render.inline(lede)}</p>\n'
        + render.body(rest).replace("<p>\x00diagram\x00</p>", figure),
        description="How Popcorn Routines work, and how to build the Routine "
        "Templates they are made from.",
        sidebar=sidebar(pages, None),
        url=url(None),
    )


def not_found(pages: list[dict]) -> str:
    """The page a missing path is answered with.

    It is served at whatever path was asked for, not at `/404.html`, so every
    link on it is root-relative — the sidebar's already are. No page is
    current, and it asks not to be indexed: a search result pointing at it
    would be a dead link that looks like a page.
    """
    return render.document(
        "Page not found — Popcorn docs",
        "<h1>Page not found</h1>\n"
        '<p class="summary">Nothing is published at this address. The page may '
        "have moved, or the link may have a typo in it.</p>\n"
        '<p>Start again from the <a href="/">Overview</a>, or, if you are an '
        'agent, from <a href="/llms.txt">/llms.txt</a>, which lists every page '
        "with its summary.</p>",
        # Not the landing page, and not any section's: "" matches no page id,
        # and the Overview link is current only for None.
        sidebar=sidebar(pages, ""),
        noindex=True,
    )


def pager(page: dict, pages: list[dict]) -> str:
    """Previous and next within the page's own part, in the sidebar's order."""
    peers = [p for p in by_topic(pages) if p.get("part") == page.get("part")]
    i = next(n for n, p in enumerate(peers) if p["id"] is page["id"])
    links = []
    if i > 0:
        prev = peers[i - 1]
        links.append(f'<a class="prev" rel="prev" href="{href(prev)}">'
                     f'<span>Previous</span>{render.inline(prev["title"])}</a>')
    if i + 1 < len(peers):
        nxt = peers[i + 1]
        links.append(f'<a class="next" rel="next" href="{href(nxt)}">'
                     f'<span>Next</span>{render.inline(nxt["title"])}</a>')
    return f'<nav class="pager" aria-label="{part_label(page["part"]) if page.get("part") else LOOK_UP}">' + "".join(links) + "</nav>\n" if links else ""


def related(page: dict, by_id: dict[str, dict]) -> list[render.Link]:
    """"See also" from the page's `concepts:` — only ids that exist.

    An id naming no page is dropped rather than linked, so a typo costs a
    missing link, not a 404 on the published site.
    """
    return [
        (render.inline(by_id[i]["title"]), href(by_id[i]), False)
        for i in page.get("concepts", [])
        if i in by_id and i != page["id"]
    ]


def version_badge(page: dict) -> str:
    """What a generated page describes, beside its title.

    Only a page whose generator records one gets a badge. `version:` is the
    release the CLI reference describes, which it would otherwise mention only
    mid-sentence. `updated:` is the date of the prod deploy the activity and
    MCP references were last regenerated from, which moves only when the page
    does — the platform has no release number a reader could use, so the date
    is what says how fresh the page is.
    A page has one or the other.
    """
    if page.get("version"):
        # Written without its `v` by the generator; stripped anyway, so a
        # value that arrives with one still reads as a version, not `vv…`.
        release = str(page["version"]).removeprefix("v")
        return f'<span class="version-badge" title="Generated from this release">v{release}</span>'
    if page.get("updated"):
        return (f'<span class="version-badge" title="Generated from the platform deployed on this date">'
                f'updated {page["updated"]}</span>')
    return ""


def eyebrow(page: dict) -> str:
    """Where the page sits: its part, its kind, and its group when it has one."""
    part, section = page.get("part"), nav_section(page)
    kind = section_label(section)
    trail = f"{part_label(part)} \u203a {kind}" if part else kind
    if page.get("group"):
        trail += f" \u203a {render.inline(page['group'])}"
    return f'<p class="eyebrow">{trail}</p>\n'


def main() -> int:
    pages = sorted(
        (parse(p) for p in CONTENT.rglob("*.md") if not p.name.startswith("_")),
        key=reading_order,
    )
    if not pages:
        print("✖  no content", file=sys.stderr)
        return 1
    for page in pages:
        check_part(page)

    # Rebuild from empty. Without this a page that was renamed or deleted in
    # `content/` keeps its old file here, and the publish is a sync rather than
    # a replacement, so the stale copy stays reachable on the site long after
    # nothing links to it.
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    # `section` in chunks.json is the page's directory on the site, so a
    # reader that builds `<section>/<id>.md` from it lands on the page —
    # which is how the channel agents' docs tool finds one.
    chunks = [
        {
            k: v
            for k, v in {
                **page,
                "section": page_dir(page),
            }.items()
            if k != "source_dir"
        }
        for page in pages
    ]
    (BUILD / "chunks.json").write_text(
        json.dumps({"site": SITE, "pages": chunks}, indent=2) + "\n"
    )

    search = []
    index = ["# Popcorn docs", "", f"> {overview()[0]}", "",
             "## Overview", f"{SITE}/index.md", "",
             "What Popcorn is, how a Routine works, and one way into each part. Start here.", ""]
    full = [
        "# Popcorn docs — full text",
        "",
        "Every written page in full. A generated reference page is listed by its "
        "title, summary and URL: fetch it there when you need its entries.",
        "",
    ]
    by_id = {page["id"]: page for page in pages}
    for page in pages:
        path = href(page, ".md").lstrip("/")
        index += [f"## {page['title']}", f"{SITE}/{path}", "", page["summary"], ""]
        if page["source_dir"] in GENERATED:
            full += [f"# {page['title']}", "", page["summary"], "", f"Full reference: {SITE}/{path}", ""]
        else:
            full += [f"# {page['title']}", "", page["summary"], "", page["body"], ""]
        page_file = BUILD / path
        page_file.parent.mkdir(parents=True, exist_ok=True)
        page_file.write_text(
            f"# {page['title']}\n\n{page['summary']}\n\n{page['body']}\n"
        )
        # A lookup page — the glossary, the activity reference — is looked up
        # rather than read through, so its own entries replace the rail's
        # contents list. Its related pages are left out: the entries already
        # link to them, and a second list would push the index down.
        lookup = page.get("layout") == "lookup"
        rendered = render.body(page["body"], terms=lookup)
        page_file.with_suffix(".html").write_text(
            render.document(
                f"{page['title']} — Popcorn docs",
                eyebrow(page)
                + f'<div class="title-row"><div class="title"><h1>{render.inline(page["title"])}</h1>'
                f"{version_badge(page)}</div>"
                f"{render.page_actions('/' + path)}</div>\n"
                f'<p class="summary">{render.inline(page["summary"])}</p>\n'
                f"{render.on_this_page(rendered, lookup=lookup)}"
                f"{rendered}\n"
                f"{pager(page, pages)}",
                description=page["summary"],
                sidebar=sidebar(pages, page["id"]),
                rail=render.rail(
                    contents=render.lookup_index(rendered) if lookup else render.toc(rendered),
                    related=[] if lookup else related(page, by_id),
                ),
                url=url(page),
                lookup=lookup,
                own_date=bool(page.get("updated")),
            )
        )

        search.append({
            "title": render.plain(page["title"]),
            "url": href(page),
            "section": (
                f"{part_label(page['part'])} \u203a {section_label(nav_section(page))}"
                if page.get("part") else section_label(nav_section(page))
            ),
            "summary": render.plain(page["summary"]),
            "headings": render.search_entries(rendered),
        })

    (BUILD / "llms.txt").write_text("\n".join(index))

    (BUILD / "search.json").write_text(
        json.dumps({"pages": search}, ensure_ascii=False, separators=(",", ":")) + "\n"
    )
    (BUILD / "llms-full.txt").write_text("\n".join(full))
    (BUILD / "index.html").write_text(landing(pages))
    shutil.copyfile(OVERVIEW, BUILD / "index.md")
    (BUILD / "404.html").write_text(not_found(pages))
    # The fonts are committed rather than generated, and the pages name them
    # by path, so a missing file is a page quietly set in the fallback face.
    # Checking here makes it a failed build instead.
    shutil.copytree(FONTS, BUILD / "fonts")
    missing = [f for f in render.FONT_FILES if not (BUILD / f.lstrip("/")).is_file()]
    if missing:
        print(f"✖  the pages load {', '.join(missing)}, which assets/fonts/ does not hold",
              file=sys.stderr)
        return 1
    (BUILD / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
    )
    locs = [url(None)] + [url(p) for p in pages]
    (BUILD / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{loc}</loc></url>\n" for loc in locs)
        + "</urlset>\n"
    )

    size = (BUILD / "llms.txt").stat().st_size
    sections = ", ".join(sorted({f"{page_dir(p)}/" for p in pages}))
    print(f"✔  {len(pages)} pages → chunks.json, llms.txt ({size:,}B), "
          f"llms-full.txt, search.json ({(BUILD / 'search.json').stat().st_size:,}B), "
          f"index.html, 404.html, robots.txt, sitemap.xml, fonts/, {sections}(.md + .html)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
