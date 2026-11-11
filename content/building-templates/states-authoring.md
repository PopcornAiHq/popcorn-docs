---
id: states-authoring
title: Author a States tier
order: 15
group: Tables and Status
summary: >
  Writing the State graph behind a Routine's Status and Actions, on
  Questionnaire's `states:` section: Flows that write Stage, the Actions'
  Flow `cta_apply`, which must start an edge's `flow` and `then` launches
  itself, a guard against a pass, adopting older Rows, and STATE CHANGE.
  Every Publish check is listed with its exact error and fix.
lede: >
  Write the States and Transitions behind a Routine's Status and Actions,
  using the Questionnaire template's own graph.
concepts: [state-machine, questionnaire-template, manifest-keys, app-bundle]
---

This guide builds a States tier the way Popcorn's Questionnaire template
does, from its `manifest.yaml` to a change you publish to a Copy of it.
What a [State Machine](https://docs.popcorn.ai/state-machine.md) *is*, and
why each Action is an edge, is that page's subject, and where the two
overlap it is authoritative. What Questionnaire does as a whole is
[the Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md).

Questionnaire uses a small part of the tier: one machine, stored in a
Column, with three [Actions](https://docs.popcorn.ai/actions-and-status.md).
Where a key it doesn't use needs an example, such as an overlay, a derived
machine or an edge that launches a Flow, the example comes from another
graph, and the text says so.

> [!NOTE] Checked only by the server
> The CLI's own checks don't look inside a graph. It is checked when the
> server parses the [Bundle](https://docs.popcorn.ai/app-bundle.md): by
> `create_routine_version`'s dry run, by `popcorn app validate` run logged
> in from a Checkout of a Copy with edits, and by every
> [Publish](https://docs.popcorn.ai/versions.md). The check stops at the
> first problem, so a new graph takes a few rounds, one error at a time.

## Questionnaire's graph

Each recipient is a Row of the `recipients`
[Table](https://docs.popcorn.ai/tables.md). Where they stand is the
`Stage` [Column](https://docs.popcorn.ai/table-columns.md), and the
[Manifest](https://docs.popcorn.ai/manifest-keys.md)'s `states:` section
turns it into the Row's Status, its Why and the Actions it offers. This is
the section as Questionnaire ships it, without its comments:

```yaml title="manifest.yaml"
states:
  table: recipients
  status:
    column: Status
    ctas_column: CTAs
    why_column: Why
  machines:
    recipient:
      column: Stage
      initial: new
      states:
        new:
          label: Not asked yet
          tone: gray
          why: Asked on the next pass, once the questionnaire, Gmail and the reply-by date are in.
        waiting:
          label: Waiting
          why: Asked, with questions still open.
          policy: {step: {type: questions}}   # the one Step, Answers
        answered:
          label: Answered
          tone: black
          terminal: true
          why: Every question is answered, or a person marked them answered.
        no_response:
          label: No response
          warn: true
          why: No answer after the last follow-up, or the reply-by date passed.
        closed:
          label: Closed
          tone: gray
          terminal: true
          why: Closed by a person; nobody follows up.
  events:
    staff: [ask_again, mark_answered, close]
    world: [asked, answered, gave_up, restarted]
  guards:
    not_held:
      all: [{column: Sending, empty: true}]
      code: RecipientBusy
      message: A pass is emailing or checking this recipient; try again once it has finished.
  transitions:
    - on: world.asked
      from: new
      to: waiting
      expected: true
      description: Sent the questionnaire
    - on: world.answered
      from: waiting
      to: answered
      expected: true
      description: Every question is answered
    - on: world.gave_up
      from: waiting
      to: no_response
      expected: true
      description: Stopped following up
    - on: world.restarted
      from: waiting
      to: new
      description: Started over at a corrected address
    - on: staff.ask_again
      from: no_response
      to: waiting
      writes: {Follow Ups: 0, Last Asked: null}
      guard: [not_held]
      expected: true
      description: Asked again, with the follow-ups starting over
      cta:
        kind: ask-again
        label: Ask again
        message: "Ask {Name|this recipient} again."
    - on: staff.mark_answered
      from: [new, waiting, no_response]
      review: true
      to: answered
      guard: [not_held]
      expected: true
      description: Marked answered by a person
      cta:
        kind: mark-answered
        label: Mark answered
        message: "Mark {Name|this recipient} as answered."
    - on: staff.close
      from: [new, waiting, no_response]
      review: true
      to: closed
      guard: [not_held]
      expected: true
      description: Closed, so nobody follows up
      cta:
        kind: close
        label: Close
        prominence: quiet
        message: "Close {Name|this recipient}."
```

Read it top to bottom:

- **One machine, `recipient`, stored in `Stage`.** A blank Column reads as
  the machine's initial State, so a Row added with no `Stage` is `new`,
  shown as *Not asked yet*. Rows stay blank there until they are asked;
  only `Status` holds the word `new`.
- **Five States.** `answered` and `closed` are `terminal: true`, so no
  person's Action leaves them. `waiting` carries a `policy.step` marker,
  which makes it Questionnaire's one [Step](https://docs.popcorn.ai/steps.md),
  Answers. `no_response` warns, which makes it the one
  [Review](https://docs.popcorn.ai/reviews.md).
- **Two Event families.** The `world` Transitions are the moves a pass
  makes. The `staff` Transitions are people's decisions, and each carries
  a `cta:`, the button that is its Action. Mark answered and Close leave
  `new` and `waiting` as well as the Review, and carry `review: true` so
  the Steps list still names them among the Review's choices (see
  [Which States are Steps](https://docs.popcorn.ai/state-machine.md#which-states-are-steps)).
- **One guard, `not_held`.** Every Action needs `Sending` empty; see
  [The guard that keeps an Action from landing under a pass](#the-guard-that-keeps-an-action-from-landing-under-a-pass).
- **Every Column it names is on the Table:** `Status`, `Why` and `CTAs`
  for the projection, `Stage` for the machine, `Follow Ups` and
  `Last Asked` for Ask again's `writes`, and `Sending` for the guard.

> [!IMPORTANT] Empty a date with null
> Ask again empties `Last Asked` with `null`. `Last Asked` is a `datetime`
> Column, and the store refuses `""` there, so a write of `""` fails the
> Action on every Row.

Publish renders a display hint onto `Status` and `Stage` from the States,
so the Table carries none of its own. Questionnaire's is:

```text
status:new,waiting,answered,no_response,closed;warn=no_response;labels=new:Not asked yet|waiting:Waiting|answered:Answered|no_response:No response|closed:Closed;tone=new:gray|answered:black|closed:gray
```

### Read a Routine's graph

> "What Statuses can a recipient in #team-offsite have?"

> [!TIP] MCP tool call
> Your assistant calls `get_table` on the `recipients` Table.

Your assistant lists the Table's Columns, with `Status` and `Stage` marked
as changed only by Transitions, and the machine with its States. For the
whole file, ask it to read `manifest.yaml` from the
[Routine](https://docs.popcorn.ai/routines.md).

## How the Flows move a recipient

Questionnaire's [Flows](https://docs.popcorn.ai/flow-grammar.md) never fire
a `world` Event. They write `Stage` as a plain fact, and the write projects
the Row as it lands. Here is the end of `ask_recipient`, which records the
first email:

```yaml title="ask_recipient.yaml"
  - id: record
    when: $steps.thread.output.value
    activity: foundation.store.patch_row
    args:
      conversation_id: $inputs.conversation_id
      table_name: recipients
      record_id: $inputs.record_id
      patch:
        Stage: waiting
        Thread: $steps.thread.output.value
        Asked: $steps.now.output.iso
        Last Asked: $steps.now.output.iso
        Follow Ups: 0
        Message Id: $steps.send.output.rfc822_message_id
        Asked Address: $steps.compose.output.to
      change_kind: questionnaire_asked
      change_action: $steps.compose.output.asked
```

`check_recipient` does the same with whatever its code block settles:
`answered`, `no_response`, or a blank `Stage` when the Email was corrected,
which reads as `new` again. Because `Stage` is a Column the projection
reads, each write composes the Row's Status and writes `Status`, `Why` and
`CTAs` in the same call (see
[Status is a projection](https://docs.popcorn.ai/state-machine.md#status-is-a-projection-not-a-column-somebody-writes)).
Neither Flow writes `Sending`: their claim is a
[Row lease](https://docs.popcorn.ai/row-leases.md) that the platform frees
when the Run ends.

Not every Row is reached by a write that projects: a Row from before the
States tier, which `adopt` below writes as a plain fact, one changed by a
writer that doesn't project, or one whose projection failed. A Row at
Answered, Closed or No response is never claimed again, so it would stay
stale. The [Schedule](https://docs.popcorn.ai/schedules.md)'s Flow,
`questionnaire_tick`, ends every pass by projecting the whole Table:

```yaml title="questionnaire_tick.yaml"
  - id: project
    activity: feature.state.project
    timeout_seconds: 180
    on_error: { policy: skip, retry: 1 }
    args:
      results: changed
```

With no `record_ids` it projects the whole Table, and writes only the Rows
whose Status, Why or Actions are stale. `results` narrows only what the
Step returns (`all`, `changed` or `warn`), not what it writes.

So the `world` Transitions don't move a Row. The claims read them:
`ask_recipient` claims with `when_legal: world.asked` and `check_recipient`
with `when_legal: world.answered`, so a recipient is taken only from a
State that Event leaves, and any other is refused as `NoEdge`. The Publish
checks need them too, because `waiting` and `no_response` are reachable
only through them, and a rendered graph draws them.

> [!WARNING] A direct write isn't judged
> A Flow that writes a stored Column itself skips the engine's judgement of
> the move. A value that isn't a declared State leaves the Row out of
> projection: `feature.state.project` reports it as `unknown_state` and
> writes nothing for it. Keep the values a Flow writes to the graph's own
> names, and hold the Rows to the graph with `feature.state.check` (see
> [Check it](#check-it)).

A template that wants the engine to judge each move fires the Event
instead, with `feature.state.transition`. Questionnaire's `check_recipient`
doesn't; if it did, giving up would be:

```yaml title="check_recipient.yaml"
- id: give_up
  activity: feature.state.transition
  args:
    event: world.gave_up
    record_ids: [$inputs.record_id]
```

Then an illegal move is refused, as an Action is, rather than written.

`create_rows` and `update_row` refuse a state Column, so neither your
assistant nor the Routine's [Agent](https://docs.popcorn.ai/agent.md) can
set `Stage` or `Status` by hand. A person moves a recipient with an Action.

## How an Action runs

A press of a button, in Popcorn or through `take_action`, starts the Bundle
Flow named `cta_apply` with the Action's `action`, the Rows' `record_ids`
and a `payload`. Questionnaire's is two Steps:

```yaml title="cta_apply.yaml"
name: cta_apply
version: 1
inputs:
  action: { type: string }
  record_ids: { type: array }
  payload: { type: object, default: {} }

steps:
  - id: apply
    activity: feature.state.transition
    timeout_seconds: 120
    on_error: { policy: fail, retry: 0 }
    args:
      event: $inputs.action
      record_ids: $inputs.record_ids
      payload: $inputs.payload
      operation_key: $trigger.run_id
      conversation_id: $trigger.conversation_id

  - id: refused
    when: "$steps.apply.output.applied == 0"
    activity: foundation.workflow.fail
    args:
      code: $steps.apply.output.first_refusal.code
      reason: $steps.apply.output.first_refusal.reason

outputs:
  applied: $steps.apply.output.applied
  refused: $steps.apply.output.refused
  results: $steps.apply.output.results
```

`action` arrives as the bare Event name, `ask_again`, and the engine finds
it in the `staff` family. For each Row it reads `Stage`, finds the one
legal edge, and writes, in one patch at the Row's read-time revision:

- the edge's `writes`, here `Follow Ups: 0` and `Last Asked: null`;
- the landing State in `Stage`, here `waiting`;
- the recomposed `Status`, `Why` and `CTAs`.

A Row changed since it was read comes back refused as `StaleRev`, and
nothing overwrites it. Each applied edge records a change on the Row in its
[History](https://docs.popcorn.ai/history.md), with the Transition's
`description` as the line: "Asked again, with the follow-ups starting
over". Nothing is sent here. A recipient asked again is followed up by the
next pass, because a blank `Last Asked` is due at once.

> [!IMPORTANT] The name is fixed
> Popcorn and `take_action` both start the Flow by the literal name
> `cta_apply`, with those three inputs. A Publish refuses a Bundle whose
> staff Transitions carry `cta:` buttons and that has no `cta_apply` Flow:
> see [the Publish checks](#the-publish-checks).

### Take one from your assistant

> "Jane answered at standup. Mark Jane as answered."

> [!TIP] MCP tool call
> Your assistant calls `list_rows` to find Jane's Row, `list_actions` to
> see what it offers, then `take_action`.

`list_actions` reads the Row's `CTAs` Column, the buttons the last
projection offered, and names the Status each one lands on. An assistant
can take only an Action that a press completes: `route: deterministic`
with `ui: button`, which all three of Questionnaire's are. Others are
listed and marked "in Popcorn", and `take_action` refuses them.

## The guard that keeps an Action from landing under a pass

`ask_recipient` and `check_recipient` start by claiming the Row: they hold
`Sending` as a [Row lease](https://docs.popcorn.ai/row-leases.md) until
their Run ends. Meanwhile they decide from the Row as the claim read it.
An Action that landed in that window would be overwritten when the pass
writes `Stage`, so every Action carries `not_held`:

```yaml title="manifest.yaml"
  guards:
    not_held:
      all: [{column: Sending, empty: true}]
      code: RecipientBusy
      message: A pass is emailing or checking this recipient; try again once it has finished.
```

The guard is judged when the Action is taken, against the Row as it is
then. The buttons were projected earlier, so a held Row may still show
them, and a press while it is held is refused. Closing a recipient a pass
is checking reads:

```text
staff.close is not legal here: A pass is emailing or checking this recipient; try again once it has finished.
```

`cta_apply` fails the Run with that reason and the guard's code,
`RecipientBusy`. A Row on a State no edge of the Event leaves gets the
edge's States instead, as in `staff.close is not legal here: recipient is
answered`. Since the claim and the lease's release are both writes to a
Column the guard reads, the Actions disappear when a pass claims the Row
and come back when its Run ends.

> [!TIP] Give a guard words
> Without `code:` and `message:`, a refusal reads `guard not_held refused`
> with the code `NoEdge`. `take_action` quotes the message when it
> explains why an Action isn't offered.

## Adopting Rows from before the States tier

Questionnaire added `states:` in 0.2.0. Before that, its Flows wrote the
recipient's state straight into `Status`, and there was no `Stage`. A
Routine upgraded from 0.1.x has Rows with a `Status` such as `waiting` and
a blank `Stage`, which would read as `new` and be asked again.

The template carries them over itself, on the first pass after the
upgrade. Its code block's `plan` operation lists every Row that has a
`Status` it knows, no `Stage`, and no `CTAs`. A Row with no `CTAs` has
never been projected, so its `Status` was written by the old Flows and is
a fact. Once projected, a Row's `Status` is the projection's and is never
read back. The tick writes each one's `Stage` before it asks or checks
anyone:

```yaml title="questionnaire_tick.yaml"
  - id: adopt
    foreach: $steps.plan.output.adopt
    as: row
    max_parallel: 3
    on_error: { policy: skip }
    activity: foundation.store.patch_row
    args:
      conversation_id: $inputs.conversation_id
      table_name: recipients
      record_id: $row.record_id
      patch:
        Stage: $row.stage
      change_kind: questionnaire_stage_adopted
      change_action: Carried the recipient's Status into Stage
```

On every later pass the list is empty. The pass's last Step projects every
Row, adopted ones included.

> [!NOTE] Nothing adopts for you
> Publish judges the graph, not the Rows a Routine already holds. A
> template that moves existing Rows onto a States tier, or drops a State
> some Row is on, has to move those Rows itself, as Questionnaire does.

## Announce a change to the graph

Popcorn's own templates name every change to the graph in their changelog
with the words `STATE CHANGE`. Questionnaire's 0.2.0 entry begins:

```yaml title="manifest.yaml"
changelog: >-
  0.2.0 — STATE CHANGE: a recipient's state moves to a new `Stage` column
  and `Status` becomes its projection, declared as a `states:` graph, so
  No response is a Review with three Actions: …
```

A change to the edges alone is announced the same way. The 0.3.0 entry
says `STATE CHANGE, to edges only (no state is added, renamed or
removed)`, then what moved.

A check in Popcorn's own repository refuses a change to a template's
`states:` section, or its removal, without that sentence, so a State added,
renamed or dropped is something a reviewer reads rather than a line inside
a YAML block. Nothing checks a Copy's changelog. Write the sentence anyway:
it is what tells the people on your Copy that their Rows can show
something new.

## Change the graph: add a Snoozed State

> "In my questionnaire Copy, add a Snoozed state: a waiting recipient can
> be snoozed so nobody follows up, and resumed later."

> [!TIP] MCP tool call
> Your assistant calls `list_routine_files` and `read_routine_file` for
> `manifest.yaml`, then `create_routine_version` without `confirm` to
> check the change, and again with `confirm=true` once you agree.

The change is the State, two Events and two Transitions:

```yaml title="manifest.yaml"
      states:
        # … new, waiting, answered, no_response, closed as before
        snoozed:
          label: Snoozed
          tone: gray
          why: Snoozed by a person; nobody follows up until it is resumed.
  events:
    staff: [ask_again, mark_answered, close, snooze, resume]
    world: [asked, answered, gave_up, restarted]
  transitions:
    # … the existing Transitions
    - on: staff.snooze
      from: waiting
      to: snoozed
      guard: [not_held]
      expected: true
      description: Snoozed by a person
      cta: {kind: snooze, label: Snooze, prominence: quiet}
    - on: staff.resume
      from: snoozed
      to: waiting
      guard: [not_held]
      expected: true
      description: Resumed, followed up when due
      cta: {kind: resume, label: Resume}
```

No Flow changes. Questionnaire's `plan` asks only Rows with a blank
`Stage` and checks only `waiting` ones, so a snoozed recipient is left
alone until Resume puts them back to `waiting`. A State your Flows must
act on needs its Flows or code block changed too. The Manifest's
`agent_summary` lists the Stage values for the Routine's Agent, so add
`snoozed` there as well.

A dry run of this change with a step missing fails one check at a time.
These are the errors in the order a first draft usually meets them:

```text
states: 'recipient': no edge reaches ['snoozed']; a state nothing enters is either dead or missing its world event
states: 'recipient': no expected edge enters ['snoozed']; mark the edge that is the normal way in with expected: (an `also:` needs a when: [{machine: recipient, …}] naming where it leaves)
states: recipient.snoozed has no way out and is not terminal
```

The first is the State with no Snooze edge, the second the Snooze edge
without `expected: true`, the third Snooze without Resume. Then bump
`version:` and say what changed:

```yaml title="manifest.yaml"
version: "0.4.0"
changelog: >-
  0.4.0 — STATE CHANGE: a new Snoozed state. Snooze stops following up on
  a waiting recipient, and Resume puts them back to Waiting.
  …
```

> [!WARNING] Every Routine on the Copy
> A new Version reaches every Routine on the Copy, not only the one you
> asked about. The dry run says which.

## Design the machines

Questionnaire needs one machine. A graph that tracks more than one thing
about a Row adds machines, and these rules decide how.

**One Funnel, then Overlays.** The Funnel is the milestone that moves
forward, as `recipient` does. An Overlay is something true *alongside* it:
blocked, parked, waiting on a side document. Test each candidate State:
can it hold at the same time as a Funnel State? If it can, it belongs in an
Overlay, declared with `overlay: true`. An Overlay has an implicit `none`
State, which you never declare. The first machine without `overlay: true`
is the primary, and Status shows it when no Overlay is set.

**Declaration order is precedence.** With no `status.compose` rules, Status
shows the first Overlay, in declaration order, that is not `none`. Declare
the one that matters most first.

**Where each value comes from:**

| Shape | Declared as | Its value comes from | Moves by |
|---|---|---|---|
| stored | `column: Stage` | the Column | a Transition, or a Flow writing the Column |
| derived | no `column` | the Bundle's code, handed in per Row | the Bundle's derivation changing |
| mirror | `column:` plus `derive: true` | the Bundle's code; the engine writes it into the Column | the same, recorded in a Column clients can read |

`recipient` is stored. A derived value reaches the engine as `machines`,
keyed by each Row's id as a string, on `feature.state.project`,
`feature.state.transition` and `feature.state.check`:

```yaml
machines: {"12": {blocker: missing_info}, "13": {blocker: none}}
```

A `patch_rows … project_states: true` write from `foundation.code.execute`
can carry the same per Row, as `states: {machines: {blocker: missing_info}}`
on its patch. A machine left out reads as its Column, or as its initial
State. A stored machine can't be supplied: its value is its Column, and a
caller that could hand one in could make an illegal edge legal. The Step
fails with `MachinesInvalid`:

```text
machines: stored machines ['recipient'] are read from their columns, not supplied
```

A mirror suits a value that is computed but must still be readable as a
Column, for filtering or for a client. Its Column belongs to the
projection, as `Status` does, and a Bundle write to it is refused. A
derived machine still needs its edges, as Questionnaire's `world` edges
are needed: the checks walk Transitions, and a rendered graph draws them.

**The initial State is the first one declared** unless `initial:` names
another. Questionnaire names `new` explicitly. Without that, a tool that
sorts YAML keys would make `answered` the initial State, and the graph
would fail:

```text
states: 'recipient': no edge reaches ['closed', 'new', 'no_response', 'waiting']; a state nothing enters is either dead or missing its world event
```

An Overlay's initial State is `none`.

## The keys

### States

| Key | Meaning |
|---|---|
| `label` | the chip text; the State name humanised when absent |
| `tone` | `green`, `red`, `gray` or `black` |
| `warn` | the chip is a warning, and a Row showing it is a work item |
| `terminal` | `true`: only a `system` Event may leave it. `reopenable`: an ending a later Event may undo |
| `stored_as` | the Column value when it is not the State name |
| `why` | the default Why while a Row shows this State |
| `why_from` | a Column whose text is the Why while a Row shows this State, ahead of `why` |
| `work_item` | overrides `warn` for the worklist: `true` opens an item without warning, `false` warns without one |
| `error` | a Row showing it stopped because something went wrong, not for a decision |
| `detail` | `{column, values, labels, tone}`: a qualifier Column for this State, one State with many reasons, that an edge landing here may stamp |

State names may not contain `,`, `;` or `|`, and labels may not contain
`;`, `:` or `|`: those are the display hint's separators. `groups:` names
sets of States, and `from:` and the predicates accept a group wherever they
accept a State.

### Events

`events:` maps a family to its Event names. Two families mean something to
the platform:

- `staff` Events are people's decisions. Only a `staff` edge may carry a
  `cta:`, so these are the buttons.
- `system` Events are the only ones that may leave a `terminal: true`
  State. Keep them for corrections the Bundle's own machinery makes, never
  for a decision.

Every other family name is yours; Questionnaire's `world` is the usual one.
A Transition names its Event as `family.event`, and
`feature.state.transition` also takes the bare name when only one family
has it. A bare `on:` key is safe: YAML reads it as `true`, and the parser
turns it back.

### Transitions

| Key | Meaning |
|---|---|
| `on` | `family.event` |
| `from` | a State, a group, a list of them, or `*`; qualify as `hold.none` when the name is ambiguous |
| `to` | one State; several, when a Flow decides; or `same` |
| `expected` | `true`, or the list of `from` States it is the normal move out of |
| `writes` | Column → literal, written when the edge lands; `null` empties a Column |
| `payload_writes` | Column → payload key, from the Event's `payload` |
| `also` | other machine → State, moved at the same time |
| `when` | predicates on the Row and the tuple; all must hold |
| `guard` | named guards; all must hold |
| `cta` | the button, on `staff` edges only |
| `flow` | a Bundle Flow that *is* the edge; the edge writes nothing itself |
| `then` | Bundle Flows to launch per Row after the writes land |
| `effects` | names of Bundle-side work, echoed back per applied Row |
| `detail` / `detail_from` | the landing State's detail value, literal or from that payload key; the landing State must declare `detail:` |
| `importance` | 1–10, how loudly a client draws the edge; display only. An int, or a map of source State to rank with an optional `default` |
| `review` | `true` lists the button among a Review's choices on the Steps list though it also leaves a Step; display only. See [Which States are Steps](https://docs.popcorn.ai/state-machine.md#which-states-are-steps) |
| `description` | the line the Row's History records when the edge lands |

The machine is inferred: a qualified reference names it, or else it is the
one machine that owns every `from`. When that is ambiguous, Publish says
`cannot infer its machine … set machine:`, and a `machine:` key settles it.

**`expected:` marks the normal way in, not the likely one.** Every State
but the initial needs one. All three of Questionnaire's Actions are
expected, and so are three of its four `world` edges; `world.restarted` is
not, because `new` is the initial State and needs no way in.

**`importance:` is all or nothing.** A graph ranks every edge or none. With
none, an expected edge draws at 6 and the rest at 3.

**`to: same`** records something without moving the machine, such as a
nudge. It may write other Columns, but not its own machine's, and it
counts as neither a way in nor a way out for the checks.

**`flow:` and `then:`** hand work to the Bundle, and Questionnaire uses
neither. A `flow:` edge is legal like any other, but
`feature.state.transition` writes nothing for it and returns the Flow to
launch, whose own writes move the Row. That is how a staff edge can land on
more than one State. From a document-sending graph:

```yaml title="manifest.yaml"
- on: staff.send
  from: draft
  to: [sent, failed]
  expected: true
  flow: send_document
  cta: {kind: send, label: Send}
- on: staff.retry
  from: failed
  to: draft
  writes: {Send Error: ""}
  then:
    - flow: send_document
      inputs: {record_id: $record_id, reason: $payload.reason}
  cta: {kind: retry, label: Try again}
```

A `then` input is a literal, `$payload.<key>`, `$row.<Column>` (read after
the writes), `$record_id` or `$conversation_id`, and an entry may carry
its own `when:`. The Activity does not start either kind of Flow: it
returns them as `launches`, and `cta_apply` must start them (see
[When edges launch Flows](#when-edges-launch-flows)).

### The button

`cta:` takes `kind` and `label`, which are required, and optional `ui`
(`button`, the default, `input`, `contact-picker`, `contact-form` or
`signing-modal`), `prominence` (`primary` or `quiet`), `route`
(`deterministic`, the default, `agent` or `noop`), `direct_only`,
`message` and `when`. One `kind` belongs to one Event. `message` is the
chat line, templated on Columns as `{Name|this recipient}`, as
Questionnaire's are.

A button's `when` can offer *less* than the edge allows. It may use a
`shown: true` predicate on the displayed Status, which a guard may not. An
Event with more than one legal edge for a Row is not offered at all,
because the press would be refused as `Ambiguous`.

### Status

| Key | Default | Meaning |
|---|---|---|
| `column` | `Status` | the projected chip |
| `ctas_column` | `CTAs` | the offered buttons; `null` for none |
| `why_column` | `Why` | the reason; `null` for none |
| `sub` | none | a machine Column a client shows under the chip |
| `compose` | none | precedence rules, first match wins |
| `row_ctas` | `all` | `unless_warn` leaves a warning Row's buttons to its worklist item |
| `worklist` | none | an action-item Table the projection keeps |

The defaults are Columns too, so a `states:` section with no `status:` key
still needs `Status`, `CTAs` and `Why` on its Table. Questionnaire spells
all three out.

`compose` overrides the overlay fall-through. A rule's `show:` names a
machine, meaning its current State, or a literal State, and may carry its
own `why`:

```yaml title="manifest.yaml"
status:
  compose:
    - when: [{machine: review, in: [approved, declined]}]
      show: review
```

With an unconditional rule, every machine no rule shows drops out of the
Status vocabulary. `worklist: {table: issues, key: cause}` keeps one open
Row per Row whose shown Status is a work item; the worklist Table must
declare every Column the reconcile writes (`cause`, `Issue`, `Stage`,
`Why`, `ctas`, `Status`, `Opened`, `Resolved` and `affected_record_ids`,
or the names set on `worklist:`).

### Guards

A guard is `all:` or `any:` of predicates, and a bare list means `all:`,
as `not_held` shows. Each predicate names one subject and one operator:

| Subject | Operators |
|---|---|
| `column: X` | `empty: true` or `false`, `equals:`, `in:`, `not_in:` (case-insensitive) |
| `machine: M` | `is:`, `in:`, `not_in:` (States or groups), `group:` |
| `guard: G` | none; add `holds: false` to negate |
| `shown: true` | `is:`, `in:`, `not_in:`, on a button's `when:` only |

A guard may build on another guard, but not on itself through a cycle.

**A Routine Setting.** `{scalar: <key>, equals: <value>}` holds while that
[Scalar](https://docs.popcorn.ai/scalar-tiers.md) equals the value, unset
reading as `""`. The engine reads it once per call. Use it for a switch
that gates an edge.

**External guards** are rules only the Bundle's code can answer, such as a
budget lookup. Declare one as `{external: true, description: …}` so the
graph still shows it. The platform never evaluates it: the caller vouches
for it per Row, by passing `guards: {"12": [budget_ok]}` to
`feature.state.transition` or `feature.state.project`. An edge behind one
that wasn't vouched for is refused for that Row
(`external guard budget_ok was not vouched for`), and a result that relied
on one carries `delegated: true`. Vouching for a guard the platform
evaluates fails with `guards: ['not_held'] are not external guards of this
graph`.

## When edges launch Flows

Questionnaire's `cta_apply` is the whole of it because its machine is
stored and its edges launch nothing. A graph with a derived machine, or
with `flow:` and `then:` edges, needs two more Steps. This one is from a
template that reviews requests, with a derived `blocker` machine:

```yaml title="cta_apply.yaml"
steps:
  - id: derive
    activity: foundation.code.execute
    on_error: { policy: fail, retry: 0 }
    args:
      code_name: request_rules
      reads:
        - { type: get_records, name: rows, table_name: tracker,
            record_ids: $inputs.record_ids, missing_ok: true }
      inputs: { op: machines }
  - id: apply
    activity: feature.state.transition
    on_error: { policy: fail, retry: 0 }
    args:
      event: $inputs.action
      record_ids: $inputs.record_ids
      payload: $inputs.payload
      machines: $steps.derive.output.machines
      operation_key: $trigger.run_id
      conversation_id: $trigger.conversation_id
  - id: launch
    foreach: $steps.apply.output.launches
    as: launch
    activity: foundation.workflow.start_flow
    on_error: { policy: skip, retry: 0 }
    args:
      conversation_id: $trigger.conversation_id
      flow_name: $launch.flow
      inputs: $launch.inputs
  - id: refused
    when: "$steps.apply.output.applied == 0 && $steps.apply.output.launch == 0"
    activity: foundation.workflow.fail
    args:
      code: $steps.apply.output.first_refusal.code
      reason: $steps.apply.output.first_refusal.reason
```

`derive` exists because the Transition recomposes Status after the edge
lands, and a derived machine left out of `machines` reads as its initial
State, so a press would clear a warning the facts still support. `launch`
starts what the edges returned, and `launch` in the last Step counts the
Rows whose edge is a Flow, which is not a refusal. The Bundle's own
`writes` input to `feature.state.transition` may not touch the projection
Columns:

```text
writes for record 12 touch projection columns ['Status']; the engine writes them from the tuple
```

## The Publish checks

Each check refuses the Publish with one message, prefixed `states:`. The
ones with Questionnaire's names were produced from variants of its graph.

**Every State must be reachable** from the initial State, and **every State
but the initial needs an `expected:` edge in**. An `also:` counts only when
its Transition's `when:` names the machine and State it leaves from. See
[the Snoozed change](#change-the-graph-add-a-snoozed-state) for both
messages.

**A State with no way out must be terminal**, except in an Overlay, which
may stay set until it clears:

```text
states: recipient.snoozed has no way out and is not terminal
```

**Only `system` leaves a `terminal: true` State.** A Resume from `closed`:

```text
states: recipient.closed is terminal but ['staff.resume'] leave it
```

Declare the State `terminal: reopenable` if people may undo the ending.

**One `cta.kind`, one Event:**

```text
states: cta kind 'ask-again' is used by both 'staff.ask_again' and 'staff.resume'
```

**Only a `staff` edge carries a button:**

```text
states: 'world.asked' carries a cta but is not a staff event
```

**`review: true` lists a button among a Review's choices**, so it needs a
`cta:`, an edge of the first machine, and a Review among its `from:`
States. Questionnaire's Close without `no_response` in its `from:`:

```text
states: transition on 'staff.close' sets review: true but its from: ['new', 'waiting'] names no Review (a warn: true state that is neither terminal nor a Step with policy.chase or policy.step); add the Review to from: or drop review
```

**No two machines share a State name**, because Status holds their union:

```text
states: state 'received' is declared by both 'review' and 'blocker'; the Status vocabulary is their union
```

**Staff edges do something and land somewhere definite.** A button that
moves only a derived machine would be undone by the next derivation, so it
must write a fact, launch a Flow or declare an effect; and a staff edge
lands on one State unless a `flow:` decides:

```text
states: staff edge 'staff.dismiss' moves only the derived machine 'blocker' and writes nothing; add writes, a flow, a then or an effect
states: staff edge 'staff.decline' must land on one state unless a flow decides the outcome
```

**A `same` edge does not write its own Column:**

```text
states: 'staff.snooze' is a `same` edge but writes its own column 'Stage'; say where it lands
```

**`importance:` ranks every edge or none**, and a map covers every `from:`
State or carries `default:`:

```text
states: importance ranks every edge or none; unranked: ['staff.reopen']
states: transition on 'staff.decline' ranks no importance from ['received']; name them or add default:
```

**A detail stamp needs a landing State that declares one, and `also:`
names other machines:**

```text
states: transition on 'staff.decline' stamps a detail but its landing state declares none
states: transition on 'staff.decline': also names its own machine 'review'; that is what to: is for
```

**A guard's `shown:` predicate belongs on a button's `when:`, and a
predicate can't name an external guard:**

```text
states: guard 'shows_hold': a shown predicate belongs on a cta's when: only what a row displays decides what a person is offered
states: guard 'can_approve': predicate names external guard 'budget_ok'; only the bundle can evaluate it — vouch for it instead
```

**Transition Flows must be in the Bundle.** Every `flow:` and `then:` names
a Flow the Bundle installs:

```text
states: transitions name flows ['notify_requester'] that this bundle does not install (flows: ['cta_apply'])
```

**The Table declares every Column the tier touches.** The graph needs
`tables:`, and its Table must declare the Status, CTAs and Why Columns,
every stored machine Column, every `writes` and `payload_writes` Column,
and every Column a predicate reads. Questionnaire without `Last Asked`, and
then without `Sending`:

```text
states: a tables: section declaring its table is required
states: table 'recipients' lacks columns ['Last Asked'] the states tier writes
states: predicates read columns ['Sending'] that table 'recipients' does not declare
```

The predicate check exists because a missing Column reads blank on every
Row, which would make `not_held` always hold.

**Drop hand-written `display:` hints.** The tier renders them, and a
Column carrying a different one fails:

```text
states: column 'Stage' carries display hint 'status:new,waiting,answered,no_response,closed' but the states tier renders 'status:new,waiting,answered,no_response,closed;warn=no_response;labels=new:Not asked yet|waiting:Waiting|answered:Answered|no_response:No response|closed:Closed;tone=new:gray|answered:black|closed:gray'; drop the literal or change the spec
```

A template moving from hand-kept hints onto the tier deletes them; there
is no need to copy the rendered value back in.

### Checks once the graph parses

Two more checks run on a graph that parses, beside the Table check. A dry
run lists everything they find at once, each under its rule's name, and
the message opens `manifest.yaml states:`, or names the Recipe's file.

**`transition_write_type`: a Transition's `writes` must be a value the
store takes for the Column as declared**: its type, a number or datetime
`format`, and `required: true`. Otherwise every press of the button would
fail after it was offered. An edit to Questionnaire's Ask again that
empties `Last Asked` with `''` rather than `null`:

```text
manifest.yaml states: transition staff.ask_again (from no_response) writes 'Last Asked': '', which the store refuses for table 'recipients' (Last Asked: not a valid ISO 8601 datetime). Write null to empty it: writes: {Last Asked: null}.
```

**`cta_apply_missing`: a Bundle with buttons ships `cta_apply`.** Every
staff Transition with a `cta:` runs it when pressed:

```text
manifest.yaml states: transitions ['staff.ask_again', 'staff.close', 'staff.mark_answered'] carry cta: buttons, and pressing one (in the app or through take_action) runs this bundle's cta_apply flow, which the bundle does not have. Add cta_apply.yaml at the bundle's root, taking inputs action, record_ids and payload and applying them with feature.state.transition; or remove the cta: keys.
```

One more is a warning, which a Publish accepts.
**`states_steps_unlisted`**: the primary machine has a Review, a State
with `warn: true` that isn't terminal, and no State carries a
`policy: {step: …}` marker, so `get_routine` lists no
[Steps](https://docs.popcorn.ai/steps.md) and the Reviews appear in no
Steps list. Questionnaire's `waiting` carries one, so it doesn't warn.

## A Recipe instead of `states:`

Questionnaire's graph is fixed by its Version: every Routine on that
Version runs the same one, and changing it is a Publish. A
[Recipe](https://docs.popcorn.ai/state-machine.md#the-recipe-a-graph-each-routine-can-replace)
holds the same keys in `recipe.yaml` at the Bundle's root, declared by
`recipe:` in the Manifest, and each Routine can install a revision of its
own. That is what lets an assistant change a Routine's
[Steps](https://docs.popcorn.ai/steps.md) with `change_routine`, which
refuses a Routine whose template declares no `recipe:`.

A template declares one or the other. A Recipe adds checks of its own:

```text
recipe: a bundle declares states: or recipe:, not both
recipe: the bundle ships no recipe.yaml at its root
recipe.yaml is present but the manifest declares no recipe: section
recipe: a tables: section declaring the graph's table is required
```

And a Recipe whose graph opens action items, through a State that warns,
must let every item stop tracking its Row, with a `tracking` Overlay and a
`staff.stop_tracking` edge. A `states:` section has no such check:

```text
recipe.yaml: the recipe opens action items (missing_info) but declares no staff.stop_tracking transition with a `cta: {kind: stop-tracking}`; every action item must be able to stop tracking its row (e.g. `on: staff.stop_tracking`, `from: tracking.none`, `to: not_tracking`, `cta: {kind: stop-tracking, prominence: quiet, direct_only: true}`)
```

The engine offers that button on every action item whose edge is legal,
whatever its `when:` says.

## Check it

A Publish that passes proves **structure**: every reference resolves,
every State is reachable with an expected way in, no Funnel State is a dead
end, terminals hold, and the Table declares what the tier touches. It does
not prove **intent**, which is still yours to check:

- **Events nothing fires.** Questionnaire's `world` edges pass every check,
  and nothing fires them: its Flows write `Stage`, and only its claims'
  `when_legal` reads them. That is by design there.
  In your own graph, search the Flows for each non-staff Event and for
  every value they write to a stored Column.
- **Terminals reached too early.** Mark answered leaves `new`, so a
  recipient can be marked answered before they are asked. Read each
  terminal's incoming edges as a list of every way a Row can end there.
- **Buttons that never show.** A guard on a Column nothing clears, or a
  button `when:` that can't hold, publishes fine and offers nothing.

`feature.state.spec` returns the graph a Run judges Rows by, with a Mermaid
diagram per machine and a `spine` of the expected edges alone, which is
quick to read against what you meant. For a `states:` section it is the
Version the Routine is bound to; for a Recipe, the revision the Run pinned.
`feature.state.check` holds every Row to the graph: each stored value must
be a declared State, each mirror must agree with the value the Bundle
supplies, and each Status must be what its tuple composes to. With
`fail_step: true`, any offender fails the Step as `StatesOutsideGraph`,
which makes it a test Flow's assertion.
