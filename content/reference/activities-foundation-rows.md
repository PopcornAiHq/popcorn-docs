---
id: activities-foundation-rows
title: foundation.rows
order: 117
group: Activities
parent: activities-foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.rows activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.rows` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.rows.update`

Apply a list of patches to in-memory rows, matched on a key field.

Each row and each patch must carry `key_field`; a patch updates the row
whose key matches (the key cell itself is never changed). Patches with no
key, or no matching row, are dropped and counted. Returns the full row
list plus `updated_count` / `dropped` — a pure transform, no store I/O.

```yaml
- id: <step>
  activity: foundation.rows.update
  args:
    rows: <array>
    key_field: <string>
    patches: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `rows` | list of object | yes |  |
| `key_field` | string | yes |  |
| `patches` | list of object, optional | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows` | list of object |  |
| `updated_count` | integer |  |
| `dropped` | integer |  |
