---
id: activities/catalog/foundation/channels
title: foundation.channels
order: 106
group: Activities
parent: activities/catalog/foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.channels activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.channels` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.channels.app`

Describe the app this channel runs: version, line, head, files.

Read-only. Names only this run's channel, so it takes no channel id.

```yaml
- id: <step>
  activity: foundation.channels.app
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `include_text` | list of string | no | Exact paths whose text to return as well, e.g. ['AGENT.md', 'manifest.yaml']. Up to 20. |
| `max_text_bytes` | integer | no | Total UTF-8 bytes of text to return across include_text, in the order given; a file that would pass it is skipped, not cut. Default `65536`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `app` | string | The app (registry identity). |
| `semver` | string | The version the channel serves now. |
| `version_id` | integer | Its bundle_version id. |
| `line` | string | 'product' for Popcorn's product line, else the fork line's name. |
| `on_fork_line` | boolean | True when `line` is a fork. |
| `head_semver` | string | The newest version on the line. |
| `head_version_id` | integer | Its bundle_version id. |
| `files` | list of string | Every path in the served version. |
| `changelog` | string | The served version's changelog, as its publish recorded it: what a flow checks to tell its own publish from anyone else's. |
| `published_by` | string | Who published the served version (a user id); blank for a product version Popcorn published. |
| `published_at` | string | When it was published (ISO-8601). |
| `texts` | map of string | path → text, for include_text. |
| `texts_skipped` | list of string | include_text paths not returned: missing, binary, or past max_text_bytes. |

### `foundation.channels.get`

Look up channels by id and return their name and type.

Answers for the channels the bot this flow runs as may read: the flow's
own channel, any public / workspace / shared channel in the workspace,
and any channel the bot is a member of. Any other id, including a
private channel the bot is not in or someone else's DM, comes back with
`found: false`, exactly like an id that does not exist. Read-only: safe
to retry.

```yaml
- id: <step>
  activity: foundation.channels.get
  args:
    channel_ids: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_ids` | list of string | yes | Up to 100 channel ids (UUIDs), e.g. a search step's `channel_ids`. Empty strings are ignored; duplicates collapse. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `channels` | list of ChannelLabel | One entry per distinct requested id, in request order, including the ones that did not resolve. |
| `requested` | integer | Distinct non-empty ids asked for. |
| `found` | integer | How many entries have found=true. |

`ChannelLabel`:

| Field | Type | Notes |
|---|---|---|
| `channel_id` | string | The requested id (echoed). |
| `found` | boolean | False when the id is unknown, deleted, not a UUID, or a channel the bot may not read. The other fields are then null. |
| `name` | string, optional | The channel's name, as shown after `#`. Null for a DM, group DM or self-DM, which have no name of their own; none is made up from the participants. |
| `type` | string, optional | workspace_channel, public_channel, private_channel, shared_channel, shared_private_channel, dm, group_dm or self_dm. |

### `foundation.channels.list`

List the workspace's open channels, most recently active first.

Only `workspace_channel`, `public_channel` and `shared_channel` can be
listed; a private channel, a DM or a group DM cannot be asked for and is
never returned. Archived channels are never listed. The order is the
newest top-level message first (channels with none last), so a capped
listing keeps the active ones. Read-only: safe to retry.

```yaml
- id: <step>
  activity: foundation.channels.list
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `types` | list of `workspace_channel` / `public_channel` / `shared_channel` | no | Which open channel types to list: workspace_channel, public_channel, shared_channel (a public channel that people from outside the workspace are in). Default the first two. No other type is accepted. |
| `limit` | integer | no | Most channels returned, 1-1000 (default 200). `has_more` says when there were more. Default `200`. |
| `cursor` | string, optional | no | A previous step's `next_cursor`, to continue a listing that came back with `has_more`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `channels` | list of ListedChannel | The channels, newest top-level message first. |
| `count` | integer | len(channels). |
| `has_more` | boolean | True when the listing holds more than `limit`. |
| `next_cursor` | string, optional | Pass as `cursor` to continue; null on the last page. |

`ListedChannel`:

| Field | Type | Notes |
|---|---|---|
| `channel_id` | string | The channel's id (UUID). |
| `name` | string, optional | The channel's name, as shown after `#`. |
| `type` | string | workspace_channel, public_channel or shared_channel. |
| `last_message_at` | string, optional | ISO-8601 time of the newest TOP-LEVEL message; null when the channel has none. A thread reply does not move it. |
| `participant_count` | integer | How many members the channel has. |
| `is_self` | boolean | True for the channel this flow is running in. |
