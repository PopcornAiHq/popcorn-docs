---
id: connect-your-assistant
title: Connect your assistant
order: 1
group: Getting started
summary: >
  Connecting an assistant to Popcorn: add the hosted MCP server at
  https://mcp.popcorn.ai/mcp, sign in to Popcorn and choose a workspace, then
  check the connection with get_workspace. The assistant works with your
  permissions, in that workspace, until you disconnect it or sign out of
  Popcorn.
lede: >
  Connect your AI assistant to Popcorn so it can work with your Routines,
  using your own permissions.
concepts: [routines, connections, reviews]
part: use
---

An assistant connected to Popcorn can find your Routines, see where their
items stand, decide at their Reviews, change their settings and
start new ones. It does this through Popcorn's hosted MCP server. This guide
connects one and checks it.

## 1. Add the server

The server's address is `https://mcp.popcorn.ai/mcp`.

- **Claude, on the web or the desktop app**: in Claude's settings, add a
  custom connector with that address.
- **Claude Code**: run
  `claude mcp add --transport http --scope user popcorn https://mcp.popcorn.ai/mcp`.
  Or install the Popcorn plugin, which adds the server along with a skill for
  working in Popcorn: `/plugin marketplace add PopcornAiHq/popcorn-claude-code`,
  then `/plugin install popcorn@popcorn`.

Any other assistant that connects to remote MCP servers with sign-in uses the
same address.

## 2. Sign in and choose a workspace

The assistant opens Popcorn's sign-in. After you sign in, a consent page
names the assistant and asks you to allow it. If you belong to more than one
workspace, you choose one there.

The connection stays bound to that workspace. To use another, disconnect and
connect again.

## 3. Check it

> "Which Popcorn workspace are you connected to?"

The assistant calls `get_workspace`. Every response from the server also
starts with the workspace's name, so the assistant always knows where it is
working.

## Whose permissions it uses

Every call runs as you, with your permissions: the assistant sees the
Routines you can see and changes what you could change. Anything that
changes a Routine, such as taking an Action, changing a setting or starting a
new Routine, is a dry run first. The assistant shows you what would happen
and asks before it goes ahead.

Signing out of Popcorn ends every assistant connection you have made. Connect
again to carry on.

## What stays in Popcorn

Some things are done in Popcorn itself, not through an assistant:

- **A Connection**, such as the mailbox a Routine sends from,
  because it signs in as you. An assistant can say which
  [Connections](https://docs.popcorn.ai/use/concepts/connections.md) a Routine is missing.
- **Reading or posting a Routine's messages**, and seeing its runs.
- **Changing a Routine's [Steps](https://docs.popcorn.ai/use/concepts/steps.md) or
  [Instructions](https://docs.popcorn.ai/use/concepts/instructions.md)**, by telling its
  agent.
- **Choices that open a form**, such as sending an agreement whose fields a
  person checks first.

Next: [setting up a Routine](https://docs.popcorn.ai/use/guides/set-up-a-routine.md).
