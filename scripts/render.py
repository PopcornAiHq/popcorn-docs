#!/usr/bin/env python3
"""The Markdown subset the concepts use, rendered to a standalone HTML page.

Not a Markdown implementation. It covers the constructs that appear in
`content/`, the same way `emit.parse` covers only the frontmatter shapes
`content/_frontmatter.md` documents: headings, paragraphs, bullet lists,
tables, fenced and indented code, and inline code, bold and italic. A page
that reaches for anything else renders as literal text, which is visible in
review rather than silently wrong.

A dependency-free renderer is the point. Everything else in `scripts/` runs
on a bare interpreter, so the site build does too — no toolchain to install,
nothing to pin, and a contributor with python3 can see their page.

The CSS is inlined into every page rather than shared. The corpus is small
and each page is a few KB, so a second request to fetch a stylesheet costs
more than the duplication does, and it keeps a page that someone saves or
pipes through a reader self-contained.

The fonts are served from this site, not a font CDN: Inter for text and
JetBrains Mono for code, committed under `assets/fonts/` with their licences
and copied into the build. A third-party request on every page view tells
that party who is reading, and Google Fonts' copy of Inter drops the
character variants the body text asks for (`cv11`, `ss01`), so those settings
did nothing. Each file is the project's own variable release cut down with
fontTools — `varLib.instancer` to the weight range the CSS uses and Inter's
text optical size, then `pyftsubset` to Latin plus the arrows, keeping every
layout feature. The files are named for their upstream version and served
with a long cache lifetime, so a replacement takes a new name rather than
overwriting one a browser has cached. Both stacks still fall back to the
system's own faces, so a font that fails to load costs the typeface and
nothing else.
"""

from __future__ import annotations

import html
import re

import highlight

_FENCE = re.compile(r"^```")
_RULE = re.compile(r"^-{3,}\s*$")
_QUOTE = re.compile(r"^>\s?(?P<text>.*)$")
_ORDERED = re.compile(r"^\d+\.\s+(?P<text>.+)$")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_HEADING = re.compile(r"^(?P<level>#{2,4})\s+(?P<text>.+)$")
_BULLET = re.compile(r"^[-*]\s+(?P<text>.+)$")
_TABLE_SEP = re.compile(r"^\|?[\s:|-]+\|[\s:|-]*$")
_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_TERM = re.compile(r"^\*\*([^*]+)\*\*")

SITE = "https://docs.popcorn.ai"
SOURCE = "https://github.com/PopcornAiHq/popcorn-docs"
# A link to one of this site's pages, as the Markdown writes it: absolute and
# ending `.md`, because the Markdown twin is what an agent follows.
_PAGE = re.compile(r"^(?:" + re.escape(SITE) + r")?(?P<path>/[\w/-]+)\.md(?P<frag>#[\w-]*)?$")


def _href(url: str) -> str:
    """Where a link in a page body should go in the HTML rendering.

    A person reading the HTML should land on the HTML twin, not the Markdown
    one, so a link to this site's `.md` becomes the root-relative `.html` at
    the same path. Root-relative, so it also works on a local build — and
    `check-links.py`, which skips absolute URLs, checks it. Anything else,
    including a `.md` on another host, is left as written.
    """
    page = _PAGE.match(url)
    if not page:
        return url
    return page.group("path") + ".html" + (page.group("frag") or "")


def inline(text: str) -> str:
    """Escape, then apply the three inline marks. Code wins over the others."""
    out = html.escape(text, quote=False)
    # Code spans are extracted first so that a * inside one is not styled.
    # They are NOT escaped again here: the whole string was escaped above, so
    # a second pass turns `<name>` into a literal &lt;name&gt; on the page.
    spans: list[str] = []

    def stash(match: re.Match) -> str:
        spans.append(match.group(1))
        return f"\x00{len(spans) - 1}\x00"

    out = _CODE.sub(stash, out)
    out = _LINK.sub(
        lambda m: f'<a href="{_href(m.group(2)).replace(chr(34), "&quot;")}">{m.group(1)}</a>',
        out,
    )
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _ITALIC.sub(r"<em>\1</em>", out)
    for i, span in enumerate(spans):
        out = out.replace(f"\x00{i}\x00", f"<code>{span}</code>")
    return out


def _continues(line: str) -> bool:
    """Is this line the wrapped remainder of the list item above it?

    Any indented, non-blank, non-fence line is. The four-space rule that means
    "code block" in open prose does not apply inside a list: markdown wants
    code indented past the item's own text, and an item numbered in double
    digits already puts its continuation at four. Treating those as code broke
    a twenty-one item list into three, each restarting at 1.
    """
    return bool(line.strip()) and line[0] in " \t" and not _FENCE.match(line.strip())


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


_TAG = re.compile(r"<[^>]+>")
_H2 = re.compile(r'<h2 id="(?P<id>[^"]+)">(?P<html>.*?)<a class="anchor"')


def _slug(text: str, seen: set[str]) -> str:
    """A heading's anchor: stable for as long as its wording is, unique per page.

    Derived from the words rather than numbered, so a link to a section
    survives a section being added above it.
    """
    base = re.sub(r"[^a-z0-9]+", "-", _TAG.sub("", inline(text)).lower()).strip("-")
    base = base or "section"
    anchor, n = base, 2
    while anchor in seen:
        anchor, n = f"{base}-{n}", n + 1
    seen.add(anchor)
    return anchor


def _toc_nav(rendered: str, minimum: int, title: str) -> str:
    """The page's second-level headings as a list, under an optional title."""
    entries = _H2.findall(rendered)
    if len(entries) < minimum:
        return ""
    items = "".join(f'<li><a href="#{a}">{h}</a></li>' for a, h in entries)
    return f'<nav class="toc spy" aria-label="On this page">{title}<ol>{items}</ol></nav>'


def toc(rendered: str, minimum: int = 2) -> str:
    """"On this page" for the right rail: the page's second-level headings.

    The rail sits beside the text rather than above it, so a short list costs
    the reader nothing; only a page with a single heading has nothing to
    navigate between.
    """
    return _toc_nav(rendered, minimum, '<p class="rail-title">On this page</p>')


_ENTRY = re.compile(
    r'<h(?P<level>[23]) id="(?P<id>[^"]+)">(?P<html>.*?)<a class="anchor"'
    r'|<li id="(?P<term_id>[^"]+)"><strong>(?P<term>.*?)</strong>'
)


def _lookup_entries(rendered: str) -> str:
    """A lookup page's entries and the filter over them.

    Built from the rendered page rather than the Markdown, so an entry is
    listed exactly when it has an anchor to link to. Second-level headings are
    the groups; third-level headings and glossary terms are the entries. An
    entry that repeats its group's name as a prefix — `foundation.agent.invoke`
    under `foundation.agent` — is listed by the part that differs, which is
    what fits in the rail.
    """
    groups: list[tuple[str, str, list[tuple[str, str, str]]]] = []
    for m in _ENTRY.finditer(rendered):
        if m.group("level") == "2":
            groups.append((m.group("id"), _TAG.sub("", m.group("html")), []))
            continue
        anchor = m.group("id") or m.group("term_id")
        name = _TAG.sub("", m.group("html") or m.group("term"))
        if not groups:
            groups.append(("", "", []))
        prefix = groups[-1][1] + "."
        label = name[len(prefix):] if name.startswith(prefix) else name
        groups[-1][2].append((anchor, name, label))

    blocks = []
    for anchor, heading, entries in groups:
        items = "".join(
            f'<li data-name="{html.escape(name.lower(), quote=True)}">'
            f'<a href="#{a}">{label}</a></li>'
            for a, name, label in entries
        )
        if not heading:
            blocks.append(f"<ul>{items}</ul>")
            continue
        blocks.append(
            f'<details open data-name="{html.escape(heading.lower(), quote=True)}">'
            f'<summary><a href="#{anchor}">{heading}</a></summary><ul>{items}</ul></details>'
        )
    return (
        '<input class="filter" type="search" placeholder="Filter\u2026" '
        'aria-label="Filter this page\'s entries" hidden>'
        '<nav class="lookup spy" aria-label="Entries">' + "".join(blocks) + "</nav>"
    )


