---
id: set-up-a-routine
title: Set up your first Routine
order: 2
group: Getting started
summary: >
  Setting up a Routine from a Routine Template: pick a template with
  list_routine_templates, create the Routine with create_routine (a dry run
  first), wait for its template to install, make its Connections with
  make_connection, add its References with add_reference, check what's left
  with get_setup, then see what starts its work with list_triggers.
lede: >
  Ask your AI assistant to set up a Routine from a template, connect what it
  needs and check it's ready to run.
concepts: [routines, connections, triggers]
---

This guide starts from "we need a Routine for this" and ends with a Routine
whose [Connections](https://docs.popcorn.ai/connections.md) are made and
whose work is ready to start. Every step is something a person can ask their
assistant for, and the assistant does it through the Popcorn MCP server. A
person still signs in to their own accounts, and a few things are done in
Popcorn; the assistant's answer says which.

The example sets up a private Routine for western-region claims, called
`#claims-west`, from the Chase template, whose
[Steps](https://docs.popcorn.ai/steps.md) start as a claims intake: questions, a
Review, then the retainer.

> [!TIP] Or describe it in Popcorn
> **New routine** in Popcorn takes a sentence such as "ask new clients a few
> questions, then send them a retainer", or an example to start from, and the
> new Routine's Agent drafts its Steps from it for the person to check.
> Popcorn can also suggest Routines from a connected inbox. Both create the
> Routine from the Chase template, so this guide applies from "Wait for the
> template to install".

## Pick a template

> "What templates could a new Routine here start from?"

`list_routine_templates` lists the Routine Templates this Workspace can
start from: each one's name, its slug, what it does, and the Connections it
needs before it runs. A template the Workspace cannot run is not listed. Note
the slug — `chase` here — and the Connections: Gmail, Google Calendar, Google
Drive, an intake Webhook and E-signature.

## Create the Routine

> "Set up a private #claims-west Routine from the Chase template, with
> Jordan in it."

`create_routine` with a `template` is a dry run first. It names the
Version that will install, the Members, and the Connections someone sets up
before the Routine runs, and changes nothing. Read it back to the person, then
call again with `confirm=true`.

- **Private or open.** A private Routine is joined only by you and the
  people you name; one that is not private adds everyone in the Workspace.
- **The name.** Spaces become hyphens, and a name already used in the
  Workspace is refused with the ID of the Routine that has it.

> [!TIP] Use its ID
> The response gives the new Routine's ID. Use the ID, not the name, in every
> call that changes it.

## Wait for the template to install

> "Is #claims-west ready?"

The template installs in the background once the Routine exists, usually in
seconds. `get_routine` with `wait_seconds` (up to 20) waits for it. Its
**Install** field says `installed` when the template has landed. Until then
the Routine exists but has nothing to run.

## Make its Connections

> "Connect my Google account to #claims-west."

`list_connections` shows each Connection the Routine needs, whose account it
uses, and what stops while it is missing. `make_connection` makes one, a dry
run first, then with `confirm=true`:

- **An account.** It lists the person's own accounts that can serve the
  Connection. One Google account fills Gmail, Google Calendar and Google
  Drive together. A Connection signs in as a person, so only their own
  accounts can be connected, and a teammate connects theirs. For a Google
  account not yet signed in to, it hands back a sign-in link to pass on.
- **The intake Webhook.** It makes the Webhook and answers with its address,
  once. The address is a credential: give it only to whoever sets up the
  system that posts to it.
- **E-signature.** Not made here: a Workspace admin or owner saves its
  Signing Provider's keys in Popcorn.

> [!WARNING] A missing Connection stops work
> Work that uses a missing Connection cannot run. Some hold the whole
> Routine back, and Popcorn shows it as not ready.

## Add its References

> "Add our intake questions to #claims-west."

A Chase Routine needs its sample email before its first Step can ask
anything, and its agreement before it can send one. `add_reference` adds a
Reference from text or an uploaded file, a dry run first; one picked from
Google Drive is picked in Popcorn instead. See
[References](https://docs.popcorn.ai/reference-documents.md).

## Check what's left

> "What's left to set up on #claims-west?"

`get_setup` reads the Routine's setup checklist: each step done or left,
which are required, and what each one left needs, such as a Connection or a
value set in the Routine's Today tab. When nothing required is left, the
Routine is ready.

## See what starts its work

> "What sets #claims-west working?"

`list_triggers` shows how work arrives: its Schedules with their cadence,
the messages and documents that start work, and any other system that posts to
it.

To see the Routine work without waiting, `run_trigger` runs one of its
Schedules now — a dry run first, because the work is real. See
[Triggers](https://docs.popcorn.ai/triggers.md).

## Next

To tune how the Routine behaves — when it sends reminders, how its emails
read — see
[changing how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md).
