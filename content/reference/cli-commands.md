---
id: cli-commands
title: commands
order: 207
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The commands command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every commands subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn commands` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `commands`

Dump CLI schema as JSON for programmatic discovery

```
popcorn commands [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--groups <str>` |  | Comma-separated command groups to include |