def lookup_index(rendered: str) -> str:
    """"On this page" for a lookup page: every entry, filterable.

    It takes the rail's place for the contents list, and the site sidebar
    stays on the left, so a reader looking a term up can still see where the
    page sits and leave it in one click.
    """
    return '<p class="rail-title">On this page</p>' + _lookup_entries(rendered)


def on_this_page(rendered: str, *, lookup: bool) -> str:
    """The rail's contents list again, collapsed above the page's text.

    Below the width that fits a rail, the rail's list is hidden and only its
    related pages follow the page, which left no way to move within a page on
    a laptop or a phone. This is that list, shown only at those widths.

    It is a second copy rather than the rail's own list moved into place. The
    page and the rail are each one cell of the layout grid, so no rule can
    lift the rail's list in between the page's summary and its text — only
    above or below the whole page. The copy repeats markup already on the
    page, which compression all but erases, and the rail stays exactly what
    it was on a wide screen.

    A native <details>, so it opens without JavaScript and starts collapsed:
    the text is what the reader came for, and the list is one tap away.
    """
    contents = _lookup_entries(rendered) if lookup else _toc_nav(rendered, 2, "")
    if not contents:
        return ""
    return (
        '<details class="on-page"><summary>On this page</summary>'
        f'<div class="on-page-body">{contents}</div></details>\n'
    )


def plain(text: str) -> str:
    """A line of the Markdown subset as the reader sees it: no marks, no tags."""
    return html.unescape(_TAG.sub("", inline(text)))


def search_entries(rendered: str) -> list[list[str]]:
    """Every place in a page that search can land on: [text, anchor] pairs.

    The same anchors the contents lists are built from — second- and
    third-level headings, and on the glossary each term — because on a lookup
    page the entry names are exactly what a reader types into search, and a
    hit on one should open the page at it rather than at the top.
    """
    return [
        [html.unescape(_TAG.sub("", m.group("html") or m.group("term"))).strip(),
         m.group("id") or m.group("term_id")]
        for m in _ENTRY.finditer(rendered)
    ]


# (title, href, current) — one link in the site sidebar.
Link = tuple[str, str, bool]


def site_nav(sections: list[tuple[str | None, list[tuple[str, list[Link]]]]]) -> str:
    """The left column: the whole site, in reading order.

    Each section is (label, groups) and each group is (label, links), where an
    empty group label means the links sit directly under the section. A
    section labelled None has no heading at all — the home page's link, which
    belongs to no section.
    """
    def link(title: str, href: str, current: bool) -> str:
        attrs = ' aria-current="page"' if current else ""
        return f'<li><a href="{href}"{attrs}>{title}</a></li>'

    out = []
    for label, groups in sections:
        if label is None:
            out.append("".join(
                f'<ul class="solo">{"".join(link(*l) for l in links)}</ul>' for _, links in groups
            ))
            continue
        parts = [f'<p class="nav-section">{html.escape(label, quote=False)}</p>']
        for group, links in groups:
            items = "".join(link(*l) for l in links)
            if group:
                parts.append(
                    f"<details open><summary>{html.escape(group, quote=False)}</summary>"
                    f"<ul>{items}</ul></details>"
                )
            else:
                parts.append(f"<ul>{items}</ul>")
        out.append("<div>" + "".join(parts) + "</div>")
    return '<nav class="site-nav" aria-label="Docs">' + "".join(out) + "</nav>"


def rail(*, contents: str = "", related: list[Link] = ()) -> str:
    """The right column: where you are in this page, then the pages around it."""
    parts = [contents] if contents else []
    if related:
        items = "".join(f'<li><a href="{href}">{title}</a></li>' for title, href, _ in related)
        parts.append(f'<div class="related"><p class="rail-title">Related</p><ul>{items}</ul></div>')
    return "".join(parts)


