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


def toc(rendered: str, minimum: int = 6) -> str:
    """A contents list of a rendered page's second-level headings.

    Empty below ``minimum``: a short page is its own contents, and a box
    listing three headings is furniture.
    """
    entries = _H2.findall(rendered)
    if len(entries) < minimum:
        return ""
    items = "".join(f'<li><a href="#{a}">{h}</a></li>' for a, h in entries)
    return f'<nav class="toc" aria-label="Contents"><p>Contents</p><ol>{items}</ol></nav>'


def body(md: str) -> str:
    """Render a concept body. Block constructs first, inline within them."""
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
            out.append(
                "<ul>" + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ul>"
            )
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
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {""" + _DARK + """}
}
:root[data-theme="dark"] {""" + _DARK + """}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 3rem 1rem 6rem; background: var(--bg); color: var(--fg);
  font-family: var(--font); font-size: 17px; line-height: 1.65;
  -webkit-text-size-adjust: 100%;
}
main { max-width: 42rem; margin: 0 auto; }
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
.site { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: .5rem 1rem;
  margin-bottom: 2.5rem; padding-bottom: .9rem; border-bottom: 1px solid var(--rule); font-size: .92rem; }
.site a { text-decoration: none; }
.site .brand { color: var(--fg); font-weight: 650; letter-spacing: -.01em; }
.site nav a { color: var(--muted); margin-left: 1rem; }
.site nav a:hover, .site .brand:hover { color: var(--accent); }
.site nav a.current { color: var(--fg); font-weight: 600; }
.eyebrow { margin: 0 0 .35rem; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; }
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
.theme { margin-left: 1rem; padding: 0 .2rem; border: 0; background: none; color: var(--muted);
  font: inherit; font-size: 1rem; line-height: 1; cursor: pointer; }
.theme:hover { color: var(--accent); }
.anchor { margin-left: .4rem; color: var(--rule); text-decoration: none; font-weight: 400; opacity: 0; }
h2:hover .anchor, h3:hover .anchor, h4:hover .anchor, .anchor:focus { opacity: 1; color: var(--muted); }
:target { scroll-margin-top: 1.5rem; }
blockquote { margin: 0 0 1.4rem; padding: .2rem 0 .2rem 1.1rem; border-left: 3px solid var(--accent); color: var(--fg); }
blockquote p:last-child { margin-bottom: 0; }
.toc { background: var(--code-bg); border-radius: 6px; padding: .9rem 1.2rem .6rem; margin: 0 0 2.5rem; font-size: .93rem; }
.toc p { margin: 0 0 .4rem; font-weight: 600; color: var(--muted); font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; }
.toc ol { margin: 0; padding: 0; list-style: none; }
.toc li { margin-bottom: .25rem; }
.toc a { text-decoration: none; }
.toc a:hover { text-decoration: underline; }
.section-title { font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin: 3rem 0 0; font-weight: 600; }
.related { margin-top: 3rem; }
.related ul { padding-left: 1.3rem; }
@media (max-width: 30rem) {
  body { padding-top: 1.5rem; font-size: 16px; }
  .site nav a { margin-left: .7rem; }
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
    'try{var t=localStorage.getItem("theme");'
    'if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}'
)

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
    nav: list[tuple[str, str, bool]] = (),
) -> str:
    """Wrap rendered content in a standalone page.

    `nav` is (label, href, current) per section; the caller builds it from the
    sections that have pages, so the header never links to one that does not
    exist.
    """
    current_attrs = ' aria-current="true" class="current"'
    links = "".join(
        f'<a href="{href}"{current_attrs if current else ""}>'
        f"{html.escape(label, quote=False)}</a>"
        for label, href, current in nav
    )
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
<main>
<header class="site"><a class="brand" href="/">Popcorn docs</a><nav>
{links}<a href="/llms.txt">llms.txt</a>
<button class="theme" type="button" hidden></button>
</nav></header>
{content}
</main>
<script>{_THEME_TOGGLE}</script>
</body>
</html>
"""
