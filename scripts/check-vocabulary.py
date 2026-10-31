#!/usr/bin/env python3
"""Report the names a page still uses where the product has its own word.

Every page is written in the product's words (`INFORMATION-ARCHITECTURE.md`,
"One vocabulary"). The CLI, the API and older copy still call
some things by other names, and the glossary's table "Names you'll
see elsewhere" pairs each with the product's word. This script reads that
table and lists each prose use of one of its names on a hand-written page.

A name is allowed:

* in code — `popcorn app fork` is what the reader types
* italicised, as the name being mentioned rather than used — usually the
  parenthetical that gives it as the other name: "a copy of the template (the
  CLI calls it a *fork line*)"
* inside a longer glossary entry: "channel agent" and "channel parameters"
  are terms of their own, not the name "channel"

Not checked: the glossary, which defines the names, and generated pages
(those carrying `updated:` or `version:`), whose text comes from the
platform itself.

Some names are everyday English as well — a person's *app*, a *project*, a
*record* of what happened — and can't be told apart from the platform's word
in prose, while in code they are allowed anyway. Those are left to review.

It also lists a glossary term written lowercase in prose. Every term the
glossary defines is capitalized where it means that concept (`CLAUDE.md`,
"Glossary terms are capitalized"), but many are everyday words too — a *run*
of the command, the server's *state* — and only a reader can tell which is
meant. So only the terms with no ordinary sense are checked: the multi-word
ones, where "merge policy" can only be the concept, and the few single words
listed in `CAPITALIZED`. Code and italicised mentions are allowed, as above,
and so is an interface label in `LABELS`, quoted as the interface spells it.
The glossary itself is checked down to its names table, whose first column
holds the other names, lowercase by design.

CI and the pre-commit hook run it with `--strict`, which exits 1 when
anything is listed. Without it, it only reports.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
GLOSSARY = CONTENT / "concepts" / "glossary.md"
TABLE_HEADING = "## Names you'll see elsewhere"

# Names that are also everyday words; see the module docstring.
ORDINARY = {"app", "project", "record"}

# Glossary terms that are never ordinary English, so a lowercase use in prose
# is always a slip. Words that are also everyday English (run, flow, state,
# copy, item, version…) are left to review; see the module docstring.
CAPITALIZED = [
    "Routine Template", "Routine Settings", "Routine Setting", "Workspace Agent",
    "Workspace Member", "Workspace Role", "Routine Member", "App Bundle",
    "App Agent", "Booking Page", "Signing Provider", "Daily Update",
    "State Machine", "Merge Policy", "Merge Policies", "Merge Key",
    "Release Track", "Message Trigger", "Trigger Report", "Connected Account",
    "Integration Requirement", "Activity Catalog", "Inbox Scan",
    "Routine", "Workspace", "Webhook", "Manifest", "Scalar", "Bundle",
]
# Interface labels, quoted as the interface spells them, like code.
LABELS = {"New routine"}

_DOC = re.compile(r"^---\n(?P<fm>.*?)\n---\n(?P<body>.*)$", re.S)
_GENERATED = re.compile(r"^(updated|version):", re.M)
# An entry can head with several terms, as "- **Agent**, **channel agent** —":
# each is a term of its own, and masks the name it holds.
_ENTRY = re.compile(
    r"^- \*\*(?P<term>[^*]+)\*\*(?:\s*\(short: \*\*(?P<short>[^*]+)\*\*\))?"
    r"(?P<more>(?:, \*\*[^*]+\*\*)*)",
    re.M,
)
_MORE = re.compile(r"\*\*([^*]+)\*\*")
# A fence may be indented inside a list item, and a code span may wrap a line.
_FENCE = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.S | re.M)
# A span may wrap a line but not cross a blank one, so a stray backtick
# cannot hide the paragraphs after it.
_CODE = re.compile(r"`(?:[^`\n]|\n(?![ \t]*\n))+`")
_LINK = re.compile(r"\]\([^)\s]+\)")
_LINK_TEXT_URL = re.compile(r"https?://\S+|<[^>\n]+>")
# Single-asterisk italics, not `**bold**`: a name in italics is being mentioned.
_ITALIC = re.compile(r"(?<![*\w])\*(?!\*)[^*\n]+?(?<!\*)\*(?![*\w])")


def names() -> list[str]:
    """The first column of the glossary's names table."""
    text = GLOSSARY.read_text()
    start = text.find(TABLE_HEADING)
    if start < 0:
        sys.exit(f"✖  {GLOSSARY.relative_to(ROOT)} has no '{TABLE_HEADING}' section")
    out = []
    for line in text[start:].splitlines()[1:]:
        if line.startswith("## "):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells[0] not in ("Name", "") and not cells[0].startswith("-"):
            out.append(cells[0].lower())
    return out


def entries() -> set[str]:
    out = set()
    for m in _ENTRY.finditer(GLOSSARY.read_text()):
        for name in (m.group("term"), m.group("short"), *_MORE.findall(m.group("more") or "")):
            if name:
                out.add(name.strip().strip("`").lower())
    return out


