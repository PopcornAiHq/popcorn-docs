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
"""

from __future__ import annotations

import html
import re

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
        lambda m: f'<a href="{m.group(2).replace(chr(34), "&quot;")}">{m.group(1)}</a>',
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


def toc(rendered: str, minimum: int = 2) -> str:
    """"On this page" for the right rail: the page's second-level headings.

    The rail sits beside the text rather than above it, so a short list costs
    the reader nothing; only a page with a single heading has nothing to
    navigate between.
    """
    entries = _H2.findall(rendered)
    if len(entries) < minimum:
        return ""
    items = "".join(f'<li><a href="#{a}">{h}</a></li>' for a, h in entries)
    return (
        '<nav class="toc spy" aria-label="On this page">'
        f'<p class="rail-title">On this page</p><ol>{items}</ol></nav>'
    )


_ENTRY = re.compile(
    r'<h(?P<level>[23]) id="(?P<id>[^"]+)">(?P<html>.*?)<a class="anchor"'
    r'|<li id="(?P<term_id>[^"]+)"><strong>(?P<term>.*?)</strong>'
)


def lookup_index(rendered: str, title: str) -> str:
    """The left column of a lookup page: its own entries, filterable.

    Built from the rendered page rather than the Markdown, so an entry is
    listed exactly when it has an anchor to link to. Second-level headings are
    the groups; third-level headings and glossary terms are the entries. An
    entry that repeats its group's name as a prefix — `foundation.agent.invoke`
    under `foundation.agent` — is listed by the part that differs, which is
    what fits in the column.
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
        '<a class="back" href="/">\u2190 All docs</a>'
        f'<p class="lookup-title">{title}</p>'
        '<input class="filter" type="search" placeholder="Filter\u2026" '
        'aria-label="Filter this page\'s entries" hidden>'
        '<nav class="lookup spy" aria-label="Entries">' + "".join(blocks) + "</nav>"
    )


# (title, href, current) — one link in the site sidebar.
Link = tuple[str, str, bool]


def site_nav(sections: list[tuple[str, list[tuple[str, list[Link]]]]]) -> str:
    """The left column on every other page: the whole site, in reading order.

    Each section is (label, groups) and each group is (label, links), where an
    empty group label means the links sit directly under the section. A
    section holding one ungrouped page of the same name — the glossary — is
    listed as that one link rather than as a heading over itself.
    """
    def link(title: str, href: str, current: bool) -> str:
        attrs = ' aria-current="page"' if current else ""
        return f'<li><a href="{href}"{attrs}>{title}</a></li>'

    out = []
    for label, groups in sections:
        if len(groups) == 1 and not groups[0][0] and len(groups[0][1]) == 1 \
                and _TAG.sub("", groups[0][1][0][0]) == label:
            out.append(f'<ul class="solo">{link(*groups[0][1][0])}</ul>')
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


def rail(*, contents: str = "", markdown: str = "", related: list[Link] = ()) -> str:
    """The right column: where you are in this page, and what to do with it.

    Most concept pages have two or three headings, so the contents list alone
    would leave the column empty on most of the site; the Markdown twin and
    the related pages are what fill it everywhere.
    """
    parts = [contents] if contents else []
    if markdown:
        parts.append(
            '<div class="actions">'
            f'<button class="copy" type="button" data-src="{markdown}" hidden>Copy as Markdown</button>'
            f'<a href="{markdown}">View as Markdown</a></div>'
        )
    if related:
        items = "".join(f'<li><a href="{href}">{title}</a></li>' for title, href, _ in related)
        parts.append(f'<div class="related"><p class="rail-title">Related</p><ul>{items}</ul></div>')
    return "".join(parts)


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
            i += 1
            code = []
            while i < len(lines) and not _FENCE.match(lines[i]):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            out.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
            continue

        # An indented block is code too. Tables and lists are matched first,
        # so this only catches genuine four-space blocks.
        if line.startswith("    "):
            code = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                code.append(lines[i][4:])
                i += 1
            out.append(
                f"<pre><code>{html.escape(chr(10).join(code).strip(chr(10)))}</code></pre>"
            )
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


# The dark palette, declared once and applied two ways: by the OS setting
# unless the reader chose light, and by the reader's choice regardless.
_DARK = """
    --bg: #1a1917; --fg: #e8e4dd; --muted: #9b958c; --rule: #33302c;
    --accent: #f0935f; --code-bg: #232120; color-scheme: dark;
"""

