---
id: activities-feature-mbox
title: feature.mbox
order: 135
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.mbox activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.mbox` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.mbox.index`

*Beta.*

Download an mbox from the agent store and build its message index.

Materializes the mbox into the worker's local cache and builds a per-message
sidecar (offsets + ids + dates) so chunk processors can range-fetch their
slice without scanning the whole file. Returns the total message count and
local paths for `mbox.plan_chunks` and the chunk steps.

```yaml
- id: <step>
  activity: feature.mbox.index
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Conversation that owns the mbox file upload. |
| `file_key` | string | yes | Key under /v1/files where the mbox file lives. |
| `rebuild` | boolean | no | Force a fresh sidecar build, ignoring any cached sidecar. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `total_messages` | integer |  |
| `local_mbox_path` | string |  |
| `local_sidecar_path` | string |  |
| `mbox_file_key` | string |  |

### `feature.mbox.index_progression`

*Beta.*

Discover a numbered mbox progression from a base key and index each part.

`base_file_key` is the prefix the parts share (`something.mbox` for
`something.mbox.1` / `.2` / …). A lone file with no numbered parts is
processed as a single file, so this is back-compatible with the original
single-mbox backfill.

```yaml
- id: <step>
  activity: feature.mbox.index_progression
  args:
    conversation_id: <string>
    base_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Conversation that owns the mbox file uploads. |
| `base_file_key` | string | yes | Base key the numbered parts share under /v1/files. The parts `<base>.1`, `<base>.2`, … are discovered contiguously; a lone `<base>` with no parts is indexed as a single file. |
| `rebuild` | boolean | no | Force a fresh sidecar build for each part. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `total_messages` | integer |  |
| `files` | list of MboxFileIndex |  |
| `file_keys` | list of string |  |

`MboxFileIndex`:

| Field | Type | Notes |
|---|---|---|
| `file_key` | string |  |
| `total_messages` | integer |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.mbox.plan_chunks`

*Beta.*

Split a message index into contiguous `[start, end)` ranges.

Pure compute: given `total_messages` (from `mbox.index`) and a
`chunk_size`, returns the chunk ranges a flow can `foreach` over, each
then processed by `mbox.process_chunk`. The chunk — not the
individual email — is the unit of replay, keeping the Temporal event history
small for large mboxes.

```yaml
- id: <step>
  activity: feature.mbox.plan_chunks
  args:
    total_messages: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `total_messages` | integer | yes | Number of messages in the mbox (from mbox.index). |
| `chunk_size` | integer | no | Messages per chunk. 500 is a reasonable default for live AI extraction concurrency=8 with the per-message-id cache. Default `500`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `chunks` | list of MboxChunk |  |
| `chunk_count` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.mbox.plan_progression`

*Beta.*

Flatten `mbox.index_progression`'s per-file list into chunk ranges.

Each file is split into `[start, end)` ranges of `chunk_size` messages;
every chunk carries its file's `file_key` / `local_mbox_path` /
`progress_offset` so one `foreach` processes the whole progression.

```yaml
- id: <step>
  activity: feature.mbox.plan_progression
  args:
    files: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `files` | list of MboxFileIndex | yes | Per-file index output from mbox.index_progression. |
| `chunk_size` | integer | no | Messages per chunk (matches mbox.plan_chunks). Default `500`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `chunks` | list of MboxChunk |  |
| `chunk_count` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

`MboxFileIndex`:

| Field | Type | Notes |
|---|---|---|
| `file_key` | string |  |
| `total_messages` | integer |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.mbox.process_chunk`

*Beta.*

Run the watcher pipeline over one `[start, end)` slice of an mbox.

The "fat" backfill activity: opens the local mbox + sidecar (from
`mbox.index`), iterates its range, and runs each message through the same
Tier0-3 filter + LLM extractor + agent-store resolver as the live watcher.
The chunk is the unit of replay; writes are idempotent under run-scoped
keys. `seed_only=True` (PDF-seeded) only patches existing rows and is
parallel-safe; `seed_only=False` (legacy) creates rows, so it runs serial.

Reads its slice from a materialized mbox.

```yaml
- id: <step>
  activity: feature.mbox.process_chunk
  args:
    conversation_id: <string>
    chunk: ...
    mbox_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation that owns the source + the target table. |
