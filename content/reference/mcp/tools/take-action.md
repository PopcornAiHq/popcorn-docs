---
id: mcp/tools/take-action
title: take_action
order: 359
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Take one Action on one or more of a Routine's items, as a person pressing
  its button in Popcorn would.
concepts: [actions-and-status]
used_with: [mcp/tools/list-actions, mcp/tools/get-run]
---

[writes] [destructive] [dry run]

```
take_action(routine_id, row_ids=None, action=None, confirm=False, run_key=None, plan_id=None)
```

One item the Action can't be taken on refuses the whole call, with the reason for each: the Action isn't offered on it now, or it's taken only in Popcorn ([`list_actions`](https://docs.popcorn.ai/mcp/tools/list-actions.md) marks those). So does a Connection the Routine's Actions need but doesn't have. Drop those items and call again.

Without `confirm=true` this is a dry run: it says what happens to each item and gives a `run_key`. To act, call again with the same items and action, `confirm=true` and that `run_key`. A `run_key` acts once: calling again with it finds the run it started. When the person named the items and the Action themselves, confirm at once, without a dry run or `run_key`; each such call starts its own run, so don't repeat one that timed out. The confirm returns at once with the Run: the Action applies in the background, and [`get_run`](https://docs.popcorn.ai/mcp/tools/get-run.md) shows how it went.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `row_ids` | `list[int]` | The items' row IDs in the Routine's main table, at most 50. Required, except on a confirm with a `plan_id`. |
| `action` | `str` | The Action, as `list_actions` names it (its "action"); its button label names it too. Required, except on a confirm with a `plan_id`. |
| `confirm` | `bool` | true to act: at once when the person named the items and the Action, otherwise after they agree to the dry run. Default `False`. |
| `run_key` | `str` | The `run_key` the dry run gave, with `confirm=true`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true`. It stands in for `row_ids`, action and the `run_key`: leave them out and the confirm takes the dry run's, or send them and they must be the same. A Routine's own agent in Popcorn must pass it, from a dry run in an earlier run; an assistant connected from outside Popcorn is given none and needn't. |

**Example** — “Close claim 4471 in #intake.”

```text
→ take_action(routine_id="c7d2…5b", row_ids=[88], action="close")

Routine: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Take: close on 1 item(s), now.
- row 88, Close claim: Open (open) → Closed (closed)
- It runs as the workspace's agent, for you, as the button would: what the Action sends or records is real.
- run_key: Hc4pW8sN…

Call again with `confirm=true` to take it, with run_key="Hc4pW8sN…" and the same items.

→ take_action(routine_id="c7d2…5b", row_ids=[88], action="close", confirm=true, run_key="Hc4pW8sNz1bVq6Tj20d155d5c65bdaaa")

Routine: #intake (c7d2…5b) · table: claims
Taking close on 1 item(s).
Run: run_WzEs…
It applies in the background; get_row shows each item's new Status once it has, and get_run with that run shows how it went.
```
