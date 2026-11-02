---
id: activities-feature-xlsx
title: feature.xlsx
order: 143
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.xlsx activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.xlsx` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.xlsx.attach_row_images`

*Beta.*

Attach an XLSX's embedded images to the rows parsed from it.

```yaml
- id: <step>
  activity: feature.xlsx.attach_row_images
  args:
    conversation_id: <string>
    conversation_file_key: <string>
    rows_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the source XLSX and images (must be the flow's own conversation). |
| `conversation_file_key` | string | yes | Conversation-level source XLSX file key (file_uploads). |
| `rows_file_key` | string | yes | Staged rows blob from feature.xlsx.parse. Rows must still carry the `_xlsx_sheet` / `_xlsx_row` anchor bookkeeping. |
| `progress_after_seconds` | number | no | Minimum elapsed time before the first progress update. Default `2.0`. |
| `progress_every_seconds` | number | no | Minimum elapsed time between progress updates. Default `2.0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows_file_key` | string |  |
| `row_count` | integer |  |
| `image_count` | integer |  |

### `feature.xlsx.parse`

*Beta.*

Parse an uploaded XLSX workbook into generic rows.

```yaml
- id: <step>
  activity: feature.xlsx.parse
  args:
    conversation_id: <string>
    conversation_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the source XLSX (must be the flow's own conversation). |
| `conversation_file_key` | string | yes | Conversation-level source XLSX file key (file_uploads). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | XlsxParseSource |  |
| `sheet_count` | integer |  |
| `row_count` | integer |  |
| `rows_file_key` | string |  |

`XlsxParseSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |
