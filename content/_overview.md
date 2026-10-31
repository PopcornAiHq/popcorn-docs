# Overview

Popcorn is a service that lets you create, configure, and run Routines. A
Routine is an ongoing piece of work that connects to your accounts and works on
your behalf, stopping whenever a human decision is needed.

## Getting started with MCP

To use Popcorn from your own AI assistant, [connect it to Popcorn's
MCP server](https://docs.popcorn.ai/use/guides/connect-your-assistant.md) at
`https://mcp.popcorn.ai/mcp`.

In Claude Code:

```bash
claude mcp add --transport http --scope user popcorn https://mcp.popcorn.ai/mcp
```

Next, [set up a Routine](https://docs.popcorn.ai/use/guides/set-up-a-routine.md) and connect the accounts it needs.

## How a Routine works

A [Routine](https://docs.popcorn.ai/use/concepts/routines.md) is created from a
[Routine Template](https://docs.popcorn.ai/use/concepts/routines.md), which defines its [Tables](https://docs.popcorn.ai/use/concepts/tables.md) for tracking Items,
[Triggers](https://docs.popcorn.ai/use/concepts/triggers.md) for starting work,
and a [Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md)
showing where each Item, such as a new claim or an order, stands.

```diagram
Triggers ──── start work ───▶ ┌─ Routine ───────────────────────┐
schedule, message,            │ its Tables hold the Items       │
document, webhook             │                                 │
                              │ Item ─▶ Step ─▶ Review ─▶ …     │
Connections ── used by ─────▶ │         asks,   a person        │
a mailbox, a calendar         │         follows decides         │
                              │         up                      │
References ─── read by ─────▶ │                                 │
a policy, a price list        └─────────────────────────────────┘
                                   │                 │
                                   ▼                 ▼
                              Status and        History
                              Actions           every change
```

The Routine reaches your accounts through
[Connections](https://docs.popcorn.ai/use/concepts/connections.md) and works
from [References](https://docs.popcorn.ai/use/concepts/reference-documents.md).
Many Routines take each Item through a series of
[Steps](https://docs.popcorn.ai/use/concepts/steps.md), following up until
each has what it needs and stopping for a
[Review](https://docs.popcorn.ai/use/concepts/reviews.md) whenever a person
should decide. Each Item's
[Actions](https://docs.popcorn.ai/use/concepts/actions-and-status.md) move it
forward, and [History](https://docs.popcorn.ai/use/concepts/history.md)
records each change to it.

## When Popcorn fits

Popcorn fits work that repeats for every client and runs through people
outside your team. Each new client, claimant or order needs answers,
documents, a booking or a signature, gathered over days, with follow-ups until
they arrive and someone on your team deciding at the points that matter. For
example:

- a law firm gathering case details and documents before the first consultation
- an accountant collecting client organizers and chasing missing paperwork
- a contractor turning new inquiries into clear job details and estimate requests
- a broker keeping application checklists and client documents in order

It does not fit one-off work. A Routine does the same work again for every
Item it tracks, so a single question or task is one for your assistant on its
own. Nor does it fit work no Routine Template covers yet: you can set up a
Routine from a template and change one, but a new template is not self-serve.

## What you can do

| To | In the Popcorn app | From your assistant | Read |
|---|---|---|---|
| See what needs you | Items at a Review show as needing review | "What's waiting on me?" | [Review what needs you](https://docs.popcorn.ai/use/guides/work-a-routines-items.md) |
| Decide on an Item | press one of its Actions | "Approve that claim." | [Actions and Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md) |
| Change the Steps | tell the Routine's Agent, "Also ask for photos of the damage." | the same request | [Steps](https://docs.popcorn.ai/use/concepts/steps.md) |
| Change one setting | — | "Write the follow-ups as drafts so I can check them." | [Routine Settings](https://docs.popcorn.ai/use/concepts/routine-settings.md) |
| Find out why something happened | — | "Why was this order closed?" | [History](https://docs.popcorn.ai/use/concepts/history.md) |
| Run scheduled work early | — | "Run the morning check now." | [Triggers](https://docs.popcorn.ai/use/concepts/triggers.md) |

From an assistant, anything that changes a Routine is a dry run first: it
shows you what would happen and asks before it goes ahead.

## Building Routine Templates

A Routine is made from a Routine Template: a directory of YAML that gives it
its Tables, [Flows](https://docs.popcorn.ai/build/concepts/flow-grammar.md) and
[Schedules](https://docs.popcorn.ai/build/concepts/schedules.md). When a Routine needs something
no setting reaches, your Workspace takes a
[Copy](https://docs.popcorn.ai/build/concepts/copying-a-template.md) of its template and changes that.

- [Change a Routine Template](https://docs.popcorn.ai/build/guides/template-authoring.md): copy, edit, publish, confirm the Install
- [Copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md): what a Copy costs, and why it is one-way
- [Debug a failed Run](https://docs.popcorn.ai/build/guides/debugging-a-failed-run.md): from a Routine's History to the Step that failed

## Look it up

- [Glossary](https://docs.popcorn.ai/glossary/glossary.md): every term, and the other names the CLI and API use
- [MCP](https://docs.popcorn.ai/reference/mcp.md), [CLI](https://docs.popcorn.ai/reference/cli.md) and [Activities](https://docs.popcorn.ai/reference/activities.md): generated from Popcorn itself

## For agents

Every page has a Markdown twin at the same path, ending `.md` instead of
`.html`; this one is [/index.md](https://docs.popcorn.ai/index.md).
[/llms.txt](https://docs.popcorn.ai/llms.txt) lists every page with its
summary, [/llms-full.txt](https://docs.popcorn.ai/llms-full.txt) holds every
written page in full, and [/chunks.json](https://docs.popcorn.ai/chunks.json)
has one record per page.
