---
id: merge-policy
title: Column merge policy
summary: >
  Every table column is last-write-wins. The only other policy is concat,
  which appends to a string column. There is no "keep the existing value", so
  a first-seen timestamp must be written by a separate step or every re-fire
  overwrites it.
concepts: [manifest-keys, table-schema]
applies_to: [cli, mcp, human]
source: [reconcile_columns, ColumnDef]
---

A table column carries a merge policy that decides what happens when a row is
upserted onto an existing row. There are two:

- **replace** (the default) — the incoming value wins.
- **concat** — the incoming value is appended to the existing string, with a
  separator. Requires a string column.

That is the whole vocabulary, and the absence is the important part.

## There is no "keep the existing value"

A column that should record *the first time we saw this* cannot be written by
the upsert that also records the latest state. Every re-fire would overwrite
it with the current timestamp.

Write it in a separate step, gated on the row having just been created. The
upsert reports whether it created or matched; that flag is what the gate reads.

This is the single most common way a tracker table ends up quietly wrong: the
column exists, it is populated, every value is today's.

## concat is how you count

There is no arithmetic anywhere in a flow — nothing adds, subtracts or
increments. So a "how many times has this happened" column cannot be a counter.

Accumulate with a `concat` string column and let whoever reads it count the
entries. This is deliberate rather than an omission: a counter column would
need read-modify-write semantics that a retried step cannot make safe, and the
concat history is strictly more informative than the number.

A consequence worth knowing: a timestamp history must be a **string** column,
not a datetime one, because `concat` requires a string.

## Merge keys are narrower than they look

The columns that identify a row for upsert must be **indexed** and
**string-typed**. A non-string merge key silently never matches — the probe
only queries the text index — so instead of an error you get a second row
every time.

Declaring a column unique satisfies the indexed requirement.
