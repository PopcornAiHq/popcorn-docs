---
id: cli-other
title: Other commands
order: 217
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The CLI's commands that take no subcommands and no arguments, each with what
  it does and its Usage line.
lede: >
  The commands that take no arguments, with what each does.
concepts: [cli]
---

The commands in `popcorn` 0.63.1 that take no subcommands and no arguments.
Global flags still go before them, as in `popcorn --json whoami`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them.

### `doctor`

Diagnose local setup: auth, API reachability, env, config

```
popcorn doctor
```

### `upgrade`

Upgrade popcorn to the latest version

```
popcorn upgrade
```

### `whoami`

Show current user and workspace

```
popcorn whoami
```
