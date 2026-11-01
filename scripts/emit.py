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
    <id>.md          the plain-Markdown twin of each page, at the path its
                     llms.txt entry advertises. Every page sits at the site's
                     root, whatever its part, so a page that moves between
                     parts keeps its address
    <id>.html        the same page for a person with a browser, which
                     opens with the page's lede where the twin has its summary.
                     It is served at `/<id>`, with no extension: `publish.py`
                     uploads it under the bare id
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
                     section, lede and every heading or lookup entry with
                     its anchor. No bodies — chunks.json carries those, and
                     the browser fetches this whole on a reader's first search

`llms.txt` is the file most likely to be fetched by something we do not
control, so it carries summaries and not bodies. A reader that wants
everything asks for `llms-full.txt` and knows what it is paying for — and
what it pays for is prose. The reference pages stay in `chunks.json` and at
their own URLs, which is where an agent that needs one argument name should
get it.

Pages are written at the path the index names, so that the link an agent
follows is the file that was emitted. They were once flattened into a
single `md/` directory while the index advertised `<section>/<id>`, and
every link in the index 404ed. `check-links.py` is what now holds the two
together.

The `.md` suffix is load-bearing: it is what makes S3 serve the page as
text/markdown without the upload having to name a content type per object.

The HTML twin sits beside the Markdown one rather than replacing it, and
`llms.txt` keeps pointing at the `.md`. An agent asking for a page should get
prose, not a document it has to strip tags out of first; a person gets the
HTML at the same address without the suffix, `/steps` beside `/steps.md`.
Neither has to content-negotiate and neither URL moves when the other changes.
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
    # The content directory the page lives in: its part, or for a page that
    # serves both parts, its kind. A page's URL never includes it; see `href`.
    meta["source_dir"] = path.parent.name
    if meta["source_dir"] in _PARTS:
        meta["part"] = meta["source_dir"]
    return meta


# The two parts of the site, Using Popcorn first: (directory, label). A
# page's part is the content directory it is written in and a heading of the
# sidebar; the pages with no part follow both, under Look it up. Popcorn is used
# headless, so a user's assistant is the first reader, and Using Popcorn leads.
PARTS = [
    ("use", "Using Popcorn"),
    ("build", "Building Routine Templates"),
]

# The kinds of page that serve both parts and belong to neither: (directory,
# label). They are looked up rather than read through, are listed once after
# both parts, and say their kind in their eyebrow and in search. Every other
# page is simply a page of its part.
SHARED = [
    ("glossary", "Glossary"),
    ("reference", "Reference"),
]

# The kinds whose pages a generator writes. llms-full.txt names them without
# inlining them; see the module docstring.
GENERATED = {"reference"}

_PARTS = [name for name, *_ in PARTS]
_SHARED = [name for name, *_ in SHARED]


def check_place(page: dict) -> None:
    """Stop the build, naming the page, when it is not in a known directory.

    check-content.py reports the same with the rest of the contract; this is
    for a build run on its own, which would otherwise publish a page under
    no part and no kind."""
    if page["source_dir"] not in _PARTS + _SHARED:
        sys.exit(f"✖  {page['id']}: content/{page['source_dir']}/ is not a part "
                 f"({', '.join(_PARTS)}) or a shared kind ({', '.join(_SHARED)})")


def kind(page: dict) -> str:
    """`glossary` or `reference` for the pages both parts share, `page` otherwise."""
    return page["source_dir"] if page["source_dir"] in _SHARED else "page"


def lede(page: dict) -> str:
    """What a person reads under the page's title, in the site's search and
    in a link preview: the page's `lede` when it has one, its `summary`
    otherwise. Agents read the summary everywhere, because it is written to
    be acted on without opening the page."""
    return page.get("lede") or page["summary"]


def href(page: dict, suffix: str = "") -> str:
    """A page's path on the site: its id, at the root. Ids are unique across
    the site, so the part a page sits in needn't be part of its address.

    The HTML page has no extension — `/steps`, the address a person types or
    shares — and is written to `<id>.html` only because a file needs one;
    `publish.py` uploads it under the bare id. The Markdown twin keeps its
    `.md`, because that suffix is what an agent and `llms.txt` name."""
    return f"/{page['id']}{suffix}"


def url(page: dict | None) -> str:
    """A page's canonical address — the one the sitemap lists. None is the home page."""
    return f"{SITE}/" if page is None else f"{SITE}{href(page)}"


def place_label(page: dict) -> str:
    """Where the page sits, as its eyebrow and the site's search name it."""
    if page.get("part"):
        return part_label(page["part"])
    return dict(SHARED).get(page["source_dir"], page["source_dir"].title())


def part_label(part: str) -> str:
    return dict(PARTS).get(part, part.title())


