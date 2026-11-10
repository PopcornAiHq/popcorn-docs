---
id: template-authoring
title: Change a Routine Template
order: 1
group: Making a change
summary: >
  Changing an existing Routine Template, as a Copy of Questionnaire does:
  check its settings, read its files, dry-run the edit, copy it, publish a
  Version, confirm the Install landed — over MCP with
  `copy_routine_template` and `create_routine_version`, or with the CLI's
  `app checkout`, `validate`, `publish` (`--yes` in agent mode) and
  `status`. Adding a template to the catalog is not self-serve.
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

Each step starts with a prompt you might give your assistant; the same loop
from the CLI follows. The CLI and the API call a Routine a *channel* and its
template an *app*, so the commands keep those names.

> [!IMPORTANT] New or changed template
> *Changing* a template that already exists is a loop you run yourself,
> with no deploy in it. A *new* template (a new `app_type`) is not
> self-serve: the set of installable templates is fixed on the server, and
> adding to it takes an internal change and a deploy. See
> [A new Routine Template](#a-new-routine-template-not-self-serve).

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

The interval is also written in words: in `strings.yaml`'s `automations`
and `waiting_body`, in `agent_summary` under the Manifest's `scalars:`, and
in `AGENT.md`. Those are what the Routine's
[Agent](https://docs.popcorn.ai/agent.md) and the setup checklist tell
people, so a change to the number changes them too.

### Try the change

> "Draft that change for #team-offsite: the Schedule every hour, and the
> wording to match. Don't copy anything yet."

> [!TIP] MCP tool call
> Your assistant calls `create_routine_version` without `confirm`.

Your assistant sends the edits as a dry run: `interval: 3600`, the four
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
[Members](https://docs.popcorn.ai/members.md) can make one.

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
running once an hour. If the Install didn't land, because the Routine's
template updates were locked or another Install held it, your assistant
retries it with `install_routine`.

## The same loop from the CLI

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
(`--changelog` is the deprecated spelling). The Manifest's own
`changelog:` key is not read by a Publish to a Copy, so a Manifest that
declares one while you pass no `-m` records nothing, and Publish says so.
`app validate` warns `changelog-not-updated` when `changelog:` is left as
the Checkout wrote it, since it arrives carrying the previous Version's
note.

> [!NOTE] The printed line is the record
> No command reads a published Version's message back, so the line
> `app publish` prints is the one chance to see it.

**`app validate`** runs two kinds of check. Its own, offline, ask whether
the files agree with each other and whether an Install will do what you
think: a fixture named `.yaml`, a write to an undeclared Column, a Schedule
naming a Flow that is not there. In a Checkout of a Copy's Head, logged in
and with edits since the Checkout, it also sends the edits to the server,
which runs the checks `app publish` runs without publishing, the Manifest's
`tables:` and `states:` among them; otherwise it prints
`server checks: skipped` with the reason. Its offline rules ship with the
CLI, so an older CLI can reject what the platform accepts: upgrade the CLI
before changing the Bundle. `popcorn flow validate` asks the server about
one Flow and is the authority on it.

**`app status`** says whether the Install has landed. Outside a Checkout,
`--channel` answers the same from the server:

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
the retry for an Install that did not land. `apply` is not a step in the
loop: `app publish` already starts the Install.

A Checkout writes two files that are not Bundle content and never publish:
`.popcorn-app.json`, the baseline the checks read, and `CLAUDE.md`, which
tells a coding agent that an edit is not a release until `app validate` and
`app publish` have run. `CLAUDE.md` is yours once written, and is not
`AGENT.md`, which ships to every Routine on the Copy.

> [!TIP] Reading an earlier Version
> `app checkout --version <id>` writes an earlier Version of the Copy,
> read-only: the way to recover the tree from before a bad Publish. See
> [Versions](https://docs.popcorn.ai/versions.md).

> [!NOTE] Copies accumulate
> `popcorn app lines` lists the Workspace's Copies, each with its Head and
> when it was published; `popcorn app list --channel '#team-offsite'`
> shows what the Routine runs. Nothing shows how many Routines ride each
> Copy, and none can be deleted. A bare `app fork` adopts the single Copy
> that exists and is refused once there are two: name one with
> `--name`.

## A new Routine Template — not self-serve

Only the first and last steps are yours. The two in the middle happen on
the Popcorn side and are not exposed through the CLI or the public API:

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
          popcorn channel create '#chan' --template <name>   (CLI)
```

The Bundle is published after the deploy: one whose Flows call a new
[Activity](https://docs.popcorn.ai/activities.md) must not become
installable before the workers that run it exist, or a Routine created in
that window installs cleanly and fails on its first Run. `channel create
--template` resolves only names the server already carries, and
`popcorn channel templates` is how you check that one has landed.

> [!NOTE] Templates follow your Release Track
> `popcorn app list` and `popcorn channel templates` show what your
> Workspace's Release Track
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
  directory: anything the format does not name is left behind at Publish
  and reported by `app validate` as `path-not-published`.
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
- **An untyped Bundle clears the Routine's `app_type`** and
  `channel_agent`. A Publish to a Copy does not refuse one: it clears both
  on every Routine on the Copy. `app validate` warns `clears-app-type`;
  treat that warning as an error.

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
would rot:

```bash
popcorn flow activities --summary              # what can I call?
popcorn flow activities --name <wire.name>     # what do I pass it?
popcorn flow validate questionnaire_tick.yaml  # is every reference real?
```

Questionnaire reads no Webhook. For a template that does, reading fields
off the payload is
[extracting fields or deriving them](https://docs.popcorn.ai/extract-or-derive.md).

## The authoring loop

Three loops, and picking the right one is most of the speed. The
**inner** loop publishes nothing and runs as often as you like:
`app validate`, `flow activities` and `flow validate`. `flow validate`
needs a Routine only to know who you are and never writes; from a Checkout
it takes the Checkout's Routine, and anywhere else it takes `--channel`.

The **middle** loop is the Copy above: a Publish and an Install, seconds
per turn, no deploy. These help while it runs:

```bash
popcorn channel-config show --channel '#team-offsite' --strict  # is the Routine wired up?
popcorn flow run questionnaire_tick --channel '#team-offsite' --wait
popcorn flow runs list --channel '#team-offsite' --flow check_recipient
popcorn table rows recipients --channel '#team-offsite'
```

`channel-config show` compares every `$channel.*` reference the Flows make
against what the Routine has, its parameters (Routine Settings) and its
Integrations (Connections). `--strict` exits non-zero on the three findings
that fail a Run: a referenced parameter that is not set, a declared
Integration that is not connected, and a Connection whose provider
contradicts the declaration. The `unused_*` findings are informational.

`flow run` takes a Flow's name or UUID and fills `conversation_id` from
`--channel`; pass `--inputs` for the Flow's own arguments. Every Run
carries `outcome` (`succeeded`, `failed` or `still_running`): poll that,
not `status`, as `--wait` does. A `#name` that matches more than one
Routine is refused with each candidate's id; pass the id instead.

The **outer** loop is only for a new template, and costs a deploy (see
[A new Routine Template](#a-new-routine-template-not-self-serve)), so a
Bundle that installs but is wrong costs a whole deploy cycle to correct.
For a template fed by a [Webhook](https://docs.popcorn.ai/triggers.md),
such as `alerttracker`, it continues:

```bash
popcorn channel create '#chan' --template alerttracker
popcorn webhook list <id> --show-url                 # names, ids and the ingest URL
popcorn webhook send Intake @fixtures/sample.json --channel <id>
popcorn flow runs get <workflow-id> --channel <id> --include-errors
```

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

`app validate` now catches the last two, and the cross-file mistakes a
per-file validator can't see (`--strict` makes warnings fail too, the CI
form). It can't catch the first two: a Merge Policy is only wrong relative
to what you meant. So install the change and run it, and test the
**boundary**, not the happy path. In Questionnaire that means a recipient
at an address you own, `popcorn.email_send_mode` at `draft`, and a check
just short of `follow_up_days` that must not follow up. `alerttracker`
has a seed Flow, `seed_test_alert`, that sends a canned payload through
its ingest Flow; Questionnaire has none.

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

1. `version:` advances every Publish, and `--bump` is the way to do it.
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
