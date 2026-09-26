---
id: adding-a-table
title: Adding a table
order: 3
summary: >
  Adding a table to an app that already exists: declare it under `tables:`,
  write it from a flow with `foundation.store.*`, run `template check`, then
  `app publish` from a fork line. Install creates the table, and each later
  install adds to it and never removes. A merge policy other than `replace`
  survives every later publish, so choose each before the first.
concepts: [manifest-keys, merge-policy, fork-line, publish-and-apply, app-bundle]
applies_to: [cli, human]
source: [ColumnDef, SchemaDef, MergeKeyDef, apply_tables, reconcile_columns, carry_merge_forward, validate_record, upsert_rows]
---

This guide adds one table to an app a channel already runs, and ends with
the table on the channel and a flow writing rows to it. The loop around it
(fork, edit, check, publish) is the one in
[authoring an app bundle](https://docs.popcorn.ai/guides/template-authoring.md),
and that guide's §5 is the column reference. This one is the order to do
things in, and the choices you cannot take back afterwards.

The running example adds a `handoffs` table to an app on `#example-intake`:
one row per ticket handed to someone, where a repeat hand-off updates the
row instead of adding another one.

## 1. Check out a fork

A publish lands on a fork line your workspace owns, so fork before you edit:

```bash
popcorn app checkout --channel '#example-intake' --fork
cd <app>
```

If the channel is already on a fork, `app checkout --channel '#example-intake'`
is enough. Forking is permanent, and a publish reaches every channel on the
line, not only this one. See
[fork lines](https://docs.popcorn.ai/concepts/fork-line.md) before forking a
production channel.

## 2. Declare the table

Add it under `tables:` in `manifest.yaml`. The key is the table's name, which
is what every flow step passes as `table_name`.

```yaml
tables:
  handoffs:
    columns:
      - { name: TicketId, type: string, unique: true }
      - { name: Owner, type: string, format: email }
      - { name: Stage, type: string,
          display: "status:open,waiting,done;warn=waiting" }
      - { name: First Seen, type: datetime, merge: keep }
      - { name: Notes, type: string, merge: concat }
      - { name: Reopened, type: number, merge: increment_on_change,
          merge_when: { column: Stage, from: done, to: open } }
      - { name: Raw, type: json, internal: true }
    merge_key:
      any_of: [TicketId]
      on_conflict: merge
```

A column has a `name` and a `type`, and everything else is optional:

| Key | Values |
|---|---|
| `type` | `string`, `number`, `boolean`, `datetime` (an ISO-8601 string), `json` |
| `format` | checked on every write. `string`: `uuid`, `email`, `url`, `phone`, `ipv4`, `ipv6`, `hex_color`, `slug`. `number`: `integer`. `datetime`: `date`. `boolean` and `json` take none |
| `display` | a rendering hint such as `status:…`, `currency:USD` or `relative`. Only the part before the first `:` is checked |
| `label` | the heading clients show in place of `name` |
| `required` | every row written must carry a non-null value |
| `index`, `unique` | indexes the column for filtering and sorting, and `unique` also rejects a duplicate value. `string`, `number` and `datetime` only |
| `merge`, `merge_separator`, `merge_when` | what a merging write does to the stored value (step 3) |
| `internal`, `pii`, `restricted`, … | governance flags, listed in the authoring guide's §5 |

Pick the column names now, because install never renames a column. The
`name` is the key every row is stored under, and a changed `name` adds a new
column next to the old one. To change what people see, change `label`
instead. A column a flow reads as `$row.<name>` must have no spaces in its
name. `TicketId` is written that way for that reason, while `First Seen` is
only ever written or filtered on, so the space does no harm.

A table declared with no columns is skipped. Install does not create it.

## 3. Decide what a repeat write does

This is the step that is hard to undo, so it comes before any flow is
written.

**The merge key decides which row a write lands on.** `merge_key.any_of`
names the columns that identify a row, so a write whose `TicketId` matches an
existing row updates that row rather than inserting a new one. Each merge-key
column must be a `string` column (or a computed one) and must be indexed,
with `unique: true` or `index: true`. While the table declares a merge key,
the per-call `merge_on` and `on_conflict` arguments of
`foundation.store.upsert_rows` are ignored, and the table's
`merge_key.on_conflict` (default `merge`) applies to every write.

**The merge policy decides what happens to each column on that row.** There
are four policies, `replace`, `concat`, `keep` and `increment_on_change`, and
[column merge policy](https://docs.popcorn.ai/concepts/merge-policy.md) is
the authoritative page for them. The example uses three:

- `First Seen: keep`: the first hand-off's time stays, however often the
  ticket comes back.
- `Notes: concat`: every hand-off's note is appended, newest last.
- `Reopened: increment_on_change`: counts `done` → `open` transitions of
  `Stage`, and ignores the value the write sends.

**Choose each policy before the first publish.** Install writes the table as
the platform, and when the platform changes a schema, the store keeps any
policy other than `replace` that a column already has. You can add a policy
to a `replace` column by publishing a new version. Once a column is `concat`,
`keep` or `increment_on_change`, though, a later manifest that says
`merge: replace`, or a different policy, is overridden and the old policy
stays. The publish succeeds and nothing reports the override. If you need a
different policy, add a new column.

## 4. Write to it from a flow

Flows reach the table through the `foundation.store.*` activities, naming it
by `table_name`:

```yaml
name: record_handoff
version: 1
description: One row per ticket handed off; a repeat merges into it.
inputs:
  conversation_id: { type: string }
  ticket: { type: string }
  owner: { type: string }
  note: { type: string, required: false, default: "" }

steps:
  - id: now
    activity: foundation.workflow.now

  - id: write
    activity: foundation.store.upsert_rows
    on_error: { policy: fail, retry: 0 }
    args:
      conversation_id: $inputs.conversation_id
      table_name: handoffs
      rows:
        - TicketId: $inputs.ticket
          Owner: $inputs.owner
          Stage: open
          First Seen: $steps.now.output.iso
          Notes: $inputs.note
          Reopened: 0
```

The write sends every column on every call, and that is deliberate. On the
first write the row is inserted, and it holds exactly what was sent, so
`Reopened` starts at `0`. On every later write the policies apply, and the
accumulating ones act only on columns the write carries. A write that left
out `Reopened` would never count, and one that left out `First Seen` would
leave a first-time row without it.

The other activities you will usually need are:

- `foundation.store.list_rows`: `filter` selects rows in the database, and
  each row in `.output.rows` carries `_record_id`.
- `foundation.store.patch_row`: changes named cells of one row by
  `record_id`. Pass `expected_rev` (the row's `_rev`) when another writer may
  have changed the row since you read it.
- `foundation.store.get_record`: reads one row by id.

Their arguments are in the
[activity reference](https://docs.popcorn.ai/reference/activities.md).

The store checks each value against its column's `type`, `format` and
`required`. It does not check column names: a key it does not know is stored
silently, unless the key differs from a declared column only by case. A
write to a table the channel does not have fails the step.

## 5. Check it offline

```bash
popcorn template check .
```

`template check` reads the manifest and the flows together. It does not
check everything, though, and a problem it misses shows up at a later stage:

| Mistake | Caught by |
|---|---|
| a merge-key column that is undeclared, not a string, or not indexed | `template check`: `merge-key-unknown-column`, `merge-key-not-string`, `merge-key-not-indexed` |
| `merge: concat` on a column that is not a string | `template check`: `concat-requires-string` |
| a flow writing a column the table does not declare | `template check`: `undeclared-column` |
| a filter on an undeclared column | `template check`, as a warning: `unknown-filter-column` |
| an unknown `type`, a `format` that does not suit the type, `increment_on_change` without `merge_when`, an index on a `boolean` or `json` column | install, which fails |
| a `table_name` misspelled in a flow | the run, whose step fails |

Publish does not validate column definitions, so the mistakes in the fifth
row get through a publish and then fail the install. Check every `table_name` by eye,
because `template check` only compares columns for tables the manifest
declares.

## 6. Publish

```bash
popcorn app publish . --bump patch -m "add handoffs table" --yes
```

Publishing needs workspace-admin rights. The publish mints the next version
on the fork line and starts an install on this channel. That install creates
the `handoffs` table before it binds the channel to the new version, so no
run on the new version can reach a channel without the table. Every other
channel on the line gets the table at its own daily update. The publish
prints how many channels that is, but only after the version exists. See
[publish and apply](https://docs.popcorn.ai/concepts/publish-and-apply.md).

If a column definition is invalid, the publish still succeeds, but the
install fails before it binds. The channel then stays on its previous
version, and so does every other channel that tries to update. The fix is
another publish.

## 7. Confirm it landed

```bash
popcorn app status .                                    # install_state: current?
popcorn table schema handoffs --channel '#example-intake'
```

`app status` says whether the channel runs the line's head. `table schema`
prints the installed columns with `unique`, `required`, `internal`, `pii`,
`restricted` and `concat` flagged. It does not show `keep`,
`increment_on_change`, `index` or the merge key, so add `--json` to see the
whole schema.

Then write a row, write it again, and read it back:

```bash
popcorn flow run record_handoff --channel '#example-intake' \
  --inputs '{"ticket":"T-1","owner":"a@example.com","note":"first"}' --wait
popcorn flow run record_handoff --channel '#example-intake' \
  --inputs '{"ticket":"T-1","owner":"a@example.com","note":"second"}' --wait
popcorn table rows handoffs --channel '#example-intake'
```

You should see one row, with both notes in `Notes` and `First Seen` still
holding the first run's time. Two rows mean the merge key did not match,
which a schema check alone cannot show you.

## Changing the table later

Each later publish reconciles the table toward the manifest, and only ever
adds to it:

- **Follows the manifest:** new columns are added, and column order is the
  manifest's. On a column already there, `type`, `format`, `display` and
  `label` are set to exactly what the manifest says, and removed if the
  manifest leaves them out.
- **Changes only when declared:** `index`, `unique`, `required`, the
  governance flags and a `replace` column's `merge` keep their installed value
  unless the manifest states a new one. Deleting `unique: true` leaves the
  column unique; write `unique: false`. A `merge_key` the manifest declares
  replaces the installed one, and one it leaves out stays in place.
- **Never changes:** a column is never removed or renamed, and a column's
  existing policy other than `replace` stays (step 3). Columns are matched
  by name, ignoring case and extra whitespace, and a matched column keeps its
  installed spelling.

A column you stop declaring stays on the table with its data, after the
declared ones. Removing a column from the manifest does not remove it from
the table.
