---
id: cli
title: CLI
order: 2
layout: lookup
version: 0.57.0
summary: >
  Every `popcorn` command, grouped the way `popcorn --help` groups them, with
  its arguments — generated from the CLI's own schema. Global flags, agent
  mode, the `--json` envelope, exit codes and error codes follow the
  commands. The CLI installs from its GitHub repository, not PyPI; this page
  describes one release, and `popcorn <command> --help` describes yours.
concepts: [template-authoring, publish-and-apply, fork-line]
applies_to: [cli, mcp, human]
---

The 79 commands `popcorn` 0.57.0 lists in its help menu, under the
menu's own headings. Each is run as `popcorn <command>`; the global flags
at the end go before the command, as in `popcorn --json app status`.

This page is generated from `popcorn --help` and `popcorn commands` by
`scripts/sync-cli.py` and never edited by hand. When it and the CLI you
have disagree, the CLI is right: run `popcorn <command> --help`.

## Messages

### `message delete`

Delete a message

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message_id>` | yes | Message UUID |

### `message download`

Download a file attachment

| Argument | Required | Notes |
|---|---|---|
| `<file_key>` | yes | File key (from message media part URL field) |
| `--output <str>`, `-o <str>` |  | Output path (default: original filename) |

### `message edit`

Edit a message

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message_id>` | yes | Message UUID |
| `<content>` | yes | New message content |

### `message get`

Get a single message by ID

| Argument | Required | Notes |
|---|---|---|
| `<message_id>` | yes | Message UUID |

### `message list`

Read message history

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

### `message react`

React to a message

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message_id>` | yes | Message UUID |
| `<emoji>` | yes | Emoji (e.g. "thumbs up") |
| `--remove` |  | Remove reaction instead of adding |

### `message search`

Full-text message search

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

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` |  | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<message>` |  | Message text (use "-" for stdin) |
| `--thread <str>` |  | Reply to thread ID |
| `--file <str>` |  | File path to upload and attach |
| `--batch` |  | Read NDJSON from stdin: {"conversation": "...", "message": "..."} |
| `--fail-fast` |  | Stop batch processing on first error |

### `message threads`

List threads in a channel

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--limit <int>` |  | Max threads (default 50) |
| `--offset <int>` |  | Pagination offset |

## Channels

### `channel archive`

Archive or unarchive a channel

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--undo` |  | Unarchive instead |

### `channel create`

Create a channel

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Channel name |
| `--type <value>` |  | Conversation type One of `public_channel`, `private_channel`. Default `public_channel`. |
| `--members <str>` |  | Comma-separated user IDs |
| `--template <str>` |  | Install a channel template (see `popcorn channel templates`) |
| `--if-not-exists` |  | Return the channel already holding this name (one you are a member of) instead of failing on the duplicate |

### `channel delete`

Delete a channel

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel edit`

Update channel name or description

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `--name <str>` |  | New name |
| `--description <str>` |  | New description |

### `channel info`

Show channel info and members

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel invite`

Invite users to a channel

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<user_ids>` | yes | Comma-separated user IDs |

### `channel join`

Join a channel

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel kick`

Remove a user from a channel

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |
| `<user_id>` | yes | User UUID to remove |

### `channel leave`

Leave a channel

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name (#general) or UUID |
| `--channel <value>` |  | Channel name (#general) or UUID — the same argument, spelled the way every command accepts |

### `channel list`

List channels

| Argument | Required | Notes |
|---|---|---|
| `<query>` |  | Filter query |
| `--dms` |  | List DMs instead of channels |
| `--include-archived` |  | Include archived channels (excluded by default) |
| `--include-hidden` |  | Include hidden channels (excluded by default) |

### `channel templates`

List available channel templates

## Flows

### `flow activities`

List the DSL activity catalog

| Argument | Required | Notes |
|---|---|---|
| `--name <str>` |  | Exact wire name — prints that activity's arguments |
| `--summary` |  | Drop the JSON schemas (~500 KB to ~45 KB) |
| `--tier <str>` |  | Filter by tier (foundation, feature, app, system) One of `foundation`, `feature`, `app`, `system`. |
| `--status <str>` |  | Filter by status One of `release`, `beta`, `alpha`, `deprecated`. |
| `--category <str>` |  | Filter by category (store, channel, …) |

### `flow validate`

Validate flow YAML without installing

| Argument | Required | Notes |
|---|---|---|
| `<path>` | yes | Flow YAML file, or a bundle directory |
| `--channel <value>` |  | Channel name or UUID (default: the checkout's) |

### `flow list`

List flows in a channel

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--limit <int>` |  | Max results (default 50) |
| `--offset <int>` |  | Pagination offset |

