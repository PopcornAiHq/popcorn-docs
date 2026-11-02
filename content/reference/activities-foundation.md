---
id: activities-foundation
title: Foundation activities
order: 102
group: Activities
parent: activities-catalog
layout: lookup
updated: 2026-10-31
summary: >
  The foundation tier: the platform operations every Flow is built from, each
  with the Step that calls it, its arguments and what it returns.
lede: >
  The platform operations every Flow is built from, with their arguments and
  results.
concepts: [activities, flow-grammar]
---

The 72 `foundation` activities at `release` or `beta` status, by
domain. `beta` ones are marked. Each also takes the optional
`integration_id` and `integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains with the
rest of what every activity shares.

## foundation.agent

### `foundation.agent.invoke`

No description in the catalog.

```yaml
- id: <step>
  activity: foundation.agent.invoke
  args:
    agent_name: <string>
    data: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `agent_name` | string | yes |  |
| `data` | object | yes |  |
| `timeout_seconds` | integer | no | Default `180`. |
| `channel_notes` | string | no | Default `""`. |
| `bundle_guidance` | string or list of string | no | Default `""`. |
| `stage_guidance` | string | no | Default `""`. |
| `process_guidance` | string | no | Default `""`. |
| `model` | string | no | Default `""`. |
| `reply` | `json` / `text` | no | Default `"json"`. |
| `act_as` | `agent` / `member` | no | `agent` (default): the workspace agent. `member`: a person, for an agent whose tools are Popcorn's MCP server. That is the person the run was started for ($trigger.user_id): who pressed Run, or the member whose message the channel agent was answering when it started the run. A call_flow child carries its parent's. A run started for nobody (a schedule, a webhook) is refused (ActAsRefused), except in a call_flow child, which acts as the channel's first admin member (NoChannelAdmin if there is none). That person's own role decides what the tools may do. Default `"agent"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | object |  |
| `model` | string |  |
| `model_source` | string |  |
| `model_requested` | string |  |
| `acted_as_user_id` | string |  |

### `foundation.agent.transform`

Transform arbitrary data with an LLM and return the parsed JSON result.

Sends `prompt` plus `data` to Claude and returns the model's JSON
output as `$steps.<id>.output`. When `output_schema` is set the result
is validated against it and a violation fails the step non-retryably.
Provider defaults to Anthropic; a `us.anthropic.*` model id (or
`CLAUDE_PROVIDER=bedrock`) routes to Bedrock.

The prompt may be supplied inline (`prompt`) or sourced from an
agent-store file (`prompt_file_key`) — exactly one is required; the file
key wins if both are set.

Two prompt styles:
  * Plain (default) — the prompt is instructions; `data` is sent as a
    separate JSON block. The (stable) instructions are sent as their own
    content block and automatically prompt-cached when they clear the
    model's minimum cacheable size, with the volatile `data` after.
  * Jinja — when `prompt_format` is `"jinja"` or the file key ends in
    `.j2`/`.jinja`, the prompt is a Jinja2 template rendered against
    `data` to produce the whole message (no separate JSON block). The
    rendered text is volatile, so it is not cached.

```yaml
- id: <step>
  activity: foundation.agent.transform
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string, optional | no |  |
| `prompt_file_key` | string, optional | no |  |
| `prompt_format` | string, optional | no |  |
| `data` | any | no |  |
| `model` | string | no | Default `"claude-sonnet-4-6"`. |
| `output_schema` | object, optional | no |  |
| `max_tokens` | integer | no | Default `4096`. |

## foundation.channel

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
no `value`; unsetting a path that is not there is a no-op.

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
can read the sibling it kept. `changed` is False when the document
already held exactly this (a retried step, an unset of an absent
path). `rev` is the config's content hash afterwards, the same token
the channel-config endpoints hand out.

| Field | Type | Notes |
|---|---|---|
| `parameter` | string |  |
| `value` | any |  |
| `changed` | boolean |  |
| `rev` | string |  |

## foundation.channels

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

## foundation.code

### `foundation.code.execute`

Run a customer-supplied code block and return its output dict.

`code_name` names a block shipped in the app bundle at `code/<name>/`
— any flow in the bundle may call any block in it, and the block comes
from the same bundle version the flow was pinned from. The block's
`run(inputs) -> dict` return value becomes `$steps.<id>.output`.
Retry is flow-owned: with `on_error.retry`
omitted the step runs on the default policy (up to 4 attempts), so set
`retry: 0` when `run()` is not idempotent.

`reads` and `writes` let the step do its store I/O inside this one
activity, both declared in the YAML. Each read (`list_rows`,
`get_records`, `get_scalar`, `get_file`, `get_file_url`) is
delivered under its `name` in `inputs`. Each write (`patch_rows`,
`ensure_table`, `upsert_rows`, `set_scalar`, `upload_file`) takes
the value returned under its `name` and stores it; consumed keys leave
the step output and
an `applied` summary takes their place (so `applied` is a reserved
output key whenever writes are declared). The block stays a pure function
of named inputs to named outputs and never sees the store. Both sides
target the run's own conversation; nothing names one.

Pure bundle blocks may opt into `recompute_on_stale` to re-read and
recalculate after a revision conflict. Only leading `patch_rows` can
trigger it; subsequent writes never cause a recomputation. This is not
a transaction: successful patches stay committed. The block must handle
its own already-applied operations on fresh rows, using fixed time and
operation IDs from inputs.
On recomputation, the reserved `inputs._code_recompute` list records
each earlier attempt's successful `applied` row references and its
`output` (excluding consumed writes). A block can preserve completed
outcomes and avoid reapplying an older intent to those targets. Staff
actions should also declare `patch_rows.skip_completed: true`.

