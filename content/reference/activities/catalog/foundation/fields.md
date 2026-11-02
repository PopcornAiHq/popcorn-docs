---
id: activities/catalog/foundation/fields
title: foundation.fields
order: 111
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.fields activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.fields` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.fields.extract`

*Beta.*

Extract declared fields from an object by path, without an LLM.

`mapping` names each output field and where it comes from:
`{"alarm": "AlarmName", "env": "Trigger.Dimensions.0.value"}`. Paths use
DOTS for both nesting and list indices, matching the DSL's own reference
convention — never brackets.

A path that does not resolve is an ERROR, not an empty value; supply
`defaults` for the fields that are genuinely optional. That asymmetry is
the point: it is what lets a flow require a field to be present instead of
silently accepting a fabricated one.

`output_schema` declares the resulting shape so the fields are
referenceable as `$steps.<id>.output.<name>`.

```yaml
- id: <step>
  activity: foundation.fields.extract
  args:
    data: <object>
    mapping: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `data` | object | yes |  |
| `mapping` | map of string | yes |  |
| `output_schema` | object, optional | no |  |
| `defaults` | object | no | Default `{}`. |
