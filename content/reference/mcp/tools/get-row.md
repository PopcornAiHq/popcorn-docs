---
id: mcp/tools/get-row
title: get_row
order: 316
group: MCP
parent: mcp/tools
updated: 2026-11-01
summary: >
  One row in full: every column, its rev (update_row needs it as
  expected_rev), when it was created and last changed, and its state if the
  Routine's state machine runs on the table.
concepts: [tables]
used_with: [mcp/tools/update-row, mcp/tools/list-tables, mcp/tools/list-rows]
---

[read-only]

```
get_row(routine, table, row_id)
```

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_id` [required] | `int` | The row's ID, as list_rows shows it ("row 88" is 88). |

**Example** — “Show me everything on row 88 of #intake's claims.”

```text
→ get_row(routine="#intake", table="claims", row_id=88)

Routine: #intake (c7d2…5b) · table: claims
Row: 88  rev: 4  created 2026-09-01 10:00  updated 2026-09-29 14:05
State: Status = Open (open) · Stage = Open (open)
- claim_no: 4471
- claimant: Ortiz
- amount: 12400
- Status: open
- Stage: open
- Decision: (empty)
- Notes: (empty)
- First seen: (empty)
- api_token: [hidden: holds a credential]
- home_address: 12 Elm St
- summary: Ortiz called about the roof
```

The [MCP server](https://docs.popcorn.ai/mcp.md) page has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
