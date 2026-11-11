---
id: manifest-keys
title: Manifest keys and what Install does to them
order: 6
group: What a Bundle holds
summary: >
  A Routine Template's Manifest decides what Install does to a Routine, key by
  key, and an absent key is not the same as an empty one — omitting Schedules
  leaves them alone, while `schedules: []` deletes every Schedule the Bundle
  manages. An unknown key, such as the typo `schedule:`, is ignored without a
  warning, and a Manifest with no app_type clears the Routine's.
lede: >
  What installing a template does to a Routine, key by key, and why leaving a
  key out differs from leaving it empty.
concepts: [scalar-tiers, merge-policy, state-machine, app-bundle]
---

A Routine Template's `manifest.yaml` is what decides what a
[Routine](https://docs.popcorn.ai/routines.md) holds and how its
[Triggers](https://docs.popcorn.ai/triggers.md) are set up, every time the
template installs. Every Manifest key but `version:` is optional, and each
one has its own Install semantics. Getting this wrong is how a live
Routine's state gets wiped, so it is worth reading once in full.

> "Show me #team-offsite's Manifest."

> [!TIP] MCP tool call
> Your assistant calls `read_routine_file` for `manifest.yaml`.

The last column says what the
[Questionnaire](https://docs.popcorn.ai/questionnaire-template.md)
Manifest, which `#team-offsite` runs, declares under each key.

| Key | What Install does | In Questionnaire |
|---|---|---|
| `version` | required to publish; must be a semver such as `1.2.0` — `1.0` parses as a number and is refused | `"0.3.0"` |
| `display_name`, `description` | catalog copy for the template picker | `Questionnaire`, and one sentence |
| `changelog` | documentation only on a Copy of the template (the CLI calls it a *fork line*); the Version's note comes from `app publish -m` | one entry per Version |
| `tables` | additive reconcile — Tables and Columns added, attributes fixed, never dropped or renamed; see [Table Columns](https://docs.popcorn.ai/table-columns.md) | `recipients`, one Row per `Email` |
| `channel_parameters` | upsert; on an update, a value a Member edited is kept; types preserved; read as `$channel.<name>` | `follow_up_days: 3`, `max_follow_ups: 3` |
| `channel_parameter_fields` | nothing written: the Routine Settings tools read each parameter's `label` and `description` from the Version the Routine runs | a label and description for each (below) |
| `stored_values` | nothing written: names the Scalars the Bundle's Flows keep, and which of them `get_status` reports; see below | none |
| `scalars` | upsert — [Scalar tiers](https://docs.popcorn.ai/scalar-tiers.md) says when an update keeps the Routine's value | `coordinator_name`, `agent_runnable_flows`, `agent_summary` |
| `default_scalars` | **write once**, on first Install only | `popcorn.email_send_mode: send` |
| `schedules` | replace the Schedules the Bundle manages, by (Flow, slug) — see [Schedules](https://docs.popcorn.ai/schedules.md) | one, `questionnaire-tick`, every 900 seconds |
| `webhooks` | create if missing; never updated, never deleted | none |
| `triggers` | the set is replaced; a Trigger's `enabled` is written the first time only, so a Member's toggle survives upgrades | none |
| `connections`, `documents`, `required_connections` | replaced on first Install; on an update, kept where the Routine's value was edited (see [Scalar tiers](https://docs.popcorn.ai/scalar-tiers.md)). `required_connections` is the legacy flat list | Gmail (`halts_workflow: true`); the `questionnaire` Reference, which starts `questionnaire_load` |
| `status_kinds` | merge per kind — kinds the Bundle stops declaring stay; on an update, a value a Member edited is kept | `questionnaire_load_progress` |
| `states` | validated as a graph at Publish, read at run time from the bound Version. A Bundle declares `states` or `recipe`, never both | the `recipient` machine on `Stage` |
| `recipe` | declares that the graph ships as `recipe.yaml`, which Publish then requires and validates like `states`; `document` (the config key, default `recipe`) and an optional `contract`. Install never overwrites a revision the Routine installed itself: it checks that revision against the new Version and refuses the update if it no longer fits. `process` is the legacy name — see [the Recipe](https://docs.popcorn.ai/state-machine.md) | none |
| `app_type` | sets the Routine's `app_type`; **absent clears it** | `questionnaire` |
| `channel_agent` | sets which Agent answers Members; **absent clears it** | `workflowmcp` |

A top-level key the parser does not know is ignored without a word. A typo
such as `schedule:` does nothing, and nothing tells you.

`scalars.agent_runnable_flows`, `scalars.agent_summary` and
`scalars.coordinator_name` are Scalars, not top-level keys, so they follow
the Scalar rules; [the Agent's keys](#the-agent-s-keys) says what each
does.

## An absent key is not an empty one

- **Omitting** a key leaves whatever the Routine has alone.
- **Declaring it empty** means "replace with nothing" — for the keys that
  replace.

So `schedules: []` in a Copy of Questionnaire deletes `questionnaire-tick`,
and no pass runs on a clock again. Omitting `schedules:` deletes none. The same holds for Triggers, Connections and
documents.

Keys that only add never remove anything, even when declared empty:
`tables: {}`, `channel_parameters: {}`, `status_kinds: {}` and `webhooks: []`
are all no-ops.

"The Schedules the Bundle manages" means those keyed by Flow name — the ones a
Manifest creates. A Schedule created some other way is left alone. On an
automatic update the rule narrows again: only Schedules the previous Version
declared and this one does not are deleted, and a declaration that did not
change is not touched at all, so a Member's pause survives.

## Labelling a parameter

A switch gets its label and description from `strings.yaml`, under
`settings.fields`; Questionnaire labels `popcorn.email_send_mode` there as
*Email sending*, with a warning on its Send option. That switch also has
the platform's own words, which the Routine Settings tools show for a
template that reads it without promoting it. A channel parameter
gets them from `channel_parameter_fields:`, which maps a top-level
parameter to an optional `label` (up to 60 characters) and `description`
(up to 400). The Routine Settings tools print them beside the value, so
whoever changes a setting knows what it holds without reading the Flows:

```yaml title="manifest.yaml"
channel_parameters:
  follow_up_days: 3
  max_follow_ups: 3

channel_parameter_fields:
  follow_up_days:
    label: Days between follow-ups
    description: >-
      Days to wait for a reply, after the first email or a follow-up,
      before following up on the questions still open.
  max_follow_ups:
    label: Follow-ups before giving up
    description: >-
      Follow-ups to send before a recipient who still hasn't answered is
      marked No response.
```

> "What does follow_up_days do on #team-offsite?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine_setting`.

Your assistant shows *Days between follow-ups* and its description beside
the value. Install writes nothing for `channel_parameter_fields:`, and
adding it does not make an installed Routine read as drifted. Publish
refuses an entry for a name not declared under `channel_parameters:`, an
entry for `prompts` or `templates` (each file there is a setting of its
own), a key other than `label` or `description`, and a present key with no
mapping under it.

## Declaring stored values

Questionnaire declares no stored values, so the example below is not
Questionnaire's. `stored_values:` names the Scalars a Bundle's Flows keep,
each with a `description` (up to 400 characters). An entry marked `readable: true` is
reported by the `get_status` tool, ahead of the Routine's Statuses, with its
description beside the value. That is how a Routine shares a view it keeps
current, such as a project brief, with an assistant connected over MCP:

```yaml title="manifest.yaml"
stored_values:
  project.brief:
    description: The project at a glance, rebuilt on every change
    readable: true
```

A Scalar that is not declared readable stays private to the Bundle's Flows:
no tool an assistant gets reads it by key. A readable key no Flow has written
yet reads as not set, and a Workspace that guards personal data withholds the
values.

Install writes nothing for it. Publish refuses:

- more than 10 readable entries, since `get_status` reads each one on every
  call;
- a key with anything but letters, digits and `._:@-`;
- a `popcorn.*` key, which is a setting: declare it in `strings.yaml`;
- a key named like a credential, which is never shown;
- an entry with no `description`, or a field other than `description` and
  `readable`.

## Declaring Connections

`connections:` lists the accounts a Routine needs, each one a
[Connection](https://docs.popcorn.ai/connections.md) a person makes on the
Routine's behalf. Questionnaire needs one, the Gmail its questions go out
from and its replies are read in:

```yaml title="manifest.yaml"
connections:
  - id: gmail
    kind: email
    label: Gmail
    config_name: inbox
    providers: [gmail, google]
    scopes:
      - https://www.googleapis.com/auth/gmail.readonly
      - https://www.googleapis.com/auth/gmail.send
      - https://www.googleapis.com/auth/gmail.compose
    min: 1
    max: 1
    halts_workflow: true
```

| Field | What it says | Default |
|---|---|---|
| `id` | the entry's name, unique in the list | required |
| `kind` | one of `email`, `calendar`, `files`, `sms`, `webhook`, `esign`, `documents` | required |
| `label` | what people see the Connection called | the `id` |
| `config_name` | the name Flows read the account by, as `$channel.integrations.<name>` | the `id` |
| `providers` | which providers' accounts may back it | none |
| `scopes` | the OAuth scopes the Routine needs on the account, as full URLs | none |
| `min`, `max` | how many accounts: at least `min` (1 or more), at most `max` (no limit when absent) | `min: 1` |
| `halts_workflow` | whether people are told the whole Routine waits on it (below) | `true` |
| `flow` | a `webhook` entry only: the Flow its Webhook starts | none |

**`config_name` is how Flows find the account.** Questionnaire's entry is
`gmail`, but its Flows read the account as
`$channel.integrations.inbox`, and its Activities take
`integration_name: inbox`, because `config_name: inbox` binds the
Connection under that name: see
[value references](https://docs.popcorn.ai/references.md). Declare it
whenever the name the Flows use differs from the `id`. It is allowed only
on a `max: 1` entry, never on a `webhook`, and no two entries may bind the
same name.

**`scopes` decide whether an account is enough.** An account
whose grant to the Routine lacks one of them is listed as needing more
access, and the work that uses it can't run. Questionnaire asks Gmail for
reading, sending and drafting, the three things its Flows do with the
mailbox. `providers` lists both `gmail` and `google` because Popcorn names
a Google account either way, depending on how it was connected.

**`min` and `max` count accounts.** `min: 1, max: 1` is exactly one, as
Questionnaire's one mailbox is; `min: 1` with no `max` is one or more,
such as several calendars to book into. `min` is at least 1.

> [!IMPORTANT] `halts_workflow` doesn't stop a Run
> `halts_workflow: true` changes what people are told:
> `list_connections` says the Routine's automations are paused until the
> account is connected, and the summary of a new Routine says the same.
> Nothing at run time reads it. What stops a Flow running without the
> account is the Flow's own
> [`required_integrations`](https://docs.popcorn.ai/flow-grammar.md), or a
> check of its own. Questionnaire does both: `ask_recipient` and
> `check_recipient` declare Gmail, and the tick probes it with
> `feature.email.check_connected`, so it asks nobody until the mailbox can
> send.

Publish refuses an unknown field, an unknown `kind` and a duplicate `id`.

> "Which Connections does #team-offsite need?"

> [!TIP] MCP tool call
> Your assistant calls `list_connections`.

## Declaring References

`documents:` lists the
[References](https://docs.popcorn.ai/reference-documents.md) a Routine
works from: a document a person adds that becomes part of the Routine's
configuration, kept for as long as the Routine lives and replaceable at
any time. Questionnaire has one, the questionnaire itself:

```yaml title="manifest.yaml"
documents:
  - id: questionnaire
    flow: questionnaire_load
    scalar: questionnaire_file
    status_kind: questionnaire_load_progress
    store_file_key_stem: onboarding/questionnaire
    accept: [text]
    required: true
    sources: [upload]
```

| Field | What it says |
|---|---|
| `id` | the Reference's name, unique in the list; required |
| `flow` | the Flow that reads a new file in; required, and installed by the same Bundle |
| `scalar` | the Scalar that Flow writes to say where the file is kept; required |
| `status_kind` | the [progress kind](#showing-progress) the Reference's card shows while that Flow runs; required |
| `store_file_key_stem` | where the Flow keeps the file; required |
| `accept` | the kinds of file the picker offers, such as `text` |
| `required` | whether people are told the Routine needs it; `false` when absent |
| `sources` | how a person supplies it: `upload`, `google_drive`, or both |
| `drive_mime_types` | which Google Drive files the picker lets be picked; derived from `accept` when absent |
| `title`, `used_for` | what the Reference is called and what it is for, when `strings.yaml` doesn't say |

What a card calls the Reference and says it is for comes from
`strings.yaml`, under `documents.<id>`: see
[strings.yaml](https://docs.popcorn.ai/strings-yaml.md). Where
`strings.yaml` has no `title` or `body` for it, `list_references` uses the
entry's own `title` and `used_for`, and failing those names the Reference
by its `id`. Questionnaire declares neither, since its `strings.yaml`
says both.

**The `flow` runs on every add and every replace.** Adding the file, from
its card in Popcorn or with `add_reference`, starts the Flow with the
upload as its `conversation_file_key` input, so the Flow must take one.
Replacing it starts the same Flow again with the new file.
`questionnaire_load` reads the questions out of the document, fails the
Run if it finds none, and only then stores anything:

```yaml title="questionnaire_load.yaml"
inputs:
  conversation_id: { type: string }
  conversation_file_key: { type: string }
```

**The `scalar` is the envelope a card reads.** Popcorn reads the file as
added once that Scalar holds a JSON object with a `store_file_key` and a
`filename`, and `v` absent or 1; anything else reads as still waiting.
The Flow builds it with `foundation.store.merge_json_scalar`, after copying
the file into the Routine's own storage under `store_file_key_stem`:

```yaml title="questionnaire_load.yaml"
  - id: record_location
    activity: foundation.store.merge_json_scalar
    args:
      conversation_id: $inputs.conversation_id
      key: questionnaire_file
      patch:
        v: 1
        source: upload
        drive_file_id: ""
        file_key: $inputs.conversation_file_key
        filename: $steps.detect.output.filename
        kind: $steps.detect.output.kind
        uploaded_at: $steps.now.output.unix
        store_file_key: $steps.copy_to_store.output.file_key
        sha256: $steps.copy_to_store.output.sha256
        size_bytes: $steps.copy_to_store.output.size_bytes
      source_file_key: $inputs.conversation_file_key
      source_filename: $steps.detect.output.filename
```

The Reference's card, `list_references` and the setup step that asks for
the file all read this envelope: `file_key` says who added it,
`uploaded_at` when. Since its existence means "added", a Flow writes it
only for a file it has accepted, which is why `questionnaire_load` checks
the questions first. What the Flow reads out of the file goes in a Scalar
of its own: Questionnaire's questions are the `questionnaire` Scalar,
which its tick reads.

**A setup step for the same Flow must agree with it.** When an
`upload_file` step of the
[setup checklist](https://docs.popcorn.ai/setup-checklist.md) names the
same `flow`, Publish refuses the Bundle unless the two declare the same
`status_kind`, `accept` and `drive_mime_types`, and the same `sources`
when both declare them. Questionnaire's `questionnaire` step says
`flow: questionnaire_load`, `status_kind: questionnaire_load_progress`,
`accept: [text]` and `sources: [upload]`, as its Reference does. The step
says when the file is first asked for; the Reference is what it becomes.

> [!NOTE] `required` is advice
> `required: true` marks a Reference the Routine's work degrades without,
> and changes only what people are shown. Nothing refuses a Run for want
> of it: Questionnaire's tick asks nobody while the `questionnaire` Scalar
> is empty, because its own Flow checks.

> "What is #team-offsite's questionnaire?"

> [!TIP] MCP tool call
> Your assistant calls `list_references`, then `read_reference`.

## Showing progress

`status_kinds:` declares the progress a Flow shows while it works, such as
the chip on a Reference's card while the file is read in. Each kind is a
list of `phases` in the order a Run passes through them:

```yaml title="manifest.yaml"
status_kinds:
  questionnaire_load_progress:
    phases:
      - { state: reading,  pct: 0,  label: "Reading the questionnaire…" }
      - { state: saving,   pct: 80, label: "Saving the questions…" }
      - { state: complete, pct: 100, terminal: true, ok: true,
          label: "Questionnaire added" }
```

| Field | What it says |
|---|---|
| `state` | the phase's name, unique in the kind; what a Flow sets |
| `pct` | where the bar stands, 0 to 100: one number, or a `[start, end]` band an Activity climbs through |
| `label` | what the chip says |
| `terminal` | the finished phase; exactly one, and it must reach 100 |
| `ok` | on the finished phase, whether it finished well |

The first phase starts at 0, the last ends at 100, and the bar only moves
forward: a phase may not start before the one above it ends. A failed
phase is not declared, since a Flow's `failure_status` writes it. A Publish
and its dry run refuse a kind that breaks one of these rules
(`status_kind_invalid`), since every Install of it would.

A Flow moves the chip with `foundation.status.set`, naming the kind and a
`state`, and the Run fills in `pct`, `label`, `terminal` and `ok` from the
matching phase; a value the Step sets itself wins. `questionnaire_load`
sets `reading` first, `saving` once the questions are out, and
`complete` before it marks the setup step done:

```yaml title="questionnaire_load.yaml"
  - id: status_reading
    activity: foundation.status.set
    on_error: { policy: skip, retry: 0 }
    args:
      conversation_id: $inputs.conversation_id
      kind: questionnaire_load_progress
      state: reading
      data:
        file_key: $inputs.conversation_file_key
```

Every write in one Run updates the same chip. Progress is a courtesy,
so each `foundation.status.set` Step skips its own errors rather than fail
the Run. When the Run fails, the Flow's `failure_status`, of kind
`questionnaire_load_progress` with the label "Questionnaire not added",
turns the chip into the failure.

## The Agent's keys

Four keys say who answers people in the Routine and what that
[Agent](https://docs.popcorn.ai/agent.md) knows and may run. Questionnaire
declares all four:

```yaml title="manifest.yaml"
channel_agent: workflowmcp

scalars:
  coordinator_name: Questionnaire
  agent_runnable_flows:
    - questionnaire_tick
    - cta_apply
    - on_auth_change
    - reply_by_set
  agent_summary: |
    This Routine emails each recipient the questions in its questionnaire
    and follows up until they've answered.
    `recipients` has one row per recipient, keyed by `Email`. …
```

**`channel_agent`** names the Agent that answers Members: `workflowmcp`
or `channelmcp`, Popcorn's own Agents, which work the Routine with the
same tools and differ in persona; or `appspecialagent:<name>`, an App
Agent the Bundle defines under `agents/<name>/` with `chat: true` (see
[Platform tools](https://docs.popcorn.ai/platform-tools.md)). An operator's
override for one Routine wins over it, and a name Popcorn doesn't
recognise is ignored, so the Workspace's default Agent answers instead.
An App Agent that doesn't resolve is refused in the Routine rather than
replaced.

**`agent_summary`** is the brief Popcorn's own Agents get on every turn:
what the Routine does, its Tables and the Columns they may write, and the
Flows to run. Keep it short, since it costs every turn. `AGENT.md` is the
longer guide, which the Agent reads when the work needs it. Questionnaire's
summary names the `recipients` Columns its Agent may write and the Actions
`cta_apply` takes; its `AGENT.md` adds what each Column means and how to
answer "Who hasn't answered?". An App Agent doesn't get the summary: its
own prompt is its brief.

> "What does #team-offsite's Agent know about this template?"

> [!TIP] MCP tool call
> Your assistant calls `get_instructions` with `guide: true`, which reads
> `AGENT.md`.

**`agent_runnable_flows`** lists the Flows Popcorn's own Agent may start.
A Flow not listed is refused, and so is every Flow when the list can't be
read; a person can still run one from the Routine in Popcorn.
Questionnaire lists its tick, `cta_apply` for Actions taken from chat, `on_auth_change` and
`reply_by_set`; `questionnaire_load`, `ask_recipient` and
`check_recipient` start only from a Reference or a pass. A listed Flow
still runs as a dry run that Members confirm, unless its file says
otherwise: `read_only: true` runs at once, and
[`confirm: when_asked`](https://docs.popcorn.ai/flow-grammar.md) takes a
Member's own message asking for it as the confirmation. `reply_by_set`
is `confirm: when_asked`, so a Member who tells the Agent the date has
it set without a second question.

**`coordinator_name`** is meant for the Agent's prompt rather than the
template picker, which reads `display_name`. Nothing in Popcorn reads it,
though: Install writes it like any other Scalar, and that is all it does.

## Two specific traps

**An untyped Bundle clears `app_type` and `channel_agent`.** A Manifest with
no `app_type:` strips whatever the Routine had (`questionnaire`, for
`#team-offsite`), which changes the client's entire interface; one with no
`channel_agent:` hands Members back to the default Agent instead of
`workflowmcp`. Never install an untyped Bundle into a Routine whose template
sets `app_type`. `app validate` warns with `clears-app-type`.

**Table changes are additive, so a rename is not a rename.** The reconcile adds
the new Column and orphans the old one, with the data still in the old:
renaming Questionnaire's `Name` to `Full Name` leaves every existing name in
`Name`.
Matching ignores case and surrounding whitespace, so a case-only rename keeps
the live name. Renaming a Column means renaming every write site too, and only
reading a Row back afterwards will tell you that you missed one.
