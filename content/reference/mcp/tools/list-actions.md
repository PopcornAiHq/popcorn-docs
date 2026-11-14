---
id: mcp/tools/list-actions
title: list_actions
order: 330
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-14
summary: >
  List the Actions a person can take on one of a Routine's items now: the
  buttons Popcorn shows on it, each with the Status it moves the item to.
concepts: [actions-and-status]
used_with: [mcp/tools/take-action, mcp/tools/list-rows]
---

[read-only]

```
list_actions(routine, row_id)
```

Which ones are offered depends on where the item stands; [`take_action`](https://docs.popcorn.ai/mcp/tools/take-action.md) takes one.

One that collects values lists their names, for `take_action`'s fields. Some are taken only in Popcorn; they're marked.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `row_id` [required] | `int` | The item's row ID in the Routine's main table, as [`list_rows`](https://docs.popcorn.ai/mcp/tools/list-rows.md) shows it ("row 88" is 88). |

**Example** — “What can I do with claim 4471 in #intake?”

```text
→ list_actions(routine="#intake", row_id=88)

Routine: #intake (c7d2…5b) · table: claims
Row 88 · Status: Open (open)
Actions offered now:
- Close claim  action: close  moves it to: Closed (closed)
- Ask for documents  action: ask_docs  [in Popcorn]
```
