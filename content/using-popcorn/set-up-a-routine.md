---
id: set-up-a-routine
title: Set up your first Routine
order: 2
group: Getting started
summary: >
  Setting up a new Routine from the Questionnaire template: pick a template
  with list_routine_templates, create the Routine with create_routine and
  wait for its template to install, make its Connections with make_connection,
  add its References with add_reference, check what's left with get_setup,
  add a first recipient with create_rows, then see what starts its work with
  list_triggers.
lede: >
  Ask your AI assistant to set up a Routine from a template, make its
  Connections and check it's ready to run.
concepts: [routines, connections, triggers]
---

This guide walks you through setting up a Routine called `#team-offsite`,
created from the Questionnaire template. The Routine emails each team member
a few questions about the offsite, such as their dietary needs, travel dates
and which sessions they'd like to attend. It records their answers and
follows up with anyone who hasn't answered them all.

Each step below starts with a prompt you might give your assistant.

## Pick a template

> "Which templates can I start a Routine from?"

> [!TIP] MCP tool call
> Your assistant calls `list_routine_templates`.

Your assistant lists the
[Routine Templates](https://docs.popcorn.ai/routines.md) available in your
Workspace, describing what each one does and which
[Connections](https://docs.popcorn.ai/connections.md) it needs. The
Questionnaire template needs only Gmail.

## Create the Routine

> "Create a private #team-offsite Routine from the Questionnaire template."

> [!TIP] MCP tool call
> Your assistant calls `create_routine`, then `get_routine` until its
> **Install** field says `installed`.

In your request:

- **Private or open.** A private Routine is joined only by you and the
  people you name, whereas an open one adds everyone in the Workspace.
- **The name.** Spaces become hyphens, and a name already used in the
  Workspace is refused.

Your assistant creates the Routine and tells you the Version that's
installing, its Members, and the Connections to set up before it runs.
Popcorn installs the template in the background, and your assistant waits
for it to finish, usually within a few seconds.

## Make its Connections

> "What does #team-offsite need connected?"

> [!TIP] MCP tool call
> Your assistant calls `list_connections`.

Your assistant lists the Routine's Connections and what each one does.
`#team-offsite` needs just one, your Gmail, which sends the questions and
reads the replies.

> "Connect my Gmail to #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `make_connection`.

If you haven't signed in to Google yet, your assistant first gives you a
link to do it. Then, if you have one Google account that can be used for
Gmail, it connects that account straight away and tells you which one; if
you have several, it asks which to use.

> [!NOTE] A teammate's or shared inbox
> A Connection signs in as the person who makes it, so you can only connect
> your own accounts. To use a teammate's inbox, they connect it themselves;
> for a shared inbox, whoever can sign in to it does.

> [!WARNING] A missing Connection stops work
> Work that uses a missing Connection can't run. Some Connections, such as
> Gmail here, hold back the whole Routine.

## Add its References

> "Add these offsite questions to #team-offsite:
>
> Subject: A few questions for the offsite
>
> 1. Do you have any dietary needs?
> 2. Which day are you arriving, and how are you travelling?
> 3. Which sessions would you like to attend?"

> [!TIP] MCP tool call
> Your assistant calls `add_reference`, passing the questions as its
> `text`.

The Questionnaire Routine needs one
[Reference](https://docs.popcorn.ai/reference-documents.md), the
questionnaire itself: a subject line for its emails and the questions to ask.

> [!NOTE] From a file
> Some assistants, such as Claude Code, can add the questionnaire from a
> text file instead of pasting it.

## Check what's left

> "What's left to set up on #team-offsite?"

> [!TIP] MCP tool call
> Your assistant calls `get_setup`.

Your assistant reads the Routine's setup checklist and tells you what's left
to do. `#team-offsite` has two required steps, connecting Gmail and adding
the questionnaire, and you've just done both. The Routine is ready.

## Add your first attendee

> "Add jane@example.com to #team-offsite as Jane."

> [!TIP] MCP tool call
> Your assistant calls `create_rows`.

Each person to ask is a row in the Routine's `recipients`
[Table](https://docs.popcorn.ai/tables.md): an email address and, if you
know it, a name. Your assistant shows you the row before adding it. Adding
an address that's already there updates that row, so nobody is asked
twice. To add everyone at once, give your assistant the whole list.

Adding a row doesn't email anyone by itself. The Routine's next Run does,
within fifteen minutes, and marks them Waiting. From then on each Run
reads their replies, records each answer on their row, and follows up on
the questions still open.

> [!TIP] Try it on yourself first
> Add your own address first to see the email everyone will get.
> Or ask your assistant to set the Routine's send mode to drafts, and each
> email waits in your Gmail Drafts for you to send.

## See what starts its work

> "What sets #team-offsite working?"

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, and `run_trigger` to run a Schedule
> now.

Your assistant shows how work arrives: the Routine's Schedules and when they
run, the messages and documents that start work, and any other system that
posts to it. `#team-offsite` has one Schedule, every fifteen minutes, that
asks new recipients, reads replies and follows up.

To email Jane without waiting, ask it to run that Schedule
now. It shows you what will run first, because the work is real. See
[Triggers](https://docs.popcorn.ai/triggers.md).

## Next

To tune how the Routine behaves — how long it waits before following up,
how many follow-ups it sends — see
[changing how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md).
