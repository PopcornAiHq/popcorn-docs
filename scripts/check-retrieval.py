#!/usr/bin/env python3
"""Smoke-test the retrieval layer against the eval question set.

Not the validation pass — that asks a model whether a summary ANSWERS the
question, and only a model can judge it. This asks something narrower and
mechanical: does the right concept even come back? A summary that never
surfaces cannot be judged, so this is the gate before the gate.

Fails only on a question whose expected concept is absent from the top three,
which is the rank a caller realistically reads.
"""

from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "server"))
import retrieval  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOP_N = 3


def questions() -> list[tuple[str, list[str]]]:
    """Read the eval set without a YAML dependency."""
    text = (ROOT / "evals" / "questions.yaml").read_text()
    out, q = [], None
    for line in text.splitlines():
        if m := re.match(r'^- q: "?(.+?)"?$', line):
            q = m.group(1)
        elif (m := re.match(r"^  concept: (.+)$", line)) and q:
            out.append((q, [c.strip() for c in m.group(1).split(",")]))
            q = None
    return out


def main() -> int:
    pages = retrieval.load(ROOT / "build" / "chunks.json")
    ids = [p["id"] for p in pages]
    misses = []

    for question, expected in questions():
        ranked = sorted(
            pages,
            key=lambda p: retrieval._score(p, retrieval._terms(question)),
            reverse=True,
        )
        top = [p["id"] for p in ranked[:TOP_N]]
        if not any(e in top for e in expected):
            misses.append((question, expected, top))

    total = len(questions())
    for question, expected, top in misses:
        print(f"\n✖  {question}")
        print(f"     expected one of {expected}")
        print(f"     got {top}")

    if misses:
        print(
            f"\n   {len(misses)} of {total} questions do not surface their "
            f"concept in the top {TOP_N}.\n"
        )
        return 1

    print(f"✔  all {total} questions surface their concept in the top {TOP_N}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
