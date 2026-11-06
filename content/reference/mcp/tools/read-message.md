---
id: mcp/tools/read-message
title: read_message
order: 345
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  One message in a Routine, in full: its whole text, a line per attachment or
  other part, the reply count and thread_id, and its reactions (marking
  yours).
concepts: []
---

[read-only]

```
read_message(message_id, include_parts=False, cursor=None)
```

Each file attached to it comes with a download link, which works for a limited time (call again for a fresh one). A text file's text is included too, up to a limit shared by the message's files; the link gives the rest.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `message_id` [required] | `str` | The message's ID. |
| `include_parts` | `bool` | Also list every part's kind and fields, including tool calls with their arguments and integration payloads: what an agent actually did. Large; leave off unless needed. The parts are paged: a response ends with next_cursor when more follow. Default `False`. |
| `cursor` | `str` | next_cursor from the previous page of parts. A later page holds only the parts, not the message text again. |

**Example** — “Show me Dana's question about claim 4471 in full.”

```text
→ read_message(message_id="7e1a…47")

Routine: #intake (c7d2…5b)
Message: 7e1a…47
Author: Dana Smith
Sent: 2026-09-29 14:01 UTC
Replies: ↳ 1 reply (thread_id: 7e1a…47)
Reactions: 👀 1

What's still open on claim 4471?
```
