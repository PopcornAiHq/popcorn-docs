---
id: steps
title: Steps
order: 6
group: What it does
summary: >
  A Routine's Steps are its work on each item, in order: what each one asks
  for by email, what finishes it, and how it follows up when no reply comes. A
  Review is the kind of Step where a person decides. Where a template has
  Steps, they stay with the Routine; get_routine lists them, and
  change_routine changes them from a description, showing the change before it
  goes in.
concepts: [reviews, customizing-a-routine, routine-settings]
layer: product
---

A Routine's **Steps** are the work it does on each item, in order. Each Step
asks for one thing and follows up until it has it. Then the item moves on to
the next Step, or stops at a [Review](https://docs.popcorn.ai/product/concepts/reviews.md) for a
person to decide.

Not every Routine has Steps. One that follows deliveries or alerts tracks each
item as it changes, in no fixed order, and Popcorn shows no Steps for it.

## Kinds of Step

In a claims intake Routine, where each item is a potential client:

- **Answers** — asks questions by email, checks each answer against what a
  complete one needs, and asks again only for what is missing.
- **Signature** — sends an agreement through the signing provider and waits
  until everyone has signed.
- **Booking** — shares the booking page and waits until a meeting is on the
  calendar.
- **Reminder** — reminds the person before a meeting they have booked.
- **Delivery** — follows a mailed letter with the carrier until it is
  delivered.
- **Review** — waits for a person on the team to decide what happens next.

Every Step works by email. None collects files: a document is asked for as
one of a Step's questions.

## Following up

A Step sends its first email, then follows up on a reminder schedule while
nothing comes back, within the Routine's sending hours. The schedule and the
hours are [Routine Settings](https://docs.popcorn.ai/product/concepts/routine-settings.md), and a
Step can have its own. When the follow-ups run out, the item closes with a
reason, such as *No response*. A reply after that reopens the Step it went
quiet on.

An item's Status names the Step it is at, such as *Collecting info* or
*Getting signatures*. The Status a finished item ends on is its **outcome**,
such as *Retained* or *Not retained*.

## Seeing and changing them

In Popcorn, the **Routine steps** tab lists a Routine's Steps in order, with
the ways an item leaves each one on its own, and each Review with its
choices.

A person changes the Steps by describing the change, for example "ask for
their date of birth too" or "check with me before the agreement goes out":
to the Routine's agent in Popcorn, or to an assistant with `change_routine`. The change stays with this Routine and survives the template's
improvements (see
[customizing a Routine](https://docs.popcorn.ai/product/concepts/customizing-a-routine.md)). An
earlier version, or the template's own, can be put back, and a change that
would remove a Step items are still at is refused.

An assistant reads the Steps with `get_routine`, which lists them in order as
the **Routine steps** tab does: each Step's kind and name, the ways an item
leaves it on its own, and each Review's reason and choices, with where each
leads and which are made only in Popcorn. Each Step also shows its Status
value, the one `list_rows` filters on. The list names the version of the
Steps installed, and `get_status` shows how many items are at each Step.

`change_routine` changes them in three moves, because the Routine's agent
takes a few minutes to draft a change:

1. **Describe it.** `change_routine` with the request starts the draft and
   returns a `change_id`. Nothing is installed.
2. **Read the proposal.** `get_routine_change` shows the Steps before and
   after, what it would set on each Step, what the agent assumed and any
   questions it left open, and whether it passed the checks against the
   Routine's items. Part of a proposal that is really a
   [Routine Setting](https://docs.popcorn.ai/product/concepts/routine-settings.md) says so.
3. **Confirm it.** `change_routine` with the `change_id` and `confirm=true`
   installs it, checking it once more first.

`change_routine` with `revert_to` puts back the version before, or the
template's own, after a dry run. One change is drafted at a time on a
Routine, and it works only where the template keeps its Steps with the
Routine.

> **Platform note** — A Routine's Steps are the states of its template's
> state machine, and a Routine with Steps of its own has them installed as a
> recipe. A Step is not a flow's `step:`. See
> [State machines](https://docs.popcorn.ai/platform/concepts/state-machine.md).