def reading_order(page: dict) -> tuple:
    """Part first, then the page's `order:`, then its kind, then its title.

    `order:` numbers a part's pages in one sequence, so a task page sits
    beside the pages about what it puts to work. Filenames sort
    alphabetically, which put an advanced task ahead of the one it builds
    on. A page with no `order:` goes after the ordered ones in its part; the
    glossary comes before the references.
    """
    part = page.get("part")
    place = _PARTS + _SHARED
    rank = place.index(page["source_dir"]) if page["source_dir"] in place else len(place)
    order = page.get("order")
    return (rank, order is None, order or 0, page["title"].lower())


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


# The header's tabs: each part, then the lookups both parts share. Shorter
# than the parts' own names, which the eyebrow above each title still uses.
TABS = [("use", "Using Popcorn"), ("build", "Building Templates"), ("", "Reference")]

# The sidebar heading over the glossary and the references.
LOOK_UP = "Look it up"

# The group the Overview leads, at the top of the first tab.
GETTING_STARTED = "Getting started"


def tab_of(page: dict | None) -> str:
    """The tab a page sits under: its part, or "" for the shared kinds. The
    Overview, None here, opens the first part."""
    return _PARTS[0] if page is None else page.get("part") or ""


def tabs(pages: list[dict], current: str | None) -> list[render.Link]:
    """The header's tabs, each linking to the first page under it. The 404
    page, `current` "", sits under no tab."""
    page = next((p for p in pages if p["id"] == current), None)
    active = None if current == "" else tab_of(page)
    first = {}
    for p in by_topic(pages):
        first.setdefault(tab_of(p), href(p))
    first[_PARTS[0]] = "/"
    return [(label, first[key], key == active) for key, label in TABS if key in first]


def sidebar(pages: list[dict], current: str | None) -> str:
    """The site sidebar: the current tab's `group:`s, each under its heading.

    A group holds every page about one topic, whether it explains a thing or
    walks through a task; pages without one are listed with no heading. The
    Overview leads the first part's Getting started, which is where the 404
    page, under no tab, starts a reader again.
    """
    page = next((p for p in pages if p["id"] == current), None)
    tab = tab_of(page)
    groups: dict[str, list] = {}
    for p in by_topic(pages):
        if tab_of(p) != tab:
            continue
        link = (render.inline(p["title"]), href(p), p["id"] == current)
        groups.setdefault(p.get("group", "") if tab else LOOK_UP, []).append(link)
    if tab == _PARTS[0]:
        home = ("Overview", "/", current is None)
        groups = {GETTING_STARTED: [home] + groups.pop(GETTING_STARTED, []), **groups}
    return render.site_nav(list(groups.items()), tabs(pages, current))


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
    rendered = render.body(rest).replace("<p>\x00diagram\x00</p>", figure)
    return render.document(
        "Overview — Popcorn docs",
        f'<h1>Overview</h1>\n<p class="summary">{render.inline(lede)}</p>\n'
        f"{render.on_this_page(rendered, lookup=False)}"
        + rendered,
        description="How Popcorn Routines work, and how to build the Routine "
        "Templates they are made from.",
        sidebar=sidebar(pages, None),
        tabs=tabs(pages, None),
        rail=render.rail(contents=render.toc(rendered)),
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
        tabs=tabs(pages, ""),
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
    """Where the page sits: its part or kind, and its group when it has one."""
    trail = place_label(page)
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
        check_place(page)

    # Rebuild from empty. Without this a page that was renamed or deleted in
    # `content/` keeps its old file here, and the publish is a sync rather than
    # a replacement, so the stale copy stays reachable on the site long after
    # nothing links to it.
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    # `path` in chunks.json is the page's Markdown twin, relative to the site,
    # and is what a reader should fetch: the docs tools in Popcorn find a page
    # by it. `kind` says what sort of page it is (`glossary` and `reference`
    # are looked up rather than read). `section` is the page's part, or its
    # kind for a page with none; it is not a directory on the site.
    chunks = [
        {
            k: v
            for k, v in {
                **page,
                "path": href(page, ".md").lstrip("/"),
                "kind": kind(page),
                "section": page["source_dir"],
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
             "What Popcorn is, how to connect an assistant over MCP, what a Routine is made of, "
             "what to ask your assistant and one way into each part. Start here.", ""]
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
                f'<p class="summary">{render.inline(lede(page))}</p>\n'
                f"{render.on_this_page(rendered, lookup=lookup)}"
                f"{rendered}\n"
                f"{pager(page, pages)}",
                description=lede(page),
                sidebar=sidebar(pages, page["id"]),
                tabs=tabs(pages, page["id"]),
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
            "section": place_label(page),
            "summary": render.plain(lede(page)),
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
    print(f"✔  {len(pages)} pages → chunks.json, llms.txt ({size:,}B), "
          f"llms-full.txt, search.json ({(BUILD / 'search.json').stat().st_size:,}B), "
          f"index.html, 404.html, robots.txt, sitemap.xml, fonts/, <id>.md + .html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
