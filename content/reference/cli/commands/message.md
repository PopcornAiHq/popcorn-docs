---
id: cli/commands/message
title: message
order: 207
group: CLI
parent: cli/commands
layout: lookup
version: 0.63.1
summary: >
  The message command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every message subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn message` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `message answer`

Answer an agent's question card, as tapping it in the app does

```
popcorn message answer <conversation> --message <value> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--message <value>` | yes | The question's message id (from `message questions`) |
| `--thread <str>` |  | Thread the question was asked in (its root message id) |
| `--question <int>` |  | Which question on the card the flags answer (default 1); the others go as skipped, as in the app |
| `--option <value>` |  | Pick option N (repeat on a pick-any question) |
| `--label <value>` |  | Pick the option with this label (repeat on a pick-any question) |
| `--custom <str>` |  | Free-text answer, alone or beside a pick |
| `--skip` |  | Skip the question |
| `--answers <str>` |  | Every question at once, as a JSON list (literal, @file or @-): [{"option": 1}, {"label": ["A", "B"], "custom": "…"}, {"skip": true}] |
| `--dry-run` |  | Print the answers part that would be sent, and send nothing |

### `message delete`

Delete a message

```
popcorn message delete <conversation> <message_id> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message_id>` | yes | Message UUID |

### `message download`

Download a file attachment

```
popcorn message download <file_key> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<file_key>` | yes | File key (from message media part URL field) |
| `--output <str>`, `-o <str>` |  | Output path (default: original filename) |

### `message edit`

Edit a message

```
popcorn message edit <conversation> <message_id> <content> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message_id>` | yes | Message UUID |
| `<content>` | yes | New message content |
| `--no-mentions` |  | Send @names as plain text; by default each @name that matches a member's username or display name notifies them (@everyone, @here too) |

### `message get`

Get a single message by ID

```
popcorn message get <message_id>
```

| Argument | Required | Notes |
|---|---|---|
| `<message_id>` | yes | Message UUID |

### `message list`

Read message history

```
popcorn message list <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--thread <str>` |  | Thread ID to read replies |
| `--limit <int>` |  | Max messages (default 25) |
| `--before <str>` |  | Message ID — show messages before this |
| `--after <str>` |  | Message ID — show messages after this |
| `--watch` |  | Tail new messages (polling) |
| `--interval <int>` |  | Poll interval in seconds (default 3, with --watch) Default `3`. |
| `--count <int>` |  | Exit after receiving N messages (with --watch) |
| `--max-wait <float>` |  | Exit after N seconds even if no messages received (with --watch) |

### `message questions`

List an agent's unanswered question cards, numbered for `message answer`

```
popcorn message questions <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--thread <str>` |  | Thread ID to look in |
| `--limit <int>` |  | Recent messages to look through (default 50) |

### `message react`

React to a message

```
popcorn message react <conversation> <message_id> <emoji> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message_id>` | yes | Message UUID |
| `<emoji>` | yes | Emoji (e.g. "thumbs up") |
| `--remove` |  | Remove reaction instead of adding |

### `message search`

Full-text message search

```
popcorn message search [<query>] [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<query>` |  | Search query |
| `--limit <int>` |  | Max results (default 50) |
| `--offset <int>` |  | Pagination offset |
| `--in <str>` |  | Only search these channels (#general or UUID, comma-separated) |
| `--from <str>` |  | Only messages from these users (username, email or UUID, comma-separated) |
| `--since <str>` |  | Only messages after this time (ISO 8601) |
| `--until <str>` |  | Only messages before this time (ISO 8601) |
| `--has <str>` |  | Only messages containing these (file, images, link, mention, video — comma-separated) |
| `--sort <str>` |  | Result order (default relevance) One of `relevance`, `date_asc`, `date_desc`. |

### `message send`

Send a message

```
popcorn message send [<conversation>] [<message>] [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` |  | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message>` |  | Message text (use "-" for stdin) |
| `--thread <str>` |  | Reply to thread ID |
| `--file <str>` |  | File path to upload and attach |
| `--batch` |  | Read NDJSON from stdin: {"conversation": "...", "message": "..."} |
| `--fail-fast` |  | Stop batch processing on first error |
| `--no-mentions` |  | Send @names as plain text; by default each @name that matches a member's username or display name notifies them (@everyone, @here too) |

### `message threads`

List threads in a channel

```
popcorn message threads <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--limit <int>` |  | Max threads (default 50) |
| `--offset <int>` |  | Pagination offset |
