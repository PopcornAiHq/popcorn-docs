---
id: tables
title: Tables, Rows and Columns
order: 10
group: What it holds
summary: >
  A Routine's Tables hold its items — claims, orders, contacts — as Rows and
  Columns. An assistant lists and reads them (list_tables, get_table,
  list_rows with filters, get_row) and adds, changes and deletes Rows
  (create_rows, update_row, delete_rows). Changing a Row starts no work, and
  a Row's Status changes only by an Action.
concepts: [actions-and-status, work-a-routines-items]
layer: product
---

A Routine's **Tables** hold what it keeps: one Table of claims, one of
contacts. Each **Row** is one item, each **Column** one kind of information
every Row has, and a **Cell** is one Row's value in one Column.

## Reading

| Tool | Gives |
|---|---|
| `list_tables` | the Routine's Tables, each with its Row count |
| `get_table` | a Table's Columns in order, each with its type and label |
| `list_rows` | Rows, newest first, with a few Columns each |
| `get_row` | one Row in full, with when it was created and last changed |

`list_rows` finds Rows by text in any Column (`query`: "4471" finds the Row
whatever Column holds it) or by conditions on Columns (`filter`): equal to,
greater or less than, one of a list, containing a text, present or absent. All
conditions must hold; there is no "or". `sort` orders by one Column, and
`columns` picks which ones to show.

Some Columns are guarded. Personal data may be hidden, depending on the
workspace, and a Column holding a credential is never shown or written.

## Writing

- `create_rows` adds up to 50 Rows. A Row that matches an existing one on
  the Table's identifying Columns merges into it instead of adding another,
  and the response says which Rows were added and which merged.
- `update_row` changes some Columns of one Row. It needs the Row's revision
  from `get_row`: if the Row changed since, nothing is written and the
  response shows it as it is now.
- `delete_rows` deletes Rows by ID, after a dry run. A deleted Row cannot be
  restored with these tools.

Writing a Row starts no work, and some Columns keep their own rules: a notes
Column may append what is written rather than replace it, and a first-seen
date may keep its first value. `update_row`'s response names any Column
where that happened. A Row's **Status** cannot be written at all: it changes
when an [Action](https://docs.popcorn.ai/product/concepts/actions-and-status.md) is taken or the
Routine moves the item on.

> **Platform note** — Those per-Column rules are *merge policies*, declared
> in the template. See [table columns](https://docs.popcorn.ai/platform/concepts/table-columns.md)
> and [column merge policy](https://docs.popcorn.ai/platform/concepts/merge-policy.md).
