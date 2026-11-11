---
id: cli/commands/channel
title: channel
order: 204
group: CLI
parent: cli/commands
layout: lookup
generated: scripts/sync-cli.py
version: 0.63.3
summary: >
  The channel command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every channel subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn channel` in `popcorn` 0.63.3. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `channel archive`

Archive or unarchive a channel

```
popcorn channel archive <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--undo` |  | Unarchive instead |

### `channel create`

Create a channel

```
popcorn channel create <name> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Channel name |
| `--type <value>` |  | workspace_channel (default): everyone in the workspace is a member, now and as people join; public_channel: anyone can see and join it; private_channel: only invited members One of `workspace_channel`, `public_channel`, `private_channel`. Default `workspace_channel`. |
| `--members <str>` |  | Comma-separated user IDs (ignored for workspace_channel, which already has everyone) |
| `--template <str>` |  | Install a channel template (see `popcorn channel templates`) |
| `--if-not-exists` |  | Return the channel already holding this name (one you are a member of) instead of failing on the duplicate |

### `channel delete`

Delete a channel

```
popcorn channel delete <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel edit`

Update channel name or description

```
popcorn channel edit <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--name <str>` |  | New name |
| `--description <str>` |  | New description |

### `channel info`

Show channel info and members

```
popcorn channel info <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel invite`

Invite users to a channel

```
popcorn channel invite <conversation> <user_ids> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<user_ids>` | yes | Comma-separated user IDs |

### `channel join`

Join a channel

```
popcorn channel join <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel kick`

Remove a user from a channel

```
popcorn channel kick <conversation> <user_id> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<user_id>` | yes | User UUID to remove |

### `channel leave`

Leave a channel

```
popcorn channel leave <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel list`

List channels

```
popcorn channel list [<query>] [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<query>` |  | Filter query |
| `--dms` |  | List DMs instead of channels |
| `--include-archived` |  | Include archived channels (excluded by default) |
| `--include-hidden` |  | Include hidden channels (excluded by default) |

### `channel templates`

List available channel templates

```
popcorn channel templates
```
