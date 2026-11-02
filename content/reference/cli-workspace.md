---
id: cli-workspace
title: workspace
order: 211
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The workspace command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every workspace subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn workspace` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `workspace check-access`

Check repository access

```
popcorn workspace check-access <repo>
```

| Argument | Required | Notes |
|---|---|---|
| `<repo>` | yes | Repository (owner/repo) |

### `workspace inbox`

Show notifications

```
popcorn workspace inbox [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--unread` |  | Show only unread |
| `--read` |  | Show only read |
| `--limit <int>` |  | Max results (default 20) |
| `--offset <int>` |  | Pagination offset |

### `workspace list`

List available workspaces

```
popcorn workspace list
```

### `workspace switch`

Switch active workspace

```
popcorn workspace switch [<workspace>]
```

| Argument | Required | Notes |
|---|---|---|
| `<workspace>` |  | Workspace name or UUID |

### `workspace users`

List workspace users

```
popcorn workspace users [<query>]
```

| Argument | Required | Notes |
|---|---|---|
| `<query>` |  | Filter query |
