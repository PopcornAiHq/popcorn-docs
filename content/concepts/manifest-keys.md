---
id: manifest-keys
title: Manifest keys and what install does to them
order: 3
summary: >
  Each manifest key has its own install semantics, and an absent key is not
  the same as an empty one — omitting schedules leaves them alone, while
  `schedules: []` deletes every schedule the bundle manages. An unknown key,
  such as the typo `schedule:`, is ignored without a warning, and a manifest
  with no app_type clears the channel's.
concepts: [scalar-tiers, merge-policy, state-machine, app-bundle]
applies_to: [cli, mcp, human]
source: [ParsedTemplateConfig, ChannelTemplateInstaller]
---

Every manifest key but `version:` is optional, and each one has its own
install semantics. Getting this wrong is how a live channel's state gets wiped,
so it is worth reading once in full.

| Key | What install does |
|---|---|
| `version` | required to publish; must be a semver such as `1.2.0` — `1.0` parses as a number and is refused |
| `display_name`, `description` | catalog copy for the template picker |
| `changelog` | documentation only on a fork line; the version's note comes from `app publish -m` |
| `tables` | additive reconcile — tables and columns added, attributes fixed, never dropped or renamed |
| `channel_parameters` | upsert; on an update, a value a member edited is kept; types preserved; read as `$channel.<name>` |
| `scalars` | upsert — `scalar-tiers` says when an update keeps the channel's value |
| `default_scalars` | **write once**, on first install only |
| `schedules` | replace the schedules the bundle manages |
| `webhooks` | create if missing; never updated, never deleted |
| `triggers` | the set is replaced; a trigger's `enabled` is written the first time only, so a member's toggle survives upgrades |
| `connections`, `documents`, `required_connections` | replaced on first install; on an update, kept where the channel's copy was edited (see `scalar-tiers`). `required_connections` is the legacy flat list |
| `status_kinds` | merge per kind — kinds the bundle stops declaring stay; on an update, a value a member edited is kept |
| `states` | validated as a graph at publish, read at run time from the bound version |
| `app_type` | sets the channel's app; **absent clears it** |
| `channel_agent` | sets which agent answers members; **absent clears it** |

A top-level key the parser does not know is ignored without a word. A typo
such as `schedule:` does nothing, and nothing tells you.

`scalars.agent_runnable_flows` lists the flows the channel's agent may run.
It is a scalar, not a top-level key, so it follows the scalar rules.

## An absent key is not an empty one

- **Omitting** a key leaves whatever the channel has alone.
- **Declaring it empty** means "replace with nothing" — for the keys that
  replace.

So `schedules: []` deletes every schedule the bundle manages. Omitting
`schedules:` deletes none. The same holds for triggers, connections and
documents.

Keys that only add never remove anything, even when declared empty:
`tables: {}`, `channel_parameters: {}`, `status_kinds: {}` and `webhooks: []`
are all no-ops.

"The schedules the bundle manages" means those keyed by flow name — the ones a
manifest creates. A schedule created some other way is left alone. On an
automatic update the rule narrows again: only schedules the previous version
declared and this one does not are deleted, and a declaration that did not
change is not touched at all, so a member's pause survives.

## Two specific traps

**An untyped bundle clears `app_type` and `channel_agent`.** A manifest with
no `app_type:` strips whatever the channel had, which changes the client's
entire interface; one with no `channel_agent:` hands members back to the
default agent. Never install an untyped bundle into a channel running a real
app. `template check` warns with `clears-app-type`.

**Table changes are additive, so a rename is not a rename.** The reconcile adds
the new column and orphans the old one, with the data still in the old.
Matching ignores case and surrounding whitespace, so a case-only rename keeps
the live name. Renaming a column means renaming every write site too, and only
reading a row back afterwards will tell you that you missed one.
