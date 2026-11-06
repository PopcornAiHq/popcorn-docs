---
id: activities/catalog/feature/gdrive
title: feature.gdrive
order: 133
group: Activities
parent: activities/catalog/feature
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.gdrive activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.gdrive` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.gdrive.check_folder`

Check a picked Drive folder before it is saved as a destination.

Carry `integration_name` (normally `gdrive`) so the step runs as
the bound Google account.

```yaml
- id: <step>
  activity: feature.gdrive.check_folder
  args:
    conversation_id: <string>
    folder: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `folder` | string | yes | Folder id or Drive URL — normally the id the person picked in the Google Picker. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `folder_id` | string |  |
| `name` | string |  |
| `web_view_link` | string |  |
| `drive_id` | string | The shared drive holding the folder; empty in a My Drive. |

### `feature.gdrive.download_to_store`

Download a picked Drive file into a permanent agent-store file.

Carry `integration_id` / `integration_name` (inherited from
ActivityInput, normally `integration_name: gdrive`) so the identity
binding swaps the auth to the bound Google account first. Prior files
under the same stem are replaced — but never before the replacement's
bytes are durably stored.

```yaml
- id: <step>
  activity: feature.gdrive.download_to_store
  args:
    conversation_id: <string>
    file: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (the durable copy lands in this conversation's agent store). |
| `file` | string | yes | Drive file id or Docs/Drive URL — normally the id the user picked via the client-side Google Picker. |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'onboarding/standard-retainer'. The activity appends '.<ext>' derived from the downloaded filename (then content type, then 'bin') and replaces any existing '<stem>.*' file. |
| `accept` | list of string, optional | no | Allowed kinds in the file.detect taxonomy (pdf, xlsx, csv, image, docx, text). A download classifying outside the list fails non-retryably (UnsupportedFileType); omit to accept anything. |
| `export_format` | string, optional | no | Export target for Google-native files (Docs/Sheets/Slides). Defaults to pdf so a native Doc satisfies accept: [pdf]; set null for the type's plain export (Docs→text, Sheets→csv). Non-native files always download verbatim. Default `"pdf"`. |
| `require_source_mime_type` | string, optional | no | Require the picked file's OWN Drive mime type to be this — 'application/vnd.google-apps.document' for a retainer that will be filled in Google Docs. Checked before anything is stored; a mismatch fails non-retryably by name (GdriveSourceNotGoogleDoc / GdriveSourceNotAccepted). None accepts any type the accept list allows. |
| `convert_word_to_doc` | boolean | no | Convert a picked Word file (.docx/.doc) to a native Google Doc before downloading, in the Word file's own folder (My Drive when that folder won't take it), named like it without the extension. Any other file is downloaded as picked. Default `false`. |
| `max_bytes` | integer | no | Hard cap on the payload. Enforced by the proxy against Drive's declared size before any content moves, and again here after decoding (Google-native exports declare no size). Either way an oversized file fails non-retryably (FileTooLarge). Default `26214400`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Final agent-store file key, e.g. 'onboarding/standard-retainer.pdf'. |
| `size_bytes` | integer |  |
| `sha256` | string |  |
| `content_type` | string, optional |  |
| `filename` | string, optional | Download filename from Drive (export target included), for display/record use. |
| `drive_file_id` | string | The Drive file the bytes came from, for provenance records: the id/URL as passed, or the converted Doc's id when convert_word_to_doc turned a Word pick into one. |
| `converted_from_file_id` | string | The picked Word file's id when it was converted to the Doc in drive_file_id; empty otherwise. |
| `source_mime_type` | string | The picked file's own Drive mime type ('application/vnd.google-apps.document' for a native Doc), as distinct from content_type, the export's. Recorded in the document envelope so a later step knows what the pick was. |

### `feature.gdrive.ensure_folder`

The app's folder carrying `tag`, made in `parent_id` (My Drive's
root when omitted) if none does.

```yaml
- id: <step>
  activity: feature.gdrive.ensure_folder
  args:
    conversation_id: <string>
    name: <string>
    tag: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `name` | string | yes | The folder's name when it has to be made. |
| `tag` | string | yes | What identifies the folder across runs, renames and moves, e.g. `signed_documents:<conversation_id>`. |
| `parent_id` | string, optional | no | The folder to make it in when no live folder carries the tag, e.g. another ensure_folder's `folder_id`; My Drive's root when omitted. A folder that already carries the tag is returned wherever it now lives, so a folder the firm moved is followed, never duplicated — unless `by_name_in_parent` is set. |
| `by_name_in_parent` | boolean | no | Find the folder by `name` directly inside `parent_id` (My Drive's root when omitted) instead of by tag anywhere: a folder moved elsewhere, renamed or on a shared drive is not reused, and a new one is made in `parent_id`. Only folders the app made or the Picker granted are visible. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `folder_id` | string |  |
| `name` | string |  |
| `web_view_link` | string |  |
| `drive_id` | string | The shared drive holding the folder; empty in a My Drive. |
| `created` | boolean | True when this call made the folder; False when a live folder already carried the tag. |

### `feature.gdrive.file_metadata`

Look up a picked Drive file's name and type.

Carry `integration_name` (normally `gdrive`) so the step runs as
the bound Google account.

```yaml
- id: <step>
  activity: feature.gdrive.file_metadata
  args:
    conversation_id: <string>
    file: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file` | string | yes | Drive file id or Docs/Drive URL — normally the id the person picked in the Google Picker. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_id` | string |  |
| `name` | string |  |
| `mime_type` | string | The file's own Drive mime type: 'application/vnd.google-apps.document' for a native Doc, 'application/pdf' for a PDF, and so on. |
| `web_view_link` | string |  |

