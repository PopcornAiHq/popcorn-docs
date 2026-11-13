---
id: mcp/tools/create-message-upload
title: create_message_upload
order: 307
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Get a URL to upload one file to attach to a message in a Routine.
concepts: []
used_with: [mcp/tools/send-message]
---

[writes]

```
create_message_upload(routine_id, filename, size, sha256)
```

Upload with the curl line this returns, then pass the `upload_id` to [`send_message`](https://docs.popcorn.ai/mcp/tools/send-message.md) in `upload_ids`. The upload goes to Popcorn's file storage host, which a sandboxed assistant (such as claude.ai's) may not reach; then send a text file as `attachment`, and add any other file in Popcorn.

Exactly `size` bytes with this `sha256`, or refused; at most 50 MiB; an image, PDF or common document (a refusal lists them). The URL works 15 minutes; the `upload_id` is yours, for one message in this Routine within an hour. Refused where `send_message` is.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID. |
| `filename` [required] | `str` | The file's name; its extension decides its kind. |
| `size` [required] | `int` | The file's size in bytes. |
| `sha256` [required] | `str` | The file's sha256, as 64 hex characters. |

**Example** — “Post the timeline diagram I just made for claim 4471 in #intake.”

```text
→ create_message_upload(routine_id="c7d2…5b", filename="Claim 4471 timeline.png", size=48211, sha256="5d41402abc4b2a76b9719d911017c5925d41402abc4b2a76b9719d911017c592")

Routine: #intake (c7d2…5b)
Upload for a message in #intake: Claim 4471 timeline.png, 48,211 bytes, sha256 5d41402a….
upload_id: 4e1a9c07….png
method: PUT
url: https://uploads.popcorn.ai/4e1a9….png?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bcontent-type%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=8a3f…
headers:
  Content-Type: image/png
  x-amz-checksum-sha256: XUFAKrxL…
The URL works for 15 minutes; the upload_id goes into one message within 60 minutes. Once uploaded, the file is in the Routine's files even if it is never sent, so upload only what you mean to post.

Run this with FILE replaced by the file's path; it prints nothing when the upload succeeds:
curl -fsS -T FILE -H 'Content-Type: image/png' -H 'x-amz-checksum-sha256: XUFAKrxL…' 'https://uploads.popcorn.ai/4e1a9….png?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bcontent-type%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=8a3f…'

Then send it: send_message(routine_id="c7d2…5b", upload_ids=["4e1a9c07….png"]), with text if you like.
If curl can't connect to uploads.popcorn.ai, this organization doesn't allow it: add the file in Popcorn instead.

→ send_message(routine_id="c7d2…5b", text="The timeline for claim 4471, from first notice to today.", upload_ids=["4e1a9c07b2d35f68/0000000000000001/9b3f62e18c4d4a07a5e1d2c3b4a59681.png"])

Message sent to #intake (id: 7e1a…47).
Attached: Claim 4471 timeline.png (image/png, 47 KB)
Replies arrive asynchronously: the Routine's agent typically answers within seconds to a few minutes. To read them: list_messages(routine="c7d2…5b", thread_id="7e1a…47"). A Routine set to reply outside threads posts its answer top-level instead; if the thread stays empty, check list_messages(routine="c7d2…5b", after="7e1a…47").
```
