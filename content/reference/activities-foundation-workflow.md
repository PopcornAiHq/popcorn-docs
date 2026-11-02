---
id: activities-foundation-workflow
title: foundation.workflow
order: 124
group: Activities
parent: activities-foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.workflow activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.workflow` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.workflow.batch_items`

Split a list into fixed-size batches.

Chunks `items` into groups of at most `batch_size` (optionally capped
at `max_items` first). Returns `batches`, `indexed_batches` (each with
start/end offsets), and the item/batch counts — typically fed into a
`foreach` over the batches.

```yaml
- id: <step>
  activity: foundation.workflow.batch_items
  args:
    items: <array>
    batch_size: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `items` | list of any | yes | Items to split into batches. |
| `batch_size` | integer | yes | Maximum number of items in each batch. |
| `max_items` | integer, optional | no | Optional cap before batching. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `batches` | list of list of any |  |
| `indexed_batches` | list of IndexedBatch |  |
| `item_count` | integer |  |
| `batch_count` | integer |  |

`IndexedBatch`:

| Field | Type | Notes |
|---|---|---|
| `batch_number` | integer |  |
| `start_index` | integer |  |
| `end_index` | integer |  |
| `items` | list of any |  |

### `foundation.workflow.coalesce`

Return the first value in `values` that is not `None`/empty.

"Empty" means `None` or an empty string — so a skipped branch (whose
output ref resolves to `None`) and a branch that produced an empty key
are both treated as absent. Falls back to `None` when every value is
empty.

```yaml
- id: <step>
  activity: foundation.workflow.coalesce
  args:
    values: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `values` | list of any | yes | Candidate values, in priority order; first non-empty wins. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `value` | any |  |

### `foundation.workflow.fail`

Terminate the flow with a structured, non-retryable failure.

Raises an application error carrying `reason`, an optional `code` (the
error type, default `WorkflowFailed`), and optional `details`. Use to
hard-stop a flow when a precondition isn't met.

```yaml
- id: <step>
  activity: foundation.workflow.fail
  args:
    reason: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `reason` | string | yes |  |
| `code` | string, optional | no |  |
| `details` | object, optional | no |  |

### `foundation.workflow.format_text`

Render a `str.format` template with named values.

Substitutes `values` into `template` (Python `{name}` fields) and
returns the rendered `text`. Fields are bare names only: conversion
(`{name!r}`) and format specs (`{n:>4}`) work, but attribute and
index access (`{a.b}`, `{a[0]}`) are rejected as a malformed
template, as is a width or precision above `_MAX_SPEC_NUMBER`. A
missing placeholder or malformed template fails the step non-retryably.

```yaml
- id: <step>
  activity: foundation.workflow.format_text
  args:
    template: <string>
    values: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `template` | string | yes |  |
| `values` | object | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |

### `foundation.workflow.hash`

Hash a string into a slash-free hex token.

```yaml
- id: <step>
  activity: foundation.workflow.hash
  args:
    text: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `text` | string | yes | The string to hash. |
| `length` | integer | no | Truncate the hex digest to this many chars; 0 = full 64-char sha256 digest. Default `0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string | The sha256 hex digest (slash-free, [0-9a-f]), truncated to `length` chars when set. |

### `foundation.workflow.log`

Emit a structured log line tied to the current run.

Logs `message` at `level` (debug/info/warn/error) with optional
structured `fields`. A side-effect-only step for flow observability;
returns `{ok: true}`.

```yaml
- id: <step>
  activity: foundation.workflow.log
  args:
    message: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message` | string | yes |  |
| `level` | `debug` / `info` / `warn` / `error` | no | Default `"info"`. |
| `fields` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |

### `foundation.workflow.now`

Read the current wall-clock time (replay-safe), taking no arguments.

Returns `unix` (epoch seconds), `unix_str` (the same as text, for
feeding straight into `store.set_scalar`), `iso` (ISO-8601 UTC) and
`unix_ms` (epoch milliseconds, for timing spans with
`math.calculate`). All four come from one clock read, so `unix` is
`unix_ms` truncated to the second.
Flows call this instead of reading the clock directly, since the
interpreter workflow body is deterministic.

```yaml
- id: <step>
  activity: foundation.workflow.now
```

Takes no arguments of its own.

**Returns**

| Field | Type | Notes |
|---|---|---|
| `unix` | integer |  |
| `unix_str` | string |  |
| `iso` | string |  |
| `unix_ms` | integer |  |

### `foundation.workflow.parse_app_agent`

Coerce `agent` to the canonical app-agent vocabulary.

```yaml
- id: <step>
  activity: foundation.workflow.parse_app_agent
  args:
    agent: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `agent` | string | yes | Requested switch position, any casing/whitespace. 'off' passes through; anything else (empty included) coerces to 'on'. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `agent` | string |  |

### `foundation.workflow.parse_app_mode`

Coerce `mode` to the canonical app-mode vocabulary.

```yaml
- id: <step>
  activity: foundation.workflow.parse_app_mode
  args:
    mode: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `mode` | string | yes | Requested mode, any casing/whitespace. 'test' and 'off' pass through; anything else (empty included) coerces to 'prod'. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `mode` | string |  |

