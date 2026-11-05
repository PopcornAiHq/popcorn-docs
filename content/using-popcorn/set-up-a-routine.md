---
id: set-up-a-routine
title: Set up your first Routine
order: 2
group: Getting started
summary: >
  Setting up a Routine from the Questionnaire template: pick it with
  list_routine_templates, create it with create_routine, check what's left
  with get_setup, connect Gmail with make_connection, add the questionnaire
  with add_reference, set the reply-by date with complete_setup_step, add a
  recipient with create_rows, find what starts its work with list_triggers,
  and read the replies with list_rows.
lede: >
  Ask your AI assistant to set up a Routine from a template, make its
  Connections and check it's ready to run.
concepts: [routines, connections, reference-documents, tables, triggers]
---

This guide walks you through setting up a Routine called `#team-offsite`,
created from the Questionnaire template. The Routine emails each team member
a few questions about the offsite, such as their dietary needs, travel dates
and which sessions they'd like to attend. It records their answers and
follows up with anyone who hasn't answered them all.

Each step below starts with a prompt you might give your assistant.

## Pick a Routine Template

> "Which templates can I start a Routine from?"

> [!TIP] MCP tool call
> Your assistant calls `list_routine_templates`.

Your assistant lists the
[Routine Templates](https://docs.popcorn.ai/routines.md) available in your
Workspace. It describes what each one does and which
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
Installing usually takes a few seconds, and your assistant waits for it to
finish.

## See what it needs

> "What does #team-offsite need before it can run?"

> [!TIP] MCP tool call
> Your assistant calls `get_setup`.

Your assistant reads the Routine's setup checklist and tells you what's
needed. `#team-offsite` has three required steps: connecting Gmail, adding
the questionnaire [Reference](https://docs.popcorn.ai/reference-documents.md)
and setting the reply-by date. The next three sections take them in turn.

## Connect Gmail

> "Connect my Gmail to #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `make_connection`.

`#team-offsite` uses Gmail to send questions and read replies. If you
haven't signed in to Google yet, your assistant gives you a link to sign in.

If you have only one Google account, your assistant connects it straight
away. If you have more than one, it asks which one to use.

> [!NOTE] A teammate's or shared inbox
> A Connection signs in as the person who makes it, so you can only connect
> your own accounts. To use a teammate's inbox, they connect it themselves.
> For a shared inbox, anyone who can sign in to it can connect it.

> [!WARNING] A missing Connection stops work
> Work that uses a missing Connection can't run. Some Connections, such as
> Gmail here, hold back the whole Routine.

## Add the questionnaire Reference

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

The questionnaire gives the Routine a subject line for its emails and the
questions to ask.

> [!NOTE] From a file
> Some assistants, such as Claude Code, can add the questionnaire from a
> text file instead of pasting it.

## Set the reply-by date

> "Set #team-offsite's reply-by date to 14 November."

> [!TIP] MCP tool call
> Your assistant calls `complete_setup_step`.

The Routine asks for replies by this date in every email it sends. Once the
date passes, it stops following up and marks anyone who hasn't answered as
*No response*.

Your assistant confirms the date and tells you setup is complete. The
Routine is ready.

## Add a Row

> "Add jane@example.com to #team-offsite as Jane."

> [!TIP] MCP tool call
> Your assistant calls `create_rows`.

Jane is added as a Row in the Routine's `recipients`
[Table](https://docs.popcorn.ai/tables.md), with her email address and name.
Her email goes out on the Routine's next Run, which the next section covers.

Each email address appears once in the Table, so adding one that's already
there updates its Row instead. To add everyone at once, give your assistant
the whole list.

> [!TIP] Use drafts mode
> To check each email before it goes out, ask your assistant to set
> `#team-offsite`'s send mode to drafts. Each email then waits in your Gmail
> Drafts for you to review and send. Set it back to send once you're happy
> with them.

## See what starts its work

> "What sets #team-offsite working?"

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`.

Your assistant shows how work arrives: the Routine's Schedules and when they
run, the messages and documents that start work, and any other system that
posts to it.

`#team-offsite` has one Schedule that runs every fifteen minutes. Each
Run emails anyone new, such as Jane, and marks them *Waiting*. It then reads
replies, records the answers on each Row, and follows up on any questions
still open. Replacing the questionnaire also starts work, reading in the new
questions.

> "Run that Schedule now."

> [!TIP] MCP tool call
> Your assistant calls `run_trigger`.

Your assistant runs it straight away, with the same work as a scheduled
Run, so Jane is emailed within a minute instead of at the next
quarter-hour. See [Triggers](https://docs.popcorn.ai/triggers.md).

## See the replies

> "Who has replied on #team-offsite so far?"

> [!TIP] MCP tool call
> Your assistant calls `list_rows`.

Your assistant lists each person's Row in the `recipients` Table, with their
Status and the answers recorded so far. Someone who has answered every
question is *Answered*. Anyone still *Waiting* gets a follow-up about the
questions they left open, until the reply-by date.

## Change how it behaves

To tune how long `#team-offsite` waits before following up, or how many
follow-ups it sends, see
[changing how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md).
