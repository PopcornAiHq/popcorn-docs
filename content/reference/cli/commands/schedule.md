---
id: cli/commands/schedule
title: schedule
order: 208
group: CLI
parent: cli/commands
layout: lookup
generated: scripts/sync-cli.py
version: 0.63.3
summary: >
  The schedule command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every schedule subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn schedule` in `popcorn` 0.63.3. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `schedule list`

List a channel's live scheduled flows

```
popcorn schedule list --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `schedule get`

Show one scheduled flow's cadence and run counters

```
popcorn schedule get <schedule> --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `<schedule>` | yes | Schedule slug, flow id, or full schedule_id |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `schedule trigger`

Run a declared schedule now, with its stored inputs

```
popcorn schedule trigger <schedule> --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<schedule>` | yes | Schedule slug, flow id, or full schedule_id |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--overlap-policy <value>` |  | Overlap policy for this run only (default: the schedule's own); allow_all runs it even while another is in flight |
