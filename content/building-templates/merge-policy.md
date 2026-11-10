---
id: merge-policy
title: Column Merge Policy
order: 14
group: Tables and Status
summary: >
  A Column's Merge Policy decides what a write does to an existing Row:
  replace (the default, last-write-wins), keep (first-write-wins: the first
  time a Row was seen never changes on later updates, as Questionnaire's
  Asked), concat (append; a timestamp history is a string Column, not a
  datetime) or increment_on_change (a counter). The Merge Key, such as
  Email, picks the Row.
lede: >
  What happens to an existing Row when a Flow writes it again: replace it,
  append to it, keep the first value, or count changes.
concepts: [table-columns, manifest-keys]
---

Every Column in a Routine's [Tables](https://docs.popcorn.ai/tables.md) has
a Merge Policy, which decides what happens when a write lands on a
[Row](https://docs.popcorn.ai/tables.md) that already exists. There are
four:

| `merge:` | What the stored value becomes | Column type |
|---|---|---|
| `replace` (default) | the incoming value | any |
| `concat` | the stored value, a separator, then the incoming value | string |
| `keep` | unchanged, once it holds a non-blank value | any |
| `increment_on_change` | the stored number plus one, when a sibling Column makes a declared transition | number |

The Questionnaire template's `recipients` Table uses two of them: `keep`
on `Asked`, and the default `replace` on every other Column.

```yaml title="manifest.yaml"
tables:
  recipients:
    columns:
      - name: Email
        type: string
        format: email
        index: true
        pii: true
      # …
      - name: Asked
        type: datetime
        merge: keep
    merge_key:
      any_of: [Email]
      on_conflict: merge
```

## The Merge Key picks the Row

A Table's `merge_key` names the Columns a write is matched on. In
`recipients` it is `Email`, so adding a recipient whose address is already
there merges into their Row instead of adding a second one, and they are
never asked twice. Matching trims surrounding whitespace and ignores case,
so `Ana@Example.com ` lands on `ana@example.com`.

> [!TIP] MCP tool call
> When your assistant adds Rows with `create_rows`, its dry run says which
> Rows would be added and which merged into one already there.

The Columns in `merge_key.any_of` must be indexed (`index: true`,
`unique: true`, or computed) and string-typed unless computed: `Email` is
`index: true`. `app publish` refuses a Manifest that breaks either rule, so
it never reaches an Install. A Merge Key set on the Routine rather than in
the Manifest is checked when the Install writes the Table, so a Manifest
that declares `index: false` on one of its Columns fails that Install.

## A policy only applies when the write merges

Policies act when a write **merges** into an existing Row: an upsert with
`on_conflict: merge`, or a patch. Questionnaire's
[Flows](https://docs.popcorn.ai/flow-grammar.md) write `recipients` with
`foundation.store.patch_row`, so every one of their writes merges. The
upsert's own default is `replace`, which swaps the whole Row for the
incoming one: every policy is ignored and any Column the write omits is
dropped.

A Table that declares a schema-level `merge_key` resolves conflicts through
its `merge_key.on_conflict`, whose default is `merge`, and ignores a
per-call `merge_on`.

The accumulating policies (`concat`, `keep` and `increment_on_change`) act
only on a Column the write carries. A patch that leaves a Column out leaves
it untouched, so a write that should count must include the counter Column;
the value it sends is discarded.

## First seen is `keep`

A Column recording *the first time this happened* is `merge: keep`. Every
later write to it is ignored once it holds a value, so re-fires cannot move
it.

In Questionnaire, `Asked` is the time the first email went. A recipient
whose Email is corrected is asked afresh at the new address, and that
second email writes `Asked` again, but the stored time stays the first.
`Last Asked`, which moves with every follow-up, is `replace`.

> [!NOTE] Answers are kept by code, not by a policy
> `Answers` is a `json` Column with `replace`. Questionnaire never loses an
> answer because its code block merges each reply into the answers already
> stored and writes the whole map back. No policy merges inside a JSON
> value.

## A history is `concat`

When every value matters, `concat` keeps them all: one entry per write,
newest last, separated by a newline unless `merge_separator` says
otherwise. Questionnaire has no such Column; a Copy that wanted a line per
email sent would add one, as
[adding a Table or a Column](https://docs.popcorn.ai/adding-a-table.md)
does with `Emails Sent`.

A Step's own retry does not append twice: a store write carries its
[Run](https://docs.popcorn.ai/history.md) and Step, and a retry of a write
that already committed replays the stored response. Anything else that
sends the value again (a new Run, another Step) appends it, and the only
duplicate `concat` skips is an incoming value equal to the whole stored
value.

> [!IMPORTANT] A timestamp history is a string Column
> `concat` requires a `string` Column, so a history of times is declared
> `type: string`, not `datetime`.

## Counting is `increment_on_change`

Questionnaire's `Follow Ups` is a plain `number` its code block computes,
so the example here is another Table's: an alert that counts how often it
fired again after resolving.

```yaml title="manifest.yaml"
- { name: Status, type: string }
- { name: Firing Count, type: number,
    merge: increment_on_change,
    merge_when: { column: Status, from: resolved, to: firing } }
```

The counter counts **transitions, not writes.** `merge_when` names a
different Column and an exact `from`/`to` pair; the counter rises by one
only when that Column goes from one to the other on a merge. The two values
are compared case-insensitively and must differ.

An insert never merges, so the Row's first value is whatever the write
sends: send the starting count.

## Changing a Column's policy

A Bundle [Install](https://docs.popcorn.ai/versions.md) sets each Column's
policy to what the Manifest declares:

- A `merge:` that differs from the installed one replaces it. The old
  policy's `merge_separator` or `merge_when` goes with it unless the
  Manifest restates one.
- Restating the same policy with a new `merge_separator` changes the
  separator; leaving it out keeps the installed one.
- An omitted `merge:` keeps the installed policy, unless the same Install
  retypes the Column out of what the policy requires (`concat` off
  `string`, `increment_on_change` off `number`). Then the Column becomes
  `replace`.

**Stored values are not rewritten.** The new policy applies to a Row the
next time a write merges into it. After `concat` becomes `replace`, a Row
keeps its accumulated text until its next write replaces it; after
`replace` becomes `keep`, the value a Row already holds is the one kept.

A schema change made by the Routine's
[Agent](https://docs.popcorn.ai/agent.md) cannot change a policy: the store
carries the installed one forward. It drops to `replace` only when that
change leaves the Column unable to hold it: retyped out of what the policy
requires, or an `increment_on_change` Column whose `merge_when` Column is
gone.
