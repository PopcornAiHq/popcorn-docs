---
id: mcp/tools/get-routine-setting
title: get_routine_setting
order: 321
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Show one of a Routine's settings in full: its whole value, the template
  default, what it accepts and who may change it.
concepts: [routine-settings]
used_with: [mcp/tools/list-routine-settings]
---

[read-only]

```
get_routine_setting(routine, key)
```

It also shows the setting's description and its options, with the warning each one carries; a prompt or email template comes as its whole text.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `key` [required] | `str` | The setting's key, as [`list_routine_settings`](https://docs.popcorn.ai/mcp/tools/list-routine-settings.md) shows it. |

**Example** — “Show me the email #chase-renewals sends when it chases someone.”

```text
→ get_routine_setting(routine="#chase-renewals", key="prompts.chase_email")

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
Setting: prompts.chase_email
Value:
Hi {{ name }}, just following up on the documents we asked for last week. If you've already sent them, thank you, and please ignore this note.

The {{ firm }} team

Template default: the same as the value
Accepts: text, the shape of the template default
Changed by: update_routine_setting, by a workspace admin who's also a member of the Routine.
```
