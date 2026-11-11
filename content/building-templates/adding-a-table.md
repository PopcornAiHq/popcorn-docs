---
id: adding-a-table
title: Add a Table or a Column
order: 12
group: Tables and Status
summary: >
  Adding a Column or a Table to a Routine Template: copy it
  (copy_routine_template), declare it under `tables:`, write it from a Flow
  with `foundation.store.*`, dry-run and publish with
  create_routine_version, and read it back with get_table. Install adds,
  never removes or renames. Publish refuses a Column the store would reject;
  only the CLI's `app validate` catches an undeclared Column.
lede: >
  Add a Column or a Table to your Workspace's Copy of a template, write to
  it from a Flow, and publish the change.
concepts: [table-columns, merge-policy, copying-a-template, versions, app-bundle]
---

This guide adds a Column to the `recipients` Table of the Questionnaire
template that `#team-offsite` runs, and ends with the Column on the Routine
and its Flows writing to it. The Column is `Emails Sent`: one line per email
sent to a recipient, first email and follow-ups alike. Adding a whole
[Table](https://docs.popcorn.ai/tables.md) takes the same steps, and
[A new Table](#a-new-table) says what differs.

The loop around it (copy, edit, check, publish) is the one in
[changing a Routine Template](https://docs.popcorn.ai/template-authoring.md),
and [Table Columns](https://docs.popcorn.ai/table-columns.md) is the Column
reference. This page is the order to do things in, and the choices you
cannot take back afterwards. Each step starts with a prompt you might give
your assistant; [With the CLI](#with-the-cli) at the end has each step's
CLI form, and the checks only the CLI makes.

## Copy the template

> "Make #team-offsite its own copy of the Questionnaire template."

> [!TIP] MCP tool call
> Your assistant calls `copy_routine_template`, then again with
> `confirm=true` once you agree.

A new Column is a change to what the template is built from, so no
[Routine Setting](https://docs.popcorn.ai/routine-settings.md) can stand in
for it, and a new [Version](https://docs.popcorn.ai/versions.md) lands only
on a [Copy](https://docs.popcorn.ai/copying-a-template.md) your Workspace
owns. The Copy starts identical to the Version the Routine runs, and the
Routine moves onto it. If the Routine is already on a Copy, skip this step.

> [!CAUTION] A Copy is permanent
> The Routine never goes back to Popcorn's template and stops receiving its
> improvements, and a Publish reaches every Routine on the Copy, not only
> this one. Try a change on a scratch Routine before copying the template
> of one in use.

## Declare the Column

> "On #team-offsite's copy, add an Emails Sent column to recipients that
> keeps a line for every email we send."

> [!TIP] MCP tool call
> Your assistant calls `read_routine_file` for `manifest.yaml`, then
> `create_routine_version` without `confirm`, which is a dry run.

Columns are declared under `tables:` in `manifest.yaml`. Add `Emails Sent`
to `recipients`, among its other Columns:

```yaml title="manifest.yaml"
tables:
  recipients:
    columns:
      # …the template's Columns, Email through Last Message…
      # One line per email sent, newest last.
      - name: Emails Sent
        type: string
        merge: concat
        label: Emails sent
```

A Column needs a `name` and a `type`.
[Table Columns](https://docs.popcorn.ai/table-columns.md) lists the rest:
`format`, which belongs to one type and is checked on every write,
`display`, `label`, the governance flags, `index` and `unique`.

Choose the name now: an [Install](https://docs.popcorn.ai/versions.md)
never renames a Column, and a Flow that dereferences one needs it
space-free
([Table Columns](https://docs.popcorn.ai/table-columns.md#names-are-permanent-and-a-flow-may-need-them-space-free)).

## Decide what a repeat write does

This step comes before any Flow is written, because the Flows are built
around it and a later change does not rewrite what is already stored.

The Merge Key decides which Row a write lands on (in `recipients`, the one
with that `Email`), and each Column's Merge Policy decides what happens to
that Column on that Row; both are in
[Column Merge Policy](https://docs.popcorn.ai/merge-policy.md).
`Emails Sent` is `concat`, so each write appends a line and nothing is
overwritten. `concat` needs a `string` Column, which is why a list of times
is not a `datetime`.

> [!IMPORTANT] Choose each policy before the first Publish
> A later Publish can change a Column's policy (see
> [Changing it later](#changing-it-later)), but it does not rewrite the
> values already stored: a Row that accumulated text under `concat` keeps
> it until its next write.

## Write to it from a Flow

[Flows](https://docs.popcorn.ai/flow-grammar.md) reach a Table through the
`foundation.store.*` [Activities](https://docs.popcorn.ai/activities.md),
naming it by `table_name`. Questionnaire's Flows already write a
recipient's Row after every email, so `Emails Sent` goes in those patches.
In `ask_recipient`, the step that records the first email:

```yaml title="ask_recipient.yaml"
  - id: record
    when: $steps.thread.output.value
    activity: foundation.store.patch_row
    args:
      conversation_id: $inputs.conversation_id
      table_name: recipients
      record_id: $inputs.record_id
      patch:
        Stage: waiting
        Thread: $steps.thread.output.value
        Asked: $steps.now.output.iso
        Last Asked: $steps.now.output.iso
        Follow Ups: 0
        Message Id: $steps.send.output.rfc822_message_id
        Asked Address: $steps.compose.output.to
        Emails Sent: $steps.now.output.iso
      change_kind: questionnaire_asked
      change_action: $steps.compose.output.asked
```

Add the same line to `record_follow_up` in `check_recipient.yaml`, which
records each follow-up. A patch is a merging write, so the policies apply:
`Emails Sent` appends, `Asked` (`keep`) ignores a second ask once it holds
the first one's time, and a counter ignores the value it is sent.

The other Activities you will usually need are:

- `foundation.store.list_rows`: `filter` selects Rows in the database, and
  each Row in `.output.rows` carries `_record_id`.
- `foundation.store.upsert_rows`: writes Rows matched by the Merge Key,
  inserting the ones it doesn't find.
- `foundation.store.get_record`: reads one Row by id.

`patch_row` takes `expected_rev` (the Row's `_rev`) when another writer may
have changed the Row since you read it. Questionnaire takes a lease on the
Row's `Sending` Column instead, with `foundation.store.claim_row`, so two
passes can't both email the same recipient; see
[Row leases](https://docs.popcorn.ai/row-leases.md).

A merging write checks the whole merged Row, not only the Cells it sent.
`Last Asked` is a `datetime`, so it is emptied with `null`, not `""`
([Table Columns](https://docs.popcorn.ai/table-columns.md#type-format-display)).

An unknown key is stored silently; see
[The store accepts undeclared Columns](https://docs.popcorn.ai/table-columns.md#the-store-accepts-undeclared-columns).

## Validate it

> "Check the change before you publish it."

> [!TIP] MCP tool call
> Your assistant calls `create_routine_version` without `confirm`. Its dry
> run shows each file's diff and every check the Version would fail.

The dry run runs the checks a Publish runs, without publishing anything.
It does not check everything, and a problem it misses shows up at a later
stage:

| Mistake | Caught by |
|---|---|
| an invalid Column definition: a merge-key Column that is undeclared, not a string or not indexed, `merge: concat` on a Column that is not a string, an unknown `type` or `display` kind, a `format` that does not suit the type, an index on `boolean` or `json`, a `merge_separator` or `merge_when` without the policy that takes it, a `merge_when` naming a missing Column or its own Column, or a `from` equal to its `to`, two Column names that differ only by case, two Table names that differ only by case, a Table or Column name containing U+FDD0 or U+FDD1 | the dry run; the Publish refuses it either way |
| a Flow writing a Column the Table does not declare | nothing before the Run, which stores it silently; the CLI's `app validate` reports it (see [With the CLI](#with-the-cli)) |
| a `table_name` misspelled in a Flow | the Run: a write fails the Step, while a `list_rows` with `missing_ok: true` reads the missing Table as empty |

> [!TIP] Check Column names and `table_name` by eye
> Nothing on the server compares a Flow's writes with the Table's Columns,
> so a misspelled Column or `table_name` passes the dry run.

## Publish

> "Publish it."

> [!TIP] MCP tool call
> Your assistant calls `create_routine_version` with `confirm=true` and
> the `plan_id` from its dry run.

Publishing needs Workspace-admin rights, and every new Version bumps
`version:` in `manifest.yaml`. The Publish mints the next
Version of the Copy and starts an Install on this Routine, which adds the
Column before it binds the Routine to the new Version, so no
[Run](https://docs.popcorn.ai/history.md) on the new Version can reach a
Routine without it. The other Routines on the Copy get it at their own
Daily Update, apart from the ones that take no updates.

> [!WARNING] A Publish reaches every Routine on the Copy
> The assistant's dry run says how many Routines will update before the
> Version exists.

Publish runs every `tables:` entry through the same validation the store
applies at Install, and refuses the whole Publish if any would be
rejected. Nothing is written and no Version is minted, so the retry is the
same Publish after the fix. Each finding names the Table and, where there
is one, the Column:

```
tables.recipients: column 'Emails Sent': merge='concat' requires a string column, got type 'datetime'
```

The findings for every Table come back in one refusal, although the checks
that compare Columns with each other (a `merge_when` Reference, duplicate
names, the Merge Key) run only once each Column of that Table is valid on
its own.

Publish checks the Manifest's Columns on their own. It cannot see a
Routine's Table, and the Install validates the schema it builds by merging
the Manifest with the Columns already live there. A combination only that
Routine has can still fail the Install: retyping a Column the Routine
already indexes to `boolean` or `json`, for instance, without writing
`index: false` and `unique: false`, since those keep their installed value
unless the Manifest states one. The reverse fails too: `index: false` on a
Column the Routine's own Merge Key uses, such as `Email`.

> [!NOTE] A failed Install
> A failed Install stops before it binds. The Routine keeps its previous
> Version, but not necessarily its previous Tables: a Table listed before
> the failing one may already have been created or changed. The fix is
> another Publish.

## Confirm it landed

> "Has #team-offsite got the Emails Sent column?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine` for the Version it runs, then
> `get_table` for `recipients`.

`get_routine` says whether the latest Install landed, and when it has not,
why: an Install still running or retrying, or one that failed, was skipped
or is locked out, with its error and what moves the Routine on. It can wait
for an Install that is running. `get_table` lists each Column in order with
its type, `label` and Merge Policy, flags `required` and `unique` Columns,
and names the Merge Key, so `Emails Sent` shows as `merge: concat`.

The Rows show the Column working once Questionnaire's next pass emails
someone:

> "Show me who #team-offsite has emailed, and when."

> [!TIP] MCP tool call
> Your assistant calls `list_rows` on `recipients`.

A recipient asked and then followed up has two lines in `Emails Sent`, and
one Row: a second Row for the same address would mean the Merge Key did not
match, which a schema check alone cannot show you.

## A new Table

A new Table is a new key under `tables:`, beside `recipients`. The key is
the Table's name, which every Flow Step passes as `table_name`. Declare its
Columns and a `merge_key` as above, and write it from a Flow.

- **A Table declared with no Columns is skipped.** Install does not create
  it.
- **Install creates the Table** before it binds the Routine to the new
  Version, as it adds a Column.
- **A Merge Key needs an indexed string Column**, as `recipients` keys on
  `Email` with `index: true`. Without one, `upsert_rows` matches an
  existing Row only by the `merge_on` Columns a call names.

## Changing it later

Each later Publish reconciles the Table toward the Manifest, and only ever
adds to it:

- **Follows the Manifest:** new Columns are added, and Column order is the
  Manifest's. On a Column already there, `type`, `format`, `display` and
  `label` are set to exactly what the Manifest says, and removed if the
  Manifest leaves them out.
- **Changes only when declared:** for `index`, `unique`, `required`, the
  governance flags and the Table's `merge_key`, a value the Manifest
  states wins, whether it turns the setting on or off, and a key it leaves
  out keeps the installed value. Deleting `unique: true` leaves the Column
  unique; to turn it off, write `unique: false`. A declared `merge_key`
  replaces the installed one; `merge_key: null` removes it; leaving
  `merge_key` out keeps it. A bare `merge_key:` with nothing after it is
  YAML for `null`, so it removes the Merge Key too.
- **Merge Policy follows a declared `merge:`**: see
  [Changing a Column's policy](https://docs.popcorn.ai/merge-policy.md#changing-a-column-s-policy).
- **Never changes:** a Column is never removed or renamed. Columns are
  matched by name, ignoring case and extra whitespace, and a matched
  Column keeps its installed spelling.
- **Existing Rows are not rewritten.** A new `type`, `format`, `required`
  or Merge Policy applies to the Rows already stored the next time anything
  merges into them. A merging write or a `patch_row` checks the whole
  merged Row, so it can fail on an old value in a Column the write never
  touched.

> [!NOTE] Removing a Column keeps it
> A Column you stop declaring stays on the Table with its data, after the
> declared ones. Removing `Emails Sent` from the Manifest does not remove
> it from `recipients`.

## With the CLI

Two things on this page have no MCP equivalent today: `app validate`'s
check of a Flow's writes against the Table's Columns, and reading a
Column's `format`, `display` and index from the Routine. The rest is the
CLI form of the steps above. The CLI calls a Routine a *channel*, its
template an *app*, and a Copy a *fork line*, so its commands keep those
names.

**Copy and check out.** `--fork` makes the Copy; on a Routine already on a
Copy, leave it out.

```bash
popcorn app checkout --channel '#team-offsite' --fork
cd <app>
```

**Validate.** From the Checkout:

```bash
popcorn app validate .
```

`app validate` reads the Manifest and the Flows together, offline:

- **`undeclared-column`**: a Flow writing a Column the Table does not
  declare.
- **`unknown-filter-column`**, as a warning: a filter on an undeclared
  Column.

It compares Columns only for Tables the Manifest declares, so a misspelled
`table_name` passes it. Run from a Checkout of the Copy's Head, logged in,
with a Routine (`--channel`, else the Checkout's), and with edits since the
Checkout, it also sends them to the server, which runs the checks the dry
run runs. Without those server checks it cannot report an invalid Column
definition: it runs the rest and prints `server checks: skipped` with the
reason, and `app publish` still refuses such a Table before any Version
exists.

**Publish.**

```bash
popcorn app publish . --bump patch -m "Emails Sent: a line per email" --yes
```

The CLI prints how many Routines will update, but only after the Version
exists. A refused Publish saves no `--bump` to `manifest.yaml`, so
re-running the same command after the fix is the retry. The refusal goes
to stderr and the CLI exits 3:

```
Error: manifest tables: the agent store would refuse these at install, so the bundle cannot be published:
  tables.recipients: column 'Emails Sent': merge='concat' requires a string column, got type 'datetime'
```

With `--json`, the same text is the `error` field, with `status: 422` and
`error_code: validation`.

**Confirm it landed.**

```bash
popcorn app status .
popcorn table schema recipients --channel '#team-offsite'
```

Inside a Checkout, `app status` says either that the Routine runs the
Copy's Head, or that it is behind, and why. A failed Install shows its
error and error code, and a `Next:` line says what moves the Routine on,
usually `app apply`. In `--json`, from a Checkout or from outside one with
`--channel`, branch on `install.state`.

`table schema` prints each Column's name and type, and flags `unique`,
`required`, `internal`, `pii`, `restricted` and `concat`. Add `--json` for
everything else, including the other policies, `format`, `display`,
`label` and the Merge Key.
