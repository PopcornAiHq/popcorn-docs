---
id: agent
title: The Routine's Agent
order: 6
group: How a Routine works
summary: >
  A Routine's Agent works inside it: it does the Routine's work, follows its
  Instructions, asks before the Steps that need a person, and answers people
  in the Routine. It is not your assistant, which reaches Popcorn through
  the MCP server and acts as you. send_message talks to it, posting as you;
  list_messages reads its answer, which arrives later.
lede: >
  Each Routine has an Agent that does its work and that people talk to, as
  they would a teammate.
concepts: [instructions, routines, members]
---

Every [Routine](https://docs.popcorn.ai/routines.md) has an **Agent**: the
assistant inside it that does its work. It reads what arrives, moves each
[Item](https://docs.popcorn.ai/work-a-routines-items.md) along, writes and
sends the Routine's emails, and answers the people in the Routine as a
teammate would. It follows the Routine's
[Instructions](https://docs.popcorn.ai/instructions.md), and asks a person
before the [Steps](https://docs.popcorn.ai/steps.md) they say need one.

## Your assistant and the Routine's Agent

These guides talk about two assistants, and they are not the same:

| | Your assistant | The Routine's Agent |
|---|---|---|
| **What it is** | Claude, ChatGPT or another assistant you use | part of the Routine, in Popcorn |
| **Where it works** | in your own app, across every Routine you can reach | inside one Routine |
| **Who it acts as** | you, with your permissions | itself, posting as *Popcorn*, the Workspace's bot |
| **How it reaches Popcorn** | the [MCP server](https://docs.popcorn.ai/mcp.md) | it runs there |
| **What starts it** | you asking it | the Routine's [Triggers](https://docs.popcorn.ai/triggers.md), and people's messages |

Your assistant sets Routines up, reads them and changes them for you. The
Routine's Agent does the Routine's work day to day, whether or not anyone is
talking to it.

## Talking to it

> "Ask #team-offsite's Agent whether Jane has answered yet."

> [!TIP] MCP tool call
> Your assistant calls `send_message`, then `list_messages` to read the
> answer.

Your assistant posts your question in the Routine, as you. The Agent answers
a little later, either in a thread under your message or after it, and your
assistant reads the answer back to you.

> [!NOTE] When it answers
> An @mention of the Agent always gets an answer. Most Routines' Agents
> answer most other messages too, but some answer only the ones that need
> it, and a Routine can be set to answer only @mentions. While the Agent is
> busy with a task in the Routine, your message may be passed into that
> task, or wait behind it, instead of getting a reply of its own.

The people in the Routine talk to it the same way, in Popcorn.

## What it remembers

When people tell the Agent a preference or a decision — "add people by
their full name", "ask me before adding anyone outside the company" — it
keeps it,
and acts on it from then on. That is one part of the Routine's Instructions,
and [Instructions](https://docs.popcorn.ai/instructions.md#reading-them) says
how your assistant reads it.

## Changing how it acts

The Agent follows the Routine's Instructions, so changing how it acts means
changing them:

- **Tell it**, in the Routine, for a preference or a decision.
- **Change a Routine Setting**, for the prompts it writes from: see
  [Change how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md).
- **Replace a [Reference](https://docs.popcorn.ai/reference-documents.md)**,
  for wording that comes from one: `#team-offsite`'s emails are worded by
  its questionnaire.
- **Change the Routine's Steps**, in a Routine whose Steps are its own,
  for what each Step asks and when it acts: see
  [Change its Steps](https://docs.popcorn.ai/change-how-a-routine-behaves.md#change-its-steps).

> [!TIP] In the template
> Building a template, the Routine's Agent is its **channel agent**, and a
> template can define Agents of its own.
> [App Bundles](https://docs.popcorn.ai/app-bundle.md) and
> [Platform tools](https://docs.popcorn.ai/platform-tools.md) describe both.
