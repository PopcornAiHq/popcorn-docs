---
id: history
title: History
order: 12
group: What people do, and what happened
summary: >
  A Routine's History is what has happened in it — did the reminders go out,
  why was this claim closed: the work it ran and how each run ended, the
  conversation in it, and the changes to its items, with who or what made each
  one. People read it in Popcorn. An assistant sees when each item was created
  and last changed; no assistant tool reads runs or the conversation yet.
concepts: [actions-and-status, triggers, tables]
layer: product
---

A Routine's **History** is what has happened in it:

- **its work** — each run, what started it, and how it ended;
- **its conversation** — the messages people and its agent posted in it;
- **changes to its items** — what changed on a Row, and who or what changed
  it.

History answers "did the reminder go out?", "why is this claim closed?" and
"what did the agent say to the carrier?".

## Where it lives today

People read a Routine's work and conversation in Popcorn. When an assistant
runs a schedule or takes an Action, the response says the work runs in the
background and that Popcorn shows how it ended.

## What an assistant can do with it

`get_row` shows when an item was created and last changed, and
`list_rows` lists items newest first. An assistant cannot yet read a
Routine's runs, its conversation, or the history of one item's changes.

## What the assistant tools would need to show

These pages describe the present, so this section is a design input, not a
promise: nothing depends on it arriving. A tool for History would need one
timeline, newest first, that mixes work, conversation and changes, each entry
with who or what made it; narrowing to one kind, one item or a time; and one
entry in full: a run's steps and result, a message and its replies, or a
change's before and after. The MCP reference's
[proposed tools](https://docs.popcorn.ai/product/reference/mcp.md) sketch `list_history` and
`read_history_entry`.

> **Platform note** — A run is a *flow run*, and the CLI reads runs today.
> See [debugging a failed run](https://docs.popcorn.ai/platform/guides/debugging-a-failed-run.md).
