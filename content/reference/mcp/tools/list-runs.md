---
id: mcp/tools/list-runs
title: list_runs
order: 334
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  The Routine's runs still going, newest first: the work each is doing, when
  it started and what started it, and its reference.
concepts: [history]
used_with: [mcp/tools/stop-run, mcp/tools/list-history]
---

[read-only]

```
list_runs(routine, cursor=None)
```

This is where a run a schedule or a webhook started is found before it has changed any item. stop_run takes a run's reference to stop it, and list_history with it follows the run.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What's running in #intake right now?”

```text
→ list_runs(routine="#intake")

Routine: #intake (c7d2…5b)
2 runs still going, newest first:
- chase tick: still running · run run_WzEs… · started 2026-10-18 09:00
- signing webhook: still running · run run_WzEs… · started 2026-10-18 08:58 by a webhook
stop_run with a run's reference stops it.
get_run with a run's reference shows it: its steps, outputs and how it ended; list_history with it, the items it changed.
list_history with an item's row_id shows that item's History, the runs that changed it among them.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
