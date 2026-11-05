---
id: mcp/tools/delete-rows
title: delete_rows
order: 311
group: MCP
parent: mcp/tools
updated: 2026-11-05
summary: >
  Delete rows from one of a Routine's tables, by ID.
concepts: [tables]
used_with: [mcp/tools/list-tables]
---

[writes] [destructive] [idempotent] [dry run]

```
delete_rows(routine_id, table, row_ids, confirm=False, plan_id=None)
```

Without confirm=true this is a dry run that deletes nothing: it lists the rows it would delete. With a person there, show them the dry run, and confirm only once they agree. A deleted row can't be restored with these tools. Rows are deleted one at a time, and the response says which were deleted, which were already gone and which failed.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_ids` [required] | `list[int]` | The rows' IDs ("row 88" is 88). At most 50. |
| `confirm` | `bool` | true to delete. With a person there, show them the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same table and row_ids. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Delete the duplicate row 91 from #intake's claims.”

```text
→ delete_rows(routine_id="c7d2…5b", table="claims", row_ids=[91])

Routine: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Delete 1 row from claims:
- row 91  claim_no: 44710  claimant: Lee  amount: 900  (updated 2026-09-29 14:05)
- Warning: the Routine's state machine runs on this table; a deleted row leaves the Routine's tracker and its open items.
- A deleted row can't be restored with these tools. Deleting starts no work.

Call again with `confirm=true` to delete this row.

→ delete_rows(routine_id="c7d2…5b", table="claims", row_ids=[91], confirm=true)

Routine: #intake (c7d2…5b) · table: claims
Deleted 1 of 1 rows: row 91.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
