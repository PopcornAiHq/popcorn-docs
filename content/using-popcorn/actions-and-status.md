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
  one, as pressing its button would.
lede: >
  An Item's Status says where it stands, and its Actions are what a person
  does to move it on, such as approve, send or close.
concepts: [tables, work-a-routines-items, triggers]
---

An Item's **Status** says where it stands. In a claims intake
[Routine](https://docs.popcorn.ai/routines.md), the Statuses include:

- *Collecting info*
- *Needs retainer review*
- *Getting signatures*
- *Retained*

Popcorn works a Status out from what has happened to the Item, so it changes
only when someone takes an Action or the Routine moves the Item on. It is
never written directly. A Status is about the Item, not about whether one
piece of the Routine's work finished.

An **Action** is something a person does to move an Item on:

- *Send retainer* or *Already signed* at a
  [Review](https://docs.popcorn.ai/reviews.md);
- *Stop tracking* and *Resume tracking* on any Item;
- *Try again* after an error.

An Item offers only the Actions that make sense for where it stands, so the
buttons and the Status can't disagree.

> [!NOTE] No archive Action
> No Action archives an Item. An Item closes for a reason the Routine
> records, such as *No response* when the follow-ups run out, or because a
> person stops tracking it.

## Seeing what an Item offers

> "What can I do with Dana's intake?"

> [!TIP] MCP tool call
> Your assistant calls `list_actions`.

Your assistant lists the Actions the Item offers now, each with the Status
it moves the Item to. Some Actions are taken only in Popcorn, such as a form
to fill in, a document to sign or a request to the Routine's Agent; your
assistant lists them and says so.

## Counting the Items at each Status

> "Where do things stand in #intake?"

> [!TIP] MCP tool call
> Your assistant calls `get_status`, then `list_rows` with a filter on the
> Status Column, such as `{"Status": "open"}`.

Your assistant counts the Items at each Status, and can list the Items at
any one of them.

## Taking one

> "Dana signed on paper. Mark Dana as already signed."

> [!TIP] MCP tool call
> Your assistant calls `take_action`.

Taking an Action is the same as pressing its button in Popcorn: whatever the
Action sends or records is real. You named the Item and the Action, so your
assistant takes it straight away. Otherwise it shows you first what happens
to each Item, and acts once you agree.

The Action applies in the background, and your assistant can show the
Item's new Status once it has.

> [!NOTE] All or nothing
> If one of the Items doesn't offer the Action now, nothing is done to any
> of them. Your assistant leaves that Item out and tries again.

## In the template

Status and Actions come from the same place. The template declares
[State Machines](https://docs.popcorn.ai/state-machine.md); each Status is
worked out from them, and each Action is the button on one of their
Transitions. That is why the Status Column can't be written with
`create_rows` or `update_row`.
