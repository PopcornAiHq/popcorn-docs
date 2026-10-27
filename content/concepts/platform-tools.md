---
id: platform-tools
title: Platform tools
order: 9
group: What a bundle holds
summary: >
  A bundle's chat agent has only the flows its agent.yaml maps and the
  channel's memory, unless it opts in to platform tools under
  platform_tools: — ask_user, set_reminder, show_setup_step,
  workspace_memory_read, and Popcorn's MCP tools by name. Only chat: true
  agents may; an unknown name fails validation.
concepts: [app-bundle, publish-and-apply, channel-binding]
layer: platform
product_terms: [Agent]
---

An app agent is defined under `agents/<name>/` in a bundle (see
[App bundles](https://docs.popcorn.ai/platform/concepts/app-bundle.md)). What
it can call is decided by its `agent.yaml` and nothing else: nothing a member
writes, and nothing a tool returns, can add a tool.

## By default

- **Its flow tools.** Each `tools:` entry maps a tool name to a flow of the
  same bundle. A call starts that flow, pinned to the version the turn runs
  under, and returns the flow's `outputs:`. No flow is a tool unless an entry
  maps it.
- **Its terminal tool**, when a flow invokes it headless: the `submit:` tool
  whose accepted call is the agent's result.
- **The channel's memory**, when members chat with it (`chat: true`), unless
  it says `memory: false`.

## Opting in to platform tools

A `chat: true` agent may also have tools the platform's own channel agents
have, each with the same rules, by naming them:

```yaml
chat: true
platform_tools:
  - ask_user
  - set_reminder
```

| Entry | What the agent gets |
|---|---|
| `ask_user` | A question card for the members. One card per run, and the card ends the run: the answers start the next one. |
| `set_reminder` | `set_reminder` and `cancel_reminder`: one reminder per channel, which brings this same agent back to the thread later. |
| `show_setup_step` | One of the channel's unfinished setup steps as a card the members complete in the conversation. Shares `ask_user`'s one card per run. |
| `workspace_memory_read` | The memory shell also shows the workspace's memory, read only. Needs the agent's own memory. |
| `popcorn__<tool>` | One of Popcorn's MCP tools (`popcorn__list_rows`, `popcorn__update_row`, …), acting on this channel as the member being answered. |
| `tables_read` | Shorthand for this channel's tables, read only: `popcorn__list_tables`, `popcorn__get_table`, `popcorn__list_rows`, `popcorn__get_row`. |
| `popcorn_mcp` | Shorthand for every `popcorn__` tool an agent may have. |

A headless agent may name none: a flow that invokes it has no member to ask,
nothing to come back to and nobody to act as. An agent that has both a
`submit:` and `chat: true` gets its platform tools when members chat with it,
and none when a flow invokes it.

## What the publish checks

The publish refuses, naming the line: an entry not in the table above, one
written twice, `workspace_memory_read` on an agent without memory, and a
platform tool whose name one of the agent's own tools already takes.

A `popcorn__` tool that changes something after a dry run — running a flow,
deleting rows, changing a setting — only goes ahead once the members confirm
the dry run on an `ask_user` card, in a later run. Naming one without
`ask_user` is refused, because the agent could never confirm it. The three
tools that change the app itself confirm in their own run and need no card.

Every tool's definition is sent with every model call, so the publish also
holds an agent's flow tools and platform tools together to one size budget.
Name the `popcorn__` tools an agent needs rather than `popcorn_mcp` when it
also maps many flows. The publish's dry run lists, for each agent, exactly the
tools it will get and the size of each.
