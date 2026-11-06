---
id: cli/commands/auth
title: auth
order: 203
group: CLI
parent: cli/commands
layout: lookup
generated: scripts/sync-cli.py
version: 0.63.1
summary: >
  The auth command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every auth subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn auth` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `auth login`

Log in via browser OAuth

```
popcorn auth login [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--with-token` |  | Read token from stdin |
| `--force` |  | Re-authenticate |

### `auth logout`

Clear stored tokens

```
popcorn auth logout
```

### `auth status`

Show current auth status

```
popcorn auth status
```

### `auth token`

Print auth token to stdout

```
popcorn auth token
```
