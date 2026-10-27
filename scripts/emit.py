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
    index.html       the landing page, every concept with its summary
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


# The two parts of the site, Using Popcorn first: (frontmatter value, label,
# who it is for). A page's part is the first segment of its URL and a heading
# of the sidebar. Popcorn is used headless, so a user's assistant is the first
# reader, and Using Popcorn leads.
PARTS = [
    ("use", "Using Popcorn",
     "For anyone working with Routines, directly or through an assistant "
     "connected over MCP: what a Routine does, and what you can ask of it."),
    ("build", "Building Routine Templates",
     "For building or customizing the templates Routines are made from: the "
     "files, flows and tools underneath, with no access to Popcorn's backend."),
]

# The kinds of page within a part, in the order a reader meets them:
# (kind, label, what it is for). The label heads the kind in the sidebar and
# on its Overview card; the blurb is the card's text. A kind not listed here
# still publishes, after these, under its own name.
SECTIONS = [
    ("concepts", "Concepts", "One idea each, in reading order."),
    ("guides", "Guides", "Walkthroughs, start to finish, each building on the last."),
    ("glossary", "Glossary", "Every term, with its synonyms and the collisions worth knowing."),
    ("reference", "Reference", "Generated from Popcorn itself, never written by hand."),
]

# The sections whose pages a generator writes. llms-full.txt names them
# without inlining them; see the module docstring.
GENERATED = {"reference"}

_KNOWN = [name for name, *_ in SECTIONS]
_PARTS = [name for name, *_ in PARTS]

# Kinds that serve both parts and belong to neither. Their pages have no
# `part:`, sit at /<kind>/<id>, and are listed once, after both parts.
SHARED = {"glossary", "reference"}

# chunks.json carries each page's `part`, and beside it the `layer` that
# readers built before the field was renamed still look for. The glossary
# answers as a page on using Popcorn and the references as building pages,
# which is where a tie between them ranks in the docs server's search too.
LEGACY_LAYER = {"use": "product", "build": "platform", "glossary": "product", "reference": "platform"}


def legacy_layer(page: dict) -> str:
    return LEGACY_LAYER[page.get("part") or nav_section(page)]

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


def section_info(section: str) -> tuple[str, str]:
    for name, label, blurb in SECTIONS:
        if name == section:
            return label, blurb
    return section.title(), ""


def part_info(part: str) -> tuple[str, str]:
    for name, label, blurb in PARTS:
        if name == part:
            return label, blurb
    return part.title(), ""


def reading_order(page: dict) -> tuple:
    """Part first, then section, then the page's `order:`, then its title.

    `order:` is what makes a reading path: filenames sort alphabetically,
    which put an advanced guide ahead of the one it builds on. A page with
    no `order:` goes after the ordered ones in its section.
    """
    part = page.get("part")
    part_rank = _PARTS.index(part) if part in _PARTS else len(_PARTS)
    section = nav_section(page)
    rank = _KNOWN.index(section) if section in _KNOWN else len(_KNOWN)
    order = page.get("order")
    return (part_rank, rank, section, order is None, order or 0, page["title"].lower())


def sidebar(pages: list[dict], current: str | None) -> str:
    """The site sidebar: sections in reading order, then `group:` within them.

    A group sits where its first page does, so groups follow the reading
    order rather than needing an order of their own; pages without a group
    sit directly under their section.
    """
    parts: dict[str, dict[str, dict[str, list]]] = {}
    # The glossary and the references serve both parts, so each is listed
    # once, after them, rather than as a section of either.
    shared: dict[str, list] = {}
    for page in pages:
        link = (render.inline(page["title"]), href(page), page["id"] == current)
        if not page.get("part"):
            shared.setdefault(nav_section(page), []).append(link)
            continue
        groups = parts.setdefault(page["part"], {}).setdefault(nav_section(page), {})
        groups.setdefault(page.get("group", ""), []).append(link)
    # The home page leads the sidebar, current when no page is — `current`
    # is None only when the landing page is the one being built.
    out: list = [(None, [("", [("Overview", "/", current is None)])])]
    for part, sections in parts.items():
        # A part is a heading with no links of its own; its kinds follow.
        out.append((part_info(part)[0], None))
        out += [
            (section_info(section)[0], list(groups.items()))
            for section, groups in sections.items()
        ]
    for kind, links in shared.items():
        out.append((section_info(kind)[0], None))
        out.append((None, [("", links)]))
    return render.site_nav(out)


# The landing page's heading for the kinds that belong to neither part.
LOOK_UP = ("Look it up", "Every term, and every command, tool and activity, for either part.")


