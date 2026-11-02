---
id: cli-flow
title: flow
order: 206
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The flow command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every flow subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn flow` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `flow activities`

List the DSL activity catalog

```
popcorn flow activities [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--name <str>` |  | Exact wire name — prints that activity's arguments |
| `--summary` |  | Drop the JSON schemas (~500 KB to ~45 KB) |
| `--tier <str>` |  | Filter by tier (foundation, feature, app, system) One of `foundation`, `feature`, `app`, `system`. |
| `--status <str>` |  | Filter by status One of `release`, `beta`, `alpha`, `deprecated`. |
| `--category <str>` |  | Filter by category (store, channel, …) |

### `flow validate`

Validate flow YAML without installing

```
popcorn flow validate <path> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<path>` | yes | Flow YAML file, or a bundle directory |
| `--channel <value>` |  | Channel name or UUID (default: the checkout's) |

### `flow list`

List flows in a channel

```
popcorn flow list --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--limit <int>` |  | Max results (default 50) |
| `--offset <int>` |  | Pagination offset |

### `flow get`

Get a flow definition and what triggers it

```
popcorn flow get <flow_id> --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<flow_id>` | yes | Flow name (as `flow list` prints it) |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--no-triggers` |  | Skip the trigger report (a cheaper read of the definition only) |

### `flow run`

Start a flow run

```
popcorn flow run <flow_id> --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<flow_id>` | yes | Flow name (as `flow list` prints it) |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--inputs <str>` |  | JSON object of flow inputs (use '@-' for stdin, '@path' for a file) |
| `--wait` |  | Poll until the server reports the run finished |
| `--timeout-run <int>` |  | Seconds to wait with --wait (default 300) |

### `flow runs list`

List flow runs in a channel

```
popcorn flow runs list --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--status <str>` |  | Filter by run status (default all) One of `all`, `running`, `failed`, `closed`. |
| `--flow <str>` |  | Flow name: list only that flow's runs on the channel (older runs may be stamped with the flow's id instead; pass the id to list those) |
| `--limit <int>` |  | Max results, 1-200 (default 50) |
| `--page-token <str>` |  | Cursor from a previous response's pagination.next |

### `flow runs get`

Get a flow run's detail

```
popcorn flow runs get <workflow_id> --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<workflow_id>` | yes | Temporal workflow ID |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--run-id <str>` |  | Specific run ID (optional) |
| `--include-errors` |  | Include error details in the run |

### `flow runs timeline`

List a flow run's steps, newest first

```
popcorn flow runs timeline <workflow_id> --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<workflow_id>` | yes | Temporal workflow ID |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--run-id <str>` |  | Specific run ID (default: the latest; pass it on later pages) |
| `--before <int>` |  | Cursor: the previous page's next_before (see pagination.next) |
| `--limit <int>` |  | Entries per page, 1-200 (default 50) |

### `flow runs cancel`

Stop a run, or every running run of a flow (--flow)

```
popcorn flow runs cancel [<workflow_id>] --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<workflow_id>` |  | Temporal workflow ID of one run (omit with --flow) |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--flow <str>` |  | Flow name: stop every running run of it on the channel |
| `--run-id <str>` |  | Specific run ID (optional) |
| `--force` |  | Terminate on the spot instead of a cooperative cancel |
| `--reason <str>` |  | Recorded on the run (optional) |
| `--page-token <str>` |  | Cursor from a previous --flow response's pagination.next |
