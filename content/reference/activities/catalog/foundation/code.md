---
id: activities/catalog/foundation/code
title: foundation.code
order: 107
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.code activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.code` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.code.execute`

Run a customer-supplied code block and return its output dict.

`code_name` names a block shipped in the app bundle at `code/<name>/`
— any flow in the bundle may call any block in it, and the block comes
from the same bundle version the flow was pinned from. The block's
`run(inputs) -> dict` return value becomes `$steps.<id>.output`.
Retry is flow-owned: with `on_error.retry`
omitted the step runs on the default policy (up to 4 attempts), so set
`retry: 0` when `run()` is not idempotent.

`reads` and `writes` let the step do its store I/O inside this one
activity, both declared in the YAML. Each read (`list_rows`,
`get_records`, `get_scalar`, `get_file`, `get_file_url`) is
delivered under its `name` in `inputs`. Each write (`patch_rows`,
`ensure_table`, `upsert_rows`, `set_scalar`, `upload_file`) takes
the value returned under its `name` and stores it; consumed keys leave
the step output and
an `applied` summary takes their place (so `applied` is a reserved
output key whenever writes are declared). The block stays a pure function
of named inputs to named outputs and never sees the store. Both sides
target the run's own conversation; nothing names one.

Pure bundle blocks may opt into `recompute_on_stale` to re-read and
recalculate after a revision conflict. Only leading `patch_rows` can
trigger it; subsequent writes never cause a recomputation. This is not
a transaction: successful patches stay committed. The block must handle
its own already-applied operations on fresh rows, using fixed time and
operation IDs from inputs.
On recomputation, the reserved `inputs._code_recompute` list records
each earlier attempt's successful `applied` row references and its
`output` (excluding consumed writes). A block can preserve completed
outcomes and avoid reapplying an older intent to those targets. Staff
actions should also declare `patch_rows.skip_completed: true`.

The block has outbound internet access: plain HTTP(S) (`urllib.request`
or a client in the block's requirements.txt) reaches public, keyless
APIs with no connection. Some hosts refuse a custom User-Agent (ESPN's
public API does), so keep the default. A source needing an API key reads
it through `env`; one needing a member's login is a connection.

`env` names the workspace secrets (`/admin/workspace-secrets`) the
block may read, each set as an environment variable of the same name.
Names only: values are fetched and encrypted inside the activity.
Customer output and error messages are published to workflow history.
Missing names fail non-retryably, listing every missing name at once.

`self_test` swaps `run()` for the block's own test suite: the runner
collects `tests/` beside the entrypoint under pytest (an image
dependency, never the block's requirements.txt), deselects tests marked
`repo`, and the step output is the report. Reads still resolve and
reach the tests as the `inputs` fixture; writes, env and
recompute_on_stale are refused. Python blocks only.

Two timeouts. `timeout_seconds` (this arg) bounds the runner's
execution of `run()` only. The STEP-level `timeout_seconds` in the
flow YAML bounds the whole activity attempt — reads, runner round trip
and writes — so a step with `reads` or `writes` must budget for the
store calls on top of the runner time.

```yaml
- id: <step>
  activity: foundation.code.execute
  args:
    code_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `code_name` | string | yes | Name of a code block shipped in this app bundle (the directory under code/). |
| `inputs` | object | no | Default `{}`. |
| `reads` | list of any | no | Store reads resolved inside the activity and delivered to the block in inputs under each entry's name. Types: list_rows (table_name, filter?, limit?, all_pages?, include_timestamps?), get_records (table_name, record_ids, missing_ok?), get_scalar (key, default?), get_file (file_key; base64 content, capped), get_file_url (file_key; presigned URL). |
| `writes` | list of any | no | Store writes applied inside the activity after run() returns, each fed by the block output key in its name (the key is then removed from the step output). Types: patch_rows (table_name; list of {record_id, expected_rev, data, change?}), ensure_table (table_name; schema), upsert_rows (table_name, merge_on?, on_conflict?; value is a list of row dicts), set_scalar (key; value is a string), upload_file (filename, content_type?, encoding text/base64; permanent; value is the content string). The step output gains applied = {count, file_keys}; patch_rows also reports patched and stale. |
| `env` | list of string | no | Workspace secret names (as set under /admin/workspace-secrets) exposed to run() as environment variables of the same name. Names only; values are read inside the activity. A name the workspace has not set fails the step. |
| `timeout_seconds` | integer | no | Seconds the runner gives run() itself. The step-level timeout_seconds in the flow bounds the whole attempt, including reads and writes. Default `60`. |
| `self_test` | boolean | no | Run the block's own test suite instead of run(): the runner collects tests/ beside the entrypoint under pytest (Python blocks only), deselects tests marked `repo`, and returns {ok, exit_code, passed, failed, errors, skipped, failures, summary, report}. `reads` still resolve and reach the tests as the `inputs` fixture; writes, env and recompute_on_stale are not allowed. Default `false`. |
| `recompute_on_stale` | integer | no | For pure, repeatable blocks: maximum re-reads and recomputations after a revision conflict in leading patch_rows writes. All patch_rows must precede other writes. Previously committed patches remain committed; the block must recognize its own operations on fresh rows. Pass time and operation IDs as fixed inputs. Default 0 fails on a conflict without recomputing. Default `0`. |

`EnsureTableWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string |  |
| `table_name` | string |  |

`GetFileRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the file under |
| `file_key` | string |  |

`GetFileUrlRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the URL under |
| `file_key` | string |  |

`GetRecordsRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string |  |
| `table_name` | string |  |
| `record_ids` | list of integer |  |
| `missing_ok` | boolean |  |

`GetScalarRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the value under |
| `key` | string |  |
| `default` | string, optional |  |

`GetTableSchemaRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the schema under |
| `table_name` | string |  |
| `missing_ok` | boolean |  |

`ListRowsRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the rows under |
| `table_name` | string |  |
| `filter` | object, optional |  |
| `limit` | integer |  |
| `missing_ok` | boolean |  |
| `drop_columns` | list of string |  |
| `all_pages` | boolean |  |
| `include_timestamps` | boolean |  |

`PatchRowsWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string |  |
| `table_name` | string |  |
| `on_stale` | `fail` / `skip` |  |
| `skip_completed` | boolean |  |
| `project_states` | boolean |  |

`SetScalarWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | output key holding the string value |
| `key` | string |  |
| `change` | object, optional |  |

`UploadFileWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | output key holding the file content |
| `filename` | string |  |
| `content_type` | string |  |
| `encoding` | `text` / `base64` |  |

`UpsertRowsWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | output key holding the list of row dicts |
| `table_name` | string |  |
| `merge_on` | list of string, optional |  |
| `on_conflict` | `replace` / `merge`, optional |  |
| `change` | object, optional |  |