def anchor(page: dict) -> str:
    """The landing card a page's eyebrow links back to: its part and kind, or its kind."""
    part = page.get("part")
    return f"{part}-{nav_section(page)}" if part else nav_section(page)


def landing(pages: list[dict]) -> str:
    """The home page: what Popcorn is, what these pages cover, one way in each.

    It does not list every page — the sidebar beside it already does. Each
    section gets a card that opens its first page in reading order, so the
    way in follows `order:` rather than being chosen again here.
    """
    first: dict[str, dict[str, dict]] = {}
    for page in pages:
        first.setdefault(page.get("part") or "", {}).setdefault(nav_section(page), page)
    blocks = []
    for part, sections in first.items():
        if part:
            label, blurb = part_info(part)
        else:
            label, blurb = LOOK_UP
        cards = []
        for section, page in sections.items():
            kind, kind_blurb = section_info(section)
            cards.append(
                f'<a class="card" id="{anchor(page)}" href="{href(page)}">'
                f'<span class="card-label">{kind}</span>'
                f"<p>{kind_blurb}</p>"
                f'<span class="card-start">{render.inline(page["title"])} \u2192</span></a>'
            )
        blocks.append(
            f'<h2 id="{part or "look-up"}">{label}</h2>\n<p>{blurb}</p>\n'
            '<div class="cards">' + "".join(cards) + "</div>\n"
        )
    return render.document(
        "Overview — Popcorn docs",
        "<h1>Overview</h1>\n"
        '<p class="summary">Popcorn runs Routines. Each one is a piece of ongoing '
        "work, such as claims intake or order follow-up, that reads across email, "
        "messages and files, catches every update and decision, and keeps itself "
        "current. People talk to its agent like a member of the team.</p>\n"
        "<p>Many Routines take each item they work on, such as a potential client "
        "or an order on its way, through a few Steps. The Routine asks for what "
        "each Step needs, follows up until it has it, and stops for your Review "
        "where you asked it to.</p>\n"
        "<p>These pages come in two parts, both in the words you see in Popcorn. "
        "<strong>Using Popcorn</strong> is for working with Routines; "
        "<strong>Building Routine Templates</strong> goes underneath, to what a "
        "template is made of and how to change one. The glossary and the "
        "references serve both.</p>\n"
        + "".join(blocks)
        + "<h2>For agents</h2>\n"
        "<p>Every page has a Markdown twin at the same path, ending "
        "<code>.md</code> instead of <code>.html</code>. "
        '<a href="/llms.txt">/llms.txt</a> lists every page with its summary, '
        '<a href="/llms-full.txt">/llms-full.txt</a> holds every written page in '
        "full and names the generated reference pages, and "
        '<a href="/chunks.json">/chunks.json</a> has one record per page.</p>',
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
    """Previous and next within the page's own section, in reading order."""
    peers = [p for p in pages if nav_section(p) == nav_section(page)]
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
    return f'<nav class="pager" aria-label="{section_info(nav_section(page))[0]}">' + "".join(links) + "</nav>\n" if links else ""


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
    mid-sentence. `deployed:` is the date of the prod deploy the activity and
    MCP references were last regenerated from — the platform has no release
    number a reader could use, so the date is what says how fresh the page is.
    A page has one or the other.
    """
    if page.get("version"):
        # Written without its `v` by the generator; stripped anyway, so a
        # value that arrives with one still reads as a version, not `vv…`.
        release = str(page["version"]).removeprefix("v")
        return f'<span class="version-badge" title="Generated from this release">v{release}</span>'
    if page.get("deployed"):
        return (f'<span class="version-badge" title="Generated from the platform deployed on this date">'
                f'deployed {page["deployed"]}</span>')
    return ""


def eyebrow(page: dict) -> str:
    """Where the page sits: its part, its kind, and its group when it has one."""
    part, section = page.get("part"), nav_section(page)
    kind = f'<a href="/#{anchor(page)}">{section_info(section)[0]}</a>'
    trail = f'<a href="/#{part}">{part_info(part)[0]}</a> \u203a {kind}' if part else kind
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
                "layer": legacy_layer(page),
            }.items()
            if k != "source_dir"
        }
        for page in pages
    ]
    (BUILD / "chunks.json").write_text(
        json.dumps({"site": SITE, "pages": chunks}, indent=2) + "\n"
    )

    search = []
    index = ["# Popcorn docs", ""]
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
            )
        )

        search.append({
            "title": render.plain(page["title"]),
            "url": href(page),
            "section": (
                f"{part_info(page['part'])[0]} \u203a {section_info(nav_section(page))[0]}"
                if page.get("part") else section_info(nav_section(page))[0]
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