The block has outbound internet access: plain HTTP(S) (`urllib.request`
or a client in the block's requirements.txt) reaches public, keyless
APIs with no connection. Some hosts refuse a custom User-Agent (ESPN's
public API does), so keep the default. A source needing an API key reads
it through `env`; one needing a member's login is a connection.

`env` names the workspace secrets (`/admin/workspace-secrets`) the
block may read, each set as an environment variable of the same name.
Names only: values are fetched and encrypted inside the activity.
Customer output and error messages are published to workflow history.
Missing names fail non-retryably, listing every missing name at once.

`self_test` swaps `run()` for the block's own test suite: the runner
collects `tests/` beside the entrypoint under pytest (an image
dependency, never the block's requirements.txt), deselects tests marked
`repo`, and the step output is the report. Reads still resolve and
reach the tests as the `inputs` fixture; writes, env and
recompute_on_stale are refused. Python blocks only.

Two timeouts. `timeout_seconds` (this arg) bounds the runner's
execution of `run()` only. The STEP-level `timeout_seconds` in the
flow YAML bounds the whole activity attempt — reads, runner round trip
and writes — so a step with `reads` or `writes` must budget for the
store calls on top of the runner time.

```yaml
- id: <step>
  activity: foundation.code.execute
  args:
    code_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `code_name` | string | yes | Name of a code block shipped in this app bundle (the directory under code/). |
| `inputs` | object | no | Default `{}`. |
| `reads` | list of any | no | Store reads resolved inside the activity and delivered to the block in inputs under each entry's name. Types: list_rows (table_name, filter?, limit?, all_pages?, include_timestamps?), get_records (table_name, record_ids, missing_ok?), get_scalar (key, default?), get_file (file_key; base64 content, capped), get_file_url (file_key; presigned URL). |
| `writes` | list of any | no | Store writes applied inside the activity after run() returns, each fed by the block output key in its name (the key is then removed from the step output). Types: patch_rows (table_name; list of {record_id, expected_rev, data, change?}), ensure_table (table_name; schema), upsert_rows (table_name, merge_on?, on_conflict?; value is a list of row dicts), set_scalar (key; value is a string), upload_file (filename, content_type?, encoding text/base64; permanent; value is the content string). The step output gains applied = {count, file_keys}; patch_rows also reports patched and stale. |
| `env` | list of string | no | Workspace secret names (as set under /admin/workspace-secrets) exposed to run() as environment variables of the same name. Names only; values are read inside the activity. A name the workspace has not set fails the step. |
| `timeout_seconds` | integer | no | Seconds the runner gives run() itself. The step-level timeout_seconds in the flow bounds the whole attempt, including reads and writes. Default `60`. |
| `self_test` | boolean | no | Run the block's own test suite instead of run(): the runner collects tests/ beside the entrypoint under pytest (Python blocks only), deselects tests marked `repo`, and returns {ok, exit_code, passed, failed, errors, skipped, failures, summary, report}. `reads` still resolve and reach the tests as the `inputs` fixture; writes, env and recompute_on_stale are not allowed. Default `false`. |
| `recompute_on_stale` | integer | no | For pure, repeatable blocks: maximum re-reads and recomputations after a revision conflict in leading patch_rows writes. All patch_rows must precede other writes. Previously committed patches remain committed; the block must recognize its own operations on fresh rows. Pass time and operation IDs as fixed inputs. Default 0 fails on a conflict without recomputing. Default `0`. |

`EnsureTableWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string |  |
| `table_name` | string |  |

`GetFileRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the file under |
| `file_key` | string |  |

`GetFileUrlRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the URL under |
| `file_key` | string |  |

`GetRecordsRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string |  |
| `table_name` | string |  |
| `record_ids` | list of integer |  |
| `missing_ok` | boolean |  |

`GetScalarRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the value under |
| `key` | string |  |
| `default` | string, optional |  |

`GetTableSchemaRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the schema under |
| `table_name` | string |  |
| `missing_ok` | boolean |  |

`ListRowsRead`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | inputs key the block reads the rows under |
| `table_name` | string |  |
| `filter` | object, optional |  |
| `limit` | integer |  |
| `missing_ok` | boolean |  |
| `drop_columns` | list of string |  |
| `all_pages` | boolean |  |
| `include_timestamps` | boolean |  |

`PatchRowsWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string |  |
| `table_name` | string |  |
| `on_stale` | `fail` / `skip` |  |
| `skip_completed` | boolean |  |
| `project_states` | boolean |  |

`SetScalarWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | output key holding the string value |
| `key` | string |  |
| `change` | object, optional |  |

`UploadFileWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | output key holding the file content |
| `filename` | string |  |
| `content_type` | string |  |
| `encoding` | `text` / `base64` |  |

`UpsertRowsWrite`:

| Field | Type | Notes |
|---|---|---|
| `type` | string |  |
| `name` | string | output key holding the list of row dicts |
| `table_name` | string |  |
| `merge_on` | list of string, optional |  |
| `on_conflict` | `replace` / `merge`, optional |  |
| `change` | object, optional |  |

## foundation.contacts

### `foundation.contacts.get`

Look up a workspace contact by id (e.g. a tracker cell's contact ref).

```yaml
- id: <step>
  activity: foundation.contacts.get
  args:
    contact_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `contact_id` | string | yes | Workspace contact id (from the contacts book). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `id` | string | The contact id (echoes the input). |
| `name` | string | Contact display name. |
| `phone` | string | Contact phone in E.164. |
| `email` | string, optional | Contact email, if set (else null). |
| `tags` | list of string | Free-form workspace labels. |
| `sms_status` | string | active / opted-out / unreachable. |

### `foundation.contacts.get_many`

Resolve many workspace contacts at once to `{sms_status, name, phone}`.

Ids that do not resolve are left out of the result rather than failing
the step. Read-only: safe to retry.

```yaml
- id: <step>
  activity: foundation.contacts.get_many
  args:
    contact_ids: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `contact_ids` | list of string | yes | Workspace contact ids (e.g. a tracker column). Empty strings are ignored; duplicates collapse. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `contacts` | map of ContactsGetManyRecord | contact_id -> record, for every id that resolved. An id missing here did not resolve (unknown, foreign, malformed). |
| `requested` | integer | Distinct non-empty ids asked for. |
| `found` | integer | len(contacts). |

`ContactsGetManyRecord`:

| Field | Type | Notes |
|---|---|---|
| `sms_status` | string | active / opted-out / unreachable, or '' when the contact has no status yet. |
| `name` | string | Contact display name ('' if unset). |
| `phone` | string | Contact phone in E.164 ('' if unset). |

### `foundation.contacts.upsert`

Create the workspace contact at `phone`, or return the existing one.

```yaml
- id: <step>
  activity: foundation.contacts.upsert
  args:
    name: <string>
    phone: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Display name for a NEW contact. |
| `phone` | string | yes | E.164 phone — the per-workspace unique key. A number already in the book resolves to that contact instead of erroring. |
| `email` | string | no | Optional email address. Default `""`. |
| `tags` | list of string | no | Optional tags. |
| `update_existing` | boolean | no | When the phone already exists: False (default) returns it untouched; True also applies name/email/tags to it. Never touches sms_status either way — that is the STOP/START handler's field. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `contact_id` | string | The contact's id. |
| `created` | boolean | True when this call created the contact. |
| `updated` | boolean | True when an existing contact was edited (update_existing). |

## foundation.csv

### `foundation.csv.parse`

Parse CSV into row objects.

By default `data` is base64-encoded bytes (decoded with `encoding`); set
`is_base64: false` to pass plain CSV text directly (e.g. a pasted
spreadsheet export). Parses the result as `delimiter`-separated text,
returning `rows` (one dict per record, keyed by the header) and the
`header` column list.

```yaml
- id: <step>
  activity: foundation.csv.parse
  args:
    data: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `data` | string | yes |  |
| `delimiter` | string | no | Default `","`. |
| `encoding` | string | no | Default `"utf-8"`. |
| `is_base64` | boolean | no | Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows` | list of object |  |
| `header` | list of string |  |

### `foundation.csv.serialize`

Serialize row objects into base64-encoded CSV bytes.

Writes `rows` as `delimiter`-separated text and returns it
base64-encoded in `data`. Columns come from `header` when given, else
from the first row's keys; cells absent from a row are written blank.

```yaml
- id: <step>
  activity: foundation.csv.serialize
  args:
    rows: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `rows` | list of object | yes |  |
| `header` | list of string, optional | no |  |
| `delimiter` | string | no | Default `","`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `data` | string |  |
| `row_count` | integer |  |

## foundation.date

### `foundation.date.add`

*Beta.*

A date plus or minus a number of calendar or business days, with a
result that lands on a weekend (or a listed holiday) optionally rolled
to the nearest business day.

`date` is the start: `YYYY-MM-DD`, or a timestamp, which is read
as the calendar date it falls on in `timezone`. Omit it for today in
`timezone`. `days` is a non-negative whole number; `direction`
is `add` (the default) or `subtract`. `unit` is `calendar`
(every day counts) or `business` (only weekdays not in `holidays`
count, and the start day itself never does). `roll` is `none` (the
default), `forward` (a result on a non-business day moves to the
next business day) or `back` (to the previous one). `holidays` is
an optional list of `YYYY-MM-DD` dates treated as non-business days;
nothing is assumed about public holidays otherwise.

Pure and deterministic for a given start; safe to retry.

```yaml
- id: <step>
  activity: foundation.date.add
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `date` | string, optional | no | The start: YYYY-MM-DD, or a timestamp read in `timezone`. Omit for today. |
| `days` | integer | no | How many days to move; non-negative. Default `0`. |
| `unit` | `calendar` / `business` | no | calendar (every day) or business (weekdays not in holidays). Default `"calendar"`. |
| `direction` | `add` / `subtract` | no | add (later) or subtract (earlier). Default `"add"`. |
| `roll` | `none` / `forward` / `back` | no | What to do with a result on a non-business day: none, forward or back. Default `"none"`. |
| `timezone` | string | no | IANA zone the dates are read and written in; UTC by default. Default `"UTC"`. |
| `holidays` | list of string | no | Dates (YYYY-MM-DD) that are not business days, beyond weekends. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `date` | string | The resulting date, YYYY-MM-DD. |
| `iso` | string | The first instant of that date in `timezone`, RFC3339 with its offset: midnight, or the first time that exists on a day the zone's clock jumps forward at midnight. What a datetime column or a comparison takes. |
| `weekday` | string | The result's weekday name, Monday to Sunday. |
| `business_day` | boolean | Whether the result is a weekday not in `holidays`. |
| `rolled` | boolean | Whether `roll` moved the result off a non-business day. |
| `start` | string | The start date as read, YYYY-MM-DD. |

## foundation.fields

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

## foundation.file

### `foundation.file.copy_to_store`

Copy a conversation upload's bytes into a permanent agent-store file.

The source stays untouched; the copy survives conversation-upload
deletion and appears in the conversation's agent-store files list under
the final key. Prior files under the same stem are replaced — but never
before the replacement's bytes are durably stored.

```yaml
- id: <step>
  activity: foundation.file.copy_to_store
  args:
    conversation_id: <string>
    conversation_file_key: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; files from other conversations are not readable). |
| `conversation_file_key` | string | yes | Conversation-level uploaded file key (file_uploads). |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'onboarding/standard-retainer'. The activity appends '.<ext>' derived from the source (filename extension, then MIME, then 'bin') and replaces any existing '<stem>.*' file. URL-safe, must start with an alphanumeric. |
| `content_type` | string, optional | no | Stored content type override; defaults to the source's MIME type (or application/octet-stream when unknown). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Final agent-store file key, e.g. 'onboarding/standard-retainer.pdf'. |
| `size_bytes` | integer |  |
| `sha256` | string |  |
| `content_type` | string, optional |  |
| `filename` | string, optional | Original upload filename (for display/attachment use). |

### `foundation.file.detect`

Classify a conversation upload by metadata (no download).

Returns a single `kind` from: pdf, xlsx, csv, image, docx, text,
unknown. Branch on it with the comparison form of `when:`, e.g.
`when: "$steps.<id>.output.kind == 'pdf'"`.

```yaml
- id: <step>
  activity: foundation.file.detect
  args:
    conversation_id: <string>
    conversation_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; files from other conversations are not readable). |
| `conversation_file_key` | string | yes | Conversation-level uploaded file key (file_uploads). |
| `accept` | list of string, optional | no | Kinds this flow can handle (subset of: pdf, xlsx, csv, image, docx, text). When set, any other detected kind — including unknown — fails the step non-retryably (UnsupportedFileType), so the flow's failure_status surfaces it. Omit to classify permissively and branch on `kind` instead. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `kind` | string | One of: pdf, xlsx, csv, image, docx, text, unknown. Branch with `when: "$steps.<id>.output.kind == 'pdf'"`. |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `extension` | string, optional | Lowercased filename extension without the dot. |
| `size_bytes` | integer, optional |  |

### `foundation.file.extract_text`

Read a conversation upload's text, or a durable agent-store file's:
a text file, a PDF or a Word document.

```yaml
- id: <step>
  activity: foundation.file.extract_text
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `conversation_file_key` | string, optional | no | A conversation upload's file key. |
| `agent_store_file_key` | string, optional | no | A durable agent-store file key the flow stored (e.g. feature.gdrive.download_to_store's file_key). |
| `mime_type` | string, optional | no | With agent_store_file_key: the stored file's type, as the step that stored it reported (download_to_store's content_type). Wins over the key's extension. |
| `accept` | list of string | no | The kinds read (text, pdf, docx); any other upload fails non-retryably (UnsupportedFileType). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |
| `kind` | string | text, pdf or docx. |
| `size_bytes` | integer | The upload's size. |
| `mime_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.read_bytes`

Read a conversation upload and return its bytes base64-encoded.

```yaml
- id: <step>
  activity: foundation.file.read_bytes
  args:
    conversation_id: <string>
    conversation_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `conversation_file_key` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `data` | string |  |
| `size_bytes` | integer |  |
| `mime_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.read_text`

Read a conversation upload — or a durable agent-store file — and
return its decoded text.

```yaml
- id: <step>
  activity: foundation.file.read_text
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `conversation_file_key` | string, optional | no | A conversation upload's file key (file_uploads). |
| `agent_store_file_key` | string, optional | no | A durable agent-store file key the flows stored (e.g. templates/<sha256[:16]>.html). |
| `encoding` | string | no | Default `"utf-8"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |
| `size_bytes` | integer |  |
| `mime_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.store_text`

Store text under `<stem>.<extension>`, replacing any `<stem>.*`.

```yaml
- id: <step>
  activity: foundation.file.store_text
  args:
    conversation_id: <string>
    content: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation). |
| `content` | string | yes | The document text to store (UTF-8). Must be non-empty. |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'onboarding/questions'. URL-safe, must start with an alphanumeric; any existing '<stem>.*' file is replaced. |
| `extension` | string | no | Extension appended to the stem (no leading dot). Default `"md"`. |
| `content_type` | string | no | Stored content type. Default `"text/markdown"`. |
| `filename` | string, optional | no | Display filename echoed in the output (e.g. the source document's title) for envelope/attachment use; defaults to the final key's leaf. |

**Returns**

Mirrors `FileCopyToStoreOutput` field-for-field so dual-source flows
can coalesce the two store steps' outputs.

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Final agent-store file key, e.g. 'onboarding/questions.md'. |
| `size_bytes` | integer |  |
| `sha256` | string |  |
| `content_type` | string, optional |  |
| `filename` | string, optional |  |

### `foundation.file.upload_to_conversation`

Upload text or base64 bytes as a conversation file; post no message.

Returns the `conversation_file_key` for `channel.post_file`'s
`conversation_file_key` list or `file.copy_to_store`. Empty content
is refused. The key is server-minted, so a retry uploads again — use
`on_error: { retry: 0 }` when a duplicate would matter.

```yaml
- id: <step>
  activity: foundation.file.upload_to_conversation
  args:
    conversation_id: <string>
    filename: <string>
    content: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; the upload is scoped to it). |
| `filename` | string | yes | Display filename for the upload, e.g. 'quotes.xlsx'. |
| `content` | string | yes | The file body: plain text by default, base64-encoded bytes when `binary` is true. |
| `binary` | boolean | no | When true, `content` is base64 and is decoded to raw bytes server-side (images, spreadsheets, PDFs). Set `mime_type` to the real type. Default `false`. |
| `mime_type` | string | no | MIME type stored on the upload. Binary uploads MUST set the real type so clients render the file. Default `"text/plain"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string | The new file_uploads key, scoped to this conversation. |
| `size_bytes` | integer | Stored size (decoded bytes). |
| `filename` | string | Echoes the input filename. |
| `mime_type` | string | Echoes the input mime_type. |

## foundation.math

### `foundation.math.calculate`

*Beta.*

One binary scalar operation — `left <operation> right` — with an
optional clamp.

`operation` is one of `add | subtract | multiply | divide`.
The numeric arguments accept numeric strings (`"5"` works, so a
stored scalar feeds in directly); booleans are rejected.
`minimum` / `maximum`, when given, clamp the result into
`[minimum, maximum]`. Integer inputs stay integers for
add/subtract/multiply — unless a clamp bound binds, in which case
`value` is the bound exactly as given (`minimum: 5.0` yields
`5.0` and a `value_str` of `"5.0"`). Divide always returns a
number with a fractional part allowed. Division by zero, non-finite
numbers, `minimum > maximum`, and integer results too large to
serialize (beyond ~4300 digits) fail the step (non-retryably).

Returns `raw_value` (unclamped), `value` (clamped — the field to
use downstream), `clamped` (whether a bound changed the value),
and `value_str` (`value` as text, for `store.set_scalar`).

```yaml
- id: <step>
  activity: foundation.math.calculate
  args:
    left: <number>
    operation: <string>
    right: <number>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `left` | number | yes |  |
| `operation` | `add` / `subtract` / `multiply` / `divide` | yes |  |
| `right` | number | yes |  |
| `minimum` | number, optional | no |  |
| `maximum` | number, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `raw_value` | integer or number |  |
| `value` | integer or number |  |
| `clamped` | boolean |  |
| `value_str` | string |  |

### `foundation.math.elapsed`

*Beta.*

Signed duration between two timestamps: end minus start.

`start_iso` and `end_iso` each accept `Z`, explicit-offset,
naive (read as UTC), and date-only (midnight UTC) timestamps — the
same parsing policy as `math.offset` — and each may be
omitted/null to mean the current wall-clock time (so "age of X" is
just `start_iso: <X>`).

Returns `{seconds, minutes, hours, days}`. Each field is the WHOLE
duration expressed in that unit, unrounded and signed (negative when
`end_iso` is before `start_iso`); `days` is 24-hour days, not
calendar days.

```yaml
- id: <step>
  activity: foundation.math.elapsed
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `start_iso` | string, optional | no |  |
| `end_iso` | string, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `seconds` | number |  |
| `minutes` | number |  |
| `hours` | number |  |
| `days` | number |  |

### `foundation.math.offset`

Shift a timestamp by a duration and return the result.

Give `iso` to shift a specific timestamp, or omit it to shift from
the current wall-clock time. `direction` is `"add"` (default) or
`"subtract"`; the duration fields are non-negative and additive —
"six hours ago" is `direction: subtract, hours: 6`; a duration
given as a numeric string (`"6"`, e.g. a stored scalar) is
accepted, booleans and fractions are not. Accepts `Z`,
explicit-offset, naive (read as UTC), and date-only timestamps —
`2026-08-10` parses as MIDNIGHT UTC, so a `$lt` filter on it
excludes that whole day. The output `iso` is normalized UTC
ISO-8601, always the `+00:00` spelling (never `Z`).

Returns the same `{unix, unix_str, iso}` shape as `workflow.now`,
so the result drops straight into a `list_rows` filter
(`{"Last Seen": {"$lt": $steps.cutoff.output.iso}}`) or
`store.set_scalar`.

```yaml
- id: <step>
  activity: foundation.math.offset
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `iso` | string, optional | no |  |
| `direction` | `add` / `subtract` | no | Default `"add"`. |
| `days` | integer | no | Default `0`. |
| `hours` | integer | no | Default `0`. |
| `minutes` | integer | no | Default `0`. |
| `seconds` | integer | no | Default `0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `unix` | integer |  |
| `unix_str` | string |  |
| `iso` | string |  |

## foundation.memory

### `foundation.memory.delete`

Delete a memory by id, or every memory at (category, key).

Pass `memory_id` (from `memory.list`), or `category` + `key`. An
id is checked to belong to this step's scope before deletion — a channel
step will not delete a workspace memory, or the reverse; a key match
deletes every row at that key so a raced duplicate goes too. An
absent memory is not an error — `deleted` is 0 — because a cleanup
step re-run must not fail the flow. Safe to retry for the same reason,
and `deleted` counts the logical operation, not the attempt: a delete
that committed before its response was lost is carried into the retry
via heartbeat details, so the count does not reset to 0.

```yaml
- id: <step>
  activity: foundation.memory.delete
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation). Required at every scope. |
| `scope` | `channel` / `workspace` | no | Who the memory belongs to. 'channel' (default) is this conversation's own memory — the entity the memory panel lists and the workflow and App Builder personas recall. 'workspace' is memory every channel in the workspace shares, written against the run's own workspace. 'workspace' is NOT private to the flow: the channel and dm agents mount that same entity read-write and unconfined, so an agent can rewrite or delete what a flow put there. Every workspace member can read it, none can delete it from a product surface, and concurrent writers from different channels are normal — use it for standing facts a flow can afford to rewrite, not for state it relies on. Default `"channel"`. |
| `memory_id` | string, optional | no | Id of the memory to delete. Exclusive with category + key. |
| `category` | string, optional | no | With `key`: the category to delete from. |
| `key` | string, optional | no | With `category`: the key whose memories to delete. |
| `key_field` | string | no | Metadata field that holds the key (see memory.upsert). Default `"key"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `deleted` | integer | Rows this step deleted across all its attempts: 0 when nothing matched, >1 only when raced duplicates existed at the key. |

### `foundation.memory.list`

List memories at this scope, by exact category or by prefix.

Returns each memory's `id`, `category`, `key` (the value at
`key_field` in its metadata, or null), `content`, `extra_metadata`
and `updated_at`, in the API's listing order. Pages are walked for you;
`limit` bounds how many rows come back and a 1 MiB serialized-output
budget bounds their size (the output rides workflow history), and
`has_more` says whether either truncated. A single memory too large for
the budget fails the step non-retryably — narrow the filter or set
`include_content: false`. An exact
`category` is filtered by the API; `category_prefix` — and no filter
at all — lists every memory at the scope and filters worker-side, so a
scope holding thousands of memories pays for all of them on each call.
Budget that against the right denominator: the workspace entity is the
largest in the system, because the default `/memories` mount puts every
channel's free-form member learnings there, while a channel entity only
ever holds one channel's. Prefer an exact `category` at
`scope: workspace`. Set `include_content: false` for
a cheap key/category browse. `key` / `keys` are filtered by the API
too: reading a few keys out of a large category costs those rows, not
the category.

Read-only: safe to retry.

```yaml
- id: <step>
  activity: foundation.memory.list
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; other conversations' memories are not readable). Required at every scope. |
| `scope` | `channel` / `workspace` | no | Who the memory belongs to. 'channel' (default) is this conversation's own memory — the entity the memory panel lists and the workflow and App Builder personas recall. 'workspace' is memory every channel in the workspace shares, written against the run's own workspace. 'workspace' is NOT private to the flow: the channel and dm agents mount that same entity read-write and unconfined, so an agent can rewrite or delete what a flow put there. Every workspace member can read it, none can delete it from a product surface, and concurrent writers from different channels are normal — use it for standing facts a flow can afford to rewrite, not for state it relies on. Default `"channel"`. |
| `category` | string, optional | no | Exact category to list, e.g. 'kb:page'. Exclusive with category_prefix. |
| `category_prefix` | string, optional | no | List every category starting with this prefix, e.g. 'kb:'. Exclusive with category. Filtered worker-side after listing everything at the scope. |
| `key` | string, optional | no | Only the memory (or memories, if duplicates raced) whose metadata key_field equals this value. Exclusive with keys. |
| `keys` | list of string, optional | no | Only memories whose metadata key_field is one of these (at most 200), in one call. Rows come back in listing order, not in the order of `keys`; a key with no memory is simply absent, and an empty list returns nothing. Exclusive with key. |
| `key_field` | string | no | Metadata field that holds a memory's key. Default 'key'; the app stores use 'fact_id' and 'page_key'. Default `"key"`. |
| `include_content` | boolean | no | When false, `content` is null on every row — a cheap way to see which keys and categories exist. Default `true`. |
| `limit` | integer | no | Maximum rows returned (1..500), applied after filtering. Fewer come back when the 1 MiB output budget fills first; `has_more` reports truncation by either. Default `100`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `memories` | list of MemoryRecord | Matching memories in listing order, at most `limit`. |
| `count` | integer | len(memories). |
| `has_more` | boolean | True when more memories matched than `limit` or the 1 MiB output budget allowed. |

`MemoryRecord`:

| Field | Type | Notes |
|---|---|---|
| `id` | string | The memory id (for memory.delete). |
| `scope` | `channel` / `workspace` | The scope this row was read at. Pass it back as the `scope` of a paired upsert or delete (`scope: $m.scope`) — a write-back that drops it silently targets the channel entity instead. |
| `category` | string, optional | The memory's category. |
| `key` | string, optional | Value of `key_field` in the memory's metadata, if any. |
| `content` | object, optional | The stored JSON object (a string upsert is stored as {text: …}); null when include_content is false. |
| `extra_metadata` | object | The memory's metadata. |
| `updated_at` | string | ISO-8601 last-write timestamp. |

### `foundation.memory.upsert`

Create or update the memory at (category, key); never a near-duplicate.

Looks the key up in `category` (or, with `match_category_prefix`,
under every category with that prefix — so a memory whose category
changed is moved rather than duplicated), then updates the first match in
place or creates the row when absent. Same `content` and same
`category` is a no-op: nothing is written and `updated_at` does not
move, so applying the same block output twice writes once. Metadata is
written as `extra_metadata` plus `{key_field: key}` plus the view
stamp `view: {app, version_id, view?}` (this run's app and version,
and `view` when the version lists it in `ui.memory.views`), and is
not part of the
unchanged check.

A string `content` is stored as `{"text": …}`. Safe to retry: a retry
that follows a create whose response was lost finds the row and updates.

```yaml
- id: <step>
  activity: foundation.memory.upsert
  args:
    conversation_id: <string>
    category: <string>
    key: <string>
    content: ...
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation). Required at every scope. |
| `scope` | `channel` / `workspace` | no | Who the memory belongs to. 'channel' (default) is this conversation's own memory — the entity the memory panel lists and the workflow and App Builder personas recall. 'workspace' is memory every channel in the workspace shares, written against the run's own workspace. 'workspace' is NOT private to the flow: the channel and dm agents mount that same entity read-write and unconfined, so an agent can rewrite or delete what a flow put there. Every workspace member can read it, none can delete it from a product surface, and concurrent writers from different channels are normal — use it for standing facts a flow can afford to rewrite, not for state it relies on. Default `"channel"`. |
| `category` | string | yes | Category to write, e.g. 'quotes:vendor' or 'kb:page'. |
| `key` | string | yes | Caller-chosen identity of this memory within its category, stored in the metadata at key_field. |
| `key_field` | string | no | Metadata field that holds the key. Default 'key'; use 'fact_id' / 'page_key' to interoperate with the app stores. Default `"key"`. |
| `content` | object or string | yes | What to remember: a JSON object, or a string (stored as {text: …}). |
| `extra_metadata` | object | no | Additional metadata to store alongside the key, e.g. {derived: true}. |
| `view` | string, optional | no | The view of this app's that draws the memory on the workspace Memory tab: a name the manifest lists under `ui.memory.views`. Omit for the app's default memory view. Every write is stamped with this app and version whatever is passed; a name the version does not declare is dropped with a warning, never an error. |
| `match_category_prefix` | string, optional | no | Look the key up under every category with this prefix instead of `category` alone, and move a match to `category` if it differs. `category` must start with it. Use when one key can change category over time (the automation facts do). Costs a walk of every memory at the scope on each call that creates (the API has no prefix filter), which at scope: workspace means every channel's agent learnings too — avoid it inside a foreach there. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `memory_id` | string | Id of the memory written or kept. |
| `action` | `created` / `updated` / `unchanged` | created: new row; updated: content or category changed; unchanged: identical content and category, nothing written. |

