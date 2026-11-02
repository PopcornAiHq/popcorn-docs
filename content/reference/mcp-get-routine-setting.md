---
id: mcp-get-routine-setting
title: get_routine_setting
order: 315
group: MCP
parent: mcp-tools
updated: 2026-11-01
summary: >
  One of a Routine's settings in full: the whole value (a prompt or email
  template's whole text), the template default, what it accepts, its
  description, its options with the warning each one carries, and who may
  change it.
concepts: [routine-settings]
used_with: [mcp-list-routine-settings]
---

[read-only]

```
get_routine_setting(routine, key)
```

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `key` [required] | `str` | The setting's key, as list_routine_settings shows it. |

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

The [MCP server](https://docs.popcorn.ai/mcp.md) page has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
