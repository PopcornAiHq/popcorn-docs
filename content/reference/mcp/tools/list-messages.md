---
id: mcp/tools/list-messages
title: list_messages
order: 334
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-14
summary: >
  A Routine's top-level messages, newest first, or one thread's replies.
concepts: []
used_with: [mcp/tools/read-message, mcp/tools/send-message]
---

[read-only]

```
list_messages(routine, thread_id=None, after=None, before=None, cursor=None, wait_seconds=0, full=False)
```

A page holds 50. Long text is cut (`full=true` or [`read_message`](https://docs.popcorn.ai/mcp/tools/read-message.md) gives it whole); a message with replies shows its `thread_id`; times are UTC. Listing marks nothing read.

To read the Routine's agent's answer to a top-level message you sent, use the `list_messages` call [`send_message`](https://docs.popcorn.ai/mcp/tools/send-message.md) returned: a Routine answers in a thread under it (its ID as `thread_id`) or top-level after it (its ID as `after`), and many answer top-level. For a message you sent inside a thread, pass the thread's ID as `thread_id` and your message's ID as `after`. Replies arrive asynchronously: if nothing is there yet, call again shortly, or pass `wait_seconds`.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine ID or "#name". |
| `thread_id` | `str` | List this thread's replies instead. A thread's ID is its first message's ID; a reply's ID finds its thread too. |
| `after` | `str` | Only messages after this ISO timestamp or message ID. |
| `before` | `str` | Only messages before this ISO timestamp or message ID. |
| `cursor` | `str` | `next_cursor` from the previous page. |
| `wait_seconds` | `int` | Wait up to this many seconds for a message newer than `after` (or, without it, than the newest one listed now) in the same Routine or thread, then answer, saying whether one arrived. Not with cursor or before. At most 20 (more is read as 20); 0, the default, doesn't wait. |
| `full` | `bool` | Whole texts, a page at most 40,000 bytes. Default `False`. |

**Example** — “What's happened in #intake today?”

```text
→ list_messages(routine="#intake", after="2026-09-29T00:00:00Z")

Routine: #intake (c7d2…5b)
3 of 3 messages, newest first:
[2026-09-29 16:40] (id: 9400…a5) Intake agent: New claim 4480 from the web form: water damage, Riverside Ave. Assigned to Jordan.
[2026-09-29 14:01] (id: 7e1a…47) Dana Smith: What's still open on claim 4471?
  ↳ 1 reply (thread_id: 7e1a…47)
[2026-09-29 09:00] (id: e769…47) Intake agent: Morning summary: 3 new claims overnight, 2 waiting on a repair estimate.
```
