#!/usr/bin/env python3
"""Run the validation set against the Gemini API and print a transcript to grade.

This automates the half of the pass that was only ever tedium: pasting the
prompt into a fresh session once per question. Each question is one stateless
`generateContent` call — a new session by construction, so no answer can lean
on an earlier turn, and the model has no browsing tool with which to fetch the
page bodies the reference only links to.

Judging stays with a model, not a string match, because "does this answer lead
to the fix" is not a pattern. The output is a transcript meant to be handed,
whole, to a different model to grade in one pass: the grading instructions, the
scoring rules copied from `evals/questions.yaml`, the exact prompt Gemini saw,
for every question its rubric and Gemini's verbatim response, and — for the
grader alone — every page in full, so a deferral can be checked against the
page it names. Grade with a model from another family than the one answering,
so the grader is not marking its own habits.

    GEMINI_API_KEY=… python3 scripts/eval-run.py > ~/gemini-run.md
    python3 scripts/eval-run.py --only 3,6,7 > ~/gemini-run.md
    python3 scripts/eval-run.py --list-models

The key comes from `$GEMINI_API_KEY`, or else from the `gemini_api_key` field
of `~/.config/popcorn-docs/eval.json` (or `--config`), which may also name a
`model`. The config lives outside the repository on purpose: this repository
is public, and a key file inside it is one `git add -A` from being published.

The transcript goes to stdout and progress to stderr, so redirect stdout
somewhere outside the repository — never into `build/`, which is published
whole. Like `eval-kit.py`, the corpus is read from `build/`: run
`scripts/emit.py` first, so what is graded is what would be published.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG = pathlib.Path.home() / ".config" / "popcorn-docs" / "eval.json"
API = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-3.8-flash"

# 429 and 5xx are the API asking for patience; anything else is an answer.
RETRYABLE = {429, 500, 502, 503, 504}
ATTEMPTS = 5


def _kit():
    """`eval-kit.py`, whose prompt and question parser this must not fork.

    Imported by path because the hyphenated filename is not importable by
    name. Sharing it is the point: a second copy of the preamble would drift,
    and then the automated pass and the manual one would test different
    prompts while reporting the same score.
    """
    spec = importlib.util.spec_from_file_location("eval_kit", ROOT / "scripts" / "eval-kit.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scoring_rules() -> str:
    """The scoring block from the header of `evals/questions.yaml`, uncommented.

    Read rather than restated, so the grader is held to the rules the set was
    written against and a change to them reaches both passes at once.
    """
    lines = (ROOT / "evals" / "questions.yaml").read_text().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("# Scoring,"))
    end = next(i for i, l in enumerate(lines[start:], start) if "is not testing anything" in l)
    return "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in lines[start:end + 1])


def api_key(config: pathlib.Path) -> tuple[str, dict]:
    settings: dict = {}
    if config.exists():
        try:
            settings = json.loads(config.read_text())
        except json.JSONDecodeError as exc:
            sys.exit(f"✖  {config} is not valid JSON: {exc}")
    key = os.environ.get("GEMINI_API_KEY") or settings.get("gemini_api_key")
    if not key:
        sys.exit(
            f"✖  no API key — set GEMINI_API_KEY, or put "
            f'{{"gemini_api_key": "…"}} in {config}'
        )
    return key, settings


def call(url: str, key: str, body: dict | None = None) -> dict:
    """One request, retried with backoff on the statuses that mean "later"."""
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(ATTEMPTS):
        request = urllib.request.Request(
            url,
            data=data,
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            method="POST" if data else "GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            if exc.code in RETRYABLE and attempt < ATTEMPTS - 1:
                time.sleep(2 ** attempt * 2)
                continue
            raise RuntimeError(f"HTTP {exc.code}: {detail[:500]}") from None
        except urllib.error.URLError as exc:
            if attempt < ATTEMPTS - 1:
                time.sleep(2 ** attempt * 2)
                continue
            raise RuntimeError(f"network error: {exc.reason}") from None
    raise AssertionError("unreachable")


def ask(model: str, key: str, prompt: str) -> str:
    """One question in one fresh session: a single user turn, no history."""
    result = call(
        f"{API}/models/{model}:generateContent",
        key,
        {"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
    )
    candidates = result.get("candidates") or []
    if not candidates:
        reason = result.get("promptFeedback", {}).get("blockReason", "no candidates")
        return f"[no response: {reason}]"
    parts = candidates[0].get("content", {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought")).strip()
    return text or f"[empty response: {candidates[0].get('finishReason', 'unknown')}]"


GRADER_BRIEF = """\
You are grading a validation pass over a documentation corpus. Another model
(the answerer) was given the prompt below, once per entry, each in a fresh
session with no other context, and answered. Grade every entry in one pass.

