---
id: flow-grammar
title: The shape of a flow
order: 9
group: How a flow runs
summary: >
  A flow is one YAML file at the bundle root, identified by the `name:`
  inside it, not its filename, so renaming it deletes one flow and creates
  another. A step is exactly one of five things: an activity, a sleep, an
  approval gate, a child flow, or a nested block, whose inner steps are
  private. `foreach` repeats a step per item, at most five in parallel.
concepts: [references, conditions, on-error, schedules]
part: build
---

A flow is how a bundle does work. Nothing in the product names it: a flow
runs when one of a Routine's Triggers or Actions starts it, and its runs are
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
  the name steps read as `$channel.integrations.<name>`. A run refuses to
  start while one is unconnected; `provider` constrains which account may
  back it.
- **`best_effort: true`** sends every start of the flow to the batch tier,
  however it was asked for, and the flows it launches follow it. For a
  fan-out nobody is waiting on.
- **`failure_status: {kind, label}`** writes one terminal status-widget update
  of that kind when a step hard-fails past every `on_error`, then fails the
  run.
- **A webhook-started flow** gets `{conversation_id, payload, headers,
  source_hint, delivery_id, webhook_id}` as its inputs, and only from a
  webhook in `trigger_workflow` mode. `payload` is an `object`, so read its
  fields as
  [extracting fields or deriving them](https://docs.popcorn.ai/build/concepts/extract-or-derive.md)
  describes.
- **`timeout_seconds`** and **`heartbeat_seconds`** on a step override the
  default per-attempt timeout; a heartbeat only matters for an activity that
  sends one.

What a flow may call is the activity catalog, served by the platform:
`popcorn flow activities`, or the
[activity reference](https://docs.popcorn.ai/reference/activities.md).
Author against `foundation` and `feature` activities at `release` or `beta`;
`app.*` activities are one Routine Template's own logic, which a copy of it
keeps calling; they are not a surface to author against.

## A flow's identity is its name

A flow is identified by the `name:` inside the YAML. The filename is not part
of its identity — any root-level `.yaml` or `.yml` name that is not reserved
will do. If `name:` is missing the filename stem stands in, which is why
`app validate` treats a missing name as an error, and two files resolving to
the same name make the bundle unpublishable. The name is a slug: lowercase
letters, digits, hyphens and underscores, starting with a letter or digit,
at most 63 characters. Publish enforces it, and so does building a
schedule's id.

A Routine keeps no copy of its flows. Each version carries an index of its
flows by name, and the Routine runs whatever the version it runs declares;
a flow the new version no longer declares stops existing for that Routine.
So changing `name:` is not a rename but a delete plus a create, and what
happens to the things that addressed the old name depends on what they are:

| Reference | After the old name disappears |
|---|---|
| a schedule in the manifest | skipped at install, then deleted as undeclared — a log line, no error |
| a webhook that already exists | never updated, so it keeps pointing at the old name |
| a trigger, document or state transition | the publish fails |

Rename the references in the same change, or don't rename. `app validate`
reports `schedule-unknown-flow` and `webhook-unknown-flow` before you
publish. `popcorn flow get <name> --channel <routine>` reports everything
that starts a flow — its schedules, webhooks and message trigger, read live
from the Routine, and the document, state-transition and sibling-flow
launches in the version it runs — so run it on the old and new names after a
rename.

## A step is exactly one of five things

`activity:`, `sleep_seconds:`, `await_approval:`, `call_flow:`, or a nested
`steps:` block. Exactly one — the model rejects a step with two, or none.

`call_flow:` runs another flow of the same bundle as a child: `flow:` is a
literal name the publish checks, `inputs:` are resolved like `args`, and
`mode: wait` (the default) returns the child's `outputs:` at
`$steps.<id>.output.outputs.<key>`, while `mode: detach` returns once it has
started. A child runs exactly once, so `on_error.retry` is refused on it —
`call_flow.timeout_seconds` bounds it instead.

- A flow may not call itself, and publish refuses a `call_flow` naming a flow
  the bundle does not have.
- Calls nest at most three deep.
- `mode: detach` returns `workflow_id` and `started`, which is false when a
  child with the same id already ran.
- A parent near its run-history limit refuses to start another child
  (`FlowHistoryBudgetExceeded`); `on_error: skip` turns that into a null
  item.

`foundation.workflow.start_flow` is the other way to launch a flow, and it is
asynchronous: the parent reports Completed at once, whatever the child does.
When the parent needs the result, use `call_flow:` with `mode: wait`.

`sleep_seconds:` is a durable timer (survives worker restarts, holds no worker
capacity), must be greater than 0, and cannot be combined with `foreach`.
Neither can `await_approval:`, which is a single blocking per-workflow gate —
fanning it out would key every iteration to the same signal.

## Blocks are private inside

Blocks nest three lists deep, counting the flow's own `steps:` as the first —
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

Inner ids are private for *reads* only: step ids are unique across the whole
flow, blocks included, and reusing one is refused as `duplicate step id`.
`outputs:` is evaluated in the block's inner scope after its steps ran, and is
legal only alongside `steps:`. Omit it and the block publishes nothing — the
same as a skipped step.

## `foreach`

`foreach:` takes a list, `as:` names the item, `collect:` names the result
list, `max_parallel:` bounds concurrency. It defaults to 1 and may be at most
5; publish refuses a higher value. A `foundation.code.execute` step inside a
`foreach` runs one item at a time whatever you set, and under a `call_flow`
with `mode: wait`, `max_parallel` bounds how many children are running at
once. A step-level `when:` on a `foreach` step is **re-evaluated per item** in
that item's scope, so `when: $row.Status == 'firing'` filters items rather
than skipping the whole step.

## Posting markdown

`foundation.channel.post`, `channel.post_file` and `channel.edit` default to
`format: plain`, so markdown in `text:` posts literally. Set
`format: markdown`. An edit does not inherit the message's format — set it
again on every edit of a markdown message.
