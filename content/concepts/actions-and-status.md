---
id: actions-and-status
title: Actions and Status
order: 11
group: What people do, and what happened
summary: >
  An item's Status says where it stands, such as Waiting on documents, and
  Popcorn works it out from what has happened, so it is never written
  directly. Actions are what a person does to move an item on: approve, send,
  close. list_actions shows the Actions an item offers now; take_action takes
  one, after a dry run, as pressing its button would.
concepts: [tables, work-a-routines-items, triggers]
layer: product
---

An item's **Status** says where it stands: in a claims intake Routine,
*Collecting info*, *Needs retainer review*, *Getting signatures*, *Retained*. Popcorn works it out from what has happened to the item,
so it changes when someone takes an Action or the Routine moves the item on —
never by writing it. `create_rows` and `update_row` refuse a Status Column.
A Status is about the item, not about whether one piece of the Routine's work
finished.

An **Action** is something a person does to move an item on: *Send
retainer* or *Already signed* at a [Review](https://docs.popcorn.ai/product/concepts/reviews.md),
*Stop tracking* and *Resume tracking* on any item, *Try again* after an error.
An item offers only the Actions that make sense for where it stands, so the
buttons and the Status cannot disagree.

There is no Action that archives an item. An item closes for a reason the
Routine records, such as *No response* when the follow-ups run out, or a
person stops tracking it.

## Seeing what an item offers

`list_actions` lists the Actions one item offers now, each with the Status
it moves the item to. Some Actions need the Popcorn app — a form to fill in, a
document to sign, a request to the Routine's agent — and are listed and marked
`[in the Popcorn app]`.

`get_status` counts the items at each Status, with the value each is stored
as. To list the items at one, filter Rows on the Status Column with
`list_rows`, for example `{"Status": "open"}`.

## Taking one

`take_action` takes one Action on one or more items, as a person pressing
its button in Popcorn would, and what the Action sends or records is real.
The first call is a dry run: it says what happens to each item and gives a
`run_key`. The call with `confirm=true` and that `run_key` acts, once —
sending it again finds the work it already started. An item that does not
offer the Action now is refused.

The Action applies in the background; `get_row` shows the item's new Status
once it has.

> **Platform note** — Status is a projection of *state machines* the template
> declares, and each Action is the button on one of their transitions. See
> [state machines in a bundle](https://docs.popcorn.ai/platform/concepts/state-machine.md).