### `foundation.workflow.parse_send_mode`

Coerce `mode` to the canonical send-mode vocabulary.

```yaml
- id: <step>
  activity: foundation.workflow.parse_send_mode
  args:
    mode: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `mode` | string | yes | Raw popcorn.email_send_mode value, any casing/whitespace. 'draft' and 'send' pass through; anything else (empty included) coerces to 'off'. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `mode` | string |  |

### `foundation.workflow.render_template`

Render `template` (Jinja text, typically `$channel.templates.<stem>`)
against `data`. Top-level keys of `data` are exposed directly
(`{{ first_name }}`) and under `data` (`{{ data.first_name }}`).
A template error fails the step non-retryably: the template ships with
the channel, so retrying cannot fix it.

```yaml
- id: <step>
  activity: foundation.workflow.render_template
  args:
    template: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `template` | string | yes | Jinja template text. |
| `data` | object | no | Values the template renders. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string | The rendered plain text. |

### `foundation.workflow.start_flow`

Launch a sibling customer flow (installed in this conversation) by name.

Resolves `flow_name` against the conversation's installed flows and
starts it with `inputs`. The interpreter does NOT apply `$inputs.X`
defaults for launched runs, so every required input of the target flow must
be supplied explicitly in `inputs`.

```yaml
- id: <step>
  activity: foundation.workflow.start_flow
  args:
    conversation_id: <string>
    flow_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Target conversation (sets X-Active-Conversation-ID). |
| `flow_name` | string | yes | Name of the flow to launch, as installed in the conversation (e.g. 'email_backfill_gmail'). |
| `inputs` | object | no | Map of input name → value passed to the launched flow. |
| `provider` | string, optional | no | DEPRECATED, ignored. Was the connector key of the removed provider-arg override; declared only so flows stored before the `integrations` rename still pass input validation. |
| `best_effort` | boolean | no | Launch on the batch tier even though the target flow does not declare `best_effort: true` itself. Implied whenever the launching flow is not on the realtime queue (a scheduled tick on system, the eval driver on batch), so background fan-out never lands on realtime; set it to send a realtime parent's launch to the batch tier too. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `workflow_id` | string | The launched flow's workflow id. |
| `run_id` | string | Its first execution run id. |
| `started` | boolean | True when a launch was issued (always true on success; kept for parity with caller dedup logic). |

### `foundation.workflow.update_schedule`

Retune the cadence of a schedule attached to a sibling flow.

Addresses the schedule by the target flow's installed name (plus `slug`
when the flow has more than one schedule) rather than the raw Temporal
schedule id, so bundle YAMLs stay portable across installs.

```yaml
- id: <step>
  activity: foundation.workflow.update_schedule
  args:
    conversation_id: <string>
    flow_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Target conversation (sets X-Active-Conversation-ID). |
| `flow_name` | string | yes | Name of the scheduled flow, as installed in the conversation (e.g. 'delivery_tick'). |
| `slug` | string, optional | no | Schedule slug (e.g. 'delivery-tick'). PASS IT when you know it (bundle YAMLs always do): the schedule id is then constructed deterministically, immune to Temporal visibility lag, and required anyway when the flow has more than one schedule. Omitting it falls back to discovery via the (eventually consistent) schedule list. |
| `interval_seconds` | integer, optional | no | New fixed-interval cadence in seconds. Mutually exclusive with cron_expr. |
| `cron_expr` | string, optional | no | New cron expression. Mutually exclusive with interval_seconds. |
| `jitter_seconds` | integer, optional | no | New jitter window in seconds; 0 removes it. A COMPRESSED cadence usually has to carry this: jitter is inherited from the live schedule when a patch does not mention it, so a manifest jitter sized for the prod interval survives into a much smaller one and can be the larger of the two. Restore the manifest value on the way back out. |
| `paused` | boolean, optional | no | Pause (true) or resume (false) the schedule. May stand alone (cadence untouched) or accompany a cadence change. Omitted means keep the current paused state. |
| `note` | string, optional | no | Schedule note recorded with the patch. set_app_mode uses marker notes so lifecycle unpausers (e.g. channel unarchive, which resumes only its own 'auto-paused: channel archived' note) never resume a deliberately-off channel. |
| `fire_at` | string, optional | no | ARM A ONE-SHOT: an RFC3339 instant (with zone) the schedule fires once at, replacing any earlier arm. The rail an on-demand schedule (a manifest entry with no cadence, created paused) is driven by: a flow computes the next instant its work falls due and arms it; re-arming with a later instant replaces the earlier one whole. An EMPTY STRING disarms: the schedule is emptied and paused. A flow whose 'next due' step yields either an instant or '' can pass it straight through. Mutually exclusive with every other cadence field and with paused. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `schedule_id` | string | The patched schedule's id. |
| `interval_seconds` | integer, optional | Cadence after the patch (interval form). |
| `cron_expr` | string, optional | Cadence after the patch (cron form). |
| `jitter_seconds` | integer, optional | Jitter window after the patch. |
| `paused` | boolean, optional | Paused state after the patch. |
| `updated` | boolean | True when a patch was issued (always true on success). |
