---
id: mcp
title: MCP
order: 3
layout: lookup
summary: >
  The tools the hosted Popcorn MCP server exposes — people, channels,
  messages and a channel's app bundle — with their arguments, generated
  from the server's own definitions. They read a bundle, fork it and install
  a version; editing and publishing it is the CLI's `app` commands, and a
  publish tool is proposed, listed apart, and not built.
concepts: [app-bundle, publish-and-apply, fork-line]
applies_to: [cli, mcp, human]
---

The hosted MCP server exposes 16 tools. They cover people, channels,
messages and a channel's app bundle: find people and channels, read and
search a channel's messages, send messages and reactions, read a bundle's
files, fork it onto the workspace's own line, bring a channel on a fork
line to its line's head, or move it onto another line. They work on
channels only; direct messages are out of reach.

Every call runs as the person who connected the server, with that person's
permissions, in the one workspace the connection is bound to; every
response starts with that workspace's name. To use another workspace,
reconnect. Read tools accept a channel's `#name` or its ID; tools that
write into a channel take `channel_id`, the ID only. A listing returns one
page and a `next_cursor` to pass back with the same arguments. A fork, and
an install that moves a channel onto another line, are a dry run until
called again with `confirm=true`; an install that brings a channel to its
own line's head starts at once.

This page is generated from the server's tool definitions by
`scripts/sync-mcp.py` after each prod deploy and never edited by hand; a
date beside the title is the day of the deploy that last changed it. The
access line under each tool is the hint the server declares to the host; a
host may use it to decide what to ask before calling.

Under some tools is an example: a request a person might make, the call
an assistant makes for it, and what the tool returns. The response is the
server's real output for sample data — the workspace Acme — produced by
running the tool in the server's tests, so it changes when the tool's
output does. IDs are shortened, as `8c1f…e2`, and a long listing keeps its
first rows.

## Tools

### `add_reaction`

Writes, idempotent. Add your emoji reaction to a channel message. Adding one that's already there succeeds and changes nothing.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message_id` | `str` | yes | The message's ID. |
| `emoji` | `str` | yes | A Unicode emoji, e.g. "👍". |

### `fork_app_bundle`

Writes, destructive. Fork the app a channel runs into a new, named fork line. The line starts as a byte-identical copy of the product version the channel runs, and the channel moves onto it. That's one-way: the channel never returns to the product line, stops receiving product updates, and from then on gets only what's published to its line. Only a fork line can be published to. These tools can't publish yet: a fork line's changes are published with the Popcorn CLI (`popcorn app checkout`, then `popcorn app publish`). To change how a tracker behaves on one channel, check its settings first; fork only for what settings can't express. Validate an edit before forking, since the fork is the step that can't be undone. Without confirm=true this is a dry run that changes nothing.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | `str` | yes | The channel's ID (not its name). |
| `name` | `str` | yes | The new line's name: lowercase letters, digits, "-" and "_", starting with a letter or digit. Fork only creates a line; to move a channel onto a line that exists, use install_app_bundle(line=...). |
| `confirm` | `bool` |  | true to fork. Show the user the dry run first. Default `False`. |

**Example.** Asked:

> Give #intake its own copy of the claims app, called acme-intake, so we can change its intake form.

The assistant calls `fork_app_bundle(channel_id="c7d2…5b", name="acme-intake")`, which returns:

```text
Workspace: Acme (8c1f…e2)
Channel: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Fork: claimcoordinator 0.15.1 (product line, version_id: 812) → new fork line "acme-intake".
- The line starts as a byte-identical copy of 0.15.1. Nothing the channel runs changes now.
- #intake moves onto the line. Product updates stop reaching it.
- One-way: a channel on a fork line never returns to the product line. From then on it follows "acme-intake", and versions published there reach it within a day.
- Reach: this channel only. Other channels running claimcoordinator stay where they are.
- Other fork lines of claimcoordinator in this workspace: "acme-west" (to join one instead: install_app_bundle(line=…)).

Call again with `confirm=true` to fork the app into line "acme-intake".
```

### `get_channel`

