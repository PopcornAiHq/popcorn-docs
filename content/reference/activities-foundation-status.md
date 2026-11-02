---
id: activities-foundation-status
title: foundation.status
order: 120
group: Activities
parent: activities-foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.status activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.status` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.status.set`

Write a live status-widget update for the conversation UI.

Emits the versioned status envelope (progress bar / spinner / terminal
result) the client renders, keyed by `status:{kind}:{instance_id}`.
`instance_id` defaults to the workflow run id, so every emit in one run
updates the same widget. See docs/agent-store-status-widgets.md.

```yaml
- id: <step>
  activity: foundation.status.set
  args:
    conversation_id: <string>
    kind: <string>
    state: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `kind` | string | yes |  |
| `state` | string | yes |  |
| `instance_id` | string, optional | no |  |
| `pct` | number, optional | no |  |
| `label` | string, optional | no |  |
| `terminal` | boolean | no | Default `false`. |
| `ok` | boolean, optional | no |  |
| `data` | object, optional | no |  |