### `feature.gdrive.file_to_client_folder`

File one agent-store file into its client's folder in the firm's
Drive. Carry `integration_name` (normally `gdrive`) so the step runs
as the bound Google account.

```yaml
- id: <step>
  activity: feature.gdrive.file_to_client_folder
  args:
    conversation_id: <string>
    file_key: <string>
    file_name: <string>
    upload_tag: <string>
    client_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | The agent-store file to upload (a PDF). |
| `file_name` | string | yes | The Drive file's name. |
| `upload_tag` | string | yes | What identifies this file across retries: a live file in the client's folder already carrying it is returned and nothing is uploaded. One per document filed (a signing round). |
| `person_name` | string | no | The client's full name; their folder is "Last, First" from it. Default `""`. |
| `client_key` | string | yes | The client's identity in this channel (the row's id): their folder's tag, so every document they sign shares it. |
| `client_folder_fallback` | string | no | The folder's name when person_name has nothing usable, e.g. `Recipient 412`. Blank: `Client <client_key>`. Default `""`. |
| `folder` | any, optional | no | The firm's pick, the `signed_documents_folder` scalar as stored ({folder_id, name, …} as JSON text or parsed); empty for the default "Active Clients". |
| `default_folder_name` | string | no | The default parent's name at the top of My Drive. Default `"Active Clients"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `filed` | boolean |  |
| `cause` | string | Why nothing was filed: not_connected, folder_missing, folder_not_writable (the channel's to fix), source_missing, too_large (this file's), filing_off. Blank when filed. |
| `error_type` | string |  |
| `reason` | string |  |
| `parent_mode` | string | picked / default |
| `parent_folder_id` | string |  |
| `routine_folder_id` | string | The channel's folder inside the parent. |
| `routine_folder_name` | string |  |
| `default_folder_id` | string |  |
| `default_folder_name` | string |  |
| `default_folder_link` | string |  |
| `default_drive_id` | string |  |
| `folder_id` | string | The client's folder. |
| `folder_name` | string |  |
| `file_id` | string |  |
| `file_name` | string |  |
| `web_view_link` | string |  |
| `created` | boolean | True when this call uploaded; False when the tagged file was already there. |

### `feature.gdrive.read_document`

Read a Google Drive document's content as markdown.

Carry `integration_id` (inherited from ActivityInput, normally
`$channel.integrations.gdrive.id`) so the identity binding swaps
the auth to the bound Google account before the read.

```yaml
- id: <step>
  activity: feature.gdrive.read_document
  args:
    file: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `file` | string | yes | Drive file id or Docs/Drive URL — normally the id the user picked via the client-side Google Picker. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `document_id` | string | Canonical Drive file id. |
| `title` | string | Document title. |
| `url` | string | Web link to the document. |
| `content` | string | Document content as markdown (plain text when the read fell back to Drive export). |
| `last_edited` | string | RFC3339 modifiedTime, '' when unavailable. |

### `feature.gdrive.template_html`

Export the pinned retainer's Google Doc as HTML, once per template.

Carry `integration_name: gdrive` so the identity binding swaps the
auth to the bound Google account — the export goes through the same
/v2 drive proxy the pick used.

```yaml
- id: <step>
  activity: feature.gdrive.template_html
  args:
    conversation_id: <string>
    template_file_key: <string>
    template_sha256: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `template_file_key` | string | yes | The pinned template PDF (feature.pdf.pin_template's file_key), whose text the Doc's is checked against. |
| `template_sha256` | string | yes | The pinned template's digest; the HTML is stored and recorded under it. |
| `drive_file_id` | string, optional | no | The picked template's Drive file id, as the pick recorded it; blank for a template that was uploaded rather than picked, which has no page to export. Default `""`. |
| `source_mime_type` | string, optional | no | The picked file's own Drive mime type; only a native Google Doc exports. Blank (an envelope from before the pick recorded it) is skipped rather than guessed. Default `""`. |
| `max_bytes` | integer | no | Cap on each export's payload; a Doc over it is skipped (the row shows the merge's pages as before). Default `10485760`. |
| `inline_images` | boolean | no | Fetch the export's googleusercontent images and inline them as data: URIs so the stored page is self-contained. Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `html_file_key` | string | templates/<sha256[:16]>.html, or blank when nothing was stored or recorded (see status / why). |
| `status` | `stored` / `cached` / `skipped` / `drifted` | stored: exported and recorded by this run; cached: an earlier run recorded it, no Drive call made; skipped: nothing to export (not a picked Google Doc, or over the cap); drifted: the Doc's text no longer matches the pinned PDF, nothing recorded. |
| `why` | string |  |
| `images_inlined` | integer |  |

### `feature.gdrive.upload_from_store`

Upload an agent-store file into a Drive folder.

```yaml
- id: <step>
  activity: feature.gdrive.upload_from_store
  args:
    conversation_id: <string>
    file_key: <string>
    folder_id: <string>
    name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | The agent-store file to upload, e.g. the `file_key` feature.signing.fetch_signed_document returned. |
| `folder_id` | string | yes | The Drive folder to land it in (check_folder's or ensure_folder's `folder_id`). |
| `name` | string | yes | The Drive file's name. |
| `mime_type` | string | no | Default `"application/pdf"`. |
| `tag` | string, optional | no | With a tag, a live file in the folder already carrying it is returned (`created: false`) and nothing is uploaded — what makes a retry safe. Include the content's hash so a different document is never mistaken for the one already filed. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_id` | string |  |
| `name` | string |  |
| `web_view_link` | string |  |
| `created` | boolean |  |
| `size_bytes` | integer |  |
| `sha256` | string |  |
