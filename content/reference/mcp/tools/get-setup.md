---
id: mcp/tools/get-setup
title: get_setup
order: 319
group: MCP
parent: mcp/tools
updated: 2026-11-05
summary: >
  Show a Routine's setup checklist, the steps on its Today tab in Popcorn, in
  order: each done or not, which are required, and what each one left still
  needs (a Connection, a document, a booking page, a value).
concepts: [set-up-a-routine]
---

[read-only]

```
get_setup(routine)
```

A step that keeps a value shows what is set. A Routine whose template builds its checklist from its Steps has it built here when it hasn't been yet, as opening its Today tab does; that can take some seconds. If it isn't done in time, the template's own steps are listed meanwhile, and it says so. A Routine with no checklist says so.

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

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
