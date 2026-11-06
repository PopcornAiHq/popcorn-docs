---
id: mcp/tools/update-routine-setting
title: update_routine_setting
order: 354
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Change one of a Routine's settings, on this Routine only.
concepts: [routine-settings]
used_with: [mcp/tools/create-routine-version, mcp/tools/list-routine-settings]
---

[writes] [destructive] [dry run]

```
update_routine_setting(routine_id, key, value="OMITTED", changes=None, confirm=False, plan_id=None)
```

Without confirm=true this is a dry run that changes nothing: it shows the old and new value, what the setting does, and the warning the new option carries. For a long value it also gives a plan_id: to change it, call again with the key, confirm=true and that plan_id, and the value needn't be sent again. Setting the template default resets the setting. A switch takes one of its options; any other setting keeps the shape of the template default (a list stays a list, a number a number). Secrets and the Routine's Steps aren't changed here. For a long text (a prompt, an email template, agent guidance), pass changes instead of value: text ops applied in order to the current text, as create_routine_version's ops are. The anchor is the text exactly and must match once: {"op": "replace", "old_string": "Hi {{name}},", "new_string": "Hello {{name}},"}. Also insert_before and insert_after (anchor, text), prepend and append (text), and replace_range (from, to, new_string). A value with credentials inside it shows them as [secret]. Keep [secret] exactly where a read shows it; the stored credential stays in place. Credentials, and what surrounds them, change in the app.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `key` [required] | `str` | The setting's key, as list_routine_settings shows it. |
| `value` | `Any` | The whole new value: text, a number, a list, a mapping, or null. Omit it to pass changes instead. Default `OMITTED`. |
| `changes` | `list[Op]` | Text ops on the current text, instead of value. |
| `confirm` | `bool` | true to change it: at once when the person asked for this change, otherwise after they agree to the dry run. A new value whose option carries a warning (drafts to sending) is confirmed only with its dry run's plan_id. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true, in place of value and changes. Required for a warned value. |

**Example** — “Stop chasing after five follow-ups on #chase-renewals.”

```text
→ update_routine_setting(routine_id="4b0e…12", key="chase_max_followups", value=5)

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
**Dry run.** Nothing was changed.

Change: chase_max_followups on #chase-renewals.
- 10 → 5
- Reach: this Routine only. It can be set back with update_routine_setting. Template updates won't change the new value.

Call again with `confirm=true` to change chase_max_followups.

→ update_routine_setting(routine_id="4b0e…12", key="chase_max_followups", value=5, confirm=true)

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
Changed chase_max_followups on #chase-renewals: 10 → 5.
Runs already under way keep the value they started with.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
