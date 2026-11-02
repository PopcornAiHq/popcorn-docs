---
id: activities/catalog/feature/state
title: feature.state
order: 142
group: Activities
parent: activities/catalog/feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.state activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.state` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.state.check`

Hold every row to the graph: each stored machine column holds a
declared state, a derive mirror agrees with the value the bundle
supplies, and Status is what the row's tuple composes to. With
`machines` supplied the derived ones are checked too; without, a
Status that only a derived overlay could explain is not an offender.

```yaml
- id: <step>
  activity: feature.state.check
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `machines` | map of map of string | no | Derived machine values per record id (as a string): {record_id: {machine: state}}. |
| `why` | map of string | no | Why prose per record id; the shown state's declared default otherwise. |
| `machine_why` | map of map of string | no | Per record id, prose per derive machine, written to its why_column: {record_id: {machine: text}}. |
| `guards` | map of list of string | no | The EXTERNAL guards that hold, per record id (as a string): {record_id: [guard, …]}. The bundle evaluates them; an edge behind one not listed here is not legal for that row. |
| `messages` | map of string | no | Chat-rail message override per CTA kind; the cta's own templated message otherwise. |
| `issue_fields` | map of object | no | Extra worklist columns per record id (bundle prose: name, contact, context). |
| `page_limit` | integer | no | Default `1000`. |
| `record_ids` | list of integer | no |  |
| `fail_step` | boolean | no | Default `false`. |
| `allow_blank_status` | boolean | no | Let a blank Status pass. Off by default: every tuple composes to a state, so a blank is a row projection never reached. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `rows` | integer |  |
| `offenders` | list of StateOffender |  |
| `offender_count` | integer |  |
| `summary` | string |  |

`StateOffender`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `column` | string |  |
| `value` | any |  |
| `problem` | string |  |

### `feature.state.project`

Re-derive the projection for rows from their tuple.

With no `record_ids` every row of the table is projected (the tick's
sweep) and the whole worklist reconciled; with some, only their own
worklist items may resolve. `write: false` computes without
patching, for a flow that wants to look first. `results` narrows
the per-row report: `warn` is the rows that are work items.

```yaml
- id: <step>
  activity: feature.state.project
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `machines` | map of map of string | no | Derived machine values per record id (as a string): {record_id: {machine: state}}. |
| `why` | map of string | no | Why prose per record id; the shown state's declared default otherwise. |
| `machine_why` | map of map of string | no | Per record id, prose per derive machine, written to its why_column: {record_id: {machine: text}}. |
| `guards` | map of list of string | no | The EXTERNAL guards that hold, per record id (as a string): {record_id: [guard, …]}. The bundle evaluates them; an edge behind one not listed here is not legal for that row. |
| `messages` | map of string | no | Chat-rail message override per CTA kind; the cta's own templated message otherwise. |
| `issue_fields` | map of object | no | Extra worklist columns per record id (bundle prose: name, contact, context). |
| `page_limit` | integer | no | Default `1000`. |
| `record_ids` | list of integer | no |  |
| `write` | boolean | no | Default `true`. |
| `results` | `all` / `changed` / `warn` | no | Default `"all"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows` | integer |  |
| `results` | list of ProjectedRow |  |
| `projected` | integer | Rows whose projection changed. |
| `unknown` | integer | Rows holding a value outside the graph. |
| `patched` | integer |  |
| `stale` | list of object |  |
| `worklist` | object | {open, resolved, upserted}. |

`ProjectedRow`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `outcome` | string | projected / unchanged / unknown_state |
| `status` | string |  |
| `tuple` | map of string |  |
| `ctas` | list of object |  |
| `why` | string |  |
| `warn` | boolean |  |
| `policy` | object |  |
| `changed` | list of string |  |
| `reason` | string |  |

### `feature.state.spec`

No arguments: the graph is the pinned manifest's.

```yaml
- id: <step>
  activity: feature.state.spec
```

Takes no arguments of its own.

**Returns**

