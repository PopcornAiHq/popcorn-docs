---
id: flow-grammar
title: The shape of a Flow
order: 15
group: How a Flow runs
summary: >
  A Flow is one YAML file at the Bundle root, identified by the `name:`
  inside it, not its filename, so renaming it deletes one Flow and creates
  another. A Step is exactly one of five things: an Activity, a sleep, an
  approval gate, a child Flow (`call_flow`), or a nested block, whose inner
  Steps are private. `foreach` repeats a Step per item, at most five at once.
lede: >
  What a Flow file contains: its name, its Steps, and the five kinds of Step
  it can run, read through the Questionnaire template's Flows.
concepts: [references, conditions, on-error, questionnaire-template]
---

A Flow is how a Bundle does work. Nothing in the product names it: a Flow
runs when one of a Routine's Triggers or Actions starts it, and each Run is
part of the Routine's [History](https://docs.popcorn.ai/history.md). This
page reads the Flows of the
[Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md),
the template behind `#team-offsite`.

> "Show me the Flows #team-offsite runs, and read me ask_recipient."

> [!TIP] MCP tool call
> Your assistant calls `list_routine_files`, then `read_routine_file`.

Questionnaire has seven, one YAML file each:

| Flow | Started by | What it does |
|---|---|---|
| `questionnaire_tick` | its [Schedule](https://docs.popcorn.ai/schedules.md), every fifteen minutes | one pass: plans, then runs a child Flow per recipient |
| `ask_recipient` | the tick, once per new recipient | claims the Row, composes, sends or drafts, records `waiting` |
| `check_recipient` | the tick, once per waiting recipient | claims the Row, reads the thread, decides, follows up |
| `cta_apply` | an [Action](https://docs.popcorn.ai/actions-and-status.md): Ask again, Mark answered, Close | applies the Transition to the Rows |
| `questionnaire_load` | adding or replacing the questionnaire [Reference](https://docs.popcorn.ai/reference-documents.md) | reads the questions with a model, stores them |
| `reply_by_set` | the reply-by setup step | parses the date in the code block, stores it |
| `on_auth_change` | connecting Gmail | checks the Connection, starts a pass |

## What a Flow file holds

Here is the start of `ask_recipient`, the Flow that emails one recipient:

```yaml title="ask_recipient.yaml"
name: ask_recipient
version: 1
description: >
  Ask one recipient the questionnaire's questions, and mark them Waiting.
  Run by `questionnaire_tick` for each recipient with no Stage yet.

inputs:
  conversation_id: { type: string }
  record_id: { type: integer }
  send_mode: { type: string }

steps:
  - id: claim
    activity: foundation.store.claim_row
    args:
      conversation_id: $inputs.conversation_id
      table_name: recipients
      record_id: $inputs.record_id
      column: Sending
      holder: $trigger.run_id
      held_code: RecipientBeingAsked
      held_message: Another run is emailing this recipient.
      refuse_when:
        - code: RecipientAlreadyAsked
          message: This recipient has already been asked.
          when:
            - { column: Stage, test: set }
  # … compose, send, draft, thread, record, release, project

outputs:
  record_id: $inputs.record_id
  sent: $steps.record.output
```

A Step's `id` matches `[A-Za-z_][A-Za-z0-9_]*` and is unique across the
whole Flow. `args` are passed to the
[Activity](https://docs.popcorn.ai/activities.md), with any `$` value
resolved first, as [value references](https://docs.popcorn.ai/references.md)
describes. A Step can also carry `when:` (see
[conditions](https://docs.popcorn.ai/conditions.md)), `on_error:` (see
[errors and retries](https://docs.popcorn.ai/on-error.md)),
`timeout_seconds:` and `heartbeat_seconds:`, which override the default
per-attempt timeout. The tick gives its `plan` Step `timeout_seconds: 180`;
a heartbeat only matters for an Activity that sends one.

Beside `name`, `version`, `description`, `inputs`, `steps` and `outputs`, a
Flow may set these keys:

| Key | What it does | In Questionnaire |
|---|---|---|
| `failure_status: {kind, label}` | writes one terminal status update of that kind when a Step fails past every `on_error`, then fails the Run | `questionnaire_load`: "Questionnaire not added" on the Reference's card |
| `confirm: when_asked` | a member's own message asking for the Run is its confirmation, so the Routine's Agent runs it without a dry run | `reply_by_set`: a member who names the date has asked for exactly this |
| `required_integrations` | the Connections a Run needs; see below | none: the tick checks Gmail itself with `feature.email.check_connected` |
| `best_effort: true` | every start goes to the batch tier, and the Flows it launches follow it; for a fan-out nobody waits on | none |
| `trigger: message` | runs the Flow for every message in the Routine, with the message as `$inputs.message` | none |
| `read_only: true` | the author's word that a Run changes nothing, so an Agent's Run of it needs no confirmation | none |
| `on_failure` | one Activity run, best-effort, when the Flow fails for good | none |

**`required_integrations`** names what the Routine must connect, keyed by
the name Steps read as `$channel.integrations.<name>`; `provider`
constrains which account may back it, and an account of another provider
counts as unconnected. While one is unconnected a Run does no work: it ends
before its first Step with empty outputs, which a Schedule, a Webhook, a
Message Trigger or running a Schedule now sees as success. Starting the
Flow directly is refused instead: `popcorn flow run` and a Flow's
`foundation.workflow.start_flow` get 409 `missing_integrations`. A
`call_flow` Step waiting on it fails, under its own `on_error`; a `detach`
child just ends empty.

> [!NOTE] Gmail in Questionnaire
> Questionnaire's Flows read Gmail as `$channel.integrations.inbox`, the
> `config_name` of its Manifest's one Connection, without declaring it
> under `required_integrations`. The tick's `probe` Step asks whether the
> Connection can send, and the code block's `plan` asks nobody until it can.

**A Webhook-started Flow** gets `{conversation_id, payload, headers,
source_hint, delivery_id, webhook_id}` as its inputs, and only from a
Webhook in `trigger_workflow` mode. `payload` is an `object`, so read its
fields as
[extracting fields or deriving them](https://docs.popcorn.ai/extract-or-derive.md)
describes. Questionnaire has no Webhook.

What a Flow may call is the Activity Catalog, served by the platform:
`popcorn flow activities`, or the
[Activity reference](https://docs.popcorn.ai/activities.md).
Author against `foundation` and `feature` Activities at `release` or `beta`;
`app.*` Activities are one Routine Template's own logic, which a Copy of it
keeps calling; they are not a surface to author against. Questionnaire
calls only `foundation` and `feature` Activities, and keeps its own rules
in a code block, called through `foundation.code.execute`.

## A Flow's identity is its name

A Flow is identified by the `name:` inside the YAML. The filename is not part
of its identity — any root-level `.yaml` or `.yml` name that is not reserved
will do. If `name:` is missing the filename stem stands in, which is why
`app validate` treats a missing name as an error, and two files resolving to
the same name make the Bundle unpublishable. The name is a slug: lowercase
letters, digits, hyphens and underscores, starting with a letter or digit,
at most 63 characters. Publish enforces it, and so does building a
Schedule's id.

A Routine keeps no copy of its Flows. Each
[Version](https://docs.popcorn.ai/versions.md) carries an index of its
Flows by name, and the Routine runs whatever the Version it runs declares;
a Flow the new Version no longer declares stops existing for that Routine.
So changing `name:` is not a rename but a delete plus a create, and what
happens to the things that addressed the old name depends on what they are:

| Reference | After the old name disappears |
|---|---|
| a Schedule in the Manifest | skipped at Install, then deleted as undeclared — a log line, no error |
| a Webhook that already exists | never updated, so it keeps pointing at the old name |
| a Trigger, document or State Transition | the Publish fails |

In Questionnaire, `questionnaire_tick` is named by its Schedule,
`questionnaire_load` by the questionnaire Reference, `cta_apply` by the
`states:` tier's Actions, `ask_recipient` and `check_recipient` by the
tick's `call_flow` Steps, and `on_auth_change` by name alone: Popcorn starts
the Flow with that name when Gmail is connected.

> [!WARNING] Rename the references in the same change
> `app validate` reports `schedule-unknown-flow` and `webhook-unknown-flow`
> before you publish. `popcorn flow get <name> --channel <routine>` reports
> everything that starts a Flow — its Schedules, Webhooks and Message
> Trigger, read live from the Routine, and the document, State-transition
> and sibling-flow launches in the Version it runs — so run it on the old
> and new names after a rename.

## A Step is exactly one of five things

`activity:`, `sleep_seconds:`, `await_approval:`, `call_flow:`, or a nested
`steps:` block. Exactly one — the model rejects a Step with two, or none.
Questionnaire uses three of them: Activities everywhere, `call_flow` in the
tick, and a block in `check_recipient`.

- **`sleep_seconds:`** is a durable timer (survives worker restarts, holds
  no worker capacity), must be greater than 0, and cannot be combined with
  `foreach`.
- **`await_approval:`** texts a prompt to a Workspace contact and pauses the
  Run until they reply or it expires. It is a single per-Run gate, so it
  cannot be combined with `foreach` either. It is not how a Routine's
  [Reviews](https://docs.popcorn.ai/reviews.md) are built: Questionnaire's
  *No response* is a State, and its buttons are Actions.

### `call_flow`: a child Flow per recipient

The tick runs one `ask_recipient` per recipient nobody has asked yet:

```yaml title="questionnaire_tick.yaml"
  - id: ask
    foreach: $steps.plan.output.ask
    as: recipient
    max_parallel: 3
    collect: asked
    # A refused claim (another pass is emailing this recipient) or a failed
    # child is a null item; the rest of the pass carries on.
    on_error: { policy: skip }
    call_flow:
      flow: ask_recipient
      mode: wait
      timeout_seconds: 300
      inputs:
        conversation_id: $inputs.conversation_id
        record_id: $recipient.record_id
        send_mode: $steps.send_mode.output.value
```

`flow:` is a literal name the Publish checks, and `inputs:` are resolved
like `args`. With `mode: wait`, the default, the Step returns once the
child has finished, with the child's `outputs:` at
`$steps.<id>.output.outputs.<key>`; with `mode: detach` it returns once the
child has started, with `workflow_id` and `started`, which is false when a
child with the same id already ran. Each child is a Run of its own, so a
failed send fails one recipient's Run and, under `on_error: skip`, leaves
the rest of the pass alone.

- A child runs exactly once, so `on_error.retry` is refused on a
  `call_flow` Step; `call_flow.timeout_seconds` bounds the child's whole
  Run instead, and the Step-level `timeout_seconds` is refused.
- A child's `workflow_id` is the parent's, then the Step id and, under
  `foreach`, the item's index: `…-ask[0]`, `…-check[2]`.
- A Flow may not call itself, Publish refuses a `call_flow` naming a Flow
  the Bundle does not have, and calls nest at most three deep.
- A parent near its Run-history limit refuses to start another child
  (`FlowHistoryBudgetExceeded`); `on_error: skip` turns that into a null
  item.

`foundation.workflow.start_flow` is the other way to launch a Flow, and it
returns once the Run has started: the parent reports Completed whatever the
child does. `questionnaire_load`, `reply_by_set` and `on_auth_change` use it
to start a pass at once, which nothing waits on. When the parent needs the
result, use `call_flow:` with `mode: wait`.

### Blocks are private inside

`check_recipient` follows up only when the code block says so, and groups
the three Steps that do it under one `when:`:

```yaml title="check_recipient.yaml"
  - id: follow_up
    when: $steps.decide.output.follow_up
    steps:
      - id: compose_follow_up
        activity: foundation.code.execute
        # …
      - id: send_follow_up
        activity: feature.email.reply
        # …
      - id: record_follow_up
        when: $steps.send_follow_up.output.id
        activity: foundation.store.patch_row
        # …
    outputs:
      sent: $steps.send_follow_up.output.id
```

The Flow's `outputs:` then reads `$steps.follow_up.output.sent`, and
nothing outside the block can read `send_follow_up` directly:

```
outer step  ──▶ sees $steps.follow_up.output.sent       ✅ (a declared output)
            ──▶ sees $steps.follow_up.output.other      ❌
            ──▶ sees $steps.send_follow_up.*            ❌ (private to the block)

inner step  ──▶ sees $inputs, $channel, $trigger, and every
                enclosing step at every level            ✅
```

- Inner ids are private for reads only: Step ids are unique across the
  whole Flow, blocks included, and reusing one is refused as
  `duplicate step id`.
- `outputs:` is evaluated in the block's inner scope after its Steps ran,
  and is legal only alongside `steps:`. Omit it and the block publishes
  nothing, the same as a skipped Step.
- Blocks nest three lists deep, counting the Flow's own `steps:` as the
  first, so a block inside a block is the deepest legal shape. `app
  validate` reports a third level as `block-too-deep`.
- A block takes no `args`, timeouts, `foreach` or `on_error.retry`: put
  them on the inner Steps.

## `foreach`

`foreach:` takes a list, `as:` names the item, `collect:` names the result
list and `max_parallel:` bounds how many items run at once. It defaults to
1 and may be at most 5; Publish refuses a higher value. Questionnaire's
tick sets 3 on each of its loops.

- **`collect:`** drops null items, so `$steps.ask.asked` holds one result
  per recipient whose child finished, and none for one whose child failed
  and was skipped. Each item is the child's `{workflow_id, flow_name,
  flow_version, outputs}`.
- **Under `call_flow` with `mode: wait`**, `max_parallel` bounds how many
  children are running at once.
- **A `foundation.code.execute` Step inside a `foreach`** runs one item at a
  time whatever you set.
- **A Step-level `when:` on a `foreach` Step is re-evaluated per item**, in
  that item's scope, so `when: $recipient.thread_id` filters items rather
  than skipping the whole Step. An item it filters out is null.

## Posting markdown

`foundation.channel.post`, `channel.post_file` and `channel.edit` default to
`format: plain`, so markdown in `text:` posts literally. Set
`format: markdown`. An edit does not inherit the message's format — set it
again on every edit of a markdown message. Questionnaire posts nothing to
its Routine; its emails are HTML that the code block's `compose` writes.
