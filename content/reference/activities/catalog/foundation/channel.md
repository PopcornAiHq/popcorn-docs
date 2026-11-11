---
id: activities/catalog/foundation/channel
title: foundation.channel
order: 105
group: Activities
parent: activities/catalog/foundation
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-11-11
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.channel activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.channel` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.channel.create`

Create a workspace channel with `template` installed and wait for
the install to finish.

```yaml
- id: <step>
  activity: foundation.channel.create
  args:
    name: <string>
    template: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | The new channel's name (spaces become hyphens). A name already taken fails the step rather than reusing that channel. |
| `template` | string | yes | The channel template to install, e.g. 'chase'. |
| `description` | string | no | Default `""`. |
| `install_timeout_seconds` | integer | no | Default `300`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `conversation_id` | string |  |
| `name` | string |  |
| `url` | string |  |
| `app` | string |  |
| `semver` | string |  |

### `foundation.channel.edit`

Edit an existing channel message in place (live progress updates).

Full content replacement: the new `text` (and any attachments) becomes
the message's entire content — any previous attachment is dropped. Same
attachment capability as `channel.post_file`: omit the file fields for a
text-only edit, or (re)attach files via an inline `content` upload
(`content`/`filename`, plus `binary=true` for images) and/or existing
`conversation_file_key` references. `format` is replaced along with
everything else, so a flow editing a markdown message must repeat
`format: markdown` on the edit.

```yaml
- id: <step>
  activity: foundation.channel.edit
  args:
    channel_id: <string>
    message_id: <string>
    text: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | string | yes | UUID of the channel / conversation the message is in. |
| `message_id` | string | yes | UUID of the message to overwrite (from channel.post). |
| `text` | string | yes | New message body. Plain text unless `format: markdown` is set. |
| `format` | `plain` / `markdown` | no | How the client renders `text`: "plain" (default) or "markdown". Not inherited from the message being edited — an edit of a markdown message must set this again or the text renders as literal markup. Default `"plain"`. |
| `finalize` | boolean | no | When true, mark the message as a finished agent turn (appends the done marker). Leave false for intermediate progress edits. Default `false`. |
| `content` | string, optional | no | Optional attachment file content. Plain text by default; when `binary=true`, base64-encoded bytes (e.g. a generated image). Omit for a text-only edit. Full replacement: omitting it drops any existing attachment. |
| `binary` | boolean | no | When true, `content` is base64-decoded and stored as binary (e.g. images) instead of UTF-8 text. Set `mime_type` to the real type (e.g. image/jpeg, image/png) so the client renders it. Default `false`. |
| `filename` | string, optional | no | Attachment filename (required when `content` is set), e.g. 'chart.png'. |
| `mime_type` | string | no | MIME type of the attachment. Defaults to text/plain; binary posts MUST set the real type (e.g. image/jpeg, image/png). Default `"text/plain"`. |
| `conversation_file_key` | list of string | no | File keys of existing conversation files to attach (e.g. images uploaded by a prior step). Each becomes its own attachment, in order; combine with `content` to also upload a new one. Full replacement: keys omitted from this edit are dropped. |
| `media_metadata` | object | no | Free-form metadata stored on the inline `content` attachment's media part for special client rendering (see channel.post_file). |

### `foundation.channel.history`

*Beta.*

Read a Popcorn channel's messages into the flow.

The read side of `channel.post`. Identity is NOT in this input: the read
happens as the bot the workflow runs as (`auth.agent_user_id`) in its
workspace (`auth.workspace_id`), so a flow chooses which channel, never
as whom. The API decides what that bot may see.

**What you can read.** Your own channel (omit `channel_id`) whatever its
type, and any public / workspace / shared channel in the same workspace.
Another channel that is private — including a DM between two people — is
refused by the API with a 403, and the step fails. That is deliberate.

**Threads.** A plain history read returns TOP-LEVEL messages only; thread
replies are excluded. `thread_message_count` on a record tells you a
discussion is hiding under it — re-read with `thread_id` set to that
message's id to get the replies. A thread read is in this flow's own
channel only; to read ANOTHER open channel's replies, set
`include_replies: true` on its history read.

