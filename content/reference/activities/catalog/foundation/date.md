---
id: activities/catalog/foundation/date
title: foundation.date
order: 110
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.date activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.date` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.date.add`

*Beta.*

A date plus or minus a number of calendar or business days, with a
result that lands on a weekend (or a listed holiday) optionally rolled
to the nearest business day.

`date` is the start: `YYYY-MM-DD`, or a timestamp, which is read
as the calendar date it falls on in `timezone`. Omit it for today in
`timezone`. `days` is a non-negative whole number; `direction`
is `add` (the default) or `subtract`. `unit` is `calendar`
(every day counts) or `business` (only weekdays not in `holidays`
count, and the start day itself never does). `roll` is `none` (the
default), `forward` (a result on a non-business day moves to the
next business day) or `back` (to the previous one). `holidays` is
an optional list of `YYYY-MM-DD` dates treated as non-business days;
nothing is assumed about public holidays otherwise.

Pure and deterministic for a given start; safe to retry.

```yaml
- id: <step>
  activity: foundation.date.add
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `date` | string, optional | no | The start: YYYY-MM-DD, or a timestamp read in `timezone`. Omit for today. |
| `days` | integer | no | How many days to move; non-negative. Default `0`. |
| `unit` | `calendar` / `business` | no | calendar (every day) or business (weekdays not in holidays). Default `"calendar"`. |
| `direction` | `add` / `subtract` | no | add (later) or subtract (earlier). Default `"add"`. |
| `roll` | `none` / `forward` / `back` | no | What to do with a result on a non-business day: none, forward or back. Default `"none"`. |
| `timezone` | string | no | IANA zone the dates are read and written in; UTC by default. Default `"UTC"`. |
| `holidays` | list of string | no | Dates (YYYY-MM-DD) that are not business days, beyond weekends. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `date` | string | The resulting date, YYYY-MM-DD. |
| `iso` | string | The first instant of that date in `timezone`, RFC3339 with its offset: midnight, or the first time that exists on a day the zone's clock jumps forward at midnight. What a datetime column or a comparison takes. |
| `weekday` | string | The result's weekday name, Monday to Sunday. |
| `business_day` | boolean | Whether the result is a weekday not in `holidays`. |
| `rolled` | boolean | Whether `roll` moved the result off a non-business day. |
| `start` | string | The start date as read, YYYY-MM-DD. |
