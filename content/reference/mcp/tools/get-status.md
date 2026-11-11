---
id: mcp/tools/get-status
title: get_status
order: 322
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  Where a Routine stands: what its template reports, how many items are at
  each Status, and what is waiting for a person.
concepts: [actions-and-status]
used_with: [mcp/tools/take-action, mcp/tools/list-actions, mcp/tools/list-rows, mcp/tools/get-table]
---

[read-only]

```
get_status(routine)
```

Start here for "where are we": a template that keeps its own summary of the work (a project brief, say) reports it first, under what it means. Each item waiting for a person comes with why, and the Actions that settle it.

[`take_action`](https://docs.popcorn.ai/mcp/tools/take-action.md) takes one of an item's Actions on the row it names; [`list_actions`](https://docs.popcorn.ai/mcp/tools/list-actions.md) shows what can be done with an item.

Each Status shows its label (what Popcorn shows) and its stored value. [`list_rows`](https://docs.popcorn.ai/mcp/tools/list-rows.md) shows the items at one Status with a filter on the Status column's stored value ([`get_table`](https://docs.popcorn.ai/mcp/tools/get-table.md) names the column; it isn't always "Status").

It counts up to 40 Statuses (those needing a person first) and lists the 10 newest items waiting. A Routine whose template has no Statuses and reports nothing is refused; `list_rows` reads its rows.

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
