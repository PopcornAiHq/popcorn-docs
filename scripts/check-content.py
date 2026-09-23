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
"""

from __future__ import annotations

import pathlib
import re
import sys

SUMMARY_MAX = 400
BODY_MIN_WORDS = 60
ROOT = pathlib.Path(__file__).resolve().parent.parent

_DOC = re.compile(r"^---\n(?P<fm>.*?)\n---\n(?P<body>.*)$", re.S)
_ID = re.compile(r"^id:\s*(\S+)", re.M)
_SUMMARY = re.compile(r"^summary:\s*>\n(?P<block>(?:[ \t]{2,}.*\n)+)", re.M)
_CONCEPTS = re.compile(r"^concepts:\s*\[(?P<ids>[^\]]*)\]", re.M)


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
