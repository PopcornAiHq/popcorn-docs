---
id: add-the-mcp-server
title: Add the MCP server
order: 1
group: Getting started
summary: >
  Adding Popcorn's MCP server to an AI assistant: add the hosted server at
  https://mcp.popcorn.ai/mcp (in Claude, a custom connector set to Register
  automatically; in Claude Code, then /mcp), sign in to Popcorn, choose a
  Workspace and Allow, then check it with get_workspace. The assistant acts
  as you, in that Workspace, until you disconnect it. Help:
  support@popcorn.ai.
lede: >
  Allow your AI assistant to find your Routines, see what needs your input
  and act on your behalf through Popcorn's MCP server.
concepts: [mcp, routines, set-up-a-routine]
---

## Connect to Popcorn MCP server

Popcorn MCP server: `https://mcp.popcorn.ai/mcp`

You need a Popcorn account that is a
[Member](https://docs.popcorn.ai/members.md) of a Workspace.

=== "Claude"

    In Claude on the web, at [claude.ai](https://claude.ai), or in the
    Claude desktop app:

    1. Open **Customize** > **Connectors**.
    2. Select **+ Add**, then **Add custom connector**.
    3. Enter `Popcorn` as the name and `https://mcp.popcorn.ai/mcp` as the
       remote MCP server URL, then select **Continue**.
    4. Under **Authentication**, choose **Sign in now**. Under
       **OAuth client**, choose **Register automatically**, then select
       **Add**.

    Claude opens Popcorn in your browser to sign in. Once you have, start
    a new chat, select **+** > **Connectors** and check that Popcorn is on.

    > [!IMPORTANT] Register automatically
    > Popcorn registers each assistant when it connects. With **Use
    > Claude's published identity**, Popcorn answers "Connection expired"
    > instead of asking you to sign in.

    > [!NOTE] Team and Enterprise plans
    > An Owner adds the connector once, in **Organization settings** >
    > **Connectors**. Everyone else finds Popcorn in **Customize** >
    > **Connectors** and selects **Connect**.

    Connectors added this way also work in Claude Cowork and Claude's
    mobile apps. See
    [Claude's help](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
    for details.

=== "Claude Code"

    ```bash
    claude mcp add --transport http --scope user popcorn https://mcp.popcorn.ai/mcp
    ```

    Then run `/mcp` in Claude Code and choose **popcorn** to sign in.

=== "ChatGPT"

    See [OpenAI's help](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)
    for details.

## Sign in and choose a Workspace

In your browser, Popcorn asks you to allow your assistant. Sign in if
prompted, choose your Workspace, then select **Allow**. If you didn't start
this from your assistant, select **Deny**.

> [!NOTE] Not a Member of a Workspace
> Popcorn connects an assistant only to a Workspace you're a Member of. If
> it says your email isn't a Member of any, ask a Workspace admin for an
> invite, or select **Switch account** and sign in with another.

> [!NOTE] One Workspace at a time
> Popcorn's MCP server works in one Workspace at a time. To use a different
> Workspace, disconnect and sign in to choose again.

## Confirm it works

Ask your assistant:

> "Which Popcorn Workspace are you connected to?"

It should name the Workspace you chose.

> [!TIP] MCP tool call
> Most assistants show the tool calls they make, sometimes inside their
> reasoning or a details view. Look for Popcorn's `get_workspace`.

## It acts as you

Every MCP tool call runs on your behalf with your permissions. A message it
sends is yours, and Popcorn's web and desktop apps mark it with a small robot
on your picture, labelled "Sent by *your name*'s agent through Popcorn's
connection", so people can tell it from one you typed.

What you ask for exactly happens at once, such as taking an
[Action](https://docs.popcorn.ai/actions-and-status.md) on Items you name.
Anything else comes back as a dry run for you to check first, and so does
anything that can't be undone or a setting that carries a warning, such as
switching to sending email without review. The
[MCP server overview](https://docs.popcorn.ai/mcp.md) lists which tools do
this.

> [!NOTE] Signing out ends access
> Signing out of Popcorn disconnects every assistant you've added. To carry
> on, sign in again from each one.

## Get help

If connecting doesn't work, or your assistant can't reach Popcorn, email
[support@popcorn.ai](mailto:support@popcorn.ai). Say which assistant you
use and what it showed.
