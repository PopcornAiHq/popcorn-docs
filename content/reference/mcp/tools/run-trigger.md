---
id: mcp/tools/run-trigger
title: run_trigger
order: 345
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  Run one of a Routine's schedules now, with the inputs it runs with on
  schedule.
concepts: [triggers]
used_with: [mcp/tools/list-history, mcp/tools/list-triggers]
---

[writes] [destructive] [dry run]

```
run_trigger(routine_id, trigger, confirm=False, plan_id=None)
```

Its schedule is unchanged: the next scheduled run still happens. The run does what the schedule's work does, for real. Without confirm=true this is a dry run that starts nothing and says what will run. Each confirmed call starts a run, so don't repeat one that timed out: the run may have started. A started run comes back with its reference, which list_history's run follows.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `trigger` [required] | `str` | The schedule's name, as list_triggers shows it. |
| `confirm` | `bool` | true to start the run. Show the user the dry run first. Default `False`. |
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
It runs in the background. list_history with that run shows how it is going or how it ended, and the items it changed; each of those items' own History lists it too.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
