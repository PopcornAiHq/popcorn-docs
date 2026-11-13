---
id: mcp/tools/create-rows
title: create_rows
order: 313
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Add rows to one of a Routine's tables.
concepts: [tables]
used_with: [mcp/tools/update-row, mcp/tools/get-table, mcp/tools/list-rows, mcp/tools/list-tables]
---

[writes] [dry run]

```
create_rows(routine_id, table, rows, merge_on=None, confirm=False, plan_id=None)
```

**Dry run.** For an outside assistant, a call without `confirm=true` is a dry run that adds nothing: it says which rows would be added and which would merge into an existing row, and what an added row starts. A new row on the table the Routine's Statuses run on is a new item, and the Routine's work acts on it for real (on a Routine that sends email, its first email goes out on the next run). Rows the person named themselves, up to 10, are added at once with `confirm=true`. For rows you composed (from a file, a page or a guess), or more than 10, show the person the dry run and confirm once they agree; more than 10 are added only with the `plan_id` that dry run gives.

**A Routine's own agent.** A Routine's own agent in Popcorn gets no dry run: every call of its adds the rows, confirm or not, as [`update_row`](https://docs.popcorn.ai/mcp/tools/update-row.md) does. Call it only for rows a member asked for.

**Merging.** A row whose merge key matches an existing row merges into it instead of adding another: the table's own merge key if it has one ([`get_table`](https://docs.popcorn.ai/mcp/tools/get-table.md) shows it), else the columns `merge_on` names. A merge on `merge_on` changes only the columns the row carries, each by the column's merge policy. A merge on the table's own key follows that key's setting: merge works the same way, but replace overwrites the matched row whole, emptying every column the new row leaves out (refused where that would erase the row's state or a credential). The confirmed response says which rows were added and which merged.

**Refused columns.** Columns the Routine's state machine owns are refused (they change only by an Action or the Routine's own work), and so are credential columns. Each confirm adds its rows: if one timed out, check with [`list_rows`](https://docs.popcorn.ai/mcp/tools/list-rows.md) before sending it again.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `table` [required] | `str` | The table's name, as [`list_tables`](https://docs.popcorn.ai/mcp/tools/list-tables.md) shows it. |
| `rows` [required] | `list[dict[str, Any]]` | The rows, each an object of column: value. At most 50. |
| `merge_on` | `list[str]` | Columns that identify an existing row to merge into, for a table with no merge key of its own. A row matches only when all of them match, so every row must carry every one of them. |
| `confirm` | `bool` | true to add the rows: at once for up to 10 the person named, otherwise after the dry run, sending the same rows and `merge_on` as it did. Default `False`. |
| `plan_id` | `str` | The `plan_id` the dry run gave for more than 10 rows, with `confirm=true` and the same rows and `merge_on`. |

**Example** — “Add claim 5002 for Kim, $900, to #intake, and update 4471's amount to 13,000 while you're at it.”

```text
→ create_rows(routine_id="c7d2…5b", table="claims", rows=[{"claim_no": "5002", "claimant": "Kim", "amount": 900}, {"claim_no": "4471", "amount": 13000}], merge_on=["claim_no"])

Routine: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Add 2 rows to claims; each row sent, in order:
- 1: added
- 2: merges into row 88 (on claim_no)
- Each added row is a new item: it shows its Status and Actions as soon as it's added, and the Routine's own work picks it up on its next run (list_triggers shows what runs and when). What that work does with it is real: on a Routine that sends email, the item's first email.
- A merge changes an existing item's columns; its Status changes only by an Action or the Routine's own work.

Call again with `confirm=true` to add them, sending the same rows.

→ create_rows(routine_id="c7d2…5b", table="claims", rows=[{"claim_no": "5002", "claimant": "Kim", "amount": 900}, {"claim_no": "4471", "amount": 13000}], merge_on=["claim_no"], confirm=true)

Routine: #intake (c7d2…5b) · table: claims
Added 1 row and merged 1 into existing rows:
- row 301  added
- row 88  merged into the existing row
get_row shows one in full.
```
