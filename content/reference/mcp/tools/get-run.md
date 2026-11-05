---
id: mcp/tools/get-run
title: get_run
order: 318
group: MCP
parent: mcp/tools
updated: 2026-11-05
summary: >
  One of a Routine's runs, by its reference: how it is going or how it ended,
  what started it, its inputs and outputs, the error it failed with, and its
  newest steps.
concepts: [history]
used_with: [mcp/tools/list-history, mcp/tools/run-trigger, mcp/tools/take-action, mcp/tools/list-runs]
---

[read-only]

```
get_run(routine, run, output=None, cursor=None, wait_seconds=0)
```

A run still going shows the step it's on; call again to follow it, or pass wait_seconds to have this call wait for it to end. Outputs too long to show together are listed by name; output=<name> reads one whole, a range at a time when it is long. list_history with run shows the items it changed.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `run` [required] | `str` | The run's reference: run_trigger and take_action give it, and list_runs and list_history show it. |
| `output` | `str` | One output's name, to read just that output whole. |
| `cursor` | `str` | next_cursor from the previous range of that output. |
| `wait_seconds` | `int` | Wait up to this many seconds for a run still going to end, then answer; the answer says whether it ended or the wait ran out. At most 20 (more is read as 20); 0, the default, doesn't wait. With output, the wait comes first. |

**Example** — “How did the chase turn on row 88 in #intake go?”

```text
→ get_run(routine="#intake", run="run_WzEsIndmLWNoYXNlLTEiLCJyLWMxIl0")

Routine: #intake (c7d2…5b)
Run:
- chase turn: succeeded · started 2026-10-14 09:04 by another run · ended 2026-10-14 09:05
Steps, newest first:
- apply · completed · 1.2s
- assess · completed · 0.8s
- load_item · completed · 0.4s
list_history with this run shows the items it changed.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
