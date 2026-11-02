---
id: activities-foundation-search
title: foundation.search
order: 119
group: Activities
parent: activities-foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.search activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.search` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.search.messages`

*Beta.*

Search the workspace's messages and return the hits as records.

One call to the search index, filtered to what the running bot may
read. Combine any of the filters; `query` may be empty when another
filter carries the question (e.g. `mentions_user_id` + `after`). At
least one filter is required. Read-only: safe to retry.

**What you can find.** Hits in your own channel, in any public /
workspace / shared channel, and in any channel the bot is a member of.
Hits in other private channels and in DMs are dropped by the API, so a
page can be shorter than `limit` with `has_more` still true. There is
no way to search as a person; the bot's view is the only one.

**Records.** Each hit is the same shape `foundation.channel.history`
returns, plus `mentioned_user_ids` so a flow can see who a message was
addressed to without re-reading it. `conversation_name` and
`conversation_type` say where each hit was found ("in #ops"); the name
is null for a DM, group DM or self-DM, which have no name of their own.

```yaml
- id: <step>
  activity: foundation.search.messages
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `query` | string | no | Words to match in message text. Empty means 'no text match', i.e. filter only. Default `""`. |
| `channel_ids` | list of string, optional | no | Restrict to these channels (UUIDs, up to 50). Omit to search every channel the bot may read. |
| `from_user_id` | string, optional | no | Only messages this user (UUID) wrote. |
| `mentions_user_id` | string, optional | no | Only messages that @mention this user (UUID). The mention has to be a real @mention; a message that merely says the person's name does not match. Combine with `query` for that. |
| `has` | list of `file` / `images` / `link` / `mention` / `video`, optional | no | Only messages carrying at least ONE of these: file, images, link, mention (any @mention), video. Several values widen the match (OR), they do not narrow it. |
| `after` | string, optional | no | Only messages sent at or after this ISO-8601 instant (what `foundation.math.offset` emits). `Z`, an offset, a naive timestamp (read as UTC) and a bare date (midnight UTC) all parse. |
| `before` | string, optional | no | Only messages sent before this ISO-8601 instant. |
| `humans_only` | boolean | no | Leave out messages a bot, agent or app wrote (the records `is_bot` would mark true). Applied by the search itself, before `sort` and `limit`: bot messages never take a place on the page, so `limit` human messages come back when that many match (less any the access check hides). On its own it is not a filter: pair it with at least one of the others. Default `false`. |
| `open_channels_only` | boolean | no | Keep only hits in open channels (workspace, public, shared). Leaves out DMs, group DMs, self-DMs and private channels — even ones the bot is a member of, and the run's own channel if it is private — before the page comes back. Use it when reading a member's messages for anything shown beyond the channel they were said in. Applied after paging: pages can come back short with `has_more` true. On its own it is not a filter. Default `false`. |
| `sort` | `relevance` / `date_desc` / `date_asc`, optional | no | relevance / date_desc / date_asc. Default: relevance when `query` is set, date_desc (newest first) otherwise. |
| `limit` | integer | no | Page size, 1–100. Default `50`. |
| `offset` | integer | no | Skip this many hits: pass back `next_offset` to read the following page. Default `0`. |
| `include_parts` | boolean | no | Also return each message's raw content parts. Default `false`. |
| `include_metadata` | boolean | no | Include each message's stored metadata (a webhook message's classification lives there). Set false to drop it. Default `true`. |

**Returns**

What `foundation.search.messages` puts in `$steps.<id>.output`.

| Field | Type | Notes |
|---|---|---|
| `messages` | list of ChannelMessageRecord | The hits, in the requested `sort` order. The same record shape as foundation.channel.history; `conversation_id`, `conversation_name` and `conversation_type` on each say which channel it was found in. |
| `count` | integer | len(messages). |
| `has_more` | boolean | True when the index had a full page of hits behind this one, or when this page was trimmed to the output budget: pass `next_offset` as `offset` to read on. Judged on the RAW page, so a page thinned — even to nothing — by hits the bot may not read still says true while more index pages exist. |
| `next_offset` | integer | `offset` + the page size the index was asked for: the `offset` for the next page. |
| `truncated` | boolean | True when the page's tail was dropped to fit the 1 MiB output budget. The dropped hits are NOT at `next_offset`; a flow that must see every hit re-reads this `offset` with a smaller `limit`, or with `include_parts: false` / `include_metadata: false`. |
| `channel_ids` | list of string | Distinct channels the hits came from, in first-seen order — the set to re-read with channel.history for context. |

`ChannelAttachment`:

| Field | Type | Notes |
|---|---|---|
| `filename` | string | The attachment's filename. |
| `mime_type` | string | Its MIME type, e.g. application/pdf. |
| `file_key` | string | The file_uploads key, scoped to the channel the message is in. When that is the flow's own channel, pass it to the foundation.file steps to read the file or to channel.post_file's `conversation_file_key` to re-attach it. A key from a CROSS-CHANNEL read is an identifier only: the file steps read the run's own conversation and nothing else, and post_file can re-attach a key only when posting back into the channel it came from. |

`ChannelMessageRecord`:

| Field | Type | Notes |
|---|---|---|
| `id` | string | The message UUID (usable as a thread root, or as a `latest`/`oldest` cursor). |
| `conversation_id` | string | UUID of the channel the message is in. |
| `conversation_name` | string, optional | That channel's name, as shown after `#`, so a flow can say 'in #ops' without a second lookup. Null for a DM, group DM or self-DM: those have no name of their own, and none is made up from the participants. Never set for a channel the bot may not read. |
| `conversation_type` | string, optional | That channel's type: workspace_channel, public_channel, private_channel, shared_channel, shared_private_channel, dm, group_dm or self_dm. Set whenever `conversation_name` could have been; null (with a null name) in the rare case the lookup did not answer. |
| `author_id` | string | User UUID of the sender. |
| `author_name` | string, optional | The sender's display name, else their username; null if the author record could not be resolved. |
| `is_bot` | boolean | True when the sender is a bot account. |
| `is_self` | boolean | True when the sender is the bot this flow runs as — how a flow asks 'have I already replied to this?'. |
| `text` | string | All text parts of the message joined with blank lines. Empty for a message that is only an attachment or a tool call. |
| `created_at` | string | ISO-8601 UTC send time. |
| `edited_at` | string, optional | ISO-8601 UTC time of the last edit, or null. |
| `thread_id` | string, optional | Root message id when this message is a thread reply, else null. Top-level messages in a history read always have null; read a thread's replies by passing its root as `thread_id`. |
| `thread_message_count` | integer | Number of replies under this message. >0 means a history read is not showing the discussion — re-read with `thread_id` set. |
| `attachments` | list of ChannelAttachment | Files attached to the message. |
| `mentioned_user_ids` | list of string | User UUIDs the message @mentions, in message order. Empty when nobody was mentioned by handle. |
| `mentioned_everyone` | boolean | True when the message used @everyone or @here. |
| `reactions` | map of list of string | Emoji reactions on the message: each emoji to the user UUIDs who reacted with it. Empty when nobody reacted. |
| `parts` | list of object, optional | The raw content parts, only when `include_parts` was true; null otherwise. Needed for tool calls, link previews and media metadata that the flattened fields drop. |
| `metadata` | object, optional | Whatever was stored on the message, passed through unchanged, or null when the message carries nothing (a person typing). A webhook-posted message holds `classification.identifying_attributes` (the facts Popcorn's classifier pulled out of the payload), `classification.matched_thread` (the incident it decided this continues) and `webhook.name` (which webhook posted it, when two share a channel). The classifier is a model, so attribute KEYS drift — the same fact arrives as `alert_name` or `alertname` — and a consumer should coalesce rather than expect one spelling. Nothing here is re-derived or renamed on the way out. Set `include_metadata: false` to drop it. |
