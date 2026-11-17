---
id: mcp/tools/delete-message
title: delete_message
order: 315
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-17
summary: >
  Delete a Routine message you wrote, at once and for everyone.
concepts: []
---

[writes] [destructive] [idempotent]

```
delete_message(message_id)
```

Use it only when the person asks for the message to be deleted: there is no dry run and no undo. Replies under a deleted message stay.

**Refused.** A message someone else wrote, an answer to an agent's question, and in an archived Routine.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `message_id` [required] | `str` | The message's ID. |

**Example** — “Delete the question I just posted in #intake, I asked in the wrong place.”

```text
→ delete_message(message_id="7e1a…47")

Deleted your message 7e1a…47 from #intake.
```
