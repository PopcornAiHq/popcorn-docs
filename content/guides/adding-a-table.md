---
id: adding-a-table
title: Adding a table
order: 4
summary: >
  Adding a table to an app that already exists: declare it under `tables:`,
  write it from a flow with `foundation.store.*`, run `template check`, then
  `app publish` from a fork line. Install creates the table, and each later
  install adds to it and never removes. Publish refuses a column the store
  would reject. A later publish can change a merge policy; stored rows keep
  values until their next write.
concepts: [manifest-keys, merge-policy, fork-line, publish-and-apply, app-bundle]
applies_to: [cli, human]
source: [ColumnDef, SchemaDef, MergeKeyDef, manifest_table_errors, apply_tables, reconcile_columns, carry_merge_forward, apply_column_merge, validate_record, upsert_rows]
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

A column needs a `name` and a `type`. The authoring guide's §5 lists the
rest: `display`, the governance flags, `index` and `unique`. Two things it
does not say:

- **Each `format` belongs to one `type`.** `string` takes `uuid`, `email`,
  `url`, `phone`, `ipv4`, `ipv6`, `hex_color` or `slug`. `number` takes
  `integer`, and `datetime` takes `date`. `boolean` and `json` take none.
  Every write is checked against the format.
- **`label` is the heading clients show in place of `name`.** It is the one
  way to change what a column is called on screen.

Choose the names now, because install never renames a column. The `name`
is the key every row is stored under, so a changed `name` adds a new column
next to the old one. A change of case alone adds nothing. The installed
spelling stays, and a flow that writes the new spelling is refused with a
"did you mean". A column that any `$` reference reads, such
as `$row.TicketId` in a `foreach`, needs a name made only of letters, digits
and underscores that does not start with a digit. The authoring guide's §5
has the rule. `First Seen` is only ever written or filtered on, so its space
does no harm.

A table declared with no columns is skipped. Install does not create it.

## 3. Decide what a repeat write does

This step comes before any flow is written, because the flows are built
around it and a later change does not rewrite what is already stored.

