---
id: mcp
title: MCP
order: 3
layout: lookup
summary: >
  The tools the hosted Popcorn MCP server exposes — identity, channel
  details, search, message history, posting and reactions — with their
  arguments, generated from the server's own definitions. None changes an
  app: that is the CLI's `app` commands. Tools for checking out, forking,
  publishing and applying an app are proposed, listed apart, and not built.
concepts: [app-bundle, publish-and-apply, fork-line]
applies_to: [cli, mcp, human]
---

The hosted MCP server exposes 6 tools. They cover the conversation
surface: who you are, a channel's details, search, message history,
posting and reactions. Reads accept a channel's `#name` or its ID. Every
call runs as the person who connected the server, in the workspace
`whoami` last selected, with that person's permissions.

This page is generated from the server's tool definitions by
`scripts/sync-mcp.py` and never edited by hand. The access line under each
tool is the hint the server declares to the host; a host may use it to
decide what to ask before calling.

## Tools

### `get_channel`

Read-only. Get channel details.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `channel` | `str` | yes | Channel name (e.g. "#my-app") or conversation ID |

### `post_message`

Writes. Post a message to a channel or reply to a thread. Provide conversation_id for a new message, or message_id for a thread reply.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `content` | `str` | yes | Message text (markdown), or file content if filename set |
| `conversation_id` | `str` |  | Post new message to this channel |
| `message_id` | `str` |  | Reply in this message's thread |
| `filename` | `str` |  | Upload content as this file (e.g. "report.md") |

### `react`

Writes, idempotent. React to a message with an emoji.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message_id` | `str` | yes | Message to react to |
| `emoji` | `str` | yes | Emoji (e.g. "👍") |
| `action` | one of `add`, `remove` |  | "add" (default) or "remove" |

### `read_messages`

Read-only. Read message history.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | `str` | yes | Channel or DM ID |
| `thread_id` | `str` |  | Read this thread's replies instead |
| `time_range` | `str` |  | "start..end", "start..", or "..end" ISO datetime (ignored for threads) |
| `limit` | `int` |  | Max messages (default 25, threads 50) |

### `search`

Read-only. Search channels, DMs, users, or messages.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `type` | one of `channels`, `dms`, `users`, `messages` | yes | "channels", "dms", "users", or "messages" |
| `query` | `str` |  | Filter text (required for messages) |

### `whoami`

Writes. Your workspace and user identity.

| Argument | Type | Required | Notes |
|---|---|---|---|
| `workspace_id` | `str` |  | Switch to this workspace (UUID). Omit to show current workspace and all available workspaces (if you belong to more than one). |

## Proposed tools

**None of these tools exist yet, and nothing depends on them arriving.** They
are a design for changing an app from an MCP host: check out a channel's
bundle, edit it, prove the edit with a publish dry run, fork if the channel is
still on the product version, publish to its fork line, and watch the
install. The dry run comes before the fork because the fork is the step that
cannot be undone. They are listed so an author can see
what is being considered; names and arguments may change before any ships.
Today an app is changed with the CLI's `app` commands.

Three rules run through the design:

1. **Every write is previewed by the server.** A call without `confirm=true`
  runs the real operation with the write removed and returns what would
  happen, with a `preview_id`. The confirming call passes that id back, and
  the server refuses a confirm whose id does not match a preview of the same
  arguments by the same caller. This proves a dry run happened; whether a
  person read it is up to the host.
2. **Writes take the channel's UUID**, never a `#name`: names are not unique,
  and a publish is the worst place to resolve one to the wrong channel.
3. **Publish takes edits, not whole files** — each edit replaces text that
  must be non-empty and occur exactly once in the file, edits apply in the
  order given, and the file is checked against its hash — so a one-line change
  costs one line.

### `app_status`

Read-only. What a channel runs: the app, its line, the bound version and the
line's head, the install state and why, and the other channels on the line.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID or `#name` |

### `app_checkout`

Read-only. Without `paths`, lists the bundle's files with sizes, hashes and
the `base_version_id` a publish must name. With `paths`, returns those files,
and never a truncated one: a file that does not fit in the response is listed
as not returned, to ask for again, and a file too large for any response comes
back in byte ranges with its hash.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID or `#name` |
| `ref` | `head` | `head` is a publish base; `bound` reads what runs and says when it is not a base |
| `paths` | | Files to return whole |
| `version_id` | | A past version, for reading; never a publish base. Wins over `ref`, and the response reports `ref` as `version` |

### `app_fork`

Moves a channel from the product version onto a fork line. One-way. Without
`confirm`, previews whether it would create a line, adopt an existing one, do
nothing because the channel is already on a fork, or refuse because more than
one line could be meant.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID |
| `line` | | The line to fork to or adopt |
| `confirm` | `false` | Perform the previewed fork |
| `preview_id` | | The id the preview returned; required with `confirm` |

### `app_publish`

Publishes a new version to the channel's line. Without `confirm`, a dry run of
the real publish: the version it would mint, a diff summary, every check the
publish runs, warnings, and how many channels on the line it reaches. Published
is not installed: the channel installs it, and the rest of the line follows.

Publishing is for workspace admins only, because a publish reaches every
channel on the line. The dry run also accepts the product version as a base,
so an edit can be proven before the channel forks; only the confirmed publish
needs the fork line.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID; the channel that installs first |
| `base_version_id` | | The head the edits were made against |
| `edits` | `[]` | `{path, old, new}`, applied in order; `old` must be non-empty and occur exactly once |
| `files` | `{}` | New files only |
| `deletes` | `[]` | Paths to remove |
| `expected_sha256` | `{}` | Per path; refuses a publish against bytes that changed |
| `changelog` | | What changed |
| `confirm` | `false` | Perform the previewed publish |
| `preview_id` | | The id the preview returned; required with `confirm` |

### `app_apply`

Installs the line's head on a channel. Catching up on the line the channel is
already on needs no confirmation; adopting a different line does.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID |
| `confirm` | `false` | Perform an adoption |
| `preview_id` | | The id the adoption preview returned; required with `confirm` |
