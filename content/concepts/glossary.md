---
id: glossary
title: Glossary
order: 11
layout: lookup
summary: >
  The platform's nouns, each with its current synonyms and the collisions
  worth knowing. An app is the thing, such as a claim coordinator; its app
  bundle is its files. "Channel template" is the older name for both, still in
  `template check` and `channel create --template`. A channel is what an app
  installs into, identified by its UUID because a name can change.
concepts: [app-bundle, bundle-version, fork-line, channel-binding, publish-and-apply, flow-identity, manifest-keys, scalar-tiers, merge-policy, state-machine]
applies_to: [cli, mcp, human]
---

One vocabulary for authors, agents and tools. Each entry gives the preferred
term first, then the other names it goes by today, then what it is most often
confused with, then the page that explains it. Where the CLI or the API still
uses an older name, the entry says so; the older name keeps working.

Two words need a qualifier every time they are used: **trigger** and
**integration**. Each has several meanings, listed under its entry. **Version**
is close behind: see *bundle version*.

## Apps and bundles

- **app** — One application, named by a slug such as `claimcoordinator`, and
  everything published under that name. The manifest's `app_type:` and the
  `app` field on app responses both carry the slug. The set of apps is fixed
  on the server: editing an existing app is self-serve, and adding a new one
  is not. *Not to be confused with* a channel: one app runs in many channels.
  See [App bundles](https://docs.popcorn.ai/concepts/app-bundle.md).
- **app bundle** (short: **bundle**) — The files of one version of an app:
  `manifest.yaml`, the flow YAML files at the root, `AGENT.md`,
  `strings.yaml`, and the `prompts/`, `templates/`, `code/` and `agents/`
  directories. *Not to be confused with* the bundle's own `templates/`
  directory, which holds email text. See
  [App bundles](https://docs.popcorn.ai/concepts/app-bundle.md).
- **channel template** — The older name for an app and its bundle. It
  survives in `popcorn template check`, `popcorn channel templates` and
  `popcorn channel create --template <app>`, which all mean the app. Prefer
  *app* or *app bundle* in prose. See
  [Authoring an app bundle](https://docs.popcorn.ai/guides/template-authoring.md).
- **manifest** — `manifest.yaml` at the bundle root; `config.yaml` is still
  read under its legacy name. Each key has its own install semantics, an
  absent key is not the same as an empty one, and an unknown key is ignored.
  See [Manifest keys](https://docs.popcorn.ai/concepts/manifest-keys.md).
- **bundle version** — One immutable published version of a bundle,
  identified two ways: `version_id`, an integer the platform assigns (what
  `app checkout --version` takes), and `semver`, the manifest's `version:`,
  unique on its line. Name both when you name one. *Not to be confused with*
  a flow's own `version:`, an integer inside the flow file that a `call_flow`
  step reports as `flow_version`; `flow_version` on a flow-run response, which
  is the bundle's `version_id`; or a table's schema version. See
  [Bundle versions](https://docs.popcorn.ai/concepts/bundle-version.md).
- **line** — A series of bundle versions with one head. The **product line**
  is the shared series Popcorn publishes (`kind: product`); a **fork line** is
  one workspace's own series, with a name (`kind: fork`, `fork_name`). Two
  lines can each hold a `1.0.1`. `popcorn app lines` lists a workspace's fork
  lines. See [Fork lines](https://docs.popcorn.ai/concepts/fork-line.md).
- **fork** — Minting a fork line from the product version a channel runs,
  with byte-identical content, and binding the channel to it. It is required
  before a publish, and it is one-way: a channel on a fork line never returns
  to the product line. `popcorn app fork --name <line>` names the line; a
  workspace may own several per app. See
  [Fork lines](https://docs.popcorn.ai/concepts/fork-line.md).
- **head** — The newest version on a line. `popcorn app checkout` checks out
  the head, and a publish must be based on it. *Not to be confused with* the
  bound version, which lags the head while an install has not landed. See
  [How a channel runs a version](https://docs.popcorn.ai/concepts/channel-binding.md).
- **binding**, **bound version** — The one version a channel runs. A run
  reads it once at start and stays pinned to it; table data is not pinned.
  See [How a channel runs a version](https://docs.popcorn.ai/concepts/channel-binding.md).
- **release track** — `alpha`, `beta` or `stable`: which product versions a
  workspace is offered, set per workspace and defaulting to stable. It filters
  `popcorn app list` and `popcorn channel templates`, and the API never says
  which track a workspace is on. *Not to be confused with* a tracker. See
  [Authoring an app bundle](https://docs.popcorn.ai/guides/template-authoring.md).

## Moving a version

- **publish** — Minting the next version on a fork line with
  `popcorn app publish`. It needs workspace-admin rights, starts an install on
  the channel you published from, and reaches every other channel on the line
  through their daily updates. It publishes to a *line*, not to a channel. See
  [Publish and apply](https://docs.popcorn.ai/concepts/publish-and-apply.md).
- **install** — Bringing one channel to one version: reconciling its tables,
  scalars, channel config, schedules and webhooks, then binding it last.
  Installs follow `channel create --template`, a publish, an apply and a daily
  update. An install can be blocked or can skip, and the version exists
  either way. See [Publish and apply](https://docs.popcorn.ai/concepts/publish-and-apply.md).
- **apply** — `popcorn app apply`: bring one channel up to its own line's
  head, from server state alone. It takes no version, reports
  `already_current` when there is nothing to do, and is the retry for an
  install that was blocked. See
  [Publish and apply](https://docs.popcorn.ai/concepts/publish-and-apply.md).
- **adoption** — A channel still on the product version moving onto a fork
  line the workspace already owns. A fork, or an apply in a workspace with
  exactly one fork line of the app, does it. See
  [Fork lines](https://docs.popcorn.ai/concepts/fork-line.md).
- **daily update** — Each channel's scheduled daily install of its line's
  head, which is how a publish reaches the channels you did not publish from.
  It skips archived channels, channels locked against app updates, and
  channels with no update schedule. See
  [Fork lines](https://docs.popcorn.ai/concepts/fork-line.md).
- **checkout** — A CLI operation, not a server one. `popcorn app checkout`
  writes a version's files to disk with a `.popcorn-app.json` baseline that
  records the app, the version it came from and the channel's UUID. It checks
  out the head; `--version <id>` checks out a past version, which
  `app publish` refuses. See
  [Bundle versions](https://docs.popcorn.ai/concepts/bundle-version.md).

## Channels and workspaces

- **channel** — What an app installs into, and the only thing it can. A
  channel is identified by its UUID; its `#name` can change, so a script or
  a note should hold the UUID. The CLI accepts either and resolves a name to
  the UUID. On the wire the id is `conversation_id`, because the API's older
  noun, *conversation*, covers direct messages too, and an app cannot install
  into a direct message. See
  [How a channel runs a version](https://docs.popcorn.ai/concepts/channel-binding.md).
- **tracker** — The product's word for a channel that runs an app, as in
  "each channel is a tracker". Many apps also name their main table
  `tracker`, and the state-machine page's "tracker row" means a row of it.
- **workspace** — The tenant: it owns channels, members and fork lines.
  `popcorn workspace switch` changes which one the CLI acts on.
- **channel config** — A per-channel document holding the channel
  parameters, the channel integrations, and the prompts and templates a
  bundle seeds, among other sections. Flows read it as `$channel.*`, and a run
  pins it at start. `popcorn channel-config show` prints it. *Not to be
  confused with* scalars, which live in the data store and are not in
  `$channel.*`. See
  [Authoring an app bundle](https://docs.popcorn.ai/guides/template-authoring.md).
- **channel parameters** — Typed values in the channel config, read as
  `$channel.<name>`. The manifest's `channel_parameters:` seeds them per key
  and leaves a value the channel changed alone on update. The CLI calls them
  `params`: `popcorn channel-config params set` and `unset`.

## Flows and runs

- **flow** — A YAML file at the bundle root declaring inputs, steps and
  outputs. Its identity is the `name:` inside the file, not the filename, so
  changing `name:` deletes one flow and creates another. Several fields and
  arguments spelled `flow_id`, such as the one `popcorn flow get` takes, hold
  that name. *Not to be confused with* a workflow: the webhook mode
  `trigger_workflow` starts a flow. See
  [A flow's identity is its name](https://docs.popcorn.ai/concepts/flow-identity.md).
- **step** — One entry in a flow's `steps:`: exactly one of an `activity`, a
  `call_flow`, an `await_approval`, a `sleep_seconds` or a nested `steps:`
  block, optionally with `when:`, `foreach:` and `on_error:`. See
  [Authoring an app bundle](https://docs.popcorn.ai/guides/template-authoring.md).
- **activity** — A platform operation a step calls, named
  `<tier>.<domain>.<verb>`, such as `foundation.store.list_rows`; the tiers
  are `foundation`, `feature`, `app` and `system`. The **activity catalog**
  (`popcorn flow activities`) decides what a flow can do. See the
  [activity reference](https://docs.popcorn.ai/reference/activities.md).
- **`call_flow`** — A step that runs another flow of the same bundle as a
  child, pinned to the parent's version, and can wait for its outputs. Its
  key is `flow:`. *Not to be confused with* the activity
  `foundation.workflow.start_flow`, which starts a separate run that reads the
  channel's binding afresh and cannot be waited on; its key is `flow_name:`.
  See [How a channel runs a version](https://docs.popcorn.ai/concepts/channel-binding.md).
- **run** — One execution of a flow, identified by its `workflow_id`
  (`popcorn flow runs get <workflow-id>`). A run is started by `flow run`, a
  schedule, a webhook, a message trigger, an agent or another flow.
- **outcome** — What a caller branches on when a run ends: `succeeded`,
  `failed` or `still_running`. *Not to be confused with* the run's status,
  which uses a finer vocabulary, or with a row's Status column.
- **trigger** — Always qualify it. A **message trigger** is a manifest
  `triggers:` entry that runs a flow for each message in the channel, and its
  `enabled` is written on first install only; a flow's own `trigger:` key is
  refused at publish. **`$trigger`** is the scope that says who and where
  asked for the run (`thread_id`, `message_id`, `user_id`, …). The **trigger
  report** that `popcorn flow get` prints is what starts a flow: schedules,
  webhooks, message triggers, documents, states and other flows. **`trigger_workflow`**
  is a webhook mode.
- **schedule** — A manifest `schedules:` entry that runs a flow on an
  `interval:` or a `cron:`, keyed by flow name and `slug`. Its cadence exists
  three ways: **declared** in the manifest, **armed** on the channel (what
  `popcorn schedule list` shows), and **intended**, the platform's own
  derivation, which a spread offset can move off the declared minute.
  `popcorn app status` compares armed with declared, and uses intended to tell
  a deliberate difference from drift. See
  [Manifest keys](https://docs.popcorn.ai/concepts/manifest-keys.md).
- **webhook** — A per-channel ingest URL (`popcorn webhook list --show-url`)
  whose `action_mode` is `silent`, `as_is`, `ai_enhanced` or
  `trigger_workflow`. In `trigger_workflow` mode each delivery starts the
  flow named by `trigger_flow_name`; responses spell that field
  `trigger_flow_id`, and it holds the name. A **delivery** is one received
  payload (`popcorn webhook deliveries`).

## Data

- **data store** — A channel's tables, scalars and files, scoped to that one
  channel. The CLI reaches it through `popcorn table`, and flows through the
  `foundation.store.*` activities. Older pages also call it the agent store.
- **table** — A named collection of rows with a schema: its columns, their
  merge policies and an optional merge key. The manifest's `tables:`
  reconciles additively — columns are added, never dropped or renamed.
  `popcorn table schema <name>` prints one.
- **row**, **record** — One entry in a table. *Row* is the word in the CLI
  (`popcorn table rows`, `table row get`), these pages and most `store`
  activities; *record* is the wire word (`records`, `record_id`) and survives
  in `foundation.store.get_record`. In a flow a row carries `_record_id` and
  `_rev`.
- **scalar** — A flat `key → text` value on a channel, always a string on
  the wire (`popcorn table scalar get` and `set`). A manifest declares
  scalars in one of two tiers, and a value a flow writes at runtime belongs
  in neither. See [The three scalar tiers](https://docs.popcorn.ai/concepts/scalar-tiers.md).
- **merge policy**, **merge key** — A column's merge policy decides what an
  upsert does to its existing value. A table's merge key decides which
  existing row an insert matches; `merge_on` is the per-call alternative. See
  [Column merge policy](https://docs.popcorn.ai/concepts/merge-policy.md).
- **rev**, **`If-Match`** — A revision token for a conditional write. A row
  carries an integer `rev` (`_rev` in a flow, the `expected_rev` argument of
  `foundation.store.patch_row`); the channel config carries a string `rev`,
  which a parameters update accepts as `If-Match: "<rev>"`. A mismatch is
  refused with 409 and `error: stale_rev`, naming the current rev; the CLI
  reports it as a `conflict`. *Not to be confused with* a `version_id`.

## Integrations and agents

- **integration** — Always qualify it. A **connected account** is one
  person's account with a provider, with an `integration_id`
  (`popcorn channel-config accounts` lists them). A **channel integration** is
  a name in the channel config bound to one account, read as
  `$channel.integrations.<name>` and set with
  `popcorn channel-config integrations set`. An **integration requirement** is
  what a bundle needs connected: a flow's `required_integrations:`, which a
  run refuses to start without, or the manifest's `connections:`. The product
  also calls these *connections*.
- **channel agent** — The agent members talk to in a channel. The manifest's
  `channel_agent:` chooses it and is written or cleared on every install, and
  `AGENT.md` holds notes it reads on demand.
- **app agent** — An agent a bundle defines for itself under
  `agents/<name>/` (`agent.yaml`, `prompt.md`, `schemas/*.json`), which a
  flow runs with `foundation.agent.invoke`. See
  [App bundles](https://docs.popcorn.ai/concepts/app-bundle.md).
- **agent mode** — The CLI setting `POPCORN_AGENT=1`, which defaults
  `--json`, `--quiet` and `--no-color` and suppresses upgrade prompts. It does
  not imply `--yes`, and `app publish` requires `--yes` in agent mode. It has
  nothing to do with the agents above.

## State machines

- **state machine** — A manifest `states:` section over one table: a set of
  small machines, each a **funnel** (the milestone that moves forward) or an
  **overlay** (what is true alongside it). See
  [State machines in a bundle](https://docs.popcorn.ai/concepts/state-machine.md).
- **state**, **event**, **transition** — A machine's values; the named
  things that happen (`staff.*`, `system.*`); and the edge an event fires,
  from one set of states to another, writing facts as it goes. A
  **guard** is a condition an edge requires.
- **CTA** — The button a user sees, declared on the transition it fires
  (`cta:`), so the graph and the interface cannot disagree.
- **Status** — A row's status column, a projection of its machines. It
  changes by firing an event, never by writing the column. *Not to be
  confused with* a run's status or outcome.
