---
id: triggers
title: Triggers
order: 3
group: How work arrives
summary: >
  A Trigger is how work arrives in a Routine: on a schedule, from a message
  posted in it, from a document added to it, or from another system posting to
  it. list_triggers shows each one and whether it is paused; run_trigger runs
  a schedule now, without waiting for its time, for real after a dry run. A
  schedule's cadence is a Routine Setting.
concepts: [routine-settings, actions-and-status, work-a-routines-items]
layer: product
---

A Trigger is how work arrives in a Routine. A Routine can have several, and
its template decides which:

| Kind | Starts work when |
|---|---|
| Schedule | its time comes: every few minutes, or each weekday at 8 |
| Message | someone posts in the Routine |
| Document | a particular document is added to it, such as a policy |
| Another system | that system posts to the Routine's address |

Work that a person starts on one item is an
[Action](https://docs.popcorn.ai/product/concepts/actions-and-status.md), not a Trigger.

## Seeing them

`list_triggers` lists every Trigger a Routine has, grouped by kind, with the
work each one starts. A schedule shows its cadence and time zone, and a Trigger
that is paused or turned off says so. The address another system posts to is
never shown: anyone holding it can send the Routine work, so it is treated
like a password.

## Running a schedule now

`run_trigger` runs one of a Routine's schedules now, with the inputs it
runs with on schedule. Its next scheduled run still happens. The work is real
— posts, emails and changes to items happen as they would on schedule — so
the first call is a dry run that says what will run, and only the call with
`confirm=true` starts it. Each confirmed call starts a run: one that timed out
may still have started, so check before sending it again. How the run ended
is shown in Popcorn, with the Routine's work.

Only schedules can be run this way. A message, document or another system
starts work by happening.

## Changing one

A schedule's cadence is a [Routine Setting](https://docs.popcorn.ai/product/concepts/routine-settings.md):
changing it reaches this Routine only and survives the template's
improvements. Adding a new kind of Trigger changes what the Routine is built
from (see [customizing a Routine](https://docs.popcorn.ai/product/concepts/customizing-a-routine.md)).

> **Platform note** — A scheduled Trigger is a *schedule* in the template's
> manifest, and the work it starts is a *flow*. See
> [Schedules in a manifest](https://docs.popcorn.ai/platform/concepts/schedules.md).
