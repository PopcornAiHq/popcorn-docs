#!/usr/bin/env python3
"""Keep the product layer in the product's words.

A page with `layer: product` is written for a Popcorn user and their
assistant, who meet a Routine and never a channel. Such a page may still need
to name a platform term — the mechanism under a product idea — and the one
place it may do so is a Platform note:

    > **Platform note** — A copy of its own is a *fork line* … See
    > [Fork lines](https://docs.popcorn.ai/platform/concepts/fork-line.md).

Checks:

* a product page uses no platform term outside a Platform note
* every Platform note links at least one `layer: platform` page, because a
  note that names the mechanism and leads nowhere strands the reader
* a platform page declares `product_terms:` — the product glossary terms it
  explains the mechanism behind — and its summary names one of them. A reader
  arriving from a Platform note, or a search in the product's words, lands on
  a page that says the term they came with. `product_terms: []` declares a
  page with no product term, such as the flow grammar, on purpose; leaving the
  field out is the omission this catches

The terms come from the platform glossary's entries, less the ones the
product glossary also defines (`workspace`, `table`, …), so a term is guarded
as soon as the glossary defines it. Some entries are ordinary English as
well — a person *runs* something, *publishes* a post — and those are matched
only in code form (`` `run` ``), where they can only mean the platform's
word. Every other entry is matched in prose too.

Generated pages (those carrying `platform:` or `version:`) are exempt: they
describe a surface entry by entry, and the MCP reference documents the
template-building tools in their own section on purpose.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
GLOSSARY = CONTENT / "concepts" / "glossary.md"
PRODUCT_GLOSSARY = CONTENT / "concepts" / "product-glossary.md"

# Platform glossary entries that are also everyday words. In prose they are
# allowed; in backticks they are the platform's term and are not.
ORDINARY = {
    "active", "activity", "adoption", "app", "apply", "binding", "bot",
    "checkout", "conversation", "flow", "fork", "head", "install",
    "integration", "line", "member", "message", "outcome", "presence",
    "project", "publish", "reaction", "run", "schedule", "state", "step",
    "thread", "user", "webhook",
}

_DOC = re.compile(r"^---\n(?P<fm>.*?)\n---\n(?P<body>.*)$", re.S)
_ENTRY = re.compile(
    r"^- \*\*(?P<term>[^*]+)\*\*(?:\s*\(short: \*\*(?P<short>[^*]+)\*\*\))?", re.M
)
_LAYER = re.compile(r"^layer:\s*(?P<value>\S+)", re.M)
_TERMS = re.compile(r"^product_terms:\s*\[(?P<terms>[^\]]*)\]", re.M)
_SUMMARY = re.compile(r"^summary:\s*>\n(?P<block>(?:[ \t]{2,}.*\n)+)", re.M)
_GENERATED = re.compile(r"^(platform|version):", re.M)
_NOTE = re.compile(r"^> \*\*Platform note\*\*")
_LINK = re.compile(r"\]\((?P<url>[^)\s]+)\)")
_DOCS_URL = re.compile(r"^https://docs\.popcorn\.ai/(?:[a-z]+/)*(?P<id>[a-z0-9-]+)\.(?:md|html)")


def _entries(path: pathlib.Path) -> set[str]:
    text = path.read_text()
    out = set()
    for m in _ENTRY.finditer(text):
        for name in (m.group("term"), m.group("short")):
            if name:
                out.add(name.strip().strip("`").lower())
    return out


def platform_terms() -> set[str]:
    return _entries(GLOSSARY) - _entries(PRODUCT_GLOSSARY)


def _pattern(term: str, code_only: bool) -> re.Pattern[str]:
    # Plurals count: "channels" is the platform's word as much as "channel".
    word = re.escape(term) + r"(?:s|es)?"
    if code_only:
        return re.compile(r"`" + word + r"`", re.I)
    return re.compile(r"(?<![\w-])" + word + r"(?![\w-])", re.I)


def split_notes(body: str) -> tuple[str, list[str]]:
    """The body with every Platform note removed, and the notes themselves."""
    kept: list[str] = []
    notes: list[str] = []
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        if _NOTE.match(lines[i]):
            note = []
            while i < len(lines) and lines[i].startswith(">"):
                note.append(lines[i])
                i += 1
            notes.append("\n".join(note))
            continue
        kept.append(lines[i])
        i += 1
    return "\n".join(kept), notes


def _prose(text: str) -> str:
    # A link's URL is an address, not prose: `/concepts/fork-line.md` names
    # the page, it does not say "fork line" to the reader.
    return _LINK.sub("]()", text)


def main() -> int:
    pages: dict[str, tuple[str, str, str]] = {}
    for f in sorted(CONTENT.rglob("*.md")):
        if f.name.startswith("_"):
            continue
        doc = _DOC.match(f.read_text())
        if not doc:
            continue
        layer = _LAYER.search(doc.group("fm"))
        pages[f.stem] = (layer.group("value") if layer else "", doc.group("fm"), doc.group("body"))

    terms = platform_terms()
    patterns = [(t, _pattern(t, t in ORDINARY)) for t in sorted(terms, key=len, reverse=True)]

    problems: list[str] = []
    checked = 0
    product_terms = _entries(PRODUCT_GLOSSARY)
    for page_id, (layer, front, body) in pages.items():
        if layer == "platform" and not _GENERATED.search(front):
            declared = _TERMS.search(front)
            if not declared:
                problems.append(
                    f"{page_id}: no product_terms: — list the product terms this page "
                    "explains, or [] when it has none"
                )
                continue
            terms_here = [t.strip() for t in declared.group("terms").split(",") if t.strip()]
            unknown = [t for t in terms_here if t.lower() not in product_terms]
            if unknown:
                problems.append(f"{page_id}: product_terms {unknown} are not product glossary entries")
            block = _SUMMARY.search(front + "\n")
            summary = " ".join(block.group("block").split()) if block else ""
            if terms_here and not any(_pattern(t.lower(), False).search(summary) for t in terms_here):
                problems.append(f"{page_id}: the summary names none of its product_terms {terms_here}")
            continue
        if layer != "product":
            continue
        rest, notes = split_notes(body)

        for note in notes:
            linked = {
                m.group("id")
                for url in _LINK.finditer(note)
                if (m := _DOCS_URL.match(url.group("url")))
            }
            if not any(pages.get(i, ("",))[0] == "platform" for i in linked):
                first = note.splitlines()[0][:70]
                problems.append(f"{page_id}: a Platform note links no platform page — {first}…")

        if _GENERATED.search(front):
            continue
        checked += 1
        prose = _prose(rest)
        for lineno, line in enumerate(prose.splitlines(), 1):
            for term, pattern in patterns:
                if pattern.search(line):
                    problems.append(
                        f"{page_id}: body line {lineno} uses the platform term "
                        f"'{term}' outside a Platform note"
                    )

    for problem in problems:
        print(f"✖  {problem}")
    if problems:
        print(f"\n   {len(problems)} problem(s) on product pages", file=sys.stderr)
        return 1
    print(
        f"✔  {checked} product page(s) speak the product's words; "
        f"{len(terms)} platform terms guarded"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
