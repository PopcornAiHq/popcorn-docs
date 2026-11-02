---
id: cli-env
title: env
order: 209
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The env command and its subcommands, each with its Usage line and arguments.
lede: >
  Every env subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn env` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `env`

Show or switch environment/profile

```
popcorn env [<target_env>]
```

| Argument | Required | Notes |
|---|---|---|
| `<target_env>` |  | Profile name to switch to |
