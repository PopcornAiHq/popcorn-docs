---
id: table-columns
title: Table columns
order: 6
group: What a bundle holds
summary: >
  A column has a name and one of five types; `format` is checked on every
  write, while `display` is checked only for its kind. Install adds columns and
  fixes attributes but never drops or renames one. A flow can dereference only
  a column whose name has no spaces, and the store silently accepts a key no
  column declares unless it differs from one only by case.
concepts: [merge-policy, manifest-keys, adding-a-table]
layer: platform
---

A bundle declares its tables under `tables:` in the manifest. Each install
reconciles them additively. In the product a table is a Routine's **Table**,
and each column a **Column**.

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

What a repeat write does to each column, and how a merge key picks the row,
is [column merge policy](https://docs.popcorn.ai/platform/concepts/merge-policy.md).

## Type, format, display

`type` is `string | number | boolean | datetime | json`. Each `format`
belongs to one type: `string` takes `uuid`, `email`, `url`, `phone`, `ipv4`,
`ipv6`, `hex_color` or `slug`; `number` takes `integer`; `datetime` takes
`date`; `boolean` and `json` take none. Every write is checked against it.

`display` is a rendering hint whose *kind* (the part before the first `:`) is
validated against the platform's list of display kinds. Its arguments are
not, so a misspelled display argument fails silently by simply not rendering.
`label` is the heading clients show in place of `name`, and the one way to
change what a column is called on screen.

## Governance flags

`pii`, `restricted`, `internal`, `outbound_ref`, `passthrough` and
`masked_read` are independent booleans. `internal: true` hides a column from
the user-facing UI, which is right for raw payloads and bookkeeping ids.
`outbound_ref` marks the recipient-facing reference an agent uses in outbound
messages in place of a client's identity. `masked_read` means anything only
alongside `pii: true`.

## Names are permanent, and a flow may need them space-free

Install never renames a column. The `name` is the key every row is stored
under, so a changed `name` adds a new column next to the old one, which keeps
its data. Matching ignores case and surrounding whitespace, so a case-only
change adds nothing and the installed spelling stays.

A column name may contain spaces if flows only ever *write* it (YAML map keys)
or *filter* on it (JSON keys). It must be made only of letters, digits and
underscores, not starting with a digit, if any flow **dereferences** it,
because `$row.Last Seen` is not parseable:

```
steps[1](touch).args.text: malformed reference '$row.Last Seen'
```

## The store accepts undeclared columns

The store checks each value against its column's `type`, `format` and
`required`, but it does not check that a key names a column. Keys are
whitespace-trimmed, and one that matches a declared column case-insensitively
is rejected with a "did you mean" naming it. Anything further off is not:
writing `Post Message Id` when the schema says `PostMessageId` silently
succeeds and produces a column no `$ref` can reach. Renaming a column means
renaming every write site, and only reading a row back catches a miss.
`app validate` reports a flow writing an undeclared column
(`undeclared-column`) for the tables its manifest declares.

Check what is actually installed with `popcorn table schema <table>`, and add
`--json` for the policies, `format`, `display`, `label` and the merge key.
