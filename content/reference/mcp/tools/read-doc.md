---
id: mcp/tools/read-doc
title: read_doc
order: 343
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Read one page of the Popcorn docs by its id, or one section of it.
concepts: []
used_with: [mcp/tools/search-docs]
---

[read-only]

```
read_doc(doc_id, section=None)
```

[`search_docs`](https://docs.popcorn.ai/mcp/tools/search-docs.md) gives the id. A page too long to return whole (the activity and MCP references) comes back as an outline of its sections; read one with `section`.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `doc_id` [required] | `str` | The page's id, e.g. "manifest-keys" or "activities". |
| `section` | `str` | A heading on the page, e.g. "foundation.http.request"; the first heading that matches is read, with what's under it. |

**Example** — “Do I have to fork the template before I publish?”

```text
→ read_doc(doc_id="copying-a-template")

# Copying a template (id: copying-a-template)
https://docs.popcorn.ai/copying-a-template.md

Customizing a Routine beyond what its settings reach gives it a copy that the workspace owns (`popcorn app fork`). A copy comes before any publish, and a change published there reaches every Routine on it by their daily update, not only the one you changed. It is one-way: nothing undoes a copy or moves a Routine back to Popcorn's version.

A Routine made from a Routine Template runs Popcorn's own version of it.
To change what the Routine is built from, the workspace makes a copy of the
template: a series of versions the workspace owns, which it publishes to.

Related: customizing-a-routine, versions.
```
