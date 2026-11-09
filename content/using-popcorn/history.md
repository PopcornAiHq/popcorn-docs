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

A [Routine](https://docs.popcorn.ai/routines.md)'s **History** is what has
happened in it:

- **changes to its Items** — what changed on an Item, who or what changed
  it, and why;
- **its work** — each Run that changed an Item, what started it, and how it
  ended;
- **its email turns** — in a Routine with
  [Steps](https://docs.popcorn.ai/steps.md), each email it sent or reply it
  assessed;
- **its conversation** — the messages people and its Agent posted in it.

History answers "did the reminder go out?", "why is this claim closed?" and
"who sent the retainer?". An Item's History is the audit log kept for its
Row.

> [!TIP] From the CLI
> Each Run in a History is a Run of one of the template's Flows, which the
> CLI also reads.
> [Debugging a failed Run](https://docs.popcorn.ai/debugging-a-failed-run.md)
> follows one to its cause.

## One Item's History

> "What happened with Ben Garrett's intake?"

> [!TIP] MCP tool call
> Your assistant calls `list_history` with the Item's Row ID.

Your assistant lists what happened to the Item, newest first, as the Item's
**Activity** tab in Popcorn does. Each entry has:

- **when**, and **who or what**: a Member by name; Popcorn, with the work it
  was doing; or "Popcorn, for a person" when someone's button started the
  work, since a Run doesn't record who pressed it;
- **what happened**, such as *Send retainer* or *Answered all 5 intake
  questions*;
- the Item's **Status** move and its new **Why**, then the other fields that
  changed.

After the entries come the Runs that changed the Item, and how each ended.
A long History comes a page at a time.

## One entry in full

> "Show me the retainer entry in full: what changed and what the Run did."

> [!TIP] MCP tool call
> Your assistant calls `read_history_entry` with an `entry_id` from
> `list_history`.

Your assistant shows every field the change touched, before and after. When
Popcorn's work made the change, it also shows that Run: how it started and
ended, and what it did, in order, with any retries and why.

A long value is cut, and the entry says so. What the Item holds now is on
its Row, not in its History.

## One Run

> "What did this morning's follow-up Run change?"

> [!TIP] MCP tool call
> Your assistant calls `list_history` with the Run instead of a Row ID.

Your assistant follows one Run: how it is going or how it ended, and the
Items it changed, or what it did if it changed none.

## What it leaves out

- **Runs that only read an Item.** An Item's History lists only work that
  changed it.
- **The Routine's conversation and email bodies.** Both are read in Popcorn,
  and email turns have no entry to read in full.
- **A timeline for the whole Routine.** History is read one Item, or one
  Run, at a time.

> [!NOTE] How far back
> Changes are kept for a limited time (30 days, as of 2026-10-19), and the
> last page of a History says how far back it goes.

## On a Workspace that guards personal data

History hides what a list of Rows would hide:

- A changed value in a Column marked as personal data shows as a
  placeholder.
- An entry is titled by its kind, such as *Email sent*, *Reply assessed* or
  *Action taken: Send retainer*, never by the words the work wrote about
  itself, which can name the person an Item is about.
- A failed Run shows only how it ended, without its error message, which
  can quote the Item.
