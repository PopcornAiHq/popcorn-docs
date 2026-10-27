---
id: template-authoring
title: Changing a Routine Template
order: 1
summary: >
  The loop for changing what a Routine Template does: check its settings,
  read its files, copy it, edit, publish a version, confirm the install
  landed — over MCP with `copy_routine_template` and
  `create_routine_version`, or with the CLI's `app checkout`, `validate`,
  `publish` (an agent runs it with `--yes`) and `status`. A new template is
  not self-serve. `flow validate` is the authority on a flow.
concepts: [app-bundle, manifest-keys, flow-grammar, versions, copying-a-template]
part: build
---

A **Routine Template** is made of an **app bundle**: a directory of YAML
that turns an empty Routine into one that runs the template — tables to hold
state, flows to do work, schedules and webhooks to invoke them. The CLI and
the API call a Routine a *channel* and its template an *app*, so the commands
below keep those names; the CLI's `channel templates` command and
`--template` flag name the template. The
[glossary](https://docs.popcorn.ai/glossary/glossary.md) has the product's words.

> **Which path you are on decides how fast you can iterate.** A *new*
> template (a new `app_type`) is not self-serve: the set of installable
> templates is fixed on the server, and adding to it takes an internal change
> plus a deploy that no CLI command and no public endpoint can perform. But
> *changing* a template that already exists is a loop you run yourself — over
> MCP with `copy_routine_template` and `create_routine_version`, or from the
> CLI with `popcorn app fork`, `checkout` and `publish` — with no deploy in
> it. Both paths are §2.

This guide is the order to do things in. What a bundle may contain is in the
concept pages it links (§1, §3, §4), and the activities a flow can call come
from the server, because they would rot here:

```bash
popcorn flow activities --summary              # what can I call?
popcorn flow activities --name <wire.name>     # what do I pass it?
popcorn flow activities --json                 # full arg + result schemas
popcorn flow validate my_flow.yaml             # is this reference real?
popcorn app validate ./mytemplate              # does the bundle hold together?
```

`flow validate` asks the server and is the authority on a flow. When this
guide or a concept page and the validator disagree, the validator is right and
the page has a bug. `app validate` works from a copy of the server's rules
that ships with the CLI, so an older CLI can reject a construct the platform
accepts. When the two disagree, upgrade the CLI before changing the bundle.
Run from a checkout of the head of the workspace's own copy of the template
(the CLI calls the copy a *fork line*, and this a *fork checkout*), logged in, with a Routine (`--channel`, else the checkout's), and with edits
since the checkout, it also
sends them to the server, which runs the checks `app publish` runs without
publishing: the manifest's `tables:` and `states:` among them. Otherwise it
runs everything else and prints `server checks: skipped` with the reason.

Its own checks answer a different question, and need no Routine:
will install do what you think, and do the files agree with each other?
Everything it reports passes `flow validate` cleanly — a fixture named
`.yaml`, a write to an undeclared column, a schedule naming a flow that is not
there. Run both; neither subsumes the other.

The shipped `alerttracker` template is the running example: one producer
(Alertmanager), a webhook whose flow names every field by path with
`fields.extract` and upserts one row per alert, and no model anywhere in it.
The choice it embodies — *extract* fields the payload states, or *derive* ones
it does not — is
[extracting fields or deriving them](https://docs.popcorn.ai/build/concepts/extract-or-derive.md), and it is the
single most consequential choice in a webhook-backed template.
[`examples/alerttracker/GOTCHAS.md`](https://github.com/PopcornAiHq/popcorn-cli/blob/main/examples/alerttracker/GOTCHAS.md) is
the raw evidence log from building an LLM-normalised, multi-producer version
of that template, and is behind most of the rules the concept pages state. Read it
as a record: it says so itself, and some of its findings predate the
[merge policies](https://docs.popcorn.ai/build/concepts/merge-policy.md).

> **Do not copy a bundle out of a repo.** The cut-down bundles under the CLI
> repo's `tests/fixtures/bundles/` exist to exercise `app validate`; none
> declares a `version:`, so none can publish, and they do not match what the
> platform ships. **Get bundle source from the server** — see §2b, where
> `app checkout` hands you the deployed version of a real one.

---

## 1. What a bundle is

```
mytemplate/
├── manifest.yaml        tables, schedules, webhooks, config, scalars
├── AGENT.md             notes the channel agent reads on demand
├── README.md            human docs, installed as a file in the Routine
├── recipe.yaml          the state graph, only when the manifest declares recipe:
└── some_flow.yaml       one flow per file, at the root
```

Only `manifest.yaml` is meaningful on its own, and a publish needs it — with
a `version:` — so everything else is optional. The full tree, the reserved
names and what publish leaves behind are
[app bundles](https://docs.popcorn.ai/build/concepts/app-bundle.md). Two rules from it that cost the most when
missed:

- **Every other root-level `.yaml` is a flow**, and a nested one is not a flow
  at all. Keep flows at the root, and keep sample payloads and fixtures
  **outside** the bundle directory: anything the format does not name is left
  behind at publish and reported by `app validate` as `path-not-published`.
- **A flow's identity is its `name:`, not its filename**, so renaming `name:`
  is one flow leaving and another arriving; see
  [a flow's identity is its name](https://docs.popcorn.ai/build/concepts/flow-grammar.md#a-flow-s-identity-is-its-name).

## 2. How a bundle gets installed

**Two paths, and which one you are on depends on whether the template
already exists.** Creating a new one costs a server deploy. *Changing* one is
a loop you run yourself, from an assistant over MCP or from the CLI.

### 2a. A new Routine Template — not self-serve

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
though you do not run either step. A bundle whose flows call a new activity
must not become installable before the workers that can run it exist: a Routine
created from it inside that window installs cleanly and then fails on the first
run, with nothing to point at. Nothing enforces the ordering; it is release
discipline.

No public endpoint takes a *new* template off your disk. `channel create --template`
only resolves names the server already carries, so a genuinely new `app_type`
has to go through that internal path — and `popcorn channel templates` is how
you check whether it has landed.

### 2b. Changing a Routine Template that exists

A Routine already running a template can be changed with no deploy and no
hand-off to anyone. An assistant connected to Popcorn over MCP runs the loop
without a working copy; the CLI runs it from a checkout. Each step names the
MCP tool first and the CLI command beside it:

1. **Check the settings.** `list_routine_settings`, then
   `update_routine_setting`. CLI: `popcorn channel-config params set` for a
   parameter, `popcorn table scalar set` for a switch. Often this is the
   whole change; see below.
2. **Read the files.** `list_routine_files`, then `read_routine_file` per
   file. CLI: `popcorn app checkout --channel '#chan'`.
3. **Copy the template.** `copy_routine_template`, with a name for the copy.
   CLI: `popcorn app fork`, then `popcorn app checkout --channel '#chan'`
   again, because `app publish` refuses a checkout of Popcorn's own version;
   or `app checkout --fork` to copy and check out in one command. Each
   version published to the copy is what the CLI calls a *bundle version*.
4. **Edit, and check.** `create_routine_version` without `confirm`: its dry
   run reports every check publish would fail, each file's diff and the
   reach, and changes nothing. CLI: edit the checkout, then
   `popcorn app validate ./<app>`.
5. **Publish a version.** `create_routine_version` again, with
   `confirm=true` and the `plan_id` a dry run on the copy gave. CLI:
   `popcorn app publish ./<app> --bump patch -m "what changed" --yes`.
6. **Confirm the install landed.** `get_routine`, whose `Install:` field says
   whether it has; `wait_seconds` waits up to 20 seconds for an install in
   progress to land. CLI: `popcorn app status`.
7. **Only if it did not land, retry it.** `install_routine`. CLI:
   `popcorn app apply`.

Over MCP, the copy can wait until a dry run passes: a Routine still on
Popcorn's own template can dry-run a change, and needs its own copy only to
publish it, so the step that cannot be undone comes after the check. That
dry run holds no plan and shows no reach. After `copy_routine_template`, call
`create_routine_version` again with the same changes and the new
`base_version` that `list_routine_files` then shows, and confirm with the
`plan_id` from that second dry run.

Copying a template, a new version, an install onto another copy and a
change to a setting are each a dry run until called again with
`confirm=true`. An `install_routine` with no `copy` on a Routine behind its
copy, and `create_routine` with no template, start at once; and
`change_routine` with a `request` starts drafting at once, though it
installs nothing until confirmed. `create_routine_version` takes changes, not a tree: each one
creates, deletes, renames or edits one file with text ops, and an edit
carries the `sha256` it was read at. A file the assistant generated rather
than typed goes up through `create_routine_file_upload`. The
[MCP reference](https://docs.popcorn.ai/reference/mcp.md) has the arguments.

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
publish changes every Routine on the copy, not only yours. In a terminal
you answer the prompt. In agent mode (`POPCORN_AGENT=1`) or any
non-interactive shell there is no one to answer, so the publish is refused
unless it carries `--yes` (or `POPCORN_ASSUME_YES=1`) — pass it once that
reach is what you mean. The examples here include it because an agent or a
script is usually what runs them.

`--bump patch|minor|major` writes `version:` in `manifest.yaml` for you, off
the copy's head, and only once the publish has been accepted — so a
publish that fails leaves the working copy untouched and re-running the same
command is the retry. Editing `version:` by hand still works; `--bump` is
refused when the manifest already advances past the head, because counting
from the head would overwrite that number and counting from the manifest
would skip the versions in between. Reach for the flag or the hand edit, not
both in one publish.

`-m` records what changed on the version, exactly like `git commit -m`
(`--changelog` is the deprecated spelling and still works). **Note what it
does not do:** `manifest.yaml`'s own `changelog:` key is not read by a publish
to a copy — the server records the request's message and nothing else — so a
manifest that declares one while you pass no `-m` records nothing at all, and
publish says so. Nor is there any command that reads a published version's
message back: no endpoint serves it. The line `app publish` prints is the one
chance to see what landed.

**Check the settings before you copy.** A change to how one Routine behaves —
a sending mode, a schedule's cadence, a limit, a prompt or email template — is
often one of its Routine Settings (step 1). A setting
reaches that Routine alone, can be set back, and survives the template's
updates. A copy is permanent and reaches every Routine on it, so copy only for
what a setting cannot express: a table, a flow, a state machine.

Publishing needs a copy: a publish lands on a copy **this
workspace owns**, so publishing from a Routine still bound to the shared
product version (Popcorn's own template, which the CLI prints as a
*PRODUCT* version) is refused. `app publish` also starts the install that moves
your Routine onto the new version, and that install converges on its own —
`app status` confirms it rather than causing it.

The bump is not optional either, and inside a checkout `app validate` is
where you find that out. A published version is immutable, so `version:` must
strictly advance past the one the checkout came from; leaving it alone gets you
a `version-not-advanced` error offline instead of a server refusal after the
upload. Leaving `changelog:` exactly as the checkout wrote it while `version:`
advances is a warning (`changelog-not-updated`) rather than an error, because
the checkout arrives carrying the *previous* version's note — so keeping it is
the default outcome, not an unlikely one. The warning says which job the field is doing for the kind
of checkout you are in: in a fork checkout it is documentation that ships with the bundle
and `-m` is what records a note on the version, matching what `app publish`
tells you rather than contradicting it. Both checks read the baseline
`app checkout` wrote and are skipped entirely on a directory that is not a
checkout.

A checkout writes two files that are not bundle content: `.popcorn-app.json`,
the baseline above, and `CLAUDE.md`, which tells a coding agent opening a file
in the directory that this is a bundle and that an edit is not a release until
`app validate` and `app publish` have run. Neither publishes. `CLAUDE.md` is
yours once written — a re-checkout leaves your edits to it alone unless you
pass `--force` — and it is not `AGENT.md`, which *is* bundle content and ships
to every Routine that installs the template.

`app apply` is **not** a step in this loop. It is the retry for an install that
did not land: the Routine had its template's updates locked, another install
held it, or it failed. Run it when `app status` says the Routine is still
behind its copy's head, not by habit.

**From outside a checkout**, `app status --channel <channel>` answers the same
question against server state alone — no working copy needed:

```bash
popcorn app status --channel '#chan'
popcorn app status --channel '#chan' --json | jq -r '.data.install.state'
```

`install.state` is `current` (the Routine runs its copy's head) or says
why it does not: `installing`, `retrying`, `locked`, `failed`, `skipped` or
`behind`. Poll that field rather than grepping a semver out of `app list`
output. A failed install comes with its error, an `error_code` and its attempt
count — only `invalid_manifest`, `invalid_schedule` and `bundle_rejected` mean
the head needs fixing, and `internal` means the platform failed, so no edit or
publish helps (report it with the workflow id) — a skipped one with its reason, and the text output carries a `Next:` line saying what moves
the Routine on — for a failed, skipped or behind Routine on a copy, `app apply
--channel <channel>`. The older `install_state` field is still there, as
`current` or `pending` for every other state.

`--fork` takes an optional name for the copy (`--fork=experiment`); bare, it
names the copy it is about to use and asks, because a workspace's single
existing copy can be far behind Popcorn's own template. `-y` answers that. `popcorn app fork` on its own is still there and does the
same thing without the checkout.

**This is also how you read a real bundle.** `app checkout` returns the whole
tree — manifest, every flow, `AGENT.md`, `strings.yaml` — for the head of the
copy the Routine runs (normally the very version it is bound to; the two
differ only while an install has not landed), so it is the one source that
cannot be stale. `app checkout --version <id>` reads an earlier version of the
same line instead, read-only — the way to recover the tree from before a bad
publish (see `versions`).
When you want to study how a shipped template does something, spend a scratch
Routine on it rather than looking for a copy in a repo:

```bash
popcorn channel create '#scratch' --template alerttracker
popcorn app checkout --channel '#scratch'          # read it as it ships
popcorn app checkout --channel '#scratch' --fork   # ... or to edit it
```

Reading needs no copy — a checkout taken without one records `"kind": "product"` and
publishing from it is refused, which is the point. Copy when you intend to
edit, and note what that costs: a copy is permanent and cannot be
deleted, so make one in a workspace you do not mind accumulating one in.
`popcorn app lines` is how you see what has accumulated.

Three things about this loop that are easy to get wrong:

- **`version:` in `manifest.yaml` must advance every publish.** Versions
  only ever move forward; the CLI refuses a reused or lower number locally
  rather than letting the registry 409 at you.
- **A publish is not scoped to the Routine you tested on.** Every other Routine
  on the same copy catches up on its own nightly auto-update tick.
- **One copy per (workspace, template).** There is no parallel-experiment path
  without naming a second copy (`app fork --name`).

`popcorn app list` shows Popcorn's own line and any copy this workspace
owns; add `--channel '#chan'` to see what that Routine currently runs.

### The template list is filtered by your release track

`popcorn app list` and `popcorn channel templates` show what **your workspace's
release track** can see — alpha, beta or stable, per-workspace and defaulting
to stable. A template released only to alpha is invisible and uninstallable for a
workspace enrolled on stable.

**The API says nothing about why**, deliberately: enrollment is internal, and a
test enforces that it does not leak. So `channel create --template X` returns a
neutral 400 for a template your track cannot see, indistinguishable from a typo.
The CLI cannot diagnose this and does not try. If a template you know shipped is
missing from the list, that is the first thing to suspect — ask rather than
debug.

## 3. What the manifest declares

Every key is optional, and each has its own install semantics:
[manifest keys and what install does to them](https://docs.popcorn.ai/build/concepts/manifest-keys.md) is the
table. The keys with pages of their own:

| Key | Page |
|---|---|
| `tables` | [table columns](https://docs.popcorn.ai/build/concepts/table-columns.md) and [column merge policy](https://docs.popcorn.ai/build/concepts/merge-policy.md); adding one end to end is [adding a table](https://docs.popcorn.ai/build/guides/adding-a-table.md) |
| `scalars`, `default_scalars` | [scalar tiers and Routine Settings](https://docs.popcorn.ai/build/concepts/scalar-tiers.md) |
| `schedules` | [schedules in a manifest](https://docs.popcorn.ai/build/concepts/schedules.md) |
| `states` | [state machines in a bundle](https://docs.popcorn.ai/build/concepts/state-machine.md); writing one is [authoring a states tier](https://docs.popcorn.ai/build/guides/states-authoring.md) |
| `recipe` | the same graph as a root `recipe.yaml` each Routine can replace — the recipe section of [state machines in a bundle](https://docs.popcorn.ai/build/concepts/state-machine.md); it is written like a `states:` section |

Three traps are worth carrying into every edit:

- **An absent key leaves the Routine alone; an empty one means "replace with
  nothing."** `schedules: []` deletes every manifest-managed schedule.
  Omitting `schedules:` does not.
- **An unknown top-level key is silently ignored.** A typo such as
  `schedule:` installs nothing and reports nothing.
- **An untyped bundle CLEARS the Routine's `app_type`** and `channel_agent`.
  A publish to a copy does not refuse one: it reaches every Routine on the
  copy and clears both on each. `app validate` warns (`clears-app-type`);
  treat that warning as an error on a copy.

## 4. Writing flows

A flow's grammar is four concept pages, each answering one question:

- [The shape of a flow](https://docs.popcorn.ai/build/concepts/flow-grammar.md) — the file's keys, the five kinds
  of step, blocks, `call_flow` and `foreach`.
- [References in a flow](https://docs.popcorn.ai/build/concepts/references.md) — the `$` roots, the syntax,
  and why nothing in a reference computes.
- [Conditions in a flow](https://docs.popcorn.ai/build/concepts/conditions.md) — `when:`'s two rails, and
  filtering rows instead of gating steps.
- [Step errors and retries](https://docs.popcorn.ai/build/concepts/on-error.md) — `on_error`, the default of
  four attempts, and what no policy catches.

Reading fields off a webhook payload is
[extracting fields or deriving them](https://docs.popcorn.ai/build/concepts/extract-or-derive.md).

## 5. The authoring loop

Three loops, and picking the right one is most of the speed. The **inner**
loop publishes nothing and runs as often as you like:

```bash
popcorn app validate .                               # server checks: logged in, in a checkout of a copy
popcorn flow activities --name <wire.name>           # what do I pass it?
popcorn flow validate my_flow.yaml                   # per file, fast
```

`flow validate` needs a Routine only as an auth/context handle — any Routine
you can reach will do; it never writes. Run from an `app checkout` and it
takes the Routine from the checkout's baseline, the same way `app publish`
and `app status` do; pass `--channel <id>` anywhere else.

The **middle** loop is the loop on a copy from §2b, and it is the one to reach
for whenever the template already exists. No deploy, no hand-off, seconds per turn:

```bash
popcorn app publish ./<app> --bump patch -m "..." --yes   # mint the next version
popcorn app status ./<app>                           # has the install landed?
popcorn app lines                                    # what copies exist?
popcorn channel-config show --channel <id> --strict  # is the Routine wired up?
popcorn flow runs list --channel <id> --flow <name>   # filtered on the server
```

`app lines` is the inventory of copies — name, head semver, and when that
head was published — and it is worth a look before copying, because a
nameless `app fork` adopts whatever single copy exists and the server refuses
outright once there are two. The copies listed are the workspace's, and it
needs no Routine. Two things it cannot tell you, both because the API does
not carry them: how many Routines ride each copy, and how to delete one.
Neither exists, so copies accumulate.

`channel-config show` is worth running the first time a bundle installs: it
diffs every `$channel.*` reference your flows make against what the Routine
actually has — its parameters (Routine Settings) and its integrations
(Connections) — and `--strict` exits non-zero on the three findings that make a
run fail — a referenced parameter that is not set, a declared integration that
is not connected, and a connected account whose provider contradicts a
declaration. The two `unused_*` findings are informational; Routine Settings and
Connections every flow shares legitimately carry keys one flow does not read.

The **outer** loop is only for a NEW Routine Template, and costs a server deploy plus
a publish (§2a), so get the inner one clean first:

```bash
# ... the app_type is registered, deployed and published (§2a, internal)

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
a whole deploy cycle to correct — which is the argument for `app validate`
and `flow validate` being pedantic, and for exercising boundaries (below) the
first time you get a real Routine rather than the third.

Once the template exists, a wrong bundle costs an `app publish` rather than a
deploy. The *first* version of a new template still has to be right, though,
and a publish to a copy still moves every other Routine on it.

A `#name` that matches more than one Routine — a case variant, or a Routine
shared in from another workspace — is refused with each candidate's id. Pass
the id in its place; `--workspace` does not narrow the lookup.

`flow run` accepts a flow **name or UUID**, and defaults `conversation_id`
into the inputs from `--channel`:

```bash
popcorn flow run basic_tick --channel <id> --wait
```

Pass `--inputs` for a flow's own arguments; an explicit `conversation_id`
there always wins, so a flow can still target another Routine.

```bash
popcorn flow run seed_test_alert --channel <id> \
  --inputs '{"severity":"critical","fingerprint":"0000000000000002"}' --wait
```

Every run carries `outcome`: `succeeded`, `failed` or `still_running`. Poll
that field, not `status` — `--wait` does. To change one parameter in a Routine's
Settings without rewriting the others, use `popcorn channel-config params set` and
`params unset`.

### Checks will not save you

Every defect found while building the example bundle passed `flow validate`
cleanly, because they were runtime semantics rather than bad references: a
merge policy overwriting a first-seen timestamp, an LLM inventing a row, an
optional schema property going missing, a write to an undeclared column.

`app validate` was written from that list and now catches the last two —
plus the whole class of cross-file mistakes a per-file validator cannot see:

```bash
popcorn app validate .            # errors exit non-zero
popcorn app validate . --strict   # warnings do too — this is the CI form
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
  result, use a `call_flow:` step with `mode: wait` instead (see
  [the shape of a flow](https://docs.popcorn.ai/build/concepts/flow-grammar.md)).
- Posting the same webhook body twice does not test your merge logic — the
  *webhook layer* drops a delivery whose body is byte-identical (SHA-256) to
  one seen in the last five minutes, and no flow runs at all. Vary the body
  while keeping the identity fields.
- A field that might be **absent** must never be dereferenced. A missing key
  is a hard `ReferenceError` that fails the run, and `on_error` does not
  rescue it — reference resolution happens before the activity is invoked.
  Guarantee presence upstream: in an `output_schema`'s `required`, or with
  `$exists: true` in the query that produced the rows.


## 6. Before you publish

Each line is a rule a concept page explains; every one of them has cost a
publish.

1. `version:` advances every publish, and `--bump` is the way to do it (§2b).
2. The manifest keeps `app_type:` and `channel_agent:` (§3).
3. No flow-written value is declared under `scalars:` —
   [scalar tiers and Routine Settings](https://docs.popcorn.ai/build/concepts/scalar-tiers.md).
4. Every schedule's `flow:` names a flow the bundle has —
   [schedules](https://docs.popcorn.ai/build/concepts/schedules.md).
5. Table changes only add: no column is dropped or renamed, and a column a
   flow dereferences has no spaces — [table columns](https://docs.popcorn.ai/build/concepts/table-columns.md).
6. A step with a side effect sets `retry: 0` —
   [step errors](https://docs.popcorn.ai/build/concepts/on-error.md).
7. Every key a reference reads is guaranteed upstream, by `required` in an
   `output_schema` or `$exists: true` in a filter —
   [references](https://docs.popcorn.ai/build/concepts/references.md).
8. A second condition in a `when:` did not change how the first compares —
   [conditions](https://docs.popcorn.ai/build/concepts/conditions.md).
9. Fields the payload states are extracted, not derived —
   [extract or derive](https://docs.popcorn.ai/build/concepts/extract-or-derive.md).
10. A markdown post sets `format: markdown`, on every edit too —
    [the shape of a flow](https://docs.popcorn.ai/build/concepts/flow-grammar.md).
