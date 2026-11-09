---
id: triggers
title: Triggers
order: 7
group: How a Routine works
summary: >
  A Trigger is how work arrives in a Routine: on a Schedule, from a message
  posted in it, from a document added to it, or from another system posting to
  it. list_triggers shows each one and whether it is paused; run_trigger runs
  a Schedule now, without waiting for its time, for real. A
  Schedule's cadence can be a Routine Setting.
lede: >
  A Trigger is how work arrives in a Routine: on a Schedule, from a message or
  document, or from another system.
concepts: [routine-settings, actions-and-status, work-a-routines-items]
---

A Trigger is how work arrives in a
[Routine](https://docs.popcorn.ai/routines.md). A Routine can have several,
and its template decides which:

| Kind | Starts work when |
|---|---|
| [Schedule](https://docs.popcorn.ai/schedules.md) | its time comes: every few minutes, or each weekday at 8 |
| Message | someone posts in the Routine |
| Document | a particular document is added to it, such as `#team-offsite`'s questionnaire |
| Another system | that system posts to the Routine's address, such as a website's intake form sending each new client |

`#team-offsite` has two:

- a Schedule, every 15 minutes, that asks anyone new, reads the replies and
  follows up;
- a Document: adding or replacing the questionnaire reads its questions.

A claims intake Routine has every kind but messages:

- Schedules that send the follow-ups and watch the calendar for bookings. A
  booking made on its Booking Page reaches it through one of these.
- An intake address its website form posts each new client to.
- Documents, such as the sample email and the agreement to sign, that set
  up its [Steps](https://docs.popcorn.ai/steps.md) when they are added.

> [!NOTE] Not a Trigger
> Work that a person starts on one
> [Item](https://docs.popcorn.ai/work-a-routines-items.md) is an
> [Action](https://docs.popcorn.ai/actions-and-status.md).

## Adding Items by hand

A person can also add Items without a Trigger: by asking the Routine's
[Agent](https://docs.popcorn.ai/agent.md)
in Popcorn to add someone, or by giving it a spreadsheet of them. Either way
the Routine's next Run picks the Item up.

Your assistant can add them too, as Rows. A Row starts nothing by itself,
but on the [Table](https://docs.popcorn.ai/tables.md) the Routine's
Statuses run on, it is a new Item, and the Routine's next
[Run](https://docs.popcorn.ai/history.md) acts on it. Your assistant adds
up to ten people you name at once; more, it shows you first.

> [!NOTE] A second arrival updates the Item
> In `#team-offsite`, adding someone already there, by the same email
> address, updates their Row and never asks them twice. That is this
> Routine's rule, not every Routine's.

## Seeing them

> "What starts the work in #team-offsite?"

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`.

Your assistant lists every Trigger the Routine has, grouped by kind, with
the work each one starts. A Schedule shows its cadence and time zone, and a
Trigger that is paused or turned off says so.

> [!NOTE] The address stays hidden
> The address another system posts to is never shown: anyone holding it can
> send the Routine work, so it is treated like a password.

## Running a Schedule now

> "Run #team-offsite's Schedule now."

> [!TIP] MCP tool call
> Your assistant calls `run_trigger`, then `get_run` to follow the Run.

Your assistant runs one of the Routine's Schedules now, with the inputs it
runs with on schedule. Its next scheduled Run still happens.

The work is real: posts, emails and changes to Items happen as they would
on schedule. So your assistant runs it at once only when you asked for that
Schedule to run; otherwise it shows you what will run first. It can then
tell you how the Run is going or how it ended, and which Items it changed.

> [!WARNING] A timeout may still have run
> Each confirmed call starts a Run: one that timed out may still have
> started, so check before sending it again.

> [!NOTE] What can run this way
> Only the Schedules a Routine's template declares. A message, document or
> another system starts work by happening. If a Run of the Schedule is
> already going, nothing new starts.

## Changing one

Where a template makes a Schedule's cadence a
[Routine Setting](https://docs.popcorn.ai/routine-settings.md), changing it
reaches this Routine only and survives the template's improvements.
`#team-offsite`'s every 15 minutes isn't one: it is part of its template.
Adding a new kind of Trigger changes what the Routine is built from (see
[customizing a Routine](https://docs.popcorn.ai/customizing-a-routine.md)).

In the template, a scheduled Trigger is an entry in its
[Manifest](https://docs.popcorn.ai/manifest-keys.md)'s `schedules:`, and
the work it starts is a [Flow](https://docs.popcorn.ai/flow-grammar.md).
