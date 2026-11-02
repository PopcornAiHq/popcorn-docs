---
id: cli-version
title: version
order: 214
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The version command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every version subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn version` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `version`

Show version (--check to check for updates)

```
popcorn version [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--check` |  | Force an update check and report the result on stdout |
