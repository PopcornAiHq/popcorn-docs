# Overview

Popcorn is a service that lets you create, configure and run Routines. A
Routine connects to your accounts and works on your behalf, stopping whenever a
human decision is needed.

## Getting started with MCP

To use Popcorn from your own AI assistant, [connect it to Popcorn's MCP
server](https://docs.popcorn.ai/connect-your-assistant.md) at
`https://mcp.popcorn.ai/mcp`.

In Claude Code:

```bash
claude mcp add --transport http --scope user popcorn https://mcp.popcorn.ai/mcp
```

Next, [set up a
Routine](https://docs.popcorn.ai/set-up-a-routine.md) and connect
the accounts it needs.

## Anatomy of a Routine

A [Routine](https://docs.popcorn.ai/routines.md) is created from a
Routine Template, which defines
[Tables](https://docs.popcorn.ai/tables.md) for tracking Items,
[Triggers](https://docs.popcorn.ai/triggers.md) for starting work,
and [Actions](https://docs.popcorn.ai/actions-and-status.md) for
updating an Item's Status. An Item is one thing the Routine tracks, such as a
potential client for a law firm or a purchase order waiting on a vendor.

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

Through [Connections](https://docs.popcorn.ai/connections.md) and
[References](https://docs.popcorn.ai/reference-documents.md), a
Routine moves each Item through a series of
[Steps](https://docs.popcorn.ai/steps.md), stopping for a
[Review](https://docs.popcorn.ai/reviews.md) whenever a person is
needed, logging each change to its
[History](https://docs.popcorn.ai/history.md).

## Using Routines

Work with Routines by asking your AI assistant in your own words.

| You want to | Ask your assistant |
|---|---|
| [See what needs you](https://docs.popcorn.ai/work-a-routines-items.md) | "What's waiting on me?" |
| [Make a decision](https://docs.popcorn.ai/actions-and-status.md) | "Mark the new client's agreement as already signed." |
| [Add a Step](https://docs.popcorn.ai/steps.md) | "Check with me before their consultation is booked." |
| [Update a Routine Setting](https://docs.popcorn.ai/routine-settings.md) | "Write the follow-ups as drafts so I can check them." |
| [Find out why something happened](https://docs.popcorn.ai/history.md) | "Why was this order closed?" |
| [Run scheduled work early](https://docs.popcorn.ai/triggers.md) | "Send today's follow-ups now." |

## Building Routine Templates

Most Routines can be configured through their Routine Settings. For advanced
use cases, you can copy a Routine Template and modify it.

- [Change a Routine Template](https://docs.popcorn.ai/template-authoring.md): copy, edit, publish, confirm the Install
- [Copying a template](https://docs.popcorn.ai/copying-a-template.md): what a Copy costs, and why it is one-way
- [Debug a failed Run](https://docs.popcorn.ai/debugging-a-failed-run.md): from a Routine's History to the Step that failed

## Look it up

- [Glossary](https://docs.popcorn.ai/glossary.md): comprehensive list of Popcorn terms
- [MCP](https://docs.popcorn.ai/mcp.md), [CLI](https://docs.popcorn.ai/cli.md) and [Activities](https://docs.popcorn.ai/activities.md): generated from Popcorn itself

## For agents

Every page has a Markdown twin at the same path, ending `.md` instead of
`.html`; this one is [/index.md](https://docs.popcorn.ai/index.md).
[/llms.txt](https://docs.popcorn.ai/llms.txt) lists every page with its
summary, [/llms-full.txt](https://docs.popcorn.ai/llms-full.txt) holds every
written page in full, and [/chunks.json](https://docs.popcorn.ai/chunks.json)
has one record per page.
