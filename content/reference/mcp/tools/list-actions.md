---
id: mcp/tools/list-actions
title: list_actions
order: 326
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  List the Actions a person can take on one of a Routine's items now, given
  where it stands: the buttons Popcorn shows on it, each with the Status it
  moves the item to. take_action takes one.
concepts: [actions-and-status]
used_with: [mcp/tools/take-action, mcp/tools/list-rows]
---

[read-only]

```
list_actions(routine, row_id)
```

Some Actions are taken only in Popcorn (a form to fill in, a document to sign, a request to the Routine's agent); they're listed and marked.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `row_id` [required] | `int` | The item's row ID in the Routine's main table, as list_rows shows it ("row 88" is 88). |

**Example** — “What can I do with claim 4471 in #intake?”

```text
→ list_actions(routine="#intake", row_id=88)

Routine: #intake (c7d2…5b) · table: claims
Row 88 · Status: Open (open)
Actions offered now:
- Close claim  action: close  moves it to: Closed (closed)
- Ask for documents  action: ask_docs  [in Popcorn]
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
