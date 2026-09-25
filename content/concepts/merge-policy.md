---
id: merge-policy
title: Column merge policy
order: 5
group: What a bundle holds
summary: >
  A column's merge policy decides what an upsert does to an existing row:
  replace (the default, last-write-wins), concat (append to a string), keep
  (first-write-wins) or increment_on_change (a counter that rises when another
  column makes a declared transition). Policies apply only when the write
  merges, which is not the upsert default.
concepts: [manifest-keys]
applies_to: [cli, mcp, human]
source: [ColumnDef, MergeWhenDef, apply_column_merge]
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
`merge_separator` says otherwise. It is not idempotent — a retried step
appends again, and the only duplicate it skips is an incoming value equal to
the whole stored value. Because `concat` requires a string column, a timestamp
history is a **string** column, not a datetime one.

## Merge keys must be indexed strings

The columns in a schema's `merge_key.any_of` must be indexed — `index: true`,
`unique: true`, or computed — and string-typed unless computed. A table that
breaks either rule is refused when its schema is validated, so the install
fails rather than producing duplicate rows.