### `flow get`

Get a flow definition and what triggers it

| Argument | Required | Notes |
|---|---|---|
| `<flow_id>` | yes | Flow name (as `flow list` prints it) |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--no-triggers` |  | Skip the trigger report (a cheaper read of the definition only) |

### `flow run`

Start a flow run

| Argument | Required | Notes |
|---|---|---|
| `<flow_id>` | yes | Flow UUID |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--inputs <str>` |  | JSON object of flow inputs (use '@-' for stdin, '@path' for a file) |
| `--wait` |  | Poll until the server reports the run finished |
| `--timeout-run <int>` |  | Seconds to wait with --wait (default 300) |

### `flow runs list`

List flow runs in a channel

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--status <str>` |  | Filter by run status (default all) One of `all`, `running`, `failed`, `closed`. |
| `--flow <str>` |  | Flow name: list only that flow's runs on the channel (older runs may be stamped with the flow's id instead; pass the id to list those) |
| `--limit <int>` |  | Max results, 1-200 (default 50) |
| `--page-token <str>` |  | Cursor from a previous response's pagination.next |

### `flow runs get`

Get a flow run's detail

| Argument | Required | Notes |
|---|---|---|
| `<workflow_id>` | yes | Temporal workflow ID |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--run-id <str>` |  | Specific run ID (optional) |
| `--include-errors` |  | Include error details in the run |

### `flow runs cancel`

Stop a run, or every running run of a flow (--flow)

| Argument | Required | Notes |
|---|---|---|
| `<workflow_id>` |  | Temporal workflow ID of one run (omit with --flow) |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--flow <str>` |  | Flow name: stop every running run of it on the channel |
| `--run-id <str>` |  | Specific run ID (optional) |
| `--force` |  | Terminate on the spot instead of a cooperative cancel |
| `--reason <str>` |  | Recorded on the run (optional) |
| `--page-token <str>` |  | Cursor from a previous --flow response's pagination.next |

### `schedule list`

List a channel's live scheduled flows

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `schedule get`

Show one scheduled flow's cadence and run counters

| Argument | Required | Notes |
|---|---|---|
| `<schedule>` | yes | Schedule slug, flow id, or full schedule_id |
| `--channel <value>` | yes | Channel name (#general) or UUID |

## Templates

### `template check`

Check a bundle's structure offline — no channel, no server

| Argument | Required | Notes |
|---|---|---|
| `<directory>` | yes | Bundle directory |
| `--dir <value>` |  | Bundle directory — the same argument, spelled the way every command accepts |
| `--strict` |  | Exit non-zero on warnings as well as errors |

## Apps

### `app list`

Show each app's product and fork lines, and with --channel what that channel runs

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` |  | Also report what this channel runs (name or UUID) |

### `app lines`

