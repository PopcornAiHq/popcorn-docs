---
id: activities/catalog/foundation/math
title: foundation.math
order: 113
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.math activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.math` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.math.calculate`

*Beta.*

One binary scalar operation — `left <operation> right` — with an
optional clamp.

`operation` is one of `add | subtract | multiply | divide`.
The numeric arguments accept numeric strings (`"5"` works, so a
stored scalar feeds in directly); booleans are rejected.
`minimum` / `maximum`, when given, clamp the result into
`[minimum, maximum]`. Integer inputs stay integers for
add/subtract/multiply — unless a clamp bound binds, in which case
`value` is the bound exactly as given (`minimum: 5.0` yields
`5.0` and a `value_str` of `"5.0"`). Divide always returns a
number with a fractional part allowed. Division by zero, non-finite
numbers, `minimum > maximum`, and integer results too large to
serialize (beyond ~4300 digits) fail the step (non-retryably).

Returns `raw_value` (unclamped), `value` (clamped — the field to
use downstream), `clamped` (whether a bound changed the value),
and `value_str` (`value` as text, for `store.set_scalar`).

```yaml
- id: <step>
  activity: foundation.math.calculate
  args:
    left: <number>
    operation: <string>
    right: <number>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `left` | number | yes |  |
| `operation` | `add` / `subtract` / `multiply` / `divide` | yes |  |
| `right` | number | yes |  |
| `minimum` | number, optional | no |  |
| `maximum` | number, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `raw_value` | integer or number |  |
| `value` | integer or number |  |
| `clamped` | boolean |  |
| `value_str` | string |  |

### `foundation.math.elapsed`

*Beta.*

Signed duration between two timestamps: end minus start.

`start_iso` and `end_iso` each accept `Z`, explicit-offset,
naive (read as UTC), and date-only (midnight UTC) timestamps — the
same parsing policy as `math.offset` — and each may be
omitted/null to mean the current wall-clock time (so "age of X" is
just `start_iso: <X>`).

Returns `{seconds, minutes, hours, days}`. Each field is the WHOLE
duration expressed in that unit, unrounded and signed (negative when
`end_iso` is before `start_iso`); `days` is 24-hour days, not
calendar days.

```yaml
- id: <step>
  activity: foundation.math.elapsed
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `start_iso` | string, optional | no |  |
| `end_iso` | string, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `seconds` | number |  |
| `minutes` | number |  |
| `hours` | number |  |
| `days` | number |  |

### `foundation.math.offset`

Shift a timestamp by a duration and return the result.

Give `iso` to shift a specific timestamp, or omit it to shift from
the current wall-clock time. `direction` is `"add"` (default) or
`"subtract"`; the duration fields are non-negative and additive —
"six hours ago" is `direction: subtract, hours: 6`; a duration
given as a numeric string (`"6"`, e.g. a stored scalar) is
accepted, booleans and fractions are not. Accepts `Z`,
explicit-offset, naive (read as UTC), and date-only timestamps —
`2026-08-10` parses as MIDNIGHT UTC, so a `$lt` filter on it
excludes that whole day. The output `iso` is normalized UTC
ISO-8601, always the `+00:00` spelling (never `Z`).

Returns the same `{unix, unix_str, iso}` shape as `workflow.now`,
so the result drops straight into a `list_rows` filter
(`{"Last Seen": {"$lt": $steps.cutoff.output.iso}}`) or
`store.set_scalar`.

```yaml
- id: <step>
  activity: foundation.math.offset
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `iso` | string, optional | no |  |
| `direction` | `add` / `subtract` | no | Default `"add"`. |
| `days` | integer | no | Default `0`. |
| `hours` | integer | no | Default `0`. |
| `minutes` | integer | no | Default `0`. |
| `seconds` | integer | no | Default `0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `unix` | integer |  |
| `unix_str` | string |  |
| `iso` | string |  |
