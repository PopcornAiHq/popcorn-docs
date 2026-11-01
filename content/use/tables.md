---
id: tables
title: Tables, Rows and Columns
order: 8
group: How a Routine works
summary: >
  A Routine's Tables hold its Items — claims, orders, contacts — as Rows and
  Columns. An assistant lists and reads them (list_tables, get_table,
  list_rows with filters, get_row) and adds, changes and deletes Rows
  (create_rows and delete_rows after a dry run, update_row). An added Row
  can be a new Item the Routine's work picks up; a Row's Status changes
  only by an Action.
lede: >
  A Routine's Tables hold its Items, such as claims, orders or contacts, as
  Rows and Columns.
concepts: [actions-and-status, work-a-routines-items]
---

A Routine's **Tables** hold what it keeps: one Table of claims, one of
contacts. Each **Row** is one Item, each **Column** one kind of information
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
Workspace, and a Column holding a credential is never shown or written.

## Writing

- `create_rows` adds up to 50 Rows, after a dry run. A Row that matches an
  existing one on the Table's identifying Columns merges into it instead of
  adding another. The dry run says which Rows would be added and which would
  merge, and what an added Row starts; the call with `confirm=true` and the
  same Rows writes them, and its response says which were added and which
  merged.
- `update_row` changes some Columns of one Row. It needs the Row's revision
  from `get_row`: if the Row changed since, nothing is written and the
  response shows it as it is now.
- `delete_rows` deletes Rows by ID, after a dry run. A deleted Row cannot be
  restored with these tools.

Writing a Row starts nothing by itself. On the Table a Routine's Statuses
run on, though, an added Row is a new Item: it starts at its first Status,
and the Routine's next Run acts on it for real, which on a Routine that
sends email means that Item's first email. Some Columns keep their own
rules: a notes Column may append what is written rather than replace it, and a first-seen
date may keep its first value. Those rules are the Column's Merge Policy,
declared in the template (see
[Table Columns](https://docs.popcorn.ai/table-columns.md) and
[Column Merge Policy](https://docs.popcorn.ai/merge-policy.md)). `update_row`'s response names any Column
where that happened. A Row's **Status** cannot be written at all: it changes
when an [Action](https://docs.popcorn.ai/actions-and-status.md) is taken or the
Routine moves the Item on.
