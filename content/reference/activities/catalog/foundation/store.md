---
id: activities/catalog/foundation/store
title: foundation.store
order: 121
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.store activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.store` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.store.claim_row`

Take a row for this run: one If-Match write that admits exactly one
holder, with the row's gates checked against exactly what was read.

The lock is `column`: the claim reads the row with its `rev`,
refuses if another holder is already in the column, checks every
`refuse_when` rule against the row, then patches
`{column: holder}` conditionally on that rev. A write that landed in
between (another claimant, an edit) makes the store answer
`stale_rev` and this run is refused `held_code` — among concurrent
claimants exactly one matches the rev it read. A retry of the same
holder finds its own id in the column and returns without writing
(`claimed: false`) BEFORE the rules run: the claim it holds was
checked when it was taken, and refusing it now — the row edited in
between, the first attempt's response lost — would leave the column
held with no release path. A row the store answers without a `rev`
fails `StoreClaimRowNoRevision`: without a rev to match on there is
no single winner, and a claim that cannot promise one is no claim.
Releasing is the flow's job: it writes
`{column: ""}` on every outcome, through whatever step re-derives the
row's state, so a failed run lands the row back where it was.

This is the read-check-write of a code block's claim without the
code runner: the decision is a handful of cell comparisons, and a
`foundation.code.execute` step spends most of its time getting to
them (the runner round trip, the declared reads, the state
projection). A flow that needs the row's derived machines repainted
at claim time keeps the code step; one that only needs the lock — the
modal is open with its own spinner while the merge runs — takes this
and lets its publish step repaint.

