---
id: activities-feature-evals
title: feature.evals
order: 131
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.evals activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.evals` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.evals.launched`

After the turns: record which of the planned turns the driver got
away, and write the terminal history row of every turn that failed
before it could score.

```yaml
- id: <step>
  activity: feature.evals.launched
  args:
    conversation_id: <string>
    run_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `run_id` | string | yes |  |
| `keys` | list of string | no | `$steps.<open>.output.keys`. |
| `cases` | list of object | no | `$steps.<open>.output.rows`: one `{Name, Rep}` per turn, all this step reads. The cases whole work too, at their weight beside every turn's output in one payload. |
| `started` | any | no | `$steps.<turns>.output`: one slot per case in the plan's order, null where the turn was skipped. |
| `error` | any | no | `$steps.<turns>.error`: the first failure the foreach absorbed. |
| `groups` | list of object | no | Further `{keys, cases, started}` triples, one per foreach the driver ran beside the first (a bundle with several kinds of case); read as one run. |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `run_id` | string |  |
| `started` | integer |  |
| `not_started` | list of string |  |
| `summary` | string |  |

### `feature.evals.mark`

A turn's first act: stamp the case's row `running` under the
turn's Run Id and repetition, and open the turn's own row in
`eval_results`. A board row that already carries a finished result
of this run is left as it is (the board keeps the run's worst).

```yaml
- id: <step>
  activity: feature.evals.mark
  args:
    conversation_id: <string>
    case: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `case` | object | yes |  |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `guidance_rev` | string | no | Default `""`. |
| `extra_columns` | object | no | The bundle's own columns to clear on the board row, e.g. where the LAST run's decision landed. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `result_id` | string |  |
| `started_at` | string |  |
| `summary` | string |  |

### `feature.evals.open`

Open the run `feature.evals.plan` planned: rebuild the seeds
from the bundle's cases against the board as it is now and write
them with the error stamps, open the run's row in `eval_runs`, and
delete the history rows the plan named. Refuses a bundle whose eval
tables lack the runner's core columns, naming them.

```yaml
- id: <step>
  activity: feature.evals.open
  args:
    conversation_id: <string>
    plan: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `plan` | object | yes | `$steps.<plan>.output.opening`. The whole plan output is accepted too, at the cost of carrying the selection twice. |
| `cases` | list of object, optional | no | The cases the bundle ships (`$steps.seed.output.cases`, the same list `plan` took): the seeds are rebuilt here, not carried over from the plan. Left out only by a driver pinned before its bundle passed them, whose plan carries `launch`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `run_id` | string |  |
| `seeded` | integer |  |
| `skipped` | list of string | Launch rows left alone because a newer run claimed the case between the plan and this open. |
| `edited` | list of string | Seeds left alone because the firm edited the row between the plan and this open (a reseeding run writes anyway). |
| `pruned` | integer |  |
| `cases` | list of object | The run to drive: the selected cases from the board as it is now, one per repetition, with their Run Id and Rep. Empty when the plan named `kinds`: the run is then under `by_kind`, and only there, so the result carries each case once. |
| `keys` | list of string | One key per case, `Name` or `Name#rep`; empty when the plan named `kinds`, like `cases`. |
| `rows` | list of object | One `{Name, Rep}` per turn, in `cases` order: what `launched` takes as its `cases`, so the corpus does not ride through that step beside every turn's output. Empty when the plan named `kinds`, like `cases`. |
| `by_kind` | map of object | `{kind: {cases, keys, rows}}` for every kind the plan named, so a driver runs `$steps.<open>.output.by_kind.<kind>.cases` and accounts with `.keys` and `.rows`; empty when it named none. |
| `names` | list of string |  |
| `count` | integer |  |
| `turns` | integer |  |
| `payload_bytes` | integer | The size of this result on the wire, against the runner's PAYLOAD_BUDGET. |
| `summary` | string |  |

### `feature.evals.plan`

Plan one eval run, writing nothing: seed the bundle's cases the
channel lacks, refresh the shipped rows nobody edited when the bundle
moved, select by `only` and multiply by `reps`, and name the
history rows a later `open` prunes. Hand the output to
`feature.evals.open` once the bundle's own check has passed the
selection.

