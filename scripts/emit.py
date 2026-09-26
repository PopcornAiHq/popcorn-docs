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
    <section>/<id>.md  the plain-Markdown twin of each page, at the path
                     its llms.txt entry advertises
    <section>/<id>.html  the same page for a person with a browser
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
    meta["section"] = path.parent.name
    return meta


# The sections in the order a reader meets them: (directory, label, what the
# section is for). The label heads the section in the sidebar and on its
# Overview card; the blurb is the card's text. The concepts come first: they
# are what every guide and every agent answer points into, so they lead the
# sidebar and the index. A section not listed here still publishes, after
# these, under its directory name.
SECTIONS = [
    ("concepts", "Concepts",
     "One idea each, in reading order: what a bundle holds, then how it ships "
     "and what a publish changes."),
    ("guides", "Guides",
     "Walkthroughs, in reading order. The first is the whole authoring loop; "
     "each later one builds on it."),
    ("glossary", "Glossary",
     "Every term, with its synonyms and the collisions worth knowing."),
    ("reference", "Reference",
     "Generated from the platform itself, never written by hand."),
]

# The sections whose pages a generator writes. llms-full.txt names them
# without inlining them; see the module docstring.
GENERATED = {"reference"}

_KNOWN = [name for name, *_ in SECTIONS]

# Pages the navigation lists under a section other than their directory's.
# Only the navigation moves: the URL is still `<directory>/<id>`, because
# that path is in llms.txt and in other pages' links, and an id is permanent
# by contract, which is what makes naming one here safe.
NAV_SECTION = {"glossary": "glossary"}


def nav_section(page: dict) -> str:
    return NAV_SECTION.get(page["id"], page["section"])


def href(page: dict, suffix: str = ".html") -> str:
    return f"/{page['section']}/{page['id']}{suffix}"


def url(page: dict | None) -> str:
    """A page's canonical address — the one the sitemap lists. None is the home page."""
    return f"{SITE}/" if page is None else f"{SITE}{href(page)}"


def section_info(section: str) -> tuple[str, str]:
    for name, label, blurb in SECTIONS:
        if name == section:
            return label, blurb
    return section.title(), ""


def reading_order(page: dict) -> tuple:
    """Section first, then the page's `order:`, then its title.

    `order:` is what makes a reading path: filenames sort alphabetically,
    which put an advanced guide ahead of the one it builds on. A page with
    no `order:` goes after the ordered ones in its section.
    """
    section = nav_section(page)
    rank = _KNOWN.index(section) if section in _KNOWN else len(_KNOWN)
    order = page.get("order")
    return (rank, section, order is None, order or 0, page["title"].lower())


def sidebar(pages: list[dict], current: str | None) -> str:
    """The site sidebar: sections in reading order, then `group:` within them.

    A group sits where its first page does, so groups follow the reading
    order rather than needing an order of their own; pages without a group
    sit directly under their section.
    """
    sections: dict[str, dict[str, list]] = {}
    for page in pages:
        groups = sections.setdefault(nav_section(page), {})
        groups.setdefault(page.get("group", ""), []).append(
            (render.inline(page["title"]), href(page), page["id"] == current)
        )
    # The home page leads the sidebar, current when no page is — `current`
    # is None only when the landing page is the one being built.
    home = (None, [("", [("Overview", "/", current is None)])])
    return render.site_nav([home] + [
        (section_info(section)[0], list(groups.items()))
        for section, groups in sections.items()
    ])


def landing(pages: list[dict]) -> str:
    """The home page: what Popcorn is, what these pages cover, one way in each.

    It does not list every page — the sidebar beside it already does. Each
    section gets a card that opens its first page in reading order, so the
    way in follows `order:` rather than being chosen again here.
    """
    first: dict[str, dict] = {}
    for page in pages:
        first.setdefault(nav_section(page), page)
    cards = []
    for section, page in first.items():
        label, blurb = section_info(section)
        cards.append(
            f'<a class="card" id="{section}" href="{href(page)}">'
            f'<span class="card-label">{label}</span>'
            f"<p>{blurb}</p>"
            f'<span class="card-start">{render.inline(page["title"])} \u2192</span></a>'
        )
    return render.document(
        "Overview — Popcorn docs",
        "<h1>Overview</h1>\n"
        '<p class="summary">Popcorn is an AI tracker. Each channel is a tracker '
        "that updates itself, reading across email, messages and files, and an "
        "<strong>app bundle</strong> defines what it tracks: its tables, the flows "
        "that update them, and the schedules and webhooks that bring an update in "
        "without anyone typing.</p>\n"
        "<p>These pages are for whoever authors, publishes or operates a bundle — "
        "a person or an agent. The first guide walks the whole loop once; the "
        "concepts are where to go when something behaves in a way you did not "
        "expect.</p>\n"
        '<div class="cards">' + "".join(cards) + "</div>\n"
        "<h2>For agents</h2>\n"
        "<p>Every page has a Markdown twin at the same path, ending "
        "<code>.md</code> instead of <code>.html</code>. "
        '<a href="/llms.txt">/llms.txt</a> lists every page with its summary, '
        '<a href="/llms-full.txt">/llms-full.txt</a> holds every written page in '
        "full and names the generated reference pages, and "
        '<a href="/chunks.json">/chunks.json</a> has one record per page.</p>',
        description="How Popcorn app bundles work: tables, flows, schedules and "
        "webhooks, and what happens when you publish.",
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
    """The release a generated page describes, beside its title.

    Only a page whose generator records a `version:` gets one — the CLI
    reference, which describes one `popcorn` release and would otherwise
    mention it only mid-sentence.
    """
    if not page.get("version"):
        return ""
    return f'<span class="version-badge" title="Generated from this release">v{page["version"]}</span>'


def eyebrow(page: dict) -> str:
    """Where the page sits: its section, and its group when it has one.

    Omitted when the section is the page itself — "Glossary" over "Glossary".
    """
    section = nav_section(page)
    label = section_info(section)[0]
    if label == page["title"]:
        return ""
    trail = f'<a href="/#{section}">{label}</a>'
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

    (BUILD / "chunks.json").write_text(
        json.dumps({"site": SITE, "pages": pages}, indent=2) + "\n"
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
        path = f"{page['section']}/{page['id']}.md"
        index += [f"## {page['title']}", f"{SITE}/{path}", "", page["summary"], ""]
        if page["section"] in GENERATED:
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
            )
        )

        search.append({
            "title": render.plain(page["title"]),
            "url": href(page),
            "section": section_info(nav_section(page))[0],
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
    sections = ", ".join(sorted({f"{p['section']}/" for p in pages}))
    print(f"✔  {len(pages)} pages → chunks.json, llms.txt ({size:,}B), "
          f"llms-full.txt, search.json ({(BUILD / 'search.json').stat().st_size:,}B), "
          f"index.html, 404.html, robots.txt, sitemap.xml, fonts/, {sections}(.md + .html)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
