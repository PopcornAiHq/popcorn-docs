---
id: table-columns
title: Table Columns
order: 13
group: Tables and Status
summary: >
  A Routine's Tables and Columns are declared in its template's Manifest, as
  Questionnaire declares `recipients`: a Column has a name and one of five
  types; `format` is checked on every write, `display` only for its kind. A
  datetime or formatted Column is emptied with null, not "". Install adds
  Columns but never drops or renames one; a Flow dereferences only a
  space-free name.
lede: >
  How a template declares a Table's Columns, and what installing a new
  Version can and can't change about them.
concepts: [merge-policy, manifest-keys, adding-a-table]
---

A Routine's [Tables](https://docs.popcorn.ai/tables.md), and each Table's
Columns, are declared in its template's
[Manifest](https://docs.popcorn.ai/manifest-keys.md), under `tables:`. Each
[Install](https://docs.popcorn.ai/versions.md) reconciles them additively.

The Questionnaire template declares one Table, `recipients`, with one Row
per person asked (shortened here; the comments are the template's):

```yaml title="manifest.yaml"
tables:
  recipients:
    columns:
      - name: Email
        type: string
        format: email
        index: true
        pii: true
      - name: Name
        type: string
        pii: true
      - name: Status
        type: string
      - name: Why
        type: string
      - name: CTAs
        type: json
        internal: true
      - name: Stage
        type: string
      - name: Answers
        type: json
        label: Answers
      - name: Asked
        type: datetime
        merge: keep
      - name: Answered
        type: datetime
      - name: Follow Ups
        type: number
        label: Follow-ups
      - name: Last Asked
        type: datetime
        internal: true
      # Held by the run emailing or checking this recipient, so two
      # passes running at once can't both email them.
      - name: Sending
        type: string
        internal: true
    # One row per address: adding a recipient already there updates their
    # row and never asks them twice.
    merge_key:
      any_of: [Email]
      on_conflict: merge
```

What a repeat write does to each Column, and how the Merge Key on `Email`
picks the Row, is [Column Merge Policy](https://docs.popcorn.ai/merge-policy.md).
`Status`, `Why`, `CTAs` and `Stage` belong to the template's
[State Machine](https://docs.popcorn.ai/state-machine.md), which writes the
first three and their display hints.

## Type, format, display

`type` is `string | number | boolean | datetime | json`. Each `format`
belongs to one type: `string` takes `uuid`, `email`, `url`, `phone`, `ipv4`,
`ipv6`, `hex_color` or `slug`; `number` takes `integer`; `datetime` takes
`date`; `boolean` and `json` take none. Every write is checked against it,
so `recipients` refuses an `Email` that is not an address.

`display` is a rendering hint whose *kind* (the part before the first `:`)
is validated against the platform's list of display kinds. Its arguments
are not, so a misspelled display argument fails silently by simply not
rendering. `label` is the heading clients show in place of `name`, and the
one way to change what a Column is called on screen: `Follow Ups` shows as
*Follow-ups*.

> [!IMPORTANT] Empty a datetime Column with null
> A `datetime` Column, or any Column with a `format`, refuses `""`: an
> empty string is not a date or an address. Write `null` to empty it.
> Questionnaire's **Ask again** writes `Last Asked: null` so the next pass
> follows up at once.

## Governance flags

`pii`, `restricted`, `internal`, `outbound_ref`, `passthrough` and
`masked_read` are independent booleans. Questionnaire marks `Email` and
`Name` `pii`, and every Column a person has no use for `internal`: `CTAs`,
`Last Asked`, `Sending`, and the thread bookkeeping it doesn't show.
`internal: true` hides a Column from the user-facing UI, which is right for
raw payloads and bookkeeping ids. `outbound_ref` marks the recipient-facing
reference an Agent uses in outbound messages in place of a client's
identity. `masked_read` means anything only alongside `pii: true`.

## Names are permanent, and a Flow may need them space-free

Install never renames a Column. The `name` is the key every Row is stored
under, so a changed `name` adds a new Column next to the old one, which
keeps its data. Matching ignores case and surrounding whitespace, so a
case-only change adds nothing and the installed spelling stays.

A Column name may contain spaces if [Flows](https://docs.popcorn.ai/flow-grammar.md)
only ever *write* it (YAML map keys) or *filter* on it (JSON keys). It must
be made only of letters, digits and underscores, not starting with a digit,
if any Flow **dereferences** it, because `$row.Last Asked` is not
parseable:

```
steps[1](touch).args.text: malformed reference '$row.Last Asked' — not valid reference syntax …
```

Questionnaire's `Follow Ups` and `Last Asked` have spaces and do no harm:
its Flows write them in a `patch:`, and hand the whole Row to its code
block, which reads them as keys. A Copy whose Flow wanted `$row.Last Asked`
would need a space-free Column.

## The store accepts undeclared Columns

The store checks each value against its Column's `type`, `format` and
`required`, but it does not check that a key names a Column. Keys are
whitespace-trimmed, and one that matches a declared Column
case-insensitively is rejected with a "did you mean" naming it. Anything
further off is not: writing `Follow Up` when the schema says `Follow Ups`
silently succeeds and produces a Column no `$ref` can reach. Renaming a
Column means renaming every write site, and only reading a Row back catches
a miss.

> [!TIP] What is installed
> Ask your assistant for a Table's Columns: it calls `get_table`, which
> shows each Column's type, `label` and Merge Policy, whether it is
> `required` or `unique`, and the Table's Merge Key.

## With the CLI

Two things here have no MCP equivalent today: catching an undeclared
Column before a Run, and reading a Column's `format`, `display` and index.

`app validate` reports a Flow writing an undeclared Column
(`undeclared-column`) for the Tables its Manifest declares.
`popcorn table schema recipients --channel '#team-offsite'` prints what a
Routine has; add `--json` for the policies, `format`, `display`, `label`
and the Merge Key.
