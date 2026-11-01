---
id: history
title: History
order: 12
group: Day to day
summary: >
  A Routine's History is what has happened in it — did the reminder emails go
  out, why was this claim closed: changes to its Items with who or what made
  each and why, the Runs that made them and how they ended, and its email
  turns. list_history shows an assistant one Item's, newest first, and
  read_history_entry shows one entry in full. The Routine's conversation is
  read in Popcorn.
lede: >
  A Routine's History records what happened in it: each change to its Items,
  who or what made it and why, and the Runs behind it.
concepts: [actions-and-status, triggers, tables]
---

A Routine's **History** is what has happened in it:

- **changes to its Items** — what changed on an Item, who or what changed
  it, and why;
- **its work** — each Run that changed an Item, what started it, and how it
  ended;
- **its email turns** — in a Routine with Steps, each email it sent or reply
  it assessed;
- **its conversation** — the messages people and its Agent posted in it.

History answers "did the reminder go out?", "why is this claim closed?" and
"who sent the retainer?". An Item's History is the audit log kept for its
Row, and each Run in it is a Run of one of the template's Flows, which the
CLI also reads;
[debugging a failed Run](https://docs.popcorn.ai/debugging-a-failed-run.md)
follows one to its cause.

## One Item's History

> "What happened with Ben Garrett's intake?"

`list_history` takes the Routine and the Item's Row ID and lists what
happened to it, newest first, as the Item's **Activity** tab in Popcorn does.
Each entry has:

- **when**, and **who or what**: a Member by name; Popcorn, with the work it
  was doing; or "Popcorn, for a person" when someone's button started the
  work, since a Run doesn't record who pressed it;
- **what happened**, such as *Send retainer* or *Answered all 5 intake
  questions*;
- the Item's **Status** move and its new **Why**, then the other fields that
  changed.

After the entries, it lists the Runs that changed the Item on that page and
how each ended. A long History comes in pages, with a `next_cursor` for the
next one.

Each change ends with its `entry_id`, for reading that entry in full.

## One entry in full

> "Show me the retainer entry in full: what changed and what the Run did."

`read_history_entry` takes the Routine and an `entry_id` from
`list_history`, and shows every field the change touched, before and after,
then the Run that made it: how it started and ended, and what it did, in
order, with any retries and why. A long value is cut, and the entry says
so; `get_row` shows what the Item holds now, not the earlier value.

An entry from another Routine is refused as not found.

## What it leaves out

- **Runs that only read the Item.** Only work that changed it is listed.
- **History older than Popcorn keeps.** Changes are kept for a limited time
  (30 days, as of 2026-10-19), and the last page says so.
- **The Routine's conversation and email bodies.** Both are read in Popcorn,
  and email turns have no entry to read in full.
- **A timeline for the whole Routine.** History is read one Item at a time.

## On a Workspace that guards personal data

`list_history` hides what `list_rows` would hide: a changed value in a
Column marked as personal data shows as a placeholder. It also never prints
the words a piece of work wrote about itself, which can name the person an
Item is about: each entry is titled by its kind instead, such as *Email sent*,
*Reply assessed* or *Action taken: Send retainer*. `read_history_entry`
follows the same rule, and also leaves out a failed Run's error message,
which can quote the Item; it shows only how the Run ended.