**Windows.** `after` / `before` take an ISO-8601 instant, so "the last 24
hours" is one step (`foundation.math.offset` with `direction: subtract,
hours: 24` produces the `iso` to pass) instead of a chain of id cursors
or a last-seen id kept in a scalar. A time-bounded read defaults `limit`
to the maximum, reads FORWARD from the window's start, and reports
`has_more` against the WINDOW.

**Classification.** Each record carries the message's stored `metadata`,
which for a webhook-posted message is where the classifier's
`identifying_attributes` live. Pass `include_metadata: false` to drop it.

**Channel name.** Each record carries `conversation_name` and
`conversation_type`, so a flow can say "in #ops" without another step.
The name is null when the channel is a DM, group DM or self-DM, which
have no name of their own.

Fails loudly rather than quietly: a refused or missing channel raises,
it does not come back as an empty list.

```yaml
- id: <step>
  activity: foundation.channel.history
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | string, optional | no | UUID of the channel to read. OMIT (default) to read the channel this flow is running in — the normal case. Pass an explicit id to read a different channel, which works for a public / workspace / shared channel in the same workspace; another channel's private conversations and DMs are refused. Cannot be combined with `thread_id` (a thread read is always in this flow's own channel). |
| `thread_id` | string, optional | no | Root message id of a thread. When set, the step returns that thread's REPLIES (oldest first, the root itself excluded) instead of the channel's top-level messages. Pass $trigger.thread_id to read the thread the flow was triggered in. Page with `offset`, not `latest`/`oldest`. |
| `limit` | integer | no | How many messages to return, 1-200 (default 50, or 200 when `after`/`before` is set and this is left unset — a time-bounded read chose a window, not a page size). A plain read returns the NEWEST `limit` messages; with `oldest` or `after` set it returns the `limit` messages that follow that cursor. Default `50`. |
| `latest` | string, optional | no | Read messages posted BEFORE this message id — the backwards-paging cursor. Pass a previous read's `oldest_message_id` to get the page before it. |
| `oldest` | string, optional | no | Read messages posted AFTER this message id — the catch-up cursor. Pass a previous read's `newest_message_id` to get just what has been said since. Combine with `latest` for a window. |
| `after` | string, optional | no | Read messages posted AFTER this ISO-8601 instant — `oldest` for a flow that has a time rather than a message id, which is what a scheduled report has. Feed it `foundation.math.offset`'s `iso` (`direction: subtract, hours: 24`) to read the last day in ONE step. Like `oldest` it reads FORWARD: you get the OLDEST `limit` messages in the window, not the newest, and `has_more` then means the window holds more. Accepts `Z`, an explicit offset, a naive timestamp (read as UTC) or a date (midnight UTC). Cannot be combined with `oldest`, which bounds the same end. |
| `before` | string, optional | no | Read messages posted BEFORE this ISO-8601 instant — `latest` by time rather than by message id. Pair with `after` for a closed window ('the hour that just closed'), or with `oldest` to page through a window the first read could not fit. Cannot be combined with `latest`, which bounds the same end. |
| `offset` | integer | no | Thread reads only: how many replies to skip. The next page is `offset` + the `count` you got back. Default `0`. |
| `include_replies` | boolean | no | Return thread replies too, interleaved with the top-level messages by send time. Each reply carries its root as `thread_id` and counts against `limit` like any message, so the window and `has_more` cover replies as well. Only for a public / workspace / shared channel: on a private channel or a DM, this flow's own included, the read is refused (403) and the step fails; read your own channel's threads with `thread_id`. Cannot be combined with `thread_id`. Default `false`. |
| `include_parts` | boolean | no | Include each message's raw content parts as `parts`. Off by default because tool-call and tool-result parts are far larger than the text and most flows only want `text`. Default `false`. |
| `include_metadata` | boolean | no | Include each message's stored `metadata`. ON by default — it is where a webhook message's classification lives, and it is small. Turn it OFF for a channel whose messages carry bulk the flow does not read: every byte returned is copied into workflow history. Default `true`. |

**Returns**

What `foundation.channel.history` puts in `$steps.<id>.output`.

| Field | Type | Notes |
|---|---|---|
| `messages` | list of ChannelMessageRecord | The messages, OLDEST FIRST — ready to paste into a prompt in reading order. |
| `count` | integer | len(messages). |
| `has_more` | boolean | True when more messages exist than this read returned (the page was full, or the size budget truncated it). Scoped to what the read ASKED for: with `after`/`before` set that means more messages inside the WINDOW, not merely elsewhere in the channel — so a windowed read can tell 'my window overflowed the page' from 'the channel is older than my window'. |
| `oldest_message_id` | string, optional | Id of the first message returned; pass it back as `latest` to read the page before this one. Null when empty. |
| `newest_message_id` | string, optional | Id of the last message returned; pass it back as `oldest` to read anything posted since. Null when empty. |
| `oldest_created_at` | string, optional | ISO-8601 send time of the first message returned; null when empty. |
| `newest_created_at` | string, optional | ISO-8601 send time of the last message returned; null when empty. The timestamp edge of this page, which a list index cannot reach — record it as a next run's floor. To continue the CURRENT window use `oldest: newest_message_id` instead: the id cursor cannot re-read or skip a message that shares a timestamp with its neighbour. |

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

