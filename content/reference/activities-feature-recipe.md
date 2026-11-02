---
id: activities-feature-recipe
title: feature.recipe
order: 138
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.recipe activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.recipe` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.recipe.check`

Check a recipe against an app's head, with no channel to install on.

Holds `document` to the version a new channel of `app` would
install in this workspace, with no channel and no dry run: the
graph, contract and section checks an install runs, for a caller with
no channel to run them on. Writes nothing. The checks that need a
channel — its live rows, stored columns and uploaded questions — are
not run, and a channel's install can still refuse a document that
passes here.

```yaml
- id: <step>
  activity: feature.recipe.check
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `document` | string | no | Default `""`. |
| `app` | string | no | Default `"chase"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `sha` | string |  |
| `stages` | list of string |  |
| `problems` | list of map of string |  |
| `warnings` | list of map of string |  |
| `summary` | string |  |
| `app` | string |  |
| `semver` | string |  |
| `bundle_version_id` | integer, optional |  |
| `label` | string |  |
| `skipped` | list of string |  |
| `note` | string |  |

### `feature.recipe.current`

Report which recipe is in force on the channel, and its text.

The recipe is the one the channel installed, or else the bundle's
own. Reads the channel's config live, so
`sha` is what is installed now and `pinned_sha` is the revision
this run judges rows by; they differ when a recipe was installed
after the run started. `include_document: false` leaves the text
out and reports only the revision, its stages and its sections.

```yaml
- id: <step>
  activity: feature.recipe.current
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `include_document` | boolean | no | Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `declared` | boolean |  |
| `document_key` | string |  |
| `contract` | string |  |
| `source` | string |  |
| `sha` | string |  |
| `pinned_sha` | string |  |
| `installed_at` | string |  |
| `installed_by` | string |  |
| `name` | string |  |
| `document` | string |  |
| `stages` | list of string |  |
| `machines` | map of list of string |  |
| `vocabulary` | map of string |  |
| `guidance` | map of string |  |
| `deadlines` | list of object |  |
| `summary` | string |  |

### `feature.recipe.install`

Check a recipe and install it on the channel, or roll one back.

Takes exactly one of: a new `document`, the `sha` of a revision
the channel already holds, or `revert_to_default` for the bundle's
own. The recipe is held to every check a `states:` section passes
at publish and to the manifest's `contract`, and is refused when a
live row holds a state it does not declare or when it moves a stored
machine to another column. An install then renders the graph's
display hints onto the live tables, renders the bundle's client copy
through the recipe's `vocabulary:`, seeds the scalar keys its
stages read, and writes the revision last: if an earlier write
fails, the previous revision stays in force. `dry_run` checks and
writes nothing; `fail_step: false` reports a refusal instead of
failing the step. Rows are re-projected by a later run, which pins
the new revision.

```yaml
- id: <step>
  activity: feature.recipe.install
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `document` | string | no | Default `""`. |
| `sha` | string | no | Default `""`. |
| `revert_to_default` | boolean | no | Default `false`. |
| `name` | string | no | Default `""`. |
| `installed_by` | string | no | Default `""`. |
| `dry_run` | boolean | no | Default `false`. |
| `fail_step` | boolean | no | Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `dry_run` | boolean |  |
| `source` | string |  |
| `sha` | string |  |
| `previous_sha` | string |  |
| `stages` | list of string |  |
| `problems` | list of map of string |  |
| `warnings` | list of map of string |  |
| `stranded` | list of object |  |
| `tables_patched` | list of string |  |
| `seeded` | list of string |  |
| `vocabulary` | map of string |  |
| `copy_rendered` | integer |  |
| `guidance_agents` | list of string |  |
| `deadlines` | list of object |  |
| `summary` | string |  |
