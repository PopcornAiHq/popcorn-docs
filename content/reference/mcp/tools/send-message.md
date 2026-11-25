---
id: mcp/tools/send-message
title: send_message
order: 360
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-25
summary: >
  Post a message in a Routine, visible to its members.
concepts: []
used_with: [mcp/tools/create-message-upload, mcp/tools/get-routine]
---

[writes]

```
send_message(routine_id, text=None, thread_id=None, mentions=None, attachment=None, upload_ids=None, answers=None, exact=False, asks_for=None)
```

In an Agent Chat Routine: post as you go, not only when you're done, and say more than feels necessary. Your teammates can't see your session.

**Who posts.** You post as yourself; the Routine's agent as itself (its bot user), never as the member it serves.

**Refused.** In an archived Routine, and in one in announcement mode unless you're its admin or a workspace admin.

**Files.** Text files go in `attachment`; any other, uploaded with [`create_message_upload`](https://docs.popcorn.ai/mcp/tools/create-message-upload.md), in `upload_ids`; at most 10 in all.

**Answers.** An @mention of the agent gets an answer. A plain message goes to a classifier: most Routines' agents answer most messages, some only those that need one, and a Routine can be set to answer only @mentions. To be surer of an answer, put the agent's handle in `mentions`. A Routine homed in another workspace never answers. While the agent runs a task here, your message may join or queue behind it.

**Replies.** A reply arrives asynchronously; the response says where.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID ([`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md) returns it). |
| `text` | `str` | Message text (markdown). Optional with a file. |
| `thread_id` | `str` | Reply in this thread (its first message's ID). The Routine's own agent, without one, posts in the thread it is answering. |
| `mentions` | `list[str]` | People to mention and notify: "@username" or a member's name (any case), email, user ID, or "me". Only these are mentioned; "@name" in the text is not parsed. |
| `attachment` | `Attachment \| list[Attachment]` | A text file, or a list of them. |
| `upload_ids` | `list[str]` | `upload_ids` from `create_message_upload`, each sent once. |
| `answers` | `str \| int` | Replying to an ask: its `row_id` or `ask_key` marks it answered, crediting you. |
| `exact` | `bool` | Agent Chat forwards a misplaced message where it belongs (it says so); true: don't. Default `False`. |
| `asks_for` | `list[str]` | Agent Chat: whom your message asks something of (who has to answer or do it; not those only told or CC'd), named as in mentions. When it can't tell, the response asks you. |

**Example** — “Send the agent in #intake my notes on claim 4471 and the adjuster's call log, ask what's still open, and tell me what it says.”

```text
→ send_message(routine_id="c7d2…5b", text="What's still open on claim 4471?", attachment=[{"filename": "claim-4471-notes.md", "content": "# Claim 4471\n\n- First notice: Sept 18\n- Repair estimate requested from Northside Auto: Sept 24\n- Rental extension: waiting on sign-off\n"}, {"filename": "adjuster-call-log.txt", "content": "Sept 19 10:02 called claimant, left voicemail\nSept 20 14:30 claimant called back, photos sent\n"}])

Message sent to #intake (id: 7e1a…47).
Attached: claim-4471-notes.md (text/markdown, 135 B), adjuster-call-log.txt (text/plain, 94 B)
Replies arrive asynchronously: the Routine's agent typically answers within seconds to a few minutes. To read them: list_messages(routine="c7d2…5b", thread_id="7e1a…47"). A Routine set to reply outside threads posts its answer top-level instead; if the thread stays empty, check list_messages(routine="c7d2…5b", after="7e1a…47").

→ list_messages(routine="c7d2…5b", thread_id="7e1a…47")

Routine: #intake (c7d2…5b) · thread: 7e1a…47
1 of 1 replies, newest first:
[2026-09-29 14:03:00] (id: 9a3c…19) Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension. Everything else is closed.
```
