---
id: schedules
title: Schedules in a Manifest
order: 9
group: What a Bundle holds
summary: >
  A Routine's scheduled Triggers are Manifest Schedules, such as
  Questionnaire's questionnaire-tick: each names one Flow and `interval:` or
  `cron:`, never both. Each Install of a new Version reconciles Schedules by
  (Flow, slug), and a Schedule whose `flow:` is not in the Bundle (a typo,
  a renamed Flow) disappears: skipped, then deleted as undeclared.
lede: >
  How a template schedules a Routine's work, and what happens to a Schedule
  when a new Version installs.
concepts: [manifest-keys, flow-grammar]
---

A Routine's scheduled [Triggers](https://docs.popcorn.ai/triggers.md) —
the ones that run on a clock — are Schedules in its template's
[Manifest](https://docs.popcorn.ai/manifest-keys.md). Each names the
[Flow](https://docs.popcorn.ai/flow-grammar.md) it runs, a cadence, and
the inputs each fire passes.

> "Show me the schedule in #team-offsite's template."

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, then `read_routine_file` for
> `manifest.yaml`.

The [Questionnaire](https://docs.popcorn.ai/questionnaire-template.md)
template that `#team-offsite` runs has one Schedule. Every fifteen minutes
it runs `questionnaire_tick`, the pass that asks new recipients, reads
replies and follows up:

```yaml title="manifest.yaml"
schedules:
  - flow: questionnaire_tick
    slug: questionnaire-tick
    interval: 900
    class: periodic
    overlap: skip
    jitter: 60
    inputs:
      conversation_id: <channel-conversation-id>
      workspace_id: <workspace-id>
```

| Key | What it does |
|---|---|
| `flow` | the Flow each fire starts, by name |
| `slug` | with `flow`, the Schedule's identity across Installs |
| `interval` or `cron` | the cadence: seconds between fires, or a cron expression with an optional `timezone:` (default `UTC`) |
| `class` | the queue and how fires are spread: `periodic` (the default), `deadline` or `window` |
| `overlap` | what a fire does while the last Run is still going: `skip` (the default), `buffer_one`, `buffer_all` or `allow_all` |
| `jitter` | up to this many seconds' random delay on each fire |
| `inputs` | the Flow's inputs on every fire |

`overlap: skip` is why a slow pass in `#team-offsite` never runs alongside
the next one: a fire that lands while a pass is going starts nothing.

## Inputs address their own Routine

Schedule `inputs` support two substitutions applied at Install:
`<channel-conversation-id>` and `<workspace-id>`. That is how Questionnaire
passes each Routine's own id into `questionnaire_tick`, so the same Bundle
works in every Routine made from it. The same two work in `triggers:`
inputs.

## One cadence, and a class that routes it

Each entry names at most one of `interval:` or `cron:`. An entry with
neither is on demand: it is created paused, and a Flow arms it with
`foundation.workflow.update_schedule`'s `fire_at`. Publish does not
refuse one naming both: the Install fails for a new Schedule, while a
Schedule that already exists is instead skipped and kept exactly as it was,
and the Install reports it as skipped. The same rule applies to an unknown
`class:`.

`class:` is routing, not decoration: it picks the queue and how the fire time
is spread — `periodic` (the default) for an interval, `deadline` for a daily
cron, `window` for deferrable work. Only `deadline` and `window` spread a
daily cron.

## Changing the cadence

To pass every hour instead of every fifteen minutes, change `interval: 900`
to `interval: 3600` in a Copy of the template (see
[copying a template](https://docs.popcorn.ai/copying-a-template.md)), and
publish a new [Version](https://docs.popcorn.ai/versions.md). Popcorn's
Questionnaire offers no Routine Setting for it.

Questionnaire's `AGENT.md`, `agent_summary` and `strings.yaml`'s
`waiting_body` say fifteen minutes in words, so change them with the number;
its automation lines follow the Schedule
([changing a Routine Template](https://docs.popcorn.ai/template-authoring.md#read-the-files)).

## Install reconciles by (Flow, slug)

Install upserts each Schedule by (Flow, slug), then deletes the name-keyed
Schedules the Manifest does not declare. A Schedule a Member created on one
of the Routine's Flows is name-keyed too, so a full Install deletes it; a
Version update does not. On a Version update an unchanged
Schedule is left as it is, so a Member's pause survives; only Schedules the
*old* Manifest declared and the new one drops are deleted, and a recreated
Schedule keeps its paused state and note.

> [!WARNING] A typo deletes the Schedule
> A Schedule whose `flow:` is not in the Bundle is skipped, then deleted as
> undeclared. Renaming `questionnaire_tick`, or mistyping it in `flow:`,
> removes `questionnaire-tick`, and nothing passes on a clock again; see
> [a Flow's identity is its name](https://docs.popcorn.ai/flow-grammar.md).

## Live Schedules can differ from the Manifest

A Routine's live Schedules can differ from its Manifest on purpose. A
template's own `set_app_mode` Flow, where it has one, compresses them for
`popcorn.app_mode: test` and pauses them for `off`, and the platform offsets
a plain daily cron of class `deadline` or `window` away from the top of
the hour. Questionnaire has no
`set_app_mode` Flow, so its Schedule matches its Manifest.

> "Do #team-offsite's live schedules match its template?"

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, then `read_routine_file` for
> `manifest.yaml`.

Your assistant reads each live Schedule's cadence, and whether it is
paused, against the Manifest's. It sees that they differ, not which
differences the platform made.

## With the CLI

Two checks here have no MCP equivalent today: an offline check of the
Manifest's Schedules, and a comparison that explains each live difference.

`app validate` reports an entry naming both `interval:` and `cron:` as
`schedule-two-triggers`, before anything reaches the server.

```bash
popcorn app status --channel team-offsite
```

`popcorn app status` compares the live Schedules with the Manifest and
knows which of those differences the platform made: it exits non-zero only
for an unexplained one, or for a Schedule paused with nothing saying why.
Compare through it rather than by reading `schedule list` against the
Manifest. A paused Schedule reports no next fire.
