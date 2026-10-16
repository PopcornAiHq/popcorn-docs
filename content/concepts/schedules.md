---
id: schedules
title: Schedules in a manifest
order: 5
group: What a bundle holds
summary: >
  A manifest schedule names a single flow and either `interval:` or
  `cron:`, never both; its `class:` picks the queue and how a fire is spread. Each install
  of a new version reconciles schedules by (flow, slug), and a schedule whose
  `flow:` is not in the bundle (a typo in it, say) disappears: skipped,
  then deleted as undeclared. `app status` explains live schedules that differ.
concepts: [manifest-keys, flow-identity]
layer: platform
---

A schedule is how a bundle runs a flow on a clock. It names the flow, a
cadence, and the inputs each fire passes. In the product it is one of a
Routine's **Triggers**.

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

## Inputs address their own channel

Schedule `inputs` support two substitutions applied at install:
`<channel-conversation-id>` and `<workspace-id>`. That is how a portable
bundle passes its own channel's id into a scheduled flow. The same two work in
`triggers:` inputs.

## One cadence, and a class that routes it

Each entry names exactly one of `interval:` or `cron:`. `app validate`
reports one naming both (`schedule-two-triggers`). If it reaches the server,
the install fails for a new schedule; a schedule that already exists is
instead skipped and kept exactly as it was, and the install reports it as
skipped. The same rule applies to an unknown `class:`.

`class:` is routing, not decoration: it picks the queue and how the fire time
is spread — `periodic` (the default) for an interval, `deadline` for a daily
cron, `window` for deferrable work. Only `deadline` and `window` spread a
daily cron.

## Install reconciles by (flow, slug)

Install upserts each schedule by (flow, slug), then deletes the name-keyed
schedules the manifest no longer declares; schedules a member created through
another surface are never touched. On a version update an unchanged
`schedules:` section is skipped, only schedules the *old* manifest declared
and the new one drops are deleted, and a recreated schedule keeps its paused
state and note.

**A schedule whose `flow:` is not in the bundle is skipped — and is then
deleted as undeclared**, so a typo in `flow:` removes the schedule it meant to
keep. A renamed flow does the same; see
[a flow's identity is its name](https://docs.popcorn.ai/concepts/flow-identity.md).

## Live schedules can differ from the manifest

A channel's live schedules can differ from its manifest on purpose.
`popcorn.app_mode: test` compresses them, and the platform offsets a plain
daily cron away from the top of the hour. `popcorn app status` compares the
live schedules with the manifest and knows which of those differences the
platform made: it exits non-zero only for an unexplained one, or for a
schedule paused with nothing saying why. Compare through it rather than by
reading `schedule list` against the manifest. A paused schedule reports no
next fire.
