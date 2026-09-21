"""Retrieval over the emitted corpus. No MCP import, on purpose.

The tools this backs are meant to be mechanical — the assistant does the
interpreting, the server returns facts — so the whole of that behaviour is
plain functions here, testable without an SDK or a transport. `docs_mcp` is
the thin wiring that exposes them.

Three rules shape every return value, and they come from what a tool result
costs rather than from taste:

* **Search returns summaries, never bodies.** A result lands in the caller's
  context whole; there is no side channel. Returning prose from a search is
  how the budget goes, and a summary is what makes the second call optional.
* **Nothing returns an empty result.** An empty list reads as "no such thing"
  when the truth is usually "not by that name", so a miss returns the nearest
  entries and says that is what it did.
* **Every return names the next call.** The caller cannot explore; the answer
  has to carry the way forward.
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any

_WORD = re.compile(r"[a-z0-9]+")
_STOP = frozenset(
    "a an and are as at be by do does for from how i in is it my of on or "
    "that the to was what when where which why with you your".split()
)


def load(path: pathlib.Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text())["pages"]


def _stem(word: str) -> str:
    """Crude suffix stripping, and crude is the right amount.

    A question is asked in whatever tense the asker is in — "delete every
    schedule" against a summary that says "deletes every one", "stops me
    publishing" against one that says "publish is ungated". Without this the
    two never meet, and the miss is invisible: the caller gets a confident
    answer from the wrong page rather than nothing.

    A real stemmer would be more accurate and is not worth a dependency here;
    over-stemming two words into one costs a slightly worse ranking, while
    under-stemming costs the answer.
    """
    for suffix in ("ing", "es", "ed", "s"):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def _terms(text: str) -> set[str]:
    return {
        _stem(w) for w in _WORD.findall(text.lower()) if w not in _STOP
    }


def _score(page: dict[str, Any], terms: set[str]) -> int:
    """Weighted by where a term hits, not by how often.

    Frequency would reward a long body, which is the opposite of what should
    rank: the pages that answer in one call are the short ones.
    """
    if not terms:
        return 0
    ident = _terms(page["id"]) | _terms(page["title"])
    summary = _terms(page["summary"])
    body = _terms(page.get("body", ""))
    return (
        8 * len(terms & ident)
        + 4 * len(terms & summary)
        + 1 * len(terms & body)
    )


def search(pages: list[dict], query: str, limit: int = 5) -> str:
    terms = _terms(query)
    ranked = sorted(pages, key=lambda p: _score(p, terms), reverse=True)
    hits = [p for p in ranked if _score(p, terms)][:limit]

    if hits:
        head = f"{len(hits)} result(s) for {query!r}."
    else:
        # Never an empty hand. A caller who cannot explore reads "no results"
        # as "the corpus has nothing", which is almost never what happened.
        hits = ranked[:limit]
        head = (
            f"Nothing matched {query!r} directly. "
            f"The {len(hits)} entries nearest to it:"
        )

    lines = [head, ""]
    for page in hits:
        lines += [f"## {page['title']}  (id: {page['id']})", page["summary"], ""]
    lines.append("Read one in full with get_doc(id).")
    return "\n".join(lines)


def get(pages: list[dict], doc_id: str) -> str:
    page = next((p for p in pages if p["id"] == doc_id), None)
    if page is None:
        known = ", ".join(sorted(p["id"] for p in pages))
        return (
            f"No concept has the id {doc_id!r}.\n\n"
            f"Known ids: {known}\n\n"
            "Search instead with search_docs(query)."
        )

    related = ", ".join(page.get("concepts", []))
    out = [f"# {page['title']}", "", page["summary"], "", page["body"]]
    if related:
        out += ["", f"Related: {related} — read one with get_doc(id)."]
    return "\n".join(out)


def explain(pages: list[dict], term: str) -> str:
    """The vocabulary question, answered without a second call.

    Distinct from search because the caller is not browsing: it has met a word
    and needs what it means here. So this leads with the one best answer and
    names the alternatives underneath, rather than ranking them as equals.
    """
    terms = _terms(term)
    ranked = sorted(pages, key=lambda p: _score(p, terms), reverse=True)
    best, rest = ranked[0], ranked[1:3]

    lines = [
        f"{term!r} in Popcorn:",
        "",
        f"**{best['title']}** — {best['summary']}",
        "",
    ]
    if rest:
        lines.append("Related terms, if that is not the sense you meant:")
        lines += [f"  - {p['title']} ({p['id']}): {p['summary']}" for p in rest]
        lines.append("")
    lines.append(f"Full explanation: get_doc({best['id']!r}).")
    return "\n".join(lines)
