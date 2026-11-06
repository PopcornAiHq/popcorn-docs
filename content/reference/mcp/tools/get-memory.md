---
id: mcp/tools/get-memory
title: get_memory
order: 314
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  One memory whole: its text, its category and name, when it was saved and
  last changed, and its metadata.
concepts: []
used_with: [mcp/tools/list-memories]
---

[read-only]

```
get_memory(memory, routine=None, scope="routine", cursor=None)
```

A very long one comes a range at a time, with a next_cursor for the rest.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `memory` [required] | `str` | The memory's name as list_memories shows it ("<category>/<key>", e.g. "autochat:channel/picture"), or its ID. |
| `routine` | `str` | Routine name ("#intake") or ID, for scope "routine". |
| `scope` | `Scope` | "routine" (the default), "workspace" or "me", as for list_memories. Leave out routine for "workspace" and "me". |
| `cursor` | `str` | next_cursor from the previous range of this memory. |

**Example** — “What's #intake's agent's picture of the channel?”

```text
→ get_memory(routine="#intake", memory="autochat:channel/picture")

Routine: #intake (c7d2…5b) · memory
Memory: autochat:channel/picture
ID: 0000…03
Created: 2026-11-05 03:00
Last changed: 2026-11-05 03:00
Metadata: {"date": "2026-11-05", "key": "picture"}
Text, 140 characters:
#intake is where Acme's claims team takes in new water-damage claims. Dana answers most of them; adjusters step in for anything over $2,000.
```

The [Tools](https://docs.popcorn.ai/mcp/tools.md) page has what every tool shares.
