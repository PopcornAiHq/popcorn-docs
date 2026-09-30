---
id: merge-policy
title: Column merge policy
order: 5
group: What a bundle holds
summary: >
  A column's merge policy decides what an upsert does to an existing row:
  replace (the default, last-write-wins), concat (append to a string), keep
  (first-write-wins) or increment_on_change (a counter that rises when another
  column makes a declared transition). Policies apply only on a merging
  write. An install sets the declared policy; stored values change on their
  next write.
concepts: [manifest-keys]
applies_to: [cli, mcp, human]
source: [ColumnDef, MergeWhenDef, apply_column_merge, reconcile_columns, carry_merge_forward]
---

A table column carries a merge policy that decides what happens when a write
lands on a row that already exists. There are four:

| `merge:` | What the stored value becomes | Column type |
|---|---|---|
| `replace` (default) | the incoming value | any |
| `concat` | the stored value, a separator, then the incoming value | string |
| `keep` | unchanged, once it holds a non-blank value | any |
| `increment_on_change` | the stored number plus one, when a sibling column makes a declared transition | number |

```yaml
- { name: First Fired, type: datetime, merge: keep }
- { name: Seen At,     type: string,   merge: concat }
- { name: Firing Count, type: number,
    merge: increment_on_change,
    merge_when: { column: Status, from: resolved, to: firing } }
```

## A policy only applies when the write merges

Policies act when a write **merges** into an existing row: an upsert with
`on_conflict: merge`, or a patch. The upsert's own default is `replace`, which
swaps the whole row for the incoming one — every policy is ignored and any
column the write omits is dropped.

A table that declares a schema-level `merge_key` resolves conflicts through
its `merge_key.on_conflict`, whose default is `merge`, and ignores a per-call
`merge_on`.

The accumulating policies — `concat`, `keep` and `increment_on_change` — act
only on a column the write carries. A patch that leaves a column out leaves it
untouched, so a write that should count must include the counter column; the
value it sends is discarded.

## First seen is `keep`

A column recording *the first time this happened* is `merge: keep`. Every
later write to it is ignored once it holds a value, so re-fires cannot move it.

## Counting is `increment_on_change`

The counter counts **transitions, not writes.** `merge_when` names a different
column and an exact `from`/`to` pair; the counter rises by one only when that
column goes from one to the other on a merge. The two values are compared
case-insensitively and must differ.

An insert never merges, so the row's first value is whatever the write sends —
send the starting count.

When the history matters more than the number, `concat` keeps the history:
one entry per write, newest last, separated by a newline unless
`merge_separator` says otherwise. A step's own retry does not append twice:
a store write carries its run and step, and a retry of a write that already
committed replays the stored response. Anything else that sends the value
again — a new run, another step — appends it, and the only duplicate `concat`
skips is an incoming value equal to the whole stored value. Because `concat` requires a string column, a timestamp
history is a **string** column, not a datetime one.

## Changing a column's policy

A bundle install sets each column's policy to what the manifest declares:

- A `merge:` that differs from the installed one replaces it. The old
  policy's `merge_separator` or `merge_when` goes with it unless the
  manifest restates one.
- Restating the same policy with a new `merge_separator` changes the
  separator; leaving it out keeps the installed one.
- An omitted `merge:` keeps the installed policy, unless the same install
  retypes the column out of what the policy requires (`concat` off `string`,
  `increment_on_change` off `number`). Then the column becomes `replace`.

**Stored values are not rewritten.** The new policy applies to a row the
next time a write merges into it. After `concat` becomes `replace`, a row
keeps its accumulated text until its next write replaces it; after `replace`
becomes `keep`, the value a row already holds is the one kept.

A schema change made by the channel's agent cannot change a policy: the
store carries the installed one forward. It drops to `replace` only when
that change leaves the column unable to hold it: retyped out of what the
policy requires, or an `increment_on_change` column whose `merge_when`
column is gone.

## Merge keys must be indexed strings

The columns in a schema's `merge_key.any_of` must be indexed — `index: true`,
`unique: true`, or computed — and string-typed unless computed. `app publish`
refuses a manifest that breaks either rule, so it never reaches an install. A
merge key set on the channel rather than in the manifest is checked when the
install writes the table, so a manifest that declares `index: false` on one
of its columns fails that install.