| `chunk` | MboxChunk | yes | One entry from mbox.plan_chunks.output.chunks. |
| `my_emails` | list of string | no |  |
| `my_domains` | list of string | no |  |
| `keep_tiers` | list of string | no | Soft filter tiers to keep-and-tag instead of dropping. Only tier2/tier3 are overridable; empty preserves delivery behavior. |
| `pool_self_sent` | boolean | no | Pool Tier-0 self-sent mail as outbound metadata while still dropping it from normal processing. Default `false`. |
| `detections_mode` | boolean | no | Write metadata-only detection pool records and bypass shipment resolution/AI. Used only by Automation Coordinator. Default `false`. |
| `table_name` | string | no | Target agent-store table. `tracker` for the PDF flow's table; `shipments` for the watcher's own (legacy). Default `"shipments"`. |
| `seed_only` | boolean | no | When true (production), the resolver drops unmatched emails instead of creating fresh shipments. Default `false`. |
| `ai_provider` | string | no | anthropic / bedrock. Maps to AIExtractor's provider. Default `"anthropic"`. |
| `ai_model` | string, optional | no | Model id. Falls back to provider default (claude-haiku-4-5-20251001) when unset. |
| `ai_batch_size` | integer | no | Per-flush batch size. The LLM-first validation found 15 produced per-email AI dropout; 5 is the safer default. Default `5`. |
| `enable_semantic_match` | boolean | no | Tracker mode only: enable the LLM-adjudicated semantic match tier (2.5) for emails that fall through the deterministic + fuzzy tiers on a vendor/designer vocabulary gap. Default `false`. |
| `semantic_shadow` | boolean | no | When the semantic tier is enabled, run it in shadow mode: log the would-be bind + confidence, persist nothing. Flip to false to enable writes once validated. Default `true`. |
| `semantic_threshold` | number | no | Minimum LLM confidence for a semantic match to bind. Default `0.8`. |
| `enable_vendor_match` | boolean | no | Tracker mode only: enable the vendor-confirmed match tier (2.4) — an email whose sender domain belongs to a row's PDF 'Vendor Id' binds on a lower description threshold (recovers VOCAB_GAP) — AND the cross-vendor gate that vetoes a fuzzy bind whose sender vendor isn't the row's. On by default. Default `true`. |
| `progress_total_messages` | integer, optional | no | Total messages across all chunks (the source's total count) — the denominator for the overall replay percentage. Paired with progress_kind to drive the status-widget progress bar. |
| `mbox_file_key` | string | yes | Key under /v1/files for the mbox. The activity materializes the mbox + sidecar into this worker's local cache from the agent store if absent, so it need NOT run on the same worker as mbox.index. |
| `local_mbox_path` | string | no | Same-worker fast-path hint from mbox.index. Ignored for correctness — the cache path is derived from mbox_file_key. Default `""`. |

**Returns**

Per-chunk counters. Aggregated by the DSL flow's collect step.

(Formerly `MboxProcessChunkOutput` in the activities layer; relocated to
the pure domain so both the worker and the runtime return the same shape.)

| Field | Type | Notes |
|---|---|---|
| `chunk_start` | integer |  |
| `chunk_end` | integer |  |
| `total` | integer |  |
| `dropped` | integer |  |
| `ai_queued` | integer |  |
| `ai_resolved` | integer |  |
| `kept_deterministic` | integer |  |
| `parse_errors` | integer |  |
| `ai_failed` | integer |  |
| `ai_no_key` | integer |  |
| `raw_fetched` | integer |  |
| `metadata_fetched` | integer |  |
| `phase_ms` | map of integer |  |
| `cpu_ms` | map of integer |  |
| `runtime_invoke_seq` | integer |  |
| `runtime_uptime_ms` | integer |  |
| `invoke_wall_ms` | integer |  |
| `agentcore_overhead_ms` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.mbox.replay_chunk`

*Beta.*

Replay one mbox chunk into the channel's `tracker` table: one row per
message (`{From, Subject, Date, Snippet, Body, message_id}`), upserted
with `merge_on=[message_id]` so re-replay is idempotent. No Gmail /
AgentCore dependency — the local-testing companion to `email.list`.

Inherits `StatusProgressArgs` (`progress_kind` / `progress_pct_start`
/ `progress_pct_end`) so the replay flow can drive a status-widget
progress bar across the serial chunks; dormant when `progress_kind` is
unset.

```yaml
- id: <step>
  activity: feature.mbox.replay_chunk
  args:
    conversation_id: <string>
    mbox_file_key: <string>
    chunk: ...
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation that owns the mbox + the target table. |
| `mbox_file_key` | string | yes | Key under /v1/files for the mbox. The activity materializes the mbox + sidecar into this worker's local cache from the agent store if absent, so it need NOT run on the same worker as mbox.index. |
| `local_mbox_path` | string | no | Same-worker fast-path hint from mbox.index. Ignored for correctness — the cache path is derived from mbox_file_key. Default `""`. |
| `chunk` | MboxChunk | yes | One entry from mbox.plan_chunks.output.chunks. |
| `snippet_chars` | integer | no | Max characters of Body kept in the Snippet column. Default `200`. |
| `table_name` | string | no | Target agent-store table (the emailreader channel table; the platform-convention primary table name). Default `"tracker"`. |
| `upsert_batch_size` | integer | no | Rows per insert_records call. Sub-batched so a chunk of full bodies isn't one multi-MB request that trips the client timeout. Default `100`. |
| `progress_total_messages` | integer, optional | no | Total messages across all chunks (mbox.index.total_messages) — the denominator for the overall replay percentage. Paired with progress_kind to drive the status-widget progress bar. |

**Returns**

Per-chunk counters. Aggregated by the DSL flow's collect step; a gap in
`batch_number` across the collected list reveals a skipped chunk.

| Field | Type | Notes |
|---|---|---|
| `chunk_start` | integer |  |
| `chunk_end` | integer |  |
| `batch_number` | integer |  |
| `total` | integer |  |
| `rows_written` | integer |  |
| `no_id` | integer |  |
| `parse_errors` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |
