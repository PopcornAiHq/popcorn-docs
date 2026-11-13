---
id: mcp
title: MCP server overview
order: 300
group: MCP
summary: >
  The hosted Popcorn MCP server, at https://mcp.popcorn.ai/mcp, gives a
  person's assistant tools for their Routines, and its docs as Resources. This
  page says what the tools do, the one Workspace a connection works in, and
  how to attach a docs page. Adding the server and the list of tools have
  pages of their own.
lede: >
  Popcorn's MCP server lets your assistant work on your Routines for you.
concepts: [add-the-mcp-server, app-bundle, versions, copying-a-template]
---

## Connect your assistant

The server's address is `https://mcp.popcorn.ai/mcp`. [Add the MCP
server](https://docs.popcorn.ai/add-the-mcp-server.md) has the steps.

> [!NOTE] One Workspace at a time
> Every call runs as you, with your permissions, in the one Workspace the
> connection is bound to. Each response shows the current Workspace's name.
> To use another, disconnect and sign in again to choose it.

## Tools

The [Tools](https://docs.popcorn.ai/mcp/tools.md) page lists every tool and
what they share.

Some things your assistant can do:

- **Start a Routine:** from a
  [Routine Template](https://docs.popcorn.ai/routines.md), or by duplicating
  one.
- **Set it up:** make its [Connections](https://docs.popcorn.ai/connections.md)
  and add its [References](https://docs.popcorn.ai/reference-documents.md).
- **Run it:** run a [Trigger](https://docs.popcorn.ai/triggers.md), follow a
  Run, or take an [Action](https://docs.popcorn.ai/actions-and-status.md) on
  an Item.
- **Work with its data:** read and change its
  [Tables](https://docs.popcorn.ai/tables.md), and read an Item's
  [History](https://docs.popcorn.ai/history.md) and the Routine's messages.
- **Take part in an [Agent Chat](https://docs.popcorn.ai/agent-chat.md):**
  check in on what waits on you, and post what you're working on.
- **Change how it works:** its
  [Routine Settings](https://docs.popcorn.ai/routine-settings.md),
  [Instructions](https://docs.popcorn.ai/instructions.md) and
  [Steps](https://docs.popcorn.ai/steps.md), or a
  [Copy](https://docs.popcorn.ai/copying-a-template.md) of its template.

## Resources

Your assistant can read these docs with the `search_docs` and `read_doc`
tools. Every page is also an MCP Resource, so an assistant that lets you
attach one can add a page to the conversation.

> [!TIP] In Claude Code
> Type `@popcorn:` and pick a page, such as
> `@popcorn:popcorn://docs/set-up-a-routine`.
