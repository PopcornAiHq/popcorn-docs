---
id: manifest-keys
title: Manifest keys and what Install does to them
order: 5
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

A Routine Template's `manifest.yaml` is what decides what a Routine holds
and how its Triggers are set up, every time the template installs. Every
Manifest key but `version:` is optional, and each one has its own Install
semantics. Getting this wrong is how a live Routine's state gets wiped, so
it is worth reading once in full.

| Key | What Install does |
|---|---|
| `version` | required to publish; must be a semver such as `1.2.0` — `1.0` parses as a number and is refused |
| `display_name`, `description` | catalog copy for the template picker |
| `changelog` | documentation only on a Copy of the template (the CLI calls it a *fork line*); the Version's note comes from `app publish -m` |
| `tables` | additive reconcile — Tables and Columns added, attributes fixed, never dropped or renamed; see `table-columns` |
| `channel_parameters` | upsert; on an update, a value a Member edited is kept; types preserved; read as `$channel.<name>` |
| `channel_parameter_fields` | nothing written: the Routine Settings tools read each parameter's `label` and `description` from the Version the Routine runs |
| `scalars` | upsert — `scalar-tiers` says when an update keeps the Routine's value |
| `default_scalars` | **write once**, on first Install only |
| `schedules` | replace the Schedules the Bundle manages, by (Flow, slug) — see `schedules` |
| `webhooks` | create if missing; never updated, never deleted |
| `triggers` | the set is replaced; a Trigger's `enabled` is written the first time only, so a Member's toggle survives upgrades |
| `connections`, `documents`, `required_connections` | replaced on first Install; on an update, kept where the Routine's value was edited (see `scalar-tiers`). `required_connections` is the legacy flat list |
| `status_kinds` | merge per kind — kinds the Bundle stops declaring stay; on an update, a value a Member edited is kept |
| `states` | validated as a graph at Publish, read at run time from the bound Version. A Bundle declares `states` or `recipe`, never both |
| `recipe` | declares that the graph ships as `recipe.yaml`, which Publish then requires and validates like `states`; `document` (the config key, default `recipe`) and an optional `contract`. Install never overwrites a revision the Routine installed itself: it checks that revision against the new Version and refuses the update if it no longer fits. `process` is the legacy name — see [the Recipe](https://docs.popcorn.ai/state-machine.md) |
| `app_type` | sets the Routine's `app_type`; **absent clears it** |
| `channel_agent` | sets which Agent answers Members; **absent clears it** |

A top-level key the parser does not know is ignored without a word. A typo
such as `schedule:` does nothing, and nothing tells you.

`scalars.agent_runnable_flows` lists the Flows the Routine's Agent may run.
It is a Scalar, not a top-level key, so it follows the Scalar rules.

## An absent key is not an empty one

- **Omitting** a key leaves whatever the Routine has alone.
- **Declaring it empty** means "replace with nothing" — for the keys that
  replace.

So `schedules: []` deletes every Schedule the Bundle manages. Omitting
`schedules:` deletes none. The same holds for Triggers, Connections and
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

A switch gets its label and description from `strings.yaml`.
A channel parameter gets them from `channel_parameter_fields:`, which maps a
top-level parameter to an optional `label` (up to 60 characters) and
`description` (up to 400). The Routine Settings tools print them beside the value, so whoever
changes a setting knows what it holds without reading the Flows:

```yaml
channel_parameters:
  reminder_days: [3, 7]

channel_parameter_fields:
  reminder_days:
    label: Reminder schedule (days)
    description: >-
      Days to wait before each reminder, one entry per reminder, each
      counted from the previous email.
```

Install writes nothing for it, and adding it does not make an installed
Routine read as drifted. Publish refuses an entry for a name not declared
under `channel_parameters:`, an entry for `prompts` or `templates` (each file
there is a setting of its own), a key other than `label` or `description`,
and a present key with no mapping under it.

## Two specific traps

**An untyped Bundle clears `app_type` and `channel_agent`.** A Manifest with
no `app_type:` strips whatever the Routine had, which changes the client's
entire interface; one with no `channel_agent:` hands Members back to the
default Agent. Never install an untyped Bundle into a Routine whose template sets
`app_type`. `app validate` warns with `clears-app-type`.

**Table changes are additive, so a rename is not a rename.** The reconcile adds
the new Column and orphans the old one, with the data still in the old.
Matching ignores case and surrounding whitespace, so a case-only rename keeps
the live name. Renaming a Column means renaming every write site too, and only
reading a Row back afterwards will tell you that you missed one.