_CSS = """
:root {
  color-scheme: light;
  --bg: #fdfdfc; --fg: #22201d; --muted: #6b665f; --rule: #e4e0d9;
  --accent: #9a3412; --code-bg: #f4f2ee;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --header: 3.25rem;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {""" + _DARK + """}
}
:root[data-theme="dark"] {""" + _DARK + """}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: var(--font); font-size: 17px; line-height: 1.65;
  -webkit-text-size-adjust: 100%;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
h1 { font-size: 1.9rem; line-height: 1.2; margin: 0 0 .5rem; letter-spacing: -.02em; }
h2 { font-size: 1.25rem; margin: 2.5rem 0 .75rem; letter-spacing: -.01em; }
h3 { font-size: 1.05rem; margin: 2rem 0 .5rem; }
p { margin: 0 0 1.1rem; }
.summary { color: var(--muted); font-size: 1.1rem; margin-bottom: 2rem; }
code {
  font-family: var(--mono); font-size: .88em; background: var(--code-bg);
  padding: .12em .35em; border-radius: 3px;
}
pre {
  background: var(--code-bg); padding: 1rem; border-radius: 6px;
  overflow-x: auto; font-size: .85rem; line-height: 1.5;
}
pre code { background: none; padding: 0; font-size: inherit; }
table { border-collapse: collapse; width: 100%; margin: 0 0 1.4rem; font-size: .93rem; display: block; overflow-x: auto; }
th, td { text-align: left; padding: .5rem .7rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
th { font-weight: 600; }
ul { margin: 0 0 1.1rem; padding-left: 1.3rem; }
li { margin-bottom: .4rem; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 3rem 0; }
.index { list-style: none; padding: 0; margin: 2.5rem 0 0; }
.index li { margin-bottom: 1.75rem; }
.index a { font-weight: 600; font-size: 1.08rem; text-decoration: none; }
.index a:hover { text-decoration: underline; }
.index p { color: var(--muted); margin: .3rem 0 0; font-size: .96rem; }
footer { margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--rule); color: var(--muted); font-size: .88rem; }
footer code { font-size: .85em; }

/* The frame: a header across the top, then sidebar | page | rail. */
.site { position: sticky; top: 0; z-index: 10; height: var(--header); display: flex; align-items: center;
  gap: 1rem; padding: 0 1.25rem; background: var(--bg); border-bottom: 1px solid var(--rule); font-size: .92rem; }
.site a { text-decoration: none; }
.site .brand { color: var(--fg); font-weight: 650; letter-spacing: -.01em; margin-right: auto; }
.site nav a { color: var(--muted); }
.site nav a:hover, .site .brand:hover { color: var(--accent); }
.theme, .menu { margin-left: 1rem; padding: 0 .2rem; border: 0; background: none; color: var(--muted);
  font: inherit; font-size: 1rem; line-height: 1; cursor: pointer; }
.theme:hover, .menu:hover { color: var(--accent); }
.menu { display: none; margin: 0; font-size: 1.2rem; }
.layout { display: grid; grid-template-columns: 15rem minmax(0, 44rem) 13rem; gap: 3rem;
  justify-content: center; padding: 0 1.25rem; }
main { min-width: 0; padding: 2.5rem 0 6rem; }
.sidebar, .rail { position: sticky; top: var(--header); align-self: start;
  max-height: calc(100vh - var(--header)); overflow-y: auto; padding: 2rem 0 3rem; font-size: .9rem; line-height: 1.45; }
.sidebar ul, .rail ul, .rail ol { list-style: none; margin: 0; padding: 0; }
.sidebar li, .rail li { margin: 0; }
.sidebar a { display: block; padding: .3rem .6rem; border-radius: 5px; color: var(--muted); text-decoration: none; }
.sidebar a:hover { color: var(--fg); }
.sidebar a[aria-current="page"], .sidebar a.current { color: var(--accent); background: var(--code-bg); font-weight: 600; }
.nav-section { margin: 1.5rem 0 .35rem .6rem; font-size: .75rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .08em; color: var(--fg); }
.site-nav > :first-child .nav-section { margin-top: 0; }
.solo { margin-top: 1.25rem !important; }
.sidebar details { margin: .2rem 0 .4rem; }
.sidebar summary { padding: .3rem .6rem; cursor: pointer; color: var(--fg); font-weight: 500; list-style-position: inside; }
.sidebar details ul { padding-left: .8rem; }
.back { font-size: .85rem; margin-bottom: .75rem; }
.lookup-title { margin: 0 .6rem .6rem; font-weight: 650; }
.filter { display: block; width: 100%; margin: 0 0 1rem; padding: .45rem .6rem; font: inherit; color: var(--fg);
  background: var(--bg); border: 1px solid var(--rule); border-radius: 6px; }
.filter:focus { outline: 2px solid var(--accent); outline-offset: -1px; }
.lookup summary a { display: inline; padding: 0; color: var(--fg); }
.lookup a { font-family: var(--mono); font-size: .82rem; padding: .2rem .6rem; }
.lookup summary { font-family: var(--mono); font-size: .82rem; }
.rail-title { margin: 0 0 .5rem; font-size: .75rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .08em; color: var(--fg); }
.rail a { color: var(--muted); text-decoration: none; }
.rail a:hover { color: var(--accent); }
.toc li a { display: block; padding: .2rem 0 .2rem .75rem; border-left: 2px solid var(--rule); }
.toc li a.current { color: var(--accent); border-left-color: var(--accent); }
.actions { margin: 1.75rem 0; padding-top: 1.25rem; border-top: 1px solid var(--rule); display: grid; gap: .5rem; justify-items: start; }
.actions:first-child { margin-top: 0; padding-top: 0; border-top: 0; }
.copy { padding: 0; border: 0; background: none; font: inherit; color: var(--muted); cursor: pointer; }
.copy:hover { color: var(--accent); }
.related li { margin-bottom: .4rem; }

.eyebrow { margin: 0 0 .35rem; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.eyebrow a { color: var(--muted); text-decoration: none; }
.eyebrow a:hover { color: var(--accent); }
.section-intro { color: var(--muted); margin: .4rem 0 0; font-size: .95rem; }
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
li:target { background: var(--code-bg); border-radius: 4px; box-shadow: 0 0 0 .4rem var(--code-bg); }
blockquote { margin: 0 0 1.4rem; padding: .2rem 0 .2rem 1.1rem; border-left: 3px solid var(--accent); color: var(--fg); }
blockquote p:last-child { margin-bottom: 0; }
.section-title { font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin: 3rem 0 0; font-weight: 600; }

/* Too narrow for the rail: its contents list goes, and the Markdown links
   and related pages follow the page instead. */
@media (max-width: 72rem) {
  .layout { grid-template-columns: 14rem minmax(0, 44rem); gap: 2.5rem; }
  .rail { grid-column: 2; position: static; max-height: none; padding: 0 0 4rem; margin-top: -3rem; }
  .rail .toc { display: none; }
  .actions:first-child { padding-top: 1.25rem; border-top: 1px solid var(--rule); }
}
/* Too narrow for the sidebar: it becomes a drawer behind the menu button.
   Only with JavaScript, which is what opens it; without, it stays in the
   flow above the page, where it is at least reachable. */
@media (max-width: 52rem) {
  body { font-size: 16px; }
  .site { padding: 0 1rem; }
  .layout { grid-template-columns: minmax(0, 1fr); gap: 0; padding: 0 1rem; }
  .rail { grid-column: 1; }
  .sidebar { position: static; max-height: none; padding: 1.5rem 0 0; }
  html.js .menu { display: inline-block; }
  /* align-self is reset because Chrome honours it on a fixed box too: at
     `start`, a list taller than the gap under the header is aligned back
     up over it rather than scrolling inside the drawer. */
  html.js .sidebar { position: fixed; top: var(--header); left: 0; bottom: 0; z-index: 20; align-self: auto;
    width: min(20rem, 85vw); max-height: none; padding: 1.5rem 1rem; background: var(--bg);
    border-right: 1px solid var(--rule); transform: translateX(-100%); visibility: hidden;
    transition: transform .2s ease, visibility .2s; }
  html.js.nav-open .sidebar { transform: none; visibility: visible; }
  main { padding-top: 1.75rem; }
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

  var copy = document.querySelector(".copy");
  if (copy && navigator.clipboard) {
    copy.hidden = false;
    copy.addEventListener("click", function () {
      fetch(copy.dataset.src).then(function (r) { return r.text(); })
        .then(function (t) { return navigator.clipboard.writeText(t); })
        .then(function () { copy.textContent = "Copied"; },
              function () { copy.textContent = "Copy failed"; })
        .then(function () { setTimeout(function () { copy.textContent = "Copy as Markdown"; }, 1500); });
    });
  }

  var filter = document.querySelector(".filter");
  if (filter) {
    filter.hidden = false;
    filter.addEventListener("input", function () {
      var q = filter.value.trim().toLowerCase();
      document.querySelectorAll(".lookup details, .lookup > ul").forEach(function (group) {
        var groupHit = !q || (group.dataset.name || "").indexOf(q) !== -1, any = false;
        group.querySelectorAll("li").forEach(function (li) {
          var hit = groupHit || li.dataset.name.indexOf(q) !== -1;
          li.hidden = !hit; any = any || hit;
        });
        group.hidden = !any && !groupHit;
        if (q && group.tagName === "DETAILS") group.open = true;
      });
    });
  }

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


def document(
    title: str,
    content: str,
    *,
    description: str = "",
    sidebar: str = "",
    rail: str = "",
) -> str:
    """Wrap rendered content in a standalone page: header, sidebar, page, rail.

    The caller builds both columns, from `site_nav` or `lookup_index` on the
    left and `rail` on the right; an empty one still takes its grid column, so
    the text sits in the same place on every page.
    """
    meta = (
        f'\n  <meta name="description" content="{html.escape(description, quote=True)}">'
        if description
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title, quote=False)}</title>{meta}
  <link rel="icon" href="{_ICON}">
  <style>{_CSS}</style>
  <script>{_THEME_EARLY}</script>
</head>
<body>
<header class="site">
<button class="menu" type="button" aria-label="Menu" aria-controls="sidebar" aria-expanded="false">\u2630</button>
<a class="brand" href="/">Popcorn docs</a><nav><a href="/llms.txt">llms.txt</a>
<button class="theme" type="button" hidden></button>
</nav></header>
<div class="layout">
<aside class="sidebar" id="sidebar">{sidebar}</aside>
<main>
{content}
</main>
<aside class="rail">{rail}</aside>
</div>
<script>{_THEME_TOGGLE}{_NAV}</script>
</body>
</html>
"""
