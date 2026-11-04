---
id: mcp/tools/list-rows
title: list_rows
order: 332
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  List a table's rows, newest first unless sort says otherwise.
concepts: [tables]
used_with: [mcp/tools/get-row, mcp/tools/list-tables, mcp/tools/get-table]
---

[read-only]

```
list_rows(routine, table, query=None, filter=None, columns=None, sort=None, cursor=None)
```

Each row shows its ID, a few columns (long values are cut and marked; get_row shows a row in full) and when it last changed.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `query` | `str` | Text to find in any column, case-insensitively: "4471" finds the row whatever column holds it. Only rows where it appears in a value you can see are listed, so with query (or filter["*"]) a page can come back short, there's no total, and next_cursor goes on to the rest. |
| `filter` | `dict[str, Any]` | Conditions on columns, all of which must hold: {"Status": "open"} or {"Status": {"$eq": "open"}}, {"amount": {"$gt": 1000}}, {"claimant": {"$contains": "ortiz"}}, {"Status": {"$in": ["open", "waiting"]}}, {"closed_at": {"$exists": false}}. Operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $exists, $contains. There's no $or. Text compares case-insensitively. |
| `columns` | `list[str]` | The columns to show, by name. By default, the first few in the table's order (get_table lists them). |
| `sort` | `str` | "column:asc" or "column:desc". By default, newest first. On a workspace that guards personal data, a column whose values are hidden can't be sorted on. |
| `cursor` | `str` | next_cursor from the previous page, with the same other arguments. When the rows end exactly at a page's end, the last page comes back empty. |

**Example** — “Find claim 4471 in #intake.”

```text
→ list_rows(routine="#intake", table="claims", query="4471")

Routine: #intake (c7d2…5b) · table: claims
Columns shown: claim_no, claimant, amount, Status, Stage (of 11; columns=[…] picks others). Empty values are left out.
2 rows matching "4471", newest first, shown on this page:
- row 91  claim_no: 44710  claimant: Lee  amount: 900  (updated 2026-09-29 14:05)
- row 88  claim_no: 4471  claimant: Ortiz  amount: 12400  Status: open  Stage: open  (updated 2026-09-29 14:05)
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
