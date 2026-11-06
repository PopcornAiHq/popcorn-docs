---
id: activities/catalog/foundation/money
title: foundation.money
order: 115
group: Activities
parent: activities/catalog/foundation
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.money activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.money` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.money.usd`

Add the US-dollar figure to each `answers[].money` in a validator
reading. `validation` is the reading exactly as the validator
submitted it; anything else is returned unchanged. Never fails: an
amount with no rate to be had gets `usd: null` and
`usd_unavailable` (`no_rate` or `lookup_failed`).

```yaml
- id: <step>
  activity: foundation.money.usd
  args:
    validation: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `validation` | object | yes | The validator's submitted reading. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `validation` | any | The same reading, each answer's `money` carrying `usd`: {figure, figure_high, rate, rate_date, source}, or null where no rate could be had, with `usd_unavailable` saying why: `no_rate` (the currency is not published) or `lookup_failed`. |