## foundation.money

### `foundation.money.usd`

Add the US-dollar figure to each `answers[].money` in a validator
reading. `validation` is the reading exactly as the validator
submitted it; anything else is returned unchanged. Never fails: an
amount with no rate to be had gets `usd: null` and
`usd_unavailable` (`no_rate` or `lookup_failed`).

```yaml
- id: <step>
  activity: foundation.money.usd
  args:
    validation: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `validation` | object | yes | The validator's submitted reading. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `validation` | any | The same reading, each answer's `money` carrying `usd`: {figure, figure_high, rate, rate_date, source}, or null where no rate could be had, with `usd_unavailable` saying why: `no_rate` (the currency is not published) or `lookup_failed`. |

## foundation.phone

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

## foundation.rows

### `foundation.rows.update`

Apply a list of patches to in-memory rows, matched on a key field.

Each row and each patch must carry `key_field`; a patch updates the row
whose key matches (the key cell itself is never changed). Patches with no
key, or no matching row, are dropped and counted. Returns the full row
list plus `updated_count` / `dropped` — a pure transform, no store I/O.

```yaml
- id: <step>
  activity: foundation.rows.update
  args:
    rows: <array>
    key_field: <string>
    patches: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `rows` | list of object | yes |  |
| `key_field` | string | yes |  |
| `patches` | list of object, optional | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows` | list of object |  |
| `updated_count` | integer |  |
| `dropped` | integer |  |

## foundation.s3

### `foundation.s3.download`

Download an S3 object and return its bytes base64-encoded.

Reads `s3://{bucket}/{key}` and returns `data` (base64), the
`size_bytes`, and the object `etag`.

