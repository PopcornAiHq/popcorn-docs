---
id: mcp/tools/run-trigger
title: run_trigger
order: 346
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-05
summary: >
  Run one of a Routine's schedules now, with the inputs it runs with on
  schedule.
concepts: [triggers]
used_with: [mcp/tools/get-run, mcp/tools/list-history, mcp/tools/list-triggers]
---

[writes] [destructive] [dry run]

```
run_trigger(routine_id, trigger, confirm=False, plan_id=None)
```

Its schedule is unchanged: the next scheduled run still happens. The run does what the schedule's work does, for real. Without confirm=true this is a dry run that starts nothing and says what will run. Each confirmed call starts a run, so don't repeat one that timed out: the run may have started. A started run comes back with its reference: get_run with it shows how it is going or how it ended, and list_history with it the items it changed.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `trigger` [required] | `str` | The schedule's name, as list_triggers shows it. |
| `confirm` | `bool` | true to start the run: at once when the person asked to run this schedule now, otherwise after they agree to the dry run. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same request. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Send #intake's morning digest now; don't wait.”

```text
→ run_trigger(routine_id="c7d2…5b", trigger="morning")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Run: the morning schedule's work on #intake, now.
- Schedule: cron '0 8 * * 1-5' (America/Los_Angeles); unchanged by this run.
- It runs as it would on schedule, in the background: posts, emails and row changes are real.

Call again with `confirm=true` to run it now.

→ run_trigger(routine_id="c7d2…5b", trigger="morning", confirm=true)

Routine: #intake (c7d2…5b)
Started the morning schedule's work.
Run: run_WzEs…
It runs in the background. get_run with that run shows how it is going or how it ended, and list_history with it the items it changed; each of those items' own History lists it too. Work it hands to runs of their own is in list_runs.
```

The [Tools](https://docs.popcorn.ai/mcp/tools.md) page has what every tool
shares: `routine` and `routine_id`, dry runs and `confirm=true`, and paging
with `next_cursor`.
