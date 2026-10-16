---
id: template-authoring
title: Authoring an app bundle
order: 1
summary: >
  The loop for changing what an app does: check its settings first, fork, check out, edit, `app validate`, `app publish`, then confirm the install landed with `app status` — from the CLI or an assistant over MCP. A new app type is not self-serve. `flow validate` is the authority on a flow; the grammar, manifest keys and table rules are concept pages this guide links.
concepts: [app-bundle, manifest-keys, flow-grammar, publish-and-apply, fork-line]
layer: platform
---

An **app bundle** is a directory of YAML that turns an empty Popcorn channel
into an app: tables to hold state, flows to do work, schedules and webhooks to
invoke them. The CLI's `channel templates` command and `--template` flag name
the same thing.

In the product, an app is a **Routine Template** and a channel is a
**Routine**. This guide uses the CLI's names, because the commands do; the
[product glossary](https://docs.popcorn.ai/concepts/product-glossary.md) maps each one.

> **Which path you are on decides how fast you can iterate.** A *new* app type
> is not self-serve: the set of installable templates is fixed on the server,
> and adding to it takes an internal change plus a deploy that no CLI command
> and no public endpoint can perform. But *editing* an app that already exists
> is a pure CLI loop — `popcorn app fork`, `checkout`, `publish` — with no
> deploy in it. Both paths are §2.

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
Run from a fork checkout of the line's head, logged in, with a channel
(`--channel`, else the checkout's), and with edits since the checkout, it also
sends them to the server, which runs the checks `app publish` runs without
publishing: the manifest's `tables:` and `states:` among them. Otherwise it
runs everything else and prints `server checks: skipped` with the reason.

Its own checks answer a different question, and need no channel:
will install do what you think, and do the files agree with each other?
Everything it reports passes `flow validate` cleanly — a fixture named
`.yaml`, a write to an undeclared column, a schedule naming a flow that is not
there. Run both; neither subsumes the other.

The shipped `alerttracker` app is the running example: one producer
(Alertmanager), a webhook whose flow names every field by path with
`fields.extract` and upserts one row per alert, and no model anywhere in it.
The choice it embodies — *extract* fields the payload states, or *derive* ones
it does not — is
[extracting fields or deriving them](https://docs.popcorn.ai/concepts/extract-or-derive.md), and it is the
single most consequential choice in a webhook-backed template.
[`examples/alerttracker/GOTCHAS.md`](https://github.com/PopcornAiHq/popcorn-cli/blob/main/examples/alerttracker/GOTCHAS.md) is
the raw evidence log from building an LLM-normalised, multi-producer version
of that app, and is behind most of the rules the concept pages state. Read it
as a record: it says so itself, and some of its findings predate the
[merge policies](https://docs.popcorn.ai/concepts/merge-policy.md).

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
├── README.md            human docs, installed as a channel file
└── some_flow.yaml       one flow per file, at the root
```

Only `manifest.yaml` is meaningful on its own, and a publish needs it — with
a `version:` — so everything else is optional. The full tree, the reserved
names and what publish leaves behind are
[app bundles](https://docs.popcorn.ai/concepts/app-bundle.md). Two rules from it that cost the most when
missed:

- **Every other root-level `.yaml` is a flow**, and a nested one is not a flow
  at all. Keep flows at the root, and keep sample payloads and fixtures
  **outside** the bundle directory: anything the format does not name is left
  behind at publish and reported by `app validate` as `path-not-published`.
- **A flow's identity is its `name:`, not its filename**, so renaming `name:`
  is one flow leaving and another arriving; see
  [a flow's identity is its name](https://docs.popcorn.ai/concepts/flow-identity.md).

## 2. How a bundle gets installed

**Two paths, and which one you are on depends on whether the app already
exists.** Creating a new app type costs a server deploy. *Changing* one is a
loop you run yourself, from the CLI or from an assistant over MCP.

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
          (over MCP: create_routine(template=…))
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
popcorn app validate ./<app>
popcorn app publish ./<app> --bump patch -m "what changed" --yes
popcorn app status ./<app>              # has the install landed?
```

`app publish` asks for confirmation before it sends anything, because a
publish changes every channel on the fork line, not only yours. In a terminal
you answer the prompt. In agent mode (`POPCORN_AGENT=1`) or any
non-interactive shell there is no one to answer, so the publish is refused
unless it carries `--yes` (or `POPCORN_ASSUME_YES=1`) — pass it once that
reach is what you mean. The examples here include it because an agent or a
script is usually what runs them.

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

**Check the settings before you fork.** A change to how one channel behaves —
a sending mode, a schedule's cadence, a limit, a prompt or email template — is
often a setting: `list_routine_settings` and `update_routine_setting` over
MCP, or in the CLI `popcorn channel-config params set` for a parameter and
`popcorn table scalar set` for a switch. A setting
reaches that channel alone, can be set back, and survives app updates. A fork
is permanent and reaches every channel on its line, so fork only for what a
setting cannot express: a table, a flow, a state machine.

Publishing needs a fork: a publish lands on a fork line **this
workspace owns**, so publishing from a channel still bound to the shared
product version is refused. `app publish` also starts the install that moves
your channel onto the new version, and that install converges on its own —
`app status` confirms it rather than causing it.

The bump is not optional either, and inside a checkout `app validate` is
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
`app validate` and `app publish` have run. Neither publishes. `CLAUDE.md` is
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
popcorn app status --channel '#chan' --json | jq -r '.data.install.state'
```

`install.state` is `current` (the channel runs its fork line's head) or says
why it does not: `installing`, `retrying`, `locked`, `failed`, `skipped` or
`behind`. Poll that field rather than grepping a semver out of `app list`
output. A failed install comes with its error, an `error_code` and its attempt
count — only `invalid_manifest`, `invalid_schedule` and `bundle_rejected` mean
the head needs fixing, and `internal` means the platform failed, so no edit or
publish helps (report it with the workflow id) — a skipped one with its reason, and the text output carries a `Next:` line saying what moves
the channel on — for a failed, skipped or behind fork channel, `app apply
--channel <channel>`. The older `install_state` field is still there, as
`current` or `pending` for every other state.

`--fork` takes an optional line name (`--fork=experiment`); bare, it names the
line it is about to use and asks, because a workspace's single existing line
can be far behind product. `-y` answers that. `popcorn app fork` on its own is still there and does the
same thing without the checkout.

**This is also how you read a real bundle.** `app checkout` returns the whole
tree — manifest, every flow, `AGENT.md`, `strings.yaml` — for the head of the
fork line the channel runs (normally the very version it is bound to; the two
differ only while an install has not landed), so it is the one source that
cannot be stale. `app checkout --version <id>` reads an earlier version of the
same line instead, read-only — the way to recover the tree from before a bad
publish (see `bundle-version`).
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
`popcorn app lines` is how you see what has accumulated.

Three things about this loop that are easy to get wrong:

- **`version:` in `manifest.yaml` must advance every publish.** Bundle versions
  only ever move forward; the CLI refuses a reused or lower number locally
  rather than letting the registry 409 at you.
- **A publish is not scoped to the channel you tested on.** Every other channel
  on the same fork line catches up on its own nightly auto-update tick.
- **One fork line per (workspace, app).** There is no parallel-experiment path
  without naming a second line (`app fork --name`).

`popcorn app list` shows the product line and any fork line this workspace
owns; add `--channel '#chan'` to see what that channel currently runs.

### The same loop from an assistant

An assistant connected to Popcorn over MCP runs this loop without a working
copy. The tools take a Routine where the CLI takes a channel, and each write
is a dry run until it is called again with `confirm=true`:

| CLI | MCP |
|---|---|
| `app checkout` | `list_app_files`, then `read_app_file` per file |
| `app fork` | `fork_app` |
| `app validate`, then `app publish` | `publish_app`: its dry run reports every check publish would fail, each file's diff and the reach; the confirm publishes by `plan_id` |
| `app status` | `get_routine`, whose `Install:` field says whether the install landed |
| `app apply` | `install_app` |

`publish_app` takes changes, not a tree: each one creates, deletes, renames or
edits one file with text ops, and an edit carries the `sha256` it was read at.
A file the assistant generated rather than typed goes up through
`create_app_upload`. The
[MCP reference](https://docs.popcorn.ai/reference/mcp.md) has the arguments.

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

## 3. What the manifest declares

Every key is optional, and each has its own install semantics:
[manifest keys and what install does to them](https://docs.popcorn.ai/concepts/manifest-keys.md) is the
table. The keys with pages of their own:

| Key | Page |
|---|---|
| `tables` | [table columns](https://docs.popcorn.ai/concepts/table-columns.md) and [column merge policy](https://docs.popcorn.ai/concepts/merge-policy.md); adding one end to end is [adding a table](https://docs.popcorn.ai/guides/adding-a-table.md) |
| `scalars`, `default_scalars` | [the three scalar tiers](https://docs.popcorn.ai/concepts/scalar-tiers.md) |
| `schedules` | [schedules in a manifest](https://docs.popcorn.ai/concepts/schedules.md) |
| `states` | [state machines in a bundle](https://docs.popcorn.ai/concepts/state-machine.md); writing one is [authoring a states tier](https://docs.popcorn.ai/guides/states-authoring.md) |

Three traps are worth carrying into every edit:

- **An absent key leaves the channel alone; an empty one means "replace with
  nothing."** `schedules: []` deletes every manifest-managed schedule.
  Omitting `schedules:` does not.
- **An unknown top-level key is silently ignored.** A typo such as
  `schedule:` installs nothing and reports nothing.
- **An untyped bundle CLEARS the channel's `app_type`** and `channel_agent`.
  A fork publish does not refuse one: it reaches every channel on the line and
  clears both on each. `app validate` warns (`clears-app-type`); treat that
  warning as an error on a fork.

## 4. Writing flows

A flow's grammar is four concept pages, each answering one question:

- [The shape of a flow](https://docs.popcorn.ai/concepts/flow-grammar.md) — the file's keys, the five kinds
  of step, blocks, `call_flow` and `foreach`.
- [References in a flow](https://docs.popcorn.ai/concepts/references.md) — the `$` roots, the syntax,
  and why nothing in a reference computes.
- [Conditions in a flow](https://docs.popcorn.ai/concepts/conditions.md) — `when:`'s two rails, and
  filtering rows instead of gating steps.
- [Step errors and retries](https://docs.popcorn.ai/concepts/on-error.md) — `on_error`, the default of
  four attempts, and what no policy catches.

Reading fields off a webhook payload is
[extracting fields or deriving them](https://docs.popcorn.ai/concepts/extract-or-derive.md).

## 5. The authoring loop

Three loops, and picking the right one is most of the speed. The **inner**
loop publishes nothing and runs as often as you like:

```bash
popcorn app validate .                               # server checks: logged in, in a fork checkout
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
popcorn app publish ./<app> --bump patch -m "..." --yes   # mint the next version
popcorn app status ./<app>                           # has the install landed?
popcorn app lines                                    # what lines exist?
popcorn channel-config show --channel <id> --strict  # is the channel wired up?
popcorn flow runs list --channel <id> --flow <name>   # filtered on the server
```

`app lines` is the fork-line inventory — name, head semver, and when that head
was published — and it is worth a look before forking, because a nameless
`app fork` adopts whatever single line exists and the server refuses outright
once there are two. The lines listed are the workspace's, and it needs no
channel. Two things it cannot tell you, both because the API does not carry
them: how many channels ride each line, and how to delete one. Neither
exists, so lines accumulate.

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
a whole deploy cycle to correct — which is the argument for `app validate`
and `flow validate` being pedantic, and for exercising boundaries (below) the
first time you get a real channel rather than the third.

Once the app exists, a wrong bundle costs an `app publish` rather than a
deploy. The *first* version of a new app still has to be right, though, and a
fork publish still moves every other channel on the line.

A `#name` that matches more than one channel — a case variant, or a channel
shared in from another workspace — is refused with each candidate's id. Pass
the id in its place; `--workspace` does not narrow the lookup.

`flow run` accepts a flow **name or UUID**, and defaults `conversation_id`
into the inputs from `--channel`:

```bash
popcorn flow run basic_tick --channel <id> --wait
```

Pass `--inputs` for a flow's own arguments; an explicit `conversation_id`
there always wins, so a flow can still target another channel.

```bash
popcorn flow run seed_test_alert --channel <id> \
  --inputs '{"severity":"critical","fingerprint":"0000000000000002"}' --wait
```

Every run carries `outcome`: `succeeded`, `failed` or `still_running`. Poll
that field, not `status` — `--wait` does. To change one channel parameter
without rewriting the others, use `popcorn channel-config params set` and
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
  [the shape of a flow](https://docs.popcorn.ai/concepts/flow-grammar.md)).
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
   [scalar tiers](https://docs.popcorn.ai/concepts/scalar-tiers.md).
4. Every schedule's `flow:` names a flow the bundle has —
   [schedules](https://docs.popcorn.ai/concepts/schedules.md).
5. Table changes only add: no column is dropped or renamed, and a column a
   flow dereferences has no spaces — [table columns](https://docs.popcorn.ai/concepts/table-columns.md).
6. A step with a side effect sets `retry: 0` —
   [step errors](https://docs.popcorn.ai/concepts/on-error.md).
7. Every key a reference reads is guaranteed upstream, by `required` in an
   `output_schema` or `$exists: true` in a filter —
   [references](https://docs.popcorn.ai/concepts/references.md).
8. A second condition in a `when:` did not change how the first compares —
   [conditions](https://docs.popcorn.ai/concepts/conditions.md).
9. Fields the payload states are extracted, not derived —
   [extract or derive](https://docs.popcorn.ai/concepts/extract-or-derive.md).
10. A markdown post sets `format: markdown`, on every edit too —
    [the shape of a flow](https://docs.popcorn.ai/concepts/flow-grammar.md).
