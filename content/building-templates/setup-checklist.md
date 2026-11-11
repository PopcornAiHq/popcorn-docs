---
id: setup-checklist
title: Give a template a setup checklist
order: 7
group: What a Bundle holds
summary: >
  A Bundle's setup checklist is `today.onboarding_steps` in
  `strings.yaml`. Questionnaire's connects Gmail, adds the questionnaire
  Reference and sets the reply-by date. A Connection step is done once the
  Connection is made; an upload or value step once its Flow calls
  `feature.onboarding.mark_step` with the step's id, and
  `feature.onboarding.evaluate` latches the Routine set up.
lede: >
  Tell a person what a new Routine needs before it can run, and mark each
  step done as it is finished.
concepts: [strings-yaml, reference-documents, connections, flow-grammar]
---

A Routine Template's setup checklist lists what a new
[Routine](https://docs.popcorn.ai/routines.md) needs before its work can
run, in the order a person should do it. Popcorn shows it on the Routine's
Today tab, and an assistant reads the same steps. The
[Questionnaire](https://docs.popcorn.ai/questionnaire-template.md)
template behind `#team-offsite` has three, all required: connect Gmail,
add the questionnaire, and set the reply-by date.

The checklist is written in the Bundle's
[`strings.yaml`](https://docs.popcorn.ai/strings-yaml.md), so changing it
needs a [Copy](https://docs.popcorn.ai/copying-a-template.md) of the
template. Its Flows mark the steps done.

## Questionnaire's three steps

```yaml title="strings.yaml"
en:
  today:
    onboarding_steps:
      - id: connect_inbox
        kind: connect_inbox
        required: true
        title: Connect Gmail
        body: >-
          The account your questions are sent from, and where replies are
          read. Nothing is sent until a recipient is added.
      - id: questionnaire
        kind: upload_file
        required: true
        title: Add your questionnaire
        body: >-
          A document listing the questions to ask, or a sample email with
          them in it. I'll pull out the questions and show you what I found.
          Anything after the questions ends each email; write {reply_by}
          where the reply-by date should go.
        flow: questionnaire_load
        status_kind: questionnaire_load_progress
        accept: [text]
        sources: [upload]
      - id: reply_by
        kind: set_value
        required: true
        title: Reply-by date
        body: >-
          The date recipients are asked to answer by. Their emails say it,
          and once it has passed, anyone still waiting is marked No
          response instead of followed up.
        cta_label: Save
        flow: reply_by_set
        scalar: questionnaire.reply_by
        field:
          name: value
          type: text
          label: Reply-by date
          placeholder: "2026-11-14 or 14 November"
          help: >-
            A date in the future. Without a year, the next such day.
```

Every step has an `id`, a `kind`, a `title` and a `body`, and the order of
the list is the order Popcorn shows them in. `required: true` makes a step
one the setup waits on. The `kind` decides how the step is completed and
how Popcorn tells it is done:

| Step | `kind` | Completed by | Done when |
|---|---|---|---|
| `connect_inbox` | `connect_inbox` | making the Gmail Connection | every email Connection is made and its sign-in still works |
| `questionnaire` | `upload_file` | adding the questionnaire, which runs `questionnaire_load` | `questionnaire_load` has marked it done, and the questionnaire is still kept |
| `reply_by` | `set_value` | typing a date, which runs `reply_by_set` with it | `questionnaire.reply_by` holds a value the field takes |

> [!NOTE] `{reply_by}` is not a placeholder here
> In the questionnaire step's `body`, `{reply_by}` is text the person reads:
> it tells them what to write in their own questionnaire.

## How each kind of step is completed

### A Connection

A `connect_inbox` step has no Flow. It stands for the template's `email`
[Connections](https://docs.popcorn.ai/connections.md), declared under
`connections:` in the Manifest (see
[Manifest keys](https://docs.popcorn.ai/manifest-keys.md)), and it is done
while every one of them is made and none of their sign-ins has stopped
working. Popcorn reads that live, so a Connection step is always
required. `connect_calendar`, `connect_documents` and `connect_signing`
stand for `calendar`, `documents` and signing Connections the same way.

Making a Connection starts the template's Flow named `on_auth_change`, if
it has one: Popcorn and an assistant both look it up by that name.
Questionnaire's checks that Gmail can send, checks whether setup is now
finished, and starts a pass, so recipients added before Gmail was
connected are asked at once:

```yaml title="on_auth_change.yaml"
steps:
  - id: probe
    activity: feature.email.check_connected
    args:
      integration_name: inbox
      for_send: true

  - id: latch_onboarding
    activity: feature.onboarding.evaluate
    on_error: { policy: skip, retry: 1 }
    args:
      conversation_id: $inputs.conversation_id
      # Needs the send scope, which the checklist's Connection read doesn't.
      email_connected: $steps.probe.output.connected

  - id: kick
    when: $steps.probe.output.connected
    activity: foundation.workflow.start_flow
    on_error: { policy: skip, retry: 1 }
    args:
      conversation_id: $inputs.conversation_id
      flow_name: questionnaire_tick
      inputs:
        conversation_id: $inputs.conversation_id
```

`integration_name: inbox` is the Connection's `config_name` in the
Manifest.

### A Reference upload

An `upload_file` step asks for a document. Its `flow` is the Flow the
upload runs, `status_kind` the progress its card shows while that Flow
runs, `accept` the kinds of file it takes and `sources` how the file is
given: `upload` is a file from the person's computer. Uploading on the
step's card, or adding the questionnaire
[Reference](https://docs.popcorn.ai/reference-documents.md) through an
assistant, runs `questionnaire_load` with the file as its
`conversation_file_key` input.

The Flow reads the questions out of the document before it stores
anything, and fails on a document with no questions in it, which leaves
the step open. Once the questions are saved, it finishes the progress and
then marks the step:

```yaml title="questionnaire_load.yaml"
  - id: status_complete
    activity: foundation.status.set
    on_error: { policy: skip, retry: 0 }
    args:
      conversation_id: $inputs.conversation_id
      kind: questionnaire_load_progress
      state: complete
      data:
        filename: $steps.detect.output.filename

  - id: mark_onboarding
    activity: feature.onboarding.mark_step
    args:
      conversation_id: $inputs.conversation_id
      step_id: questionnaire
```

The order matters: Popcorn hides the checklist the moment its last step
reads done, so a progress frame written after the mark would never be
seen. `mark_onboarding` has no `on_error`, so a failed mark fails the
upload: a step that never reads done is worse than an upload that can be
tried again.

A marked upload step reads done only while its document is still kept, in
the envelope Scalar of the `documents:` entry whose `flow` is the step's:
`questionnaire_file` for Questionnaire. Deleting the questionnaire opens
the step again. A step can name another envelope under
`inputs.envelope_key`, and a step whose Flow two `documents:` entries share
goes by its mark alone, since which document it uploads can't be told.

> [!NOTE] `get_setup` goes by the mark
> An assistant's `get_setup` lists an upload step done once its Flow has
> marked it, and still lists it done after the document is deleted.

### A typed value

A `set_value` step asks for one value. Its `field` is the input the card
shows, with its `label`, `placeholder` and `help`, and `cta_label` is the
text on the card's button. `flow` is the Flow the value runs, and
`scalar` is where that Flow keeps it.

A value given on the card, or through an assistant, is checked against
the `field` first. A `type: text` field takes text, `number` takes a
number (whole, or within `min` and `max`, when the field says so) and
`url` takes a web link, and a `pattern` must match. The step's Flow then
runs with the value under the field's `name`: Questionnaire's `name:
value` is `reply_by_set`'s `value` input.

```yaml title="reply_by_set.yaml"
inputs:
  conversation_id: { type: string }
  value:
    type: string
    description: The reply-by date, as typed.

steps:
  # … parse the date, and refuse one that isn't a date or has passed …

  - id: store
    activity: foundation.store.set_scalar
    args:
      conversation_id: $inputs.conversation_id
      key: questionnaire.reply_by
      value: $steps.parse.output.date

  - id: mark_onboarding
    activity: feature.onboarding.mark_step
    args:
      conversation_id: $inputs.conversation_id
      step_id: reply_by
```

The Flow does its own checking: a value that isn't a date fails the run
with `ReplyByRefused`, and the person sees the Flow's reason. A
`set_value` step is done while its `scalar` holds a value its `field`
takes, read live, so clearing the value opens the step again. The Flow
marks the step all the same: `get_setup` reads the mark, and the step
falls back on it when the value can't be read.

## How the Routine is marked set up

`feature.onboarding.mark_step` records one step as done.
`feature.onboarding.evaluate` decides whether the whole setup is, by the
same rule Popcorn applies when a step is completed on its card or with
`complete_setup_step`: the first time every required step of the
checklist is done, each read as the table above says, it sets the
Routine's `setup_fulfilled`
[Scalar](https://docs.popcorn.ai/scalar-tiers.md) to `"true"`. It never
clears it again.

```yaml title="reply_by_set.yaml"
  - id: probe
    activity: feature.email.check_connected
    on_error: { policy: skip, retry: 1 }
    args:
      integration_name: inbox
      for_send: true

  - id: latch_onboarding
    activity: feature.onboarding.evaluate
    on_error: { policy: skip, retry: 1 }
    args:
      conversation_id: $inputs.conversation_id
      # Needs the send scope, which the checklist's Connection read doesn't.
      email_connected: $steps.probe.output.connected
```

Any of the three steps can be the last one done, so Questionnaire
evaluates in every Flow that completes one (`questionnaire_load`,
`reply_by_set` and `on_auth_change`) and again at the end of each pass of
`questionnaire_tick`. Popcorn sets the same Scalar when a value step
completed through it or an assistant leaves no required step open.

The checklist says what setup waits on: every `required: true` step, read
live, so Questionnaire's Flows pass no list of steps. On a checklist
written in `strings.yaml`, a `required_steps` argument is accepted and
ignored, and a dry run warns (`required_steps_mismatch`) when it differs
from the checklist's required steps, leaving out Connection steps.

`email_connected` is the Flow's own probe: `false` holds the latch, and
when it is left out the rule reads the Connection itself. Questionnaire
passes it because the rule counts the Gmail Connection as made even on a
sign-in without the send scope, which its passes would never send from.

Once `setup_fulfilled` is set, Popcorn stops showing the checklist on the
Today tab, and a later Gmail disconnect asks the person to reconnect
rather than showing the checklist again. It doesn't start or hold back
the Routine's work: Questionnaire's pass checks the questionnaire, Gmail
and the reply-by date for itself.

> [!NOTE] `onboarding_complete`
> `feature.onboarding.evaluate` also takes `fully_live`, the template's own
> signal that the Routine is running, and sets `onboarding_complete` once
> it holds. Questionnaire passes none, so its Routines never set it.

## Ids that must agree

A checklist spans `strings.yaml`, the Manifest and the Flows, and they
find each other only by name:

| In `strings.yaml` | Must equal |
|---|---|
| an upload or value step's `id` | the `step_id` its Flow passes to `feature.onboarding.mark_step` |
| an upload step's `flow`, `status_kind` and `accept`, and `sources` when both say | the `documents:` entry naming the same Flow |
| an upload step's `status_kind` | an entry under `status_kinds:` in the Manifest, and the `kind` its Flow's `foundation.status.set` writes |
| an upload step's `accept` | the `accept` its Flow gives `foundation.file.detect`, which refuses any other file |
| a value step's `field.name` | an input of its `flow` |
| a value step's `scalar` | the key its `flow` sets |

The Manifest's `documents:`, `connections:` and `status_kinds:` keys are
described in [Manifest keys](https://docs.popcorn.ai/manifest-keys.md).

> [!WARNING] Only the document link is refused
> A Bundle whose upload step and `documents:` entry disagree is refused
> when it is validated or published. Two more disagreements are warnings
> in a dry run, which a Publish accepts: a `documents:` entry whose
> `accept` differs from its Flow's `foundation.file.detect`
> (`document_accept_mismatch`), and a `required_steps` list that differs
> from the checklist (`required_steps_mismatch`). Nothing checks the rest:
> a step id misspelt in `mark_step` never reads done.

## What a person sees

On the Routine's Today tab, Popcorn shows the template's
`today.onboarding_intro` above the steps, and each step as a card with its
title, its body and a way to complete it: a button to connect, a file
picker, or the field and its Save button. An assistant reads the same
checklist:

> "What does #team-offsite need before it can run?"

> [!TIP] MCP tool call
> Your assistant calls `get_setup`.

Your assistant lists each step with whether it's done and, for a step
left, what completes it. [Set up your first
Routine](https://docs.popcorn.ai/set-up-a-routine.md) completes
Questionnaire's three:

> "Connect my Gmail to #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `make_connection`.

> "Add these offsite questions to #team-offsite: …"

> [!TIP] MCP tool call
> Your assistant calls `add_reference` for the `questionnaire` Reference.

> "Set #team-offsite's reply-by date to 14 November."

> [!TIP] MCP tool call
> Your assistant calls `complete_setup_step`.

A value step answers once its Flow has run: the value it saved, or the
Flow's reason for refusing it, then the checklist as it now reads.

## Add a step

> "Add a 'pick a sender name' step to my questionnaire copy."

> [!TIP] MCP tool call
> Your assistant calls `create_routine_version` without `confirm`, shows
> you the dry run, then calls it with `confirm=true`.

On a Copy, your assistant drafts two changes. The step itself, in
`strings.yaml`:

```yaml title="strings.yaml"
      - id: sender_name
        kind: set_value
        required: true
        title: Sender name
        body: >-
          The name your questions are signed with.
        flow: sender_name_set
        scalar: questionnaire.sender_name
        field:
          name: value
          type: text
          label: Sender name
```

A Flow named `sender_name_set` that takes `value`, stores it in
`questionnaire.sender_name` with `foundation.store.set_scalar`, marks
`sender_name` done with `feature.onboarding.mark_step`, and evaluates the
setup as `reply_by_set` does. The Flows that already evaluate need no
change: the step holds setup because it says `required: true`.

The step only asks for the name. For the emails to be signed with it,
the template's code block has to read `questionnaire.sender_name` when it
writes them, which is a change of its own.

> [!NOTE] A Routine already set up
> `setup_fulfilled` is never cleared, so Popcorn doesn't show the
> checklist again on a Routine that finished setup before the step was
> added. An assistant still lists the new step as left, and completes it
> the same way.
