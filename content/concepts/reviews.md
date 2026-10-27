---
id: reviews
title: Reviews
order: 9
group: What it does
summary: >
  A Review is the kind of Step where a person makes the call instead of
  Popcorn: the item waits, says why, and gives a few choices of where it goes
  next. Approval is one kind of Review, and its passing outcome. get_status
  lists what is waiting and why; take_action takes a choice, except one that
  opens a form in Popcorn.
concepts: [steps, actions-and-status, routine-settings]
part: use
---

A **Review** is a [Step](https://docs.popcorn.ai/use/concepts/steps.md) where the Routine stops
and waits for a person. The item says why it is waiting and offers a few
choices, each an [Action](https://docs.popcorn.ai/use/concepts/actions-and-status.md) that
leads somewhere: on to the next Step, straight to an outcome, or past work
already done.

In a claims intake Routine, the Review after the questions says: "Intake is
done. Send the document for signature, record it as already signed, or do
not send the retainer." Its choices are:

- **Send retainer** — opens the agreement for a person to check every field
  before it goes. Once it is sent, the item moves on to signing.
- **Already signed** — for an agreement signed outside Popcorn. The item moves
  on as a signature would have moved it.
- **Do not send retainer** — the item ends as *Not retained*, and the person
  is sent a short, neutral email saying the firm cannot take it further.

**Approval** is one kind of Review, "should this go ahead?", and also what a
Review that passes ends in. A Review can end in other ways too, such as "not a
fit" or "already done".

## What is waiting

In Popcorn, items at a Review show as needing review. Each one's Status names
its Review, such as *Needs retainer review*.

An assistant asks `get_status`, which counts the items at each Status, marks
the Statuses that need a person, and lists what is waiting, newest first, with
why and which items. `list_rows`, filtering on the Status Column, lists the
items at one Review in full.

## Making the choice

`list_actions` shows the choices an item offers, and `take_action` takes one
after a dry run, as pressing its button would. A choice that opens a form,
such as sending an agreement whose fields a person checks first, is marked
`[in the Popcorn app]` and is made there.

## Work done outside Popcorn

Some work happens without the Routine: an answer given on the phone, a call
already held. When the Routine's **Step forward** setting is on, an item
offers choices such as *Already answered* or *Call already held*, which move
it past a Step without waiting for it.

## Adding or removing a Review

A Review is a Step, so a person adds or removes one by telling the Routine's
agent in Popcorn, for example "check with me before booking the meeting". The
change stays with this Routine and survives the template's improvements; it
does not give the Routine a copy of its own. Without a Review, the Routine
moves the item on by itself.

In the template, a Review is a state that warns, with the transitions people
can take from it (see
[state machines in a bundle](https://docs.popcorn.ai/build/concepts/state-machine.md)).
It is not a flow's `await_approval`, which pauses one run until someone
replies.
