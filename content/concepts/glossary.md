---
id: glossary
title: Glossary
order: 1
layout: lookup
summary: >
  The words a person and their assistant use, from running a Routine to
  building its template. A Routine (the CLI and API say *channel*; once a
  *project*) is ongoing work made from a Routine Template; its Triggers bring
  work in, its Tables hold it, its Status says where each item stands and
  its Actions move it on. A closing table maps the other names.
concepts: [routines, customizing-a-routine, app-bundle, manifest-keys, copying-a-template, versions, flow-grammar, scalar-tiers, merge-policy, state-machine]
---

The words a person sees, and the words an assistant should use when it talks
to one. Ask for an outcome in these terms, such as "add a reminder to this
Routine" or "start a Routine like this one for the Denver office", and
Popcorn decides what has to change underneath. The same words carry on into
building a Routine Template; the files a template is made of keep their own
names (`manifest`, flow, activity), because those are what a template author
types.

Each entry gives the term first, then the other names it goes by, then what
it is most often confused with, then the page that explains it. The CLI, the
API and older copy still call some things by other names; the table at the
end, *Names you'll see elsewhere*, maps each to the word used here.

Two words need a qualifier whenever they mean something other than the
product's sense: **trigger** and **integration**. Each has several meanings,
listed under its entry. **Version** is close behind.

## Routines and workspaces

- **workspace** — Your organisation's space in Popcorn. It holds its
  Routines, its people, its Routine Templates and its copies of them, and an
  assistant connected to Popcorn works in one workspace at a time. Its people
  are its members, each with a workspace role (see *member*).
  `popcorn workspace switch` changes which one the CLI acts on.