```yaml
- id: <step>
  activity: foundation.s3.download
  args:
    bucket: <string>
    key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `bucket` | string | yes |  |
| `key` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `data` | string |  |
| `size_bytes` | integer |  |
| `etag` | string, optional |  |

### `foundation.s3.upload`

Upload bytes to an S3 object.

Writes the base64-decoded `body` to `s3://{bucket}/{key}` (with an
optional `content_type`) and returns the `s3_uri`, `size_bytes`, and
`etag`.

```yaml
- id: <step>
  activity: foundation.s3.upload
  args:
    bucket: <string>
    key: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `bucket` | string | yes |  |
| `key` | string | yes |  |
| `body` | string | yes |  |
| `content_type` | string, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `s3_uri` | string |  |
| `size_bytes` | integer |  |
| `etag` | string, optional |  |

## foundation.search

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

## foundation.status

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

## foundation.store

### `foundation.store.claim_row`

Take a row for this run: one If-Match write that admits exactly one
holder, with the row's gates checked against exactly what was read.

The lock is `column`: the claim reads the row with its `rev`,
refuses if another holder is already in the column, checks every
`refuse_when` rule against the row, then patches
`{column: holder}` conditionally on that rev. A write that landed in
between (another claimant, an edit) makes the store answer
`stale_rev` and this run is refused `held_code` — among concurrent
claimants exactly one matches the rev it read. A retry of the same
holder finds its own id in the column and returns without writing
(`claimed: false`) BEFORE the rules run: the claim it holds was
checked when it was taken, and refusing it now — the row edited in
between, the first attempt's response lost — would leave the column
held with no release path. A row the store answers without a `rev`
fails `StoreClaimRowNoRevision`: without a rev to match on there is
no single winner, and a claim that cannot promise one is no claim.
Releasing is the flow's job: it writes
`{column: ""}` on every outcome, through whatever step re-derives the
row's state, so a failed run lands the row back where it was.

This is the read-check-write of a code block's claim without the
code runner: the decision is a handful of cell comparisons, and a
`foundation.code.execute` step spends most of its time getting to
them (the runner round trip, the declared reads, the state
projection). A flow that needs the row's derived machines repainted
at claim time keeps the code step; one that only needs the lock — the
modal is open with its own spinner while the merge runs — takes this
and lets its publish step repaint.

`holder` is the claimant's identity, normally `$trigger.run_id`,
and the release step compares the column to the same value. Passing
it explicitly (rather than reading the activity's own run id) keeps
the claim and its release on one source and lets a flow claim on
behalf of a run it launched.

`wait_for_holder_seconds` > 0 polls the row once a second, for at
most that long, while another holder has it, then claims the row as
it is afterwards instead of refusing at once. For a claim a person
is waiting on that meets a short-lived holder (a merge that is about
to finish for them anyway). 0, the default, refuses at once.

`file_stem_prefix` asks for a per-claim file stem in the result:
`<prefix>/<record_id>/<holder>`, the holder reduced to key-safe
characters and its first 32 — unique per (row, holder), so files a
run produces for the row it claimed never collide with another run's
and can be swept by stem. Here because the flow language has no
string concatenation, and the claim already holds both parts.

Refusals fail the run by name — `code` becomes the failure type,
`message` its reason — so `on_error: {policy: fail}` (the default)
surfaces them to the caller exactly as `foundation.workflow.fail`
would. A row that does not exist fails `StoreClaimRowNotFound`.

```yaml
- id: <step>
  activity: foundation.store.claim_row
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
    column: <string>
    holder: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |
