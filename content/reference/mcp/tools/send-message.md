---
id: mcp/tools/send-message
title: send_message
order: 357
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Post a message in a Routine, visible to its members.
concepts: []
used_with: [mcp/tools/create-message-upload, mcp/tools/list-messages, mcp/tools/get-routine]
---

[writes]

```
send_message(routine_id, text=None, thread_id=None, mentions=None, attachment=None, upload_ids=None)
```

**Who posts.** You post as yourself; the Routine's own agent posts as itself (its bot user), never as the member it is serving.

**Refused.** It is refused in an archived Routine, and in one in announcement mode unless you are its admin or a workspace admin.

**Files.** Text files go in `attachment`; any other, uploaded with [`create_message_upload`](https://docs.popcorn.ai/mcp/tools/create-message-upload.md), in `upload_ids`; at most 10 in all. One unusable `upload_id` refuses the whole send, saying why.

**Answers.** An @mention of the agent gets an answer. A plain message goes to a classifier: most Routines' agents answer most messages, some only those that need an answer, and a Routine can be set to answer only @mentions. To be surer of an answer, put the agent's handle (the bot in the Routine's member list) in `mentions`. There is no answer in a Routine homed in another workspace. While the agent is already running a task in the Routine, your message may be passed into that task, or queued behind it, instead of getting a reply of its own.

**Replies.** A reply arrives asynchronously: to a top-level message, in a thread under it or, in a Routine that answers top-level (many do), after it; inside a thread, in that thread. The response gives the new message's ID and the [`list_messages`](https://docs.popcorn.ai/mcp/tools/list-messages.md) calls that read the answer.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID ([`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md) returns it). |
| `text` | `str` | Message text (markdown). Optional with a file. |
| `thread_id` | `str` | Reply in this thread (its first message's ID). The Routine's own agent, without one, posts in the thread it is answering. |
| `mentions` | `list[str]` | People to mention and notify: "@username", email, user ID, or "me". Only these are mentioned; "@name" in the text is not parsed. |
| `attachment` | `Attachment \| list[Attachment]` | A text file, or a list of them. |
| `upload_ids` | `list[str]` | `upload_ids` from `create_message_upload`, each sent once. |

**Example** — “Send the agent in #intake my notes on claim 4471 and the adjuster's call log, ask what's still open, and tell me what it says.”

```text
→ send_message(routine_id="c7d2…5b", text="What's still open on claim 4471?", attachment=[{"filename": "claim-4471-notes.md", "content": "# Claim 4471\n\n- First notice: Sept 18\n- Repair estimate requested from Northside Auto: Sept 24\n- Rental extension: waiting on sign-off\n"}, {"filename": "adjuster-call-log.txt", "content": "Sept 19 10:02 called claimant, left voicemail\nSept 20 14:30 claimant called back, photos sent\n"}])

Message sent to #intake (id: 7e1a…47).
Attached: claim-4471-notes.md (text/markdown, 135 B), adjuster-call-log.txt (text/plain, 94 B)
Replies arrive asynchronously: the Routine's agent typically answers within seconds to a few minutes. To read them: list_messages(routine="c7d2…5b", thread_id="7e1a…47"). A Routine set to reply outside threads posts its answer top-level instead; if the thread stays empty, check list_messages(routine="c7d2…5b", after="7e1a…47").

→ list_messages(routine="c7d2…5b", thread_id="7e1a…47")

Routine: #intake (c7d2…5b) · thread: 7e1a…47
1 of 1 replies, newest first:
[2026-09-29 14:03] (id: 9a3c…19) Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension. Everything else is closed.
```
