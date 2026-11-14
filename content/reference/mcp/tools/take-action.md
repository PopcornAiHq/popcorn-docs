---
id: mcp/tools/take-action
title: take_action
order: 359
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-14
summary: >
  Take one Action on one or more of a Routine's items, as a person pressing
  its button in Popcorn would.
concepts: [actions-and-status]
used_with: [mcp/tools/get-run, mcp/tools/list-actions]
---

[writes] [destructive] [dry run]

```
take_action(routine_id, row_ids=None, action=None, fields=None, confirm=False, run_key=None, plan_id=None)
```

One item it can't be taken on (not offered now, or Popcorn only), or a Connection it needs and lacks, refuses the whole call, saying why.

Without `confirm=true` this is a dry run: it says what happens to each item and gives a `run_key`. To act, call again with the same request, `confirm=true` and that `run_key`, which acts once (sent again, it finds its run). When the person named the items and the Action, confirm at once, without a dry run or `run_key`; each such call starts its own run, so don't repeat one that timed out. The confirm returns at once with the Run, which applies it in the background ([`get_run`](https://docs.popcorn.ai/mcp/tools/get-run.md) shows how it went).

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `row_ids` | `list[int]` | The items' row IDs in the Routine's main table, at most 50. Required, except on a confirm with a `plan_id`. |
| `action` | `str` | The Action, as [`list_actions`](https://docs.popcorn.ai/mcp/tools/list-actions.md) names it (its "action"); its button label names it too. Required, except on a confirm with a `plan_id`. |
| `fields` | `dict[str, str]` | Values the Action collects, named as `list_actions` says, e.g. `{"to": "@ana"}`. |
| `confirm` | `bool` | true to act: at once when the person named the items and the Action, otherwise after they agree to the dry run. Default `False`. |
| `run_key` | `str` | The `run_key` the dry run gave, with `confirm=true`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true`. It stands in for the rest of the request: leave it out and the confirm takes the dry run's, or send it and it must be the same. A Routine's own agent in Popcorn must pass it, from a dry run in an earlier run; an assistant connected from outside Popcorn is given none and needn't. |

**Example** — “Close claim 4471 in #intake.”

```text
→ take_action(routine_id="c7d2…5b", row_ids=[88], action="close")

Routine: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Take: close on 1 item(s), now.
- row 88, Close claim: Open (open) → Closed (closed)
- It runs as the workspace's agent, for you, as the button would: what the Action sends or records is real. The template's own checks, such as who may make the move, run then and may still refuse it; get_run shows how it went.
- run_key: Hc4pW8sN…

Call again with `confirm=true` to take it, with run_key="Hc4pW8sN…" and the same items.

→ take_action(routine_id="c7d2…5b", row_ids=[88], action="close", confirm=true, run_key="Hc4pW8sNz1bVq6Tj20d155d5c65bdaaa")

Routine: #intake (c7d2…5b) · table: claims
Taking close on 1 item(s).
Run: run_WzEs…
It applies in the background; get_row shows each item's new Status once it has, and get_run with that run shows how it went.
```
