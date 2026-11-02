---
id: activities-feature-chase
title: feature.chase
order: 125
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.chase activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.chase` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.chase.agent_apply`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_apply
  args:
    conversation_id: <string>
    record_id: <integer>
    expected_revision: <integer>
    fingerprint: <string>
    turn_key: <string>
    plan: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |
| `expected_revision` | integer | yes |  |
| `fingerprint` | string | yes |  |
| `turn_key` | string | yes |  |
| `plan` | object | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `sent` | boolean |  |

### `feature.chase.agent_deliver`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_deliver
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `sent` | boolean |  |

### `feature.chase.agent_due`

`agent_prepare`'s arguments for every lead of a tick: the policy,
columns and guidance `claim_turn` hands prepare, over `record_ids`.
They must be the same arguments, or the fingerprint differs and every
lead launches (the bundle's tests hold the two steps together).

```yaml
- id: <step>
  activity: feature.chase.agent_due
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | no | Default `0`. |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |
| `record_ids` | list of integer | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `record_ids` | list of integer |  |
| `candidates` | integer |  |
| `launched` | integer |  |
| `skipped` | map of integer |  |
| `uncertain` | integer |  |
| `seeded` | integer |  |

### `feature.chase.agent_ingest`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_ingest
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `record_ids` | list of integer |  |
| `ingested` | integer |  |
| `skipped_other_channel` | integer |  |

### `feature.chase.agent_prepare`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_prepare
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ready` | boolean |  |
| `needs_agent` | boolean |  |
| `context` | object |  |
| `plan` | object |  |
| `expected_revision` | integer |  |
| `fingerprint` | string |  |
| `turn_key` | string |  |
| `channel_notes` | map of string |  |
| `bundle_guidance` | map of string |  |
| `guidance_rev` | string |  |

### `feature.chase.agent_timed_out`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_timed_out
  args:
    conversation_id: <string>
    record_id: <integer>
    error: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `turn_key` | string | no | Default `""`. |
| `error` | object | yes |  |
| `agent_steps` | list of string | no |  |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `timeouts` | integer |  |
