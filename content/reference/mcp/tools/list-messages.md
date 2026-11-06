---
id: mcp/tools/list-messages
title: list_messages
order: 330
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  A Routine's messages, newest first, or one thread's replies.
concepts: []
used_with: [mcp/tools/read-message]
---

[read-only]

```
list_messages(routine, thread_id=None, after=None, before=None, cursor=None, wait_seconds=0)
```

Each row is a timestamp (UTC), the message ID, the author, the text (long text is cut and marked; read_message returns it whole), one bracketed line per attachment, tool run or other part, and the reply count with the thread_id that lists the replies. Listing doesn't mark anything read. To read the Routine's agent's answer to a top-level message you sent, pass that message's ID as `thread_id`: in a Routine the agent answers in a thread under the message that asked. For a message you sent inside a thread, pass the thread's ID as `thread_id` and your message's ID as `after`. A Routine set to reply outside threads posts top-level instead, so if the thread stays empty, list the Routine with `after=<your message's ID>`. Replies arrive asynchronously, so if nothing is there yet, call again shortly, or pass wait_seconds to have this call wait for one.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine ID or "#name". |
| `thread_id` | `str` | List this thread's replies instead. A thread's ID is its first message's ID; a reply's ID finds its thread too. |
| `after` | `str` | Only messages after this ISO timestamp or message ID. |
| `before` | `str` | Only messages before this ISO timestamp or message ID. |
| `cursor` | `str` | next_cursor from the previous page. |
| `wait_seconds` | `int` | Wait up to this many seconds for a message newer than `after` (or, without it, than the newest one listed now) in the same Routine or thread, then answer; the answer says whether one arrived or the wait ran out. Not with cursor or before. At most 20 (more is read as 20); 0, the default, doesn't wait. |

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

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
