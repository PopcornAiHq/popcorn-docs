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
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _ITALIC.sub(r"<em>\1</em>", out)
    for i, span in enumerate(spans):
        out = out.replace(f"\x00{i}\x00", f"<code>{span}</code>")
    return out


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def body(md: str) -> str:
    """Render a concept body. Block constructs first, inline within them."""
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
            out.append(f"<h{level}>{inline(heading.group('text'))}</h{level}>")
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
                cont = lines[i]
                if items and cont.strip() and cont[0] in " \t" \
                        and not cont.startswith("    "):
                    items[-1] += " " + cont.strip()
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
        ):
            para.append(lines[i].strip())
            i += 1
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
        else:
            i += 1

    return "\n".join(out)


_CSS = """
:root {
  --bg: #fdfdfc; --fg: #22201d; --muted: #6b665f; --rule: #e4e0d9;
  --accent: #9a3412; --code-bg: #f4f2ee;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1917; --fg: #e8e4dd; --muted: #9b958c; --rule: #33302c;
    --accent: #f0935f; --code-bg: #232120;
  }
}
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
.home { display: inline-block; margin-bottom: 2.5rem; color: var(--muted); font-size: .9rem; }
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
"""


def document(title: str, content: str, *, description: str = "") -> str:
    """Wrap rendered content in a standalone page."""
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
  <style>{_CSS}</style>
</head>
<body>
<main>
{content}
</main>
</body>
</html>
"""