| Field | Type | Notes |
|---|---|---|
| `table` | string |  |
| `status_column` | string |  |
| `status_values` | list of string | The Status column's whole vocabulary, in order. |
| `labels` | map of string | Status value → label. |
| `warn` | list of string | Status values that warn. |
| `work_items` | list of string | Status values that open a worklist item: the reds, and any state declared `work_item: true`. |
| `tones` | map of string | Status value → tone. |
| `machines` | map of MachineSummary |  |
| `events` | map of list of string |  |
| `hints` | map of string | Column → display hint. |
| `mermaid` | map of string | Machine → stateDiagram-v2. |
| `spine` | map of string | Machine → stateDiagram-v2 of the EXPECTED edges only. Every edge in `mermaid` is legal and most are rare, so a graph that draws them alike shows a lead routinely going straight from its first state to archived; this is the path it actually takes. A machine that marks nothing expected has no entry. |
| `edges` | map of list of MachineEdgeOut | Machine → its arrows, for a client drawing its own graph. Includes edges another machine's transition moves this one through `also:`, which a walk over transitions by machine misses entirely — that is how a whole arm of a graph ends up rendered as unreachable floating states. |
| `spec` | object | The states: section as declared. |

`MachineEdgeOut`:

| Field | Type | Notes |
|---|---|---|
| `on` | string |  |
| `source` | string | The state the edge leaves. Empty when an `also:` edge's `when:` never says, which is honest rather than a guess. |
| `target` | string |  |
| `expected` | boolean | Is this the path a row is expected to take, or only one it may? |
| `importance` | integer | How loudly to draw it, 1–10 on one scale across every machine of the spec (10 is the spine through the firm's decisions, 1 an internal machine's bookkeeping). Display only. |
| `via` | string | The machine whose transition declared it, for an `also:` edge. |

`MachineSummary`:

| Field | Type | Notes |
|---|---|---|
| `column` | string, optional |  |
| `overlay` | boolean |  |
| `derive` | boolean |  |
| `internal` | boolean |  |
| `initial` | string |  |
| `states` | list of string |  |
| `groups` | map of list of string |  |

### `feature.state.transition`

Fire one event on some rows.

`event` is `family.name` or the bare name when unique (a CTA's
`action`). `payload` feeds the edge's `payload_writes`,
`detail_from` and `then` inputs. `operation_key` is recorded on
the change stamp so a retried flow can be told from a second click.
`writes` merges the bundle's own columns into each applied row's
one patch.

```yaml
- id: <step>
  activity: feature.state.transition
  args:
    event: <string>
    record_ids: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `machines` | map of map of string | no | Derived machine values per record id (as a string): {record_id: {machine: state}}. |
| `why` | map of string | no | Why prose per record id; the shown state's declared default otherwise. |
| `machine_why` | map of map of string | no | Per record id, prose per derive machine, written to its why_column: {record_id: {machine: text}}. |
| `guards` | map of list of string | no | The EXTERNAL guards that hold, per record id (as a string): {record_id: [guard, …]}. The bundle evaluates them; an edge behind one not listed here is not legal for that row. |
| `messages` | map of string | no | Chat-rail message override per CTA kind; the cta's own templated message otherwise. |
| `issue_fields` | map of object | no | Extra worklist columns per record id (bundle prose: name, contact, context). |
| `page_limit` | integer | no | Default `1000`. |
| `event` | string | yes |  |
| `record_ids` | list of integer | yes |  |
| `payload` | object | no |  |
| `operation_key` | string | no | Default `""`. |
| `writes` | map of RowWrites | no | Bundle writes per record id (as a string): {record_id: {rev, data}}; merged into the row's patch when the edge applies, refused StaleRev when rev moved. |
| `conversation_id` | string | no | Resolves $conversation_id in then inputs. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `event` | string |  |
| `results` | list of TransitionRow |  |
| `applied` | integer |  |
| `launch` | integer | Rows whose edge is a flow to start. |
| `refused` | integer |  |
| `not_found` | integer |  |
| `patched` | integer |  |
| `stale` | list of object |  |
| `launches` | list of Launch | Every flow to start, across rows: flow edges and then entries, inputs resolved. |
| `first_refusal` | Refusal, optional | The first refused row, for a flow that fails by name when nothing applied. |
| `worklist` | object |  |

`Launch`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `flow` | string |  |
| `inputs` | object |  |

`Refusal`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `code` | string |  |
| `reason` | string |  |

`RowWrites`:

| Field | Type | Notes |
|---|---|---|
| `rev` | integer |  |
| `data` | object |  |

`TransitionRow`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `outcome` | string | applied / launch / refused / not_found / unknown_state |
| `reason` | string |  |
| `code` | string |  |
| `delegated` | boolean | An external guard on the edge was vouched for by the caller; its own check is what allowed it. |
| `from_status` | string |  |
| `landing_status` | string |  |
| `tuple` | map of string |  |
| `flow` | string | The flow that IS this edge, to launch per row. |
| `launches` | list of Launch | Flows the edge launches for this row after its writes, inputs resolved. |
| `effects` | list of string | Bundle-side effects the edge declares; the bundle runs them for this row. |
