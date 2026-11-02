---
id: schedules
title: Schedules in a Manifest
order: 6
group: What a Bundle holds
summary: >
  A Routine's scheduled Triggers are Manifest Schedules: each names a single
  Flow and either `interval:` or `cron:`, never both, and its `class:` picks
  the queue and how a fire is spread. Each Install of a new Version reconciles
  Schedules by (Flow, slug), and a Schedule whose `flow:` is not in the Bundle
  (a typo in it, say) disappears: skipped, then deleted as undeclared.
lede: >
  How a template schedules a Routine's work, and what happens to a Schedule
  when a new Version installs.
concepts: [manifest-keys, flow-grammar]
---

A Routine's scheduled Triggers — the ones that run on a clock — are
Schedules in its template's Manifest. Each names the Flow it runs, a
cadence, and the inputs each fire passes.

```yaml
schedules:
  - flow: basic_tick
    slug: basic-tick
    interval: 3600         # seconds; or cron: "0 8 * * *" + timezone:
    class: periodic        # periodic | deadline | window
    overlap: skip
    jitter: 60
    inputs:
      conversation_id: <channel-conversation-id>
```

## Inputs address their own Routine

Schedule `inputs` support two substitutions applied at Install:
`<channel-conversation-id>` and `<workspace-id>`. That is how a portable
Bundle passes its own Routine's id into a scheduled Flow. The same two work in
`triggers:` inputs.

## One cadence, and a class that routes it

Each entry names exactly one of `interval:` or `cron:`. `app validate`
reports one naming both (`schedule-two-triggers`). If it reaches the server,
the Install fails for a new Schedule; a Schedule that already exists is
instead skipped and kept exactly as it was, and the Install reports it as
skipped. The same rule applies to an unknown `class:`.

`class:` is routing, not decoration: it picks the queue and how the fire time
is spread — `periodic` (the default) for an interval, `deadline` for a daily
cron, `window` for deferrable work. Only `deadline` and `window` spread a
daily cron.

## Install reconciles by (Flow, slug)

Install upserts each Schedule by (Flow, slug), then deletes the name-keyed
Schedules the Manifest no longer declares; Schedules a Member created through
another surface are never touched. On a Version update an unchanged
`schedules:` section is skipped, only Schedules the *old* Manifest declared
and the new one drops are deleted, and a recreated Schedule keeps its paused
state and note.

**A Schedule whose `flow:` is not in the Bundle is skipped — and is then
deleted as undeclared**, so a typo in `flow:` removes the Schedule it meant to
keep. A renamed Flow does the same; see
[a Flow's identity is its name](https://docs.popcorn.ai/flow-grammar.md).

## Live Schedules can differ from the Manifest

A Routine's live Schedules can differ from its Manifest on purpose.
`popcorn.app_mode: test` compresses them, and the platform offsets a plain
daily cron away from the top of the hour. `popcorn app status` compares the
live Schedules with the Manifest and knows which of those differences the
platform made: it exits non-zero only for an unexplained one, or for a
Schedule paused with nothing saying why. Compare through it rather than by
reading `schedule list` against the Manifest. A paused Schedule reports no
next fire.
