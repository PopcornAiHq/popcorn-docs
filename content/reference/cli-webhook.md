---
id: cli-webhook
title: webhook
order: 215
group: CLI
parent: cli-command-reference
layout: lookup
version: 0.63.1
summary: >
  The webhook command and its subcommands, each with its Usage line and
  arguments.
lede: >
  Every webhook subcommand, with how to run it and its arguments.
concepts: [cli]
---

`popcorn webhook` in `popcorn` 0.63.1. Global flags go before the command, as
in `popcorn --json app status`; the
[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the
`--json` envelope and the exit codes every command shares.

### `webhook create`

Create a webhook

```
popcorn webhook create <conversation> <name> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name or UUID |
| `--channel <value>` |  | Channel name or UUID — the same argument, spelled the way every command accepts |
| `<name>` | yes | Webhook name |
| `--description <str>` |  | Webhook description |
| `--avatar-url <str>` |  | Avatar URL |
| `--action-mode <str>` |  | How deliveries are processed One of `silent`, `as_is`, `ai_enhanced`, `trigger_workflow`. |
| `--trigger-flow-name <str>` |  | Flow NAME to start, as shown by `popcorn flow list` (with --action-mode=trigger_workflow) |

### `webhook list`

List webhooks for a channel

```
popcorn webhook list <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name or UUID |
| `--channel <value>` |  | Channel name or UUID — the same argument, spelled the way every command accepts |
| `--show-url` |  | Print each webhook's ingest URL — it embeds a secret token, so it is hidden by default |

### `webhook get`

Show one webhook's settings

```
popcorn webhook get <webhook> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |
| `--show-url` |  | Print the ingest URL — it embeds a secret token, so it is hidden by default |

### `webhook update`

Change a webhook's settings

```
popcorn webhook update <webhook> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |
| `--name <str>` |  | New name |
| `--description <str>` |  | New description |
| `--avatar-url <str>` |  | New avatar URL |
| `--action-mode <str>` |  | How deliveries are processed One of `silent`, `as_is`, `ai_enhanced`, `trigger_workflow`. |
| `--activate` |  | Resume accepting deliveries |
| `--deactivate` |  | Stop accepting deliveries, keeping the webhook |
| `--enforce-hmac` |  | Reject posts without a valid signature — only takes effect once the webhook has an HMAC secret |
| `--no-enforce-hmac` |  | Accept unsigned posts again |

### `webhook delete`

Delete a webhook (prompts; --yes to skip)

```
popcorn webhook delete <webhook> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |

### `webhook override-rules get`

Show a webhook's override rules

```
popcorn webhook override-rules get <webhook> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |

### `webhook override-rules set`

Replace a webhook's override rules wholesale

```
popcorn webhook override-rules set <webhook> <rules> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `<rules>` | yes | JSON object keyed by "event_type.action" ('@-' reads stdin, '@path' reads a file) |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |

### `webhook deliveries`

List webhook deliveries

```
popcorn webhook deliveries <conversation> [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name or UUID |
| `--channel <value>` |  | Channel name or UUID — the same argument, spelled the way every command accepts |
| `--limit <int>` |  | Max results (1-100) Default `50`. |
| `--since <str>` |  | ISO timestamp — deliveries after this |
| `--after <str>` |  | Delivery UUID — deliveries after this ID (cursor) |
| `--status <str>` |  | Filter: completed,ignored,failed,processing |
| `--include <str>` |  | Comma-separated optional fields to hydrate (e.g. payload_raw) |

### `webhook event-types`

List valid webhook sources and action modes

```
popcorn webhook event-types
```

### `webhook send`

Send a payload to a webhook's ingest URL

```
popcorn webhook send <target> [<payload>] [flags]
```

| Argument | Required | Notes |
|---|---|---|
| `<target>` | yes | Ingest URL, webhook UUID, or webhook name |
| `<payload>` |  | JSON body (default {}; '@-' reads stdin, '@path' reads a file) |
| `--channel <str>` |  | Channel name or UUID — needed only when <target> is a name |
