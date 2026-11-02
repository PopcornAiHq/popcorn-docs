---
id: cli
title: CLI overview
order: 200
group: CLI
version: 0.63.1
summary: >
  The `popcorn` CLI works with Popcorn from a terminal or a script. It
  installs from its GitHub repository, not PyPI, and `popcorn auth login`
  signs in. This page has what every command shares: global flags, agent mode,
  the `--json` envelope, exit codes and error codes. Each command group has
  its own page.
lede: >
  Install the popcorn CLI, sign in, and learn the flags and output every
  command shares.
concepts: [template-authoring, versions, copying-a-template]
---

The `popcorn` CLI works with Popcorn from a terminal or a script: building and
publishing Routine Templates, reading and posting messages, running Flows and
reading their Runs. The CLI and the API call a Routine a *channel* and a
Routine Template an *app*, and its commands keep those names.

These pages describe `popcorn` 0.63.1 and are generated from the CLI's own
`popcorn --help` and `popcorn commands`. When they and the CLI you have
disagree, the CLI is right: run `popcorn <command> --help`.

## Install

The CLI installs from its GitHub repository; it is not on PyPI.

```
# With uv (recommended)
uv tool install git+https://github.com/PopcornAiHq/popcorn-cli.git

# With pipx
pipx install git+https://github.com/PopcornAiHq/popcorn-cli.git

# With pip
pip install git+https://github.com/PopcornAiHq/popcorn-cli.git
```

`popcorn --version` shows the version installed, and `popcorn upgrade`
upgrades it to the latest. `popcorn doctor` checks the local setup: sign-in,
whether the API is reachable, the environment and the config.

## Sign in

```
popcorn auth login
popcorn whoami
```

`popcorn auth login` signs in through the browser, then asks which Workspace
to use; `--workspace <name>` chooses it instead. `popcorn whoami` shows who
you are signed in as and in which Workspace, and `popcorn workspace switch`
moves to another. A profile holds one sign-in: `-e <name>` uses a profile
for one command, and `popcorn env <name>` switches to it. The
[auth](https://docs.popcorn.ai/cli-auth.md) and [workspace](https://docs.popcorn.ai/cli-workspace.md) have the rest.

## Basics

Each command is run as `popcorn <command>`, and the global flags go before
the command, as in `popcorn --json app status`.

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

## Command reference

[Commands](https://docs.popcorn.ai/cli-command-reference.md) lists every command, A to Z, with a
page for each and its subcommands: 87 in all.