- **Routine** — One piece of ongoing work that Popcorn runs for you, such as
  claims intake or order follow-up, together with everything it needs: how
  work arrives, what it knows, what it holds and who takes part. A Routine is
  the one thing a person manages; ask for a change to it, and Popcorn works
  out how to make it. It is identified by its ID; its `#name` can change, so a
  script or a note should hold the ID, which the API calls
  `conversation_id`. The CLI and the MCP read tools accept either and resolve
  a name to the ID; tools that write take the ID. See
  [Routines](https://docs.popcorn.ai/use/concepts/routines.md).
- **Routine Template** — The starting point a Routine is made from, such as
  a claims coordinator. One template can start many Routines, and a Routine
  made from one keeps receiving the template's improvements unless it has been
  changed into a copy of its own (see *customizing a Routine*). Its files are
  its *app bundle*. The set of templates is fixed by Popcorn: changing an
  existing one, through a copy, is self-serve, and adding a new one is not.
  See [App bundles](https://docs.popcorn.ai/build/concepts/app-bundle.md).
- **Inbox Scan** — The Routine Template that reads a mailbox, suggests
  Routines from the work it finds there, and shows how the team writes.
- **customizing a Routine** — Changing one Routine without changing the
  others made from the same template. Most changes stay with that one Routine
  and survive the template's improvements: its Routine Settings, its
  Connections, its Instructions and, where its template keeps them with the
  Routine, its steps and the Actions between them. A change to what the
  Routine is built from (a new Table, a kind of step its template does not
  offer) gives it a copy of its own instead. That copy no longer
  receives the template's improvements, which cannot be undone. Popcorn says
  which kind a change is before it makes it. See
  [Customizing a Routine](https://docs.popcorn.ai/use/concepts/customizing-a-routine.md).
- **member**, **role** — Always qualify them. A **workspace member** is a
  person in that workspace, and its **workspace role** is `owner`, `admin`,
  `member`, `guest` or `workspace_agent`. A **Routine member** has a
  membership of one Routine, and its role there is `owner`, `admin`,
  `member`, `guest`, `agent` or `channel_agent`; a Routine's creator is its
  owner. The two roles are separate, and `owner`, `admin`, `member` and
  `guest` exist at both levels: someone who joins a Routine by invitation
  from another workspace is a `guest` there whatever their workspace role.
  A Routine's admin actions are open to its owners and admins and to
  workspace admins, and only a workspace admin can publish a version of a
  template. `get_user` and `list_workspace_members` report the workspace
  role.
- **active**, **deactivated** — Whether a person still belongs to the
  workspace; `get_user` reports it as **Active**. Removing someone from a
  workspace deactivates them and marks them deleted; their account stays, and
  Popcorn no longer finds them by email or username, so their requests to
  that workspace are refused with `user_not_found`. Joining the same
  workspace again with the same email reactivates the same person, ID
  included.
- **bot**, **workspace agent** — A bot is an account with `is_bot` set, which
  `get_user` reports as **Bot**. Every workspace is created with one, the
  **workspace agent**: a bot with the workspace role `workspace_agent`, named
  after the workspace's agent identity. Installs of a template's versions run
  as the workspace agent, never as the person who asked, and it can read
  every Routine in its workspace. The API that people sign in to refuses a
  request made as a bot. *Not to be confused with* a Routine's Agent (see
  *Agent*).

## How work arrives

- **Trigger** — How work arrives in a Routine: on a schedule, from a message
  in the Routine, from a document added to it, from a booking made through
  its calendar link, or from another system posting to it. A Routine can have
  several. In this sense it needs no qualifier. Building a template, qualify
  it: a **message trigger** is a manifest `triggers:` entry that runs a flow
  for each message in the Routine, and its `enabled` is written once, by the
  install that first brings the trigger to the Routine, and kept after that;
  a flow's own `trigger:` key is refused at publish. **`$trigger`** is the
  scope that says who and where asked for a run (`thread_id`, `message_id`,
  `user_id`, …). The **trigger report** that `popcorn flow get` prints is
  everything that starts a flow: schedules, webhooks, message triggers,
  documents, states and other flows. **`trigger_workflow`** is a webhook mode.
  *Not to be confused with* an Action, which is a person moving one item on.
  See [Triggers](https://docs.popcorn.ai/use/concepts/triggers.md).
- **schedule** — The scheduled kind of Trigger: a manifest `schedules:` entry
  that runs a flow on an `interval:` or a `cron:`, keyed by flow name and
  `slug`. Its cadence exists three ways: **declared** in the manifest,
  **armed** on the Routine (what `popcorn schedule list` shows), and
  **intended**, what Popcorn's own rewrites make of the armed cadence — a
  `deadline` or `window` schedule's spread offset can move a daily cron off
  the declared minute. `popcorn app status` compares armed with declared, and
  uses intended to tell a deliberate difference from drift. See
  [Schedules in a manifest](https://docs.popcorn.ai/build/concepts/schedules.md).
- **webhook** — The Trigger for another system posting to a Routine: a
  per-Routine ingest URL (`popcorn webhook list --show-url`) whose
  `action_mode` is `silent`, `as_is`, `ai_enhanced` or `trigger_workflow`. In
  `trigger_workflow` mode each delivery starts the flow named by
  `trigger_flow_name`; responses spell that field `trigger_flow_id`, and it
  holds the name. A **delivery** is one received payload
  (`popcorn webhook deliveries`).
- **Connection**, **integration** — An account Popcorn uses on the Routine's
  behalf, such as a mailbox it reads from or a calendar it books into. It
  signs in as a person, so only their own accounts can be connected; an
  assistant can say which ones a Routine is missing and, after a dry run,
  connect an account the person has signed in to, or make a webhook.
  Building a template, *integration* is the word, and it always needs a
  qualifier. A **connected account** is one person's account with a provider,
  with an `integration_id` (`popcorn channel-config accounts` lists them). A
  **channel integration** is a name in the Routine's configuration bound to
  one account, read as `$channel.integrations.<name>` and set with
  `popcorn channel-config integrations set`. An **integration requirement**
  is what a template needs connected: a flow's `required_integrations:`, or
  the manifest's `connections:`. Only `required_integrations:` is enforced:
  while one is unconnected (or bound to an account of another provider) a
  run does no work, ending before its first step with empty outputs, which a
  schedule, a webhook or a message trigger sees as success. Starting the flow
  directly is refused instead: `popcorn flow run` and
  `foundation.workflow.start_flow` get 409 `missing_integrations`. A
  `call_flow` step waiting on it fails, under its own `on_error`; a `detach`
  child just ends empty. `connections:` declares what to connect and stops
  nothing. See
  [Connections](https://docs.popcorn.ai/use/concepts/connections.md).
- **Reference** — A document a Routine works from: a policy, a price list, a
  form to fill, an example of good work. A Reference informs the Routine; it
  is not one of the items the Routine tracks. *Not to be confused with* a
  [value reference](https://docs.popcorn.ai/build/concepts/references.md)
  in a flow, such as `$steps.fetch.output`. See
  [References](https://docs.popcorn.ai/use/concepts/reference-documents.md).
- **booking page** — The calendar link people book a meeting through. A
  booking made on it can start an item's work, or complete a booking Step.
- **signing provider** — The service an agreement is sent through for
  signature. Its account is set up per Routine, and Popcorn tracks who has
  signed.

## How it behaves

- **Instructions** — What the Routine should do and how, in plain language:
  how to word a follow-up, when to ask a person first, which deadlines matter,
  when to send a reminder. Changing them changes how the Routine behaves from
  then on. See
  [Instructions](https://docs.popcorn.ai/use/concepts/instructions.md).
- **Routine Settings** — The values that tune a Routine without changing
  what it does: switches that turn a behaviour on or off, and values such as a
  reminder interval or a sender name. A setting reaches only its own Routine,
  can be set back, and survives the template's improvements. Many are a
  Routine's scalars or channel parameters. See
  [Routine Settings](https://docs.popcorn.ai/use/concepts/routine-settings.md).
- **channel parameters** — Typed values in a Routine's configuration, read in
  a flow as `$channel.<name>`; the prompts and templates a bundle seeds are
  folded into them, as `$channel.prompts.<name>` and
  `$channel.templates.<name>`. The manifest's `channel_parameters:` seeds
  them per key and leaves a value the Routine changed alone on update. A run
  pins them, with the rest of `$channel.*`, when it starts. The CLI calls them
  `params`: `popcorn channel-config params set` and `unset`, and
  `popcorn channel-config show` prints the whole configuration. *Not to be
  confused with* scalars, which are not in `$channel.*`. They are Routine
  Settings. See
  [Scalar tiers and Routine Settings](https://docs.popcorn.ai/build/concepts/scalar-tiers.md).
- **scalar** — A flat `key → text` value on a Routine, always a string on
  the wire (`popcorn table scalar get` and `set`). A manifest declares
  scalars in one of two tiers, and a value a flow writes at runtime belongs
  in neither. A scalar a person sets, such as a switch, is a Routine Setting.
  See [Scalar tiers and Routine Settings](https://docs.popcorn.ai/build/concepts/scalar-tiers.md).
- **Agent**, **channel agent**, **app agent** — The assistant inside a
  Routine that does its work and that people talk to. It follows the
  Routine's Instructions, and it asks before the steps the Instructions say
  need a person. Building a template, it is the **channel agent**: the
  manifest's `channel_agent:` proposes it and is written or cleared on every
  install; a Routine-level override set by an operator wins over it, and the
  workspace default applies when neither names an allowed agent. `AGENT.md`
  holds notes it reads on demand. An **app agent** is an agent a template
  defines for itself under `agents/<name>/` (`agent.yaml`, `prompt.md`,
  `schemas/*.json`), which a flow runs with `foundation.agent.invoke`; with
  `chat: true` in `agent.yaml` it can also serve as the Routine's Agent. See
  [App bundles](https://docs.popcorn.ai/build/concepts/app-bundle.md) and
  [Platform tools](https://docs.popcorn.ai/build/concepts/platform-tools.md).

## What it does

- **Step** — Two senses, and the collision is the first one a template
  author meets. A **Routine's Step** is one part of its work on each item, in
  order: what it asks for, what finishes it, and how it follows up until then.
  Not every Routine has Steps, and they are the states of its template's state
  machine (see *state machine*). A **flow's step** is one entry in a flow's
  `steps:`: exactly one of an `activity`, a `call_flow`, an `await_approval`,
  a `sleep_seconds` or a nested `steps:` block, optionally with `when:`,
  `foreach:` and `on_error:`. Not every kind takes every modifier:
  `foreach:` is refused on `sleep_seconds`, `await_approval` and a nested
  block, and `on_error.retry` on `call_flow` and a nested block. An
  `await_approval` step pauses one run until a person replies; it is not how
  a Routine's Reviews or Approvals are built. *Not to be confused with* a
  Trigger, which brings an item in; Steps are what happens to it after. See
  [Steps](https://docs.popcorn.ai/use/concepts/steps.md) and
  [The shape of a flow](https://docs.popcorn.ai/build/concepts/flow-grammar.md).
- **Review** — The kind of Step where a person decides instead of Popcorn.
  The item waits, says why, and offers the Actions that decide where it goes
  next. *Not to be confused with* an Action: a Review is the Step that
  waits, and an Action is the button that ends it. See
  [Reviews](https://docs.popcorn.ai/use/concepts/reviews.md).
- **Approval** — One kind of Review, "should this go ahead?", and the
  outcome of a Review that passes.
- **state machine** — What a Routine's Steps, Status and Actions are built
  from: a manifest `states:` section, or a recipe, over one table — a set of
  small machines. At least one is not an overlay; the first of those is the
  primary, usually a **funnel** (the milestone that moves forward). An
  **overlay** (`overlay: true`) holds what is true alongside it. See
  [State machines in a bundle](https://docs.popcorn.ai/build/concepts/state-machine.md).
- **recipe** — A template's state graph shipped as a root `recipe.yaml`,
  declared by the manifest's `recipe:` block instead of `states:`; it is how
  a Routine's Steps are written. Each Routine can install a revision of its
  own, which runs pinned per run and survives the template's updates.
  Formerly **process** (`process:`, `process.yaml`). See
  [State machines in a bundle](https://docs.popcorn.ai/build/concepts/state-machine.md).
- **state**, **event**, **transition** — A machine's values; the named
  things that happen, grouped in families the template names (`staff.*`,
  `world.*`, `system.*`, …); and the edge an event fires, from one set of
  states to another, writing facts as it goes. A **guard** is a condition an
  edge requires. Two families are special: the staff family (`staff` unless
  the section renames it) is the one Actions fire, and only `system` events
  leave a terminal state.

## What it holds

- **item** — One thing a Routine works on, such as a potential client in an
  intake Routine or an order on its way to a customer. Each item is a Row in
  one of the Routine's Tables. An item is not always a person.
- **Table** — A set of items the Routine keeps, such as claims, orders or
  contacts, shown as rows and columns. Building a template, a table is a
  named collection of rows with a schema: its columns, their merge policies
  and an optional merge key. The manifest's `tables:` reconciles additively
  — columns are added, never dropped or renamed — while a matched column's
  type, format, display and label and the column order follow the manifest,
  and any other setting it declares, on or off, wins; a setting it leaves out
  keeps its installed value. `popcorn table schema <name>` prints one. See
  [Tables](https://docs.popcorn.ai/use/concepts/tables.md) and
  [Table columns](https://docs.popcorn.ai/build/concepts/table-columns.md).
- **Row** — One item in a Table: one claim, one order. *Row* is the word in
  the CLI (`popcorn table rows`, `table row get`) and most `store`
  activities, and in a flow a row carries `_record_id` and `_rev`.
- **Column** — One kind of information every Row in a Table has, such as a
  due date or an amount.
- **Cell** — One Row's value in one Column.
- **Status** — Where an item stands, such as *Waiting on documents* or
  *Approved*. Popcorn works it out from what has happened to the item, so it
  changes when an Action is taken or the Routine moves the item on, not by
  editing the Cell. Building a template, it is a row's status column, a
  projection of its state machines: change it by firing an event. A state
  transition or projected patch that writes it is refused; a plain store
  write is not, and lasts only until the engine next projects the row. *Not
  to be confused with* a run's status or outcome. See
  [Actions and Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md).
- **outcome** — Two senses. An item's outcome is the Status a finished item
  ends on, such as *Retained* or *Not retained*. A run's outcome is what a
  caller branches on when the run ends: `succeeded`, `failed` or
  `still_running`. *Not to be confused with* the run's status, which uses a
  finer vocabulary.
- **merge policy**, **merge key** — A column's merge policy decides what an
  upsert does to its existing value. A table's merge key decides which
  existing row an insert matches. `merge_on` names the match per call, for a
  table without a merge key; on a table with one, `merge_on` is ignored. See
  [Column merge policy](https://docs.popcorn.ai/build/concepts/merge-policy.md).
- **rev**, **`If-Match`** — A revision token for a conditional write. A row
  carries an integer `rev` (`_rev` in a flow, the `expected_rev` argument of
  `foundation.store.patch_row`); a Routine's configuration carries a string
  `rev`, which a per-key parameters patch accepts as `If-Match: "<rev>"`. A
  mismatch is refused with status 412, `error: stale_rev` and the current
  `rev`, for a row and for the configuration alike, and the CLI reports it as
  a `conflict`. `popcorn channel-config params set` sends no `If-Match`, so
  it never meets this refusal. *Not to be confused with* a version's id.

## What people do, and what happened

- **Action** — Something a person does to move an item on: approve, send,
  archive, retry. A Routine offers an item the Actions that make sense for
  where it stands, so the buttons and the Status cannot disagree. See
  [Actions and Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md).
- **CTA** — An Action as a template declares it: the button, declared on the
  transition it fires (`cta:`), so the graph and the interface cannot
  disagree. Only a staff-family transition may carry one.
- **History** — What has happened in a Routine: the work it ran and how each
  run ended, the conversation in it, and the changes to its items, with who or
  what made each one. See
  [History](https://docs.popcorn.ai/use/concepts/history.md).
- **run** — One execution of a flow, and one entry of a Routine's History,
  identified by its `workflow_id` (`popcorn flow runs get <workflow-id>`). A
  run is started by `flow run`, a schedule, a webhook, a message trigger, a
  document, a state machine, an agent or another flow. See
  [Debugging a failed run](https://docs.popcorn.ai/build/guides/debugging-a-failed-run.md).

## Building a template

- **app bundle** (short: **bundle**) — The files of one version of a Routine
  Template: `manifest.yaml`, the flow YAML files at the root, `AGENT.md`,
  `README.md`, `strings.yaml`, and the `prompts/`, `templates/`, `code/` and
  `agents/` directories. The template's slug, such as `claimcoordinator`, is
  the manifest's `app_type:`. *Not to be confused with* the bundle's own
  `templates/` directory, which holds email text. See
  [App bundles](https://docs.popcorn.ai/build/concepts/app-bundle.md).
- **manifest** — `manifest.yaml` at the bundle root; `config.yaml` is still
  read under its legacy name. Each key has its own install semantics, and an
  absent key is not the same as an empty one. An unknown top-level key is
  ignored; an unknown key inside `connections:`, `documents:` or `triggers:`
  is refused.
  See [Manifest keys](https://docs.popcorn.ai/build/concepts/manifest-keys.md).
- **flow** — A YAML file at the bundle root declaring inputs, steps and
  outputs; a Routine's Triggers and Actions start one. Its identity is the
  `name:` inside the file, not the filename, so changing `name:` deletes one
  flow and creates another. Several fields and arguments spelled `flow_id`,
  such as the one `popcorn flow get` takes, hold that name. *Not to be
  confused with* a workflow: the webhook mode `trigger_workflow` starts a
  flow. See
  [The shape of a flow](https://docs.popcorn.ai/build/concepts/flow-grammar.md).
- **activity** — A platform operation a step calls, named
  `<tier>.<domain>.<verb>`, such as `foundation.store.list_rows`, sometimes
  with more segments before the verb (`app.delivery.briefing.collect`); the
  tiers are `foundation`, `feature`, `app` and `system`. The **activity
  catalog** (`popcorn flow activities`) decides what a flow can do. See the
  [activity reference](https://docs.popcorn.ai/reference/activities.md).
- **`call_flow`** — A step that runs another flow of the same bundle as a
  child, pinned to the parent's version. By default (`mode: wait`) it waits
  for the child's outputs; `mode: detach` returns once the child has started.
  Its key is `flow:`. *Not to be confused with* the activity
  `foundation.workflow.start_flow`, which starts a separate run that reads the
  Routine's version afresh and cannot be waited on; its key is `flow_name:`.
  See [Versions](https://docs.popcorn.ai/build/concepts/versions.md).

## Versions and copies

- **version** — One immutable published version of a Routine Template,
  identified two ways: `version_id`, an integer Popcorn assigns (what
  `popcorn app checkout --version` and the MCP tools' `version` take), and
  `semver`, the manifest's `version:`, unique on its copy. Name both when you
  name one. A Routine runs one version at a time, and a run reads it once at
  start and stays pinned to it; table data is not pinned. *Not to be confused
  with* a flow's own `version:`, an integer inside the flow file that a
  `call_flow` step reports as `flow_version`; `flow_version` on a flow-run
  response, which is the bundle's `version_id`; or a table's schema version.
  See [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **copy** — A workspace's own series of versions of a Routine Template, with
  one head and a name; the CLI calls it a *fork line* (`kind: fork`,
  `fork_name`). Until a Routine is copied it runs Popcorn's own version, the
  shared series Popcorn publishes (MCP output calls it the *product line*;
  the API, `kind: product`). Making a copy
  (`copy_routine_template`, `popcorn app fork --name <copy>`) starts it
  byte-identical to the version the Routine runs and moves the Routine onto
  it; a copy is required before a publish, and it is one-way: a Routine on a
  copy never returns to Popcorn's version. Moving a Routine still on
  Popcorn's version onto a copy the workspace already has (`install_routine`
  with `copy`) is called *adoption*, and an install in a workspace with
  exactly one copy does it unasked. A workspace may own several copies of one
  template, and two copies can each hold a `1.0.1`. `popcorn app lines`
  lists them. *Not to be confused with*
  [copying a Routine](https://docs.popcorn.ai/use/concepts/routines.md)
  (`duplicate_routine`), which makes a second Routine running the same
  template, on the same copy if the first is on one, with its settings and
  Steps; it makes no new copy of the template. See
  [Copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md).
- **head** — The newest version on a copy; on Popcorn's version, the version
  the workspace's release track points at. `list_routine_files` and
  `popcorn app checkout` read a copy's head, and a publish must be based on
  it; on a Routine still on Popcorn's version they read the version it runs.
  *Not to be confused with* the version a Routine runs, which lags the head
  while an install has not landed. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **publish** — Minting the next version on a copy, with
  `create_routine_version` or `popcorn app publish`. It needs a workspace
  admin, starts an install on the Routine it names, and reaches every other
  Routine on the copy through their daily updates. It publishes to a *copy*,
  not to one Routine. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **install** — Bringing one Routine to one version: reconciling its tables,
  scalars, configuration, schedules and webhooks, then moving it onto the
  version last. Installs follow creating a Routine from a template, a
  publish, an apply and a daily update. An install can be blocked or can
  skip, and the version exists either way. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **apply** — `install_routine` without `copy`, or `popcorn app apply`: bring
  one Routine on a copy up to that copy's head, from the server's state
  alone. It takes no version, says there is nothing to do when the Routine is
  current, and is the retry for an install that was blocked or failed. A
  Routine still on Popcorn's version is never upgraded by an apply, whose
  answer depends on the workspace's copies: with exactly one, the Routine
  adopts it; with two or more, the apply is refused as ambiguous unless it
  names one; with none, nothing is installed, and the MCP says Popcorn's new
  versions arrive through the daily update. An apply is refused on a Routine
  locked against template updates. It needs a Routine role of `member` or
  above, or a workspace admin. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **daily update** — Each Routine's scheduled daily install of its copy's
  head, which is how a publish reaches the Routines you did not publish from,
  and how a Routine on Popcorn's version reaches its release track's head. It
  runs as the workspace agent and never moves a Routine onto a copy. It skips
  archived Routines, Routines locked against template updates, and Routines
  with no update schedule. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **checkout** — A CLI operation, not a server one. `popcorn app checkout`
  writes a version's files to disk with a `.popcorn-app.json` baseline that
  records the template, the version it came from and the Routine's ID. It
  checks out the head (see *head*); `--version <id>` checks out a past
  version, which `app publish` refuses. Over MCP, `list_routine_files` and
  `read_routine_file` read the same files without a checkout. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **release track** — `alpha`, `beta` or `stable`: which product versions a
  workspace is offered, set per workspace and defaulting to stable. It filters
  `popcorn app list` and `popcorn channel templates`, and the API never says
  which track a workspace is on. See
  [Authoring an app bundle](https://docs.popcorn.ai/build/guides/template-authoring.md).

## Names you'll see elsewhere

The CLI, the API and older copy call some things by a name the product
doesn't use. Pages say the product's word and give the other name once,
where the reader will meet it; this table is where to look one up.

| Name | In the product | Where you'll see it |
|---|---|---|
| app | Routine Template | `popcorn app …`, a manifest's `app_type:`, the `app` field on app responses, MCP output (`App: …`) |
| channel | Routine | the CLI and the API, a `#name`, `conversation_id` on the wire |
| project | Routine | older MCP tools and the web app; *not to be confused with* `feature.state.project`, which recomposes a row's Status |
| tracker | Routine | older product copy and MCP descriptions; many templates also name their main table `tracker` |
| channel template | Routine Template | `popcorn channel templates`, `popcorn channel create --template` |
| channel config | a Routine's configuration: Routine Settings, for its parameters; Connections, for its integrations; it also holds the Routine's installed recipe and other sections | `popcorn channel-config`, `$channel.*` in a flow |
| agent store | a Routine's tables, scalars and files: Tables, for its tables; Routine Settings, for its scalars | some API paths and older pages; flows reach it through `foundation.store.*` |
| record | Row | the wire (`records`, `record_id`), `foundation.store.get_record` |
| fork line | a copy of a Routine Template | `popcorn app fork`, `popcorn app lines`, `kind: fork` on the API, `line:` in MCP output |
| bundle version | a version of a Routine Template | `version_id` on the CLI and the API, `popcorn app checkout --version` |
