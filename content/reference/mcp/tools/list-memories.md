---
id: mcp/tools/list-memories
title: list_memories
order: 329
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  List memories, newest first: what people told a Routine's agent
  (preferences, decisions, feedback) and what its template keeps there
  (categories named "<feature>:<name>", such as autochat:day).
concepts: []
used_with: [mcp/tools/get-memory]
---

[read-only]

```
list_memories(routine=None, scope="routine", category=None, cursor=None)
```

Without category, the first page lists each category with its count and last change, then the newest memories across them; with one, that category's. Each row is the memory's name (<category>/<key>), when it last changed and the start of its text; [`get_memory`](https://docs.popcorn.ai/mcp/tools/get-memory.md) shows one whole.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` | `str` | Routine name ("#intake") or ID, for scope "routine". |
| `scope` | `Scope` | "routine" (the default) for the Routine's own memory, "workspace" for what every Routine in the workspace shares (the Knowledge Base tab shows it), or "me" for your own. Leave out routine for "workspace" and "me". |
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
