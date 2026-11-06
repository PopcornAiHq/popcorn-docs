---
id: activities/catalog/foundation/testing
title: foundation.testing
order: 122
group: Activities
parent: activities/catalog/foundation
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.testing activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.testing` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.testing.assert_column_values`

Check a table's rows against the values its columns declare.

`columns` defaults to every column of `table_name` whose manifest
`display` hint is `status:…` — the ones a client renders as chips,
which is exactly the set with a closed vocabulary. `allowed` maps a
column to the values it may hold and both adds unhinted columns and
overrides hinted ones. Blank (`""` or null) passes unless
`allow_blank` is false: a Decision is blank until taken.

```yaml
- id: <step>
  activity: foundation.testing.assert_column_values
  args:
    table_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `table_name` | string | yes | Store table to read. |
| `columns` | list of string | no | Columns to check; default every column with a `status:` display hint in the pinned manifest. |
| `allowed` | map of list of string | no | Explicit allowed values per column; adds a column the manifest does not hint, or overrides one it does. |
| `allow_blank` | boolean | no | Whether '' / null passes in every column. Default `true`. |
| `page_limit` | integer | no | Store page size; every page is read. Default `1000`. |
| `fail_step` | boolean | no | Raise ColumnValuesOutsideVocabulary on any offender instead of returning ok: false. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `table_name` | string |  |
| `rows` | integer | Rows read and checked. |
| `columns` | map of list of string | The vocabulary each checked column was held to. |
| `offenders` | list of Offender | Up to 200 rows outside it, by record id, column and value. |
| `offender_count` | integer |  |
| `summary` | string |  |

`Offender`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer, optional |  |
| `column` | string |  |
| `value` | any |  |
