---
id: mcp/tools/delete-message-as-admin
title: delete_message_as_admin
order: 316
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-17
summary: >
  Delete a message someone else wrote in a Routine you administer.
concepts: []
used_with: [mcp/tools/delete-message]
---

[writes] [destructive] [idempotent] [dry run]

```
delete_message_as_admin(message_id, confirm=False, plan_id=None)
```

For an admin of the Routine or of the workspace. Without `confirm=true` this is a dry run that deletes nothing: it shows the message and who wrote it. Show the person the dry run, and confirm only once they agree: there is no undo. Replies under a deleted message stay. For a message you wrote, use [`delete_message`](https://docs.popcorn.ai/mcp/tools/delete-message.md).

**Refused.** A caller who is no admin, an answer to an agent's question, and in an archived Routine.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `message_id` [required] | `str` | The message's ID. |
| `confirm` | `bool` | true to delete. Default `False`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true` and the same `message_id`. An assistant connected from outside Popcorn is given none and needn't. |

**Example** — “Take down the message Sam posted in #intake with a customer's card number in it.”

```text
→ delete_message_as_admin(message_id="7e1a…47")

**Dry run.** Nothing was changed.

Would delete Sam Ortiz's message 7e1a…47 from #intake, for everyone:
Sent: 2026-11-16 09:12:00
Text: Card on file: NNNN

Call again with `confirm=true` to delete Sam Ortiz's message.

→ delete_message_as_admin(message_id="7e1a…47", confirm=true)

Deleted Sam Ortiz's message 7e1a…47 from #intake.
```
