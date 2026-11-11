---
id: cli/commands/channel-config
title: channel-config
order: 205
group: CLI
parent: cli/commands
layout: lookup
generated: scripts/sync-cli.py
version: 0.63.3
summary: >
  The channel-config command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every channel-config subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn channel-config` in `popcorn` 0.63.3. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `channel-config show`

Config, the flows' $channel.* usage, and the diff between them

```
popcorn channel-config show --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--strict` |  | Exit 5 when a finding would make a run fail |

### `channel-config params set`

Set key=value, keeping the other parameters

```
popcorn channel-config params set <assignment> --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `<assignment>` | yes | key=value (repeatable); values parse as JSON when they can |
| `--replace` |  | Make these the ONLY parameters, dropping the rest |

### `channel-config params unset`

Remove parameters, keeping the rest

```
popcorn channel-config params unset <key> --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `<key>` | yes | Parameter name (repeatable) |

### `channel-config integrations set`

Point a name at one of YOUR connected accounts

```
popcorn channel-config integrations set --channel <value> --name <value> --integration-id <value>
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--name <value>` | yes | Integration name, as $channel.integrations.<name> |
| `--integration-id <value>` | yes | One of your account ids (see 'channel-config accounts') |

### `channel-config integrations unset`

Remove a named binding (leaves the OAuth grant)

```
popcorn channel-config integrations unset --channel <value> --name <value>
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--name <value>` | yes | Integration name, as $channel.integrations.<name> |

### `channel-config accounts`

Your connected accounts, with the ids 'integrations set' needs

```
popcorn channel-config accounts [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` |  | Ignored — your accounts are not channel-scoped; accepted so every channel-config subcommand takes it |
