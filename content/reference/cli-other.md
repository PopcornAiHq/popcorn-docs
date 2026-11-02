---
id: cli-other
title: Other commands
order: 212
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The CLI's commands that have no subcommands, each with what it does, its
  Usage line and its arguments.
lede: >
  The commands that have no subcommands, with how to run each and its
  arguments.
concepts: [cli]
---

The commands in `popcorn` 0.63.1 that have no subcommands.
Global flags still go before them, as in `popcorn --json whoami`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them.

### `api`

Raw API call (escape hatch, like gh api)

```
popcorn api <path> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<path>` | yes | API path (e.g. /api/users/me) |
| `-X <str>`, `--method <str>` |  | HTTP method (default: GET, or POST if --data) |
| `--data <str>`, `-d <str>` |  | JSON request body (use '@-' to read stdin, '@path' to read a file) |
| `-p <value>`, `--param <value>` |  | Query parameter (repeatable, e.g. -p file_key=abc) |
| `--raw` |  | Output raw JSON without envelope (even with --json) |

### `commands`

Dump CLI schema as JSON for programmatic discovery

```
popcorn commands [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--groups <str>` |  | Comma-separated command groups to include |

### `completion`

Generate shell completions (bash, zsh)

```
popcorn completion <shell>
```

| Argument | Required | Notes |
|---|---|---|
| `<shell>` | yes | Shell type One of `bash`, `zsh`. |

### `doctor`

Diagnose local setup: auth, API reachability, env, config

```
popcorn doctor
```

### `env`

Show or switch environment/profile

```
popcorn env [<target_env>]
```

| Argument | Required | Notes |
|---|---|---|
| `<target_env>` |  | Profile name to switch to |

### `upgrade`

Upgrade popcorn to the latest version

```
popcorn upgrade
```

### `version`

Show version (--check to check for updates)

```
popcorn version [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--check` |  | Force an update check and report the result on stdout |

### `whoami`

Show current user and workspace

```
popcorn whoami
```
