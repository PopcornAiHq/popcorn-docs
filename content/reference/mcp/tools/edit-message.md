---
id: mcp/tools/edit-message
title: edit_message
order: 319
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-25
summary: >
  Replace the text of a Routine message you wrote, keeping its files.
concepts: []
used_with: [mcp/tools/send-message]
---

[writes] [destructive] [idempotent]

```
edit_message(message_id, text=None, mentions=None, asks_for=None)
```

The new text takes the place of the old; the message's files and its place in the Routine stay, and it shows as edited.

**Refused.** A message someone else wrote, an answer to an agent's question, and wherever [`send_message`](https://docs.popcorn.ai/mcp/tools/send-message.md) is refused.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `message_id` [required] | `str` | The message's ID. |
| `text` | `str` | The new text (markdown), whole: it replaces the old. |
| `mentions` | `list[str]` | Who the message mentions now, named as in `send_message`; they replace those it had. Left out, the mentions stay as they were. |
| `asks_for` | `list[str]` | Agent Chat: whom the message asks something of, as `send_message` takes it; alone, the text stays as it is. |

**Example** — “I got the claim number wrong in my question in #intake. It's 4417, not 4471.”

```text
→ edit_message(message_id="7e1a…47", text="Status of claim 4417?")

Edited your message 7e1a…47 in #intake.
```
