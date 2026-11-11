---
id: mcp/tools/get-setup
title: get_setup
order: 321
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  Show a Routine's setup checklist, the steps on its Today tab in Popcorn, in
  order, each with whether it's done and what it still needs.
concepts: [set-up-a-routine]
used_with: [mcp/tools/make-connection, mcp/tools/add-reference, mcp/tools/complete-setup-step]
---

[read-only]

```
get_setup(routine)
```

Required steps are marked, and each step left says what it still needs and which tool does it: a Connection ([`make_connection`](https://docs.popcorn.ai/mcp/tools/make-connection.md)), a document ([`add_reference`](https://docs.popcorn.ai/mcp/tools/add-reference.md)), a value such as a booking page's link ([`complete_setup_step`](https://docs.popcorn.ai/mcp/tools/complete-setup-step.md)), or Popcorn, for a step no tool here can complete. A step that keeps a value shows what is set; a credential shows only that it is set.

A Routine whose template builds its checklist from its Steps has it built here when it hasn't been yet, as opening its Today tab does; that can take some seconds. If it isn't done in time, the template's own steps are listed meanwhile, and it says so: their step ids may change, so call `get_setup` again before completing one. A Routine with no checklist says so.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What's left to set up on #intake?”

```text
→ get_setup(routine="#intake")

Routine: #intake (c7d2…5b)
Setup: 4 of 6 steps done; 1 required left.
- [done] Connect your company email (step: connect_email)
- [left] Connect the adjusters' calendar (step: connect_calendar)
  Needs a Connection: make_connection makes it, and list_connections shows what it needs.
- [done, required] Intake: choose the questions document (step: document_questions)
- [done] Add your booking page (step: connect_booking_link) · set: "Consult with Acme"
  Warning: No booking of this page yet, so whose calendar it is can't be told until its first booking.
- [left, required] Days to wait for a reply (step: setting_wait_days)
  Needs a value for Days to wait for a reply (days, 1–30): complete_setup_step sets it.
  About: How long the Routine waits for an answer before it follows up.
  Takes: Counted in calendar days. For example: 7.
- [done] Connect your intake form (step: connect_intake_webhook)
Also needed, with no step Popcorn shows: secret:portal_token.
```