| `column` | string | yes | The holder column, e.g. Regenerating or Sending. |
| `holder` | string | yes | This claimant's identity; normally $trigger.run_id. An opaque, exact string: compared byte for byte with the column. |
| `held_code` | string | no | Failure type when another holder has the column, or the row changed under the claim. Default `"StoreClaimRowHeld"`. |
| `held_message` | string | no | Default `"Another run holds this row; wait for it to finish."`. |
| `refuse_when` | list of StoreClaimRefusal | no |  |
| `wait_for_holder_seconds` | number | no | Default `0.0`. |
| `file_stem_prefix` | string, optional | no | Set to get `file_stem` = <prefix>/<record_id>/<holder>. |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. regenerate_claimed. Unset = anonymous workflow write. |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for the audit row's change blob. |

**Returns**

`claimed` — this call wrote the holder into the column; false
when the column already carried this holder (a retry). `row` is the
row's cells exactly as the claim read them, BEFORE the write, so a
flow reads `$steps.<id>.output.row.<Column>` for what it is about to
act on; `rev` is the row's revision after the claim.

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `holder` | string |  |
| `claimed` | boolean |  |
| `rev` | integer, optional |  |
| `row` | object |  |
| `file_stem` | string, optional |  |

`StoreClaimCondition`:

| Field | Type | Notes |
|---|---|---|
| `column` | string |  |
| `test` | `set` / `unset` / `equals` / `not_equals` / `in` / `not_in` |  |
| `value` | string or list of string, optional |  |

`StoreClaimRefusal`:

| Field | Type | Notes |
|---|---|---|
| `code` | string | Error type the run fails with. |
| `message` | string | What the refusal tells the caller. |
| `when` | list of StoreClaimCondition |  |

### `foundation.store.create_table`

Create a new agent-store table in the conversation.

Defines `table_name` with `schema_def` (a `{"columns": [...]}` spec).
Fails if the table already exists — use `store.ensure_table` to
create-or-reconcile. `workspace_id` is taken from the auth context.

```yaml
- id: <step>
  activity: foundation.store.create_table
  args:
    conversation_id: <string>
    table_name: <string>
    schema_def: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `schema_def` | object | yes |  |

### `foundation.store.delete_files`

Best-effort delete of scratch files by key.

For cleaning up page images / staging blobs. `file_keys` accepts scalar
keys and/or lists of keys (flattened one level), so a DSL ref to a
`list[str]` output drops straight in. Per-key errors (including 404) are
swallowed so cleanup never fails the flow.

```yaml
- id: <step>
  activity: foundation.store.delete_files
  args:
    conversation_id: <string>
    file_keys: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_keys` | list of string or list of string | yes |  |

### `foundation.store.delete_row`

Hard-delete ONE table row by its agent-store record id.

The row identified by `record_id` is removed and an audit row is
written with its cells as `data_before`, so the data stays recoverable
from history. The delete is deliberate by construction: the flow must
already hold the id (from `store.list_rows`'s `_record_id` or a
`get_record`), so a retention sweep is `list_rows` with a date
`filter` and a `limit`, then this step under `foreach`.

`expected_rev` (the row's `_rev` from `list_rows`) makes the
delete conditional, as it does for `patch_row`: a row another writer
updated between the list and the delete 412s (`AgentStoreStaleRev`)
and survives, instead of the sweep deleting a row that is no longer the
one it listed. Set it whenever the filtered column can change under
you; a sweep that should simply leave such rows for its next run pairs
it with `on_error: {policy: skip, retry: 0}` on the foreach step. As
for `patch_row`, a bare Temporal retry replays the same stale rev and
cannot succeed — the conflict is the answer, not a transient, which is
why `retry: 0`: `policy: skip` alone still burns the interpreter's
default attempts with backoff on every conflicting row before skipping.

Retry semantics. The write carries the workflow's `run_id` +
`step_id`, from which agent_store derives an idempotency key, and the
delete commits in the same transaction as its cached response. A Temporal
retry of the SAME attempt (a lost response) therefore replays the cached
204 and returns `{deleted: true, existed: true}` without touching the
row again. `missing_ok` covers the other case — the row is already
gone because another run or actor removed it, the flow re-ran under a new
run id, or the cached response aged out — where the store answers 404:
`True` returns `{deleted: false, existed: false}`; `False` (the
default) fails the step. Note that agent_store 404s a missing TABLE the
same way it 404s a missing row, so `missing_ok` tolerates both — the
same conflation `list_rows.missing_ok` carries. Keep the default for
on-demand flows, where a missing table is usually a wrong table name.

```yaml
- id: <step>
  activity: foundation.store.delete_row
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |
| `missing_ok` | boolean | no | Default `false`. |
| `expected_rev` | integer, optional | no |  |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. pool_retention. Unset = anonymous workflow delete. |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for the audit row's change blob. |

