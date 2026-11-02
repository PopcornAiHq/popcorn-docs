---
id: mcp/tools/update-row
title: update_row
order: 344
group: MCP
parent: mcp/tools
updated: 2026-11-01
summary: >
  Change some columns of one row.
concepts: [tables]
used_with: [mcp/tools/get-row, mcp/tools/list-tables]
---

[writes] [idempotent]

```
update_row(routine_id, table, row_id, data, expected_rev)
```

Only the columns in data change; the rest stay as they are. Each changes by its merge policy, and the response names any column where that policy, not the value sent, decided what's stored. expected_rev is the rev get_row shows. If the row has changed since (its rev moved on), nothing is written and the response shows the row as it is now, with its new rev, so you can decide again. Changing a row starts no work. Columns the Routine's state machine owns are refused (they change only by a transition), and so are credential columns.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_id` [required] | `int` | The row's ID ("row 88" is 88). |
| `data` [required] | `dict[str, Any]` | The columns to change, as column: value. |
| `expected_rev` [required] | `int` | The row's rev, from get_row. |

**Example** — “Add a note to claim 4471 in #intake that the adjuster called back.”

```text
→ update_row(routine_id="c7d2…5b", table="claims", row_id=88, data={"Notes": "Adjuster called back 10/6."}, expected_rev=4)

Routine: #intake (c7d2…5b) · table: claims
Changed row 88: rev 4 → 5.
Where the table's merge policy decided what's stored:
- Notes: the value sent was appended to the stored text (merge: concat).
The row as stored:
- claim_no: 4471
- claimant: Ortiz
- amount: 12400
- Status: open
- Stage: open
- Decision: (empty)
- Notes: Claimant called 9/28.
  Adjuster called back 10/6.
- First seen: (empty)
- api_token: [hidden: holds a credential]
- home_address: 12 Elm St
- summary: Ortiz called about the roof
```

The [MCP server](https://docs.popcorn.ai/mcp.md) page has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
