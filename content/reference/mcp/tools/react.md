---
id: mcp/tools/react
title: react
order: 339
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  Add an emoji reaction to a Routine message, or take yours off with
  remove=true.
concepts: []
---

[writes] [idempotent]

```
react(emoji, message_id=None, remove=False)
```

You react as yourself; the Routine's own agent reacts as itself (its bot user), never as the member it is serving. Adding one that's already there, or removing one that isn't, succeeds and changes nothing.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `emoji` [required] | `str` | A Unicode emoji, e.g. "👍". |
| `message_id` | `str` | The message's ID. The Routine's own agent may leave it out for the message it is answering. |
| `remove` | `bool` | Take your reaction off instead of adding it. Default `False`. |

**Example** — “Give the agent's answer on claim 4471 a thumbs up, and take my 👀 off the question.”

```text
→ react(message_id="9a3c…19", emoji="👍")

Reacted 👍 to message 9a3c…19.

→ react(message_id="7e1a…47", emoji="👀", remove=true)

Removed your 👀 from message 7e1a…47.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
