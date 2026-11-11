---
id: mcp/tools/list-memories
title: list_memories
order: 330
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  List the memories kept for a Routine, the workspace or you, most recently
  changed first: what people told an agent and what templates keep.
concepts: []
used_with: [mcp/tools/get-memory]
---

[read-only]

```
list_memories(routine=None, scope="routine", category=None, cursor=None)
```

People's preferences, decisions and feedback are kept here. A template keeps its own in categories named feature:name, such as autochat:day. Popcorn's own working state (the plan, knowledge-base pages, the inbox scan's) isn't shown for a Routine or the workspace.

Without category, the first page lists each category with its count and last change, then the newest memories across them; with one, that category's. Each row is the memory's name (category/key, or category/short ID for one saved without a key), when it last changed and the start of its text; [`get_memory`](https://docs.popcorn.ai/mcp/tools/get-memory.md) shows one whole.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` | `str` | Routine name ("#intake") or ID, for scope "routine". |
| `scope` | `Scope` | "routine" (the default) for the Routine's own memory, "workspace" for what every Routine in the workspace shares (a guest can't read it), or "me" for your own. Leave out routine for "workspace" and "me". |
| `category` | `str` | Only this category, e.g. "preferences". |
| `cursor` | `str` | `next_cursor` from the previous page. |

**Example** — “What does #intake's agent remember?”

```text
→ list_memories(routine="#intake")

Routine: #intake (c7d2…5b) · memory
Categories (4):
- autochat:channel  1 memory, last changed 2026-11-05 03:00
- autochat:day  1 memory, last changed 2026-11-05 02:00
- decisions  1 memory, last changed 2026-11-02 09:00
- preferences  1 memory, last changed 2026-11-04 09:00
4 of 4 memories, newest first:
- autochat:channel/picture  2026-11-05 03:00: #intake is where Acme's claims team takes in new water-damage claims. Dana answers most of them; adjusters step in for anything over $2,000.
- autochat:day/2026-11-04  2026-11-05 02:00: Six new claims; two waiting on photos.
- preferences/00000003  2026-11-04 09:00: Mrs. Ortiz prefers a call after 5pm.
- decisions/00000004  2026-11-02 09:00: Water damage under $2,000 skips the adjuster call.
```
