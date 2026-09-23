#!/usr/bin/env python3
"""Everything needed to run the validation pass by hand, in the right order.

This is the by-hand route: it asks whether a summary ANSWERS a question, and
only a model can judge that. What can be removed is the friction around it —
pasting the corpus, keeping the questions in order, not letting an answer be
scored against a rubric read after the fact. `eval-run.py` drives the same
prompt through the Gemini API instead; this remains the way to test an
assistant through its own app, which an API call is not.

Three outputs, in the order they are used:

    --prompt   the preamble, llms.txt fenced, and a trailing
               `Question or problem: ` slot.
               Pasted into a NEW session for every question, then the question
               typed onto the end of it — one message, no ambiguity about where
               the corpus stops. It stays on the clipboard for the whole run
    --ask      the questions, one per line, to send one at a time
    --sheet    a scoring sheet on stdout, with pass and trap spelled out per
               question and a blank verdict to fill in — redirect it somewhere
               outside this repository, it is a working document

One question per session, and the session is thrown away afterwards. Most of
these questions share a concept with another one, so a run that asks them in
sequence lets the model answer from its own earlier turn instead of from the
summary — and by the fifteenth it has learned what a good answer looks like
here, which is learning the test rather than reading the corpus. Pasting the
same reference once per question is the isolation; removing the tedium
removes the measurement.

The sheet is the part that matters. Scoring every answer from memory against a
rubric is how a gate quietly becomes a vibe: the `trap` for question 19 is not
in anyone's head by the time they reach it, and an answer that sounds right
gets a pass it did not earn. Reading the trap before the verdict is the whole
discipline, so the sheet puts it above the box.

The corpus is read from `build/`, so run `scripts/emit.py` first. That is
deliberate: the pass is run against what would be published, not against what
`content/` happens to contain.

Everything here writes to stdout and nothing writes into `build/`. That
directory is the publish set: `publish.py` uploads all of it and the link
check refuses anything in it that the index does not advertise. A scoring
sheet dropped there fails the build, and would otherwise have been served
from the docs site.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
QUESTIONS = ROOT / "evals" / "questions.yaml"

# The reference is fenced and the question has a labelled slot at the end, so
# that both the corpus and the question paste as one message with no ambiguity
# about where one stops. Without the fence the question lands as loose prose
# after the last summary, and the corpus is itself Markdown with `##` headings,
# so a heading would read as a twelfth entry rather than as the ask. The slot
# says "or problem" because half the set are symptom reports, not questions,
# and a report pasted after a bare `Question:` reads as a mislabelled ask.
PREAMBLE = """\
You are answering questions and problem reports about Popcorn, an AI
tracker, using only the reference between the markers below. Answer as if you
were about to act on it: say what the person should do, concretely.

If the reference does not contain enough to answer, say so and name the entry
you would read in full. Do not open the links or search the web; the reference
is everything you have. Do not guess at how similar systems usually behave.

===== REFERENCE START =====
"""

POSTAMBLE = """
===== REFERENCE END =====

Question or problem: """


def questions() -> list[dict]:
    """Read the eval set without a YAML dependency.

    The same deliberately small parser the retrieval check uses: this file is
    a flat list of records with known keys, and a dependency to read it would
    be the only one in the repository.
    """
    out: list[dict] = []
    current: dict | None = None
    for line in QUESTIONS.read_text().splitlines():
        if line.startswith("- q:"):
            current = {"q": line[len("- q:"):].strip()}
            out.append(current)
        elif current is not None and line.startswith("  ") and ":" in line:
            key, _, value = line.strip().partition(":")
            if key in ("concept", "pass", "trap"):
                current[key] = value.strip()
    return out


def corpus() -> str:
    index = BUILD / "llms.txt"
    if not index.exists():
        sys.exit("✖  build/llms.txt missing — run scripts/emit.py first")
    return index.read_text()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", action="store_true",
                       help="preamble + corpus, to paste once")
    group.add_argument("--ask", action="store_true",
                       help="the questions, one per line")
    group.add_argument("--sheet", action="store_true",
                       help="print the scoring sheet (redirect it to a file)")
    args = ap.parse_args()

    qs = questions()
    if not qs:
        sys.exit("✖  no questions parsed from evals/questions.yaml")

    if args.prompt:
        # No trailing newline: the question is pasted straight onto the slot.
        sys.stdout.write(PREAMBLE + corpus().rstrip("\n") + POSTAMBLE)
        return 0

    if args.ask:
        for i, q in enumerate(qs, 1):
            print(f"{i:2}. {q['q']}")
        return 0

    lines = [
        "# Validation pass — scoring sheet",
        "",
        "One question per section. Each goes in its OWN new session, given",
        "`--prompt` and nothing else — never several questions in one chat, or",
        "the model answers later ones from its earlier turns. No follow-ups, no",
        "hints, never name the concept. Read `trap` BEFORE writing a verdict.",
        "",
        "`PASS` the answer leads to **pass**, or defers to something that answers.",
        "`FAIL` the answer leads to **trap**, or is confidently wrong.",
        "",
        "Assistant under test: ______________    Date: ______________",
        "",
        "---",
        "",
    ]
    for i, q in enumerate(qs, 1):
        lines += [
            f"## {i}. {q['q']}",
            "",
            f"- **concept** — `{q.get('concept', '?')}`",
            f"- **pass** — {q.get('pass', '?')}",
            f"- **trap** — {q.get('trap', '?')}",
            "",
            "**Verdict:** PASS / FAIL",
            "",
            "**What it actually said:**",
            "",
            "> ",
            "",
            "---",
            "",
        ]
    lines += [
        "## Result",
        "",
        f"__ / {len(qs)} pass.",
        "",
        "A failure is a summary to rewrite, not a question to drop. Record which",
        "summary and what it failed to stop the model from concluding.",
        "",
    ]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
