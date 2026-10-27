#!/usr/bin/env python3
"""Enforce the frontmatter contract in `content/_frontmatter.md`.

That document tells a writer a file missing `id` or `summary` fails the build.
This is what makes that true. Without it the contract is a convention, and a
convention is what the summary cap was already losing to — a retrieval surface
returns many summaries in one response, so one long summary is a cost every
caller pays.

Checks, in the order a writer meets them:

* frontmatter parses at all
* `id` is present and equals the filename, because the id is a permanent
  address and a file whose name disagrees with it has two
* `summary` is present and within the cap
* no unwritten body is left behind a finished-looking summary
* every id in `concepts:` names a page that exists. The build drops a dangling
  one from "Related" rather than linking a 404, which is right for the site
  and exactly why nobody sees it: the reference just silently stops working
* `order`, when present, is a whole number from 1 — the build sorts by it, and
  a value it cannot read would crash the build rather than fail here by name
* `layout`, when present, is `lookup` — the only layout the build knows, so
  anything else would silently render as an ordinary page
* `deployed`, when present, is a real `YYYY-MM-DD` date — it is shown to
  readers as the day the page was last regenerated, so a malformed one would
  be published as a claim about freshness nobody can read. Its old name,
  `platform:`, is refused
* no `source:` field. The backend symbols behind a page are private names,
  kept in a mapping in the private backend repository; this repository is
  public, so a page that lists them leaks them, and this is the guard that
  stops one page at a time bringing the field back
* `part` is `use` or `build`: which half of the site the page is in, Using
  Popcorn or Building Routine Templates. The sidebar, the page's address and
  search all read it, so a page without one would belong to neither. The
  glossary and the reference pages serve both parts and carry none. The
  field's old name, `layer:`, is refused
* no `applies_to:` field. It recorded which readers a page was for and
  nothing read it; a page that needs the CLI says so
  in its prose
* no `product_terms:` field. It named the product terms a page written in
  the platform's words explained; every page is now written in the
  product's words, so nothing reads it
"""

from __future__ import annotations

import datetime
import pathlib
import re
import sys

SUMMARY_MAX = 400
BODY_MIN_WORDS = 60
ROOT = pathlib.Path(__file__).resolve().parent.parent

_DOC = re.compile(r"^---\n(?P<fm>.*?)\n---\n(?P<body>.*)$", re.S)
_ID = re.compile(r"^id:\s*(\S+)", re.M)
_SUMMARY = re.compile(r"^summary:\s*>\n(?P<block>(?:[ \t]{2,}.*\n)+)", re.M)
_ORDER = re.compile(r"^order:\s*(?P<value>.*)$", re.M)
_LAYOUT = re.compile(r"^layout:\s*(?P<value>.*)$", re.M)
LAYOUTS = {"lookup"}
_DEPLOYED = re.compile(r"^deployed:\s*(?P<value>.*)$", re.M)
_OLD_PLATFORM = re.compile(r"^platform\s*:", re.M)
_CONCEPTS = re.compile(r"^concepts:\s*\[(?P<ids>[^\]]*)\]", re.M)
_SOURCE = re.compile(r"^source\s*:", re.M)
_PART = re.compile(r"^part:\s*(?P<value>.*)$", re.M)
PARTS = {"use", "build"}
_LAYER = re.compile(r"^layer\s*:", re.M)
_APPLIES_TO = re.compile(r"^applies_to\s*:", re.M)
_PRODUCT_TERMS = re.compile(r"^product_terms\s*:", re.M)


def check(path: pathlib.Path, ids: set[str]) -> list[str]:
    text = path.read_text()
    doc = _DOC.match(text)
    if not doc:
        return ["no frontmatter block"]

    problems: list[str] = []
    front, body = doc.group("fm"), doc.group("body")

    ident = _ID.search(front)
    if not ident:
        problems.append("no id")
    elif ident.group(1) != path.stem:
        problems.append(f"id '{ident.group(1)}' does not match the filename")

    summary = _SUMMARY.search(front)
    if not summary:
        problems.append("no summary, or it is not a folded block (summary: >)")
    else:
        folded = " ".join(
            line.strip() for line in summary.group("block").splitlines()
        ).strip()
        if len(folded) > SUMMARY_MAX:
            problems.append(f"summary is {len(folded)} chars, cap is {SUMMARY_MAX}")

    concepts = _CONCEPTS.search(front)
    if concepts:
        for ref in (i.strip() for i in concepts.group("ids").split(",")):
            if ref and ref not in ids:
                problems.append(f"concepts: '{ref}' is not the id of any page")

    order = _ORDER.search(front)
    if order and not order.group("value").strip().isdigit():
        problems.append(f"order '{order.group('value').strip()}' is not a whole number")
    elif order and int(order.group("value")) < 1:
        problems.append("order starts at 1")

    layout = _LAYOUT.search(front)
    if layout and layout.group("value").strip() not in LAYOUTS:
        problems.append(f"layout '{layout.group('value').strip()}' is not one of {sorted(LAYOUTS)}")

    deployed = _DEPLOYED.search(front)
    if deployed:
        value = deployed.group("value").strip()
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError
            datetime.date.fromisoformat(value)
        except ValueError:
            problems.append(f"deployed '{value}' is not a YYYY-MM-DD date")
    if _OLD_PLATFORM.search(front):
        problems.append(
            "platform: is the old name of the deploy-date field; write deployed:"
        )

    # The glossary and the references serve both parts; every other page is in one.
    shared = path.parent.name == "reference" or (ident is not None and ident.group(1) == "glossary")
    part = _PART.search(front)
    if _LAYER.search(front):
        problems.append("layer: is renamed part: — use for using Popcorn, build for building templates")
    elif shared and part:
        problems.append("part: is for a page in one part; the glossary and the references have none")
    elif not shared and not part:
        problems.append(f"no part — every page but the glossary and the references is one of {sorted(PARTS)}")
    elif part and part.group("value").strip() not in PARTS:
        problems.append(f"part '{part.group('value').strip()}' is not one of {sorted(PARTS)}")

    if _APPLIES_TO.search(front):
        problems.append("applies_to: is retired — say in the page's prose when it needs the CLI")
    if _PRODUCT_TERMS.search(front):
        problems.append(
            "product_terms: is retired — every page is written in the product's words, "
            "so none needs to declare which it explains"
        )

    if _SOURCE.search(front):
        problems.append(
            "source: is refused — a page's backend symbols are private and live "
            "in the backend's mapping, not here (see content/_frontmatter.md)"
        )

    words = len(body.split())
    if words < BODY_MIN_WORDS:
        problems.append(f"body is {words} words; a stub is not publishable")

    return problems


def main() -> int:
    files = sorted((ROOT / "content").rglob("*.md"))
    files = [f for f in files if not f.name.startswith("_")]
    if not files:
        print("✖  no content files found", file=sys.stderr)
        return 1

    # A page's id is its filename, which the id check above enforces, so the
    # stems are the ids a `concepts:` entry may name.
    ids = {f.stem for f in files}
    failed = 0
    for path in files:
        problems = check(path, ids)
        if problems:
            failed += 1
            print(f"\n✖  {path.relative_to(ROOT)}")
            for problem in problems:
                print(f"     {problem}")

    if failed:
        print(
            f"\n   {failed} of {len(files)} files break the contract in "
            "content/_frontmatter.md.\n"
        )
        return 1

    print(f"✔  {len(files)} content files satisfy the frontmatter contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