_ICON_COPY = (
    '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="5" y="5" width="9" height="9" '
    'rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M11 5V3.5A1.5 1.5 0 0 0 9.5 2h-6A1.5 '
    '1.5 0 0 0 2 3.5v6A1.5 1.5 0 0 0 3.5 11H5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
)
_ICON_CARET = (
    '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true"><path d="M4 6l4 4 4-4" fill="none" '
    'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def page_actions(markdown: str) -> str:
    """What a reader can do with the page's Markdown twin, beside its title.

    Copy is the common case — pasting a page into a model — so it is the
    button; viewing the twin and copying its address sit behind the caret.
    The menu is a native <details>, so it opens without JavaScript. Both
    copies need it, and ship hidden until the script reveals them, which
    leaves a reader without JavaScript a "Markdown" menu holding the link.
    """
    return (
        '<div class="page-actions">'
        f'<button class="copy" type="button" data-src="{markdown}" hidden>{_ICON_COPY}<span>Copy page</span></button>'
        f'<details><summary aria-label="More ways to use this page">'
        f'<span class="no-copy">Markdown</span>{_ICON_CARET}</summary>'
        '<div class="page-menu">'
        f'<a href="{markdown}">View as Markdown</a>'
        f'<button class="copy-link" type="button" data-src="{markdown}" hidden>Copy Markdown link</button>'
        "</div></details></div>"
    )


# Every code block's copy button. It ships hidden and the script reveals it,
# the same as the page's own Copy, so a reader without JavaScript — or without
# a clipboard — never sees a control that cannot work.
_COPY_CODE = (
    '<button class="code-copy" type="button" aria-label="Copy code" hidden>'
    f'{_ICON_COPY}<span class="code-copy-done" aria-live="polite"></span></button>'
)


def code_block(code: str, lang: str = "") -> str:
    """One code block, with its copy button beside it.

    The wrapper is what the button is positioned against. The <pre> itself
    scrolls sideways, and a button inside it would scroll away with the text.
    A YAML block is highlighted here, at build time, so the page needs no
    script to show it; every other language is escaped and nothing more.
    """
    if lang in highlight.LANGUAGES:
        inner = f'<code class="language-yaml">{highlight.yaml(code)}</code>'
    else:
        inner = f"<code>{html.escape(code)}</code>"
    return f'<div class="code"><pre>{inner}</pre>{_COPY_CODE}</div>'


def body(md: str, *, terms: bool = False) -> str:
    """Render a concept body. Block constructs first, inline within them.

    With ``terms``, a bullet that opens with a bold term — a glossary entry —
    gets an anchor named for the term, so the term can be linked to and listed
    in the lookup sidebar.
    """
    seen: set[str] = set()
    lines = md.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if _FENCE.match(line):
            lang = line.strip()[3:].strip().lower()
            i += 1
            code = []
            while i < len(lines) and not _FENCE.match(lines[i]):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            out.append(code_block(chr(10).join(code), lang))
            continue

        # An indented block is code too. Tables and lists are matched first,
        # so this only catches genuine four-space blocks.
        if line.startswith("    "):
            code = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                code.append(lines[i][4:])
                i += 1
            out.append(code_block(chr(10).join(code).strip(chr(10))))
            continue

        heading = _HEADING.match(line)
        if heading:
            level = len(heading.group("level"))
            text = heading.group("text")
            anchor = _slug(text, seen)
            out.append(
                f'<h{level} id="{anchor}">{inline(text)}'
                f'<a class="anchor" href="#{anchor}" aria-label="Link to this section">#</a>'
                f"</h{level}>"
            )
            i += 1
            continue

        if line.lstrip().startswith("|") and i + 1 < len(lines) and _TABLE_SEP.match(lines[i + 1]):
            head = _cells(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(_cells(lines[i]))
                i += 1
            thead = "".join(f"<th>{inline(c)}</th>" for c in head)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        if _RULE.match(line):
            out.append("<hr>")
            i += 1
            continue

        # A quote's contents are rendered as a body of their own: these carry
        # whole paragraphs and lists, not one styled sentence. The markers are
        # stripped first, so the recursion cannot re-enter this branch.
        if _QUOTE.match(line):
            inner = []
            while i < len(lines) and _QUOTE.match(lines[i]):
                inner.append(_QUOTE.match(lines[i]).group("text"))
                i += 1
            out.append(f"<blockquote>{body(chr(10).join(inner))}</blockquote>")
            continue

        if _ORDERED.match(line):
            items: list[str] = []
            while i < len(lines):
                item = _ORDERED.match(lines[i])
                if item:
                    items.append(item.group("text"))
                    i += 1
                    continue
                if items and _continues(lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
                    continue
                break
            out.append(
                "<ol>" + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ol>"
            )
            continue

        if _BULLET.match(line):
            items: list[str] = []
            while i < len(lines):
                bullet = _BULLET.match(lines[i])
                if bullet:
                    items.append(bullet.group("text"))
                    i += 1
                    continue
                # A wrapped item continues on an indented line. Four spaces is
                # a code block, so only a shallower indent continues the item;
                # without this the tail of a wrapped bullet became its own
                # paragraph, sitting outside the list that owned it.
                if items and _continues(lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
                    continue
                break
            def item(text: str) -> str:
                term = _TERM.match(text) if terms else None
                if term:
                    return f'<li id="{_slug(term.group(1), seen)}">{inline(text)}</li>'
                return f"<li>{inline(text)}</li>"

            out.append("<ul>" + "".join(item(t) for t in items) + "</ul>")
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not (
            _HEADING.match(lines[i])
            or _BULLET.match(lines[i])
            or _FENCE.match(lines[i])
            or lines[i].startswith("    ")
            or lines[i].lstrip().startswith("|")
            or _RULE.match(lines[i])
            or _QUOTE.match(lines[i])
            or _ORDERED.match(lines[i])
        ):
            para.append(lines[i].strip())
            i += 1
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
        else:
            i += 1

    return "\n".join(out)


# The palette follows popcorn.ai: warm paper and near-black ink, cobalt for
# anything a reader can click, and the orange of the site's sun as the brand
# mark. Orange is too light to read as text on paper, so it only ever marks —
# the current heading, a quote's rule, the logo — and never carries words.
#
# The dark palette, declared once and applied two ways: by the OS setting
# unless the reader chose light, and by the reader's choice regardless.
_DARK = """
    --bg: #151412; --fg: #f2eee6; --muted: #a29d93; --rule: #2f2c28;
    --accent: #8ea1ff; --brand: #f26522; --code-bg: #1f1d1a; --wash: #3a2f14; --card: #1c1a18; --edge: #57524a;
    --hl-key: #9fb0ff; --hl-string: #9ccc8a; --hl-literal: #f0a36b; --hl-comment: #8c867c; --hl-anchor: #d6a4e8;
    color-scheme: dark;
"""

# The two typefaces, by the path the build serves them at. emit.py fails the
# build if either is missing, and check-published.py fetches them, so these
# names are what ties the CSS to the files in `assets/fonts/`.
FONT_TEXT = "/fonts/inter-4.1-latin.woff2"
FONT_MONO = "/fonts/jetbrains-mono-2.304-latin.woff2"
FONT_FILES = (FONT_TEXT, FONT_MONO)

# `swap` shows the text in the fallback face at once and changes face when the
# file arrives, rather than holding the page blank for it. The weight ranges
# are the ranges each file was instanced to, so the browser never synthesises
# a weight the file already has.
_CSS = """
@font-face { font-family: "Inter"; font-style: normal; font-weight: 400 700; font-display: swap;
  src: url(""" + FONT_TEXT + """) format("woff2"); }
@font-face { font-family: "JetBrains Mono"; font-style: normal; font-weight: 400 600; font-display: swap;
  src: url(""" + FONT_MONO + """) format("woff2"); }
/* Off-screen until it takes focus, so it costs a sighted mouse user nothing
   and is the first thing a keyboard reader reaches. */
.skip { position: absolute; left: 1rem; top: 0; z-index: 30; padding: .5rem .9rem; border-radius: 0 0 6px 6px;
  background: var(--accent); color: var(--bg); font-weight: 600; text-decoration: none; transform: translateY(-110%); }
.skip:focus { transform: none; outline: 2px solid var(--brand); outline-offset: 2px; }
main:focus { outline: none; }
:root {
  color-scheme: light;
  --bg: #fffdf8; --fg: #1a1a1e; --muted: #6b6760; --rule: #e9e3d6;
  --accent: #1a3de8; --brand: #f26522; --code-bg: #fbf6e8; --wash: #fef3c7; --card: #ffffff; --edge: #1a1a1e;
  --hl-key: #1a3de8; --hl-string: #2e6b1f; --hl-literal: #b3470c; --hl-comment: #6e695f; --hl-anchor: #8a2f9e;
  --font: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --header: 3.25rem;
  /* The header's contents span exactly the columns below them, so both read
     their width from here; each breakpoint redefines it with the grid. */
  --frame: calc(15rem + 44rem + 13rem + 2 * 3rem + 2 * 1.25rem);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {""" + _DARK + """}
}
:root[data-theme="dark"] {""" + _DARK + """}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: var(--font); font-size: 16px; line-height: 1.7;
  font-feature-settings: "cv11", "ss01"; /* Inter's single-storey a and open digits */
  -webkit-text-size-adjust: 100%;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
h1 { font-size: 1.9rem; line-height: 1.2; margin: 0 0 .5rem; letter-spacing: -.02em; }
h2 { font-size: 1.25rem; margin: 2.5rem 0 .75rem; letter-spacing: -.01em; }
h3 { font-size: 1.05rem; margin: 2rem 0 .5rem; }
p { margin: 0 0 1.1rem; }
.summary { color: var(--muted); font-size: 1.1rem; margin-bottom: 2rem; }
code {
  font-family: var(--mono); font-size: .85em; background: var(--code-bg);
  padding: .12em .35em; border-radius: 3px;
}
pre {
  background: var(--code-bg); padding: 1rem; border-radius: 6px;
  overflow-x: auto; font-size: .85rem; line-height: 1.5;
}
pre code { background: none; padding: 0; font-size: inherit; }
/* A code block and its copy button. The button sits over the block's top
   corner rather than beside it, so revealing it moves nothing. */
.code { position: relative; }
.code-copy { position: absolute; top: .45rem; right: .45rem; display: flex; align-items: center; gap: .35rem;
  padding: .3rem .4rem; border: 1px solid var(--rule); border-radius: 5px; background: var(--code-bg);
  color: var(--muted); font: inherit; font-size: .75rem; line-height: 1; cursor: pointer; opacity: 0;
  transition: opacity .12s ease; }
/* The display rule above would otherwise override `hidden`, showing a button
   that cannot copy until the script reveals it. */
.code-copy[hidden] { display: none; }
.code:hover .code-copy, .code-copy:focus-visible, .code-copy.done { opacity: 1; }
.code-copy:hover { color: var(--fg); border-color: var(--muted); }
.code-copy:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
.code-copy-done:empty { display: none; }
/* A touch screen has no hover to reveal the button with. */
@media (hover: none) { .code-copy { opacity: 1; } }
/* YAML, highlighted at build time; the classes are `highlight.py`'s. Keys
   take the link colour's hue and strings a green, so the two things a reader
   scans a block for differ in hue as well as in weight. */
.language-yaml .k { color: var(--hl-key); }
.language-yaml .s { color: var(--hl-string); }
.language-yaml .n { color: var(--hl-literal); }
.language-yaml .c { color: var(--hl-comment); font-style: italic; }
.language-yaml .a { color: var(--hl-anchor); }
.language-yaml .p { color: var(--muted); }
table { border-collapse: collapse; width: 100%; margin: 0 0 1.4rem; font-size: .93rem; display: block; overflow-x: auto; }
th, td { text-align: left; padding: .5rem .7rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
th { font-weight: 600; }
ul { margin: 0 0 1.1rem; padding-left: 1.3rem; }
li { margin-bottom: .4rem; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 3rem 0; }
/* The home page's way in, one card per section. The hard offset shadow is
   popcorn.ai's card treatment, scaled down for a page of text. */
.cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.25rem; margin: 2.25rem 0 3rem; }
.card { display: flex; flex-direction: column; gap: .45rem; padding: 1.1rem 1.25rem 1rem;
  border: 1px solid var(--edge); border-radius: 10px; background: var(--card); color: var(--fg);
  text-decoration: none; box-shadow: 4px 4px 0 var(--edge); transition: transform .12s ease, box-shadow .12s ease; }
.card:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 var(--edge); }
.card-label { font-size: .75rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; }
.card p { flex: 1; margin: 0; color: var(--muted); font-size: .95rem; line-height: 1.5; }
.card-start { color: var(--accent); font-weight: 600; font-size: .93rem; }
@media (max-width: 40rem) { .cards { grid-template-columns: minmax(0, 1fr); } }

/* The frame: a header across the top, then sidebar | page | rail. */
.site { position: sticky; top: 0; z-index: 10; height: var(--header);
  background: var(--bg); border-bottom: 1px solid var(--rule); font-size: .92rem; }
.bar { display: flex; align-items: center; gap: 1rem; height: 100%; max-width: var(--frame);
  margin: 0 auto; padding: 0 1.25rem; }
.site a { text-decoration: none; }
/* Inset like the sidebar's links, so the name lines up with the text under it. */
.site .brand { display: flex; align-items: center; gap: .5rem; padding-left: .6rem;
  color: var(--fg); font-weight: 650; letter-spacing: -.01em; margin-right: auto; }
.mark { width: .85rem; height: .85rem; border-radius: 50%; background: var(--brand); }
.site nav a { color: var(--muted); }
.site nav a:hover, .site .brand:hover { color: var(--accent); }
.theme, .menu { margin-left: 1rem; padding: 0 .2rem; border: 0; background: none; color: var(--muted);
  font: inherit; font-size: 1rem; line-height: 1; cursor: pointer; }
.theme:hover, .menu:hover { color: var(--accent); }
.menu { display: none; margin: 0; font-size: 1.2rem; }
.layout { display: grid; grid-template-columns: 15rem minmax(0, 44rem) 13rem; gap: 3rem;
  max-width: var(--frame); margin: 0 auto; padding: 0 1.25rem; }
main { min-width: 0; padding: 2.5rem 0 4rem; }
/* The footer is a cell of the grid, under the page's column, so at the widths
   where the rail drops below the page it follows the rail rather than
   landing between the page and the rail's links. */
.site-footer { grid-column: 2; display: flex; flex-wrap: wrap; justify-content: space-between; gap: .5rem 1.5rem;
  padding: 1.25rem 0 3rem; border-top: 1px solid var(--rule); color: var(--muted); font-size: .85rem; }
.site-footer span:last-child { display: flex; gap: 1.25rem; }
.site-footer a { color: var(--muted); text-decoration: none; }
.site-footer a:hover { color: var(--accent); }
.sidebar, .rail { position: sticky; top: var(--header); align-self: start;
  max-height: calc(100vh - var(--header)); overflow-y: auto; padding: 2rem 0 3rem; font-size: .9rem; line-height: 1.45; }
/* The right padding keeps the filter's border and the current link's fill off
   the scroll edge, where macOS draws its overlay scrollbar on top of them. */
.sidebar, .rail { padding-right: .75rem; }
.sidebar ul, .rail ul, .rail ol { list-style: none; margin: 0; padding: 0; }
.sidebar li, .rail li { margin: 0; }
.sidebar a { display: block; padding: .3rem .6rem; border-radius: 5px; color: var(--muted); text-decoration: none; }
.sidebar a:hover { color: var(--fg); }
.sidebar a[aria-current="page"], .sidebar a.current { color: var(--accent); background: var(--code-bg);
  font-weight: 600; box-shadow: inset 2px 0 0 var(--brand); }
.nav-section { margin: 1.5rem 0 .35rem .6rem; font-size: .75rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .08em; color: var(--fg); }
.site-nav > :first-child .nav-section { margin-top: 0; }
.solo { margin-top: 1.25rem !important; }
.site-nav > .solo:first-child { margin-top: 0 !important; }
.sidebar details { margin: .2rem 0 .4rem; }
.sidebar summary { padding: .3rem .6rem; cursor: pointer; color: var(--fg); font-weight: 500; list-style-position: inside; }
.sidebar details ul { padding-left: .8rem; }
.filter { display: block; width: 100%; margin: 0 0 1rem; box-sizing: border-box; padding: .45rem .6rem; font: inherit; color: var(--fg);
  background: var(--bg); border: 1px solid var(--rule); border-radius: 6px; }
/* The display rule above would otherwise override `hidden`, showing a filter
   that does nothing until the script reveals it. */
.filter[hidden] { display: none; }
.filter:focus { outline: none; border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
.lookup details { margin: 0 0 .5rem; }
.lookup summary { padding: .2rem 0; cursor: pointer; font-family: var(--mono); font-size: .78rem; }
.lookup summary a { color: var(--fg); }
.lookup li a { font-family: var(--mono); font-size: .78rem; overflow-wrap: anywhere; }
.rail-title { margin: 0 0 .5rem; font-size: .75rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .08em; color: var(--fg); }
.rail a { color: var(--muted); text-decoration: none; }
.rail a:hover { color: var(--accent); }
.toc li a, .lookup li a { display: block; padding: .2rem 0 .2rem .75rem; border-left: 2px solid var(--rule); }
.toc li a.current, .lookup li a.current { color: var(--fg); border-left-color: var(--brand); }
.related { margin-top: 1.75rem; }
.related:first-child { margin-top: 0; }

/* "On this page" above the text: only at the widths where the rail's list is
   hidden, so the two are never on screen together. */
.on-page { display: none; margin: 0 0 2rem; border: 1px solid var(--rule); border-radius: 8px;
  font-size: .9rem; line-height: 1.45; }
.on-page > summary { display: flex; align-items: center; justify-content: space-between; padding: .6rem .85rem;
  list-style: none; cursor: pointer; font-size: .75rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .08em; color: var(--fg); }
.on-page > summary::-webkit-details-marker { display: none; }
.on-page > summary::after { content: ""; width: .4rem; height: .4rem; margin: 0 .2rem .2rem 0;
  border-right: 1.5px solid var(--muted); border-bottom: 1.5px solid var(--muted); transform: rotate(45deg); }
.on-page[open] > summary::after { margin: .2rem .2rem 0 0; transform: rotate(-135deg); }
/* A lookup page lists every entry, which on a phone is several screens; the
   list scrolls inside its box so the text stays a short scroll away. */
.on-page-body { max-height: min(60vh, 30rem); overflow-y: auto; padding: .75rem .85rem .85rem;
  border-top: 1px solid var(--rule); }
.on-page ul, .on-page ol { list-style: none; margin: 0; padding: 0; }
.on-page li { margin: 0; }
.on-page a { color: var(--muted); text-decoration: none; }
.on-page a:hover { color: var(--accent); }

/* Search: a button in the header, and the dialog it opens. */
.search-open { display: flex; align-items: center; gap: .5rem; min-width: 13rem; padding: .3rem .45rem .3rem .6rem;
  border: 1px solid var(--rule); border-radius: 7px; background: var(--bg); color: var(--muted);
  font: inherit; font-size: .85rem; line-height: 1.4; cursor: pointer; }
.search-open:hover { color: var(--fg); border-color: var(--muted); }
/* The display rule above would otherwise override `hidden`, and search needs
   the script. */
.search-open[hidden] { display: none; }
.search-open kbd, .search-field kbd { margin-left: auto; padding: .05rem .35rem; border: 1px solid var(--rule);
  border-radius: 4px; background: var(--code-bg); font-family: var(--mono); font-size: .7rem; color: var(--muted); }
html:has(.search[open]) { overflow: hidden; }
.search { width: min(40rem, calc(100vw - 2rem)); max-height: min(36rem, calc(100vh - 8rem)); margin: 10vh auto auto;
  padding: 0; border: 1px solid var(--rule); border-radius: 12px; background: var(--card); color: var(--fg);
  box-shadow: 0 18px 50px rgba(0, 0, 0, .22); overflow: hidden; }
.search[open] { display: flex; flex-direction: column; }
.search::backdrop { background: rgba(20, 18, 16, .45); }
.search-field { display: flex; align-items: center; gap: .65rem; padding: .8rem 1rem; border-bottom: 1px solid var(--rule);
  color: var(--muted); }
.search-field input { flex: 1; min-width: 0; padding: 0; border: 0; outline: none; background: none;
  font: inherit; font-size: 1.05rem; color: var(--fg); }
.search-field input::-webkit-search-cancel-button { display: none; }
.search-status { margin: 0; padding: 1rem 1.1rem; color: var(--muted); font-size: .9rem; }
.search-status[hidden] { display: none; }
.search-results { flex: 1; overflow-y: auto; list-style: none; margin: 0; padding: .4rem; }
.search-results:empty { display: none; }
.search-results li { margin: 0; }
.search-results a { display: block; padding: .55rem .75rem; border-radius: 7px; color: var(--fg); text-decoration: none;
  line-height: 1.4; }
.search-results [aria-selected="true"] a { background: var(--code-bg); box-shadow: inset 2px 0 0 var(--brand); }
.search-results .hit-title { font-weight: 600; }
.search-results .hit-section { margin-left: .5rem; font-size: .72rem; font-weight: 500; text-transform: uppercase;
  letter-spacing: .06em; color: var(--muted); }
.search-results .hit-heading { display: block; margin-top: .1rem; color: var(--accent); font-size: .9rem; }
.search-results .hit-summary { display: -webkit-box; margin-top: .15rem; overflow: hidden; color: var(--muted);
  font-size: .84rem; -webkit-box-orient: vertical; -webkit-line-clamp: 2; }
/* A page with entries under it is already explained by them; one line of its
   summary is enough context. */
.search-results .hit-page:has(+ .hit-entry) .hit-summary { -webkit-line-clamp: 1; }
/* A page's entries hang under it, indented on a rule, and each page after
   the first starts a new group. */
.search-results .hit-page + .hit-page, .search-results .hit-entry + .hit-page { margin-top: .35rem; }
.search-results .hit-entry a { margin-left: .75rem; padding: .3rem .75rem; border-left: 2px solid var(--rule);
  border-radius: 0 7px 7px 0; }
.search-results .hit-entry .hit-heading { margin-top: 0; }
/* The wash alone nearly vanishes on the dark theme's selected row; the brand
   underline carries the mark there, which is the one job orange has. */
.search mark { background: var(--wash); color: inherit; border-radius: 2px; box-shadow: inset 0 -2px 0 var(--brand); }

/* The title row: the page's name, and the one control for its Markdown twin. */
.title-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.title-row .title { display: flex; flex-wrap: wrap; align-items: baseline; gap: .35rem .75rem; min-width: 0; }
.version-badge { padding: .1rem .5rem; border-radius: 999px; background: var(--code-bg); border: 1px solid var(--rule);
  font-family: var(--mono); font-size: .78rem; color: var(--muted); white-space: nowrap; }
.page-actions { position: relative; flex-shrink: 0; display: flex; margin-top: .35rem;
  border: 1px solid var(--rule); border-radius: 7px; background: var(--bg); font-size: .85rem; }
.page-actions button, .page-actions summary { display: flex; align-items: center; gap: .4rem; padding: .35rem .6rem;
  border: 0; background: none; font: inherit; color: var(--muted); cursor: pointer; }
.page-actions button:hover, .page-actions summary:hover, .page-actions details[open] summary { color: var(--fg); }
.page-actions summary { list-style: none; padding: .35rem .5rem; }
/* The display rules above would otherwise override `hidden` on the two copy
   buttons, showing controls that cannot work until the script reveals them. */
.page-actions [hidden] { display: none; }
.page-actions summary::-webkit-details-marker { display: none; }
.page-actions .copy:not([hidden]) + details summary { border-left: 1px solid var(--rule); }
/* With Copy revealed, the caret alone says "more"; without it, the menu
   needs its name. */
.page-actions .copy:not([hidden]) + details .no-copy { display: none; }
.page-menu { position: absolute; right: -1px; top: calc(100% + .35rem); z-index: 5; min-width: 12rem;
  display: grid; padding: .3rem; background: var(--card); border: 1px solid var(--rule); border-radius: 8px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, .08); }
.page-menu a, .page-menu button { display: block; width: 100%; padding: .45rem .6rem; border-radius: 5px; text-align: left;
  color: var(--fg); text-decoration: none; }
.page-menu a:hover, .page-menu button:hover { background: var(--code-bg); color: var(--fg); }
.related li { margin-bottom: .4rem; }

.eyebrow { margin: 0 0 .35rem; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.eyebrow a { color: var(--muted); text-decoration: none; }
.eyebrow a:hover { color: var(--accent); }
.pager { display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem; }
.pager a { flex: 1 1 0; display: block; padding: .8rem 1rem; border: 1px solid var(--rule);
  border-radius: 6px; text-decoration: none; font-weight: 600; }
.pager a:hover { border-color: var(--accent); }
.pager a.next { text-align: right; margin-left: auto; }
.pager span { display: block; font-size: .78rem; font-weight: 400; color: var(--muted);
  text-transform: uppercase; letter-spacing: .06em; margin-bottom: .15rem; }
.anchor { margin-left: .4rem; color: var(--rule); text-decoration: none; font-weight: 400; opacity: 0; }
h2:hover .anchor, h3:hover .anchor, h4:hover .anchor, .anchor:focus { opacity: 1; color: var(--muted); }
[id] { scroll-margin-top: calc(var(--header) + 1.25rem); }
li:target { background: var(--wash); border-radius: 4px; box-shadow: 0 0 0 .4rem var(--wash); }
blockquote { margin: 0 0 1.4rem; padding: .2rem 0 .2rem 1.1rem; border-left: 3px solid var(--brand); color: var(--fg); }
blockquote p:last-child { margin-bottom: 0; }

/* Too narrow for the rail: its contents list goes, and the related pages
   follow the page instead. */
@media (max-width: 72rem) {
  :root { --frame: calc(14rem + 44rem + 2.5rem + 2 * 1.25rem); }
  .layout { grid-template-columns: 14rem minmax(0, 44rem); gap: 2.5rem; }
  .rail { grid-column: 2; position: static; max-height: none; padding: 0 0 2.5rem; margin-top: -1.5rem; }
  .rail .toc, .rail .lookup, .rail .filter, .rail > .rail-title { display: none; }
  .on-page { display: block; }
  .related { padding-top: 1.25rem; border-top: 1px solid var(--rule); }
}
/* Too narrow for the sidebar: it becomes a drawer behind the menu button.
   Only with JavaScript, which is what opens it; without, it stays in the
   flow above the page, where it is at least reachable. */
@media (max-width: 52rem) {
  .bar { padding: 0 1rem; }
  .site .brand { padding-left: 0; }
  .layout { grid-template-columns: minmax(0, 1fr); gap: 0; padding: 0 1rem; }
  .rail, .site-footer { grid-column: 1; }
  .sidebar { position: static; max-height: none; padding: 1.5rem 0 0; }
  html.js .menu { display: inline-block; }
  /* The header has no room for the labelled field: search becomes an icon
     beside the other controls. */
  .search-open { min-width: 0; padding: .2rem; border: 0; background: none; }
  .search-open span, .search-open kbd { display: none; }
  /* align-self is reset because Chrome honours it on a fixed box too: at
     `start`, a list taller than the gap under the header is aligned back
     up over it rather than scrolling inside the drawer. */
  html.js .sidebar { position: fixed; top: var(--header); left: 0; bottom: 0; z-index: 20; align-self: auto;
    width: min(20rem, 85vw); max-height: none; padding: 1.5rem 1rem; background: var(--bg);
    border-right: 1px solid var(--rule); transform: translateX(-100%); visibility: hidden;
    transition: transform .2s ease, visibility .2s; }
  html.js.nav-open .sidebar { transform: none; visibility: visible; }
  main { padding-top: 1.75rem; }
  .search { margin-top: .75rem; max-height: calc(100vh - 1.5rem); }
}
"""


# An emoji favicon, inline: no file to publish, advertise or keep in sync.
_ICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%F0%9F%8D%BF%3C/text%3E%3C/svg%3E"
)


# A reader's explicit theme choice, applied in <head> so the page is never
# painted in the other theme first. Storage can be unavailable (private
# windows, blocked site data); the page then simply follows the OS.
_THEME_EARLY = (
    'document.documentElement.classList.add("js");'
    'try{var t=localStorage.getItem("theme");'
    'if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}'
)

# The page's other behaviour, all optional: without it the drawer stays open
# in the flow, the filter and the copy button stay hidden, and nothing tracks
# where the reader is.
#
# Where-you-are is computed on scroll from the headings' positions rather
# than with an IntersectionObserver: "the last target above the fold line" is
# the definition a reader expects, and an observer reports crossings, which
# lose it when a jump skips several targets at once.
_NAV = """
(function () {
  var root = document.documentElement;
  var menu = document.querySelector(".menu"), sidebar = document.querySelector(".sidebar");
  if (menu && sidebar) {
    menu.addEventListener("click", function () {
      var open = root.classList.toggle("nav-open");
      menu.setAttribute("aria-expanded", open ? "true" : "false");
    });
    sidebar.addEventListener("click", function (e) {
      if (e.target.closest("a")) { root.classList.remove("nav-open"); menu.setAttribute("aria-expanded", "false"); }
    });
  }

  // Copy the page's Markdown, or its address. Each button says what happened
  // for a moment, then goes back to its label.
  function flash(button, text) {
    var label = button.querySelector("span") || button, original = label.textContent;
    label.textContent = text;
    setTimeout(function () { label.textContent = original; }, 1500);
  }
  var copy = document.querySelector(".copy"), copyLink = document.querySelector(".copy-link");
  var menu = document.querySelector(".page-actions details");
  if (navigator.clipboard) {
    if (copy) {
      copy.hidden = false;
      copy.addEventListener("click", function () {
        fetch(copy.dataset.src).then(function (r) { return r.text(); })
          .then(function (t) { return navigator.clipboard.writeText(t); })
          .then(function () { flash(copy, "Copied"); }, function () { flash(copy, "Copy failed"); });
      });
    }
    if (copyLink) {
      copyLink.hidden = false;
      copyLink.addEventListener("click", function () {
        navigator.clipboard.writeText(location.origin + copyLink.dataset.src)
          .then(function () { flash(copyLink, "Link copied"); }, function () { flash(copyLink, "Copy failed"); });
      });
    }
  }
  // Each code block's copy button copies the block's text — the text, not
  // its markup, so a highlighted block pastes exactly as it was written.
  if (navigator.clipboard) {
    document.querySelectorAll(".code-copy").forEach(function (button) {
      var code = button.parentNode.querySelector("code"), done = button.firstElementChild.nextElementSibling, timer;
      button.hidden = false;
      button.addEventListener("click", function () {
        navigator.clipboard.writeText(code.textContent).then(function () { return "Copied"; }, function () { return "Copy failed"; })
          .then(function (text) {
            clearTimeout(timer);
            done.textContent = text;
            button.classList.add("done");
            timer = setTimeout(function () { done.textContent = ""; button.classList.remove("done"); }, 1500);
          });
      });
    });
  }
  // A menu closes the way menus do: a click elsewhere, or Escape.
  if (menu) {
    document.addEventListener("click", function (e) { if (!menu.contains(e.target)) menu.open = false; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") menu.open = false; });
  }

  // Each copy of a lookup index — the rail's, and the one above the text at
  // narrow widths — has its own filter, which narrows only the list beside it.
  document.querySelectorAll(".filter").forEach(function (filter) {
    var scope = filter.parentNode;
    filter.hidden = false;
    filter.addEventListener("input", function () {
      var q = filter.value.trim().toLowerCase();
      scope.querySelectorAll(".lookup details, .lookup > ul").forEach(function (group) {
        var groupHit = !q || (group.dataset.name || "").indexOf(q) !== -1, any = false;
        group.querySelectorAll("li").forEach(function (li) {
          var hit = groupHit || li.dataset.name.indexOf(q) !== -1;
          li.hidden = !hit; any = any || hit;
        });
        group.hidden = !any && !groupHit;
        if (q && group.tagName === "DETAILS") group.open = true;
      });
    });
  });

  // Picking an entry from the list above the text closes it before the jump,
  // so the page lands on the section and not on a list still open over it.
  document.querySelectorAll(".on-page").forEach(function (list) {
    list.addEventListener("click", function (e) { if (e.target.closest("a")) list.open = false; });
  });

  document.querySelectorAll(".spy").forEach(function (nav) {
    var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var scroller = nav.closest(".sidebar, .rail"), shown = null, queued = false;
    function update() {
      queued = false;
      var line = parseFloat(getComputedStyle(root).getPropertyValue("--header")) * 16 + 32, at = -1;
      for (var i = 0; i < targets.length; i++) {
        if (targets[i] && targets[i].getBoundingClientRect().top <= line) at = i;
      }
      var link = links[at] || null;
      if (link === shown) return;
      if (shown) shown.classList.remove("current");
      shown = link;
      if (!link) return;
      link.classList.add("current");
      if (scroller && scroller.scrollHeight > scroller.clientHeight) {
        var top = link.getBoundingClientRect().top - scroller.getBoundingClientRect().top;
        if (top < 0 || top > scroller.clientHeight - 40) scroller.scrollTop += top - scroller.clientHeight / 3;
      }
    }
    addEventListener("scroll", function () { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  });
})();
"""

# The toggle. The button ships hidden and is revealed here, so a reader
# without JavaScript never sees a control that does nothing.
_THEME_TOGGLE = """
(function () {
  var root = document.documentElement, button = document.querySelector(".theme");
  if (!button) return;
  var dark = matchMedia("(prefers-color-scheme: dark)");
  function current() { return root.dataset.theme || (dark.matches ? "dark" : "light"); }
  function label() {
    var isDark = current() === "dark";
    button.textContent = isDark ? "\u2600" : "\u263E";
    button.title = isDark ? "Switch to light mode" : "Switch to dark mode";
    button.setAttribute("aria-label", button.title);
  }
  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
    label();
  });
  dark.addEventListener("change", label);
  button.hidden = false;
  label();
})();
"""

# Search over every page, from `search.json`. The button and the shortcuts
# exist only here, so without JavaScript there is no control that cannot work.
# The index is fetched on the first open rather than with the page: most
# visits never search, and they should not pay for it.
#
# Results are pages, each with the headings or lookup entries in it that
# matched listed underneath, so a page that matches in several places appears
# once. A page ranks by its title first: any title match outranks any match in
# a page's entries, because a page about the thing beats an entry that names
# it — "fork" finds Fork lines before the glossary's "fork". Within each of
# those two bands an exact name beats a name the query starts, which beats a
# word inside a name the query starts, which beats the query anywhere in a
# name. A match only in a summary ranks below every name. Names are compared
# with `_`, `.`, `-` and `/` read as spaces, so `post message` finds
# `post_message` and `agent.invoke` finds `foundation.agent.invoke`.
_SEARCH = """
(function () {
  var button = document.querySelector(".search-open"), dialog = document.querySelector(".search");
  if (!button || !dialog || !dialog.showModal || !window.fetch) return;
  var input = dialog.querySelector("input"), list = dialog.querySelector(".search-results");
  var status = dialog.querySelector(".search-status"), pages = null, loading = null, active = -1;
  if (!/Mac|iPhone|iPad/.test(navigator.platform)) button.querySelector("kbd").textContent = "Ctrl K";
  button.hidden = false;

  function norm(text) { return text.toLowerCase().replace(/[\\s_.\\/-]+/g, " ").trim(); }
  function rank(name, q) {
    var t = norm(name), i = t.indexOf(q);
    if (i < 0) return 0;
    if (t === q) return 4;
    if (i === 0) return 3;
    return t.charAt(i - 1) === " " ? 2 : 1;
  }
  // At most this many entries under one page; the page itself is one more
  // click away and lists the rest.
  var ENTRIES_PER_PAGE = 3;
  function search(raw, q) {
    var hits = [], loose = [];
    // Words are what the reader separated with spaces. `post_message` is one
    // name, not two words, and splitting it would match every page that
    // mentions posting and messages somewhere.
    var words = raw.toLowerCase().split(/\s+/).map(norm);
    pages.forEach(function (page, order) {
      var title = rank(page.title, q);
      var entries = [];
      page.headings.forEach(function (h, at) {
        var r = rank(h[0], q);
        if (r) entries.push({ heading: h, rank: r, at: at });
      });
      entries.sort(function (a, b) { return b.rank - a.rank || a.at - b.at; });
      var score = title ? 100 + title * 10
        : entries.length ? entries[0].rank * 10
        : norm(page.summary).indexOf(q) !== -1 ? 5 : 0;
      if (score) {
        hits.push({ page: page, score: score, order: order, byTitle: title > 0,
                    entries: entries.slice(0, ENTRIES_PER_PAGE) });
      } else if (words.length > 1) {
        var all = norm(page.title + " " + page.summary + " " + page.headings.map(function (h) { return h[0]; }).join(" "));
        if (words.every(function (w) { return all.indexOf(w) !== -1; })) {
          loose.push({ page: page, score: 1, order: order, entries: [] });
        }
      }
    });
    // Several words that appear nowhere as a phrase still find the pages
    // holding every one of them — but only then, since beside a phrase
    // match they are mostly pages that happen to use both words.
    if (!hits.length) hits = loose;
    // Equal scores keep the site's reading order, so ties are predictable.
    return hits.sort(function (a, b) { return b.score - a.score || a.order - b.order; }).slice(0, 20);
  }

  // Marks the first place the query matches, allowing the same separators
  // that `norm` reads as spaces. Text only: nothing from the index is ever
  // parsed as HTML.
  function marked(text, q) {
    var span = document.createElement("span");
    var pattern = q.split(" ").map(function (w) { return w.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&"); })
      .join("[\\\\s_.\\\\/-]+");
    var m = new RegExp(pattern, "i").exec(text);
    if (!m) { span.textContent = text; return span; }
    var mark = document.createElement("mark");
    mark.textContent = m[0];
    span.append(text.slice(0, m.index), mark, text.slice(m.index + m[0].length));
    return span;
  }
  function el(tag, cls, child) {
    var node = document.createElement(tag);
    node.className = cls;
    if (typeof child === "string") node.textContent = child; else node.appendChild(child);
    return node;
  }

  function select(i) {
    var items = list.children;
    if (active >= 0 && items[active]) items[active].setAttribute("aria-selected", "false");
    active = items.length ? (i + items.length) % items.length : -1;
    if (active < 0) { input.removeAttribute("aria-activedescendant"); return; }
    items[active].setAttribute("aria-selected", "true");
    input.setAttribute("aria-activedescendant", items[active].id);
    items[active].scrollIntoView({ block: "nearest" });
  }
  function show(message) { status.textContent = message; status.hidden = !message; }
  function run() {
    var raw = input.value.trim(), q = norm(raw);
    list.textContent = "";
    active = -1;
    if (!pages) return;
    if (!q) { show("Search every page by title, heading or term."); return; }
    var hits = search(raw, q), n = 0;
    show(hits.length ? "" : "Nothing matches \u201c" + raw + "\u201d.");
    // One option per page and one per entry under it, in a single list, so
    // the arrow keys walk the entries as well as the pages.
    function option(cls, href, parts) {
      var a = document.createElement("a"), li = document.createElement("li");
      a.href = href;
      a.tabIndex = -1;
      parts.forEach(function (part) { a.append(part); });
      li.className = cls;
      li.id = "search-hit-" + n++;
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", "false");
      li.append(a);
      list.append(li);
    }
    hits.forEach(function (hit) {
      var head = el("span", "hit-title", marked(hit.page.title, q));
      option("hit-page", hit.page.url, [head, el("span", "hit-section", hit.page.section),
        el("span", "hit-summary", hit.page.summary)]);
      hit.entries.forEach(function (e) {
        option("hit-entry", hit.page.url + "#" + e.heading[1], [el("span", "hit-heading", marked(e.heading[0], q))]);
      });
    });
    // Enter should land where the match is. When the best page matched only
    // through an entry — `post_message` is a tool on the MCP page, not the
    // page — start on that entry rather than on the top of its page.
    select(hits.length && !hits[0].byTitle && hits[0].entries.length ? 1 : 0);
  }

  function open() {
    if (dialog.open) return;
    dialog.showModal();
    input.select();
    if (pages) { run(); return; }
    show("Loading\u2026");
    loading = loading || fetch("/search.json")
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (index) { pages = index.pages; run(); },
            function () { loading = null; show("Search could not load its index. Try again in a moment."); });
  }

  button.addEventListener("click", open);
  input.addEventListener("input", run);
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      select(active + (e.key === "ArrowDown" ? 1 : -1));
    } else if (e.key === "Enter" && active >= 0) {
      e.preventDefault();
      list.children[active].querySelector("a").click();
    }
  });
  list.addEventListener("mousemove", function (e) {
    var li = e.target.closest("li");
    if (li) select(Array.prototype.indexOf.call(list.children, li));
  });
  // A hit on this same page only moves to an anchor, so the dialog has to be
  // closed by hand; on another page it goes with the navigation anyway.
  list.addEventListener("click", function (e) { if (e.target.closest("a")) dialog.close(); });
  // The dialog's own box fills with its contents, so a click that lands on
  // the dialog itself landed on the backdrop around it.
  dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
  document.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && !e.altKey && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (dialog.open) dialog.close(); else open();
      return;
    }
    var t = e.target;
    if (e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey && !dialog.open
        && !(t.closest && t.closest("input, textarea, select, [contenteditable]"))) {
      e.preventDefault();
      open();
    }
  });
})();
"""

_ICON_SEARCH = (
    '<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><circle cx="7" cy="7" r="4.75" fill="none" '
    'stroke="currentColor" stroke-width="1.5"/><path d="M10.5 10.5L14 14" fill="none" stroke="currentColor" '
    'stroke-width="1.5" stroke-linecap="round"/></svg>'
)

# The search dialog. Empty until the script fills it; a closed <dialog> is
# not rendered at all, so without JavaScript it is simply never there.
_SEARCH_DIALOG = (
    '<dialog class="search" aria-label="Search the docs">'
    f'<div class="search-field">{_ICON_SEARCH}'
    '<input type="search" placeholder="Search the docs" aria-label="Search the docs" role="combobox" '
    'aria-controls="search-results" aria-expanded="true" aria-autocomplete="list" autocomplete="off" spellcheck="false">'
    "<kbd>Esc</kbd></div>"
    '<p class="search-status" role="status" hidden></p>'
    '<ul class="search-results" id="search-results" role="listbox" aria-label="Results"></ul>'
    "</dialog>"
)


def document(
    title: str,
    content: str,
    *,
    description: str = "",
    sidebar: str = "",
    rail: str = "",
    url: str = "",
    noindex: bool = False,
) -> str:
    """Wrap rendered content in a standalone page: header, sidebar, page, rail.

    The caller builds both columns, from `site_nav` or `lookup_index` on the
    left and `rail` on the right; an empty one still takes its grid column, so
    the text sits in the same place on every page.

    ``url`` is the page's canonical address, the same one the sitemap lists.
    It becomes `<link rel="canonical">` and the Open Graph URL, which is what
    a chat app or a search engine files the page under whichever way it was
    reached. A page with no single address — the not-found page, served at
    every missing path — passes none, and ``noindex`` keeps it out of search.
    """
    attr = lambda text: html.escape(text, quote=True)
    head = [f'<meta name="description" content="{attr(description)}">'] if description else []
    if noindex:
        head.append('<meta name="robots" content="noindex">')
    if url:
        head.append(f'<link rel="canonical" href="{attr(url)}">')
    # A link pasted into a chat app unfurls from these. There is no og:image:
    # a card image per page would need an image pipeline, and "summary" is
    # the card type that looks deliberate without one.
    head += [
        '<meta property="og:site_name" content="Popcorn docs">',
        f'<meta property="og:title" content="{attr(title)}">',
        f'<meta property="og:type" content="{"website" if url == SITE + "/" else "article"}">',
    ]
    if url:
        head.append(f'<meta property="og:url" content="{attr(url)}">')
    if description:
        head.append(f'<meta property="og:description" content="{attr(description)}">')
    head.append('<meta name="twitter:card" content="summary">')
    meta = "".join(f"\n  {tag}" for tag in head)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title, quote=False)}</title>{meta}
  <link rel="icon" href="{_ICON}">
  <link rel="preload" href="{FONT_TEXT}" as="font" type="font/woff2" crossorigin>
  <style>{_CSS}</style>
  <script>{_THEME_EARLY}</script>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site"><div class="bar">
<button class="menu" type="button" aria-label="Menu" aria-controls="sidebar" aria-expanded="false">\u2630</button>
<a class="brand" href="/"><span class="mark" aria-hidden="true"></span>Popcorn docs</a>
<button class="search-open" type="button" aria-label="Search the docs" aria-keyshortcuts="Meta+K Control+K /" hidden>{_ICON_SEARCH}<span>Search</span><kbd>\u2318K</kbd></button>
<nav><a href="/llms.txt">llms.txt</a>
<button class="theme" type="button" hidden></button>
</nav></div></header>
<div class="layout">
<aside class="sidebar" id="sidebar">{sidebar}</aside>
<main id="content" tabindex="-1">
{content}
</main>
<aside class="rail">{rail}</aside>
<footer class="site-footer"><span>\u00a9 2026 A Dream Inc. | All rights reserved.</span>
<span><a href="https://www.popcorn.ai/">popcorn.ai</a><a href="{SOURCE}">Source on GitHub</a></span></footer>
</div>
{_SEARCH_DIALOG}
<script>{_THEME_TOGGLE}{_NAV}{_SEARCH}</script>
</body>
</html>
"""
