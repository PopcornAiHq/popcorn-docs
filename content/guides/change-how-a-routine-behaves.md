---
id: change-how-a-routine-behaves
title: Changing how a Routine behaves
order: 3
summary: >
  Changing how one Routine behaves: find the Routine Setting that covers it
  with list_routine_settings, read it in full, change it with
  update_routine_setting after a dry run, and confirm it. A setting stays with
  that Routine and can be set back. Otherwise: its Steps, with change_routine
  after reading the proposal; its other Instructions, in Popcorn; or a copy of
  its own.
concepts: [routine-settings, customizing-a-routine, instructions]
part: use
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
  [Instructions](https://docs.popcorn.ai/use/concepts/instructions.md): a person tells the
  Routine's agent in Popcorn.
- **Its steps** — another question before the agreement goes out, a review
  before a meeting is booked. Where the template keeps its steps with the
  Routine, that is `change_routine` (step 6), or the Routine's agent in
  Popcorn, and the change stays with this Routine.
- **What the Routine is built from** — a new Table, a new kind of Trigger, a
  kind of step its template does not offer. That gives the Routine a copy of its own, which
  no longer receives the template's improvements and cannot be undone. See
  [customizing a Routine](https://docs.popcorn.ai/use/concepts/customizing-a-routine.md)
  before agreeing to it. Making that change is building on the template
  itself: see
  [authoring an app bundle](https://docs.popcorn.ai/build/guides/template-authoring.md).

## 6. Change its Steps

> "In #intake, once a claimant signs, ask them to book the interview
> straight away."

1. **Start the draft.** `change_routine` with `routine_id` and the request,
   in the person's words. It returns a `change_id` and installs nothing; the
   Routine's agent takes a few minutes to draft it.
2. **Read the proposal.** `get_routine_change` with that `change_id`, and
   `wait_seconds` (up to 20) to wait in the call. While it is drafting it
   says so. When it is proposed, it shows the Steps before and after, what it
   sets on each Step, what the agent assumed, any questions it left open, and
   the checks against the Routine's items. Read it back to the person. If
   part of it is a Routine Setting, it says which, so that part can be
   changed with `update_routine_setting` instead.
3. **Install it.** Once the person agrees, `change_routine` with the
   `change_id` and `confirm=true`. It checks the proposal once more and
   refuses if the Steps changed in the meantime. `get_routine_change` shows
   when it is installed, and the version before it.
4. **Undo it, if needed.** `change_routine` with `revert_to` set to that
   version, `"previous"` or `"template"` is a dry run that shows the Steps
   it would put back; confirm it with the `run_key` it gives.

A new request while one is drafting is refused; open questions in a proposal
are answered with a new request.
