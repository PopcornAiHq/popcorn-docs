---
id: template-authoring
title: Change a Routine Template
order: 1
group: Making a change
summary: >
  Changing an existing Routine Template, as a Copy of Questionnaire does:
  check its settings, read its files, dry-run the edit, copy it, publish a
  Version, confirm the Install landed, over MCP; the CLI (`app publish
  --yes` in agent mode) is one section. `create_routine_template` makes a
  Workspace's own template; `run_code_block` tests a code block
  unpublished. Popcorn's catalog is not self-serve.
lede: >
  Change what a Routine Template does: copy it, edit it, publish a new
  Version and confirm it installed.
concepts: [app-bundle, manifest-keys, flow-grammar, versions, copying-a-template]
---

A [Routine Template](https://docs.popcorn.ai/routines.md) is made of an
[App Bundle](https://docs.popcorn.ai/app-bundle.md): a directory of YAML
that turns an empty Routine into one that runs the template, with Tables to
hold state, Flows to do work, and Schedules and Webhooks to start them.
This guide changes the Questionnaire template behind `#team-offsite`, from
[Set up your first Routine](https://docs.popcorn.ai/set-up-a-routine.md),
so that its pass runs once an hour instead of every fifteen minutes.
[The Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md)
describes what it is made of.

Each step starts with a prompt you might give your assistant, followed by
the MCP tools it calls. The CLI's form of the loop, and what only the CLI
can do, is in [With the CLI](#with-the-cli) at the end.

> [!IMPORTANT] New or changed template
> *Changing* a template that already exists is a loop you run yourself,
> with no deploy in it. A *new* template your Workspace owns is the same
> loop, started from empty files: see
> [A template of your own](#a-template-of-your-own). A new template in
> Popcorn's catalog, offered to every Workspace, is not self-serve: see
> [A template in Popcorn's catalog](#a-template-in-popcorn-s-catalog-not-self-serve).

## Change #team-offsite's template

### Check the settings

> "Can I make #team-offsite check for replies once an hour instead of every
> fifteen minutes?"

> [!TIP] MCP tool call
> Your assistant calls `list_routine_settings`.

Your assistant lists the
[Routine Settings](https://docs.popcorn.ai/routine-settings.md) the
template offers. A setting reaches this Routine alone, can be set back, and
survives the template's updates, so it is always the first place to look.
Questionnaire's cover how often it follows up, whether emails are sent,
and its two prompts, but not how often its pass runs: that is the
`interval:` of the Schedule in its
[Manifest](https://docs.popcorn.ai/manifest-keys.md), which only a Copy can
change.

### Read the files

> "Show me #team-offsite's Schedule and everything that says how often it
> runs."

> [!TIP] MCP tool call
> Your assistant calls `list_routine_files`, then `read_routine_file` for
> each file it needs.

Your assistant reads the Version of the template the Routine runs, which
is also the version a Copy starts from. The Schedule is one entry in
`manifest.yaml`:

```yaml title="manifest.yaml"
schedules:
  - flow: questionnaire_tick
    slug: questionnaire-tick
    interval: 900
    class: periodic
    overlap: skip
    jitter: 60
```

The interval is also written in words: in `strings.yaml`'s
`waiting_body`, in `agent_summary` under the Manifest's `scalars:`, and in
`AGENT.md`. Those are what the Routine's
[Agent](https://docs.popcorn.ai/agent.md) and the setup checklist tell
people, so a change to the number changes them too. The `automations`
lines in `strings.yaml` take their cadence from the Schedule itself.

### Try the change

> "Draft that change for #team-offsite: the Schedule every hour, and the
> wording to match. Don't copy anything yet."

> [!TIP] MCP tool call
> Your assistant calls `create_routine_version` without `confirm`.

Your assistant sends the edits as a dry run: `interval: 3600`, the three
pieces of wording, and `version:` bumped past the one it read. The dry run
reports every check a Publish would fail and each file's diff, and changes
nothing. A Routine still on Popcorn's template can dry-run a change, so the
step that can't be undone comes after the check.

Each edit is a text op on one file, and carries the `sha256` the file was
read at; a file the assistant generated rather than typed goes up through
`create_routine_file_upload`. The
[MCP reference](https://docs.popcorn.ai/mcp.md) has the arguments.

### Copy the template

> "Give #team-offsite its own copy of the template, called team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `copy_routine_template`, shows you the dry run, then
> calls it again with `confirm=true`.

The [Copy](https://docs.popcorn.ai/copying-a-template.md) starts
byte-identical to the Version `#team-offsite` runs, and the Routine moves
onto it. Other Routines made from Questionnaire stay where they are.
Workspace admins and the Routine's
[Members](https://docs.popcorn.ai/members.md), but not its guests, can make
one.

> [!CAUTION] A Copy is for good
> The Routine never goes back to Popcorn's template and stops receiving its
> improvements, and a Copy can't be deleted.

### Publish a Version

> "Now make that change on the copy."

> [!TIP] MCP tool call
> Your assistant calls `create_routine_version` again with the same edits,
> shows you the dry run, then calls it with `confirm=true` and the
> `plan_id` that dry run gave.

The Copy starts with the same files, so the edits read against Popcorn's
Version apply to it unchanged. This dry run also shows the reach: which
Routines the new [Version](https://docs.popcorn.ai/versions.md) goes to.
Confirming creates it, and `#team-offsite` starts installing it at once.

> [!IMPORTANT] Workspace admins only
> Only a Workspace admin can publish a Version to a Copy.

> [!WARNING] A Publish reaches every Routine on the Copy
> Other Routines on the same Copy install the new Version at their next
> [Daily Update](https://docs.popcorn.ai/versions.md), not only the one you
> tested on.

### Confirm the Install landed

> "Has #team-offsite installed the new version? What starts its work now?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine`, waiting up to 20 seconds with
> `wait_seconds`, then `list_triggers`.

Your assistant reads the Routine's **Install** field, which says
`installed` once the new Version has landed, then shows its one Schedule
running once an hour. Until then the field says why not: `installing`,
`retrying` with its attempt count, `locked`, `failed` with its error,
`skipped` with its reason, or `behind`, and names the next step where one
helps. If the Install didn't land, because the Routine's
template updates were locked or another Install held it, your assistant
retries it with `install_routine`.

## A template of your own

> "Make a new template for this Workspace called intake: one Table of
> claims and a Flow that reads each new email into it."

> [!TIP] MCP tool call
> Your assistant calls `create_routine_template` without `confirm`, shows
> you the dry run, then calls it again with `confirm=true` and the
> `plan_id` that dry run gave. Then it calls `create_routine` with
> `template="ws_intake"`.

Your assistant writes every file of the [App Bundle](#what-a-bundle-is),
each as a `create` change over an empty template, and the dry run runs
the checks a Publish runs. The template's key is `ws_` and its name, so
`manifest.yaml` says `app_type: ws_intake`. Confirming creates it with
its first [Version](https://docs.popcorn.ai/versions.md), and
`create_routine` makes a Routine that installs it.

From then on the template changes as a Copy does: `create_routine_version`
on any of its Routines publishes its next Version, and every Routine on
it installs that Version.

> [!IMPORTANT] Workspace admins only
> Only a Workspace admin can create a template, and only that Workspace
> sees it. It is never in Popcorn's catalog and takes none of Popcorn's
> updates.

> [!NOTE] No upload for a first Version
> `create_routine_template` takes a file's content or a `from_url`, not an
> upload from `create_routine_file_upload`, which belongs to a Routine. Add
> a generated file in a later Version instead.

## A template in Popcorn's catalog — not self-serve

Only the first and last steps are yours. The two in the middle happen on
the Popcorn side and are not exposed through MCP, the CLI or the public
API:

```
your bundle dir                                    (author here)
      │
      ├─▶ the new app_type is registered and the workers
      │   that run its flows are deployed            (internal)
      │
      ├─▶ the bundle is published to the template registry
      │                                              (internal)
      │
      └─▶ create_routine(template=…)                 (over MCP)
```

The Bundle is published after the deploy: one whose Flows call a new
[Activity](https://docs.popcorn.ai/activities.md) must not become
installable before the workers that run it exist, or a Routine created in
that window installs cleanly and fails on its first Run. `create_routine`
resolves only templates the server already carries, and
`list_routine_templates` is how you check that one has landed.

> [!NOTE] Templates follow your Release Track
> `list_routine_templates` shows what your Workspace's Release Track
> (alpha, beta or stable; stable by default) can see. A template your
> track can't see is refused with the same neutral error as a typo, and
> the API deliberately doesn't say why. If a template you know shipped is
> missing, suspect that first and ask.

## What a Bundle is

Questionnaire's tree is in
[The Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md#read-its-files).
Only `manifest.yaml` is required, and a Publish needs its `version:`; the
full tree and the reserved names are
[App Bundles](https://docs.popcorn.ai/app-bundle.md). Two rules from it
cost the most when missed:

- **Every other root-level `.yaml` is a Flow**, and a nested one is not a
  Flow at all. Keep sample payloads and fixtures outside the Bundle
  directory: a path the format does not name never publishes.
- **A Flow's identity is its `name:`, not its filename**, so renaming
  `name:` is one Flow leaving and another arriving; see
  [a Flow's identity is its name](https://docs.popcorn.ai/flow-grammar.md#a-flow-s-identity-is-its-name).

> [!WARNING] Don't copy a Bundle from a repo
> The cut-down Bundles under the CLI repo's `tests/fixtures/bundles/` exist
> to exercise `app validate`; none declares a `version:`, so none can
> publish. Read a real Bundle from the server, as above. To study another
> shipped template, create a scratch Routine from it and read that.

## What the Manifest declares

Every key is optional, and each has its own Install semantics:
[Manifest keys](https://docs.popcorn.ai/manifest-keys.md) is the table.
Questionnaire uses every key with a page of its own except `recipe`:

| Key | In Questionnaire | Page |
|---|---|---|
| `tables` | `recipients` | [Table Columns](https://docs.popcorn.ai/table-columns.md), [Column Merge Policy](https://docs.popcorn.ai/merge-policy.md), [adding a Table](https://docs.popcorn.ai/adding-a-table.md) |
| `scalars`, `default_scalars` | `agent_summary`; `popcorn.email_send_mode: send` | [Scalar tiers and Routine Settings](https://docs.popcorn.ai/scalar-tiers.md) |
| `schedules` | `questionnaire_tick`, every 900 seconds | [Schedules in a Manifest](https://docs.popcorn.ai/schedules.md) |
| `states` | the `recipient` machine on `Stage` | [State Machines in a Bundle](https://docs.popcorn.ai/state-machine.md), [authoring a States tier](https://docs.popcorn.ai/states-authoring.md) |
| `recipe` | none | the same graph as a root `recipe.yaml` each Routine can replace: [the Recipe](https://docs.popcorn.ai/state-machine.md#the-recipe-a-graph-each-routine-can-replace) |

Three traps are worth carrying into every edit:

- **An absent key leaves the Routine alone; an empty one means "replace
  with nothing."** `schedules: []` deletes every Manifest-managed Schedule.
  Omitting `schedules:` does not.
- **An unknown top-level key is silently ignored.** A typo such as
  `schedule:` installs nothing and reports nothing.
- **Keep `app_type:`.** A Publish refuses a Manifest without it. Dropping
  `channel_agent:` hands the Routine's Members back to the default Agent;
  see [Manifest keys](https://docs.popcorn.ai/manifest-keys.md).

## Writing Flows

A Flow's grammar is four concept pages, each answering one question, and
Questionnaire's Flows are worked examples of each:

- [The shape of a Flow](https://docs.popcorn.ai/flow-grammar.md): the
  file's keys, the five kinds of Step, blocks, `call_flow` and `foreach`.
  `questionnaire_tick` fans out with `foreach` over `call_flow`.
- [References in a Flow](https://docs.popcorn.ai/references.md): the `$`
  roots, the syntax, and why nothing in a reference computes.
- [Conditions in a Flow](https://docs.popcorn.ai/conditions.md): `when:`'s
  two rails, and filtering Rows instead of gating Steps.
- [Step errors and retries](https://docs.popcorn.ai/on-error.md):
  `on_error`, the default of four attempts, and what no policy catches.
  `ask_recipient`'s send sets `retry: 0`, since a retried send could email
  twice.

The Activities a Flow can call come from the server, because a list here
would rot. The Activities reference is generated from it after each
deploy:

> "Which Activity sends an email from #team-offsite, and what do I pass
> it?"

> [!TIP] MCP tool call
> Your assistant calls `search_docs`, then `read_doc` on the Activities
> reference with the Activity's name as `section`.

`create_routine_version`'s dry run checks every Flow the change touches
against the same catalog and reports what isn't real, such as a
reference to a key the Activity doesn't return, as a `flow_invalid`
warning.

Questionnaire reads no Webhook. For a template that does, reading fields
off the payload is
[extracting fields or deriving them](https://docs.popcorn.ai/extract-or-derive.md).

## The authoring loop

Three loops, and picking the right one is most of the speed. The
**inner** loop publishes nothing and runs as often as you like:
`create_routine_version` without `confirm`, whose dry run runs every
check a Publish runs and lists the warnings, and the Activities reference.

A code block, the code under `code/<block>/` that a Flow calls with
`code.execute`, can be run in the inner loop too:

> "Run #team-offsite's questionnaire block on this reply and show me what
> it decides, with my change to the follow-up rule."

> [!TIP] MCP tool call
> Your assistant calls `run_code_block` with the block's name, the inputs,
> and its edits as `changes`.

The block runs on the runner and in the sandbox a Flow's step uses, so its
output is what the step's would be; `tests=true` runs its `tests/` instead.
Nothing is published or written: the block can't read or write the
Routine's Tables and gets no secrets, so pass as inputs what the step's
`reads` would. Once the output is right, the same `changes` go to
`create_routine_version`. Only Workspace admins can run one, one at a
time per Routine.

The **middle** loop is the Copy above: a Publish and an Install, seconds
per turn, no deploy. While it runs:

> "Run #team-offsite's pass now, show me how it went, and list the
> recipients it touched."

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, then `run_trigger`, as a dry run
> and again with `confirm=true`, then `get_run` with `wait_seconds`, and
> `list_rows` on `recipients`.

`run_trigger` runs a Schedule the template declares, doing for real what
the Schedule does, and leaves the Schedule as it was. `get_run` shows a
failed Run's error, and a running one's current Step; `list_runs` finds
the Runs a Schedule or a Webhook started. A `#name` that matches more
than one Routine is answered with each candidate's ID; pass the ID
instead.

A Run also fails when a `$channel.*` reference its Flows make has nothing
behind it. `create_routine_version`'s dry run compares every one against
the Routine and warns on the three findings that fail a Run:
`missing_parameter`, a referenced parameter (a Routine Setting) that is
not set; `missing_integration`, a declared Integration that is not
connected; and `provider_mismatch`, a Connection whose provider
contradicts the declaration. `list_routine_settings` and
`list_connections` show what the Routine has now.

The **outer** loop is only for a new template in Popcorn's catalog, and
costs a deploy (see
[A template in Popcorn's catalog](#a-template-in-popcorn-s-catalog-not-self-serve)), so a
Bundle that installs but is wrong costs a whole deploy cycle to correct.
For a template fed by a [Webhook](https://docs.popcorn.ai/triggers.md),
such as `alerttracker`, it continues with `create_routine`,
`list_triggers` for the Routine's Webhooks, a test Delivery, and
`get_run` on the Run it starts. Sending the test Delivery needs the CLI.

### Checks will not save you

The evidence here is from building `alerttracker`, which Questionnaire has
no counterpart for: every defect found while building it passed
`flow validate`, because they were runtime semantics rather than bad
references. A Merge Policy overwrote a first-seen timestamp, an LLM
invented a Row, an optional schema property went missing, and a Flow wrote
an undeclared Column.
[`examples/alerttracker/GOTCHAS.md`](https://github.com/PopcornAiHq/popcorn-cli/blob/main/examples/alerttracker/GOTCHAS.md)
is the raw log; read it as a record, since some findings predate
[Merge Policies](https://docs.popcorn.ai/merge-policy.md).

The CLI's offline checks now catch the last two (see
[With the CLI](#with-the-cli)); nothing catches the first two: a Merge
Policy is only wrong relative to what you meant. So install the change
and run it, and test the **boundary**, not the happy path. In
Questionnaire that means a recipient at an address you own,
`popcorn.email_send_mode` at `draft`, and a check just short of
`follow_up_days` that must not follow up. `alerttracker` has a seed Flow,
`seed_test_alert`, that sends a canned payload through its ingest Flow;
Questionnaire has none.

Watch for these when reading results:

- Many Activities have permissive result schemas
  (`additionalProperties: true`). For those, `$steps.x.output.anything`
  passes validation, and at runtime a key the response lacks is a hard
  `ReferenceError: … key not found`; only a null partway along the path
  resolves to null. Verify against the real response.
- `start_flow` is asynchronous. A parent that launches a child reports
  Completed at once; check the child's Run, or use a `call_flow:` Step
  with `mode: wait`, as `questionnaire_tick` does.
- Posting the same Webhook body twice does not test merge logic: a
  Delivery byte-identical to one seen in the last five minutes is dropped
  before any Flow runs. Vary the body while keeping the identity fields.
- A field that might be absent must never be dereferenced: a missing key
  fails the Run before the Activity is called, so `on_error` can't rescue
  it. Guarantee it upstream, in an `output_schema`'s `required` or with
  `$exists: true` in the query that produced the Rows.

## Before you publish

Each line is a rule a concept page explains; every one has cost a Publish.

1. `version:` advances every Publish, bumped in the same change.
2. The Manifest keeps `app_type:` and `channel_agent:`.
3. No Flow-written value is declared under `scalars:` —
   [Scalar tiers and Routine Settings](https://docs.popcorn.ai/scalar-tiers.md).
4. Every Schedule's `flow:` names a Flow the Bundle has —
   [Schedules](https://docs.popcorn.ai/schedules.md).
5. Table changes only add: no Column is dropped or renamed, and a Column a
   Flow dereferences has no spaces —
   [Table Columns](https://docs.popcorn.ai/table-columns.md).
6. A Step with a side effect sets `retry: 0` —
   [Step errors](https://docs.popcorn.ai/on-error.md).
7. Every key a reference reads is guaranteed upstream —
   [references](https://docs.popcorn.ai/references.md).
8. A second condition in a `when:` did not change how the first compares —
   [conditions](https://docs.popcorn.ai/conditions.md).
9. Fields the payload states are extracted, not derived —
   [extract or derive](https://docs.popcorn.ai/extract-or-derive.md).
10. A markdown post sets `format: markdown`, on every edit too —
    [the shape of a Flow](https://docs.popcorn.ai/flow-grammar.md).
11. Wording that restates a number you changed, in `strings.yaml`,
    `AGENT.md` or `agent_summary`, changed with it.

## With the CLI

A Checkout on disk, `app validate`'s offline rules, `--bump`, agent
mode's `--yes`, `app lines`, `channel-config show` without an edit,
running a Flow by name with your own inputs, and sending a Webhook
Delivery have no MCP equivalent today; the rest is the CLI's form of the
steps above.

The CLI and the API call a Routine a *channel* and its
template an *app*, so the commands keep those names.

### The loop

```bash
popcorn app checkout --channel '#team-offsite' --fork   # copy, then check out its Head
# ... edit ./questionnaire
popcorn app validate ./questionnaire
popcorn app publish ./questionnaire --bump patch -m "Run the pass hourly" --yes
popcorn app status ./questionnaire                      # has the Install landed?
```

`--fork` takes an optional name for the Copy (`--fork=offsite`);
bare, it names the Copy it is about to use and asks, because a Workspace's
single existing Copy can be far behind Popcorn's template. `popcorn app
fork` makes the Copy without the Checkout. `app publish` refuses a
Checkout of Popcorn's own version, which the CLI prints as *PRODUCT*.

> [!WARNING] `--yes` in agent mode
> `app publish` asks before it sends anything, because a Publish reaches
> every Routine on the Copy. In agent mode (`POPCORN_AGENT=1`) or any
> non-interactive shell there is no one to answer, so it is refused unless
> it carries `--yes` (or `POPCORN_ASSUME_YES=1`).

**`--bump patch|minor|major`** writes `version:` in `manifest.yaml` off the
Copy's Head, and only once the Publish has been accepted, so a Publish that
fails leaves the working copy untouched and running it again is the retry.
Editing `version:` by hand also works; `--bump` is refused when the
Manifest already advances past the Head. A published Version can't change,
so `version:` must advance past the one the Checkout came from:
`app validate` reports `version-not-advanced` offline rather than the
server refusing it after the upload.

**`-m`** records what changed on the Version, like `git commit -m`
(`--changelog` is the deprecated spelling), as `create_routine_version`'s
`changelog` does. The Manifest's own `changelog:` key is not read by a
Publish to a Copy, so a Manifest that declares one while you pass no `-m`
records nothing, and Publish says so. `app validate` warns
`changelog-not-updated` when `changelog:` is left as the Checkout wrote
it, since it arrives carrying the previous Version's note.

> [!NOTE] The printed line is the record
> No command reads a published Version's message back, so the line
> `app publish` prints is the one chance to see it.

### Validating

**`app validate`** runs two kinds of check. Its own, offline, ask whether
the files agree with each other and whether an Install will do what you
think: a fixture named `.yaml`, a write to an undeclared Column, a Schedule
naming a Flow that is not there, a path the Bundle format does not name
(`path-not-published`, left behind at Publish), and a Manifest that has
lost `app_type:` (`clears-app-type`, an error in a Checkout).
`--strict` makes warnings fail too, the CI form. In a Checkout of a Copy's
Head, logged in and with edits since the Checkout, it also sends the edits
to the server, which runs the checks `create_routine_version`'s dry run
runs, the Manifest's `tables:` and `states:` among them; otherwise it
prints `server checks: skipped` with the reason. Its offline rules ship
with the CLI, so an older CLI can reject what the platform accepts:
upgrade the CLI before changing the Bundle.

The Activities and one Flow's references can be checked from the shell
too:

```bash
popcorn flow activities --summary              # what can I call?
popcorn flow activities --name <wire.name>     # what do I pass it?
popcorn flow validate questionnaire_tick.yaml  # is every reference real?
```

`flow validate` asks the server about one Flow and is the authority on
it. It needs a Routine only to know who you are and never writes; from a
Checkout it takes the Checkout's Routine, and anywhere else it takes
`--channel`.

### Install status

**`app status`** says whether the Install has landed, as `get_routine`'s
**Install** field does. Outside a Checkout, `--channel` answers the same
from the server:

```bash
popcorn app status --channel '#team-offsite' --json | jq -r '.data.install.state'
```

`install.state` is `current` (the Routine runs its Copy's Head) or says
why not: `installing`, `retrying`, `locked`, `failed`, `skipped` or
`behind`. A failed Install comes with its error, an `error_code` and its
attempt count: only `invalid_manifest`, `invalid_schedule` and
`bundle_rejected` mean the Head needs fixing, and `internal` means the
platform failed, so no edit helps. The text output ends with a `Next:`
line; for a failed, skipped or behind Routine it is `popcorn app apply`,
the CLI's `install_routine` and the retry for an Install that did not
land. `apply` is not a step in the loop: `app publish` already starts the
Install.

### The Checkout's own files

A Checkout writes two files that are not Bundle content and never publish:
`.popcorn-app.json`, the baseline the checks read, and `CLAUDE.md`, which
tells a coding agent that an edit is not a release until `app validate` and
`app publish` have run. `CLAUDE.md` is yours once written, and is not
`AGENT.md`, which ships to every Routine on the Copy.

> [!TIP] Reading an earlier Version
> `app checkout --version <id>` writes an earlier Version of the Copy,
> read-only, as `read_routine_file`'s `version` reads one file of it: the
> way to recover the tree from before a bad Publish. See
> [Versions](https://docs.popcorn.ai/versions.md).

> [!NOTE] Copies accumulate
> `popcorn app lines` lists the Workspace's Copies, each with its Head and
> when it was published; `popcorn app list --channel '#team-offsite'`
> shows what the Routine runs, as `get_routine` does. `list_routines` with
> `template` and `copy` lists the Routines on one, and no Copy can be
> deleted. A bare `app fork`
> adopts the single Copy that exists and is refused once there are two:
> name one with `--name`.

### While the Copy runs

```bash
popcorn channel-config show --channel '#team-offsite' --strict  # is the Routine wired up?
popcorn flow run questionnaire_tick --channel '#team-offsite' --wait
popcorn flow runs list --channel '#team-offsite' --flow check_recipient
popcorn table rows recipients --channel '#team-offsite'
```

`channel-config show` compares every `$channel.*` reference the Flows make
against what the Routine has, its parameters (Routine Settings) and its
Integrations (Connections), without an edit to dry-run. `--strict` exits
non-zero on the three findings that fail a Run, the ones the dry run warns
on. The `unused_*` findings are informational.

`flow run` takes a Flow's name or UUID, not only a Schedule's, and fills
`conversation_id` from `--channel`; pass `--inputs` for the Flow's own
arguments. Every Run carries `outcome` (`succeeded`, `failed` or
`still_running`): poll that, not `status`, as `--wait` does. `flow runs`
and `table rows` are the CLI's `list_runs` and `list_rows`.

### A Webhook template

```bash
popcorn channel create '#chan' --template alerttracker
popcorn webhook list <id> --show-url                 # names, ids and the ingest URL
popcorn webhook send Intake @fixtures/sample.json --channel <id>
popcorn flow runs get <workflow-id> --channel <id> --include-errors
```

`webhook send` posts a test Delivery, which nothing over MCP does, and
`webhook list --show-url` shows an ingest URL again, which `list_triggers`
never does.

### Templates in the catalog

`popcorn channel create '#chan' --template <name>` is `create_routine`'s
form, and resolves only names the server already carries. `popcorn
channel templates` and `popcorn app list` show what your Workspace's
Release Track can see, as `list_routine_templates` does.
