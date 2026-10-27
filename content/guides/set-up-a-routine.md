---
id: set-up-a-routine
title: Setting up a Routine
order: 2
summary: >
  Setting up a Routine from a Routine Template: pick a template with
  list_routine_templates, create the Routine with create_routine (a dry run
  first), wait for its template to install, have the right person connect each
  account it needs, then check what starts its work with list_triggers.
concepts: [routines, connections, triggers]
part: use
---

This guide starts from "we need a Routine for this" and ends with a Routine
whose Connections are made and whose work is ready to start. Every step is
something a person can ask their assistant for, and the assistant does it
through the Popcorn MCP server; one step needs the person themselves.

The example sets up a private Routine for western-region claims, called
`#claims-west`, from the Chase template, whose
[Steps](https://docs.popcorn.ai/use/concepts/steps.md) start as a claims intake: questions, a
Review, then the retainer.

## Or describe it in Popcorn

A person can also start a Routine in Popcorn without picking a template.
**New routine** takes a sentence such as "ask new clients a few questions,
then send them a retainer", or an example to start from, and the new
Routine's agent drafts its Steps from it for the person to check. Popcorn can
also suggest Routines from a connected inbox, from the work it finds waiting
there. Both start from the same template as this guide, so the rest of it
applies once the Routine exists.

## 1. Pick a template

> "What templates could a new Routine here start from?"

`list_routine_templates` lists the Routine Templates this workspace can
start from: each one's name, its slug, what it does, and the Connections it
needs before it runs. A template the workspace cannot run is not listed. Note
the slug — `chase` here — and the Connections (Gmail, Google Drive, Google
Calendar and an intake address), because someone has to make them in step 4.

## 2. Create the Routine

> "Set up a private #claims-west Routine from the Chase template, with
> Jordan in it."

`create_routine` with a `template` is a dry run first. It names the
version that will install, the members, and the Connections someone sets up
before the Routine runs, and changes nothing. Read it back to the person, then
call again with `confirm=true`.

- **Private or open.** A private Routine is joined only by you and the
  people you name; one that is not private adds everyone in the workspace.
- **The name.** Spaces become hyphens, and a name already used in the
  workspace is refused with the ID of the Routine that has it.

The response gives the new Routine's ID. Use the ID, not the name, in every
call that changes it.

## 3. Wait for the template to install

The template installs in the background once the Routine exists, usually in
seconds. `get_routine` with `wait_seconds` (up to 20) waits for it:

> "Is #claims-west ready?"

Its **Install** field says `installed` when the template has landed. Until
then the Routine exists but has nothing to run.

## 4. Make its Connections

`get_routine` lists each Connection the Routine needs, as connected or
**NOT CONNECTED**. A Connection signs in as a person, so the assistant cannot
make one: the person who owns the account connects it in the Routine's
settings in Popcorn, in a browser. Tell them which ones, and why — work that
uses a missing Connection cannot run.

When they are done, `get_routine` again: every Connection should read
connected. See [Connections](https://docs.popcorn.ai/use/concepts/connections.md).

## 5. See what starts its work

> "What sets #claims-west working?"

`list_triggers` shows how work arrives: its schedules with their cadence,
the messages and documents that start work, and any other system that posts to
it. A Chase Routine needs its sample email before its first Step can ask
anything, and its agreement before it can send one; adding them is a
person's step in Popcorn (see
[References](https://docs.popcorn.ai/use/concepts/reference-documents.md)).

To see the Routine work without waiting, `run_trigger` runs one of its
schedules now — a dry run first, because the work is real. See
[Triggers](https://docs.popcorn.ai/use/concepts/triggers.md).

## Next

To tune how the Routine behaves — when it sends reminders, how its emails
read — see
[changing how a Routine behaves](https://docs.popcorn.ai/use/guides/change-how-a-routine-behaves.md).
