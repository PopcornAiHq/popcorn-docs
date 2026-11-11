---
id: cli/commands/app
title: app
order: 202
group: CLI
parent: cli/commands
layout: lookup
generated: scripts/sync-cli.py
version: 0.63.3
summary: >
  The app command and its subcommands, each with its Usage line and arguments.
lede: >
  Every app subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn app` in `popcorn` 0.63.3. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `app list`

Show each app's product and fork lines, and with --channel what that channel runs

```
popcorn app list [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` |  | Also report what this channel runs (name or UUID) |

### `app lines`

List this workspace's fork lines — name, head, published_at

```
popcorn app lines [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` |  | Not needed, and ignored: the lines listed are the workspace's. Accepted so older scripts keep working |
| `--app <value>` |  | Only this app's lines (default: every app) |

### `app checkout`

Write the fork line's head (or, with --version, one past version) to disk, with a baseline

```
popcorn app checkout [<directory>] --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `<directory>` |  | Target directory (default: ./<app>) |
| `--dir <value>` |  | Target directory (default: ./<app>) — the same argument, spelled the way every command accepts |
| `--fork <value>` |  | Fork first, then check out the line's head. Takes an optional line name; bare, it confirms the line it infers. It cannot be told apart from the directory positional, so '--fork mydir' names the LINE 'mydir' — write '--fork=<line>', spell the directory '--dir <path>', or put the directory ahead of a bare --fork |
| `--version <int>` |  | Check out this version id of the channel's own line instead of its head, into ./<app>-<semver> by default. A past version is for reading and diffing; 'app publish' refuses it. Ids appear in 'app publish' and 'app status' output |
| `--force` |  | Overwrite bundle files in a non-empty directory without asking (--yes does not cover this). Nothing is deleted: files the new tree lacks stay, and are listed |

### `app fork`

Give this workspace its own fork line of the channel's app

```
popcorn app fork --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--name <value>` |  | Fork line name (default: the single line, or 'default') |

### `app publish`

Publish a checkout's edits as the next version on its fork line. Every channel on the line picks it up, so it confirms first; --yes skips that, and agent mode requires it

```
popcorn app publish [<directory>] [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<directory>` |  | Checkout directory (default: .) |
| `--dir <value>` |  | Checkout directory (default: .) — the same argument, spelled the way every command accepts |
| `--message <value>`, `-m <value>`, `--changelog <value>` |  | What changed, recorded on the version (-m, like git commit). --changelog is a deprecated alias |
| `--bump <value>` |  | Mint the next version off the fork line's head, writing manifest.yaml's 'version:' on a successful publish. Refused when the manifest already advances past the head One of `major`, `minor`, `patch`. |
| `--channel <value>` |  | Channel to act on (default: the checkout's baseline) |

### `app validate`

Check a bundle before publishing: structure offline, and in a fork checkout while logged in, the server's publish checks too (the manifest's tables among them)

```
popcorn app validate <directory> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<directory>` | yes | Bundle directory |
| `--dir <value>` |  | Bundle directory — the same argument, spelled the way every command accepts |
| `--strict` |  | Exit non-zero on warnings as well as errors |
| `--channel <value>` |  | Channel the server checks run against (default: the checkout's baseline); it must run the checkout's fork line |

### `app apply`

Recovery only: retry an install that did not land. 'publish' starts one and it normally converges on its own

```
popcorn app apply [<directory>] [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<directory>` |  | Checkout directory (default: .) |
| `--dir <value>` |  | Checkout directory (default: .) — the same argument, spelled the way every command accepts |
| `--channel <value>` |  | Channel to act on (default: the checkout's baseline) |

### `app status`

Has the publish landed? With a checkout, also what differs from the fork line's head

```
popcorn app status [<directory>] [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<directory>` |  | Checkout directory (default: .) |
| `--dir <value>` |  | Checkout directory (default: .) — the same argument, spelled the way every command accepts |
| `--channel <value>` |  | Channel to act on (default: the checkout's baseline). Outside a checkout this reports that channel's bound version, its line's head and the install state |