**Returns**

`deleted` — this call removed the row (or replayed the cached
success of the attempt that did). `existed` — false only on the
`missing_ok` branch, when the store answered 404.

| Field | Type | Notes |
|---|---|---|
| `deleted` | boolean |  |
| `existed` | boolean |  |

### `foundation.store.ensure_table`

Create the table, or patch its schema if it already exists.

Idempotent `store.create_table`: returns `action` of `created`,
`exists` (nothing to write), or `patched`. Use this when a flow may
run repeatedly.

`on_conflict` decides what "already exists" means:

* `replace` (the default) — the stored schema becomes `schema_def`
  exactly. For a flow declaring its OWN table with its COMPLETE schema,
  which is every caller that predates the other mode.
* `merge` — `schema_def`'s columns are DECLARED on the stored table:
  the ones already there are left exactly as stored, the rest are
  appended, and nothing else about the stored definition is touched.
  For a flow reaching into a channel it does not own, where replace
  would delete every column it has never heard of. `added` names the
  columns the call declared and `blocked` the ones a stored column
  already owns on terms the caller cannot write; both are always on a
  merge answer. This mode never CREATES — see `_declare_columns`.

```yaml
- id: <step>
  activity: foundation.store.ensure_table
  args:
    conversation_id: <string>
    table_name: <string>
    schema_def: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `schema_def` | object | yes |  |
| `on_conflict` | `replace` / `merge` | no | Default `"replace"`. |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |

**Returns**

Result of ensuring a table exists with a schema.

| Field | Type | Notes |
|---|---|---|
| `action` | `created` / `exists` / `patched` | What the ensure did to reach the schema. |
| `table` | object | The resulting table metadata. |
| `added` | list of string | Columns this call declared. On every `on_conflict: merge` answer and on no other; empty when the table already declared them all. |
| `blocked` | list of string | Declared columns a stored column already owns on other terms — a different spelling of the name, another type, internal or computed — so the declaration was not made and a writer keyed on it will not reach them. On every `on_conflict: merge` answer and on no other. |

### `foundation.store.get_file_url`

Get a presigned download URL for a stored file.

Returns the URL (a bare string) for `file_key` so a later step can fetch
the bytes.

```yaml
- id: <step>
  activity: foundation.store.get_file_url
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_key` | string | yes |  |

### `foundation.store.get_record`

Fetch ONE table record by its agent-store record id.

The filter DSL only matches `data` columns, so this is the only way for a
flow to read a row by its primary-key id. The row's cells are returned
under `$steps.<id>.output.data`.

```yaml
- id: <step>
  activity: foundation.store.get_record
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |

**Returns**

One record fetched by id; cells under .data, its revision as .rev.

| Field | Type | Notes |
|---|---|---|
| `id` | integer | The record id. |
| `rev` | integer | The record's revision, the expected_rev a write fenced to this read passes. It sits beside the cells: data holds no _rev (a table read's rows do). |
| `data` | object | The row's cells. Read via $steps.<id>.output.data. |

### `foundation.store.get_scalar`

Read a conversation-scoped scalar by key.

Returns the stored `{key, value}`. Provide `default` to get that value
instead of a 404 when the key isn't set yet — useful for reading a
not-yet-initialized cursor on a flow's first run.

```yaml
- id: <step>
  activity: foundation.store.get_scalar
  args:
    conversation_id: <string>
    key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `key` | string | yes |  |
| `default` | string, optional | no |  |

### `foundation.store.list_rows`

List table records.

Returns the agent store's response with two row collections:
`records` is the raw store metadata shape, and `rows` is a
convenience list of each record's `data` object with `_record_id`
attached. Use `$steps.<id>.output.rows` when feeding table data into
`code.execute`.

```yaml
- id: <step>
  activity: foundation.store.list_rows
  args:
    conversation_id: <string>
    table_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `filter` | object, optional | no |  |
| `limit` | integer | no | Default `50`. |
| `missing_ok` | boolean | no | Default `false`. |
| `drop_columns` | list of string | no |  |

**Returns**

Table records in two views. Prefer $steps.<id>.output.rows over .records for downstream code/templating.

| Field | Type | Notes |
|---|---|---|
| `records` | list of any | Raw store records: each has `id` and a nested `data` object plus store metadata. |
| `rows` | list of any | Flattened convenience view: each record's `data` object with `_record_id` attached. Use $steps.<id>.output.rows for table data, especially as code.execute input. |

### `foundation.store.merge_json_scalar`

Deep-merge a JSON object into a JSON-object scalar.

Sends `patch` to the agent_store service, which merges it into the
stored JSON object under a row lock and writes the result back in one
atomic transaction — where both sides hold a dict at a key the merge
recurses, anything else is replaced by the patch value. For envelope
scalars several flows share (e.g. the onboarding-state `steps` map,
where each upload flow patches its own step id), where a plain
`set_scalar` — or a shallow merge — would clobber the sibling entries.
Concurrent merges to the same key serialize under the row lock and
converge correctly. Still not a counter: the server merges *objects*,
not numbers — an increment (`$inc`) primitive is deliberately not built.

```yaml
- id: <step>
  activity: foundation.store.merge_json_scalar
  args:
    conversation_id: <string>
    key: <string>
    patch: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `key` | string | yes |  |
| `patch` | object | yes |  |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |

### `foundation.store.patch_row`

Update one table row's cells by its record id.

Applies `patch` (column → value) to the row identified by `record_id`;
columns not in the patch are left unchanged. Without a fence the write
lands whatever else changed. A fence makes it conditional on what the
caller read, and a write it refuses 412s (`AgentStoreStaleRev`)
instead of silently clobbering. One fence per call:

* `expected_rev` (the row's `_rev`): nothing in the row changed;
* `unchanged_since` + `unchanged`: these columns did not change.
  The patched columns are always among them; other cells may have
  moved, and the patch lands over them on the fresh revision.

```yaml
- id: <step>
  activity: foundation.store.patch_row
  args:
    conversation_id: <string>
    table_name: <string>
    record_id: <integer>
    patch: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_id` | integer | yes |  |
| `patch` | object | yes |  |
| `expected_rev` | integer, optional | no | Fence: write only if NOTHING in the row changed since it was read, given as the revision read (the row's _rev). Any other write in between refuses it (AgentStoreStaleRev). Not with unchanged_since. |
| `unchanged_since` | object, optional | no | Fence: write only if the patched columns and the `unchanged` ones still hold what they held in this row as it was read: a list_rows row (cells plus _rev) or a get_record result (data plus rev). It must carry its revision. Other cells may have changed since, and are kept. Not with expected_rev. |
| `unchanged` | list of string | no | With unchanged_since: the columns the write was decided on besides the ones it patches (those are always checked). Any of them changed refuses the write (AgentStoreStaleRev), naming them. |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. investigation_applied. Unset = anonymous workflow write. |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for the audit row's change blob. |

### `foundation.store.patch_rows`

*Beta.*

Update several rows of one table in one step.

Each entry of `patches` is applied exactly as `patch_row` would apply
it: a merge of `patch` into the row `record_id`, conditional on
`expected_rev` when set, with its own audit row and realtime event.
At most 100 entries; an empty list is a no-op. A `record_id` may appear
once.

NOT atomic. Each row lands or not on its own, and the output reports
every row's fate in input order: `patched`, `conflict` (the row moved
past `expected_rev`; `rev` is its current one), `not_found`, or
`rejected` (the store refused the patch, e.g. a validation error).
None of these fail the step — gate on the counts (`rejected`,
`conflicts`) if the flow needs to. A missing table fails it, as does a
store or network error, which Temporal retries; rows already written
replay their cached result, not a second write.

`change_kind` / `change_action` / `change_detail` attribute every
row's audit entry as `patch_row`'s do; `fields` is each row's own
patched columns.

```yaml
- id: <step>
  activity: foundation.store.patch_rows
  args:
    conversation_id: <string>
    table_name: <string>
    patches: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `patches` | list of StorePatchRowsItem | yes |  |
| `change_kind` | string, optional | no | change.kind slug for every row's audit entry, e.g. triage_applied. Unset = anonymous workflow write. |
| `change_action` | string, optional | no | Human one-liner for the audit rows (≤140 chars). |
| `change_detail` | object | no | Extra machine fields for every row's change blob. |

**Returns**

Per-row results in input order, plus a count per status. No row's
cells are returned: a hundred records would be history-sized.

