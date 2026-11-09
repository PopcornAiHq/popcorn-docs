---
id: tables
title: Tables, Rows and Columns
order: 11
group: How a Routine works
summary: >
  A Routine's Tables hold its Items — claims, orders, contacts — as Rows and
  Columns. An assistant lists and reads them (list_tables, get_table,
  list_rows with filters, get_row) and adds, changes and deletes Rows
  (create_rows, delete_rows after a dry run, update_row). An added Row
  can be a new Item the Routine's work picks up; a Row's Status changes
  only by an Action.
lede: >
  A Routine's Tables hold its Items, such as claims, orders or contacts, as
  Rows and Columns.
concepts: [actions-and-status, work-a-routines-items]
---

A Routine's **Tables** hold what it keeps. `#team-offsite` has one,
`recipients`, with a Row for each person asked; a claims intake Routine
keeps one of claims and one of contacts. Each **Row** is one
[Item](https://docs.popcorn.ai/work-a-routines-items.md), each **Column** one
kind of information
every Row has, and a **Cell** is one Row's value in one Column.

## Reading

> "Show me who in #team-offsite is still waiting to answer."

> [!TIP] MCP tool call
> Your assistant calls `list_tables`, `get_table`, then `list_rows` with a
> `filter`, and `get_row` for one Row in full.

| Your assistant can show | With |
|---|---|
| the Routine's Tables, each with its Row count | `list_tables` |
| a Table's Columns in order, each with its type and label | `get_table` |
| Rows, newest first, with a few Columns each | `list_rows` |
| one Row in full, with when it was created and last changed | `get_row` |

Your assistant finds Rows in two ways:

- **By text in any Column.** "jane" finds the Row whatever Column holds it.
- **By conditions on Columns:** equal to, greater or less than, one of a
  list, containing a text, present or absent. All conditions must hold;
  there is no "or".

It can also sort by one Column and pick which Columns to show.

> [!NOTE] Guarded Columns
> Personal data may be hidden, depending on the Workspace, and a Column
> holding a credential is never shown or written.

## Writing

> "Add Sam Lee, sam@example.com, to #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `create_rows`, `update_row` or `delete_rows`.

- **Adding.** Your assistant adds up to 50 Rows in one go, and up to ten
  Rows you named at once. More than ten, or Rows it put together from a
  file or a page, come back as a dry run first, saying which would be added, which would merge, and what an
  added Row starts.
- **Merging.** A Row that matches an existing one on the Table's
  identifying Columns merges into it instead of adding another. The answer
  says which Rows were added and which merged.
- **Changing.** Your assistant changes some Columns of one Row. If the Row
  changed since it read it, nothing is written and it shows you the Row as
  it is now.
- **Deleting.** Your assistant deletes Rows after showing you which, and
  once you agree.

> [!CAUTION] Deleting is permanent
> A deleted Row can't be restored with these tools.

> [!IMPORTANT] An added Row can start work
> Writing a Row starts nothing by itself, except on the Table a Routine's
> [Statuses](https://docs.popcorn.ai/actions-and-status.md) run on. There an
> added Row is a new Item, and the Routine's next
> [Run](https://docs.popcorn.ai/history.md) acts on it for real, giving it
> its first Status if the Routine hasn't yet. On a
> Routine that sends email, that means
> the Item's first email.

A Row's Status can't be written at all: it changes when an
[Action](https://docs.popcorn.ai/actions-and-status.md) is taken or the
Routine moves the Item on.

Some Columns keep their own rules. A notes Column may append what is
written rather than replace it, and a first-seen date may keep its first
value. Those rules are the Column's
[Merge Policy](https://docs.popcorn.ai/merge-policy.md), declared in the
template (see [Table Columns](https://docs.popcorn.ai/table-columns.md)).
When a change is decided by one, your assistant says which Column.
