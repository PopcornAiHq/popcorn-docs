---
id: mcp/tools/send-message
title: send_message
order: 348
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  Post a message in a Routine, visible to its members.
concepts: []
used_with: [mcp/tools/list-messages, mcp/tools/get-routine]
---

[writes]

```
send_message(routine_id, text=None, thread_id=None, mentions=None, attachment=None)
```

You post as yourself; the Routine's own agent posts as itself (its bot user), never as the member it is serving. Whether the Routine's agent answers: an @mention of the agent gets an answer. A plain message goes to a classifier; the agent of a Routine that runs an app answers most messages, other Routines' agents only those that need it. To be surer of an answer, put the agent's handle (the bot in the Routine's member list) in `mentions`. There is no answer in a Routine homed in another workspace, and while the agent is already running a task in the Routine, your message joins that task instead of getting its own reply. Replies arrive asynchronously, in a thread under a top-level message (unless the Routine is set to reply outside threads). The response gives the new message's ID and the list_messages call that reads the answer. Without a `thread_id`, the Routine's own agent posts in the thread it is answering.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (get_routine returns it). |
| `text` | `str` | Message text (markdown). Optional with an attachment. |
| `thread_id` | `str` | Reply in this thread (its first message's ID). |
| `mentions` | `list[str]` | People to mention and notify: "@username", email, user ID, or "me". Only these are mentioned; "@name" in the text is not parsed. |
| `attachment` | `Attachment` | A text file to attach. |

**Example** — “Ask the agent in #intake what's still open on claim 4471, and tell me what it says.”

```text
→ send_message(routine_id="c7d2…5b", text="What's still open on claim 4471?")

Message sent to #intake (id: 7e1a…47).
Replies arrive asynchronously: the Routine's agent typically answers within seconds to a few minutes. To read them: list_messages(routine="c7d2…5b", thread_id="7e1a…47"). A Routine set to reply outside threads posts its answer top-level instead; if the thread stays empty, check list_messages(routine="c7d2…5b", after="7e1a…47").

→ list_messages(routine="c7d2…5b", thread_id="7e1a…47")

Routine: #intake (c7d2…5b) · thread: 7e1a…47
1 of 1 replies, newest first:
[2026-09-29 14:03] (id: 9a3c…19) Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension. Everything else is closed.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
