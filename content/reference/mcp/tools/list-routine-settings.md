---
id: mcp/tools/list-routine-settings
title: list_routine_settings
order: 333
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  List the settings of a Routine's Routine Template, set or not.
concepts: [routine-settings]
used_with: [mcp/tools/copy-routine-template, mcp/tools/get-routine-setting, mcp/tools/update-routine-setting]
---

[read-only]

```
list_routine_settings(routine, query=None, cursor=None)
```

A setting changes how this Routine alone behaves: sending modes, schedules, limits, and the prompts and email templates its agents use. A changed setting reaches one Routine, can be set back, and is kept through template updates, so check here before giving the Routine its own copy of its template (copy_routine_template). Each prompt or email template file is its own setting, so changing one leaves the others following template updates. Each row shows the value; an unset one says what unset means, and one changed from the template default says so. Secrets show only whether they're set. get_routine_setting shows one in full; update_routine_setting changes one.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `query` | `str` | Only settings whose key or label contains this. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What can I change about how #chase-renewals chases people, without giving it its own copy of its template?”

```text
→ list_routine_settings(routine="#chase-renewals", query="chase")

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
4 of 4 settings matching "chase":
- chase_days  [1, 3, 7]
- chase_max_followups  5  (changed; template default 10)
- chase_window_timezone  America/Los_Angeles
- prompts.chase_email  Hi {{ name }}, just following up on the documents we asked for last week. If you've already sent them, thank you, and pl… [truncated; get_routine_setting(key="prompts.chase_email") for the full text]
2 values set on this Routine are read by nothing and not shown.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
