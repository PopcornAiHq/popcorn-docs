---
id: cli/commands/table
title: table
order: 209
group: CLI
parent: cli/commands
layout: lookup
generated: scripts/sync-cli.py
version: 0.63.1
summary: >
  The table command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every table subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn table` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `table list`

List tables in a channel

```
popcorn table list --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table schema`

Show a table's columns

```
popcorn table schema <name> --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table rows`

List rows in a table

```
popcorn table rows <name> --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--filter <str>` |  | Equality map, e.g. '{"Status":"firing"}' |
| `--limit <int>` |  | Max rows (default 50) |
| `--cursor <str>` |  | Cursor from a previous response's pagination.next |

### `table import`

Create rows in bulk from a .jsonl, .json (array) or .csv file

```
popcorn table import <name> --channel <value> --file <str> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--file <str>` | yes | Rows to create: .jsonl/.ndjson (an object per line), .json (an array of objects) or .csv (header row = column names, cells typed from the table's schema); '-' for stdin |
| `--format <value>` |  | Input format when the file's extension doesn't say (required for '-') One of `jsonl`, `json`, `csv`. |
| `--merge-on <value>` |  | Column identifying an existing row to write over instead of adding one (repeatable). A match REPLACES that row: columns the new row omits are emptied |
| `--batch-size <int>` |  | Rows per request (default 500); each batch is written or refused whole |
| `--skip <int>` |  | Skip the first N rows of the file — resume after a failed batch |

### `table row create`

Create one row and print it as `row get` would

```
popcorn table row create <name> --channel <value> --data <str> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--data <str>` | yes | JSON object of the row's columns (use '@-' for stdin, '@path' for a file) |
| `--merge-on <value>` |  | Column identifying an existing row to write over instead of adding one (repeatable). A match REPLACES that row: columns the new row omits are emptied |

### `table row get`

Get one row

```
popcorn table row get <name> <record_id> --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `<record_id>` | yes | Record id |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table row patch`

Patch one row's columns

```
popcorn table row patch <name> <record_id> --channel <value> --data <str>
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `<record_id>` | yes | Record id |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--data <str>` | yes | JSON object of columns to set (use '@-' for stdin, '@path' for a file) |

### `table row delete`

Delete one row

```
popcorn table row delete <name> <record_id> --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `<record_id>` | yes | Record id |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table scalar list`

List scalars

```
popcorn table scalar list --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--limit <int>` |  | Max scalars (default 50) |
| `--cursor <str>` |  | Cursor from a previous response's pagination.next |

### `table scalar get`

Read one scalar

```
popcorn table scalar get <key> --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `<key>` | yes | Scalar key |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table scalar set`

Write one scalar

```
popcorn table scalar set <key> <value> --channel <value>
```

| Argument | Required | Notes |
|---|---|---|
| `<key>` | yes | Scalar key |
| `<value>` | yes | Scalar value (strings on the wire) |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table audit`

Recent agent-store audit entries

```
popcorn table audit --channel <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--entity-type <str>` |  | Filter by entity type (record, scalar, table, …) |
| `--entity-id <str>` |  | Filter by entity id — one row's or scalar's history |
| `--since <str>` |  | ISO 8601 datetime; entries at or after it (2026-09-01T00:00:00Z) |
| `--limit <int>` |  | Max entries (default 50) |
| `--cursor <str>` |  | Cursor from a previous response's pagination.next |
