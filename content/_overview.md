# Overview

Popcorn is a service that uses AI agents to carry out ongoing work, such as
client intake and delivery coordination. Each piece of that work is a Routine,
which works through the accounts you already use and from documents such as
your policies and price lists.

## Start here

To use Popcorn from your own AI assistant, connect it to Popcorn's MCP server
at `https://mcp.popcorn.ai/mcp`.

In Claude Code:

```bash
claude mcp add --transport http --scope user popcorn https://mcp.popcorn.ai/mcp
```

1. [Connect your assistant](https://docs.popcorn.ai/use/guides/connect-your-assistant.md): add the server in any client, sign in, and check the connection
2. [Set up a Routine](https://docs.popcorn.ai/use/guides/set-up-a-routine.md): pick a template, create the Routine, and connect the accounts it needs

## How a Routine works

A [Routine](https://docs.popcorn.ai/use/concepts/routines.md) is created from
a Routine Template, which defines its [Tables](https://docs.popcorn.ai/use/concepts/tables.md) for tracking items,
[Triggers](https://docs.popcorn.ai/use/concepts/triggers.md) for starting work,
and a [Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md)
showing where each item stands.

```diagram
Triggers ──── start work ───▶ ┌─ Routine ───────────────────────┐
schedule, message,            │ its Tables hold the items       │
document, webhook             │                                 │
                              │ item ─▶ Step ─▶ Review ─▶ …     │
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
Many Routines take each item through a few
[Steps](https://docs.popcorn.ai/use/concepts/steps.md): the Routine asks for
what each one needs, follows up until it has it, and stops at a
[Review](https://docs.popcorn.ai/use/concepts/reviews.md) wherever a person
on your team should decide. Each item's
[Actions](https://docs.popcorn.ai/use/concepts/actions-and-status.md) move it
on, and [History](https://docs.popcorn.ai/use/concepts/history.md) records who
changed what, and why.

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
item it tracks, so a single question or task is one for your assistant on its
own. Nor does it fit work no Routine Template covers yet: you can set up a
Routine from a template and change one, but a new template is not self-serve.

## What you can ask

Anything that changes a Routine is a dry run first: the assistant shows you
what would happen and asks before it goes ahead.

| Ask your assistant | What it does | Read |
|---|---|---|
| "What's waiting on me?" | lists the items at a Review, and why | [Review what needs you](https://docs.popcorn.ai/use/guides/work-a-routines-items.md) |
| "Approve that claim." | takes the Action, as its button would | [Actions and Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md) |
| "Write the follow-ups as drafts so I can check them." | changes one Routine Setting | [Routine Settings](https://docs.popcorn.ai/use/concepts/routine-settings.md) |
| "Also ask for photos of the damage." | proposes a change to the Steps | [Steps](https://docs.popcorn.ai/use/concepts/steps.md) |
| "Why was this order closed?" | reads the item's History | [History](https://docs.popcorn.ai/use/concepts/history.md) |
| "Run the morning check now." | runs a scheduled Trigger early | [Triggers](https://docs.popcorn.ai/use/concepts/triggers.md) |

## Building Routine Templates

A Routine is made from a Routine Template: a directory of YAML that gives it
its Tables, flows and schedules. When a Routine needs something no setting
reaches, your workspace takes a copy of its template and changes that.

- [Change a Routine Template](https://docs.popcorn.ai/build/guides/template-authoring.md): copy, edit, publish, confirm the install
- [Copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md): what a copy costs, and why it is one-way
- [Debug a failed run](https://docs.popcorn.ai/build/guides/debugging-a-failed-run.md): from a Routine's History to the step that failed

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
