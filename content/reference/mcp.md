---
id: mcp
title: MCP server
order: 300
group: MCP
updated: 2026-11-01
summary: >
  The hosted Popcorn MCP server, at https://mcp.popcorn.ai/mcp, gives a
  person's assistant tools for their Routines. This page says how to connect
  and what every tool shares: the Workspace a call runs in, dry runs and
  `confirm=true`, `routine` and `routine_id`, and paging. The tools themselves
  are listed A to Z on their own page.
lede: >
  Connect your assistant to Popcorn's MCP server, and learn what every tool
  shares.
concepts: [connect-your-assistant, app-bundle, versions, copying-a-template]
---

The hosted MCP server gives a person's assistant 43 tools. With them it
can find people and Routines, list the Routine Templates a new Routine can
be made from, create a Routine (optionally from a template), see whether a
Routine's Connections are made and make one from an account already
signed in to or as a webhook, see what starts its work and run a
schedule now, list and take the Actions on its items, read and change its
settings, read its tables and rows and add, change or delete rows, and read
the files of the app a Routine runs, fork it onto the workspace's own line,
publish changes to a fork line, and bring a Routine on a fork line to its
line's head or move it onto another line. They work on Routines only; a
Routine's messages and runs are read in Popcorn.

A Routine is what the CLI and the API call a channel, and its Routine
Template's code is what they call an app (an app bundle); the `#name` and
the IDs are the same.

## Connect

The server's address is `https://mcp.popcorn.ai/mcp`. In Claude Code:

```
claude mcp add --transport http --scope user popcorn https://mcp.popcorn.ai/mcp
```

The assistant opens Popcorn's sign-in; after you sign in and allow it, you
choose a Workspace if you belong to more than one. The connection stays
bound to that Workspace. [Connect your assistant](https://docs.popcorn.ai/connect-your-assistant.md)
has the steps for other assistants and how to check the connection.

## What every tool shares

Every call runs as the person who connected the server, with that person's
permissions, in the one workspace the connection is bound to; every
response starts with that workspace's name. To use another workspace,
reconnect. Read tools accept a Routine's `#name` or its ID as `routine`;
tools that write into a Routine take `routine_id`, the ID only. A listing
returns one page and a `next_cursor` to pass back with the same arguments.
A fork, a publish, an install that moves a Routine onto another line,
creating a Routine from a template, running a Trigger, taking an Action,
making a Connection, changing a setting and deleting rows are a dry run
until called again with
`confirm=true`. An
install that brings a Routine to its own line's head starts at once, and
so does creating a Routine with no template.

These pages are generated from the server's tool definitions by
`scripts/sync-mcp.py` after each prod deploy and never edited by hand; a
date beside the title is the day of the deploy that last changed it. The
badges under each tool are the access hints the server declares to the
host — `[read-only]`, or `[writes]` with `[destructive]` or `[idempotent]`
— and a host may use them to decide what to ask before calling. An argument
marked `[required]` must be passed; every other one may be left out.

Under some tools is an example: a request a person might make, then each
call an assistant makes for it, marked `→`, followed by what the tool
returns. The response is the server's real output for sample data — the
workspace Acme — produced by running the tool in the server's tests, so it
changes when the tool's output does. Examples leave out the workspace line
every response opens with. IDs are shortened, as `8c1f…e2`, a cursor keeps
its first characters, and a long listing keeps its first rows.

## Tool reference

[Tools](https://docs.popcorn.ai/mcp-tools.md) lists all 43 tools A to Z, each linking a
page of its own with its call, arguments and access hints.

