---
id: mcp/tools/stop-run
title: stop_run
order: 358
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Stop one of a Routine's runs that's still going.
concepts: [history]
used_with: [mcp/tools/run-trigger, mcp/tools/take-action, mcp/tools/list-runs, mcp/tools/list-history]
---

[writes] [destructive] [idempotent]

```
stop_run(routine_id, run)
```

The run stops at its next step, so a step already under way finishes, and what the run already did (items changed, messages posted) stays done: nothing is undone. A run that already ended is left as it was, so calling again is safe. Only stop a run the person asked you to stop.

A guest can't stop runs; a member or admin can, in an archived Routine too.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `run` [required] | `str` | The run's reference: [`run_trigger`](https://docs.popcorn.ai/mcp/tools/run-trigger.md) and [`take_action`](https://docs.popcorn.ai/mcp/tools/take-action.md) give it for the run they start, and [`list_runs`](https://docs.popcorn.ai/mcp/tools/list-runs.md) and [`list_history`](https://docs.popcorn.ai/mcp/tools/list-history.md) show it beside a run still going. |

**Example** — “Stop the claim tick I just started in #intake.”

```text
→ stop_run(routine_id="c7d2…5b", run="run_WzEsImFjbWUtaW50YWtlLWNsYWltX3RpY2stMjAyNi0xMC0wNlQwOTEyMDBaLWMzZDQiLCIwMTk5YjllNi01MWMyLTdhMDgtYjNmNC02ZTFkMmM5YTBiNzUiXQ")

Routine: #intake (c7d2…5b)
Stopping the run: it stops at its next step. list_history with this run shows when it has.
```
