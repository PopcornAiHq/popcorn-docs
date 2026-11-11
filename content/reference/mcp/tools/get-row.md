---
id: mcp/tools/get-row
title: get_row
order: 319
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  Show one row in full: every column, its rev, when it was created and last
  changed, and its state if the table has a state machine.
concepts: [tables]
used_with: [mcp/tools/update-row, mcp/tools/list-tables, mcp/tools/list-rows]
---

[read-only]

```
get_row(routine, table, row_id)
```

[`update_row`](https://docs.popcorn.ai/mcp/tools/update-row.md) needs the rev as `expected_rev`.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as [`list_tables`](https://docs.popcorn.ai/mcp/tools/list-tables.md) shows it. |
| `row_id` [required] | `int` | The row's ID, as [`list_rows`](https://docs.popcorn.ai/mcp/tools/list-rows.md) shows it ("row 88" is 88). |

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
