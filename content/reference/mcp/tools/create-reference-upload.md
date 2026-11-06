---
id: mcp/tools/create-reference-upload
title: create_reference_upload
order: 306
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Get a URL to upload one file for one of a Routine's References, for
  add_reference to take.
concepts: [reference-documents]
used_with: [mcp/tools/add-reference, mcp/tools/list-references]
---

[writes]

```
create_reference_upload(routine_id, reference, filename, size, sha256)
```

Nothing changes in the Routine until add_reference is confirmed.

Upload with the curl line this returns, then call add_reference with the upload_id. The upload goes straight to Popcorn's file storage host, which an assistant whose network access is restricted (such as claude.ai's sandbox) may not reach. In that case, pass a text Reference to add_reference as `text` instead, or add the file in Popcorn.

One file per upload, for this Routine and Reference only. The upload must be exactly `size` bytes with this `sha256`, or it is refused; at most 50 MiB (a text file 1.5 MB), and of a kind the Reference takes (the refusal says which). The URL works for 15 minutes. Not for a Reference picked from Google Drive, or one holding the Routine's Steps; list_references marks both. Workspace admins and members of the Routine only.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `reference` [required] | `str` | The Reference, as list_references names it. |
| `filename` [required] | `str` | The file's name with its extension, e.g. fees.pdf; the extension decides what kind of file it is. |
| `size` [required] | `int` | The file's size in bytes. |
| `sha256` [required] | `str` | The file's sha256, as 64 hex characters (`sha256sum FILE`). |

**Example** — “Here's our 2026 fee schedule PDF; give it to #intake.”

```text
→ create_reference_upload(routine_id="c7d2…5b", reference="fee_schedule", filename="Fee schedule 2026.pdf", size=48211, sha256="5d41402abc4b2a76b9719d911017c5925d41402abc4b2a76b9719d911017c592")

Routine: #intake (c7d2…5b)
Upload for Fee schedule (reference "fee_schedule"): 48,211 bytes, sha256 5d41402a….
upload_id: 4e1a9c07….pdf
method: PUT
url: https://acme-uploads.s3.us-west-2.amazonaws.com/4e1a….pdf?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bcontent-type%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=8a3f…
headers:
  Content-Type: application/pdf
  x-amz-checksum-sha256: XUFAKrxL…
The URL works for 15 minutes.

Run this with FILE replaced by the file's path; it prints nothing when the upload succeeds:
curl -fsS -T FILE -H 'Content-Type: application/pdf' -H 'x-amz-checksum-sha256: XUFAKrxL…' 'https://acme-uploads.s3.us-west-2.amazonaws.com/4e1a….pdf?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bcontent-type%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=8a3f…'

Then add it: add_reference(routine_id="c7d2…5b", reference="fee_schedule", upload_id="4e1a9c07….pdf") shows what it changes first.
If curl can't connect to acme-uploads.s3.us-west-2.amazonaws.com, this organization doesn't allow it: add the Reference in Popcorn instead.

→ add_reference(routine_id="c7d2…5b", reference="fee_schedule", upload_id="4e1a9c07b2d35f68/0000000000000001/7c2e91d04f3b4a6e8d5c1b0a9f7e6d51.pdf")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Add: Fee schedule (reference "fee_schedule") on #intake.
- From upload 4e1a9c07….pdf: a PDF (.pdf), 48,211 bytes, file Fee schedule 2026.pdf.
- First add: nobody has added it yet.
- Used for: The fees quoted when a claimant asks what it costs.
- Popcorn reads the file in the background, and the Routine works from it from then on.

Call again with `confirm=true` to add it.
```
