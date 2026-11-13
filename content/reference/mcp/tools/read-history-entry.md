---
id: mcp/tools/read-history-entry
title: read_history_entry
order: 348
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  One change from an item's History, in full: every field it changed, before
  and after, and who or what made it and why.
concepts: [history]
used_with: [mcp/tools/list-history]
---

[read-only]

```
read_history_entry(routine, entry_id)
```

When Popcorn's work made it, it also shows what that run did, in order, and how it ended.

Only the fields the change touched are shown, not the whole item. An email turn [`list_history`](https://docs.popcorn.ai/mcp/tools/list-history.md) shows has no `entry_id` and isn't read here.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `entry_id` [required] | `int` | The entry's ID, as `list_history` shows it ("`entry_id` 6" is 6). |

**Example** — “Show me entry 6 of row 88's history in #intake in full: what changed and what the run did.”

```text
→ read_history_entry(routine="#intake", entry_id=6)

Routine: #intake (c7d2…5b) · table: clients
Item: row 88
- 2026-10-17 15:00 · Popcorn, for a person (cta apply): Send retainer (entry_id 6)
  Status: Needs review → Retainer sent
  Why: Retainer sent; waiting for the signature.
Each field it changed, before → after:
- Status: Needs review → Retainer sent
- Why: Answers are in; check them before the retainer goes out. → Retainer sent; waiting for the signature.
- Retainer Sent At: 2026-10-17T15:00:00+00:00
The run that made it:
- cta apply: succeeded · started 2026-10-17 14:59 by a person's button · ended 2026-10-17 15:00
  What it did, in order:
  - load item: completed · 0.4s
  - send retainer: completed · 0.8s · attempt 2 · the signing provider didn't answer in time
  - apply: completed · 1.2s
A run a person's button started shows as Popcorn, for a person: runs don't record who pressed it.
```
