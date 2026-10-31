---
id: flow-grammar
title: The shape of a Flow
order: 13
group: How a Flow runs
summary: >
  A Flow is one YAML file at the Bundle root, identified by the `name:`
  inside it, not its filename, so renaming it deletes one Flow and creates
  another. A Step is exactly one of five things: an Activity, a sleep, an
  approval gate, a child Flow, or a nested block, whose inner Steps are
  private. `foreach` repeats a Step per item, at most five in parallel.
lede: >
  What a Flow file contains: its name, its Steps, and the five kinds of Step
  it can run.
concepts: [references, conditions, on-error, schedules]
part: build
---

A Flow is how a Bundle does work. Nothing in the product names it: a Flow
runs when one of a Routine's Triggers or Actions starts it, and its Runs are
part of the Routine's History.

```yaml
name: my_flow             # identity — not the filename
version: 1
description: >
  What this does and why it is shaped this way.
best_effort: false        # true: run on the batch tier; children follow
failure_status: { kind: my_kind, label: My flow }   # one terminal status update on a hard failure
required_integrations:
  mail: { description: The inbox to read, provider: google }

inputs:
  conversation_id: { type: string }
  thing: { type: string, required: false, default: "" }

steps:
  - id: fetch             # [A-Za-z_][A-Za-z0-9_]*, unique across the flow
    activity: foundation.store.list_rows
    when: $inputs.thing != ''
    on_error: { policy: skip, retry: 1 }
    timeout_seconds: 600  # per attempt; heartbeat_seconds too
    args: { ... }

  - id: each
    activity: foundation.store.patch_row
    foreach: $steps.fetch.output.rows
    as: row
    max_parallel: 1
    collect: patched
    args:
      record_id: $row._record_id

outputs:
  ids: $steps.fetch.output.rows
```

- **`required_integrations`** names what the Routine must connect, keyed by
  the name Steps read as `$channel.integrations.<name>`; `provider`
  constrains which account may back it, and an account of another provider
  counts as unconnected. While one is unconnected a Run does no work: it ends
  before its first Step with empty outputs, which a Schedule, a Webhook, a
  Message Trigger or running a Schedule now sees as success. Starting the
  Flow directly is refused instead: `popcorn flow run` and a Flow's
  `foundation.workflow.start_flow` get 409 `missing_integrations`. A
  `call_flow` Step waiting on it fails, under its own `on_error`; a `detach`
  child just ends empty.
- **`best_effort: true`** sends every start of the Flow to the batch tier,
  however it was asked for, and the Flows it launches follow it. For a
  fan-out nobody is waiting on.
- **`failure_status: {kind, label}`** writes one terminal status-widget update
  of that kind when a Step hard-fails past every `on_error`, then fails the
  Run.