The merge key decides which row a write lands on, and each column's merge
policy decides what happens to that column on that row. Both are explained
in [column merge policy](https://docs.popcorn.ai/concepts/merge-policy.md).
Keep `on_conflict: merge`: `replace` swaps the whole row for the incoming one
and applies no column policy at all. The example uses three policies:

- `First Seen: keep`: the first hand-off's time stays, however often the
  ticket comes back.
- `Notes: concat`: every hand-off's note is appended, newest last.
- `Reopened: increment_on_change`: counts `done` → `open` transitions of
  `Stage`, and ignores the value the write sends.

**Choose each policy before the first publish.** A later publish can change
a column's policy (see "Changing the table later" below),
but it does not rewrite the values already stored: a row that accumulated
text under `concat` keeps it until its next write. Choosing now avoids a
table whose older rows were built under a different rule.

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

The write sends every column on every call. The first write inserts the
row exactly as sent, so `Reopened` starts at `0`. After that, the
accumulating policies act only on columns a write carries (see
[column merge policy](https://docs.popcorn.ai/concepts/merge-policy.md)).

The other activities you will usually need are:

- `foundation.store.list_rows`: `filter` selects rows in the database, and
  each row in `.output.rows` carries `_record_id`.
- `foundation.store.patch_row`: changes named cells of one row by
  `record_id`. It is a merging write, so the policies apply: a `concat` cell
  appends, a `keep` cell that holds a value ignores the patch, and a counter
  ignores the value it is sent. Pass `expected_rev` (the row's `_rev`) when
  another writer may have changed the row since you read it.
- `foundation.store.get_record`: reads one row by id.

Their arguments are in the
[activity reference](https://docs.popcorn.ai/reference/activities.md).

The store checks each value against its column's `type`, `format` and
`required`. On a merging write, including `patch_row`, it checks the whole
merged row, not only the cells the write sent. The store trims whitespace
from keys, but it does not check that a key names a column: an unknown key
is stored silently, unless it differs from a declared column only by case.

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
| any other invalid column definition: an unknown `type` or `display` kind, a `format` that does not suit the type, an index on `boolean` or `json`, a `merge_separator` or `merge_when` without the policy that takes it, a `merge_when` naming a missing column or its own column, or a `from` equal to its `to`, two column names that differ only by case, two table names that differ only by case, a table or column name containing U+FDD0 or U+FDD1 | `app publish`, which refuses it |
| a `table_name` misspelled in a flow | the run: a write fails the step, while a `list_rows` with `missing_ok: true` reads the missing table as empty |

`template check` does not report the fifth row; `app publish` does, before
any version exists (step 6). Check every `table_name` by eye, because
`template check` only compares columns for tables the manifest declares.

## 6. Publish

```bash
popcorn app publish . --bump patch -m "add handoffs table" --yes
```

Publishing needs workspace-admin rights. The publish mints the next version
on the fork line and starts an install on this channel. That install creates
the `handoffs` table before it binds the channel to the new version, so no
run on the new version can reach a channel without the table. The other
channels on the line get the table at their own daily update, apart from the
ones that take no updates (see
[publish and apply](https://docs.popcorn.ai/concepts/publish-and-apply.md)).
The publish prints how many channels will update, but only after the version
exists.

Publish runs every `tables:` entry through the same validation the store
applies at install, and refuses the whole publish if any would be rejected.
Nothing is written: no version is minted, and a `--bump` is not saved to
`manifest.yaml`, so re-running the same command after the fix is the retry.
The CLI prints the refusal to stderr and exits 3:

```
Error: manifest tables: the agent store would refuse these at install, so the bundle cannot be published:
  tables.handoffs: column 'Stage': display: unknown display kind 'statu'; valid: [...]
  tables.handoffs: column 'Notes': column 'Notes': merge='concat' requires a string column, got type 'number'
```

Each line names the table and, where there is one, the column. The findings
for every table come back in one refusal, although the checks that compare
columns with each other (a `merge_when` reference, duplicate names, the
merge key) run only once each column of that table is valid on its own. With
`--json`, the same text is the `error` field, with `status: 422` and
`error_code: validation`.

Publish checks the manifest's columns on their own. It cannot see a
channel's table, and the install validates the schema it builds by merging
the manifest with the columns already live there. A combination only that
channel has can still fail the install: retyping a column the channel
already indexes to `boolean` or `json`, for instance, without writing
`index: false` and `unique: false`, since those keep their installed value
unless the manifest states one. A failed install stops before it binds. The
channel keeps its previous version, but not necessarily its previous tables:
a table listed before the failing one may already have been created or
changed. The fix is another publish.

## 7. Confirm it landed

```bash
popcorn app status .
popcorn table schema handoffs --channel '#example-intake'
```

Inside a checkout, `app status` says either that the channel runs the line's
head, or that it is behind, and then why: an install still running or
retrying, or one that failed, was skipped or is locked out. A failed install
shows its error and error code, and a `Next:` line says what moves the channel on — usually
`app apply`. In `--json`, from a checkout or from outside one with
`--channel`, branch on `install.state`.

`table schema` prints each column's name and type, and flags `unique`,
`required`, `internal`, `pii`, `restricted` and `concat`. To see everything
else, including the other policies, `format`, `display`, `label` and the
merge key, add `--json`.

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
- **Changes only when declared:** `index`, `unique`, `required` and the
  governance flags keep their installed value unless the manifest states a
  new one. Deleting `unique: true` leaves the
  column unique; write `unique: false`. A `merge_key` the manifest declares
  replaces the installed one, and one it leaves out stays in place.
- **Merge policy follows a declared `merge:`.** A `merge:` that differs from
  the installed one replaces it, and the old policy's `merge_separator` or
  `merge_when` is dropped unless the manifest restates one. An omitted
  `merge:` keeps the installed policy, unless the same publish retypes the
  column out of what that policy requires (`concat` off `string`,
  `increment_on_change` off `number`); then the column becomes `replace`.
- **Never changes:** a column is never removed or renamed. Columns are matched by name, ignoring
  case and extra whitespace, and a matched column keeps its installed
  spelling.
- **Existing rows are not rewritten.** A new `type`, `format`, `required`
  or merge policy applies to the rows already stored the next time anything
  merges into them. After `concat` becomes `replace`, a row keeps its
  accumulated text until its next write replaces it. A merging write or a `patch_row` checks the whole merged row, so it
  can fail on an old value in a column the write never touched.

A column you stop declaring stays on the table with its data, after the
declared ones. Removing a column from the manifest does not remove it from
the table.