| Field | Type | Notes |
|---|---|---|
| `results` | list of StorePatchRowsResult |  |
| `patched` | integer |  |
| `conflicts` | integer |  |
| `not_found` | integer |  |
| `rejected` | integer |  |

`StorePatchRowsItem`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `patch` | object |  |
| `expected_rev` | integer, optional |  |

`StorePatchRowsResult`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `status` | `patched` / `conflict` / `not_found` / `rejected` |  |
| `rev` | integer, optional |  |
| `error` | string, optional |  |

### `foundation.store.set_scalar`

Set a conversation-scoped scalar (a named key/value).

Writes `value` under `key` — a small piece of flow state (e.g. a cursor
or last-success timestamp) read back later with `store.get_scalar`.

```yaml
- id: <step>
  activity: foundation.store.set_scalar
  args:
    conversation_id: <string>
    key: <string>
    value: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `key` | string | yes |  |
| `value` | string | yes |  |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |

### `foundation.store.upload_file`

Upload a text file into the conversation's agent store.

Stores `content` under `filename` with `content_type` and returns the
file metadata (including `file_key`). Set `lifetime="workflow"` for a
scratch file reaped when the workflow chain closes; omit it for a durable
file.

```yaml
- id: <step>
  activity: foundation.store.upload_file
  args:
    conversation_id: <string>
    filename: <string>
    content: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `filename` | string | yes |  |
| `content` | string | yes |  |
| `content_type` | string | no | Default `"text/plain"`. |
| `lifetime` | string, optional | no |  |

### `foundation.store.upsert_rows`

Insert or merge rows into an agent-store table.

Provide exactly one of `rows` (inline) or `rows_file_key` (a staged
blob). With `merge_on` columns an existing match is updated rather than
duplicated; `on_conflict` chooses `replace` (default) or `merge` (keep
the columns the incoming row omits). `change_kind` / `change_action`
name the write in the audit log (see `patch_row`); without them a write
with no source file is anonymous.

```yaml
- id: <step>
  activity: foundation.store.upsert_rows
  args:
    conversation_id: <string>
    table_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `rows` | list of object, optional | no |  |
| `rows_file_key` | string, optional | no |  |
| `merge_on` | list of string, optional | no |  |
| `on_conflict` | string, optional | no |  |
| `source_file_key` | string, optional | no |  |
| `source_filename` | string, optional | no |  |
| `source_kind` | string, optional | no |  |
| `change_kind` | string, optional | no | change.kind slug for the audit row, e.g. lead_intake. Unset = anonymous workflow write (or the import kind, when a source file is given). |
| `change_action` | string, optional | no | Human one-liner for the audit row (≤140 chars). |

## foundation.testing

### `foundation.testing.assert_column_values`

Check a table's rows against the values its columns declare.

`columns` defaults to every column of `table_name` whose manifest
`display` hint is `status:…` — the ones a client renders as chips,
which is exactly the set with a closed vocabulary. `allowed` maps a
column to the values it may hold and both adds unhinted columns and
overrides hinted ones. Blank (`""` or null) passes unless
`allow_blank` is false: a Decision is blank until taken.

```yaml
- id: <step>
  activity: foundation.testing.assert_column_values
  args:
    table_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `table_name` | string | yes | Store table to read. |
| `columns` | list of string | no | Columns to check; default every column with a `status:` display hint in the pinned manifest. |
| `allowed` | map of list of string | no | Explicit allowed values per column; adds a column the manifest does not hint, or overrides one it does. |
| `allow_blank` | boolean | no | Whether '' / null passes in every column. Default `true`. |
| `page_limit` | integer | no | Store page size; every page is read. Default `1000`. |
| `fail_step` | boolean | no | Raise ColumnValuesOutsideVocabulary on any offender instead of returning ok: false. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `table_name` | string |  |
| `rows` | integer | Rows read and checked. |
| `columns` | map of list of string | The vocabulary each checked column was held to. |
| `offenders` | list of Offender | Up to 200 rows outside it, by record id, column and value. |
| `offender_count` | integer |  |
| `summary` | string |  |

`Offender`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer, optional |  |
| `column` | string |  |
| `value` | any |  |

## foundation.users

### `foundation.users.find`

*Beta.*

Find workspace members by name or username and return their ids.

Matches `query` case-insensitively against each member's username and
display name, as a prefix or anywhere inside: "shaun", "Shaun Smith" and
"smith" all find Shaun Smith. Best match first: exact username, exact
display name, a name that starts with the query, a later word that
does, then the rest. Active members of the flow's own workspace only.
Each entry has the same fields `foundation.users.get` returns: no
email, no avatar. No match is an empty list. Read-only: safe to retry.

```yaml
- id: <step>
  activity: foundation.users.find
  args:
    query: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `query` | string | yes | The name or handle to look up, e.g. 'Shaun' or '@shaun'. A leading '@' is ignored. Must not be blank. |
| `limit` | integer | no | Most members to return (1-50). Default `10`. |
| `include_bots` | boolean | no | Also match agent and bot accounts. Off by default, so a name resolves to a person. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `users` | list of UserIdentity | Matching members, best match first; empty when none match. Every entry has found=true. |
| `count` | integer | How many entries `users` holds. |

`UserIdentity`:

| Field | Type | Notes |
|---|---|---|
| `user_id` | string | The requested id (echoed). |
| `found` | boolean | False when the id is unknown, in another workspace, or not a UUID. The other fields are then null. |
| `display_name` | string, optional | The user's chosen name; null if unset (fall back to `username`). |
| `username` | string, optional | Login handle. |
| `is_bot` | boolean, optional | True for agent / bot accounts. |
| `timezone` | string, optional | The IANA timezone the user chose, e.g. 'America/New_York'. Null when they left it on 'auto' (the device's clock decides, so the server knows no zone) or it is unknown: fall back, e.g. to the workspace's or UTC. |
| `role` | string, optional | Workspace role: owner, admin, member, guest or workspace_agent. Null when unknown. A guest is an outside collaborator; leave them out of anything about members. |

### `foundation.users.get`

Look up workspace users by id and return their display identity.

Give exactly one of `user_id` or `user_ids`. Ids that do not resolve
come back with `found: false` rather than failing the step. Returns
names, the bot flag, the user's chosen timezone and workspace role
(either null when unknown): no email, no avatar. Read-only: safe to
retry.

```yaml
- id: <step>
  activity: foundation.users.get
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `user_id` | string, optional | no | One workspace user id, e.g. $trigger.user_id. The result is in `user` (and as the single entry of `users`). |
| `user_ids` | list of string, optional | no | Up to 100 workspace user ids, e.g. a `display: user` column. Empty strings are ignored; duplicates collapse. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `user` | UserIdentity, optional | The `user_id` form's entry (found or not); null in the `user_ids` form. |
| `users` | list of UserIdentity | One entry per distinct requested id, in request order, including the ones that did not resolve. |
| `requested` | integer | Distinct non-empty ids asked for. |
| `found` | integer | How many entries have found=true. |

`UserIdentity`:

| Field | Type | Notes |
|---|---|---|
| `user_id` | string | The requested id (echoed). |
| `found` | boolean | False when the id is unknown, in another workspace, or not a UUID. The other fields are then null. |
| `display_name` | string, optional | The user's chosen name; null if unset (fall back to `username`). |
| `username` | string, optional | Login handle. |
| `is_bot` | boolean, optional | True for agent / bot accounts. |
| `timezone` | string, optional | The IANA timezone the user chose, e.g. 'America/New_York'. Null when they left it on 'auto' (the device's clock decides, so the server knows no zone) or it is unknown: fall back, e.g. to the workspace's or UTC. |
| `role` | string, optional | Workspace role: owner, admin, member, guest or workspace_agent. Null when unknown. A guest is an outside collaborator; leave them out of anything about members. |

## foundation.workflow

### `foundation.workflow.batch_items`

Split a list into fixed-size batches.

Chunks `items` into groups of at most `batch_size` (optionally capped
at `max_items` first). Returns `batches`, `indexed_batches` (each with
start/end offsets), and the item/batch counts — typically fed into a
`foreach` over the batches.

```yaml
- id: <step>
  activity: foundation.workflow.batch_items
  args:
    items: <array>
    batch_size: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `items` | list of any | yes | Items to split into batches. |
| `batch_size` | integer | yes | Maximum number of items in each batch. |
| `max_items` | integer, optional | no | Optional cap before batching. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `batches` | list of list of any |  |
| `indexed_batches` | list of IndexedBatch |  |
| `item_count` | integer |  |
| `batch_count` | integer |  |

`IndexedBatch`:

| Field | Type | Notes |
|---|---|---|
| `batch_number` | integer |  |
| `start_index` | integer |  |
| `end_index` | integer |  |
| `items` | list of any |  |

### `foundation.workflow.coalesce`

Return the first value in `values` that is not `None`/empty.

"Empty" means `None` or an empty string — so a skipped branch (whose
output ref resolves to `None`) and a branch that produced an empty key
are both treated as absent. Falls back to `None` when every value is
empty.

```yaml
- id: <step>
  activity: foundation.workflow.coalesce
  args:
    values: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `values` | list of any | yes | Candidate values, in priority order; first non-empty wins. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `value` | any |  |

### `foundation.workflow.fail`

Terminate the flow with a structured, non-retryable failure.

Raises an application error carrying `reason`, an optional `code` (the
error type, default `WorkflowFailed`), and optional `details`. Use to
hard-stop a flow when a precondition isn't met.

```yaml
- id: <step>
  activity: foundation.workflow.fail
  args:
    reason: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `reason` | string | yes |  |
| `code` | string, optional | no |  |
| `details` | object, optional | no |  |

### `foundation.workflow.format_text`

Render a `str.format` template with named values.

Substitutes `values` into `template` (Python `{name}` fields) and
returns the rendered `text`. Fields are bare names only: conversion
(`{name!r}`) and format specs (`{n:>4}`) work, but attribute and
index access (`{a.b}`, `{a[0]}`) are rejected as a malformed
template, as is a width or precision above `_MAX_SPEC_NUMBER`. A
missing placeholder or malformed template fails the step non-retryably.

```yaml
- id: <step>
  activity: foundation.workflow.format_text
  args:
    template: <string>
    values: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `template` | string | yes |  |
| `values` | object | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |

### `foundation.workflow.hash`

Hash a string into a slash-free hex token.

```yaml
- id: <step>
  activity: foundation.workflow.hash
  args:
    text: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `text` | string | yes | The string to hash. |
| `length` | integer | no | Truncate the hex digest to this many chars; 0 = full 64-char sha256 digest. Default `0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string | The sha256 hex digest (slash-free, [0-9a-f]), truncated to `length` chars when set. |

### `foundation.workflow.log`

Emit a structured log line tied to the current run.

Logs `message` at `level` (debug/info/warn/error) with optional
structured `fields`. A side-effect-only step for flow observability;
returns `{ok: true}`.

```yaml
- id: <step>
  activity: foundation.workflow.log
  args:
    message: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message` | string | yes |  |
| `level` | `debug` / `info` / `warn` / `error` | no | Default `"info"`. |
| `fields` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |

### `foundation.workflow.now`

Read the current wall-clock time (replay-safe), taking no arguments.

Returns `unix` (epoch seconds), `unix_str` (the same as text, for
feeding straight into `store.set_scalar`), `iso` (ISO-8601 UTC) and
`unix_ms` (epoch milliseconds, for timing spans with
`math.calculate`). All four come from one clock read, so `unix` is
`unix_ms` truncated to the second.
Flows call this instead of reading the clock directly, since the
interpreter workflow body is deterministic.

```yaml
- id: <step>
  activity: foundation.workflow.now
```

Takes no arguments of its own.

**Returns**

| Field | Type | Notes |
|---|---|---|
| `unix` | integer |  |
| `unix_str` | string |  |
| `iso` | string |  |
| `unix_ms` | integer |  |

### `foundation.workflow.parse_app_agent`

Coerce `agent` to the canonical app-agent vocabulary.

```yaml
- id: <step>
  activity: foundation.workflow.parse_app_agent
  args:
    agent: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `agent` | string | yes | Requested switch position, any casing/whitespace. 'off' passes through; anything else (empty included) coerces to 'on'. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `agent` | string |  |

### `foundation.workflow.parse_app_mode`

Coerce `mode` to the canonical app-mode vocabulary.

```yaml
- id: <step>
  activity: foundation.workflow.parse_app_mode
  args:
    mode: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `mode` | string | yes | Requested mode, any casing/whitespace. 'test' and 'off' pass through; anything else (empty included) coerces to 'prod'. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `mode` | string |  |

### `foundation.workflow.parse_send_mode`

Coerce `mode` to the canonical send-mode vocabulary.

```yaml
- id: <step>
  activity: foundation.workflow.parse_send_mode
  args:
    mode: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `mode` | string | yes | Raw popcorn.email_send_mode value, any casing/whitespace. 'draft' and 'send' pass through; anything else (empty included) coerces to 'off'. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `mode` | string |  |

### `foundation.workflow.render_template`

Render `template` (Jinja text, typically `$channel.templates.<stem>`)
against `data`. Top-level keys of `data` are exposed directly
(`{{ first_name }}`) and under `data` (`{{ data.first_name }}`).
A template error fails the step non-retryably: the template ships with
the channel, so retrying cannot fix it.

```yaml
- id: <step>
  activity: foundation.workflow.render_template
  args:
    template: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `template` | string | yes | Jinja template text. |
| `data` | object | no | Values the template renders. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string | The rendered plain text. |

### `foundation.workflow.start_flow`

Launch a sibling customer flow (installed in this conversation) by name.

Resolves `flow_name` against the conversation's installed flows and
starts it with `inputs`. The interpreter does NOT apply `$inputs.X`
defaults for launched runs, so every required input of the target flow must
be supplied explicitly in `inputs`.

```yaml
- id: <step>
  activity: foundation.workflow.start_flow
  args:
    conversation_id: <string>
    flow_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Target conversation (sets X-Active-Conversation-ID). |
| `flow_name` | string | yes | Name of the flow to launch, as installed in the conversation (e.g. 'email_backfill_gmail'). |
| `inputs` | object | no | Map of input name → value passed to the launched flow. |
| `provider` | string, optional | no | DEPRECATED, ignored. Was the connector key of the removed provider-arg override; declared only so flows stored before the `integrations` rename still pass input validation. |
| `best_effort` | boolean | no | Launch on the batch tier even though the target flow does not declare `best_effort: true` itself. Implied whenever the launching flow is not on the realtime queue (a scheduled tick on system, the eval driver on batch), so background fan-out never lands on realtime; set it to send a realtime parent's launch to the batch tier too. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `workflow_id` | string | The launched flow's workflow id. |
| `run_id` | string | Its first execution run id. |
| `started` | boolean | True when a launch was issued (always true on success; kept for parity with caller dedup logic). |

### `foundation.workflow.update_schedule`

Retune the cadence of a schedule attached to a sibling flow.

Addresses the schedule by the target flow's installed name (plus `slug`
when the flow has more than one schedule) rather than the raw Temporal
schedule id, so bundle YAMLs stay portable across installs.

```yaml
- id: <step>
  activity: foundation.workflow.update_schedule
  args:
    conversation_id: <string>
    flow_name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Target conversation (sets X-Active-Conversation-ID). |
| `flow_name` | string | yes | Name of the scheduled flow, as installed in the conversation (e.g. 'delivery_tick'). |
| `slug` | string, optional | no | Schedule slug (e.g. 'delivery-tick'). PASS IT when you know it (bundle YAMLs always do): the schedule id is then constructed deterministically, immune to Temporal visibility lag, and required anyway when the flow has more than one schedule. Omitting it falls back to discovery via the (eventually consistent) schedule list. |
| `interval_seconds` | integer, optional | no | New fixed-interval cadence in seconds. Mutually exclusive with cron_expr. |
| `cron_expr` | string, optional | no | New cron expression. Mutually exclusive with interval_seconds. |
| `jitter_seconds` | integer, optional | no | New jitter window in seconds; 0 removes it. A COMPRESSED cadence usually has to carry this: jitter is inherited from the live schedule when a patch does not mention it, so a manifest jitter sized for the prod interval survives into a much smaller one and can be the larger of the two. Restore the manifest value on the way back out. |
| `paused` | boolean, optional | no | Pause (true) or resume (false) the schedule. May stand alone (cadence untouched) or accompany a cadence change. Omitted means keep the current paused state. |
| `note` | string, optional | no | Schedule note recorded with the patch. set_app_mode uses marker notes so lifecycle unpausers (e.g. channel unarchive, which resumes only its own 'auto-paused: channel archived' note) never resume a deliberately-off channel. |
| `fire_at` | string, optional | no | ARM A ONE-SHOT: an RFC3339 instant (with zone) the schedule fires once at, replacing any earlier arm. The rail an on-demand schedule (a manifest entry with no cadence, created paused) is driven by: a flow computes the next instant its work falls due and arms it; re-arming with a later instant replaces the earlier one whole. An EMPTY STRING disarms: the schedule is emptied and paused. A flow whose 'next due' step yields either an instant or '' can pass it straight through. Mutually exclusive with every other cadence field and with paused. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `schedule_id` | string | The patched schedule's id. |
| `interval_seconds` | integer, optional | Cadence after the patch (interval form). |
| `cron_expr` | string, optional | Cadence after the patch (cron form). |
| `jitter_seconds` | integer, optional | Jitter window after the patch. |
| `paused` | boolean, optional | Paused state after the patch. |
| `updated` | boolean | True when a patch was issued (always true on success). |