### `foundation.channel.post`

Post a plain-text message to a Popcorn channel from a flow step.

Identity is NOT in this input — both workspace and posting bot are
sourced from the auth context. The flow only chooses `channel_id`
(where) and `text` (what). This keeps flow YAMLs out of the
business of knowing bot user ids and makes it impossible to post
as a different bot than the one that triggered the workflow.

```yaml
- id: <step>
  activity: foundation.channel.post
  args:
    channel_id: <string>
    text: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | string | yes | UUID of the channel / conversation to post into. Must belong to the same workspace as the running flow. |
| `text` | string | yes | Message body. Plain text unless `format: markdown` is set, in which case the client renders it as markdown. |
| `format` | `plain` / `markdown` | no | How the client renders `text`: "plain" (default) or "markdown" for a message written with markdown markup (bold, italics, lists). Default `"plain"`. |
| `finalize` | boolean | no | When true (default) the message is posted as a finished agent turn. Set false to post a live, still-updating message that a later channel.edit step will keep refreshing and finalize. Default `true`. |
| `thread_id` | string, optional | no | Root message id to reply under. OMIT (default) to auto-reply in the thread the flow was triggered from — the normal case. Pass a message id to thread elsewhere, or "none" to force a top-level post. Runs with no chat trigger (scheduled / webhook) always post top-level. Threads are flat: pass the thread root, not an intermediate reply. |
| `mention_user_ids` | list of string, optional | no | User ids to @mention, at most 20. Each one is mentioned exactly as a person typing their @name would: the message opens with `@username` (unless the text already carries it) and they are notified. Each id must be a person in this workspace who can see the channel: anyone in the workspace for a public, workspace or shared channel, a channel member otherwise. Any other id, a bot's included, fails the step and nothing is posted. When set, only these ids are mentioned: an `@name` written in `text` is not looked up as well. OMIT (default) or pass an empty list for the usual post, where an `@username` in the text mentions that person if they are a channel member. A later channel.edit replaces the text, so it drops the added names. |

### `foundation.channel.post_file`

Post an agent message with one or more files attached.

Uploads / references files in the `file_uploads` system scoped to
`channel_id`, then posts a message with a `text` part (`text`) plus a
`media` attachment part per file. Identity (workspace + posting bot)
comes from the auth context, same as `channel.post`.

Attachments come from two sources (use either or both; at least one is
required): an inline `content` upload, and/or existing
`conversation_file_key` references. For images / binary files set
`binary=true` and pass base64-encoded bytes in `content` (with a real
`mime_type`); leaving `binary=false` on base64 image data stores it as
UTF-8 text, so the attachment renders broken.

```yaml
- id: <step>
  activity: foundation.channel.post_file
  args:
    channel_id: <string>
    text: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | string | yes | UUID of the channel / conversation to post into. |
| `text` | string | yes | Intro text shown above the attachment. Plain text unless `format: markdown` is set. |
| `format` | `plain` / `markdown` | no | How the client renders `text`: "plain" (default) or "markdown" for a caption written with markdown markup (bold, italics, lists). Default `"plain"`. |
| `content` | string, optional | no | Optional inline attachment content. Plain text by default; when `binary=true`, base64-encoded bytes (e.g. a generated image). To attach already-uploaded conversation files instead, use `conversation_file_key`. At least one of the two is required. |
| `binary` | boolean | no | When true, `content` is base64-decoded and stored as binary (e.g. images) instead of UTF-8 text. Set `mime_type` to the real type (e.g. image/jpeg, image/png) so the client renders it. Default `false`. |
| `filename` | string, optional | no | Filename for the inline `content` upload (required when `content` is set), e.g. 'reply-draft.txt'. |
| `mime_type` | string | no | MIME type of the inline `content`. Defaults to text/plain; binary posts MUST set the real type (e.g. image/jpeg, image/png) so the client renders the attachment. Default `"text/plain"`. |
| `conversation_file_key` | list of string | no | File keys of existing conversation files to attach (e.g. images uploaded by a prior step). Each becomes its own attachment, in order; combine with `content` to also upload a new one. |
| `finalize` | boolean | no | When true (default) post as a finished agent turn. Default `true`. |
| `thread_id` | string, optional | no | Root message id to post this reply under. OMIT (default) to auto-reply in the thread the flow was triggered from. Pass a message id to thread elsewhere, or "none" to force a top-level post. Runs with no chat trigger always post top-level. Threads are flat: pass the thread root, not an intermediate reply. |
| `media_metadata` | object | no | Free-form metadata stored on the inline `content` attachment's media part for special client rendering, e.g. {'kind': 'message_draft', 'to': ..., 'subject': ...} to render an email/SMS draft card. |

