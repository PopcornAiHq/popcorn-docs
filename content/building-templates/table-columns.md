---
id: table-columns
title: Table Columns
order: 10
group: Tables and Status
summary: >
  A Routine's Tables and Columns are declared in its template: a Column has a
  name and one of five types; `format` is checked on every write, while
  `display` is checked only for its kind. Install adds Columns and fixes
  attributes but never drops or renames one. A Flow can dereference only a
  Column whose name has no spaces.
lede: >
  How a template declares a Table's Columns, and what installing a new Version
  can and can't change about them.
concepts: [merge-policy, manifest-keys, adding-a-table]
---

A Routine's Tables, and each Table's Columns, are declared in its template's
Manifest, under `tables:`. Each Install reconciles them additively.

```yaml
tables:
  alerts:
    columns:
      - { name: Fingerprint, type: string, unique: true }
      - { name: Status, type: string }
      - { name: First Fired, type: datetime, merge: keep }
      - { name: Seen At, type: string, merge: concat }
      - { name: Firing Count, type: number, merge: increment_on_change,
          merge_when: { column: Status, from: resolved, to: firing } }
      - { name: Raw, type: json, internal: true }
    merge_key:
      any_of: [Fingerprint]
      on_conflict: merge
```

What a repeat write does to each Column, and how a Merge Key picks the Row,
is [Column Merge Policy](https://docs.popcorn.ai/merge-policy.md).

## Type, format, display

`type` is `string | number | boolean | datetime | json`. Each `format`
belongs to one type: `string` takes `uuid`, `email`, `url`, `phone`, `ipv4`,
`ipv6`, `hex_color` or `slug`; `number` takes `integer`; `datetime` takes
`date`; `boolean` and `json` take none. Every write is checked against it.

`display` is a rendering hint whose *kind* (the part before the first `:`) is
validated against the platform's list of display kinds. Its arguments are
not, so a misspelled display argument fails silently by simply not rendering.
`label` is the heading clients show in place of `name`, and the one way to
change what a Column is called on screen.

## Governance flags

`pii`, `restricted`, `internal`, `outbound_ref`, `passthrough` and
`masked_read` are independent booleans. `internal: true` hides a Column from
the user-facing UI, which is right for raw payloads and bookkeeping ids.
`outbound_ref` marks the recipient-facing reference an Agent uses in outbound
messages in place of a client's identity. `masked_read` means anything only
alongside `pii: true`.

## Names are permanent, and a Flow may need them space-free

Install never renames a Column. The `name` is the key every Row is stored
under, so a changed `name` adds a new Column next to the old one, which keeps
its data. Matching ignores case and surrounding whitespace, so a case-only
change adds nothing and the installed spelling stays.

A Column name may contain spaces if Flows only ever *write* it (YAML map keys)
or *filter* on it (JSON keys). It must be made only of letters, digits and
underscores, not starting with a digit, if any Flow **dereferences** it,
because `$row.Last Seen` is not parseable:

```
steps[1](touch).args.text: malformed reference '$row.Last Seen'
```

## The store accepts undeclared Columns

The store checks each value against its Column's `type`, `format` and
`required`, but it does not check that a key names a Column. Keys are
whitespace-trimmed, and one that matches a declared Column case-insensitively
is rejected with a "did you mean" naming it. Anything further off is not:
writing `Post Message Id` when the schema says `PostMessageId` silently
succeeds and produces a Column no `$ref` can reach. Renaming a Column means
renaming every write site, and only reading a Row back catches a miss.
`app validate` reports a Flow writing an undeclared Column
(`undeclared-column`) for the Tables its Manifest declares.

Check what is actually installed with `popcorn table schema <table>`, and add
`--json` for the policies, `format`, `display`, `label` and the Merge Key.
