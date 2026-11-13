---
id: mcp/tools/search-docs
title: search_docs
order: 355
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Search the Popcorn docs and get the best pages' titles, ids and summaries.
concepts: []
used_with: [mcp/tools/read-doc]
---

[read-only]

```
search_docs(query, limit=5)
```

The docs are docs.popcorn.ai. Search before building or changing a Routine Template: the docs cover manifest keys, flow activities, table columns and merge policy, schedules, state machines, and copying a template and publishing its versions, which these tools' descriptions don't. Also search when a term or an error names a concept you can't define exactly. [`read_doc`](https://docs.popcorn.ai/mcp/tools/read-doc.md) reads a page in full.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `query` [required] | `str` | What you want to know, in your own words or by name. |
| `limit` | `int` | How many pages to return, 1 to 10; default 5. Nothing is ever empty: with no match it returns the nearest pages, so try another name before concluding there's no such thing. |

**Example** — “If I publish a change to our copy of the intake template, which Routines does it reach?”

```text
→ search_docs(query="publish a version to a copy")

2 docs page(s) for 'publish a version to a copy':

## Versions: publishing and installing (id: versions)
A change reaches a Routine in two steps: publishing mints an immutable version of a Routine Template on its copy, and installing brings each Routine on the copy to it, the one published from at once and the rest on their daily update.

## Copying a template (id: copying-a-template)
Customizing a Routine beyond what its settings reach gives it a copy that the workspace owns (`popcorn app fork`). A copy comes before any publish, and a change published there reaches every Routine on it by their daily update, not only the one you changed. It is one-way: nothing undoes a copy or moves a Routine back to Popcorn's version.

Read one with read_doc(doc_id).
```
