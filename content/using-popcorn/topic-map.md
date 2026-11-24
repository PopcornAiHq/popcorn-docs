---
id: topic-map
title: Topic Map
order: 17
group: Day to day
summary: >
  A Topic Map Routine gathers what the Workspace's other Routines publish
  into the strands of work a team has in flight, one topic per Item. One
  Action on a topic reads Mark done while it is on the map and Reopen once it
  is closed, and taking it records who closed the topic and when. A query
  matches your words as one phrase, so search by one distinctive word.
lede: >
  The map of what your team has in flight: find the piece of work you mean,
  and mark it done or put it back.
concepts: [routines, actions-and-status, work-a-routines-items, tables]
---

A **Topic Map** is a [Routine](https://docs.popcorn.ai/routines.md) that
keeps the map of what a team has in flight. It reads what the Workspace's
other Routines publish — mail, documents, pull requests, the team's own
chat — and gathers what belongs together into topics: a spec, the work
implementing it and the thread arguing about it are one topic, not three.
Each topic is an
[Item](https://docs.popcorn.ai/work-a-routines-items.md) with a name that
holds still and a headline that moves as the work does.

You don't have to name the Routine. Ask about the piece of work in your own
words, and your assistant finds the Topic Map in the Workspace and then the
topic in it.

## Find the topic you mean

> "Where has the Notion scanning work got to?"

> [!TIP] MCP tool call
> Your assistant calls `list_routines`, then `list_rows` with a `query`.

A query matches your words **as one phrase**, as you wrote them, inside a
single [Column](https://docs.popcorn.ai/tables.md)'s value; only case is
ignored. It does not split the phrase or look for the words in any order,
so wording from your own head often matches nothing: "the Notion privacy
work" misses a topic whose headline reads *Notion scanning is restricted to
chosen teamspaces*.

Search by **one distinctive word** instead — a product, a person, a
feature — and read the few topics that come back.

> [!NOTE] A short page is not an empty one
> A query lists a [Row](https://docs.popcorn.ai/tables.md) only where the
> text appears in a value you can see, so a page can come back holding
> fewer Rows than it found, and there is no total.

## Mark it done, or put it back

> "That's finished — mark it done."

> [!TIP] MCP tool call
> Your assistant calls `list_actions`, then `take_action`.

A topic offers **one**
[Action](https://docs.popcorn.ai/actions-and-status.md), and where the
topic already stands decides which way it goes: **Mark done** while it is
on the map, **Reopen** once it is closed. Your assistant never picks
between two verbs — it takes the Action the topic offers.

Mark done closes the topic there and then and records which
[Member](https://docs.popcorn.ai/members.md) closed it and when. Reopen
clears that and puts the topic back on the map. The Routine goes on reading
either way, and a Member's call outranks its own: a topic someone reopened
is left alone until the work under it falls quiet again.

> [!NOTE] The Action is the only way
> A topic's [Status](https://docs.popcorn.ai/actions-and-status.md) changes
> only when its Action fires. Writing the Column that holds it is refused,
> so there is nothing to put right by hand.

## What a topic's Status says

| Status | What it means |
|---|---|
| **New** | first seen on this pass |
| **Active** | something under it moved on this pass |
| **Stalled** | quiet for a while, with something still open under it |
| **Done** | closed, by a Member or because nothing under it was left waiting |
| **Gone** | off the map, a while after closing or because the grouping no longer produces it |

A topic closes by itself too, once nothing under it is waiting and it has
been quiet for long enough; how long is a
[Routine Setting](https://docs.popcorn.ai/routine-settings.md). Gone is not
the end — a Row newer than the closure brings the topic back.