For each entry you have the question or problem report, a `pass` condition, a
`trap`, and the answerer's verbatim response. Apply the scoring rules exactly
as written. In particular:

- Score the ACTION the response leads the reader to, not how well it reads.
- A deferral ("read <entry> in full") passes only if the entry it names
  actually answers the question. The appendix holds every entry's full body so
  you can check; the answerer never saw it. A deferral to an entry whose body
  does not answer the question is a FAIL (misroute).
- A response can reach the right diagnosis and still recommend a wrong step.
  Ask what a reader who followed it would DO. If that is the wrong thing — an
  operation that does not do what the response claims — it is a FAIL, however
  right the diagnosis. A wrong detail that would not change what they do is a
  PASS; list it under the wrong details below.

Output one line per entry, then a total:

    #<n>  PASS | PASS (deferral) | FAIL  —  <one-line reason>
          <for a FAIL: quote the exact sentence at fault>

    Total: <passes> / <entries>

Then list, separately, any entry that passed but contains a wrong detail worth
fixing in the reference, quoting the sentence. Do not rewrite the reference.
"""


def transcript(
    prompt: str, rules: str, entries: list[tuple[int, dict, str]], model: str, bodies: str
) -> str:
    out = [
        "# Validation pass — transcript for grading",
        "",
        f"Answerer: `{model}` via the Gemini API, one stateless call per entry.",
        "",
        "## Grading instructions",
        "",
        GRADER_BRIEF,
        "## Scoring rules (from evals/questions.yaml)",
        "",
        "```",
        rules,
        "```",
        "",
        "## The prompt the answerer saw",
        "",
        "Each entry's question was appended to this, after the final label.",
        "",
        "````",
        prompt,
        "````",
        "",
        "## Entries",
        "",
    ]
    for n, q, answer in entries:
        out += [
            f"### #{n}. {q['q']}",
            "",
            f"- **concept** — `{q.get('concept', '?')}`",
            f"- **pass** — {q.get('pass', '?')}",
            f"- **trap** — {q.get('trap', '?')}",
            "",
            "**Response:**",
            "",
            "````",
            answer,
            "````",
            "",
        ]
    # The bodies are for judging deferrals only: whether the entry an answer
    # points at really answers it cannot be told from a summary, which is the
    # very thing under test.
    out += [
        "## Appendix — every entry in full (the answerer did NOT see this)",
        "",
        "`````",
        bodies,
        "`````",
        "",
    ]
    return "\n".join(out)


def selected(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    picked = []
    for token in spec.split(","):
        token = token.strip()
        if "-" in token:
            lo, hi = token.split("-", 1)
            picked += range(int(lo), int(hi) + 1)
        elif token:
            picked.append(int(token))
    bad = [n for n in picked if not 1 <= n <= total]
    if bad:
        sys.exit(f"✖  no such question: {bad} (the set has {total})")
    return sorted(set(picked))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="question numbers to run, e.g. 3,6,7 or 1-5")
    ap.add_argument("--model", help=f"Gemini model id (default: config, else {DEFAULT_MODEL})")
    ap.add_argument("--config", type=pathlib.Path, default=CONFIG, help=f"config file (default: {CONFIG})")
    ap.add_argument("--list-models", action="store_true", help="list the models this key can call, and exit")
    args = ap.parse_args()

    key, settings = api_key(args.config)
    model = args.model or settings.get("model") or DEFAULT_MODEL

    if args.list_models:
        names = []
        url = f"{API}/models?pageSize=1000"
        while url:
            page = call(url, key)
            names += [
                m["name"].removeprefix("models/")
                for m in page.get("models", [])
                if "generateContent" in m.get("supportedGenerationMethods", [])
            ]
            token = page.get("nextPageToken")
            url = f"{API}/models?pageSize=1000&pageToken={token}" if token else None
        print("\n".join(sorted(names)))
        return 0

    kit = _kit()
    qs = kit.questions()
    prompt = kit.PREAMBLE + kit.corpus().rstrip("\n") + kit.POSTAMBLE
    numbers = selected(args.only, len(qs))

    entries = []
    for n in numbers:
        q = qs[n - 1]
        print(f"  #{n:<2} {q['q']}", file=sys.stderr)
        try:
            answer = ask(model, key, prompt + q["q"])
        except RuntimeError as exc:
            # One failed call should not throw away the rest of the run; the
            # grader sees it and scores nothing for it.
            answer = f"[request failed: {exc}]"
            print(f"      ✖ {exc}", file=sys.stderr)
        entries.append((n, q, answer))

    bodies = (kit.BUILD / "llms-full.txt").read_text().rstrip("\n")
    print(transcript(prompt, scoring_rules(), entries, model, bodies))
    failed = sum(a.startswith("[request failed") for _, _, a in entries)
    print(f"✔  {len(entries) - failed} of {len(entries)} answered by {model}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
