---
id: activities/catalog/feature/sms
title: feature.sms
order: 141
group: Activities
parent: activities/catalog/feature
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.sms activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.sms` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.sms.send`

*Beta.*

Send an SMS to a workspace contact. The text goes out from the
workspace's own phone number; opted-out contacts are rejected.

```yaml
- id: <step>
  activity: feature.sms.send
  args:
    contact_id: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `contact_id` | string | yes | Workspace contact id (from the contacts book). |
| `body` | string | yes | Message text (1600 chars max). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `message_id` | string | sms_messages row id of the send. |
| `to_phone` | string | Resolved contact number (E.164). |
| `status` | string | Provider status (queued / sent); pending when this retry found the original attempt still in flight. |
| `duplicate` | boolean | True when this was an activity retry of an already-sent message (idempotency hit) — nothing was re-sent. |
