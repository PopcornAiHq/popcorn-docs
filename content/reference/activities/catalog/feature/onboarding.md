---
id: activities/catalog/feature/onboarding
title: feature.onboarding
order: 136
group: Activities
parent: activities/catalog/feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.onboarding activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `feature.onboarding` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.onboarding.evaluate`

Evaluate the channel's onboarding signals and latch `setup_fulfilled`
/ `onboarding_complete` the moment they hold. One-way: already-latched
flags are never re-evaluated or rewritten.

```yaml
- id: <step>
  activity: feature.onboarding.evaluate
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `email_connected` | boolean, optional | no |  |
| `required_steps` | list of string | no |  |
| `ready_scalar` | string, optional | no |  |
| `fully_live` | boolean, optional | no |  |
| `client_owned_setup` | boolean | no | Let the client's Continue action own setup_fulfilled. Only latch the fully-live safety net here. Exclusive with required_steps and ready_scalar. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `setup_fulfilled` | boolean | The latch's value after this pass. |
| `onboarding_complete` | boolean | The latch's value after this pass. |
| `user_steps_done` | boolean | Whether the user-steps gate held this pass (independent of whether anything newly latched). |

### `feature.onboarding.mark_step`

Mark one onboarding checklist step done in the `onboarding_state`
envelope the Today view reads. Deep-merges, so other steps' entries are
preserved.

```yaml
- id: <step>
  activity: feature.onboarding.mark_step
  args:
    conversation_id: <string>
    step_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `step_id` | string | yes | The strings.yaml today.onboarding_steps id of the finished step, e.g. upload_questions. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `step_id` | string | The step just marked done. |
| `steps` | map of string | The post-merge steps map (every step's state so far). |