List this workspace's fork lines — name, head, published_at

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` |  | Not needed, and ignored: the lines listed are the workspace's. Accepted so older scripts keep working |
| `--app <value>` |  | Only this app's lines (default: every app) |

### `app checkout`

Write the fork line's head (or, with --version, one past version) to disk, with a baseline

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `<directory>` |  | Target directory (default: ./<app>) |
| `--dir <value>` |  | Target directory (default: ./<app>) — the same argument, spelled the way every command accepts |
| `--fork <value>` |  | Fork first, then check out the line's head. Takes an optional line name; bare, it confirms the line it infers. It cannot be told apart from the directory positional, so '--fork mydir' names the LINE 'mydir' — write '--fork=<line>', spell the directory '--dir <path>', or put the directory ahead of a bare --fork |
| `--version <int>` |  | Check out this version id of the channel's own line instead of its head, into ./<app>-<semver> by default. A past version is for reading and diffing; 'app publish' refuses it. Ids appear in 'app publish' and 'app status' output |
| `--force` |  | Overwrite bundle files in a non-empty directory without asking (--yes does not cover this). Nothing is deleted: files the new tree lacks stay, and are listed |

### `app fork`

Give this workspace its own fork line of the channel's app

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--name <value>` |  | Fork line name (default: the single line, or 'default') |

### `app publish`

Publish a checkout's edits as the next version on its fork line. Every channel on the line picks it up, so it confirms first; --yes skips that, and agent mode requires it

