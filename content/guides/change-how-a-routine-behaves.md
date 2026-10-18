---
id: change-how-a-routine-behaves
title: Changing how a Routine behaves
order: 2
summary: >
  Changing how one Routine behaves: find the Routine Setting that covers it
  with list_routine_settings, read it in full, change it with
  update_routine_setting after a dry run, and confirm the new value. A setting
  stays with that Routine and can be set back; what no setting covers is
  Instructions or the Routine's steps, both changed in Popcorn, or a copy of
  its own.
concepts: [routine-settings, customizing-a-routine, instructions]
layer: product
---

This guide starts from a request such as "remind people every three days
instead of every week" and ends with one Routine behaving the new way, and
every other Routine made from the same template unchanged.

## 1. Say what should change

Start from the outcome, in the person's words: *chase five times at most*,
*send reminders from the claims team*, *run the morning digest at 7*. The
change belongs to one Routine; note its name.

## 2. Find the setting

> "What can I change about how #chase-renewals chases people?"

`list_routine_settings` with a `query` lists the settings that match:
each one's key, its value, and whether it was changed from the template's
default. Most "can it do X differently" requests are one of these: a
reminder interval, a follow-up limit, a sending mode, a schedule's cadence,
the wording of an email.

If nothing matches, go to step 5.

## 3. Read it in full

`get_routine_setting` shows the whole value, the template's default, what
it accepts, its options and the warning each carries, and who may change it.
A sending mode's warning matters: switching from drafts to sending means
emails go out without a person reviewing them.

## 4. Change it

> "Stop chasing after five follow-ups on #chase-renewals."

`update_routine_setting` is a dry run first: it shows the old and new value
and that the change reaches this Routine only. Read it back to the person,
then call again with `confirm=true`.

- **A switch** takes one of its options.
- **A value** keeps the shape of its default: a list stays a list.
- **A long text**, such as an email's wording, is changed with edits to the
  current text, so the rest of it stays exactly as it was.

Work already under way keeps the value it started with; the next run uses the
new one. To undo the change later, set the setting back to the template's
default.

## 5. When no setting covers it

Three other kinds of change remain:

- **How the Routine's agent should act** — "ask me before sending anything
  to the carrier", "always copy the adjuster". That is its
  [Instructions](https://docs.popcorn.ai/product/concepts/instructions.md): a person tells the
  Routine's agent in Popcorn.
- **Its steps** — another question before the agreement goes out, a review
  before a meeting is booked. Where the template keeps its steps with the
  Routine, a person asks the Routine's agent in Popcorn, and the change stays
  with this Routine.
- **What the Routine is built from** — a new Table, a new kind of Trigger, a
  kind of step its template does not offer. That gives the Routine a copy of its own, which
  no longer receives the template's improvements and cannot be undone. See
  [customizing a Routine](https://docs.popcorn.ai/product/concepts/customizing-a-routine.md)
  before agreeing to it.

> **Platform note** — Making that second kind of change is building on the
> template itself: see
> [authoring an app bundle](https://docs.popcorn.ai/platform/guides/template-authoring.md).
