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
| `version` | required to publish; must be a semver such as `1.2.0` — `1.0` parses as a number and is refused | `"0.2.1"` |
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

`scalars.agent_runnable_flows` lists the Flows the Routine's
[Agent](https://docs.popcorn.ai/agent.md) may run: in Questionnaire,
`questionnaire_tick`, `cta_apply`, `on_auth_change` and `reply_by_set`. It
is a Scalar, not a top-level key, so it follows the Scalar rules.

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
*Email sending*, with a warning on its Send option. A channel parameter
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
