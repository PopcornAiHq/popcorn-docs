---
id: activities/catalog/foundation/notifications
title: foundation.notifications
order: 116
group: Activities
parent: activities/catalog/foundation
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-11-25
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.notifications activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.notifications` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.notifications.sync`

*Beta.*

Bring the notification rows for these posts to whom each is on now.

Say how things stand, every time they may have changed: the step
notifies whoever a post is newly on, resolves the row of whoever it
left, rewords a line that changed, and does nothing for a post that
stands as it did. Rows are only created for active human members of
the run's conversation.

```yaml
- id: <step>
  activity: foundation.notifications.sync
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The run's own conversation; any other is refused. |
| `posts` | list of NotificationPost | no | The posts to bring up to date. |

**Returns**

What the step did, summed over its posts. `skipped` counts posts
left alone (not a message of this conversation, or an id that is no
UUID); `stale` those handed with a revision older than the one
already applied. Of the people newly notified, `delivery_started`
counts those whose delivery was started and `delivery_skipped` those
left alone because
their settings let nothing be sent for it.

| Field | Type | Notes |
|---|---|---|
| `notified` | integer |  |
| `resolved` | integer |  |
| `reworded` | integer |  |
| `skipped` | integer |  |
| `stale` | integer |  |
| `delivery_started` | integer |  |
| `delivery_skipped` | integer |  |

`NotificationPerson`:

| Field | Type | Notes |
|---|---|---|
| `user_id` | string | The person's user id. |
| `line` | string | The one short line they read in their notifications. |

`NotificationPost`:

| Field | Type | Notes |
|---|---|---|
| `post_id` | string | The post's message id, in the run's conversation. |
| `rev` | integer, optional | The revision of what `on` was read from (a store row's `_rev`), which only grows. A step handed an older revision than the one last applied to this post leaves it alone, so overlapping runs cannot apply out of order. Omitted: always applied. |
| `section` | `urgent` / `needs_you` | The section its rows sit in. |
| `on` | list of NotificationPerson | Everyone the post is on now. Empty resolves the rows of everyone it was on. |
| `own` | list of string | Those of `on` it is on by their own doing: no notification is created for them. |