```yaml
- id: <step>
  activity: feature.evals.plan
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `cases` | list of object | no | The cases the bundle ships (its seed block's output). Every key a case carries is a fixture column of `eval_cases`. |
| `run_id` | string | no | `$trigger.run_id`: the workflow's Temporal run id, of which eight hex make the launch time unique. Default `""`. |
| `only` | string | no | A substring of a case's Name or Section, or a comma-separated list of them; every case any term matches runs. Default `""`. |
| `reseed` | boolean | no | Replace the rows the firm edited with the bundle's shipped cases too. Default `false`. |
| `reps` | integer | no | Run every selected case this many times under one Run Id, at most ten. Default `1`. |
| `kinds` | list of string | no | The flows the bundle runs its cases as, by the row's `Kind`; the output groups the cases under `by_kind`, every kind present. Leave empty when every case runs as one flow. |
| `default_kind` | string | no | What a blank `Kind` reads as, e.g. `intake`. Default `""`. |
| `stamp_columns` | list of string | no | The bundle's own result columns on `eval_cases` (where a decision landed, e.g. `Event`, `Funnel State`): never handed to a turn as fixture. |

**Returns**

One copy of the selection (`cases`, for the bundle's check) and
the small `opening` that `feature.evals.open` takes. The rows to
seed are not here: `open` rebuilds them from the bundle's seeds and
the board. A plan's result is one Temporal payload, and the corpus
goes through it once (`payload_bytes` says how much of the budget).

| Field | Type | Notes |
|---|---|---|
| `run_id` | string |  |
| `cases` | list of object | The selection, one per repetition, for the bundle's check; the driver runs `open`'s. |
| `opening` | object | What `feature.evals.open` takes as `plan`: the run id and row, the names, the prune, the settings. Never the cases. |
| `run_row` | object |  |
| `prune` | list of integer |  |
| `keys` | list of string |  |
| `launch` | list of object | Only for a driver pinned before its bundle passed the seeds to `open` (SEEDS_TO_OPEN_SINCE): the rows to seed, as that driver's `open` reads them from the plan. Empty otherwise. |
| `by_kind` | map of object | Only for such a driver, likewise: the selection by kind. Empty otherwise; a current driver runs `open`'s. |
| `reseed` | boolean |  |
| `fields` | list of string |  |
| `stamp_columns` | list of string |  |
| `kinds` | list of string |  |
| `default_kind` | string |  |
| `names` | list of string |  |
| `count` | integer |  |
| `turns` | integer |  |
| `reps` | integer |  |
| `seeded` | integer |  |
| `refreshed` | list of string |  |
| `stale` | list of string |  |
| `unfinished` | list of string |  |
| `payload_bytes` | integer | The size of this result on the wire, against the runner's PAYLOAD_BUDGET; the plan refuses over it, naming the count that fits. |
| `summary` | string |  |

### `feature.evals.reconcile`

The run's own pass over its roll-up once every turn is done: the
same merge the turns make, with no turn of its own, so a run with a
lost turn still reads complete.

```yaml
- id: <step>
  activity: feature.evals.reconcile
  args:
    conversation_id: <string>
    run_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `run_id` | string | yes |  |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `recompute_on_stale` | integer | no | Default `5`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `run_id` | string |  |
| `rollup` | object |  |
| `summary` | string |  |

### `feature.evals.rollup`

Fold this turn's result into the run's row in `eval_runs`, under
the revision it read, re-reading on a conflict: the counts, the
rounds, the flaky cases, the handoffs, and the run before it.

```yaml
- id: <step>
  activity: feature.evals.rollup
  args:
    conversation_id: <string>
    case: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `case` | object | yes |  |
| `result` | string | no | Default `""`. |
| `rounds` | integer | no | Default `0`. |
| `reason` | string | no | Default `""`. |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `guidance_rev` | string | no | Default `""`. |
| `recompute_on_stale` | integer | no | Default `5`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `run_id` | string |  |
| `rollup` | object |  |
| `summary` | string |  |

### `feature.evals.score`

A turn's last act: compare `actual` with the row's `Expect`,
fold in the problems the bundle's own scorer found, and write the
verdict twice: to the turn's row in `eval_results` (never
overwritten) and to the case's row on the board (this run's worst).
A turn a newer run overtook is `superseded` and writes only its
history row, `Counted: false`.

```yaml
- id: <step>
  activity: feature.evals.score
  args:
    conversation_id: <string>
    case: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `case` | object | yes |  |
| `ready` | boolean | no | Default `true`. |
| `actual` | object, optional | no | The decision, flat: every key `Expect` may name, plus `rounds` and `body`. Stored as Decision (minus `body`) and Draft. |
| `problems` | list of string | no | What the bundle's own scorer found wrong. |
| `handled_keys` | list of string | no | The `Expect` keys the bundle's scorer compared itself; any other key the runner does not know fails the case. |
| `failures` | list of string | no | Steps that failed softly in the turn; any makes the case an error with them as its Detail. |
| `trace` | object, optional | no |  |
| `reason` | string | no | Why the case's row would land on a person, blank otherwise; what the run's Handoff Reasons count. Default `""`. |
| `extra_columns` | object | no | The bundle's own columns for the board and history rows, e.g. where the decision would land. |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `guidance_rev` | string | no | Default `""`. |
| `started_at` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `result_id` | string |  |
| `rounds` | integer |  |
| `problems` | list of string |  |
| `summary` | string |  |
