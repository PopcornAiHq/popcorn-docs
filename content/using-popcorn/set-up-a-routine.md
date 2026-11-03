---
id: set-up-a-routine
title: Set up your first Routine
order: 2
group: Getting started
summary: >
  Setting up a new Routine from a Routine Template, such as client intake
  from the Chase template: pick a template with list_routine_templates, create
  the Routine with create_routine, wait for its template to
  install, make its Connections with make_connection, add its References with
  add_reference, check what's left with get_setup, then see what starts its
  work with list_triggers.
lede: >
  Ask your AI assistant to set up a Routine from a template, make its
  Connections and check it's ready to run.
concepts: [routines, connections, triggers]
---

This guide sets up a Routine called `#new-clients` from the Chase template.
It emails each new client a few questions and follows up until they
answer. Each step starts with a prompt you might give your assistant.

## Pick a template

> "Which templates can I start a Routine from?"

> [!TIP] MCP tool call
> Your assistant calls `list_routine_templates`.

Your assistant lists the
[Routine Templates](https://docs.popcorn.ai/routines.md) available in your
Workspace, describing what each one does and which
[Connections](https://docs.popcorn.ai/connections.md) it needs. The Chase
template needs only Gmail to get started.

> [!NOTE] Optional Connections
> Chase's other Connections, such as Google Calendar and E-signature, add
> features you can set up later.

## Create the Routine

> "Create a private #new-clients Routine from the Chase template."

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

> "Is #new-clients ready?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine` with `wait_seconds` until its
> **Install** field says `installed`.

Popcorn installs the Routine's template in the background, usually within
seconds. Wait for it to finish before making the Routine's Connections.

## Make its Connections

> "Connect my Google account to #new-clients."

> [!TIP] MCP tool call
> Your assistant calls `list_connections`, then `make_connection`.

What happens:

- Your assistant lists the Routine's Connections and what each one is for.
- If you haven't signed in to Google yet, it gives you a link to do it.
- Once you agree, it connects your Google account to Gmail.

A Connection signs in as you, so only your own accounts can be connected.

The same account can fill Google Calendar and Google Drive too. The rest of
the Connections are on the
[Connections](https://docs.popcorn.ai/connections.md) page.

> [!WARNING] A missing Connection stops work
> Work that uses a missing Connection cannot run. Some hold the whole
> Routine back, and Popcorn shows it as not ready.

## Add its References

> "Add our intake questions to #new-clients."

> [!TIP] MCP tool call
> Your assistant calls `add_reference`.

A Chase Routine needs one Reference: the sample email its first
[Step](https://docs.popcorn.ai/steps.md) takes its questions and wording
from. Your assistant adds it from text or a file, after showing you what it
will add. The agreement it sends for signature is optional; see
[References](https://docs.popcorn.ai/reference-documents.md).

## Check what's left

> "What's left to set up on #new-clients?"

> [!TIP] MCP tool call
> Your assistant calls `get_setup`.

Your assistant reads the Routine's setup checklist: each step done or left,
which are required, and what each one left needs, such as a Connection or a
value set in the Routine's Today tab. When nothing required is left, the
Routine is ready.

## See what starts its work

> "What sets #new-clients working?"

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, and `run_trigger` to run a Schedule
> now.

Your assistant shows how work arrives: the Routine's Schedules and when they
run, the messages and documents that start work, and any other system that
posts to it. To see the Routine work without waiting, ask it to run a
Schedule now. It shows you what will run first, because the work is real.
See [Triggers](https://docs.popcorn.ai/triggers.md).

## Next

To tune how the Routine behaves — when it sends reminders, how its emails
read — see
[changing how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md).
