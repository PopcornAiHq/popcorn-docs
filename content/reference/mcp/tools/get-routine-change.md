---
id: mcp/tools/get-routine-change
title: get_routine_change
order: 314
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  Where a change to a Routine's Steps stands: still drafting, the proposal as
  Steps before and after, refused and why, or installed.
concepts: [steps]
used_with: [mcp/tools/change-routine]
---

[read-only]

```
get_routine_change(routine, change_id, wait_seconds=0, detail=None)
```

A proposal shows the Steps that change, what it would set on each Step (saying which part is a Routine Setting the person could change directly), the author's assumptions and open questions, and the checks it passed. An installed change names the version before it, which change_routine's revert_to puts back.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `change_id` [required] | `str` | The change_id change_routine returned. |
| `wait_seconds` | `int` | Wait up to this many seconds for a change that is drafting or installing to move on, then answer. At most 20 (more is read as 20); 0, the default, doesn't wait. |
| `detail` | `str` | "recipe" adds the recipe's own text diff to a proposal, for people who author templates. |

**Example** — “Did the change to #intake's Steps go in?”

```text
→ get_routine_change(routine="#intake", change_id="wf-draft")

Routine: #intake (c7d2…5b)
Change wf-draft: installed 2026-10-19T09:06:00+00:00 (version 45f7332bb200).
Steps, before → after (- before, + after):
  3. Signature — Getting signatures (Status value: signing)
+    - on its own: The claimant signed the standard retainer agreement and is asked to book the interview → Scheduling meeting (step 5)
get_routine shows all 16 Steps.
Set:
- `interview`: reminders 2, then 5 days after our last email; copy subject
Before it: version dd42ed0330f4. To go back: change_routine with revert_to="dd42ed03…".
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
