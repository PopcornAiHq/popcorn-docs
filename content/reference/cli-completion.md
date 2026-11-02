---
id: cli-completion
title: completion
order: 208
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The completion command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every completion subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn completion` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `completion`

Generate shell completions (bash, zsh)

```
popcorn completion <shell>
```

| Argument | Required | Notes |
|---|---|---|
| `<shell>` | yes | Shell type One of `bash`, `zsh`. |
