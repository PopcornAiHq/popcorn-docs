---
id: template-authoring
title: Authoring a channel template
summary: >
  A channel template is a directory of YAML that turns an empty channel into an application. This is the whole authoring loop: what a bundle holds, how it reaches a channel, the manifest keys, flow grammar and table schemas, and the traps. Where it disagrees with `flow validate` or `template check`, the tool is right and the guide has a bug.
concepts: [app-bundle, manifest-keys, publish-and-apply, fork-line, merge-policy]
applies_to: [cli, mcp, human]
---

A **channel template** is a directory of YAML that turns an empty Popcorn
channel into an application: tables to hold state, flows to do work, schedules
and webhooks to invoke them.

> **Which path you are on decides how fast you can iterate.** A *new* app type
> is not self-serve: the set of installable templates is fixed on the server,
> and adding to it takes an internal change plus a deploy that no CLI command
> and no public endpoint can perform. But *editing* an app that already exists
> is a pure CLI loop — `popcorn app fork`, `checkout`, `publish` — with no
> deploy in it. Both paths are §2. `popcorn flow import` is gone and neither
> path replaces it.
>
> Everything else in this guide applies to both: the grammar, the manifest
> semantics, and `popcorn template check` are about the bundle itself, not
> about how it gets installed.

This guide is what you need that the API cannot tell you. It deliberately does
**not** list activities or their arguments — those come from the server and
would rot here:

```bash
popcorn flow activities --summary              # what can I call?
popcorn flow activities --name <wire.name>     # what do I pass it?
popcorn flow activities --json                 # full arg + result schemas
popcorn flow validate my_flow.yaml             # is this reference real?
popcorn template check ./mytemplate            # does the bundle hold together?
```

`flow validate` is the authority on a reference. When this guide and the
validator disagree, the validator is right and this guide has a bug.

`template check` answers a different question, offline and with no channel:
will the importer install what you think, and do the files agree with each
other? Everything it reports passes `flow validate` cleanly — a fixture named
`.yaml`, a write to an undeclared column, a schedule naming a flow that is not
there. Run both; neither subsumes the other.