| Argument | Required | Notes |
|---|---|---|
| `<directory>` |  | Checkout directory (default: .) |
| `--dir <value>` |  | Checkout directory (default: .) — the same argument, spelled the way every command accepts |
| `--message <value>`, `-m <value>`, `--changelog <value>` |  | What changed, recorded on the version (-m, like git commit). --changelog is a deprecated alias |
| `--bump <value>` |  | Mint the next version off the fork line's head, writing manifest.yaml's 'version:' on a successful publish. Refused when the manifest already advances past the head One of `major`, `minor`, `patch`. |
| `--channel <value>` |  | Channel to act on (default: the checkout's baseline) |

### `app apply`

Recovery only: retry an install that did not land. 'publish' starts one and it normally converges on its own

| Argument | Required | Notes |
|---|---|---|
| `<directory>` |  | Checkout directory (default: .) |
| `--dir <value>` |  | Checkout directory (default: .) — the same argument, spelled the way every command accepts |
| `--channel <value>` |  | Channel to act on (default: the checkout's baseline) |

### `app status`

Has the publish landed? With a checkout, also what differs from the fork line's head

| Argument | Required | Notes |
|---|---|---|
| `<directory>` |  | Checkout directory (default: .) |
| `--dir <value>` |  | Checkout directory (default: .) — the same argument, spelled the way every command accepts |
| `--channel <value>` |  | Channel to act on (default: the checkout's baseline). Outside a checkout this reports that channel's bound version, its line's head and the install state |

### `channel-config show`

Config, the flows' $channel.* usage, and the diff between them

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--strict` |  | Exit 5 when a finding would make a run fail |

### `channel-config params set`

Set key=value, keeping the other parameters

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `<assignment>` | yes | key=value (repeatable); values parse as JSON when they can |
| `--replace` |  | Make these the ONLY parameters, dropping the rest |

### `channel-config params unset`

Remove parameters, keeping the rest

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `<key>` | yes | Parameter name (repeatable) |

### `channel-config integrations set`

Point a name at one of YOUR connected accounts

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--name <value>` | yes | Integration name, as $channel.integrations.<name> |
| `--integration-id <value>` | yes | One of your account ids (see 'channel-config accounts') |

### `channel-config integrations unset`

Remove a named binding (leaves the OAuth grant)

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#alerts) or UUID |
| `--name <value>` | yes | Integration name, as $channel.integrations.<name> |

### `channel-config accounts`

Your connected accounts, with the ids 'integrations set' needs

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` |  | Ignored — your accounts are not channel-scoped; accepted so every channel-config subcommand takes it |

## Tables

### `table list`

List tables in a channel

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table schema`

Show a table's columns

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table rows`

List rows in a table

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--filter <str>` |  | Equality map, e.g. '{"Status":"firing"}' |
| `--limit <int>` |  | Max rows (default 50) |
| `--cursor <str>` |  | Cursor from a previous response's pagination.next |

### `table row get`

Get one row

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `<record_id>` | yes | Record id |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table row patch`

Patch one row's columns

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `<record_id>` | yes | Record id |
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--data <str>` | yes | JSON object of columns to set (use '@-' for stdin, '@path' for a file) |

### `table row delete`

Delete one row

| Argument | Required | Notes |
|---|---|---|
| `<name>` | yes | Table name |
| `<record_id>` | yes | Record id |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table scalar list`

List scalars

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--limit <int>` |  | Max scalars (default 50) |
| `--cursor <str>` |  | Cursor from a previous response's pagination.next |

### `table scalar get`

Read one scalar

| Argument | Required | Notes |
|---|---|---|
| `<key>` | yes | Scalar key |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table scalar set`

Write one scalar

| Argument | Required | Notes |
|---|---|---|
| `<key>` | yes | Scalar key |
| `<value>` | yes | Scalar value (strings on the wire) |
| `--channel <value>` | yes | Channel name (#general) or UUID |

### `table audit`

Recent data-store audit entries

| Argument | Required | Notes |
|---|---|---|
| `--channel <value>` | yes | Channel name (#general) or UUID |
| `--entity-type <str>` |  | Filter by entity type (record, scalar, table, …) |
| `--entity-id <str>` |  | Filter by entity id — one row's or scalar's history |
| `--since <str>` |  | ISO 8601 datetime; entries at or after it (2026-09-01T00:00:00Z) |
| `--limit <int>` |  | Max entries (default 50) |
| `--cursor <str>` |  | Cursor from a previous response's pagination.next |

## Webhooks

### `webhook create`

Create a webhook

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

| Argument | Required | Notes |
|---|---|---|
| `<conversation>` | yes | Channel name or UUID |
| `--channel <value>` |  | Channel name or UUID — the same argument, spelled the way every command accepts |
| `--show-url` |  | Print each webhook's ingest URL — it embeds a secret token, so it is hidden by default |

### `webhook get`

Show one webhook's settings

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |
| `--show-url` |  | Print the ingest URL — it embeds a secret token, so it is hidden by default |

### `webhook update`

Change a webhook's settings

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

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |

### `webhook override-rules get`

Show a webhook's override rules

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |

### `webhook override-rules set`

Replace a webhook's override rules wholesale

| Argument | Required | Notes |
|---|---|---|
| `<webhook>` | yes | Webhook UUID, or its name with --channel |
| `<rules>` | yes | JSON object keyed by "event_type.action" ('@-' reads stdin, '@path' reads a file) |
| `--channel <value>` |  | Channel holding the webhook — only needed for a name |

### `webhook deliveries`

List webhook deliveries

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

### `webhook send`

Send a payload to a webhook's ingest URL

| Argument | Required | Notes |
|---|---|---|
| `<target>` | yes | Ingest URL, webhook UUID, or webhook name |
| `<payload>` |  | JSON body (default {}; '@-' reads stdin, '@path' reads a file) |
| `--channel <str>` |  | Channel name or UUID — needed only when <target> is a name |

## Auth & identity

### `auth login`

Log in via browser OAuth

| Argument | Required | Notes |
|---|---|---|
| `--with-token` |  | Read token from stdin |
| `--force` |  | Re-authenticate |

### `auth logout`

Clear stored tokens

### `auth status`

Show current auth status

### `auth token`

Print auth token to stdout

### `workspace check-access`

Check repository access

| Argument | Required | Notes |
|---|---|---|
| `<repo>` | yes | Repository (owner/repo) |

### `workspace inbox`

Show notifications

| Argument | Required | Notes |
|---|---|---|
| `--unread` |  | Show only unread |
| `--read` |  | Show only read |
| `--limit <int>` |  | Max results (default 20) |
| `--offset <int>` |  | Pagination offset |

### `workspace list`

List available workspaces

### `workspace switch`

Switch active workspace

| Argument | Required | Notes |
|---|---|---|
| `<workspace>` |  | Workspace name or UUID |

### `workspace users`

List workspace users

| Argument | Required | Notes |
|---|---|---|
| `<query>` |  | Filter query |

### `env`

Show or switch environment/profile

| Argument | Required | Notes |
|---|---|---|
| `<target_env>` |  | Profile name to switch to |

### `whoami`

Show current user and workspace

## Other

### `api`

Raw API call (escape hatch, like gh api)

| Argument | Required | Notes |
|---|---|---|
| `<path>` | yes | API path (e.g. /api/users/me) |
| `-X <str>`, `--method <str>` |  | HTTP method (default: GET, or POST if --data) |
| `--data <str>`, `-d <str>` |  | JSON request body (use '@-' to read stdin, '@path' to read a file) |
| `-p <value>`, `--param <value>` |  | Query parameter (repeatable, e.g. -p file_key=abc) |
| `--raw` |  | Output raw JSON without envelope (even with --json) |

### `completion`

Generate shell completions (bash, zsh)

| Argument | Required | Notes |
|---|---|---|
| `<shell>` | yes | Shell type One of `bash`, `zsh`. |

### `commands`

Dump CLI schema as JSON for programmatic discovery

| Argument | Required | Notes |
|---|---|---|
| `--groups <str>` |  | Comma-separated command groups to include |

### `doctor`

Diagnose local setup: auth, API reachability, env, config

## Global options

### Global flags

| Argument | Required | Notes |
|---|---|---|
| `--json` |  | Output as JSON |
| `--workspace <str>` |  | Workspace name or ID (at login, selects it instead of prompting) |
| `-e <str>`, `--env <str>` |  | Profile/environment name to use |
| `--no-color` |  | Disable color output |
| `-q`, `--quiet` |  | Suppress informational stderr messages |
| `--timeout <float>` |  | HTTP request timeout in seconds (default: 30) |
| `--debug` |  | Log HTTP requests and responses to stderr (may include sensitive data) |
| `-y`, `--yes` |  | Assume yes on all interactive prompts (also POPCORN_ASSUME_YES=1) |

### Agent mode

`POPCORN_AGENT=1`. Set POPCORN_AGENT=1 to default --json, --quiet, and --no-color on every invocation, and to suppress auto-upgrade prompts. It does not imply --yes, and 'app publish' requires --yes in agent mode even on a TTY.

### The --json envelope

- Every command with --json emits this envelope.
- Success payloads never contain a top-level `ok` key.
- On failure, exit code is non-zero; see exit_codes.

```json
{"ok": true, "data": "<command-specific payload>"}
{"ok": false, "error": "<human-readable message>", "error_code": "<stable machine code — see error_codes>", "code": "<Python exception class name (legacy, avoid branching on)>", "retryable": "<bool — true for 5xx and 429>"}
```

**Streaming.** Streaming commands (--watch) emit one envelope per line, newline-terminated, stdout-flushed. Each line is a complete {'ok': true, 'data': ...} envelope; no trailing summary.

**Pagination.** Paginated commands include data.pagination.next. When there are more results, `next` is a dict of CLI flag→value pairs the agent can feed back to the same command to fetch the next page. When there are no more results, `next` is null.

### Exit codes

| Code | Meaning |
|---|---|
| `0` | ok |
| `1` | validation |
| `2` | auth |
| `3` | client |
| `4` | server |
| `5` | unhealthy |
| `6` | timeout |
| `130` | interrupt |

### Error codes

| `error_code` | Meaning |
|---|---|
| `validation` | Bad input, missing args, or invalid state |
| `unauthorized` | Not logged in or token expired — re-auth |
| `forbidden` | Authenticated but lacks permission |
| `not_found` | Resource does not exist |
| `conflict` | Conflicts with current state (e.g. already exists, or a stale `If-Match` revision) |
| `rate_limited` | Rate limited — honor retry_after field |
| `client_error` | Other 4xx error — request is wrong |
| `server_error` | 5xx error — retryable with backoff |
| `network_error` | Transport failure (no HTTP response) |
| `unhealthy` | The command succeeded but the thing it checked is unhealthy (`channel-config show --strict` with fatal findings) |
| `timeout` | Client-side wait elapsed before the operation finished |
| `internal` | Unexpected internal CLI error |
