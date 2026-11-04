---
id: set-up-a-routine
title: Set up your first Routine
order: 2
group: Getting started
summary: >
  Setting up a new Routine from the Questionnaire template: pick a template
  with list_routine_templates, create the Routine with create_routine, wait
  for its template to install, make its Connections with make_connection,
  add its References with add_reference, check what's left with get_setup,
  add a first recipient with create_rows, then see what starts its work with
  list_triggers.
lede: >
  Ask your AI assistant to set up a Routine from a template, make its
  Connections and check it's ready to run.
concepts: [routines, connections, triggers]
---

This guide sets up a Routine called `#team-offsite` from the Questionnaire
template, to ask everyone coming to a team offsite a few questions before
it: dietary needs, travel dates and the sessions they want. It emails each
person the questions, records their answers from the replies, and follows
up until they've answered. Each step starts with a prompt you might give
your assistant.

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
> Your assistant calls `create_routine`.

In your request:

- **Private or open.** A private Routine is joined only by you and the
  people you name, whereas an open one adds everyone in the Workspace.
- **The name.** Spaces become hyphens, and a name already used in the
  Workspace is refused.

Your assistant creates the Routine and tells you the Version that's
installing, its Members, and the Connections to set up before it runs.

## Wait for the install

> "Has #team-offsite finished installing?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine` with `wait_seconds` until its
> **Install** field says `installed`.

Popcorn installs the Routine's template in the background, usually within
seconds. Wait for it to finish before making the Routine's Connections.

## Make its Connections

> "What does #team-offsite need connected?"

> [!TIP] MCP tool call
> Your assistant calls `list_connections`.

Your assistant lists the Routine's Connections and how each one is used.
`#team-offsite` has one: the Gmail its questions are sent from and its
replies are read in.

> "Connect my Gmail to #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `make_connection`.

If you haven't signed in to Google yet, your assistant first gives you a
link to do it. It then lists your Google accounts that can be used for
Gmail. Pick one and confirm, and it connects that account to the Routine.

> [!NOTE] A teammate's or shared inbox
> A Connection signs in as the person who makes it, so you can only connect
> your own accounts. To use a teammate's inbox, they connect it themselves;
> for a shared inbox, whoever can sign in to it does.

> [!WARNING] A missing Connection stops work
> Work that uses a missing Connection can't run. Some Connections, such as
> Gmail here, hold back the whole Routine.

## Add its References

> "Add our offsite questions to #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `add_reference`.

A Questionnaire Routine needs one Reference: the questionnaire, a document
listing the questions to ask, or a sample email with them in it. Your
assistant adds it from text or a file, after showing you what it will add.
Popcorn then reads the questions out of it, and the subject and opening
line for the email if it has them. A document with no questions in it
doesn't load, and Popcorn says no questions were found. See
[References](https://docs.popcorn.ai/reference-documents.md).

## Check what's left

> "What's left to set up on #team-offsite?"

> [!TIP] MCP tool call
> Your assistant calls `get_setup`.

Your assistant reads the Routine's setup checklist: each step done or left,
which are required, and what each one left needs. `#team-offsite` has two,
both required: connect Gmail, and add the questionnaire. When neither is
left, the Routine is ready.

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