def _phrase(term: str) -> re.Pattern[str]:
    # Plurals count: "channels" is the name as much as "channel".
    return re.compile(r"(?<![\w-])" + re.escape(term) + r"(?:s|es)?(?![\w-])", re.I)


def _singular(term: str) -> str:
    return term[:-1] if term.endswith("s") and not term.endswith("ss") else term


def prose(body: str) -> str:
    """The body as a reader reads it: no code and no addresses."""
    text = _FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), body)
    # A wrapped code span keeps its line breaks, so line numbers stay true.
    text = _CODE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return _LINK.sub("]", text)


def paragraphs(text: str) -> list[tuple[int, str]]:
    """Each paragraph joined onto one line, with the body line it starts on.

    A term wrapped across a line break ("a channel" / "parameter") is still
    one term, so matching runs over paragraphs, not lines.
    """
    out, start, buf = [], 0, []
    for lineno, line in enumerate(text.splitlines() + [""], 1):
        if line.strip():
            if not buf:
                start = lineno
            buf.append(line.strip())
        elif buf:
            out.append((start, _ITALIC.sub("", " ".join(buf))))
            buf = []
    return out


def _term(term: str) -> re.Pattern[str]:
    # A wrapped term is still one term, and a filename ("manifest.yaml") or a
    # hyphenated compound is not prose use of it.
    words = r"\s+".join(re.escape(w) for w in term.split())
    return re.compile(r"(?<![\w-])" + words + r"s?(?![\w-]|\.\w)", re.I)


def _lowercase(text: str) -> list[str]:
    """Each term in `text` written with a lowercase word, longest term first."""
    out = []
    for term in sorted(CAPITALIZED, key=len, reverse=True):
        pattern = _term(term)
        for m in pattern.finditer(text):
            if any(w[0].islower() for w in m.group(0).split()):
                out.append(" ".join(m.group(0).split()))
        text = pattern.sub("", text)
    return out


def _fields(fm: str) -> list[tuple[int, str]]:
    """The frontmatter fields a reader sees: title, summary and lede."""
    out = []
    for m in re.finditer(r"^(title|summary|lede):(.*(?:\n[ \t]+.*)*)", fm, re.M):
        out.append((0, _ITALIC.sub("", " ".join(prose(m.group(2)).split()))))
    return out


def capitalization(f: pathlib.Path, doc: re.Match[str]) -> list[str]:
    body = doc.group("body")
    if f == GLOSSARY:
        body = body[: body.find(TABLE_HEADING)]
    for label in LABELS:
        body = body.replace(f"**{label}**", "")
    hits = []
    for lineno, line in _fields(doc.group("fm")) + paragraphs(prose(body)):
        where = f"paragraph at body line {lineno}" if lineno else "frontmatter"
        hits += [f"{where}: '{t}' lowercase" for t in _lowercase(_LINK_TEXT_URL.sub("", line))]
    return hits


def main() -> int:
    guarded = [n for n in names() if n not in ORDINARY]
    # A longer entry holding a name ("channel agent") is masked first, so the
    # name inside it is never matched.
    masks = sorted(
        (e for e in entries() if e not in guarded and any(_phrase(n).search(e) for n in guarded)),
        key=len, reverse=True,
    )
    # Some entries are headed in the plural ("channel parameters"), and prose
    # also uses them in the singular, so a mask matches from the singular up.
    mask_patterns = [_phrase(_singular(m)) for m in masks]
    patterns = [(n, _phrase(n)) for n in sorted(guarded, key=len, reverse=True)]

    found: dict[str, list[str]] = {}
    checked = 0
    for f in sorted(CONTENT.rglob("*.md")):
        if f.name.startswith("_") and f.name != "_overview.md":
            continue
        text = f.read_text()
        # The Overview has no frontmatter; it is prose all the same.
        doc = _DOC.match(text) or _DOC.match(f"---\n\n---\n{text}")
        if not doc or _GENERATED.search(doc.group("fm")):
            continue
        checked += 1
        for hit in capitalization(f, doc):
            found.setdefault(f.stem, []).append(hit)
        if f == GLOSSARY or f.name.startswith("_"):
            continue
        for lineno, line in paragraphs(prose(doc.group("body"))):
            for mask in mask_patterns:
                line = mask.sub("", line)
            for name, pattern in patterns:
                if pattern.search(line):
                    found.setdefault(f.stem, []).append(f"paragraph at body line {lineno}: '{name}'")
                    line = pattern.sub("", line)

    total = sum(len(v) for v in found.values())
    for page, hits in found.items():
        print(f"{page}: {len(hits)}")
        for hit in hits:
            print(f"    {hit}")
    mark = "✖ " if total and "--strict" in sys.argv else "• "
    print(
        f"{mark} {total} use(s) of {len(guarded)} names or {len(CAPITALIZED)} lowercase "
        f"terms in {len(found)} of {checked} hand-written pages"
        + ("" if total else " — every page uses the product's words, capitalized")
    )
    return 1 if total and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
