---
id: mcp/tools/create-routine-file-upload
title: create_routine_file_upload
order: 310
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Get a URL to upload one file you made, for the next version of a Routine's
  template.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/create-routine-version]
---

[writes]

```
create_routine_file_upload(routine_id, path, size, sha256)
```

For a file too large to send in a change to [`create_routine_version`](https://docs.popcorn.ai/mcp/tools/create-routine-version.md), such as a bundled script or a generated data file. Works only where your network lets you reach uploads.popcorn.ai (on claude.ai, the organization's network egress settings). Upload with the curl line this returns, then create the version with the change below. If the upload fails or can't connect, don't retry it: use `from_url` for a public file, or send the content in the change.

```text
{"path": "…", "from_upload": "<upload_id>"}
```

One file per upload, for this Routine and path only. The upload must be exactly `size` bytes with this `sha256`, or it is refused; UTF-8 text only, at most 4 MiB. The URL works for 15 minutes, and the upload can go into one version for most of a day. You can have at most 10 uploads from the last 15 minutes that aren't yet in a version. Workspace admins only, like `create_routine_version`.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name), as for `create_routine_version`. |
| `path` [required] | `str` | The path the file will have in the template, e.g. code/engine/lib.js. |
| `size` [required] | `int` | The file's size in bytes. |
| `sha256` [required] | `str` | The file's sha256, as 64 hex characters (`sha256sum FILE`). |

**Example** — “I bundled the chess engine into engine.js; publish it to #intake's app without pasting it.”

```text
→ create_routine_file_upload(routine_id="c7d2…5b", path="code/engine/engine.js", size=48213, sha256="9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c")

Routine: #intake (c7d2…5b)
Upload for code/engine/engine.js: 48,213 bytes, sha256 9f2c9f2c….
upload_id: 3f6a…93
method: PUT
url: https://uploads.popcorn.ai/staging/8c1f…e2/3f6a…93?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=5e1d…
headers:
  x-amz-checksum-sha256: nyyfLJ8s…
URL expires: 2026-10-13T18:15:00Z. Usable in a version until 2026-10-14T17:00:00Z.

Run this with FILE replaced by the file's path; it prints nothing when the upload succeeds:
curl -fsS -T FILE -H 'x-amz-checksum-sha256: nyyfLJ8s…' 'https://uploads.popcorn.ai/staging/8c1f…e2/3f6a…93?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=5e1d…'

Then pass it to create_routine_version with this change (add expected_sha256 to replace a file that exists):
{"path": "code/engine/engine.js", "from_upload": "3f6a…93"}
If curl can't connect to uploads.popcorn.ai, this organization doesn't allow it: use from_url for a public file, or send the content in the change.
```
