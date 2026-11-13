---
id: mcp/tools/list-routine-templates
title: list_routine_templates
order: 338
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  List the Routine Templates a new Routine in this workspace can start from.
concepts: [set-up-a-routine]
used_with: [mcp/tools/create-routine, mcp/tools/create-routine-template]
---

[read-only]

```
list_routine_templates(query=None, cursor=None)
```

Each row shows the template's name, its slug (what [`create_routine`](https://docs.popcorn.ai/mcp/tools/create-routine.md)'s `template` takes), what it does, the connections someone sets up before it runs, and the optional ones that only the work using them needs. A template this workspace can't run isn't listed. Templates this workspace made itself ([`create_routine_template`](https://docs.popcorn.ai/mcp/tools/create-routine-template.md)) are listed too, marked as its own; no other workspace sees them.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive substring of the template's name or slug. |
| `cursor` | `str` | The `next_cursor` from the previous page, with the same query. |

**Example** — “What templates could a new Routine here start from?”

```text
→ list_routine_templates()

5 of 5 Routine Templates:
- Alert Tracker  alerttracker  Ingests Alertmanager alerts from a webhook and keeps one row per alert.  needs no connections
- Chat  chat  A Routine with a calendar. Ask when everyone's free and it checks every connected calendar.  needs Google Calendar
- Claim Coordinator  claimcoordinator  Imports arbitration leads, emails each one its questions, and tracks every answer until the claim is complete.  needs Gmail, Google Calendar, Google Drive
- … 2 more rows
```