Read-only. Show one channel: its details, your membership, and the app it runs, with the version it's on, the head of its line, and whether the latest install landed. list_channel_members lists who's in it.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel` | `str` | yes | The channel's ID, or its name ("#intake" or "intake"). Names aren't unique: if more than one channel has it, the call lists them with their IDs; pass an ID instead. |

**Example.** Asked:

> Is #intake on the latest version of its app?

The assistant calls `get_channel(channel="#intake")`, which returns:

```text
Workspace: Acme (8c1f…e2)
ID: c7d2…5b
Name: #intake
Kind: channel
Description: New claims, triaged and assigned
Archived: no
Members (incl. bots): 9
Joined: yes
Your role: admin
Unread: 4
Mentions: 1
Muted: no
App: claimcoordinator
Line: product
Version: 0.15.1 (the line's head)
Version ID: 812
Install: installed
```

### `get_user`

Read-only. Look up a person by handle: yourself, a member of this workspace, or someone from another workspace you share a channel or DM with. For a member: ID, username, display name, email, workspace role, whether they're active (no once deactivated or removed) and whether they're a bot. For someone from another workspace: display name, username and bot only. To find someone by name, use list_workspace_members. Someone from another workspace is found by user ID only, and so is a deactivated member: usernames and emails are looked up among this workspace's active members, since a username is unique only within one workspace. list_channel_members shows the IDs.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `user` | `str` |  | "me" (the default) for yourself, or a user ID, email, or username ("@name" works too). "me" always means you, even if someone's username is "me"; look them up by email or ID. Other spellings such as "self" are refused. |

### `get_workspace`

Read-only. The Popcorn workspace this connection is bound to. Every tool acts in this one workspace. It was chosen when the user connected Popcorn and can't be changed from here: to use a different workspace, the user reconnects Popcorn.

### `install_app_bundle`

Writes, destructive. Install the newest version of a channel's line on the channel. Without line, this is a catch-up (as `popcorn app apply`): a channel on a fork line installs its line's head. It runs without confirm, because the daily update would install the same version. Use it after a publish whose install was blocked, or when get_channel shows the channel behind its line. With line, or when a product-line channel would join the workspace's only fork line, it's an adoption: the channel moves onto that fork line, one-way, and installs its head. An adoption is a dry run that changes nothing unless confirm=true. It doesn't put an app on a channel that has none, and product versions reach product-line channels through the daily update, not through this tool. To change how a tracker behaves on one channel, check its settings first; a move between lines is one-way.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | `str` | yes | The channel's ID (not its name). |
| `line` | `str` |  | A fork line of this channel's app to move onto. |
| `confirm` | `bool` |  | true to make an adoption. Show the user the dry run first. Default `False`. |

### `list_app_bundle_files`

Read-only. List the files of the app a channel runs, with sizes and sha256. The header names the app, its line and the version listed. By default that's the version edits are based on, and its version_id is the publish base: on a fork line, the line's head; on the product line, the version the channel runs, which is what a fork copies. Each row's sha256 is exact: copy it, don't retype it. Read a file's content with read_app_bundle_file. To change how a tracker behaves on one channel, check its settings first: a fork is one-way, and a publish reaches every channel on the line.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel` | `str` | yes | Channel name ("#intake") or ID. |
| `version_id` | `int` |  | Another version of the channel's own line, to read history. Omit for the publish base. |
| `paths` | `list[str]` |  | Only files matching any of these: an exact path or a glob ("flows/*", "code/**"). |
| `cursor` | `str` |  | next_cursor from the previous page. |

### `list_channel_members`

Read-only. List the people in a channel, with each one's role in it. Includes people from other workspaces in a shared channel (marked [other workspace], shown without email), whom list_workspace_members doesn't list.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel` | `str` | yes | The channel's ID, or its name ("#intake" or "intake"). |
| `include_bots` | `bool` |  | Also list bots (marked [bot]). Default `False`. |
| `cursor` | `str` |  | The next_cursor from the previous page, with the same other arguments. |

### `list_channels`

Read-only. List the channels you can see in this workspace: the ones you're in (including channels shared in from another workspace) and the ones you can view without joining (marked [not joined]). Direct messages are not listed. Each row shows the channel's name, the app it runs, your unread count and mentions, and its ID. get_channel shows one channel's version and install state.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `query` | `str` |  | Case-insensitive substring of the channel name. |
| `app` | `str` |  | Only channels running this app, by its slug (e.g. "claimcoordinator"). |
| `include_archived` | `bool` |  | Also list archived channels (marked [archived]). Default `False`. |
| `sort` | one of `name`, `recent` |  | "name" (default), or "recent": pinned first, then by last message. |
| `cursor` | `str` |  | The next_cursor from the previous page, with the same other arguments. |

**Example.** Asked:

> Which of our channels run the claims coordinator app?

The assistant calls `list_channels(app="claimcoordinator")`, which returns:

```text
Workspace: Acme (8c1f…e2)
50 of 137 channels running claimcoordinator:
- #claims-central  claimcoordinator  (id: 2af4…0c)
- #claims-east  claimcoordinator  4 unread, 1 mention  (id: be23…ef)  [pinned]
- #claims-north  claimcoordinator  (id: bd7d…b9)  [not joined]
- … 47 more rows
next_cursor: eyJ2IjoxLCJzb3J0IjoibmFtZSIsInEiOiIiLCJhcHAiOiJjbGFpbWNvb3JkaW5hdG9yIiwiaW5jbHVkZV9hcmNoaXZlZCI6ZmFsc2UsImFmdGVyIjpbImNsYWltcy1yZWdpb24tNDciLCJjMGI0MzYwMy00M2M0LTVkZTYtOGRiOS00MWJhMzc3OGZjZjIiXX0
```

### `list_messages`

Read-only. A channel's messages, newest first, or one thread's replies. Each row is a timestamp (UTC), the message ID, the author, the text (long text is cut and marked; read_message returns it whole), one bracketed line per attachment, tool run or other part, and the reply count with the thread_id that lists the replies. Listing doesn't mark anything read. To read a channel agent's answer to a top-level message you sent, pass that message's ID as `thread_id`: in a channel the agent answers in a thread under the message that asked. For a message you sent inside a thread, pass the thread's ID as `thread_id` and your message's ID as `after`. A channel set to reply in the channel posts top-level instead, so if the thread stays empty, list the channel with `after=<your message's ID>`. Replies arrive asynchronously, so if nothing is there yet, call again shortly.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel` | `str` | yes | Channel ID or "#name". |
| `thread_id` | `str` |  | List this thread's replies instead. A thread's ID is its first message's ID; a reply's ID finds its thread too. |
| `after` | `str` |  | Only messages after this ISO timestamp or message ID. |
| `before` | `str` |  | Only messages before this ISO timestamp or message ID. |
| `cursor` | `str` |  | next_cursor from the previous page. |

### `list_workspace_members`

Read-only. List the members of this workspace, alphabetically by name. This workspace's members only: someone from another workspace who is in a shared channel isn't listed here, and deactivated members never are. To look up one person by ID, email or @username (a bot included), use get_user.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `query` | `str` |  | Case-insensitive text to find in a username, display name or email, e.g. "dana". A leading "@" also matches the username after it ("@dsmith"), and still matches inside emails, so "@acme.example" finds everyone at that domain. |
| `include_bots` | `bool` |  | Also list bots. Default `False`. |
| `cursor` | `str` |  | The next_cursor of the previous page, to continue. Pass the same query and include_bots as that call. |

### `read_app_bundle_file`

Read-only. Read one file of the app a channel runs, exactly as stored. The content is never cut. A file too big for one response comes in byte ranges: the header says which bytes this is, and next_cursor reads the next range. Join the ranges in order to get the file, whose sha256 the header gives. Everything after the "Content:" line is the file's text, verbatim.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel` | `str` | yes | Channel name ("#intake") or ID. |
| `path` | `str` | yes | The file's path, as list_app_bundle_files shows it. |
| `version_id` | `int` |  | Another version of the channel's own line. Omit for the publish base. |
| `cursor` | `str` |  | next_cursor from the previous range. |

### `read_message`

Read-only. One channel message in full: its whole text, a line per attachment or other part, the reply count and thread_id, and its reactions (marking yours).

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message_id` | `str` | yes | The message's ID. |
| `include_parts` | `bool` |  | Also list every part's kind and fields, including tool calls with their arguments and integration payloads: what an agent actually did. Large; leave off unless needed. The parts are paged: a response ends with next_cursor when more follow. Default `False`. |
| `cursor` | `str` |  | next_cursor from the previous page of parts. A later page holds only the parts, not the message text again. |

### `remove_reaction`

Writes, idempotent. Remove your emoji reaction from a channel message. Removing one that isn't there succeeds and changes nothing.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message_id` | `str` | yes | The message's ID. |
| `emoji` | `str` | yes | The emoji to remove, e.g. "👍". |

### `search_messages`

Read-only. Search message text across the channels you can see, ranked by relevance (or newest first with sort="recent"). Direct messages are never searched. Each result names its channel; read_message returns a result in full, and list_messages(channel, after=<id>) shows what followed it. To page through one channel in time order, use list_messages.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `query` | `str` | yes | Words to search for. |
| `channel` | `str` |  | Only this channel (ID or "#name"). |
| `author` | `str` |  | Only messages from this person: "@username", email, user ID, or "me". |
| `after` | `str` |  | Only messages from this ISO timestamp on (inclusive), or from this message's time on, the message itself left out. |
| `before` | `str` |  | Only messages up to this ISO timestamp (inclusive), or up to this message's time, the message itself left out. |
| `sort` | one of `relevance`, `recent` |  | "relevance" (default) or "recent". |
| `cursor` | `str` |  | next_cursor from the previous page. |

### `send_message`

Writes. Post a message in a channel, as you, visible to its members. Whether the channel's agent answers: an @mention of the agent gets an answer. A plain message goes to a classifier; a tracker or app channel's agent answers most messages, other channel agents only those that need it. To be surer of an answer, put the agent's handle (the bot in the channel's member list) in `mentions`. There is no answer in a channel homed in another workspace, and while the agent is already running a task in the channel, your message joins that task instead of getting its own reply. Replies arrive asynchronously, in a thread under a top-level message (unless the channel is set to reply in the channel). The response gives the new message's ID and the list_messages call that reads the answer.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel_id` | `str` | yes | The channel's ID (get_channel returns it). |
| `text` | `str` |  | Message text (markdown). Optional with an attachment. |
| `thread_id` | `str` |  | Reply in this thread (its first message's ID). |
| `mentions` | `list[str]` |  | People to mention and notify: "@username", email, user ID, or "me". Only these are mentioned; "@name" in the text is not parsed. |
| `attachment` | `Attachment` |  | A text file to attach. |

**Example.** Asked:

> Ask the agent in #intake what's still open on claim 4471, and tell me what it says.

The assistant calls `send_message(channel_id="c7d2…5b", text="What's still open on claim 4471?")`, which returns:

```text
Workspace: Acme (8c1f…e2)
Message sent to #intake (id: 7e1a…47).
Replies arrive asynchronously: a channel agent's answer typically takes seconds to a few minutes. To read them: list_messages(channel="c7d2…5b", thread_id="7e1a…47"). A channel set to reply in the channel posts its answer top-level instead; if the thread stays empty, check list_messages(channel="c7d2…5b", after="7e1a…47").
```

Then it calls `list_messages(channel="c7d2…5b", thread_id="7e1a…47")`, which returns:

```text
Workspace: Acme (8c1f…e2)
Channel: #intake (c7d2…5b) · thread: 7e1a…47
1 of 1 replies, newest first:
[2026-09-29 14:03] (id: 9a3c…19) Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension. Everything else is closed.
```

## Proposed tools

**This tool does not exist yet, and nothing depends on it arriving.** It is
listed so an author can see what is being considered; its arguments may change
before it ships. Today a bundle's files are edited and published with the
CLI's `app` commands.

### `publish_app_bundle`

Publishes a new version of the channel's bundle to its fork line. Without
`confirm=true`, a dry run of the real publish: the version it would mint, a
diff summary, every check the publish runs, warnings, and how many channels on
the line it reaches. Published is not installed: the channel installs it, and
the rest of the line follows.

Publishing is for workspace admins only, because a publish reaches every
channel on the line. It takes edits rather than whole files, so a one-line
change costs one line; the exact shape of an edit is not settled.

| Argument | Default | Notes |
|---|---|---|
| `channel_id` | | Channel ID; the channel that installs first |
| `base_version_id` | | The head the edits were made against |
| `changes` | | The edits, applied in order; shape not settled |
| `expected_sha256` | `{}` | Per path; refuses a publish against bytes that changed |
| `changelog` | | What changed |
| `confirm` | `false` | Perform the publish the dry run showed |
