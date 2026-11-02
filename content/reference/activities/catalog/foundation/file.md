---
id: activities/catalog/foundation/file
title: foundation.file
order: 112
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.file activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.file` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.file.copy_to_store`

Copy a conversation upload's bytes into a permanent agent-store file.

The source stays untouched; the copy survives conversation-upload
deletion and appears in the conversation's agent-store files list under
the final key. Prior files under the same stem are replaced — but never
before the replacement's bytes are durably stored.

```yaml
- id: <step>
  activity: foundation.file.copy_to_store
  args:
    conversation_id: <string>
    conversation_file_key: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; files from other conversations are not readable). |
| `conversation_file_key` | string | yes | Conversation-level uploaded file key (file_uploads). |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'onboarding/standard-retainer'. The activity appends '.<ext>' derived from the source (filename extension, then MIME, then 'bin') and replaces any existing '<stem>.*' file. URL-safe, must start with an alphanumeric. |
| `content_type` | string, optional | no | Stored content type override; defaults to the source's MIME type (or application/octet-stream when unknown). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Final agent-store file key, e.g. 'onboarding/standard-retainer.pdf'. |
| `size_bytes` | integer |  |
| `sha256` | string |  |
| `content_type` | string, optional |  |
| `filename` | string, optional | Original upload filename (for display/attachment use). |

### `foundation.file.detect`

Classify a conversation upload by metadata (no download).

Returns a single `kind` from: pdf, xlsx, csv, image, docx, text,
unknown. Branch on it with the comparison form of `when:`, e.g.
`when: "$steps.<id>.output.kind == 'pdf'"`.

```yaml
- id: <step>
  activity: foundation.file.detect
  args:
    conversation_id: <string>
    conversation_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; files from other conversations are not readable). |
| `conversation_file_key` | string | yes | Conversation-level uploaded file key (file_uploads). |
| `accept` | list of string, optional | no | Kinds this flow can handle (subset of: pdf, xlsx, csv, image, docx, text). When set, any other detected kind — including unknown — fails the step non-retryably (UnsupportedFileType), so the flow's failure_status surfaces it. Omit to classify permissively and branch on `kind` instead. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `kind` | string | One of: pdf, xlsx, csv, image, docx, text, unknown. Branch with `when: "$steps.<id>.output.kind == 'pdf'"`. |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `extension` | string, optional | Lowercased filename extension without the dot. |
| `size_bytes` | integer, optional |  |

### `foundation.file.extract_text`

Read a conversation upload's text, or a durable agent-store file's:
a text file, a PDF or a Word document.

```yaml
- id: <step>
  activity: foundation.file.extract_text
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `conversation_file_key` | string, optional | no | A conversation upload's file key. |
| `agent_store_file_key` | string, optional | no | A durable agent-store file key the flow stored (e.g. feature.gdrive.download_to_store's file_key). |
| `mime_type` | string, optional | no | With agent_store_file_key: the stored file's type, as the step that stored it reported (download_to_store's content_type). Wins over the key's extension. |
| `accept` | list of string | no | The kinds read (text, pdf, docx); any other upload fails non-retryably (UnsupportedFileType). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |
| `kind` | string | text, pdf or docx. |
| `size_bytes` | integer | The upload's size. |
| `mime_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.read_bytes`

Read a conversation upload and return its bytes base64-encoded.

```yaml
- id: <step>
  activity: foundation.file.read_bytes
  args:
    conversation_id: <string>
    conversation_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `conversation_file_key` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `data` | string |  |
| `size_bytes` | integer |  |
| `mime_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.read_text`

Read a conversation upload — or a durable agent-store file — and
return its decoded text.

```yaml
- id: <step>
  activity: foundation.file.read_text
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `conversation_file_key` | string, optional | no | A conversation upload's file key (file_uploads). |
| `agent_store_file_key` | string, optional | no | A durable agent-store file key the flows stored (e.g. templates/<sha256[:16]>.html). |
| `encoding` | string | no | Default `"utf-8"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |
| `size_bytes` | integer |  |
| `mime_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.store_text`

Store text under `<stem>.<extension>`, replacing any `<stem>.*`.

```yaml
- id: <step>
  activity: foundation.file.store_text
  args:
    conversation_id: <string>
    content: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation). |
| `content` | string | yes | The document text to store (UTF-8). Must be non-empty. |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'onboarding/questions'. URL-safe, must start with an alphanumeric; any existing '<stem>.*' file is replaced. |
| `extension` | string | no | Extension appended to the stem (no leading dot). Default `"md"`. |
| `content_type` | string | no | Stored content type. Default `"text/markdown"`. |
| `filename` | string, optional | no | Display filename echoed in the output (e.g. the source document's title) for envelope/attachment use; defaults to the final key's leaf. |

**Returns**

Mirrors `FileCopyToStoreOutput` field-for-field so dual-source flows
can coalesce the two store steps' outputs.

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Final agent-store file key, e.g. 'onboarding/questions.md'. |
| `size_bytes` | integer |  |
| `sha256` | string |  |
| `content_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.upload_to_conversation`

Upload text or base64 bytes as a conversation file; post no message.

Returns the `conversation_file_key` for `channel.post_file`'s
`conversation_file_key` list or `file.copy_to_store`. Empty content
is refused. The key is server-minted, so a retry uploads again — use
`on_error: { retry: 0 }` when a duplicate would matter.

```yaml
- id: <step>
  activity: foundation.file.upload_to_conversation
  args:
    conversation_id: <string>
    filename: <string>
    content: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; the upload is scoped to it). |
| `filename` | string | yes | Display filename for the upload, e.g. 'quotes.xlsx'. |
| `content` | string | yes | The file body: plain text by default, base64-encoded bytes when `binary` is true. |
| `binary` | boolean | no | When true, `content` is base64 and is decoded to raw bytes server-side (images, spreadsheets, PDFs). Set `mime_type` to the real type. Default `false`. |
| `mime_type` | string | no | MIME type stored on the upload. Binary uploads MUST set the real type so clients render the file. Default `"text/plain"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string | The new file_uploads key, scoped to this conversation. |
| `size_bytes` | integer | Stored size (decoded bytes). |
| `filename` | string | Echoes the input filename. |
| `mime_type` | string | Echoes the input mime_type. |
