---
id: adding-a-table
title: Add a Table
order: 11
group: What a Bundle holds
summary: >
  Adding a Table to a Routine Template that already exists: declare it under
  `tables:`, write it from a Flow with `foundation.store.*`, run `app
  validate`, then `app publish` from the Workspace's Copy of it. Install creates the Table,
  and each later Install adds to it and never removes. Publish refuses a
  Column the store would reject; a later Publish can change a Merge Policy.
lede: >
  Add a new Table to your Workspace's Copy of a Routine Template, write to it
  from a Flow, and publish the change.
concepts: [manifest-keys, merge-policy, copying-a-template, versions, app-bundle]
part: build
---

This guide adds one Table to a Routine Template a Routine already runs, and
ends with the Table on the Routine and a Flow writing Rows to it. The loop
around it (copy, edit, check, publish) is the one in
[changing a Routine Template](https://docs.popcorn.ai/build/guides/template-authoring.md),
and [Table Columns](https://docs.popcorn.ai/build/concepts/table-columns.md) is the Column reference. This one is the order to do
things in, and the choices you cannot take back afterwards.

The CLI calls a Routine a *channel* and its template an *app*, so the
commands keep those names (see the [glossary](https://docs.popcorn.ai/glossary/glossary.md)).
This guide runs from the CLI throughout. An assistant over MCP can publish the same
change with `create_routine_version`, but it is not given the Flow-run tools
that "Confirm it landed" uses to check the result.

The running example adds a `handoffs` Table to the template `#example-intake`
runs: one Row per ticket handed to someone, where a repeat hand-off updates
the Row instead of adding another one.

## Check out a Copy

A Publish lands on a Copy of the template your Workspace owns (the CLI calls
it a *fork line*), so copy it before you edit:

```bash
popcorn app checkout --channel '#example-intake' --fork
cd <app>
```

If the Routine is already on a Copy, `app checkout --channel '#example-intake'`
is enough. A Table is a change to what the template is built from, so no
setting can stand in for it. Adding one gives the Routine a Copy of its own,
which no longer receives the template's improvements. Copying is permanent, and a
Publish reaches every Routine on the Copy, not only this one. See
[copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md) before copying the template of a
production Routine.

## Declare the Table

Add it under `tables:` in `manifest.yaml`. The key is the Table's name, which
is what every Flow Step passes as `table_name`.

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

A Column needs a `name` and a `type`. [Table Columns](https://docs.popcorn.ai/build/concepts/table-columns.md) lists the
rest: `format`, which belongs to one type and is checked on every write,
`display`, `label`, the governance flags, `index` and `unique`.

Choose the names now, because Install never renames a Column. The `name`
is the key every Row is stored under, so a changed `name` adds a new Column
next to the old one. A change of case alone adds nothing. The installed
spelling stays, and a Flow that writes the new spelling is refused with a
"did you mean". A Column that any `$` reference reads, such
as `$row.TicketId` in a `foreach`, needs a name made only of letters, digits
and underscores that does not start with a digit. `First Seen` is only ever written or filtered on, so its space
does no harm.

A Table declared with no Columns is skipped. Install does not create it.

## Decide what a repeat write does

This step comes before any Flow is written, because the Flows are built
around it and a later change does not rewrite what is already stored.

The Merge Key decides which Row a write lands on, and each Column's Merge
Policy decides what happens to that Column on that Row. Both are explained
in [Column Merge Policy](https://docs.popcorn.ai/build/concepts/merge-policy.md).
Keep `on_conflict: merge`: `replace` swaps the whole Row for the incoming one
and applies no Column policy at all. The example uses three policies:

- `First Seen: keep`: the first hand-off's time stays, however often the
  ticket comes back.
- `Notes: concat`: every hand-off's note is appended, newest last.
- `Reopened: increment_on_change`: counts `done` → `open` transitions of
  `Stage`, and ignores the value the write sends.

**Choose each policy before the first Publish.** A later Publish can change
a Column's policy (see "Changing the Table later" below),
but it does not rewrite the values already stored: a Row that accumulated
text under `concat` keeps it until its next write. Choosing now avoids a
Table whose older Rows were built under a different rule.

## Write to it from a Flow

Flows reach the Table through the `foundation.store.*` Activities, naming it
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

The write sends every Column on every call. The first write inserts the
Row exactly as sent, so `Reopened` starts at `0`. After that, the
accumulating policies act only on Columns a write carries (see
[Column Merge Policy](https://docs.popcorn.ai/build/concepts/merge-policy.md)).

The other Activities you will usually need are:

- `foundation.store.list_rows`: `filter` selects Rows in the database, and
  each Row in `.output.rows` carries `_record_id`.
- `foundation.store.patch_row`: changes named Cells of one Row by
  `record_id`. It is a merging write, so the policies apply: a `concat` Cell
  appends, a `keep` Cell that holds a value ignores the patch, and a counter
  ignores the value it is sent. Pass `expected_rev` (the Row's `_rev`) when
  another writer may have changed the Row since you read it.
- `foundation.store.get_record`: reads one Row by id.

Their arguments are in the
[Activity reference](https://docs.popcorn.ai/reference/activities.md).

The store checks each value against its Column's `type`, `format` and
`required`. On a merging write, including `patch_row`, it checks the whole
merged Row, not only the Cells the write sent. The store trims whitespace
from keys, but it does not check that a key names a Column: an unknown key
is stored silently, unless it differs from a declared Column only by case.

## Validate it

```bash
popcorn app validate .
```

`app validate` reads the Manifest and the Flows together. Run from a
Checkout of the Copy's Head, logged in, with a Routine (`--channel`, else the
Checkout's), and with edits since the Checkout, it also sends them to the server, which runs the checks
`app publish` runs without publishing anything. It does not check everything,
though, and a problem it misses shows up at a later stage:

| Mistake | Caught by |
|---|---|
| a Flow writing a Column the Table does not declare | `app validate`: `undeclared-column` |
| a filter on an undeclared Column | `app validate`, as a warning: `unknown-filter-column` |
| an invalid Column definition: a merge-key Column that is undeclared, not a string or not indexed, `merge: concat` on a Column that is not a string, an unknown `type` or `display` kind, a `format` that does not suit the type, an index on `boolean` or `json`, a `merge_separator` or `merge_when` without the policy that takes it, a `merge_when` naming a missing Column or its own Column, or a `from` equal to its `to`, two Column names that differ only by case, two Table names that differ only by case, a Table or Column name containing U+FDD0 or U+FDD1 | `app validate`'s server checks; `app publish` refuses it either way |
| a `table_name` misspelled in a Flow | the Run: a write fails the Step, while a `list_rows` with `missing_ok: true` reads the missing Table as empty |

Without its server checks, `app validate` cannot report the third row: it runs
the other checks and prints `server checks: skipped` with the reason. `app publish` still refuses such a Table
before any Version exists (see "Publish"). Check every `table_name` by eye, because
`app validate` only compares Columns for Tables the Manifest declares.

## Publish

```bash
popcorn app publish . --bump patch -m "add handoffs table" --yes
```

Publishing needs Workspace-admin rights. The Publish mints the next Version
of the Copy and starts an Install on this Routine. That Install creates
the `handoffs` Table before it binds the Routine to the new Version, so no
Run on the new Version can reach a Routine without the Table. The other
Routines on the Copy get the Table at their own Daily Update, apart from the
ones that take no updates (see
[Versions](https://docs.popcorn.ai/build/concepts/versions.md)).
The Publish prints how many Routines will update, but only after the Version
exists.

Publish runs every `tables:` entry through the same validation the store
applies at Install, and refuses the whole Publish if any would be rejected.
Nothing is written: no Version is minted, and a `--bump` is not saved to
`manifest.yaml`, so re-running the same command after the fix is the retry.
The CLI prints the refusal to stderr and exits 3:

```
Error: manifest tables: the agent store would refuse these at install, so the bundle cannot be published:
  tables.handoffs: column 'Stage': display: unknown display kind 'statu'; valid: [...]
  tables.handoffs: column 'Notes': merge='concat' requires a string column, got type 'number'
```

Each line names the Table and, where there is one, the Column. The findings
for every Table come back in one refusal, although the checks that compare
Columns with each other (a `merge_when` Reference, duplicate names, the
Merge Key) run only once each Column of that Table is valid on its own. With
`--json`, the same text is the `error` field, with `status: 422` and
`error_code: validation`.

Publish checks the Manifest's Columns on their own. It cannot see a
Routine's Table, and the Install validates the schema it builds by merging
the Manifest with the Columns already live there. A combination only that
Routine has can still fail the Install: retyping a Column the Routine
already indexes to `boolean` or `json`, for instance, without writing
`index: false` and `unique: false`, since those keep their installed value
unless the Manifest states one. The reverse fails too: `index: false` on a
Column the Routine's own Merge Key uses, because a Merge Key's Columns must
stay indexed. A failed Install stops before it binds. The
Routine keeps its previous Version, but not necessarily its previous Tables:
a Table listed before the failing one may already have been created or
changed. The fix is another Publish.

## Confirm it landed

```bash
popcorn app status .
popcorn table schema handoffs --channel '#example-intake'
```

Inside a Checkout, `app status` says either that the Routine runs the Copy's
Head, or that it is behind, and then why: an Install still running or
retrying, or one that failed, was skipped or is locked out. A failed Install
shows its error and error code, and a `Next:` line says what moves the Routine on — usually
`app apply`. In `--json`, from a Checkout or from outside one with
`--channel`, branch on `install.state`.

`table schema` prints each Column's name and type, and flags `unique`,
`required`, `internal`, `pii`, `restricted` and `concat`. To see everything
else, including the other policies, `format`, `display`, `label` and the
Merge Key, add `--json`.

Then write a Row, write it again, and read it back:

```bash
popcorn flow run record_handoff --channel '#example-intake' \
  --inputs '{"ticket":"T-1","owner":"a@example.com","note":"first"}' --wait
popcorn flow run record_handoff --channel '#example-intake' \
  --inputs '{"ticket":"T-1","owner":"a@example.com","note":"second"}' --wait
popcorn table rows handoffs --channel '#example-intake'
```

You should see one Row, with both notes in `Notes` and `First Seen` still
holding the first Run's time. Two Rows mean the Merge Key did not match,
which a schema check alone cannot show you.

## Changing the Table later

Each later Publish reconciles the Table toward the Manifest, and only ever
adds to it:

- **Follows the Manifest:** new Columns are added, and Column order is the
  Manifest's. On a Column already there, `type`, `format`, `display` and
  `label` are set to exactly what the Manifest says, and removed if the
  Manifest leaves them out.
- **Changes only when declared:** for `index`, `unique`, `required`, the
  governance flags and the Table's `merge_key`, a value the Manifest states
  wins, whether it turns the setting on or off, and a key it leaves out keeps
  the installed value. Deleting `unique: true` leaves the Column unique; to
  turn it off, write `unique: false`. A declared `merge_key` replaces the
  installed one; `merge_key: null` removes it; leaving `merge_key` out keeps
  it. A bare `merge_key:` with nothing after it is YAML for `null`, so it
  removes the Merge Key too.
- **Merge Policy follows a declared `merge:`.** A `merge:` that differs from
  the installed one replaces it, and the old policy's `merge_separator` or
  `merge_when` is dropped unless the Manifest restates one. An omitted
  `merge:` keeps the installed policy, unless the same Publish retypes the
  Column out of what that policy requires (`concat` off `string`,
  `increment_on_change` off `number`); then the Column becomes `replace`.
- **Never changes:** a Column is never removed or renamed. Columns are matched by name, ignoring
  case and extra whitespace, and a matched Column keeps its installed
  spelling.
- **Existing Rows are not rewritten.** A new `type`, `format`, `required`
  or Merge Policy applies to the Rows already stored the next time anything
  merges into them. After `concat` becomes `replace`, a Row keeps its
  accumulated text until its next write replaces it. A merging write or a `patch_row` checks the whole merged Row, so it
  can fail on an old value in a Column the write never touched.

A Column you stop declaring stays on the Table with its data, after the
declared ones. Removing a Column from the Manifest does not remove it from
the Table.
