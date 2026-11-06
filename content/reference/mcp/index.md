---
id: mcp
title: MCP server overview
order: 300
group: MCP
summary: >
  The hosted Popcorn MCP server, at https://mcp.popcorn.ai/mcp, gives a
  person's assistant tools for their Routines. This page says what they cover
  and what every tool shares: the Workspace a call runs in, dry runs and
  `confirm=true`, `routine` and `routine_id`, and paging. Adding the server to
  an assistant has its own page, and the tools are listed A to Z on theirs.
lede: >
  Popcorn's MCP server lets your assistant work on your Routines for you.
concepts: [add-the-mcp-server, app-bundle, versions, copying-a-template]
---

## Connect your assistant

The server's address is `https://mcp.popcorn.ai/mcp`. [Add the MCP
server](https://docs.popcorn.ai/add-the-mcp-server.md) has the steps for
Claude, Claude Code and other assistants, from signing in and choosing a
Workspace to checking the connection.

## What your assistant can do

- **Start a Routine.** List the [Routine
  Templates](https://docs.popcorn.ai/routines.md) and create a Routine from
  one, or duplicate a Routine you already have.
- **Set it up.** See what it still needs, make its
  [Connections](https://docs.popcorn.ai/connections.md) and add its
  [References](https://docs.popcorn.ai/reference-documents.md).
- **Run it.** See what starts its work and run a
  [Trigger](https://docs.popcorn.ai/triggers.md) now, follow or stop a Run,
  and take an [Action](https://docs.popcorn.ai/actions-and-status.md) on an
  Item.
- **Read and change its data.** Read its
  [Tables](https://docs.popcorn.ai/tables.md), and add, change or delete
  Rows.
- **Follow along.** Read where its Items stand, an Item's
  [History](https://docs.popcorn.ai/history.md) and the Routine's messages.
- **Change how it behaves.** Configure its [Routine
  Settings](https://docs.popcorn.ai/routine-settings.md) and
  [Instructions](https://docs.popcorn.ai/instructions.md), or change its
  [Steps](https://docs.popcorn.ai/steps.md).
- **Customize its template.** Read the files of its Routine Template, make
  a [Copy](https://docs.popcorn.ai/copying-a-template.md), and publish and
  install a new [Version](https://docs.popcorn.ai/versions.md).
- **Look things up.** Find people in the Workspace, and search and read
  these docs.

## How every tool behaves

- **One Workspace.** The connection is bound to one Workspace, and every
  response starts with its name. To use another, reconnect.
- **Your permissions.** Every call runs as the person who connected the
  server, and can do only what they can.
- **`routine` or `routine_id`.** A tool that reads takes a Routine's
  `#name` or its ID as `routine`. A tool that writes takes the ID only, as
  `routine_id`.
- **Dry runs.** A tool marked `[dry run]` shows what it would do, and does
  it when called again with `confirm=true`. Some act at once when the
  person asked for exactly that, such as an Action on Items they named.
  Each tool's page says which.
- **Paging.** A listing returns one page and a `next_cursor`. Pass it back
  with the same arguments for the next page.
- **Other names.** The CLI and the API call a Routine a *channel*, and its
  Routine Template's code an *app*.

## Docs as Resources

These docs are also MCP Resources, for an assistant that lets you attach
one to a conversation. `popcorn://docs/index` lists every page, and
`popcorn://docs/<id>` is one page, such as
`popcorn://docs/mcp/tools/get-status`.

## Reading the tool pages

- **Badges.** `[read-only]`, or `[writes]` with `[destructive]` or
  `[idempotent]`, are the hints the server declares to your assistant's
  app, which may use them to decide what to ask before a call.
- **Arguments.** One marked `[required]` must be passed. Any other may be
  left out.
- **Examples.** Some tools show a request a person might make, each call
  an assistant makes for it, marked `→`, and what the tool returns. The
  response is the server's real output for sample data, the Workspace
  Acme, produced by its tests. It leaves out the Workspace line, shortens
  IDs as `8c1f…e2`, and keeps the first rows of a long listing.

The tool pages are generated from the server's own definitions after each
prod deploy, and never edited by hand.

