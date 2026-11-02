---
id: activities/catalog/foundation/phone
title: foundation.phone
order: 116
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.phone activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.phone` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.phone.check`

Read one phone answer against libphonenumber and report what was seen,
never the number itself.

`number` is the answer exactly as the person wrote it — punctuation,
surrounding words and an extension included. `region` is a two-letter
country code (`AU`, `GB`), only when their own words named a
country; anything else, or empty, means none was named. A number
written with `+` is read under its own country code; otherwise under
`region`; otherwise under an assumed US plan, reported as
`region_assumed: true`.

Never fails the step: a checker that cannot run returns
`{available: false, reading}`, and an empty `number` returns
`{rejected: true, reading}`. Pure, so it is safe to retry and to run
any number of times.

```yaml
- id: <step>
  activity: foundation.phone.check
  args:
    number: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `number` | string | yes | The phone answer exactly as written. |
| `region` | string | no | Two-letter country code their own words named, or empty. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `check` | object | What was seen, never the number. Normally: available, parsed, valid (allocated under the plan), possible (a length the plan allows), digits, extension_written, country_code_written, country_code ('+44' or null), region (the plan's two-letter code, or null), region_assumed, too_long_for_any_plan, and reading (one sentence saying all of that). {available: false, reading} when the checker could not run; {rejected: true, reading} for an empty number. |
