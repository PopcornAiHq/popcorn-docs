---
id: actions-and-status
title: Actions and Status
order: 11
group: Day to day
summary: >
  An Item's Status says where it stands, such as Waiting on documents, and
  Popcorn works it out from what has happened, so it is never written
  directly. Actions are what a person does to move an Item on: approve, send,
  close. list_actions shows the Actions an Item offers now; take_action takes
  one, after a dry run, as pressing its button would.
lede: >
  An Item's Status says where it stands, and its Actions are what a person
  does to move it on, such as approve, send or close.
concepts: [tables, work-a-routines-items, triggers]
---

An Item's **Status** says where it stands: in a claims intake Routine,
*Collecting info*, *Needs retainer review*, *Getting signatures*, *Retained*. Popcorn works it out from what has happened to the Item,
so it changes when someone takes an Action or the Routine moves the Item on —
never by writing it. `create_rows` and `update_row` refuse a Status Column.
A Status is about the Item, not about whether one piece of the Routine's work
finished.

An **Action** is something a person does to move an Item on: *Send
retainer* or *Already signed* at a [Review](https://docs.popcorn.ai/reviews.md),
*Stop tracking* and *Resume tracking* on any Item, *Try again* after an error.
An Item offers only the Actions that make sense for where it stands, so the
buttons and the Status cannot disagree. Both come from the same place: the
template declares State Machines, Status is worked out from them, and each
Action is the button on one of their Transitions (see
[State Machines in a Bundle](https://docs.popcorn.ai/state-machine.md)).

There is no Action that archives an Item. An Item closes for a reason the
Routine records, such as *No response* when the follow-ups run out, or a
person stops tracking it.

## Seeing what an Item offers

`list_actions` lists the Actions one Item offers now, each with the Status
it moves the Item to. Some Actions need the Popcorn app — a form to fill in, a
document to sign, a request to the Routine's Agent — and are listed and marked
`[in the Popcorn app]`.

`get_status` counts the Items at each Status, with the value each is stored
as. To list the Items at one, filter Rows on the Status Column with
`list_rows`, for example `{"Status": "open"}`.

## Taking one

`take_action` takes one Action on one or more Items, as a person pressing
its button in Popcorn would, and what the Action sends or records is real.
The first call is a dry run: it says what happens to each Item and gives a
`run_key`. The call with `confirm=true` and that `run_key` acts, once —
sending it again finds the work it already started. An Item that does not
offer the Action now is refused.

The Action applies in the background; `get_row` shows the Item's new Status
once it has.
