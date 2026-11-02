---
id: platform-tools
title: Platform tools
order: 8
group: What a Bundle holds
summary: >
  A Bundle's chat agent has only the Flows its agent.yaml maps and the
  Routine's memory, unless it opts in to platform tools under
  platform_tools: — ask_user, set_reminder, show_setup_step,
  workspace_memory_read, and Popcorn's MCP tools by name. Only chat: true
  agents may; an unknown name fails validation.
concepts: [app-bundle, versions, tables]
---

An App Agent is defined under `agents/<name>/` in a Bundle (see
[App Bundles](https://docs.popcorn.ai/app-bundle.md)). What
it can call is decided by its `agent.yaml` and nothing else: nothing a Member
writes, and nothing a tool returns, can add a tool.

## By default

- **Its Flow tools.** Each `tools:` entry maps a tool name to a Flow of the
  same Bundle. A call starts that Flow, pinned to the Version the turn Runs
  under, and returns the Flow's `outputs:`. No Flow is a tool unless an entry
  maps it.
- **Its terminal tool**, when a Flow invokes it headless: the `submit:` tool
  whose accepted call is the agent's result.
- **The Routine's memory**, when Members chat with it (`chat: true`), unless
  it says `memory: false`.

## Opting in to platform tools

A `chat: true` agent may also have tools the platform's own Routine Agents
have, each with the same rules, by naming them:

```yaml
chat: true
platform_tools:
  - ask_user
  - set_reminder
```

| Entry | What the agent gets |
|---|---|
| `ask_user` | A question card for the Members. One card per Run, and the card ends the Run: the answers start the next one. |
| `set_reminder` | `set_reminder` and `cancel_reminder`: one reminder per Routine, which brings this same agent back to the thread later. |
| `show_setup_step` | One of the Routine's unfinished setup steps as a card the Members complete in the conversation. Shares `ask_user`'s one card per Run. |
| `workspace_memory_read` | The memory shell also shows the Workspace's memory, read only. Needs the agent's own memory. |
| `popcorn__<tool>` | One of Popcorn's MCP tools (`popcorn__list_rows`, `popcorn__update_row`, …), acting on this Routine as the Member being answered. Reading the Routine's Tables is the same tools, named one by one: `popcorn__list_tables`, `popcorn__get_table`, `popcorn__list_rows`, `popcorn__get_row`. |
| `popcorn_mcp` | Shorthand for every `popcorn__` tool an agent may have. |

The `popcorn__` tools reach this Routine only, as the Routine's own Agent's
do: naming another Routine is refused before anything of it is read. The
few Workspace-wide ones, such as `popcorn__list_routines`, answer as for the
Member, and still cannot open another Routine.

A headless agent may name none: a Flow that invokes it has no Member to ask,
nothing to come back to and nobody to act as. An agent that has both a
`submit:` and `chat: true` gets its platform tools when Members chat with it,
and none when a Flow invokes it.

## What the Publish checks

The Publish refuses, naming the line: an entry not in the table above, one
written twice, `workspace_memory_read` on an agent without memory, and a
platform tool whose name one of the agent's own tools already takes.

A `popcorn__` tool that changes something after a dry run — running a Flow,
deleting Rows, changing a setting — only goes ahead once the Members confirm
the dry run on an `ask_user` card, in a later Run. Naming one without
`ask_user` is refused, because the agent could never confirm it. The three
tools that change the app itself confirm in their own Run and need no card.

Every tool's definition is sent with every model call, so the Publish also
holds an agent's Flow tools and platform tools together to one size budget.
Name the `popcorn__` tools an agent needs rather than `popcorn_mcp` when it
also maps many Flows. The Publish's dry run lists, for each agent, exactly the
tools it will get and the size of each.
