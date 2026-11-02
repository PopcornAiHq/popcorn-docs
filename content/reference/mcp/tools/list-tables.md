---
id: mcp/tools/list-tables
title: list_tables
order: 332
group: MCP
parent: mcp/tools
updated: 2026-11-01
summary: >
  List the tables in a Routine, with each one's row count.
concepts: [tables]
used_with: [mcp/tools/get-table, mcp/tools/list-rows]
---

[read-only]

```
list_tables(routine, cursor=None)
```

A Routine's tables hold the rows its template, agents and people keep. get_table shows a table's columns; list_rows reads its rows.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What does #intake keep track of?”

```text
→ list_tables(routine="#intake")

Routine: #intake (c7d2…5b)
2 of 2 tables:
- claims  212 rows
- Contacts  3 rows
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
