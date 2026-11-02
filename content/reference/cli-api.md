---
id: cli-api
title: api
order: 202
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The api command and its subcommands, each with its Usage line and arguments.
lede: >
  Every api subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn api` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

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