The shipped `alerttracker` app is the running example: one producer
(Alertmanager), a webhook whose flow names every field by path with
`fields.extract` and upserts one row per alert, and no model anywhere in it.
The choice it embodies — *extract* fields the payload states, or *derive* ones
it does not — is §6, and it is the single most consequential choice in a
webhook-backed template.
[`examples/alerttracker/GOTCHAS.md`](https://github.com/PopcornAiHq/popcorn-cli/blob/main/examples/alerttracker/GOTCHAS.md) is
the raw evidence log from building an LLM-normalised, multi-producer version
of that app, and is behind most of the rules below. Read it as a record: it
says so itself, and some of its findings predate the merge policies in §5.

> **Do not copy a bundle out of a repo.** The cut-down bundles under the CLI
> repo's `tests/fixtures/bundles/` exist to exercise `template check`; none
> declares a `version:`, so none can publish, and they do not match what the
> platform ships. **Get bundle source from the server** — see §2b, where
> `app checkout` hands you the deployed version of a real one.

---

## 1. What a bundle is

```
mytemplate/
├── manifest.yaml        tables, schedules, webhooks, config, scalars
├── AGENT.md             notes the channel agent reads on demand
├── README.md            human docs, installed as a channel file
└── some_flow.yaml       one flow per file, at the root
```

Only `manifest.yaml` is meaningful on its own, and a publish needs it — with
a `version:` — so everything else is optional. Sample payloads and
notes belong **outside** the bundle directory — anything the format does not
name is left behind at publish and reported by `template check` (§2).

## 2. How a bundle gets installed

**Two paths, and which one you are on depends on whether the app already
exists.** Creating a new app type still costs a server deploy. *Changing* one
is now entirely a CLI loop.

### 2a. A new app type — not self-serve

Only the first and last steps are yours. The two in the middle happen on the
Popcorn side and are not exposed through the CLI or the public API:

```
your bundle dir                                    (author here)
      │
      ├─▶ the new app type is registered and the workers
      │   that run its flows are deployed            (internal)
      │
      ├─▶ the bundle is published to the template registry
      │                                              (internal)
      │
      └─▶ popcorn channel create '#chan' --template <name>
```

**Publish after the deploy** — that ordering is the part worth carrying even
though you do not run either step. A bundle whose flows call a new activity
must not become installable before the workers that can run it exist: a channel
created from it inside that window installs cleanly and then fails on the first
run, with nothing to point at. Nothing enforces the ordering; it is release
discipline.

No public endpoint takes a *new* app off your disk. `channel create --template`
only resolves names the server already carries, so a genuinely new `app_type`
has to go through that internal path — and `popcorn channel templates` is how
you check whether it has landed.

### 2b. Changing an app that exists — `popcorn app`

A channel already running a bundle can be edited from the CLI, with no deploy
and no hand-off to anyone:

```bash
# fork onto this workspace's own line, then check its head out — one command
popcorn app checkout --channel '#chan' --fork
# ... edit
popcorn template check ./<app>
popcorn app publish ./<app> --bump patch -m "what changed"
popcorn app status ./<app>              # has the install landed?
```

`--bump patch|minor|major` writes `version:` in `manifest.yaml` for you, off
the fork line's head, and only once the publish has been accepted — so a
publish that fails leaves the working copy untouched and re-running the same
command is the retry. Editing `version:` by hand still works; `--bump` is
refused when the manifest already advances past the head, because counting
from the head would overwrite that number and counting from the manifest
would skip the versions in between. Reach for the flag or the hand edit, not
both in one publish.

`-m` records what changed on the version, exactly like `git commit -m`
(`--changelog` is the deprecated spelling and still works). **Note what it
does not do:** `manifest.yaml`'s own `changelog:` key is not read by a fork
publish — the server records the request's message and nothing else — so a
manifest that declares one while you pass no `-m` records nothing at all, and
publish says so. Nor is there any command that reads a published version's
message back: no endpoint serves it. The line `app publish` prints is the one
chance to see what landed.

The fork comes first and is not optional: a publish lands on a fork line **this
workspace owns**, so publishing from a channel still bound to the shared
product version is refused. `app publish` also starts the install that moves
your channel onto the new version, and that install converges on its own —
`app status` confirms it rather than causing it.

The bump is not optional either, and inside a checkout `template check` is
where you find that out. A published version is immutable, so `version:` must
strictly advance past the one the checkout came from; leaving it alone gets you
a `version-not-advanced` error offline instead of a server refusal after the
upload. Leaving `changelog:` exactly as the checkout wrote it while `version:`
advances is a warning (`changelog-not-updated`) rather than an error, because
the checkout arrives carrying the *previous* version's note — so keeping it is
the default outcome, not an unlikely one. The warning says which job the field is doing for the line
you are on: in a fork checkout it is documentation that ships with the bundle
and `-m` is what records a note on the version, matching what `app publish`
tells you rather than contradicting it. Both checks read the baseline
`app checkout` wrote and are skipped entirely on a directory that is not a
checkout.

A checkout writes two files that are not bundle content: `.popcorn-app.json`,
the baseline above, and `CLAUDE.md`, which tells a coding agent opening a file
in the directory that this is a bundle and that an edit is not a release until
`template check` and `app publish` have run. Neither publishes. `CLAUDE.md` is
yours once written — a re-checkout leaves your edits to it alone unless you
pass `--force` — and it is not `AGENT.md`, which *is* bundle content and ships
to every channel that installs the app.

`app apply` is **not** a step in this loop. It is the retry for an install that
did not land: the channel had app updates locked, another install held it, or
it failed. Run it when `app status` says the channel is still behind its line,
not by habit.

**From outside a checkout**, `app status --channel <channel>` answers the same
question against server state alone — no working copy needed:

```bash
popcorn app status --channel '#chan'
popcorn app status --channel '#chan' --json | jq -r '.data.install_state'
```

`install_state` is `current` (the channel runs its fork line's head) or
`pending` (it does not). Poll that field rather than grepping a semver out of
`app list` output. One caveat worth knowing: the API exposes no status for the
install job itself, so `pending` cannot distinguish an install still running
from one that failed — `app apply --channel <channel>` is the retry for both.

`--fork` takes an optional line name (`--fork=experiment`); bare, it names the
line it is about to use and asks, because a workspace's single existing line
can be anywhere — one production line sat 23 minor versions behind product.
`-y` answers that. `popcorn app fork` on its own is still there and does the
same thing without the checkout.

**This is also how you read a real bundle.** `app checkout` returns the whole
tree — manifest, every flow, `AGENT.md`, `strings.yaml` — for the head of the
fork line the channel runs (normally the very version it is bound to; the two
differ only while an install has not landed), so it is the one source that
cannot be stale.
When you want to study how a shipped app does something, spend a scratch
channel on it rather than looking for a copy in a repo:

```bash
popcorn channel create '#scratch' --template alerttracker
popcorn app checkout --channel '#scratch'          # read it as it ships
popcorn app checkout --channel '#scratch' --fork   # ... or to edit it
```

Reading needs no fork — a fork-less checkout records `"kind": "product"` and
publishing from it is refused, which is the point. Fork when you intend to
edit, and note what that costs: a fork line is permanent and cannot be
deleted, so do it in a workspace you do not mind accumulating one in.
`popcorn app lines --channel <id>` is how you see what has accumulated.

Three things about this loop that are easy to get wrong:

- **`version:` in `manifest.yaml` must advance every publish.** Bundle versions
  only ever move forward; the CLI refuses a reused or lower number locally
  rather than letting the registry 409 at you.
- **A publish is not scoped to the channel you tested on.** Every other channel
  on the same fork line catches up on its own nightly auto-update tick.
- **One fork line per (workspace, app).** There is no parallel-experiment path
  without naming a second line (`app fork --name`).

`popcorn app list --channel '#chan'` shows the product line, any fork line this
workspace owns, and what the channel currently runs.

### The app list is filtered by your release track

`popcorn app list` and `popcorn channel templates` show what **your workspace's
release track** can see — alpha, beta or stable, per-workspace and defaulting
to stable. An app released only to alpha is invisible and uninstallable for a
workspace enrolled on stable.

**The API says nothing about why**, deliberately: enrollment is internal, and a
test enforces that it does not leak. So `channel create --template X` returns a
neutral 400 for an app your track cannot see, indistinguishable from a typo.
The CLI cannot diagnose this and does not try. If an app you know shipped is
missing from the list, that is the first thing to suspect — ask rather than
debug.

### What the reader does with your files

The registry reads your directory off disk and classifies every path:

- **Reserves four names**: `manifest.yaml`, `AGENT.md`, `README.md`, and
  `strings.yaml` (client copy — `config.yaml` is a legacy manifest alias).
  Most shipped templates carry a `strings.yaml`; it is optional.
- **Treats every other root-level `.yaml` / `.yml` as a flow.** Flows are read
  from the bundle root only, so a stray `.yaml` there is installed as a flow
  (`template check` reports one with no `name:`/`steps:`), while a nested
  `.yaml` is not a flow at all.
- **Descends `prompts/` and `templates/`**, one level, seeding
  `$channel.prompts.<stem>` and `$channel.templates.<stem>`.
- **Descends `code/<block>/` to any depth** — one directory per custom code
  block, so a block may be a small package rather than a single file. The block
  name is a slug (it rides inside flow YAML as `code_name:`), and every segment
  below it must be visible: the server refuses a tree with a hidden entry
  there, and `app publish` drops dotfiles under `code/` before upload — so from
  the CLI a hidden file is silently left behind rather than refused.
  Unlike the two directories above, files here are **not** seeded into channel
  config — `foundation.code.execute` reads them by block name at run time.
- **Reads `agents/<name>/`** — one directory per agent the bundle defines for
  itself: `agent.yaml`, `prompt.md` and `schemas/*.json`, parsed and refused at
  publish if they would not run. The CLI does not currently upload this
  directory: `app publish` leaves `agents/` behind like any other unrecognized
  path.
- **Does not read anything else.** A `fixtures/` directory, a `notes.txt`, a
  file nested a level too deep: `template check` reports each as
  `path-not-published` (a warning, so `--strict` fails), `app publish` leaves
  it behind, and the server refuses such a path if one reaches it. Only
  dotfiles and `__pycache__` are dropped without comment. Move fixtures
  outside the bundle directory — renaming them to `.json` does not make them
  part of the format.

A block file may carry any extension, `.yaml` included, and is block source
rather than a flow. `template check` reports `code-file-outside-block` for a
loose file directly under `code/` and `code-block-name-invalid` for a name that
is not a slug — both are trees `app publish` refuses.

**Keep flows at the root.** A flow in a subdirectory is not a flow: through
`app publish` it never gets that far — the CLI reports it and leaves it behind
— and `template check` flags the nesting.

**Flow identity is the `name:` inside the YAML, not the filename.** A name
matches `FLOW_NAME_RE` — `^[a-z0-9][a-z0-9_-]{0,62}$`: lowercase, digits,
`_` and `-`, not starting with `_`, at most 63 characters. No flow is copied
into a channel: schedules, webhooks and runs resolve flows by name from the
flow index of the version the channel is bound to. So renaming `name:` is one
flow leaving and another arriving — the old name disappears the moment a
channel binds the new version, and anything still pointing at it points at
nothing.

## 3. Manifest keys

Every key is optional. The install semantics differ per key and getting this
wrong is how you wipe a live channel's state.

| Key | Semantics | Notes |
|---|---|---|
| `display_name`, `description` | catalog copy | for the template picker |
| `version` | bundle semver | **required to publish**; shape-validated when present |
| `changelog` | the version's note | a fork publish ignores it and records `-m` instead (§2b) |
| `app_type` | sets the channel's app | **written or cleared every install** — see the warning below |
| `channel_agent` | the channel's agent | written or cleared every install, exactly like `app_type` |
| `tables` | **additive reconcile** | columns are added and attributes fixed, never dropped or renamed |
| `states` | a state machine over one table | requires `tables:`; see below |
| `channel_parameters`, `status_kinds` | **upsert per key**; drift-preserving on update | parameters keep their types and read as `$channel.<name>` |
| `scalars` | **upsert per key**; drift-preserving on update | never put flow-written runtime state here |
| `default_scalars` | **write once, first install only** | safe place for an operator-owned switch |
| `schedules` | **reconcile by (flow, slug)** | omitted = leave alone; `[]` = delete every manifest-managed one |
| `webhooks` | **create-if-missing** | never updated or deleted |
| `triggers`, `required_connections`, `connections`, `documents` | replace, omit-vs-empty | `[]` means "replace with nothing"; a trigger's `enabled` is a seed, applied the first time only |

The `*_declared` distinction runs through the list-shaped keys: **an absent key
leaves the channel alone; a present-but-empty key means "replace with
nothing."** `schedules: []` deletes every manifest-managed schedule. Omitting
`schedules:` does not.

**An unknown top-level key is silently ignored.** A typo such as `schedule:`
installs nothing and reports nothing, so a key that seems to do nothing is
worth spelling-checking against this table first.

`states:` declares a state machine over one declared table. It is validated as
a graph at publish, and every transition's `flow` and `then` must name a flow
in the bundle. The grammar is its own page:
[the state machine](https://docs.popcorn.ai/concepts/state-machine.md).

> **An untyped bundle CLEARS the channel's `app_type`.** A manifest with no
> `app_type:` key strips whatever was there, which changes the client's whole
> interface paradigm. Never import an untyped bundle into a channel running a
> real app. `template check` warns you (`clears-app-type`).

### Runtime state must not appear under `scalars:`

A first install, and an install by template name, write every declared scalar
unconditionally. A version update — `app publish` moving the channel on,
`app apply`, or the daily auto-update of a bound channel — is drift-preserving
per key: it writes a declared scalar only if the channel has no value for it
or still holds the *old* bundle's declared value, and otherwise keeps the
channel's. Channel config sections (`channel_parameters`, `status_kinds`) and
`AGENT.md`'s agent docs follow the same rule.

That rule is built for configuration a member may edit, and it is wrong for
state a flow maintains. If a flow writes a `last_swept_at` key the manifest
also declares, a fresh install resets it, and an update overwrites it whenever
the live value happens to equal the old declared one. Declare only
install-time configuration; let flows create their own runtime keys.
`template check` warns (`runtime-state-in-scalars`) when it sees a flow write
a scalar the manifest declares.

### Schedules address their own channel

Schedule `inputs` support two substitutions applied at install:
`<channel-conversation-id>` and `<workspace-id>`. That is how a portable
bundle passes its own channel's id into a scheduled flow.

```yaml
schedules:
  - flow: basic_tick
    slug: basic-tick
    interval: 3600         # seconds; or cron: "0 8 * * *" + timezone:
    class: periodic        # periodic | deadline | window
    overlap: skip
    jitter: 60
    inputs:
      conversation_id: <channel-conversation-id>
```

Each entry names exactly one of `interval:` or `cron:` — one naming both is
refused. `class:` is routing, not decoration: it picks the queue and how the
fire time is spread (`periodic` for an interval, `deadline` for a daily cron,
`window` for deferrable work).

Install upserts each schedule by (flow, slug), then deletes the name-keyed
schedules the manifest no longer declares; schedules a member created through
another surface are never touched. On a version update an unchanged
`schedules:` section is skipped, only schedules the *old* manifest declared
and the new one drops are deleted, and a recreated schedule keeps its paused
state and note. A schedule whose `flow:` is not in the bundle is skipped — and
is then deleted as undeclared, so a typo in `flow:` removes the schedule it
meant to keep.

## 4. Flow grammar

```yaml
name: my_flow             # identity — not the filename
version: 1
description: >
  What this does and why it is shaped this way.

inputs:
  conversation_id: { type: string }
  thing: { type: string, required: false, default: "" }

steps:
  - id: fetch
    activity: foundation.store.list_rows
    when: $inputs.thing != ''
    on_error: { policy: skip, retry: 1 }
    args: { ... }

  - id: each
    activity: foundation.store.patch_row
    foreach: $steps.fetch.output.rows
    as: row
    max_parallel: 1
    collect: patched
    args:
      record_id: $row._record_id

outputs:
  ids: $steps.fetch.output.rows
```

### Reference roots

| Root | Reads |
|---|---|
| `$inputs.*` | the run's declared inputs |
| `$steps.<id>.output.*` | a prior step's result |
| `$steps.<id>.<collect>` | a `foreach` step's collected list, under the name `collect:` gave it |
| `$channel.*` | channel config — `channel_parameters` plus the seeded `integrations` / `integration_list`; scalars are **not** here |
| `$trigger.*` | what triggered the run |
| `as:` name | the current item inside a `foreach` |

`$trigger` carries exactly `thread_id`, `message_id`, `user_id`,
`conversation_id`, `thread_root`, `contact_id`, `workflow_id`, `run_id` — a
closed set, so a typo in it is caught offline. Every key is always present; one
that does not apply to the run's trigger kind (`user_id` on a scheduled run,
say) resolves to null rather than erroring. `$channel` is not closed: its keys
come from a per-channel config the bundle cannot see, which is why an
unrecognized one is a warning.

**The root and the first segment after it start with a letter or
underscore**; the whole reference carries only letters, digits, underscores
and dots. `$a.`, `$a..b` and `$a.1b` are not references at all. `flow
validate` flags one that starts with a real root (`$steps.x.`, say) as a
malformed reference; a flow that ships one anyway resolves it as a literal
string at runtime, which is a silently wrong value
rather than an error. Later segments may be numeric, which means an array
index (`$steps.x.output.rows.0.title`).

**A `foreach` alias shadows `$channel` and `$trigger`**, deliberately, so
`as: channel` or `as: trigger` keeps working. It does not shadow `$inputs` or
`$steps` — those resolve before aliases are consulted.

**Index arrays with dots, never brackets**: `$steps.x.output.ids.0`. Brackets
are rejected as malformed and would be treated as a literal string.

**A reference path is `[A-Za-z_][A-Za-z0-9_.]*` — no spaces.** This matters
more than it sounds; see §5.

### `when:` has four rails, and the seam between two of them bites

Routing is **legacy-first**: a string the legacy parser accepts stays legacy
forever, even if it contains new-syntax tokens.

| Form | Rail | Semantics |
|---|---|---|
| `$ref` | legacy | truth-tested |
| `$ref == value`, `$ref != value` | legacy | **lenient** equality; a skipped step is `None` and compares unequal |
| anything with `&&` `\|\|` `<` `<=` `>` `>=` `!` `(` `)`, or a second comparison | expression | **strict, typed** |
| a plain literal | legacy | truthy as-is |

The expression grammar is `!`, `&&`, `||`, `==`, `!=`, `<`, `<=`, `>`, `>=`,
parentheses; operands are `$ref`s, numbers, `true`/`false`, and quoted strings.
Precedence is parens → `!` → comparisons → `&&` → `||`. Bounds: depth ≤ 8, ≤ 32
conditions, ≤ 8 terms per chain, literals ≤ 1024 chars. No functions, no
arithmetic, no `${}` interpolation.

> **The seam.** A standalone `$a == 1` is *lenient* legacy equality; the same
> comparison inside `$a == 1 && $b != ''` is *strict and typed* on the
> expression rail. Adding a second condition can therefore change how the first
> one compares. And a string that routes to the expression rail but fails to
> parse is an **error** — never a fallback to literal truthiness.

`template check` does not police any of this: mirroring the routing rule
offline means reimplementing the predicate parser, and a near-miss
reimplementation reports valid clauses as broken. It
checks the references inside a `when:` and leaves the grammar to `flow
validate`, which calls the real parser.

**Even so, prefer a query filter to a gate when you are selecting rows.** The
agent-store filter DSL runs in the database rather than after the fact:

```yaml
filter:
  Status: firing                                  # shorthand for $eq
  Last Seen: { $lt: $steps.cutoffs.output.iso }   # $gt $gte $lt $lte
  Nudged At: { $exists: false }                   # $in, $contains too
```

Ordering comparisons on ISO-8601 strings are correct because they are
lexicographic — in a filter *or* on the expression rail. The difference is
where the work happens: a filter selects rows in the database, while a `when:`
gate can only skip a step you already decided to run.

### `foreach`

`foreach:` takes a list, `as:` names the item, `collect:` names the result
list, `max_parallel:` bounds concurrency — omitted, items run one at a time,
and the authoring gates refuse a value above the platform's cap. A step-level `when:` on a `foreach`
step is **re-evaluated per item** in that item's scope, so `when: $row.Status
== 'firing'` filters items rather than skipping the whole step.

### A step is exactly one of five things

`activity:`, `sleep_seconds:`, `await_approval:`, `call_flow:`, or a nested
`steps:` block. Exactly one — the model rejects a step with two, or none.

`call_flow:` runs another flow of the same bundle as a child: `flow:` is a
literal name the publish checks, `inputs:` are resolved like `args`, and
`mode: wait` (the default) returns the child's `outputs:` at
`$steps.<id>.output.outputs.<key>`, while `mode: detach` returns once it has
started. A child runs exactly once, so `on_error.retry` is refused on it —
`call_flow.timeout_seconds` bounds it instead.

Blocks nest three lists deep, counting the flow's own `steps:` as the first —
so a block inside a block is the deepest legal shape and a third level is
rejected. `template check` reports it as `block-too-deep`; without that you
would not hear about it until the install failed.

```yaml
  - id: maybe                     # a BLOCK: `when:` gates the whole group
    when: $steps.check.output.ok
    steps:
      - id: inner
        activity: foundation.channel.post
        args: { ... }
    outputs:
      posted: $steps.inner.output   # the ONLY thing outside can read
```

A block's scoping is the part worth internalizing:

```
outer step  ──▶ sees $steps.maybe.output.posted        ✅ (a declared output)
            ──▶ sees $steps.maybe.output.anything_else ❌
            ──▶ sees $steps.inner.*                    ❌ (private to the block)

inner step  ──▶ sees $inputs, $channel, $trigger, and every
                enclosing step at every level           ✅
```

Inner ids are private for *reads* only: step ids are unique across the whole
flow, blocks included, and reusing one is refused as `duplicate step id`. `outputs:` is
evaluated in the block's inner scope after its steps ran, and is legal only
alongside `steps:`. Omit it and the block publishes nothing — the same as a
skipped step.

`sleep_seconds:` is a durable timer (survives worker restarts, holds no worker
capacity) and cannot be combined with `foreach`. Neither can `await_approval:`,
which is a single blocking per-workflow gate — fanning it out would key every
iteration to the same signal.

### Errors and retries

Retry is flow-owned. **No `on_error` means up to 4 attempts** — any
non-idempotent step must set `retry: 0`. `retry:` is capped at 10, and
`backoff_seconds:` sets the wait before the first retry (it needs a `retry`
of 1 or more). `policy: skip` continues the flow with the step's output null
and the failure under `$steps.<id>.error`; `policy: fail` stops it.
`policy: fallback` (with `fallback: <step id>`) is accepted by the grammar,
but the interpreter runs it as `fail` — nothing is invoked in its place.
`on_error.retry` is refused on a block — retrying a group would repeat its
inner side effects, so put retries on the inner steps — and on `call_flow`.

### Arithmetic is an activity, not syntax

Nothing in a reference or an `args` value computes. You cannot write
`$a + $b`, and you cannot even negate a reference — `-$channel.minutes` is
parsed as a literal string and fails type validation. Arithmetic is
`foundation.math.calculate`: one binary operation per step (`left`,
`operation: add | subtract | multiply | divide`, `right`), chained through
`$steps.<id>.output.value`. Consequences:

- **A counter belongs to the store, not to a read-add-write pair of steps.**
  `merge: increment_on_change` (§5) counts transitions under the row lock;
  two runs doing their own read and `add` can lose an increment.
- **Prefer an activity that names the direction.** A signed value is easy to
  get backwards, which is why `math.offset` takes `direction: subtract`
  rather than a negative duration.

**Time windows have their own activity.**
`foundation.math.offset` shifts a timestamp by a duration and returns
`workflow.now`'s `{unix, unix_str, iso}` shape, so its output drops straight
into a filter:

```yaml
  - id: cutoff
    activity: foundation.math.offset
    args:
      iso: $steps.now.output.iso     # omit to shift from now
      direction: subtract            # durations stay non-negative
      hours: 6

  - id: stale
    activity: foundation.store.list_rows
    args:
      filter:
        Last Seen: { $lt: $steps.cutoff.output.iso }
```

Pass `iso` explicitly when several cutoffs must derive from the same instant.
`basicapp`'s `request_intake` uses the same activity the other way —
`direction: add`, `days: $channel.default_due_days` — to stamp a default due
date with no model involved.

## 5. Table schemas

Declared under `tables:` in the manifest; reconciled additively on every
import.

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

`type` is `string | number | boolean | datetime | json`. `format` validates on
write. `display` is a rendering hint whose *kind* (the part before the first
`:`) is validated against `DISPLAY_KINDS`; its arguments are not — a
misspelled display arg fails silently by simply not rendering.

Governance flags (`pii`, `restricted`, `internal`, `outbound_ref`,
`passthrough`, `masked_read`) are independent booleans. `internal: true` hides
a column from the user-facing UI — right for raw payloads and bookkeeping ids.
`outbound_ref` marks the recipient-facing reference an agent uses in outbound
messages in place of a client's identity. `masked_read` means anything only
alongside `pii: true`.

### Merge policy

A policy acts only when a write **merges into an existing row**: an
`upsert_rows` with `on_conflict: merge`, or a PATCH. `upsert_rows` defaults to
`on_conflict: replace`, which overwrites the whole row and applies no policy.
A table whose schema declares a `merge_key` uses `merge_key.on_conflict`
(default `merge`) and ignores a per-call `merge_on`.

| Policy | Type | On merge |
|---|---|---|
| `replace` (default) | any | the incoming value overwrites |
| `concat` | string only | appends with `merge_separator` (default newline); skips an incoming value equal to the whole stored value |
| `keep` | any | first write wins — a non-blank stored value is never overwritten |
| `increment_on_change` | number only | ignores the incoming value; adds 1 when the `merge_when` column goes `from` → `to` |

`increment_on_change` requires `merge_when: {column, from, to}` naming a
*different* column; `from` and `to` must differ and are compared
case-folded. The accumulating policies act only on a column the write
**carries** — omit `Firing Count` from a write and it does not increment even
when `Status` flips. So write it on every delivery; the value is discarded.

`alerttracker` uses all of this: `First Fired: merge: keep` holds the first
episode's start however often the alert re-fires, and `Firing Count:
increment_on_change` counts `resolved` → `firing` episodes while its ingest
flow sends the same `First Fired` and a constant `1` on every delivery. Write
a "first time we saw this" column unconditionally into a `keep` column rather
than gating a separate step on `created`.

A timestamp history is a `concat` column, so it cannot be `datetime`.

Check what is actually installed with:

```bash
popcorn table schema alerts --channel '#chan'
#   Seen At    string   [concat]
```

### Merge keys

`merge_key.any_of` columns must be **indexed** (`unique: true` satisfies it)
and **string-typed** or computed — the OR-probe only queries the text index,
so schema validation rejects a non-string merge key outright.

### Name columns without spaces if a flow reads them

A column name may contain spaces if flows only ever *write* it (YAML map keys)
or *filter* on it (JSON keys). It must be space-free if any flow
**dereferences** it, because `$row.Last Seen` is not parseable:

```
steps[1](touch).args.text: malformed reference '$row.Last Seen'
```

Renaming later is not free — the installer is additive and never renames, so a
rename *adds* a column and orphans the old one.

**And the store accepts undeclared columns.** Keys are whitespace-trimmed,
and one that matches a declared column case-insensitively is rejected with a
"did you mean" naming it. Anything further off is not: writing
`Post Message Id` when the schema says `PostMessageId` silently succeeds and
produces a column no `$ref` can reach. Renaming a column means renaming every
write site; only reading a row back catches a miss.

## 6. Reading fields off an object input

The DSL cannot reach sub-fields of an `object` input — `$inputs.payload.name`
is statically unreachable, because an input declaration has no way to describe
an object's properties. To read fields off a webhook payload you must first
obtain a **typed** shape, and the only mechanism is an activity that declares
its output schema at the call site.

Two of those exist. **Reach for the deterministic one first.**

### `foundation.fields.extract` — when the fields are simply there

Names fields by path. No model, no prompt, and an absent path is an error
rather than a guess:

```yaml
  - id: fields
    activity: foundation.fields.extract
    args:
      data: $inputs.payload
      mapping:
        alarm: AlarmName
        service: Trigger.Dimensions.1.value    # dots for nesting AND indices
      defaults:
        note: ""                               # only for genuinely optional fields
      output_schema:
        type: object
        required: [alarm, service]
        properties:
          alarm: { type: string }
          service: { type: string }
```

`$steps.fields.output.alarm` then resolves statically, so `flow validate`
checks it. `alerttracker` is a whole bundle built this way — a single
producer, every field read by path, and not one model call in it. Its
`alert_webhook` flow extracts the payload's `alerts` array, extracts each
alert's fields in a `foreach`, and upserts one row per alert.

Three behaviours worth knowing:

- **An unresolvable path fails the step** (`ExtractPathNotFound`), listing
  every bad path at once. That is the point — it is how a flow *requires* a
  field to be present rather than accepting something invented in its place.
  Posting a body with no `alerts` key at `alerttracker`'s webhook fails its
  first extract, and writes nothing:

  ```
  ExtractPathNotFound: fields.extract could not resolve: alerts <- alerts
  ```

  Compare `agent.transform` given the same junk: it fabricates a row. The
  guard is structural here rather than a step you must remember to write.
- **`null` is a value, not an absence.** A stored null passes through; only a
  genuinely missing path errors.
- **The result is validated against `output_schema`** (`ExtractSchemaViolation`),
  so a value contradicting the type you declared fails here rather than in
  whichever later step consumes it.

### `foundation.agent.transform` — when the answer must be derived

Still the right tool when the payload does not *state* what you need — one
flow normalising several unrelated producers, a severity no field carries, a
human-readable title, prose. Judgement, not lookup.

The dividing line is worth applying literally, because it decides your risk:
extraction reads what is there, derivation invents what is not. A CloudWatch
alarm body has no `severity` and no `env` key at all, so those must be derived;
its `AlarmName` and `NewStateValue` are right there and should not be.

The same decision answered both ways, where the input decides it, not taste —
the shipped `alerttracker` on one side, and on the other the several-producer
design the evidence log records:

| | extract (`alerttracker`) | derive (several producers) |
|---|---|---|
| producers | one (Alertmanager) | several, unrelated |
| identity | Alertmanager's `fingerprint`, stated | composed from fields that differ per producer |
| environment | the `cluster` label, stated | absent from a CloudWatch body — derived |
| tool | `fields.extract` | `agent.transform` |
| cost | none | one LLM call per delivery |
| junk input | fails, names every missing path | invents a plausible alert unless a `recognized` guard stops it |

Narrowing a bundle to one producer is therefore not just a scope decision —
it is what makes the deterministic tool available at all.

When you do need it, three rules, each paid for in a live failure:

**1. A required output schema is a formatting contract, not a validation
gate.** Given junk, the model *invents* a plausible object to satisfy
`required`, and `enum` merely constrains which lie it tells. Add an explicit
recognition flag and hard-stop on it:

```yaml
  - id: guard
    activity: foundation.workflow.fail
    when: $steps.normalize.output.recognized == false
    args: { reason: ..., code: UnrecognizedPayload }
```

**2. Every property you dereference must be in `required:`.** A declared-but-
optional property is genuinely optional — the model returned `details` on one
run and omitted it on the next, and a missing key is a hard failure:
`ReferenceError: $steps.normalize.output.details: key not found`.

**3. Keep the prompt and the schema consistent.** Telling the model to blank a
field whose `enum` excludes `""` is a contradiction, and it does not fail
cleanly — the model reasons about the conflict *in its output* and breaks JSON
parsing.

Finally, know which kind of transform you are writing. Mapping fields is
risky; **writing prose is not**. A digest whose wording drifts costs nothing,
because nothing downstream parses it.

## 7. The authoring loop

Three loops now, and picking the right one is most of the speed. The **inner**
loop is offline and runs as often as you like:

```bash
popcorn template check .                             # no channel, no server
popcorn flow activities --name <wire.name>           # what do I pass it?
popcorn flow validate my_flow.yaml                   # per file, fast
```

`flow validate` needs a channel only as an auth/context handle — any channel
you can reach will do; it never writes. Run from an `app checkout` and it
takes the channel from the checkout's baseline, the same way `app publish`
and `app status` do; pass `--channel <id>` anywhere else.

The **middle** loop is the fork loop from §2b, and it is the one to reach for
whenever the app already exists. No deploy, no hand-off, seconds per turn:

```bash
popcorn app publish ./<app> --bump patch -m "..."    # mint the next version
popcorn app status ./<app>                           # has the install landed?
popcorn app lines --channel <id>                     # what lines exist?
popcorn channel-config show --channel <id> --strict  # is the channel wired up?
popcorn flow runs list --channel <id>
```

`app lines` is the fork-line inventory — name, head semver, and when that head
was published — and it is worth a look before forking, because a nameless
`app fork` adopts whatever single line exists and the server refuses outright
once there are two. `--channel` there is the API's authorization handle, not a
filter: the lines listed are the workspace's. Two things it cannot tell you,
both because the API does not carry them: how many channels ride each line,
and how to delete one. Lines accumulate until the backend grows those.

`channel-config show` is worth running the first time a bundle installs: it
diffs every `$channel.*` reference your flows make against what the channel
actually has, and `--strict` exits non-zero on the three findings that make a
run fail — a referenced parameter that is not set, a declared integration that
is not connected, and a connected account whose provider contradicts a
declaration. The two `unused_*` findings are informational; a shared config
legitimately carries keys one flow does not read.

The **outer** loop is only for a NEW app type, and costs a server deploy plus
a publish (§2a), so get the inner one clean first:

```bash
# ... the app type is registered, deployed and published (§2a, internal)

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

Because the outer loop is expensive, a bundle that installs but is wrong costs
a whole deploy cycle to correct — which is the argument for `template check`
and `flow validate` being pedantic, and for exercising boundaries (below) the
first time you get a real channel rather than the third.

That argument is weaker than it was: once the app exists, a wrong bundle costs
a `app publish` rather than a deploy. It is not gone, though — the *first*
version of a new app still has to be right, and a fork publish still moves
every other channel on the line.

A freshly created channel is **not resolvable by `#name` for ~5 minutes**
(negative resolution caching). Use the conversation UUID immediately after
creating it.

`flow run` accepts a flow **name or UUID**, and defaults `conversation_id`
into the inputs from `--channel`:

```bash
popcorn flow run basic_tick --channel <id> --wait
```

Pass `--inputs` for a flow's own arguments; an explicit `conversation_id`
there always wins, so a flow can still target another conversation.

```bash
popcorn flow run seed_test_alert --channel <id> \
  --inputs '{"severity":"critical","fingerprint":"0000000000000002"}' --wait
```

### Checks will not save you

Every defect found while building the example bundle passed `flow validate`
cleanly, because they were runtime semantics rather than bad references: a
merge policy overwriting a first-seen timestamp, an LLM inventing a row, an
optional schema property going missing, a write to an undeclared column.

`template check` was written from that list and now catches the last two —
plus the whole class of cross-file mistakes a per-file validator cannot see:

```bash
popcorn template check .            # errors exit non-zero
popcorn template check . --strict   # warnings do too — this is the CI form
```

It cannot catch the first two. A merge policy is only wrong relative to what
you meant, and no offline tool knows an LLM is about to invent a row.

**So install it and run it.** A seed flow such as `alerttracker`'s
`seed_test_alert` exists purely so a bundle can be exercised without a real
producer — it sends a canned payload through the same ingest flow a real
delivery takes.

And exercise the **boundary**, not the happy path. A sweep that resolves
everything Completes just as cheerfully as a correct one; the only proof a
cutoff works is that a row just inside it moves and a row just outside it does
not.

Watch for these when reading results:

- Many activities have permissive result schemas (`additionalProperties:
  true`). For those, `$steps.x.output.anything` **passes validation** — and at
  runtime a key the response lacks is a hard `ReferenceError: … key not
  found`; only a null partway along the path resolves to null. Verify against
  the real response, not the catalog.
- `start_flow` is asynchronous. A parent that launches a child reports
  Completed immediately; check the **child's** run. When the parent needs the
  result, use a `call_flow:` step with `mode: wait` instead (§4).
- Posting the same webhook body twice does not test your merge logic — the
  *webhook layer* drops a delivery whose body is byte-identical (SHA-256) to
  one seen in the last five minutes, and no flow runs at all. Vary the body
  while keeping the identity fields.
- A field that might be **absent** must never be dereferenced. A missing key
  is a hard `ReferenceError` that fails the run, and `on_error` does not
  rescue it — reference resolution happens before the activity is invoked.
  Guarantee presence upstream: in an `output_schema`'s `required`, or with
  `$exists: true` in the query that produced the rows.

## 8. Gotchas, condensed

1. `$inputs.<object>.field` is statically unreachable — get a typed shape
   first, with `fields.extract` when the fields are there and
   `agent.transform` when the answer must be derived.
2. `workspace_id` is never an input; it rides the auth context.
3. `scalars` are written on install and drift-preserved on update,
   `schedules` reconcile by (flow, slug) and drop the undeclared,
   `default_scalars` write once. Runtime state belongs in none of them.
4. Flow identity is `name:`, not the filename.
5. Flows are read from the bundle root only; anything the format does not
   recognise is left behind by `app publish` and refused by the server.
6. Webhook-triggered flows get `{conversation_id, payload, headers,
   source_hint, delivery_id, webhook_id}`, and only in `trigger_workflow` mode.
7. `<channel-conversation-id>` / `<workspace-id>` are substituted in schedule
   inputs and in `triggers:` inputs.
8. No `on_error.retry` means up to 4 attempts.
9. Table changes are additive — never dropped, never renamed.
10. `app.*` activities are private to shipped apps. Author against
    `tier: foundation|feature`, `status: release`.
11. Scalars are strings on the wire; `channel_parameters` keep their types.
12. **No arithmetic in a reference**, and no negating one. Compute with
    `foundation.math.calculate`, one operation per step; count with
    `merge: increment_on_change`; shift time with `foundation.math.offset`.
13. **An untyped bundle CLEARS `app_type`.**
14. A root-level `.yaml` becomes a flow; a nested one is not a flow at all.
    Fixtures live outside the bundle directory.
15. Permissive output schemas validate any path.
16. Index arrays with dots, never brackets.
17. `when:` has a legacy rail and an expression rail, and adding a second
    condition can change how the first compares (§4). Selecting rows is a
    `filter`'s job, not a gate's.
18. A column name with a space cannot be dereferenced.
19. The store accepts undeclared columns silently — unless one differs from a
    declared column only by case, which is rejected with a "did you mean".
20. Every `output_schema` property you reference must be `required`.
21. A missing key is a hard `ReferenceError`, and `on_error` cannot rescue it —
    resolution precedes invocation. Guarantee presence in the query
    (`$exists: true`) or the schema (`required`).
