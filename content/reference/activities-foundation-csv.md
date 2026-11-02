---
id: activities-foundation-csv
title: foundation.csv
order: 109
group: Activities
parent: activities-foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.csv activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `foundation.csv` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.csv.parse`

Parse CSV into row objects.

By default `data` is base64-encoded bytes (decoded with `encoding`); set
`is_base64: false` to pass plain CSV text directly (e.g. a pasted
spreadsheet export). Parses the result as `delimiter`-separated text,
returning `rows` (one dict per record, keyed by the header) and the
`header` column list.

```yaml
- id: <step>
  activity: foundation.csv.parse
  args:
    data: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `data` | string | yes |  |
| `delimiter` | string | no | Default `","`. |
| `encoding` | string | no | Default `"utf-8"`. |
| `is_base64` | boolean | no | Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows` | list of object |  |
| `header` | list of string |  |

### `foundation.csv.serialize`

Serialize row objects into base64-encoded CSV bytes.

Writes `rows` as `delimiter`-separated text and returns it
base64-encoded in `data`. Columns come from `header` when given, else
from the first row's keys; cells absent from a row are written blank.

```yaml
- id: <step>
  activity: foundation.csv.serialize
  args:
    rows: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `rows` | list of object | yes |  |
| `header` | list of string, optional | no |  |
| `delimiter` | string | no | Default `","`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `data` | string |  |
| `row_count` | integer |  |
