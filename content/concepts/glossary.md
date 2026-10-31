---
id: glossary
title: Glossary
order: 1
layout: lookup
summary: >
  The words a person and their assistant use, from running a Routine to
  building its template. A Routine (the CLI and API say *channel*; once a
  *project*) is ongoing work made from a Routine Template; its Triggers bring
  work in, its Tables hold it, its Status says where each Item stands and
  its Actions move it on. A closing table maps the other names.
lede: >
  The words Popcorn uses, from running a Routine to building its template, and
  the other names you'll see for them.
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
product's sense: **Trigger** and **Integration**. Each has several meanings,
listed under its entry. **Version** is close behind.

## Routines and Workspaces

- **Workspace** — Your organisation's space in Popcorn. It holds its
  Routines, its people, its Routine Templates and its Copies of them, and an
  assistant connected to Popcorn works in one Workspace at a time. Its people
  are its Members, each with a Workspace Role (see *Member*).
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
  changed into a Copy of its own (see *customizing a Routine*). Its files are
  its *App Bundle*. The set of templates is fixed by Popcorn: changing an
  existing one, through a Copy, is self-serve, and adding a new one is not.
  See [App Bundles](https://docs.popcorn.ai/build/concepts/app-bundle.md).
- **Inbox Scan** — The Routine Template that reads a mailbox, suggests
  Routines from the work it finds there, and shows how the team writes.
- **customizing a Routine** — Changing one Routine without changing the
  others made from the same template. Most changes stay with that one Routine
  and survive the template's improvements: its Routine Settings, its
  Connections, its Instructions and, where its template keeps them with the
  Routine, its Steps and the Actions between them. A change to what the
  Routine is built from (a new Table, a kind of Step its template does not
  offer) gives it a Copy of its own instead. That Copy no longer
  receives the template's improvements, which cannot be undone. Popcorn says
  which kind a change is before it makes it. See
  [Customizing a Routine](https://docs.popcorn.ai/use/concepts/customizing-a-routine.md).
- **Member**, **Role** — Always qualify them. A **Workspace Member** is a
  person in that Workspace, and its **Workspace Role** is `owner`, `admin`,
  `member`, `guest` or `workspace_agent`. A **Routine Member** has a
  membership of one Routine, and its Role there is `owner`, `admin`,
  `member`, `guest`, `agent` or `channel_agent`; a Routine's creator is its
  owner. The two Roles are separate, and `owner`, `admin`, `member` and
  `guest` exist at both levels: someone who joins a Routine by invitation
  from another Workspace is a `guest` there whatever their Workspace Role.
  A Routine's admin actions are open to its owners and admins and to
  Workspace admins, and only a Workspace admin can publish a Version of a
  template. `get_user` and `list_workspace_members` report the Workspace
  Role.
- **active**, **deactivated** — Whether a person still belongs to the
  Workspace; `get_user` reports it as **Active**. Removing someone from a
  Workspace deactivates them and marks them deleted; their account stays, and
  Popcorn no longer finds them by email or username, so their requests to
  that Workspace are refused with `user_not_found`. Joining the same
  Workspace again with the same email reactivates the same person, ID
  included.
- **Bot**, **Workspace Agent** — A Bot is an account with `is_bot` set, which
  `get_user` reports as **Bot**. Every Workspace is created with one, the
  **Workspace Agent**: a Bot with the Workspace Role `workspace_agent`, named
  after the Workspace's agent identity. Installs of a template's Versions run
  as the Workspace Agent, never as the person who asked, and it can read
  every Routine in its Workspace. The API that people sign in to refuses a
  request made as a Bot. *Not to be confused with* a Routine's Agent (see
  *Agent*).

## How work arrives

- **Trigger** — How work arrives in a Routine: on a Schedule, from a message
  in the Routine, from a document added to it, from a booking made through
  its calendar link, or from another system posting to it. A Routine can have
  several. In this sense it needs no qualifier. Building a template, qualify
  it: a **Message Trigger** is a Manifest `triggers:` entry that runs a Flow
  for each message in the Routine, and its `enabled` is written once, by the
  Install that first brings the Trigger to the Routine, and kept after that;
  a Flow's own `trigger:` key is refused at Publish. **`$trigger`** is the
  scope that says who and where asked for a Run (`thread_id`, `message_id`,
  `user_id`, …). The **Trigger Report** that `popcorn flow get` prints is
  everything that starts a Flow: Schedules, Webhooks, Message Triggers,
  documents, States and other Flows. **`trigger_workflow`** is a Webhook mode.
  *Not to be confused with* an Action, which is a person moving one Item on.
  See [Triggers](https://docs.popcorn.ai/use/concepts/triggers.md).
- **Schedule** — The scheduled kind of Trigger: a Manifest `schedules:` entry
  that runs a Flow on an `interval:` or a `cron:`, keyed by Flow name and
  `slug`. Its cadence exists three ways: **declared** in the Manifest,
  **armed** on the Routine (what `popcorn schedule list` shows), and
  **intended**, what Popcorn's own rewrites make of the armed cadence — a
  `deadline` or `window` Schedule's spread offset can move a daily cron off
  the declared minute. `popcorn app status` compares armed with declared, and
  uses intended to tell a deliberate difference from drift. See
  [Schedules in a Manifest](https://docs.popcorn.ai/build/concepts/schedules.md).
- **Webhook** — The Trigger for another system posting to a Routine: a
  per-Routine ingest URL (`popcorn webhook list --show-url`) whose
  `action_mode` is `silent`, `as_is`, `ai_enhanced` or `trigger_workflow`. In
  `trigger_workflow` mode each Delivery starts the Flow named by
  `trigger_flow_name`; responses spell that field `trigger_flow_id`, and it
  holds the name. A **Delivery** is one received payload
  (`popcorn webhook deliveries`).
- **Connection**, **Integration** — An account Popcorn uses on the Routine's
  behalf, such as a mailbox it reads from or a calendar it books into. It
  signs in as a person, so only their own accounts can be connected; an
  assistant can say which ones a Routine is missing and, after a dry run,
  connect an account the person has signed in to, or make a Webhook.
  Building a template, *Integration* is the word, and it always needs a
  qualifier. A **Connected Account** is one person's account with a provider,
  with an `integration_id` (`popcorn channel-config accounts` lists them). A
  **channel integration** is a name in the Routine's configuration bound to
  one account, read as `$channel.integrations.<name>` and set with
  `popcorn channel-config integrations set`. An **Integration Requirement**
  is what a template needs connected: a Flow's `required_integrations:`, or
  the Manifest's `connections:`. Only `required_integrations:` is enforced:
  while one is unconnected (or bound to an account of another provider) a
  Run does no work, ending before its first Step with empty outputs, which a
  Schedule, a Webhook or a Message Trigger sees as success. Starting the Flow
  directly is refused instead: `popcorn flow run` and
  `foundation.workflow.start_flow` get 409 `missing_integrations`. A
  `call_flow` Step waiting on it fails, under its own `on_error`; a `detach`
  child just ends empty. `connections:` declares what to connect and stops
  nothing. See
  [Connections](https://docs.popcorn.ai/use/concepts/connections.md).
- **Reference** — A document a Routine works from: a policy, a price list, a
  form to fill, an example of good work. A Reference informs the Routine; it
  is not one of the Items the Routine tracks. *Not to be confused with* a
  [value reference](https://docs.popcorn.ai/build/concepts/references.md)
  in a Flow, such as `$steps.fetch.output`. See
  [References](https://docs.popcorn.ai/use/concepts/reference-documents.md).
- **Booking Page** — The calendar link people book a meeting through. A
  booking made on it can start an Item's work, or complete a booking Step.
- **Signing Provider** — The service an agreement is sent through for
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
  Routine's Scalars or channel parameters. See
  [Routine Settings](https://docs.popcorn.ai/use/concepts/routine-settings.md).
- **channel parameters** — Typed values in a Routine's configuration, read in
  a Flow as `$channel.<name>`; the prompts and templates a Bundle seeds are
  folded into them, as `$channel.prompts.<name>` and
  `$channel.templates.<name>`. The Manifest's `channel_parameters:` seeds
  them per key and leaves a value the Routine changed alone on update. A Run
  pins them, with the rest of `$channel.*`, when it starts. The CLI calls them
  `params`: `popcorn channel-config params set` and `unset`, and
  `popcorn channel-config show` prints the whole configuration. *Not to be
  confused with* Scalars, which are not in `$channel.*`. They are Routine
  Settings. See
  [Scalar tiers and Routine Settings](https://docs.popcorn.ai/build/concepts/scalar-tiers.md).
- **Scalar** — A flat `key → text` value on a Routine, always a string on
  the wire (`popcorn table scalar get` and `set`). A Manifest declares
  Scalars in one of two tiers, and a value a Flow writes at runtime belongs
  in neither. A Scalar a person sets, such as a switch, is a Routine Setting.
  See [Scalar tiers and Routine Settings](https://docs.popcorn.ai/build/concepts/scalar-tiers.md).
- **Agent**, **channel agent**, **App Agent** — The assistant inside a
  Routine that does its work and that people talk to. It follows the
  Routine's Instructions, and it asks before the Steps the Instructions say
  need a person. Building a template, it is the **channel agent**: the
  Manifest's `channel_agent:` proposes it and is written or cleared on every
  Install; a Routine-level override set by an operator wins over it, and the
  Workspace default applies when neither names an allowed Agent. `AGENT.md`
  holds notes it reads on demand. An **App Agent** is an agent a template
  defines for itself under `agents/<name>/` (`agent.yaml`, `prompt.md`,
  `schemas/*.json`), which a Flow runs with `foundation.agent.invoke`; with
  `chat: true` in `agent.yaml` it can also serve as the Routine's Agent. See
  [App Bundles](https://docs.popcorn.ai/build/concepts/app-bundle.md) and
  [Platform tools](https://docs.popcorn.ai/build/concepts/platform-tools.md).

## What it does

- **Step** — Two senses, and the collision is the first one a template
  author meets. A **Routine's Step** is one part of its work on each Item, in
  order: what it asks for, what finishes it, and how it follows up until then.
  Not every Routine has Steps, and they are the States of its template's State
  Machine (see *State Machine*). A **Flow's Step** is one entry in a Flow's
  `steps:`: exactly one of an `activity`, a `call_flow`, an `await_approval`,
  a `sleep_seconds` or a nested `steps:` block, optionally with `when:`,
  `foreach:` and `on_error:`. Not every kind takes every modifier:
  `foreach:` is refused on `sleep_seconds`, `await_approval` and a nested
  block, and `on_error.retry` on `call_flow` and a nested block. An
  `await_approval` Step pauses one Run until a person replies; it is not how
  a Routine's Reviews or Approvals are built. *Not to be confused with* a
  Trigger, which brings an Item in; Steps are what happens to it after. See
  [Steps](https://docs.popcorn.ai/use/concepts/steps.md) and
  [The shape of a Flow](https://docs.popcorn.ai/build/concepts/flow-grammar.md).
- **Review** — The kind of Step where a person decides instead of Popcorn.
  The Item waits, says why, and offers the Actions that decide where it goes
  next. *Not to be confused with* an Action: a Review is the Step that
  waits, and an Action is the button that ends it. See
  [Reviews](https://docs.popcorn.ai/use/concepts/reviews.md).
- **Approval** — One kind of Review, "should this go ahead?", and the
  Outcome of a Review that passes.
- **State Machine** — What a Routine's Steps, Status and Actions are built
  from: a Manifest `states:` section, or a Recipe, over one Table — a set of
  small machines. At least one is not an Overlay; the first of those is the
  primary, usually a **Funnel** (the milestone that moves forward). An
  **Overlay** (`overlay: true`) holds what is true alongside it. See
  [State Machines in a Bundle](https://docs.popcorn.ai/build/concepts/state-machine.md).
- **Recipe** — A template's State graph shipped as a root `recipe.yaml`,
  declared by the Manifest's `recipe:` block instead of `states:`; it is how
  a Routine's Steps are written. Each Routine can install a revision of its
  own, which runs pinned per Run and survives the template's updates.
  Formerly **process** (`process:`, `process.yaml`). See
  [State Machines in a Bundle](https://docs.popcorn.ai/build/concepts/state-machine.md).
- **State**, **Event**, **Transition** — A machine's values; the named
  things that happen, grouped in families the template names (`staff.*`,
  `world.*`, `system.*`, …); and the edge an Event fires, from one set of
  States to another, writing facts as it goes. A **Guard** is a condition an
  edge requires. Two families are special: the staff family (`staff` unless
  the section renames it) is the one Actions fire, and only `system` Events
  leave a terminal State.

## What it holds

- **Item** — One thing a Routine works on, such as a potential client in an
  intake Routine or an order on its way to a customer. Each Item is a Row in
  one of the Routine's Tables. An Item is not always a person.
- **Table** — A set of Items the Routine keeps, such as claims, orders or
  contacts, shown as Rows and Columns. Building a template, a Table is a
  named collection of Rows with a schema: its Columns, their Merge Policies
  and an optional Merge Key. The Manifest's `tables:` reconciles additively
  — Columns are added, never dropped or renamed — while a matched Column's
  type, format, display and label and the Column order follow the Manifest,
  and any other setting it declares, on or off, wins; a setting it leaves out
  keeps its installed value. `popcorn table schema <name>` prints one. See
  [Tables](https://docs.popcorn.ai/use/concepts/tables.md) and
  [Table Columns](https://docs.popcorn.ai/build/concepts/table-columns.md).
- **Row** — One Item in a Table: one claim, one order. *Row* is the word in
  the CLI (`popcorn table rows`, `table row get`) and most `store`
  Activities, and in a Flow a Row carries `_record_id` and `_rev`.
- **Column** — One kind of information every Row in a Table has, such as a
  due date or an amount.
- **Cell** — One Row's value in one Column.
- **Status** — Where an Item stands, such as *Waiting on documents* or
  *Approved*. Popcorn works it out from what has happened to the Item, so it
  changes when an Action is taken or the Routine moves the Item on, not by
  editing the Cell. Building a template, it is a Row's Status Column, a
  projection of its State Machines: change it by firing an Event. A State
  Transition or projected patch that writes it is refused; a plain store
  write is not, and lasts only until the engine next projects the Row. *Not
  to be confused with* a Run's status or Outcome. See
  [Actions and Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md).
- **Outcome** — Two senses. An Item's Outcome is the Status a finished Item
  ends on, such as *Retained* or *Not retained*. A Run's Outcome is what a
  caller branches on when the Run ends: `succeeded`, `failed` or
  `still_running`. *Not to be confused with* the Run's status, which uses a
  finer vocabulary.
- **Merge Policy**, **Merge Key** — A Column's Merge Policy decides what an
  upsert does to its existing value. A Table's Merge Key decides which
  existing Row an insert matches. `merge_on` names the match per call, for a
  Table without a Merge Key; on a Table with one, `merge_on` is ignored. See
  [Column Merge Policy](https://docs.popcorn.ai/build/concepts/merge-policy.md).
- **rev**, **`If-Match`** — A revision token for a conditional write. A Row
  carries an integer `rev` (`_rev` in a Flow, the `expected_rev` argument of
  `foundation.store.patch_row`); a Routine's configuration carries a string
  `rev`, which a per-key parameters patch accepts as `If-Match: "<rev>"`. A
  mismatch is refused with status 412, `error: stale_rev` and the current
  `rev`, for a Row and for the configuration alike, and the CLI reports it as
  a `conflict`. `popcorn channel-config params set` sends no `If-Match`, so
  it never meets this refusal. *Not to be confused with* a Version's id.

## What people do, and what happened

- **Action** — Something a person does to move an Item on: approve, send,
  archive, retry. A Routine offers an Item the Actions that make sense for
  where it stands, so the buttons and the Status cannot disagree. See
  [Actions and Status](https://docs.popcorn.ai/use/concepts/actions-and-status.md).
- **CTA** — An Action as a template declares it: the button, declared on the
  Transition it fires (`cta:`), so the graph and the interface cannot
  disagree. Only a staff-family Transition may carry one.
- **History** — What has happened in a Routine: the work it ran and how each
  Run ended, the conversation in it, and the changes to its Items, with who or
  what made each one. See
  [History](https://docs.popcorn.ai/use/concepts/history.md).
- **Run** — One execution of a Flow, and one entry of a Routine's History,
  identified by its `workflow_id` (`popcorn flow runs get <workflow-id>`). A
  Run is started by `flow run`, a Schedule, a Webhook, a Message Trigger, a
  document, a State Machine, an Agent or another Flow. See
  [Debug a failed Run](https://docs.popcorn.ai/build/guides/debugging-a-failed-run.md).

## Building a template

- **App Bundle** (short: **Bundle**) — The files of one Version of a Routine
  Template: `manifest.yaml`, the Flow YAML files at the root, `AGENT.md`,
  `README.md`, `strings.yaml`, and the `prompts/`, `templates/`, `code/` and
  `agents/` directories. The template's slug, such as `claimcoordinator`, is
  the Manifest's `app_type:`. *Not to be confused with* the Bundle's own
  `templates/` directory, which holds email text. See
  [App Bundles](https://docs.popcorn.ai/build/concepts/app-bundle.md).
- **Manifest** — `manifest.yaml` at the Bundle root; `config.yaml` is still
  read under its legacy name. Each key has its own Install semantics, and an
  absent key is not the same as an empty one. An unknown top-level key is
  ignored; an unknown key inside `connections:`, `documents:` or `triggers:`
  is refused.
  See [Manifest keys](https://docs.popcorn.ai/build/concepts/manifest-keys.md).
- **Flow** — A YAML file at the Bundle root declaring inputs, Steps and
  outputs; a Routine's Triggers and Actions start one. Its identity is the
  `name:` inside the file, not the filename, so changing `name:` deletes one
  Flow and creates another. Several fields and arguments spelled `flow_id`,
  such as the one `popcorn flow get` takes, hold that name. *Not to be
  confused with* a workflow: the Webhook mode `trigger_workflow` starts a
  Flow. See
  [The shape of a Flow](https://docs.popcorn.ai/build/concepts/flow-grammar.md).
- **Activity** — A platform operation a Step calls, named
  `<tier>.<domain>.<verb>`, such as `foundation.store.list_rows`, sometimes
  with more segments before the verb (`app.delivery.briefing.collect`); the
  tiers are `foundation`, `feature`, `app` and `system`. The **Activity
  Catalog** (`popcorn flow activities`) decides what a Flow can do. See the
  [Activity reference](https://docs.popcorn.ai/reference/activities.md).
- **`call_flow`** — A Step that runs another Flow of the same Bundle as a
  child, pinned to the parent's Version. By default (`mode: wait`) it waits
  for the child's outputs; `mode: detach` returns once the child has started.
  Its key is `flow:`. *Not to be confused with* the Activity
  `foundation.workflow.start_flow`, which starts a separate Run that reads the
  Routine's Version afresh and cannot be waited on; its key is `flow_name:`.
  See [Versions](https://docs.popcorn.ai/build/concepts/versions.md).

## Versions and Copies

- **Version** — One immutable published Version of a Routine Template,
  identified two ways: `version_id`, an integer Popcorn assigns (what
  `popcorn app checkout --version` and the MCP tools' `version` take), and
  `semver`, the Manifest's `version:`, unique on its Copy. Name both when you
  name one. A Routine runs one Version at a time, and a Run reads it once at
  start and stays pinned to it; Table data is not pinned. *Not to be confused
  with* a Flow's own `version:`, an integer inside the Flow file that a
  `call_flow` Step reports as `flow_version`; `flow_version` on a Flow-run
  response, which is the Bundle's `version_id`; or a Table's schema version.
  See [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **Copy** — A Workspace's own series of Versions of a Routine Template, with
  one Head and a name; the CLI calls it a *fork line* (`kind: fork`,
  `fork_name`). Until a Routine is copied it runs Popcorn's own version, the
  shared series Popcorn publishes (MCP output says *Popcorn's*; the API,
  `kind: product`). Making a Copy
  (`copy_routine_template`, `popcorn app fork --name <copy>`) starts it
  byte-identical to the Version the Routine runs and moves the Routine onto
  it; a Copy is required before a Publish, and it is one-way: a Routine on a
  Copy never returns to Popcorn's version. Moving a Routine still on
  Popcorn's version onto a Copy the Workspace already has (`install_routine`
  with `copy`) is called *adoption*, and an Install in a Workspace with
  exactly one Copy does it unasked. A Workspace may own several Copies of one
  template, and two Copies can each hold a `1.0.1`. `popcorn app lines`
  lists them, and `list_routines` with `copy` lists the Routines on one.
  *Not to be confused with*
  [copying a Routine](https://docs.popcorn.ai/use/concepts/routines.md)
  (`duplicate_routine`), which makes a second Routine running the same
  template, on the same Copy if the first is on one, with its settings and
  Steps; it makes no new Copy of the template. See
  [Copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md).
- **Head** — The newest Version on a Copy; on Popcorn's version, the Version
  the Workspace's Release Track points at. `list_routine_files` and
  `popcorn app checkout` read a Copy's Head, and a Publish must be based on
  it; on a Routine still on Popcorn's version they read the Version it runs.
  *Not to be confused with* the Version a Routine runs, which lags the Head
  while an Install has not landed. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **Publish** — Minting the next Version on a Copy, with
  `create_routine_version` or `popcorn app publish`. It needs a Workspace
  admin, starts an Install on the Routine it names, and reaches every other
  Routine on the Copy through their Daily Updates. It publishes to a *Copy*,
  not to one Routine. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **Install** — Bringing one Routine to one Version: reconciling its Tables,
  Scalars, configuration, Schedules and Webhooks, then moving it onto the
  Version last. Installs follow creating a Routine from a template, a
  Publish, an Apply and a Daily Update. An Install can be blocked or can
  skip, and the Version exists either way. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **Apply** — `install_routine` without `copy`, or `popcorn app apply`: bring
  one Routine on a Copy up to that Copy's Head, from the server's state
  alone. It takes no Version, says there is nothing to do when the Routine is
  current, and is the retry for an Install that was blocked or failed. A
  Routine still on Popcorn's version is never upgraded by an Apply, whose
  answer depends on the Workspace's Copies: with exactly one, the Routine
  adopts it; with two or more, the Apply is refused as ambiguous unless it
  names one; with none, nothing is installed, and the MCP says Popcorn's new
  Versions arrive through the Daily Update. An Apply is refused on a Routine
  locked against template updates. It needs a Routine Role of `member` or
  above, or a Workspace admin. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **Daily Update** — Each Routine's scheduled daily Install of its Copy's
  Head, which is how a Publish reaches the Routines you did not publish from,
  and how a Routine on Popcorn's version reaches its Release Track's Head. It
  runs as the Workspace Agent and never moves a Routine onto a Copy. It skips
  archived Routines, Routines locked against template updates, and Routines
  with no update schedule. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **Checkout** — A CLI operation, not a server one. `popcorn app checkout`
  writes a Version's files to disk with a `.popcorn-app.json` baseline that
  records the template, the Version it came from and the Routine's ID. It
  checks out the Head (see *Head*); `--version <id>` checks out a past
  Version, which `app publish` refuses. Over MCP, `list_routine_files` and
  `read_routine_file` read the same files without a Checkout. See
  [Versions](https://docs.popcorn.ai/build/concepts/versions.md).
- **Release Track** — `alpha`, `beta` or `stable`: which product Versions a
  Workspace is offered, set per Workspace and defaulting to stable. It filters
  `popcorn app list` and `popcorn channel templates`, and the API never says
  which track a Workspace is on. See
  [Authoring an App Bundle](https://docs.popcorn.ai/build/guides/template-authoring.md).

## Names you'll see elsewhere

The CLI, the API and older copy call some things by a name the product
doesn't use. Pages say the product's word and give the other name once,
where the reader will meet it; this table is where to look one up.

| Name | In the product | Where you'll see it |
|---|---|---|
| app | Routine Template | `popcorn app …`, a Manifest's `app_type:`, the `app` field on app responses |
| channel | Routine | the CLI and the API, a `#name`, `conversation_id` on the wire |
| project | Routine | older MCP tools and the web app; *not to be confused with* `feature.state.project`, which recomposes a Row's Status |
| tracker | Routine | older product copy and MCP descriptions; many templates also name their main Table `tracker` |
| channel template | Routine Template | `popcorn channel templates`, `popcorn channel create --template` |
| channel config | a Routine's configuration: Routine Settings, for its parameters; Connections, for its Integrations; it also holds the Routine's installed Recipe and other sections | `popcorn channel-config`, `$channel.*` in a Flow |
| agent store | a Routine's Tables, Scalars and files: Tables, for its Tables; Routine Settings, for its Scalars | some API paths and older pages; Flows reach it through `foundation.store.*` |
| record | Row | the wire (`records`, `record_id`), `foundation.store.get_record` |
| fork line | a Copy of a Routine Template | `popcorn app fork`, `popcorn app lines`, `kind: fork` on the API |
| product line | Popcorn's own version of a Routine Template, before a Copy | `popcorn app list`, `kind: product` on the API |
| bundle version | a Version of a Routine Template | `version_id` on the CLI and the API, `popcorn app checkout --version` |