- **A Webhook-started Flow** gets `{conversation_id, payload, headers,
  source_hint, delivery_id, webhook_id}` as its inputs, and only from a
  Webhook in `trigger_workflow` mode. `payload` is an `object`, so read its
  fields as
  [extracting fields or deriving them](https://docs.popcorn.ai/build/concepts/extract-or-derive.md)
  describes.
- **`timeout_seconds`** and **`heartbeat_seconds`** on a Step override the
  default per-attempt timeout; a heartbeat only matters for an Activity that
  sends one.

What a Flow may call is the Activity Catalog, served by the platform:
`popcorn flow activities`, or the
[Activity reference](https://docs.popcorn.ai/reference/activities.md).
Author against `foundation` and `feature` Activities at `release` or `beta`;
`app.*` Activities are one Routine Template's own logic, which a Copy of it
keeps calling; they are not a surface to author against.

## A Flow's identity is its name

A Flow is identified by the `name:` inside the YAML. The filename is not part
of its identity — any root-level `.yaml` or `.yml` name that is not reserved
will do. If `name:` is missing the filename stem stands in, which is why
`app validate` treats a missing name as an error, and two files resolving to
the same name make the Bundle unpublishable. The name is a slug: lowercase
letters, digits, hyphens and underscores, starting with a letter or digit,
at most 63 characters. Publish enforces it, and so does building a
Schedule's id.

A Routine keeps no copy of its Flows. Each Version carries an index of its
Flows by name, and the Routine runs whatever the Version it runs declares;
a Flow the new Version no longer declares stops existing for that Routine.
So changing `name:` is not a rename but a delete plus a create, and what
happens to the things that addressed the old name depends on what they are:

| Reference | After the old name disappears |
|---|---|
| a Schedule in the Manifest | skipped at Install, then deleted as undeclared — a log line, no error |
| a Webhook that already exists | never updated, so it keeps pointing at the old name |
| a Trigger, document or State Transition | the Publish fails |

Rename the references in the same change, or don't rename. `app validate`
reports `schedule-unknown-flow` and `webhook-unknown-flow` before you
publish. `popcorn flow get <name> --channel <routine>` reports everything
that starts a Flow — its Schedules, Webhooks and Message Trigger, read live
from the Routine, and the document, State-transition and sibling-flow
launches in the Version it runs — so run it on the old and new names after a
rename.

## A Step is exactly one of five things

`activity:`, `sleep_seconds:`, `await_approval:`, `call_flow:`, or a nested
`steps:` block. Exactly one — the model rejects a Step with two, or none.

`call_flow:` runs another Flow of the same Bundle as a child: `flow:` is a
literal name the Publish checks, `inputs:` are resolved like `args`, and
`mode: wait` (the default) returns the child's `outputs:` at
`$steps.<id>.output.outputs.<key>`, while `mode: detach` returns once it has
started. A child runs exactly once, so `on_error.retry` is refused on it —
`call_flow.timeout_seconds` bounds it instead.

- A Flow may not call itself, and Publish refuses a `call_flow` naming a Flow
  the Bundle does not have.
- Calls nest at most three deep.
- `mode: detach` returns `workflow_id` and `started`, which is false when a
  child with the same id already ran.
- A parent near its Run-history limit refuses to start another child
  (`FlowHistoryBudgetExceeded`); `on_error: skip` turns that into a null
  item.

`foundation.workflow.start_flow` is the other way to launch a Flow, and it is
asynchronous: the parent reports Completed at once, whatever the child does.
When the parent needs the result, use `call_flow:` with `mode: wait`.

`sleep_seconds:` is a durable timer (survives worker restarts, holds no worker
capacity), must be greater than 0, and cannot be combined with `foreach`.
Neither can `await_approval:`, which is a single blocking per-workflow gate —
fanning it out would key every iteration to the same signal.

## Blocks are private inside

Blocks nest three lists deep, counting the Flow's own `steps:` as the first —
so a block inside a block is the deepest legal shape and a third level is
rejected. `app validate` reports it as `block-too-deep`.

```yaml
  - id: maybe                     # a BLOCK: `when:` gates the whole group
    when: $steps.check.output.ok
    steps:
      - id: inner
        activity: foundation.channel.post
        args: { ... }
    outputs:
      posted: $steps.inner.output   # the ONLY thing outside can read
```

```
outer step  ──▶ sees $steps.maybe.output.posted        ✅ (a declared output)
            ──▶ sees $steps.maybe.output.anything_else ❌
            ──▶ sees $steps.inner.*                    ❌ (private to the block)

inner step  ──▶ sees $inputs, $channel, $trigger, and every
                enclosing step at every level           ✅
```

Inner ids are private for *reads* only: Step ids are unique across the whole
Flow, blocks included, and reusing one is refused as `duplicate step id`.
`outputs:` is evaluated in the block's inner scope after its Steps ran, and is
legal only alongside `steps:`. Omit it and the block publishes nothing — the
same as a skipped Step.

## `foreach`

`foreach:` takes a list, `as:` names the item, `collect:` names the result
list, `max_parallel:` bounds concurrency. It defaults to 1 and may be at most
5; Publish refuses a higher value. A `foundation.code.execute` Step inside a
`foreach` runs one item at a time whatever you set, and under a `call_flow`
with `mode: wait`, `max_parallel` bounds how many children are running at
once. A Step-level `when:` on a `foreach` Step is **re-evaluated per item** in
that item's scope, so `when: $row.Status == 'firing'` filters items rather
than skipping the whole Step.

## Posting markdown

`foundation.channel.post`, `channel.post_file` and `channel.edit` default to
`format: plain`, so markdown in `text:` posts literally. Set
`format: markdown`. An edit does not inherit the message's format — set it
again on every edit of a markdown message.