### `foundation.channel.react`

Add an emoji reaction to a message in a channel the bot can read.

The lightest acknowledgement a flow can give: a 👀 on an ask that is
being looked at, a ✅ on one that is done. Reacts as the workflow's bot
(`auth.agent_user_id`) on `message_id` in `channel_id`; the message
must be in that channel. Several emoji in one string ("👍🎉") are
added one each. Idempotent: a reaction the bot already has on the
message answers `already: true` instead of failing. A refused or
unknown message fails the step non-retryably.

```yaml
- id: <step>
  activity: foundation.channel.react
  args:
    channel_id: <string>
    message_id: <string>
    emoji: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | string | yes | UUID of the channel the message is in. |
| `message_id` | string | yes | UUID of the message to react to (from channel.history or search.messages, or a tracker column). |
| `emoji` | string | yes | The emoji itself, e.g. 👀 or ✅ — a Unicode character, not a :shortcode:. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `message_id` | string | The message reacted to (echoed). |
| `emoji` | string | The emoji added (echoed). |
| `already` | boolean | True when the bot had already reacted with this emoji and nothing was added. |

### `foundation.channel.set_attachment_metadata`

Stamp metadata onto a single attachment part of an existing message.

Targets the `media` part whose `url` equals `attachment_url` (the
file key) and MERGES `media_metadata` into that part — the message text
and every other part are left intact (unlike `channel.edit`, which
replaces the whole content). Used to flip a composed draft card to a saved
state (e.g. `{"status": "saved"}`) without rebuilding the card.

```yaml
- id: <step>
  activity: foundation.channel.set_attachment_metadata
  args:
    channel_id: <string>
    message_id: <string>
    attachment_url: <string>
    media_metadata: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | string | yes | UUID of the channel / conversation the message is in. |
| `message_id` | string | yes | UUID of the message whose attachment to stamp (from channel.post_file). |
| `attachment_url` | string | yes | The target attachment's `url` — i.e. the file key of the media part to stamp (the `file_key` channel.post_file returned). |
| `media_metadata` | object | yes | Metadata merged into the matched part's `media_metadata` (e.g. {'status': 'saved'}). Keys overwrite, others are preserved. |

### `foundation.channel.set_parameter`

*Beta.*

Set or unset one channel parameter on the run's own channel.

`key` is a dotted path: the first segment is the parameter (the name
the flow declares under `writes_channel_parameters:` and reads back as
`$channel.<name>`), the rest descends into its value, so
`stages.collecting_1.chase_days` sets one stage's one field and
leaves every other stage alone. Mappings on the path are created when
absent and descended into when present; a non-mapping on the path is
refused. `value` is any JSON (a mapping, a list, a number, a string,
null) up to 32 KiB. `unset: true` removes the leaf instead and takes
no `value`; unsetting a path that is not there is a no-op, and
unsetting a whole parameter puts the app's own value back in force.

The run's own `$channel.*` keeps its pinned values: read the new
value from this step's output, not from `$channel` again.

```yaml
- id: <step>
  activity: foundation.channel.set_parameter
  args:
    key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `key` | string | yes | Dotted path to write, e.g. `stages.collecting_1`. The first segment must be declared under the flow's `writes_channel_parameters:`. |
| `value` | any | no | The JSON value to store at `key`. Ignored (and refused if given) with `unset: true`. |
| `unset` | boolean | no | Remove the value at `key` instead of setting one. Default `false`. |

**Returns**

What the write left behind.

`parameter` is the top-level name written (the first segment of
`key`) and `value` its WHOLE value after the write — the mapping a
nested write descended into, not just the leaf — so a following step
can read the sibling it kept; after an unset of the whole parameter it
is the value the channel falls back to. `changed` is False when the
channel already resolved to exactly this (a retried step, an unset of
an absent path). `rev` is the config's content hash afterwards, the
same token the channel-config endpoints hand out.

| Field | Type | Notes |
|---|---|---|
| `parameter` | string |  |
| `value` | any |  |
| `changed` | boolean |  |
| `rev` | string |  |
