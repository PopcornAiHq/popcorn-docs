#!/usr/bin/env python3
"""The YAML highlighter never changes a block's text, and marks what it should.

A code block's copy button copies the block's text, so the highlighted HTML
must read back as exactly the code that was written: strip the tags, unescape
the entities, and every character is where it was. That is checked against
every YAML block in `content/`, which is the input the highlighter actually
meets, and against a handful of shapes chosen to be awkward — markup
characters, quotes that escape themselves, a `#` that is not a comment.

The token cases below pin the classes a reader sees. They are few on purpose:
the invariant is the check that matters, and these only catch a scanner that
has stopped recognising a key or a comment at all.
"""

from __future__ import annotations

import html
import pathlib
import re
import sys

import highlight
import render

ROOT = pathlib.Path(__file__).resolve().parent.parent
_TAG = re.compile(r"<[^>]+>")
_OPEN = re.compile(r"^```(?P<lang>\S*)\s*$")

AWKWARD = """\
key: <not-a-tag> & "quoted <b>" # comment with </code>
'it''s': "say \\"hi\\" # not a comment"
url: http://example.com:8080/#frag
flow: { a: 1, b: [x, "y, z"], c: { d: ~ } }
- &base { k: v }
- *base
run: |-
  echo "<script>" # stays in the string
  second line

after: yes
"""

# (line, [(class, text)...]) — the spans that line must contain.
TOKENS = [
    ("name: my_flow  # identity", [("k", "name"), ("c", "# identity")]),
    ('label: "a: b"', [("k", "label"), ("s", '"a: b"')]),
    ("version: 1", [("n", "1")]),
    ("best_effort: false", [("n", "false")]),
    ("x: null", [("n", "null")]),
    ("  - id: step", [("p", "-"), ("k", "id")]),
    ("Last Seen: { $lt: $steps.a }", [("k", "Last Seen"), ("k", "$lt"), ("p", "{")]),
    ("- &anchor a: *alias", [("a", "&amp;anchor"), ("a", "*alias")]),
    ("description: >\n  text: # not a key", [("p", "&gt;"), ("s", "text: # not a key")]),
]


def yaml_blocks() -> list[tuple[pathlib.Path, str]]:
    """Every fenced YAML block in content/, as the renderer would read it."""
    out = []
    for path in sorted((ROOT / "content").rglob("*.md")):
        lines, i = path.read_text().splitlines(), 0
        while i < len(lines):
            m = _OPEN.match(lines[i])
            i += 1
            if not m:
                continue
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            if m.group("lang").lower() in highlight.LANGUAGES:
                out.append((path, "\n".join(code)))
    return out


def text_of(rendered: str) -> str:
    return html.unescape(_TAG.sub("", rendered))


def main() -> int:
    problems: list[str] = []
    blocks = yaml_blocks()
    if not blocks:
        problems.append("content/ holds no YAML blocks — the round trip below checked nothing")
    for label, code in [(p.relative_to(ROOT), c) for p, c in blocks] + [("the awkward case", AWKWARD)]:
        rendered = highlight.yaml(code)
        if text_of(rendered) != code:
            problems.append(f"{label}: highlighting changed the block's text")
        # A raw < or & left in the output is markup the page would parse.
        if re.search(r"<(?!/?span[ >])|&(?!(?:amp|lt|gt|quot|#x27);)", rendered):
            problems.append(f"{label}: unescaped markup in the highlighted HTML")

    for line, expected in TOKENS:
        rendered = highlight.yaml(line)
        for cls, text in expected:
            if f'<span class="{cls}">{text}</span>' not in rendered:
                problems.append(f"{line!r}: expected {text!r} marked {cls!r}, got {rendered}")

    # Anything not tagged YAML is escaped and nothing more.
    plain = render.code_block("a: <b> & c", "bash")
    if "<code>a: &lt;b&gt; &amp; c</code>" not in plain:
        problems.append(f"a bash block was highlighted or mis-escaped: {plain}")

    for p in problems:
        print(f"✖  {p}", file=sys.stderr)
    if problems:
        return 1
    print(f"✔  {len(blocks)} YAML blocks highlight without changing their text")
    return 0


if __name__ == "__main__":
    sys.exit(main())
