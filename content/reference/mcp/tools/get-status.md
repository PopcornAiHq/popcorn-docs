---
id: mcp/tools/get-status
title: get_status
order: 320
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-05
summary: >
  Where a Routine's items stand: how many are at each Status, and what is
  waiting for a person, with why and the Actions that settle it (take_action
  takes one on the item's row).
concepts: [actions-and-status]
used_with: [mcp/tools/take-action, mcp/tools/list-rows, mcp/tools/list-actions]
---

[read-only]

```
get_status(routine)
```

Each Status shows its label (what Popcorn shows) and its stored value. list_rows shows the items at one Status, filtered on the value: filter={"Status": "<value>"}. list_actions shows what can be done with an item and take_action does it.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What needs my attention in #intake?”

```text
→ get_status(routine="#intake")

Routine: #intake (c7d2…5b) · table: claims
212 items, by Status (label: count, then the stored value):
- Open: 182  value "open"
- Needs adjuster review: 3  value "review"  [needs a person]
- Paid: 27  value "paid"
None at: Closed.
Waiting for a person (3, newest first, from table issues):
- Needs adjuster review  row 88  opened 2026-10-15
  Why: The roof photos show water damage the estimate leaves out.
- Needs adjuster review  row 91  opened 2026-10-14
  Why: Repair quote is above the $10,000 auto-approve limit.
- Needs adjuster review  row 97  opened 2026-10-09
  Why: Claimant disputes the deductible.
list_rows shows the items; list_actions and take_action act on one.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
