---
id: mcp/tools/complete-setup-step
title: complete_setup_step
order: 304
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-05
summary: >
  Complete one step of a Routine's setup that asks for a value, as its card on
  the Today tab in Popcorn does: a setting its work needs (a reply-by date, a
  waiting period) or a booking page's link. get_setup lists the steps and what
  each asks for.
concepts: [set-up-a-routine]
used_with: [mcp/tools/get-setup, mcp/tools/make-connection, mcp/tools/add-reference]
---

[writes] [destructive] [dry run]

```
complete_setup_step(routine_id, step, value, confirm=False, run_key=None, plan_id=None)
```

Giving a step another value later replaces the first. The step runs its own checks, and marks itself done when it passes. A refusal comes back in the step's own words, and the step isn't done; a run may have saved part of its work before it failed, so read get_setup before trying again. The answer is the step's outcome and the setup checklist as it then reads. A Connection step is made with make_connection, and a document step with add_reference. Without confirm=true this is a dry run that saves nothing and gives a run_key. When the person asked to set this step to this value, confirm at once, without a dry run or run_key; otherwise show the dry run, and confirm with its run_key once they agree. A run_key runs once: calling again with it finds the run it started.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `step` [required] | `str` | The step, as get_setup names it (its "step:" id), or its title. |
| `value` [required] | `str | int | float` | What the step asks for: the date, number or text its field takes, or the booking page's share link. |
| `confirm` | `bool` | true to complete it: at once on the person's own request, otherwise after they agree to the dry run. Default `False`. |
| `run_key` | `str` | The run_key the dry run gave, with confirm=true. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same step and value. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Set #intake's wait for a reply to 5 days.”

```text
→ complete_setup_step(routine_id="c7d2…5b", step="setting_wait_days", value=5, confirm=true)

Routine: #intake (c7d2…5b)
Set Days to wait for a reply to 5.
Setup: 5 of 6 steps done.
- [done] Connect your company email (step: connect_email)
- [left] Connect the adjusters' calendar (step: connect_calendar)
  Needs a Connection: make_connection makes it, and list_connections shows what it needs.
- [done, required] Intake: choose the questions document (step: document_questions)
- [done] Add your booking page (step: connect_booking_link) · set: "Consult with Acme"
  Warning: No booking of this page yet, so whose calendar it is can't be told until its first booking.
- [done, required] Days to wait for a reply (step: setting_wait_days)
- [done] Connect your intake form (step: connect_intake_webhook)
Also needed, with no step Popcorn shows: secret:portal_token.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
