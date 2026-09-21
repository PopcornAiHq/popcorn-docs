#!/usr/bin/env python3
"""The docs MCP server — three read-only tools over the emitted corpus.

Thin by design. Every answer is computed in `retrieval`, which imports no SDK,
so what this file contains is the tool surface and nothing else. If a change
here needs a test, it belongs in `retrieval` instead.

Tools, and why there are three rather than one or ten:

    search_docs(query)   what is there about X — summaries only
    get_doc(id)          one concept in full
    explain(term)        what a word means here, answered in one call

`explain` is not a search with a different name. The caller has met a word
mid-task and needs its meaning; leading with the single best answer and naming
the alternatives underneath is a different shape from ranking five equals, and
it is the shape that ends the exchange in one round trip.

Tools rather than resources, against the specification's own suggestion that
documentation is resource-shaped. Resources are application-controlled, so
whether the model ever sees them is the host's choice, and the bar here is the
weakest host rather than the best one. The documentation servers that exist in
the wild made the same call.

Read-only, and it stays that way: nothing in this corpus is per-user, per-
workspace or writable, so there is no authenticated path to get wrong.
"""

from __future__ import annotations

import pathlib

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

import retrieval

CHUNKS = pathlib.Path(__file__).resolve().parent.parent / "build" / "chunks.json"

mcp = FastMCP("popcorn-docs")
_pages = retrieval.load(CHUNKS)

_READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False)


@mcp.tool(annotations=_READ_ONLY)
def search_docs(query: str, limit: int = 5) -> str:
    """Find Popcorn concepts matching a question or phrase.

    Returns each match's summary, never its full text — read one with get_doc.
    A query that matches nothing returns the nearest entries rather than an
    empty result.

    Args:
        query: a question, error message, or phrase
        limit: maximum results (default 5)
    """
    return retrieval.search(_pages, query, limit=limit)


@mcp.tool(annotations=_READ_ONLY)
def get_doc(doc_id: str) -> str:
    """Read one Popcorn concept in full, by its id.

    Args:
        doc_id: an id from search_docs, e.g. "fork-line"
    """
    return retrieval.get(_pages, doc_id)


@mcp.tool(annotations=_READ_ONLY)
def explain(term: str) -> str:
    """What a Popcorn term means — one answer, plus the near neighbours.

    For a word met mid-task ("concat", "bound", "fork line") where the question
    is what it means here, not what documents mention it.

    Args:
        term: the word or phrase to define
    """
    return retrieval.explain(_pages, term)


if __name__ == "__main__":
    mcp.run()
