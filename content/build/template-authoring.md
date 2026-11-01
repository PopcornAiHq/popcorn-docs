---
id: template-authoring
title: Change a Routine Template
order: 1
group: Getting started
summary: >
  The loop for changing what a Routine Template does: check its settings,
  read its files, copy it, edit, publish a Version, confirm the Install
  landed — over MCP with `copy_routine_template` and
  `create_routine_version`, or with the CLI's `app checkout`, `validate`,
  `publish` (an agent runs it with `--yes`) and `status`. A new template is
  not self-serve. `flow validate` is the authority on a Flow.
lede: >
  Change what a Routine Template does: copy it, edit it, publish a new Version
  and confirm it installed.
concepts: [app-bundle, manifest-keys, flow-grammar, versions, copying-a-template]
---

A **Routine Template** is made of an **App Bundle**: a directory of YAML
that turns an empty Routine into one that runs the template — Tables to hold
state, Flows to do work, Schedules and Webhooks to invoke them. The CLI and
the API call a Routine a *channel* and its template an *app*, so the commands
below keep those names; the CLI's `channel templates` command and
`--template` flag name the template. The
[glossary](https://docs.popcorn.ai/glossary.md) has the product's words.

> **Which path you are on decides how fast you can iterate.** A *new*
> template (a new `app_type`) is not self-serve: the set of installable
> templates is fixed on the server, and adding to it takes an internal change
> plus a deploy that no CLI command and no public endpoint can perform. But
> *changing* a template that already exists is a loop you run yourself — over
> MCP with `copy_routine_template` and `create_routine_version`, or from the
> CLI with `popcorn app fork`, `checkout` and `publish` — with no deploy in
> it. Both paths are in "How a Bundle gets installed".

This guide is the order to do things in. What a Bundle may contain is in the
concept pages it links ("What a Bundle is", "What the Manifest declares" and "Writing Flows"), and the Activities a Flow can call come
from the server, because they would rot here:

```bash
popcorn flow activities --summary              # what can I call?
popcorn flow activities --name <wire.name>     # what do I pass it?
popcorn flow activities --json                 # full arg + result schemas
popcorn flow validate my_flow.yaml             # is this reference real?
popcorn app validate ./mytemplate              # does the bundle hold together?
```

`flow validate` asks the server and is the authority on a Flow. When this
guide or a concept page and the validator disagree, the validator is right and
the page has a bug. `app validate` works from a copy of the server's rules
that ships with the CLI, so an older CLI can reject a construct the platform
accepts. When the two disagree, upgrade the CLI before changing the Bundle.
Run from a Checkout of the Head of the Workspace's own Copy of the template
(the CLI calls the Copy a *fork line*, and this a *fork checkout*), logged in, with a Routine (`--channel`, else the Checkout's), and with edits
since the Checkout, it also
sends them to the server, which runs the checks `app publish` runs without
publishing: the Manifest's `tables:` and `states:` among them. Otherwise it
runs everything else and prints `server checks: skipped` with the reason.

Its own checks answer a different question, and need no Routine:
will Install do what you think, and do the files agree with each other?
Everything it reports passes `flow validate` cleanly — a fixture named
`.yaml`, a write to an undeclared Column, a Schedule naming a Flow that is not
there. Run both; neither subsumes the other.

The shipped `alerttracker` template is the running example: one producer
(Alertmanager), a Webhook whose Flow names every field by path with
`fields.extract` and upserts one Row per alert, and no model anywhere in it.
The choice it embodies — *extract* fields the payload states, or *derive* ones
it does not — is
[extracting fields or deriving them](https://docs.popcorn.ai/extract-or-derive.md), and it is the
single most consequential choice in a Webhook-backed template.
[`examples/alerttracker/GOTCHAS.md`](https://github.com/PopcornAiHq/popcorn-cli/blob/main/examples/alerttracker/GOTCHAS.md) is
the raw evidence log from building an LLM-normalised, multi-producer version
of that template, and is behind most of the rules the concept pages state. Read it
as a record: it says so itself, and some of its findings predate the
[Merge Policies](https://docs.popcorn.ai/merge-policy.md).

> **Do not copy a Bundle out of a repo.** The cut-down Bundles under the CLI
> repo's `tests/fixtures/bundles/` exist to exercise `app validate`; none
> declares a `version:`, so none can publish, and they do not match what the
> platform ships. **Get Bundle source from the server** — see "Changing a Routine Template that exists", where
> `app checkout` hands you the deployed Version of a real one.

---

## What a Bundle is

```
mytemplate/
├── manifest.yaml        tables, schedules, webhooks, config, scalars
├── AGENT.md             notes the channel agent reads on demand
├── README.md            human docs, installed as a file in the Routine
├── recipe.yaml          the state graph, only when the manifest declares recipe:
└── some_flow.yaml       one flow per file, at the root
```

Only `manifest.yaml` is meaningful on its own, and a Publish needs it — with
a `version:` — so everything else is optional. The full tree, the reserved
names and what Publish leaves behind are
[App Bundles](https://docs.popcorn.ai/app-bundle.md). Two rules from it that cost the most when
missed:

- **Every other root-level `.yaml` is a Flow**, and a nested one is not a Flow
  at all. Keep Flows at the root, and keep sample payloads and fixtures
  **outside** the Bundle directory: anything the format does not name is left
  behind at Publish and reported by `app validate` as `path-not-published`.
- **A Flow's identity is its `name:`, not its filename**, so renaming `name:`
  is one Flow leaving and another arriving; see
  [a Flow's identity is its name](https://docs.popcorn.ai/flow-grammar.md#a-flow-s-identity-is-its-name).

## How a Bundle gets installed

**Two paths, and which one you are on depends on whether the template
already exists.** Creating a new one costs a server deploy. *Changing* one is
a loop you run yourself, from an assistant over MCP or from the CLI.

### A new Routine Template — not self-serve

Only the first and last steps are yours. The two in the middle happen on the
Popcorn side and are not exposed through the CLI or the public API:

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

**Publish after the deploy** — that ordering is the part worth carrying even
though you do not run either step. A Bundle whose Flows call a new Activity
must not become installable before the workers that can run it exist: a Routine
created from it inside that window installs cleanly and then fails on the first
Run, with nothing to point at. Nothing enforces the ordering; it is release
discipline.

No public endpoint takes a *new* template off your disk. `channel create --template`
only resolves names the server already carries, so a genuinely new `app_type`
has to go through that internal path — and `popcorn channel templates` is how
you check whether it has landed.

### Changing a Routine Template that exists

A Routine already running a template can be changed with no deploy and no
hand-off to anyone. An assistant connected to Popcorn over MCP runs the loop
without a working copy; the CLI runs it from a Checkout. Each step names the
MCP tool first and the CLI command beside it:

1. **Check the settings.** `list_routine_settings`, then
   `update_routine_setting`. CLI: `popcorn channel-config params set` for a
   parameter, `popcorn table scalar set` for a switch. Often this is the
   whole change; see below.
2. **Read the files.** `list_routine_files`, then `read_routine_file` per
   file. CLI: `popcorn app checkout --channel '#chan'`.
3. **Copy the template.** `copy_routine_template`, with a name for the Copy.
   CLI: `popcorn app fork`, then `popcorn app checkout --channel '#chan'`
   again, because `app publish` refuses a Checkout of Popcorn's own version;
   or `app checkout --fork` to copy and check out in one command. Each
   Version published to the Copy is what the CLI calls a *bundle version*.
4. **Edit, and check.** `create_routine_version` without `confirm`: its dry
   run reports every check Publish would fail, each file's diff and the
   reach, and changes nothing. CLI: edit the Checkout, then
   `popcorn app validate ./<app>`.
5. **Publish a Version.** `create_routine_version` again, with
   `confirm=true` and the `plan_id` a dry run on the Copy gave. CLI:
   `popcorn app publish ./<app> --bump patch -m "what changed" --yes`.
6. **Confirm the Install landed.** `get_routine`, whose `Install:` field says
   whether it has; `wait_seconds` waits up to 20 seconds for an Install in
   progress to land. CLI: `popcorn app status`.
7. **Only if it did not land, retry it.** `install_routine`. CLI:
   `popcorn app apply`.

Over MCP, the Copy can wait until a dry run passes: a Routine still on
Popcorn's own template can dry-run a change, and needs its own Copy only to
publish it, so the step that cannot be undone comes after the check. That
dry run holds no plan and shows no reach. After `copy_routine_template`, call
`create_routine_version` again with the same `base_version`, changes and
changelog: the Copy starts with the same files, so the Version the first
dry run was based on names the Copy's first Version. Confirm with the
`plan_id` from that second dry run, which shows the reach.

Copying a template, a new Version, an Install onto another Copy and a
change to a setting are each a dry run until called again with
`confirm=true`. An `install_routine` with no `copy` on a Routine behind its
Copy, and `create_routine` with no template, start at once; and
`change_routine` with a `request` starts drafting at once, though it
installs nothing until confirmed. `create_routine_version` takes changes, not a tree: each one
creates, deletes, renames or edits one file with text ops, and an edit
carries the `sha256` it was read at. A file the assistant generated rather
than typed goes up through `create_routine_file_upload`. The
[MCP reference](https://docs.popcorn.ai/mcp.md) has the arguments.

From the CLI, the loop is:

```bash
# make this workspace's own copy, then check its head out — one command
popcorn app checkout --channel '#chan' --fork
# ... edit
popcorn app validate ./<app>
popcorn app publish ./<app> --bump patch -m "what changed" --yes
popcorn app status ./<app>              # has the install landed?
```

`app publish` asks for confirmation before it sends anything, because a
Publish changes every Routine on the Copy, not only yours. In a terminal
you answer the prompt. In agent mode (`POPCORN_AGENT=1`) or any
non-interactive shell there is no one to answer, so the Publish is refused
unless it carries `--yes` (or `POPCORN_ASSUME_YES=1`) — pass it once that
reach is what you mean. The examples here include it because an agent or a
script is usually what runs them.

`--bump patch|minor|major` writes `version:` in `manifest.yaml` for you, off
the Copy's Head, and only once the Publish has been accepted — so a
Publish that fails leaves the working copy untouched and re-running the same
command is the retry. Editing `version:` by hand still works; `--bump` is
refused when the Manifest already advances past the Head, because counting
from the Head would overwrite that number and counting from the Manifest
would skip the Versions in between. Reach for the flag or the hand edit, not
both in one Publish.

`-m` records what changed on the Version, exactly like `git commit -m`
(`--changelog` is the deprecated spelling and still works). **Note what it
does not do:** `manifest.yaml`'s own `changelog:` key is not read by a Publish
to a Copy — the server records the request's message and nothing else — so a
Manifest that declares one while you pass no `-m` records nothing at all, and
Publish says so. Nor is there any command that reads a published Version's
message back: no endpoint serves it. The line `app publish` prints is the one
chance to see what landed.

**Check the settings before you copy.** A change to how one Routine behaves —
a sending mode, a Schedule's cadence, a limit, a prompt or email template — is
often one of its Routine Settings (step 1). A setting
reaches that Routine alone, can be set back, and survives the template's
updates. A Copy is permanent and reaches every Routine on it, so copy only for
what a setting cannot express: a Table, a Flow, a State Machine.

Publishing needs a Copy: a Publish lands on a Copy **this
Workspace owns**, so publishing from a Routine still bound to the shared
product version (Popcorn's own template, which the CLI prints as a
*PRODUCT* version) is refused. `app publish` also starts the Install that moves
your Routine onto the new Version, and that Install converges on its own —
`app status` confirms it rather than causing it.

The bump is not optional either, and inside a Checkout `app validate` is
where you find that out. A published Version is immutable, so `version:` must
strictly advance past the one the Checkout came from; leaving it alone gets you
a `version-not-advanced` error offline instead of a server refusal after the
upload. Leaving `changelog:` exactly as the Checkout wrote it while `version:`
advances is a warning (`changelog-not-updated`) rather than an error, because
the Checkout arrives carrying the *previous* Version's note — so keeping it is
the default outcome, not an unlikely one. The warning says which job the field is doing for the kind
of Checkout you are in: in a fork checkout it is documentation that ships with the Bundle
and `-m` is what records a note on the Version, matching what `app publish`
tells you rather than contradicting it. Both checks read the baseline
`app checkout` wrote and are skipped entirely on a directory that is not a
Checkout.

A Checkout writes two files that are not Bundle content: `.popcorn-app.json`,
the baseline above, and `CLAUDE.md`, which tells a coding agent opening a file
in the directory that this is a Bundle and that an edit is not a release until
`app validate` and `app publish` have run. Neither publishes. `CLAUDE.md` is
yours once written — a re-checkout leaves your edits to it alone unless you
pass `--force` — and it is not `AGENT.md`, which *is* Bundle content and ships
to every Routine that installs the template.

`app apply` is **not** a step in this loop. It is the retry for an Install that
did not land: the Routine had its template's updates locked, another Install
held it, or it failed. Run it when `app status` says the Routine is still
behind its Copy's Head, not by habit.

**From outside a Checkout**, `app status --channel <channel>` answers the same
question against server state alone — no working copy needed:

```bash
popcorn app status --channel '#chan'
popcorn app status --channel '#chan' --json | jq -r '.data.install.state'
```

`install.state` is `current` (the Routine runs its Copy's Head) or says
why it does not: `installing`, `retrying`, `locked`, `failed`, `skipped` or
`behind`. Poll that field rather than grepping a semver out of `app list`
output. A failed Install comes with its error, an `error_code` and its attempt
count — only `invalid_manifest`, `invalid_schedule` and `bundle_rejected` mean
the Head needs fixing, and `internal` means the platform failed, so no edit or
Publish helps (report it with the workflow id) — a skipped one with its reason, and the text output carries a `Next:` line saying what moves
the Routine on — for a failed, skipped or behind Routine on a Copy, `app apply
--channel <channel>`. The older `install_state` field is still there, as
`current` or `pending` for every other state.

`--fork` takes an optional name for the Copy (`--fork=experiment`); bare, it
names the Copy it is about to use and asks, because a Workspace's single
existing Copy can be far behind Popcorn's own template. `-y` answers that. `popcorn app fork` on its own is still there and does the
same thing without the Checkout.

**This is also how you read a real Bundle.** `app checkout` returns the whole
tree — Manifest, every Flow, `AGENT.md`, `strings.yaml` — for the Head of the
Copy the Routine runs (normally the very Version it is bound to; the two
differ only while an Install has not landed), so it is the one source that
cannot be stale. `app checkout --version <id>` reads an earlier Version of the
same line instead, read-only — the way to recover the tree from before a bad
Publish (see `versions`).
When you want to study how a shipped template does something, spend a scratch
Routine on it rather than looking for a copy in a repo:

```bash
popcorn channel create '#scratch' --template alerttracker
popcorn app checkout --channel '#scratch'          # read it as it ships
popcorn app checkout --channel '#scratch' --fork   # ... or to edit it
```

Reading needs no Copy — a Checkout taken without one records `"kind": "product"` and
publishing from it is refused, which is the point. Copy when you intend to
edit, and note what that costs: a Copy is permanent and cannot be
deleted, so make one in a Workspace you do not mind accumulating one in.
`popcorn app lines` is how you see what has accumulated.

Three things about this loop that are easy to get wrong:

- **`version:` in `manifest.yaml` must advance every Publish.** Versions
  only ever move forward; the CLI refuses a reused or lower number locally
  rather than letting the registry 409 at you.
- **A Publish is not scoped to the Routine you tested on.** Every other Routine
  on the same Copy catches up on its own nightly auto-update tick.
- **One Copy per (Workspace, template).** There is no parallel-experiment path
  without naming a second Copy (`app fork --name`).

`popcorn app list` shows Popcorn's own line and any Copy this Workspace
owns; add `--channel '#chan'` to see what that Routine currently runs.

### The template list is filtered by your Release Track

`popcorn app list` and `popcorn channel templates` show what **your Workspace's
Release Track** can see — alpha, beta or stable, per-workspace and defaulting
to stable. A template released only to alpha is invisible and uninstallable for a
Workspace enrolled on stable.

**The API says nothing about why**, deliberately: enrollment is internal, and a
test enforces that it does not leak. So `channel create --template X` returns a
neutral 400 for a template your track cannot see, indistinguishable from a typo.
The CLI cannot diagnose this and does not try. If a template you know shipped is
missing from the list, that is the first thing to suspect — ask rather than
debug.

## What the Manifest declares

Every key is optional, and each has its own Install semantics:
[Manifest keys and what Install does to them](https://docs.popcorn.ai/manifest-keys.md) is the
table. The keys with pages of their own:

| Key | Page |
|---|---|
| `tables` | [Table Columns](https://docs.popcorn.ai/table-columns.md) and [Column Merge Policy](https://docs.popcorn.ai/merge-policy.md); adding one end to end is [adding a Table](https://docs.popcorn.ai/adding-a-table.md) |
| `scalars`, `default_scalars` | [Scalar tiers and Routine Settings](https://docs.popcorn.ai/scalar-tiers.md) |
| `schedules` | [Schedules in a Manifest](https://docs.popcorn.ai/schedules.md) |
| `states` | [State Machines in a Bundle](https://docs.popcorn.ai/state-machine.md); writing one is [authoring a States tier](https://docs.popcorn.ai/states-authoring.md) |
| `recipe` | the same graph as a root `recipe.yaml` each Routine can replace — the Recipe section of [State Machines in a Bundle](https://docs.popcorn.ai/state-machine.md); it is written like a `states:` section |

Three traps are worth carrying into every edit:

- **An absent key leaves the Routine alone; an empty one means "replace with
  nothing."** `schedules: []` deletes every Manifest-managed Schedule.
  Omitting `schedules:` does not.
- **An unknown top-level key is silently ignored.** A typo such as
  `schedule:` installs nothing and reports nothing.
- **An untyped Bundle CLEARS the Routine's `app_type`** and `channel_agent`.
  A Publish to a Copy does not refuse one: it reaches every Routine on the
  Copy and clears both on each. `app validate` warns (`clears-app-type`);
  treat that warning as an error on a Copy.

## Writing Flows

A Flow's grammar is four concept pages, each answering one question:

- [The shape of a Flow](https://docs.popcorn.ai/flow-grammar.md): the file's keys, the five kinds
  of Step, blocks, `call_flow` and `foreach`.
- [References in a Flow](https://docs.popcorn.ai/references.md): the `$` roots, the syntax,
  and why nothing in a reference computes.
- [Conditions in a Flow](https://docs.popcorn.ai/conditions.md): `when:`'s two rails, and
  filtering Rows instead of gating Steps.
- [Step errors and retries](https://docs.popcorn.ai/on-error.md): `on_error`, the default of
  four attempts, and what no policy catches.

Reading fields off a Webhook payload is
[extracting fields or deriving them](https://docs.popcorn.ai/extract-or-derive.md).

## The authoring loop

Three loops, and picking the right one is most of the speed. The **inner**
loop publishes nothing and runs as often as you like:

```bash
popcorn app validate .                               # server checks: logged in, in a checkout of a copy
popcorn flow activities --name <wire.name>           # what do I pass it?
popcorn flow validate my_flow.yaml                   # per file, fast
```

`flow validate` needs a Routine only as an auth/context handle — any Routine
you can reach will do; it never writes. Run from an `app checkout` and it
takes the Routine from the Checkout's baseline, the same way `app publish`
and `app status` do; pass `--channel <id>` anywhere else.

The **middle** loop is the loop on a Copy from "Changing a Routine Template that exists", and it is the one to reach
for whenever the template already exists. No deploy, no hand-off, seconds per turn:

```bash
popcorn app publish ./<app> --bump patch -m "..." --yes   # mint the next version
popcorn app status ./<app>                           # has the install landed?
popcorn app lines                                    # what copies exist?
popcorn channel-config show --channel <id> --strict  # is the Routine wired up?
popcorn flow runs list --channel <id> --flow <name>   # filtered on the server
```

`app lines` is the inventory of Copies — name, Head semver, and when that
Head was published — and it is worth a look before copying, because a
nameless `app fork` adopts whatever single Copy exists and the server refuses
outright once there are two. The Copies listed are the Workspace's, and it
needs no Routine. Two things it cannot tell you, both because the API does
not carry them: how many Routines ride each Copy, and how to delete one.
Neither exists, so Copies accumulate.

`channel-config show` is worth running the first time a Bundle installs: it
diffs every `$channel.*` reference your Flows make against what the Routine
actually has — its parameters (Routine Settings) and its Integrations
(Connections) — and `--strict` exits non-zero on the three findings that make a
Run fail — a referenced parameter that is not set, a declared Integration that
is not connected, and a Connected Account whose provider contradicts a
declaration. The two `unused_*` findings are informational; Routine Settings and
Connections every Flow shares legitimately carry keys one Flow does not read.

The **outer** loop is only for a NEW Routine Template, and costs a server deploy plus
a Publish (see "A new Routine Template — not self-serve"), so get the inner one clean first:

```bash
# ... the app_type is registered, deployed and published (see "A new Routine Template — not self-serve"; internal)

popcorn channel templates                            # is my version installable?
popcorn channel create '#chan' --template mytemplate # note the UUID — see below

popcorn webhook list <id>                            # names and ids
popcorn webhook list <id> --show-url                 # + the ingest URL
popcorn webhook send Intake @fixtures/sample.json --channel <id>

popcorn flow runs list --channel <id>
popcorn flow runs get <workflow-id> --channel <id> --include-errors
popcorn flow runs cancel --flow <flow-name> --channel <id>   # stop every running run of a flow
popcorn table rows alerts --channel <id>
popcorn table schema alerts --channel <id>
```

Because the outer loop is expensive, a Bundle that installs but is wrong costs
a whole deploy cycle to correct — which is the argument for `app validate`
and `flow validate` being pedantic, and for exercising boundaries (below) the
first time you get a real Routine rather than the third.

Once the template exists, a wrong Bundle costs an `app publish` rather than a
deploy. The *first* Version of a new template still has to be right, though,
and a Publish to a Copy still moves every other Routine on it.

A `#name` that matches more than one Routine — a case variant, or a Routine
shared in from another Workspace — is refused with each candidate's id. Pass
the id in its place; `--workspace` does not narrow the lookup.

`flow run` accepts a Flow **name or UUID**, and defaults `conversation_id`
into the inputs from `--channel`:

```bash
popcorn flow run basic_tick --channel <id> --wait
```

Pass `--inputs` for a Flow's own arguments; an explicit `conversation_id`
there always wins, so a Flow can still target another Routine.

```bash
popcorn flow run seed_test_alert --channel <id> \
  --inputs '{"severity":"critical","fingerprint":"0000000000000002"}' --wait
```

Every Run carries `outcome`: `succeeded`, `failed` or `still_running`. Poll
that field, not `status` — `--wait` does. To change one parameter in a Routine's
Settings without rewriting the others, use `popcorn channel-config params set` and
`params unset`.

### Checks will not save you

Every defect found while building the example Bundle passed `flow validate`
cleanly, because they were runtime semantics rather than bad references: a
Merge Policy overwriting a first-seen timestamp, an LLM inventing a Row, an
optional schema property going missing, a write to an undeclared Column.

`app validate` was written from that list and now catches the last two —
plus the whole class of cross-file mistakes a per-file validator cannot see:

```bash
popcorn app validate .            # errors exit non-zero
popcorn app validate . --strict   # warnings do too — this is the CI form
```

It cannot catch the first two. A Merge Policy is only wrong relative to what
you meant, and no offline tool knows an LLM is about to invent a Row.

**So install it and run it.** A seed Flow such as `alerttracker`'s
`seed_test_alert` exists purely so a Bundle can be exercised without a real
producer — it sends a canned payload through the same ingest Flow a real
Delivery takes.

And exercise the **boundary**, not the happy path. A sweep that resolves
everything Completes just as cheerfully as a correct one; the only proof a
cutoff works is that a Row just inside it moves and a Row just outside it does
not.

Watch for these when reading results:

- Many Activities have permissive result schemas (`additionalProperties:
  true`). For those, `$steps.x.output.anything` **passes validation** — and at
  runtime a key the response lacks is a hard `ReferenceError: … key not
  found`; only a null partway along the path resolves to null. Verify against
  the real response, not the catalog.
- `start_flow` is asynchronous. A parent that launches a child reports
  Completed immediately; check the **child's** Run. When the parent needs the
  result, use a `call_flow:` Step with `mode: wait` instead (see
  [the shape of a Flow](https://docs.popcorn.ai/flow-grammar.md)).
- Posting the same Webhook body twice does not test your merge logic — the
  *Webhook layer* drops a Delivery whose body is byte-identical (SHA-256) to
  one seen in the last five minutes, and no Flow runs at all. Vary the body
  while keeping the identity fields.
- A field that might be **absent** must never be dereferenced. A missing key
  is a hard `ReferenceError` that fails the Run, and `on_error` does not
  rescue it — reference resolution happens before the Activity is invoked.
  Guarantee presence upstream: in an `output_schema`'s `required`, or with
  `$exists: true` in the query that produced the Rows.


## Before you publish

Each line is a rule a concept page explains; every one of them has cost a
Publish.

1. `version:` advances every Publish, and `--bump` is the way to do it (see "Changing a Routine Template that exists").
2. The Manifest keeps `app_type:` and `channel_agent:` (see "What the Manifest declares").
3. No Flow-written value is declared under `scalars:` —
   [Scalar tiers and Routine Settings](https://docs.popcorn.ai/scalar-tiers.md).
4. Every Schedule's `flow:` names a Flow the Bundle has —
   [Schedules](https://docs.popcorn.ai/schedules.md).
5. Table changes only add: no Column is dropped or renamed, and a Column a
   Flow dereferences has no spaces — [Table Columns](https://docs.popcorn.ai/table-columns.md).
6. A Step with a side effect sets `retry: 0` —
   [Step errors](https://docs.popcorn.ai/on-error.md).
7. Every key a reference reads is guaranteed upstream, by `required` in an
   `output_schema` or `$exists: true` in a filter —
   [references](https://docs.popcorn.ai/references.md).
8. A second condition in a `when:` did not change how the first compares —
   [conditions](https://docs.popcorn.ai/conditions.md).
9. Fields the payload states are extracted, not derived —
   [extract or derive](https://docs.popcorn.ai/extract-or-derive.md).
10. A markdown post sets `format: markdown`, on every edit too —
    [the shape of a Flow](https://docs.popcorn.ai/flow-grammar.md).
