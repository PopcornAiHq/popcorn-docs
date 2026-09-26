#!/usr/bin/env python3
"""YAML syntax highlighting for the HTML pages, done at build time.

At build time rather than in the browser so that the page is highlighted
with no script at all, and so that the site keeps its no-dependency build:
no highlighter to vendor, pin or load from a CDN.

Not a YAML parser. It is a line scanner that knows the handful of shapes a
reader's eye uses to find its way around a block — keys, quoted strings,
numbers and booleans and null, comments, anchors and aliases, list dashes,
flow brackets, and the lines of a `|` or `>` block scalar. Plain unquoted
values are left in the text colour: in a flow file most values are plain
(`$steps.x.output`, activity names), and colouring every one of them would
leave nothing standing out.

The one invariant that matters: the output, with its tags stripped and its
entities unescaped, is exactly the input. The copy button copies the text
of the block, so a highlighter that altered a character would change what
a reader pastes. `check-highlight.py` holds every YAML block in `content/`
to that.
"""

from __future__ import annotations

import html
import re

# The token classes, as CSS classes. The stylesheet in render.py colours them.
KEY, STRING, LITERAL, COMMENT, ANCHOR, PUNCT = "k", "s", "n", "c", "a", "p"

LANGUAGES = {"yaml", "yml"}

# YAML 1.2 core schema scalars, plus the 1.1 booleans a reader still writes.
_LITERAL = re.compile(
    r"^(?:~|null|Null|NULL|true|True|TRUE|false|False|FALSE|yes|Yes|YES|no|No|NO|on|On|ON|off|Off|OFF"
    r"|[-+]?(?:\d[\d_]*)(?:\.\d*)?(?:[eE][-+]?\d+)?|[-+]?\.\d+(?:[eE][-+]?\d+)?"
    r"|0x[0-9a-fA-F]+|0o[0-7]+|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$"
)
# A block scalar's header: `|` or `>`, then an optional chomping and
# indentation indicator in either order, then nothing but a comment.
_BLOCK = re.compile(r"[|>](?:[-+]?[1-9]?|[1-9][-+])(?=[ \t]*$|[ \t]+#)")
_ANCHOR = re.compile(r"[&*][^\s,\[\]{}]+")
_FLOW = "{}[],"


def _span(cls: str, text: str) -> str:
    return f'<span class="{cls}">{html.escape(text, quote=False)}</span>' if text else ""


class _Line:
    """One line's tokens, and what the scan learned that outlives the line."""

    def __init__(self, line: str, depth: int):
        self.line, self.depth = line, depth
        self.out: list[str] = []
        self.block_indent: int | None = None  # set when a block scalar opens here

    def emit(self, cls: str | None, text: str) -> None:
        self.out.append(_span(cls, text) if cls else html.escape(text, quote=False))

    def html(self) -> str:
        return "".join(self.out)


def _quoted(line: str, i: int) -> int:
    """The index just past the quoted scalar starting at ``i``, or the line's end."""
    quote, j = line[i], i + 1
    while j < len(line):
        if quote == '"' and line[j] == "\\":
            j += 2
            continue
        if line[j] == quote:
            if quote == "'" and line[j + 1:j + 2] == "'":  # '' is an escaped quote
                j += 2
                continue
            return j + 1
        j += 1
    return len(line)


def _is_key_colon(line: str, j: int, depth: int) -> bool:
    """Does the `:` at ``j`` end a key? Only when followed by space or the end —
    or, inside a flow collection, by one of its brackets or a comma."""
    if j >= len(line) or line[j] != ":":
        return False
    after = line[j + 1:j + 2]
    return after in ("", " ", "\t") or (depth > 0 and after in _FLOW)


def _scan(state: _Line) -> None:
    line, n = state.line, len(state.line)
    i = 0
    # Where a node starts in block context: after the indent and any list
    # dashes. A block scalar's lines are the ones indented past its key.
    start = True
    node_col = len(line) - len(line.lstrip(" "))
    while i < n:
        c = line[i]
        if c in " \t":
            j = i
            while j < n and line[j] in " \t":
                j += 1
            state.emit(None, line[i:j])
            i = j
            continue
        if c == "#" and (i == 0 or line[i - 1] in " \t"):
            state.emit(COMMENT, line[i:])
            return
        if start and state.depth == 0 and c == "-" and line[i + 1:i + 2] in ("", " ", "\t"):
            state.emit(PUNCT, "-")
            node_col = i + 1
            i += 1
            continue
        if c in "\"'":
            j = _quoted(line, i)
            k = j
            while k < n and line[k] in " \t":
                k += 1
            if _is_key_colon(line, k, state.depth):
                state.emit(KEY, line[i:j])
                state.emit(None, line[j:k])
                state.emit(PUNCT, ":")
                node_col, i = i, k + 1
            else:
                state.emit(STRING, line[i:j])
                i = j
            start = False
            continue
        if c in "&*":
            m = _ANCHOR.match(line, i)
            if m and len(m.group()) > 1:
                state.emit(ANCHOR, m.group())
                i = m.end()
                continue
        if c in "{[":
            state.depth += 1
            state.emit(PUNCT, c)
            i += 1
            continue
        if c in "}]," and state.depth > 0:
            if c != ",":
                state.depth -= 1
            state.emit(PUNCT, c)
            i += 1
            continue
        if state.depth == 0 and c in "|>":
            m = _BLOCK.match(line, i)
            if m:
                state.emit(PUNCT, m.group())
                state.block_indent = node_col
                i = m.end()
                continue
        # A plain scalar: up to a comment, a key's colon, or — in a flow
        # collection — the next bracket or comma.
        j = i
        while j < n:
            ch = line[j]
            if ch == "#" and line[j - 1] in " \t":
                break
            if ch == ":" and _is_key_colon(line, j, state.depth):
                break
            if state.depth > 0 and ch in _FLOW:
                break
            j += 1
        text = line[i:j]
        body = text.rstrip(" \t")
        is_key = j < n and line[j] == ":"
        state.emit(KEY if is_key else LITERAL if _LITERAL.match(body) else None, body)
        state.emit(None, text[len(body):])
        if is_key:
            state.emit(PUNCT, ":")
            node_col, j = i, j + 1
        i = j
        start = False


def yaml(code: str) -> str:
    """``code`` as HTML: escaped, with its tokens wrapped in classed spans."""
    out: list[str] = []
    depth = 0
    block: int | None = None  # the column a block scalar's lines must pass
    for line in code.split("\n"):
        if block is not None:
            indent = len(line) - len(line.lstrip(" "))
            if not line.strip() or indent > block:
                out.append(html.escape(line[:indent], quote=False) + _span(STRING, line[indent:]))
                continue
            block = None
        state = _Line(line, depth)
        _scan(state)
        depth, block = state.depth, state.block_indent
        out.append(state.html())
    return "\n".join(out)
