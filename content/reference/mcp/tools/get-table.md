---
id: mcp/tools/get-table
title: get_table
order: 320
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  A table's columns, in order: each one's name, type, label and merge policy,
  the table's merge key, and its state machine if the Routine runs one on it.
concepts: [tables]
used_with: [mcp/tools/create-rows, mcp/tools/update-row, mcp/tools/list-tables]
---

[read-only]

```
get_table(routine, table)
```

A merge policy says what a write that merges into an existing row does to that column: replace (the default), keep the first value, concat (append), or increment_on_change (a counter the store keeps). Columns marked as state change only when one of the state machine's transitions fires, so create_rows and update_row refuse them.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |

**Example** — “What columns does #intake's claims table have?”

```text
→ get_table(routine="#intake", table="claims")

Routine: #intake (c7d2…5b) · table: claims
Table: claims  (schema version 3)
Merge key: none; create_rows merges only on the columns its merge_on names.
Columns (11), in order:
- claim_no  string  label "Claim #"
- claimant  string  [personal data]
- amount  number
- Status  string  [state: changed only by transitions]
- Stage  string  [state: changed only by transitions]
- Decision  string  [fact a transition writes]
- Notes  string  merge: concat
- First seen  string  merge: keep
- api_token  string  [credential: never shown or written]
- home_address  string  [personal data]
- summary  string  [personal data]
State machine:
- Status column: Status · Actions: CTAs · sub: Stage
- funnel (column Stage): open, closed
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