`holder` is the claimant's identity, normally `$trigger.run_id`,
and the release step compares the column to the same value. Passing
it explicitly (rather than reading the activity's own run id) keeps
the claim and its release on one source and lets a flow claim on
behalf of a run it launched.

`wait_for_holder_seconds` > 0 polls the row once a second, for at
most that long, while another holder has it, then claims the row as
it is afterwards instead of refusing at once. For a claim a person
is waiting on that meets a short-lived holder (a merge that is about
to finish for them anyway). 0, the default, refuses at once.

`file_stem_prefix` asks for a per-claim file stem in the result:
`<prefix>/<record_id>/<holder>`, the holder reduced to key-safe
characters and its first 32 — unique per (row, holder), so files a
run produces for the row it claimed never collide with another run's
and can be swept by stem. Here because the flow language has no
string concatenation, and the claim already holds both parts.

Refusals fail the run by name — `code` becomes the failure type,
`message` its reason — so `on_error: {policy: fail}` (the default)
surfaces them to the caller exactly as `foundation.workflow.fail`
would. A row that does not exist fails `StoreClaimRowNotFound`.

```yaml
- id: <step>
  activity: foundation.store.claim_row
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
    column: <string>
    holder: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |
| `column` | string | yes | The holder column, e.g. Regenerating or Sending. |
| `holder` | string | yes | This claimant's identity; normally $trigger.run_id. An opaque, exact string: compared byte for byte with the column. |
| `held_code` | string | no | Failure type when another holder has the column, or the row changed under the claim. Default `"StoreClaimRowHeld"`. |
| `held_message` | string | no | Default `"Another run holds this row; wait for it to finish."`. |
| `refuse_when` | list of StoreClaimRefusal | no |  |
| `wait_for_holder_seconds` | number | no | Default `0.0`. |
| `file_stem_prefix` | string, optional | no | Set to get `file_stem` = <prefix>/<record_id>/<holder>. |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. regenerate_claimed. Unset = anonymous workflow write. |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for the audit row's change blob. |

**Returns**

`claimed` — this call wrote the holder into the column; false
when the column already carried this holder (a retry). `row` is the
row's cells exactly as the claim read them, BEFORE the write, so a
flow reads `$steps.<id>.output.row.<Column>` for what it is about to
act on; `rev` is the row's revision after the claim.

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `holder` | string |  |
| `claimed` | boolean |  |
| `rev` | integer, optional |  |
| `row` | object |  |
| `file_stem` | string, optional |  |

`StoreClaimCondition`:

| Field | Type | Notes |
|---|---|---|
| `column` | string |  |
| `test` | `set` / `unset` / `equals` / `not_equals` / `in` / `not_in` |  |
| `value` | string or list of string, optional |  |

`StoreClaimRefusal`:

| Field | Type | Notes |
|---|---|---|
| `code` | string | Error type the run fails with. |
| `message` | string | What the refusal tells the caller. |
| `when` | list of StoreClaimCondition |  |

### `foundation.store.create_table`

Create a new agent-store table in the conversation.

Defines `table_name` with `schema_def` (a `{"columns": [...]}` spec).
Fails if the table already exists — use `store.ensure_table` to
create-or-reconcile. `workspace_id` is taken from the auth context.

```yaml
- id: <step>
  activity: foundation.store.create_table
  args:
    conversation_id: <string>
    table_name: <string>
    schema_def: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `schema_def` | object | yes |  |

### `foundation.store.delete_files`

Best-effort delete of scratch files by key.

For cleaning up page images / staging blobs. `file_keys` accepts scalar
keys and/or lists of keys (flattened one level), so a DSL ref to a
`list[str]` output drops straight in. Per-key errors (including 404) are
swallowed so cleanup never fails the flow.

```yaml
- id: <step>
  activity: foundation.store.delete_files
  args:
    conversation_id: <string>
    file_keys: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_keys` | list of string or list of string | yes |  |

### `foundation.store.delete_row`

Hard-delete ONE table row by its agent-store record id.

The row identified by `record_id` is removed and an audit row is
written with its cells as `data_before`, so the data stays recoverable
from history. The delete is deliberate by construction: the flow must
already hold the id (from `store.list_rows`'s `_record_id` or a
`get_record`), so a retention sweep is `list_rows` with a date
`filter` and a `limit`, then this step under `foreach`.

`expected_rev` (the row's `_rev` from `list_rows`) makes the
delete conditional, as it does for `patch_row`: a row another writer
updated between the list and the delete 412s (`AgentStoreStaleRev`)
and survives, instead of the sweep deleting a row that is no longer the
one it listed. Set it whenever the filtered column can change under
you; a sweep that should simply leave such rows for its next run pairs
it with `on_error: {policy: skip, retry: 0}` on the foreach step. As
for `patch_row`, a bare Temporal retry replays the same stale rev and
cannot succeed — the conflict is the answer, not a transient, which is
why `retry: 0`: `policy: skip` alone still burns the interpreter's
default attempts with backoff on every conflicting row before skipping.

Retry semantics. The write carries the workflow's `run_id` +
`step_id`, from which agent_store derives an idempotency key, and the
delete commits in the same transaction as its cached response. A Temporal
retry of the SAME attempt (a lost response) therefore replays the cached
204 and returns `{deleted: true, existed: true}` without touching the
row again. `missing_ok` covers the other case — the row is already
gone because another run or actor removed it, the flow re-ran under a new
run id, or the cached response aged out — where the store answers 404:
`True` returns `{deleted: false, existed: false}`; `False` (the
default) fails the step. Note that agent_store 404s a missing TABLE the
same way it 404s a missing row, so `missing_ok` tolerates both — the
same conflation `list_rows.missing_ok` carries. Keep the default for
on-demand flows, where a missing table is usually a wrong table name.

```yaml
- id: <step>
  activity: foundation.store.delete_row
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |
| `missing_ok` | boolean | no | Default `false`. |
| `expected_rev` | integer, optional | no |  |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. pool_retention. Unset = anonymous workflow delete. |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for the audit row's change blob. |

**Returns**

`deleted` — this call removed the row (or replayed the cached
success of the attempt that did). `existed` — false only on the
`missing_ok` branch, when the store answered 404.

| Field | Type | Notes |
|---|---|---|
| `deleted` | boolean |  |
| `existed` | boolean |  |

### `foundation.store.ensure_table`

Create the table, or patch its schema if it already exists.

Idempotent `store.create_table`: returns `action` of `created`,
`exists` (nothing to write), or `patched`. Use this when a flow may
run repeatedly.

`on_conflict` decides what "already exists" means:

* `replace` (the default) — the stored schema becomes `schema_def`
  exactly. For a flow declaring its OWN table with its COMPLETE schema,
  which is every caller that predates the other mode.
* `merge` — `schema_def`'s columns are DECLARED on the stored table:
  the ones already there are left exactly as stored, the rest are
  appended, and nothing else about the stored definition is touched.
  For a flow reaching into a channel it does not own, where replace
  would delete every column it has never heard of. `added` names the
  columns the call declared and `blocked` the ones a stored column
  already owns on terms the caller cannot write; both are always on a
  merge answer. This mode never CREATES — see `_declare_columns`.

```yaml
- id: <step>
  activity: foundation.store.ensure_table
  args:
    conversation_id: <string>
    table_name: <string>
    schema_def: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `schema_def` | object | yes |  |
| `on_conflict` | `replace` / `merge` | no | Default `"replace"`. |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |

**Returns**

Result of ensuring a table exists with a schema.

| Field | Type | Notes |
|---|---|---|
| `action` | `created` / `exists` / `patched` | What the ensure did to reach the schema. |
| `table` | object | The resulting table metadata. |
| `added` | list of string | Columns this call declared. On every `on_conflict: merge` answer and on no other; empty when the table already declared them all. |
| `blocked` | list of string | Declared columns a stored column already owns on other terms — a different spelling of the name, another type, internal or computed — so the declaration was not made and a writer keyed on it will not reach them. On every `on_conflict: merge` answer and on no other. |

### `foundation.store.get_file_url`

Get a presigned download URL for a stored file.

Returns the URL (a bare string) for `file_key` so a later step can fetch
the bytes.

```yaml
- id: <step>
  activity: foundation.store.get_file_url
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_key` | string | yes |  |

### `foundation.store.get_record`

Fetch ONE table record by its agent-store record id.

The filter DSL only matches `data` columns, so this is the only way for a
flow to read a row by its primary-key id. The row's cells are returned
under `$steps.<id>.output.data`.

```yaml
- id: <step>
  activity: foundation.store.get_record
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |

**Returns**

One record fetched by id; cells under .data, its revision as .rev.

| Field | Type | Notes |
|---|---|---|
| `id` | integer | The record id. |
| `rev` | integer | The record's revision, the expected_rev a write fenced to this read passes. It sits beside the cells: data holds no _rev (a table read's rows do). |
| `data` | object | The row's cells. Read via $steps.<id>.output.data. |

### `foundation.store.get_scalar`

Read a conversation-scoped scalar by key.

Returns the stored `{key, value}`. Provide `default` to get that value
instead of a 404 when the key isn't set yet — useful for reading a
not-yet-initialized cursor on a flow's first run.

```yaml
- id: <step>
  activity: foundation.store.get_scalar
  args:
    conversation_id: <string>
    key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `key` | string | yes |  |
| `default` | string, optional | no |  |

### `foundation.store.list_rows`

List table records.

Returns the agent store's response with two row collections:
`records` is the raw store metadata shape, and `rows` is a
convenience list of each record's `data` object with `_record_id`
attached. Use `$steps.<id>.output.rows` when feeding table data into
`code.execute`.

```yaml
- id: <step>
  activity: foundation.store.list_rows
  args:
    conversation_id: <string>
    table_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `filter` | object, optional | no |  |
| `limit` | integer | no | Default `50`. |
| `missing_ok` | boolean | no | Default `false`. |
| `drop_columns` | list of string | no |  |

**Returns**

Table records in two views. Prefer $steps.<id>.output.rows over .records for downstream code/templating.

| Field | Type | Notes |
|---|---|---|
| `records` | list of any | Raw store records: each has `id` and a nested `data` object plus store metadata. |
| `rows` | list of any | Flattened convenience view: each record's `data` object with `_record_id` attached. Use $steps.<id>.output.rows for table data, especially as code.execute input. |

### `foundation.store.merge_json_scalar`

Deep-merge a JSON object into a JSON-object scalar.

Sends `patch` to the agent_store service, which merges it into the
stored JSON object under a row lock and writes the result back in one
atomic transaction — where both sides hold a dict at a key the merge
recurses, anything else is replaced by the patch value. For envelope
scalars several flows share (e.g. the onboarding-state `steps` map,
where each upload flow patches its own step id), where a plain
`set_scalar` — or a shallow merge — would clobber the sibling entries.
Concurrent merges to the same key serialize under the row lock and
converge correctly. Still not a counter: the server merges *objects*,
not numbers — an increment (`$inc`) primitive is deliberately not built.

```yaml
- id: <step>
  activity: foundation.store.merge_json_scalar
  args:
    conversation_id: <string>
    key: <string>
    patch: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `key` | string | yes |  |
| `patch` | object | yes |  |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |

### `foundation.store.patch_row`

Update one table row's cells by its record id.

Applies `patch` (column → value) to the row identified by `record_id`;
columns not in the patch are left unchanged. Without a fence the write
lands whatever else changed. A fence makes it conditional on what the
caller read, and a write it refuses 412s (`AgentStoreStaleRev`)
instead of silently clobbering. One fence per call:

* `expected_rev` (the row's `_rev`): nothing in the row changed;
* `unchanged_since` + `unchanged`: these columns did not change.
  The patched columns are always among them; other cells may have
  moved, and the patch lands over them on the fresh revision.

```yaml
- id: <step>
  activity: foundation.store.patch_row
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
    patch: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |
| `patch` | object | yes |  |
| `expected_rev` | integer, optional | no | Fence: write only if NOTHING in the row changed since it was read, given as the revision read (the row's _rev). Any other write in between refuses it (AgentStoreStaleRev). Not with unchanged_since. |
| `unchanged_since` | object, optional | no | Fence: write only if the patched columns and the `unchanged` ones still hold what they held in this row as it was read: a list_rows row (cells plus _rev) or a get_record result (data plus rev). It must carry its revision. Other cells may have changed since, and are kept. Not with expected_rev. |
| `unchanged` | list of string | no | With unchanged_since: the columns the write was decided on besides the ones it patches (those are always checked). Any of them changed refuses the write (AgentStoreStaleRev), naming them. |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. investigation_applied. Unset = anonymous workflow write. |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for the audit row's change blob. |

### `foundation.store.patch_rows`

*Beta.*

Update several rows of one table in one step.

Each entry of `patches` is applied exactly as `patch_row` would apply
it: a merge of `patch` into the row `record_id`, conditional on
`expected_rev` when set, with its own audit row and realtime event.
At most 100 entries; an empty list is a no-op. A `record_id` may appear
once.

NOT atomic. Each row lands or not on its own, and the output reports
every row's fate in input order: `patched`, `conflict` (the row moved
past `expected_rev`; `rev` is its current one), `not_found`, or
`rejected` (the store refused the patch, e.g. a validation error).
None of these fail the step — gate on the counts (`rejected`,
`conflicts`) if the flow needs to. A missing table fails it, as does a
store or network error, which Temporal retries; rows already written
replay their cached result, not a second write.

`change_kind` / `change_action` / `change_detail` attribute every
row's audit entry as `patch_row`'s do; `fields` is each row's own
patched columns.

```yaml
- id: <step>
  activity: foundation.store.patch_rows
  args:
    conversation_id: <string>
    table_name: <string>
    patches: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `patches` | list of StorePatchRowsItem | yes |  |
| `change_kind` | string, optional | no | change.kind slug for every row's audit entry, e.g. triage_applied. Unset = anonymous workflow write. |
| `change_action` | string, optional | no | Human one-liner for the audit rows (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for every row's change blob. |

**Returns**

Per-row results in input order, plus a count per status. No row's
cells are returned: a hundred records would be history-sized.

| Field | Type | Notes |
|---|---|---|
| `results` | list of StorePatchRowsResult |  |
| `patched` | integer |  |
| `conflicts` | integer |  |
| `not_found` | integer |  |
| `rejected` | integer |  |

`StorePatchRowsItem`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `patch` | object |  |
| `expected_rev` | integer, optional |  |

`StorePatchRowsResult`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `status` | `patched` / `conflict` / `not_found` / `rejected` |  |
| `rev` | integer, optional |  |
| `error` | string, optional |  |

### `foundation.store.set_scalar`

Set a conversation-scoped scalar (a named key/value).

Writes `value` under `key` — a small piece of flow state (e.g. a cursor
or last-success timestamp) read back later with `store.get_scalar`.

```yaml
- id: <step>
  activity: foundation.store.set_scalar
  args:
    conversation_id: <string>
    key: <string>
    value: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `key` | string | yes |  |
| `value` | string | yes |  |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |

### `foundation.store.upload_file`

Upload a text file into the conversation's agent store.

Stores `content` under `filename` with `content_type` and returns the
file metadata (including `file_key`). Set `lifetime="workflow"` for a
scratch file reaped when the workflow chain closes; omit it for a durable
file.

```yaml
- id: <step>
  activity: foundation.store.upload_file
  args:
    conversation_id: <string>
    filename: <string>
    content: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `filename` | string | yes |  |
| `content` | string | yes |  |
| `content_type` | string | no | Default `"text/plain"`. |
| `lifetime` | string, optional | no |  |

### `foundation.store.upsert_rows`

Insert or merge rows into an agent-store table.

Provide exactly one of `rows` (inline) or `rows_file_key` (a staged
blob). With `merge_on` columns an existing match is updated rather than
duplicated; `on_conflict` chooses `replace` (default) or `merge` (keep
the columns the incoming row omits). `change_kind` / `change_action`
name the write in the audit log (see `patch_row`); without them a write
with no source file is anonymous.

```yaml
- id: <step>
  activity: foundation.store.upsert_rows
  args:
    conversation_id: <string>
    table_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `rows` | list of object, optional | no |  |
| `rows_file_key` | string, optional | no |  |
| `merge_on` | list of string, optional | no |  |
| `on_conflict` | string, optional | no |  |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. lead_intake. Unset = anonymous workflow write (or the import kind, when a source file is given). |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |
