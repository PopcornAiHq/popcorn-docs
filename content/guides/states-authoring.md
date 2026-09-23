---
id: states-authoring
title: Authoring a states tier
summary: >
  Writing a bundle's `states:` section end to end: stored, derived and
  mirrored machines; states, events, transitions and buttons; guards; and the
  flows that fire an edge, which must start its `flow` and `then` launches
  themselves. Every publish check is listed with its exact error — `no
  expected edge enters`, `lacks columns … the states tier writes`, a terminal
  left by staff — and its fix.
concepts: [state-machine, manifest-keys, app-bundle]
applies_to: [cli, mcp, human]
source: [StatesSpec, parse_states, render_hints_into_tables, project_row, compose_shown, projection_columns, state_transition, state_project]
---

This guide takes one `states:` section from design to a published, wired
graph. What a state machine *is* — the tuple, the projection, why a button is
an edge — is [the state machine](https://docs.popcorn.ai/concepts/state-machine.md),
and where the two overlap that page is authoritative.

The loop is the ordinary one from
[authoring a channel template](https://docs.popcorn.ai/guides/template-authoring.md):
edit `manifest.yaml`, `popcorn app publish`, read the error, repeat. One thing
is different. `popcorn template check` does not look inside `states:`; the
graph is checked only when the server parses the manifest at publish. The
check stops at the first problem, so a new graph usually takes several
publishes to pass, one error at a time.

## The worked example

A tracker of requests that someone reviews. Most `states:` blocks later in
this guide are changes to it, and every one was parsed by the engine.

```yaml
tables:
  tracker:
    columns:
      - {name: Title, type: string}
      - {name: Owner, type: string}
      - {name: Decision, type: string}
      - {name: Decision Note, type: string}
      - {name: Stage, type: string}
      - {name: Hold, type: string}
      - {name: Status, type: string}
      - {name: CTAs, type: json}
      - {name: Why, type: string}

states:
  table: tracker
  status: {column: Status, ctas_column: CTAs, why_column: Why}
  machines:
    review:
      column: Stage
      states:
        received: {label: Received}
        in_review: {label: In review}
        approved: {label: Approved, tone: green, terminal: true}
        declined: {label: Declined, tone: gray, terminal: reopenable}
      groups: {open: [received, in_review]}
    blocker:
      overlay: true
      states:
        missing_info: {label: Missing information, warn: true}
    hold:
      column: Hold
      overlay: true
      states:
        on_hold: {label: On hold, tone: gray}
  events:
    staff: [start_review, approve, decline, reopen, hold, release]
    world: [withdrawn, info_missing, info_received]
  guards:
    has_owner: [{column: Owner, empty: false}]
  transitions:
    - on: staff.start_review
      from: received
      to: in_review
      expected: true
      cta: {kind: start-review, label: Start review}
    - on: staff.approve
      from: in_review
      to: approved
      expected: true
      guard: [has_owner]
      writes: {Decision: approve}
      cta: {kind: approve, label: Approve}
    - on: staff.decline
      from: open
      to: declined
      expected: [in_review]
      writes: {Decision: decline}
      also: {hold: none}
      cta: {kind: decline, label: Decline, prominence: quiet}
    - on: staff.reopen
      from: declined
      to: in_review
      writes: {Decision: ""}
      cta: {kind: reopen, label: Reopen}
    - on: staff.hold
      from: hold.none
      to: hold.on_hold
      expected: true
      when: [{machine: review, group: open}]
      cta: {kind: hold, label: Put on hold}
    - on: staff.release
      from: hold.on_hold
      to: hold.none
      cta: {kind: release, label: Release}
    - on: world.withdrawn
      from: open
      to: declined
      writes: {Decision: withdrawn}
      payload_writes: {Decision Note: note}
      also: {hold: none}
    - on: world.info_missing
      from: blocker.none
      to: blocker.missing_info
      expected: true
    - on: world.info_received
      from: blocker.missing_info
      to: blocker.none
```

It has three machines. `review` is the funnel, stored in `Stage`. `blocker`
is an overlay with no column, so the bundle's own code decides it from the
row's facts. `hold` is an overlay stored in `Hold`. Publish renders display
hints onto `Status`, `Stage` and `Hold`. The one on `Status` lists the whole
vocabulary and marks `missing_info` as a warning:

```text
status:received,in_review,approved,declined,missing_info,on_hold;warn=missing_info;labels=…;tone=…
```

A row in review, with an owner and nothing blocking it, shows `in_review` and
offers Approve, Decline and Put on hold. Put it on hold and it shows `on_hold`.
Now Approve is still offered but Put on hold is not, because its edge leaves
only `hold.none`.

## 1. Design the machines

**One funnel, then overlays.** The funnel is the milestone that moves
forward. An overlay is something true *alongside* it: blocked, parked,
waiting on a side document. An overlay has an implicit `none` state, and you
never declare it. Test each candidate state against this: can it hold at the
same time as a funnel state? If it can, it belongs in an overlay. The first
machine with no `overlay: true` is the **primary**. When no overlay is
active, Status shows the primary.

**Declaration order is precedence.** With no `status.compose` rules, Status
shows the first overlay, in declaration order, that is not `none`. The
example declares `blocker` before `hold`, so a row that is held *and* missing
information shows the warning, not the parking.

**Where each value comes from:**

| Shape | Declared as | Its value comes from | Moves by |
|---|---|---|---|
| stored | `column: Stage` | the column | events: the engine writes the column when an edge lands |
| derived | no `column` | the bundle's code, handed in per row | the bundle's derivation changing |
| mirror | `column:` plus `derive: true` | the bundle's code; the engine writes it into the column | the same, recorded in a column clients can read |

A derived value reaches the engine as `machines`, keyed by record id as a
string. That input goes to `feature.state.project`,
`feature.state.transition` and `feature.state.check`:

```yaml
machines: {"12": {blocker: missing_info}, "13": {blocker: none}}
```

A block can also carry the value on its own row patch. In a
`patch_rows … project_states: true` write from `foundation.code.execute`,
each patch carries `states: {machines: {blocker: missing_info}}` for its own
row. A machine you leave out reads as its column, or as its initial state. A
stored machine cannot be supplied: its value is its column, and a caller that
could hand one in could make an illegal edge legal. The step fails with
`MachinesInvalid`:

```text
machines: stored machines ['review'] are read from their columns, not supplied
```

A mirror suits a value that is computed but must still be readable as a
column, for filtering or for a client:

```yaml
machines:
  payment:
    column: Payment
    derive: true
    states:
      unpaid: {label: Unpaid}
      paid: {label: Paid, tone: green, terminal: true}
```

A mirror's column belongs to the projection, the same as `Status`. A bundle
patch that writes it is refused.

**A derived machine still needs edges.** The graph checks walk transitions,
so `blocker` declares `world.info_missing` and `world.info_received` even
though nothing fires them. The bundle simply starts supplying
`missing_info`. The edges say how the value moves, and they are what a
rendered graph draws.

**The initial state is the first one declared** unless `initial:` names
another. Put the entry state first, and keep that order in any tool that
rewrites YAML: one that sorts keys changes the initial state without a
word. An overlay's initial state is `none`.

## 2. States, events, transitions and status

### States

| Key | Meaning |
|---|---|
| `label` | the chip text; the state name humanised when absent |
| `tone` | `green`, `red`, `gray` or `black` |
| `warn` | the chip is a warning, and a row showing it is a work item |
| `terminal` | `true`: only a `system` event may leave it. `reopenable`: an ending that a later event may undo |
| `stored_as` | the column value when it is not the state name |
| `why` | the default Why prose while a row shows this state |
| `work_item` | overrides `warn` for the worklist: `true` opens an item without warning, `false` warns without one |

State names may not contain `,`, `;` or `|`, and labels may not contain `;`,
`:` or `|`. Hints are built from both, and those characters are the hint's
separators. `groups:` names sets of states. `from:` and the predicates accept
a group wherever they accept a state.

### Events

`events:` maps a **family** to its event names. Two family names mean
something to the platform:

- `staff` events are people's decisions. Only a `staff` edge may carry a
  `cta:`, so these are the buttons.
- `system` events are the only ones allowed to leave a `terminal: true`
  state. Keep them for corrections the bundle's own machinery makes, such as
  a failed step that has to move a finished row, never for a decision.

Every other family name is yours; `world` and `agent` are the usual ones. A
transition names its event as `family.event`. `feature.state.transition`
also accepts the bare event name when only one family has it, which is how
a button's `action` arrives. A bare `on:` key is safe. YAML reads it as the
boolean `true`, and the parser turns it back.

### Transitions

| Key | Meaning |
|---|---|
| `on` | `family.event` |
| `from` | a state, a group, a list of them, or `*`; qualify as `hold.none` when the name is ambiguous |
| `to` | one state; several, when a flow or a written value decides; or `same` |
| `expected` | `true`, or the list of `from` states it is the normal move out of |
| `writes` | column → literal, written when the edge lands |
| `payload_writes` | column → payload key, from the event's `payload` |
| `also` | other machine → state, moved at the same time |
| `when` | predicates on the row and the tuple; all must hold |
| `guard` | named guards; all must hold |
| `cta` | the button, on `staff` edges only |
| `flow` | a bundle flow that *is* the edge; the edge writes nothing itself |
| `then` | bundle flows to launch per row after the writes land |
| `effects` | names of bundle-side work, echoed back per applied row |

The machine is inferred. A qualified reference (`hold.none`) names it;
otherwise it is the one machine that owns every `from` reference. If that
is ambiguous, publish says `cannot infer its machine … set machine:`, and a
`machine:` key settles it.

**`expected:` marks the normal way in, not the likely one.** Every edge is
legal, and most are shortcuts. A client that draws only the expected edges
must still show every state, which is why every state but the initial needs
one (§3). `staff.decline` is `from: open` but `expected: [in_review]`:
declining from review is the normal path, and declining an unread request
is a shortcut.

**`to: same`** records something without moving the machine: a nudge, a
snooze. It may write other columns, but not its own machine's.

```yaml
- on: staff.nudge
  from: open
  to: same
  writes: {Nudged At: now}
  cta: {kind: nudge, label: Nudge}
```

A `same` edge counts as neither a way in nor a way out, so it cannot
satisfy the reachability, expected or exit checks. This one also needs
`nudge` added to `events.staff` and a `Nudged At` column.

**`flow:` and `then:`** hand work to the bundle. A flow edge is legal like
any other, but `feature.state.transition` writes nothing for it and returns
the flow to launch. The flow's own writes move the row, which is how a
staff edge can land on more than one state. From a separate graph, a
`document` machine whose `sent` is terminal:

```yaml
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

A `then` input is a literal or one of `$payload.<key>`, `$row.<Column>`
(read after the writes), `$record_id` or `$conversation_id`. A `then` entry
may carry its own `when:`, judged against the row after the writes.

### The button

`cta:` takes `kind` and `label`, which are required, and optional `ui`,
`prominence` (`primary` or `quiet`), `route`, `message` and `when`. The
`kind` names the button, and one kind belongs to one event. `route`
defaults to `deterministic`: a click runs your `cta_apply` flow directly
(§5) and posts nothing. `message` is the chat line, templated on columns as
`{Title}` or `{Title|this request}`.

A button's `when` can offer *less* than the edge allows. Approve is legal
while a row is on hold, but a held card should not invite it:

```yaml
- on: staff.approve
  from: in_review
  to: approved
  expected: true
  guard: [has_owner]
  writes: {Decision: approve}
  cta:
    kind: approve
    label: Approve
    when: [{machine: hold, is: none}]
```

Held, the row now offers Decline and Release. An event with more than one
legal edge for a row is not offered at all, because the click would be
refused as `Ambiguous`.

### Status

| Key | Default | Meaning |
|---|---|---|
| `column` | `Status` | the projected chip |
| `ctas_column` | `CTAs` | the offered buttons; `null` for none |
| `why_column` | `Why` | the reason prose; `null` for none |
| `sub` | none | a machine column a client shows under the chip |
| `compose` | none | precedence rules, first match wins |
| `row_ctas` | `all` | `unless_warn` leaves a warning row's buttons to its worklist item |
| `worklist` | none | an action-item table the projection keeps |

The defaults are columns too. A section with no `status:` key still needs
`Status`, `CTAs` and `Why` declared on the table.

`compose` overrides the overlay fall-through. A rule's `show:` names a
machine, meaning its current state, or a literal state, and a rule may carry
its own `why`.
To let a decided request show its decision even while a stale blocker is
still derived:

```yaml
status:
  column: Status
  ctas_column: CTAs
  why_column: Why
  compose:
    - when: [{machine: review, in: [approved, declined]}]
      show: review
```

With no unconditional rule, anything the rules do not match falls through as
before. With one, every machine no rule shows drops out of the Status
vocabulary and its hint.

`worklist: {table: issues, key: cause}` keeps one open row per tracker row
whose shown status is a work item. The worklist table must declare every
column the reconcile writes: `cause`, `Issue`, `Stage`, `Why`, `ctas`,
`Status`, `Opened`, `Resolved` and `affected_record_ids`, or the names you
set on `worklist:` instead.

## 3. The publish checks that trip authors

Each check refuses the publish with one message, prefixed `states:`. The
wording is the engine's, and these are the messages the example's variants
produce.

**Every state but the initial needs an `expected:` edge in.** This is the
one new graphs hit first. Here `expected: true` was left off
`staff.start_review`:

```text
states: 'review': no expected edge enters ['in_review']; mark the edge that is the normal way in with expected: (an `also:` needs a when: [{machine: review, …}] naming where it leaves)
```

Mark the edge that is the state's normal way in. An `also:` counts only
when its transition's `when:` names the machine and state it leaves from;
otherwise its source is unknown and no spine can draw it.

**Every state must be reachable** from the initial state, through edges or
through `also:`. A state nothing enters is dead, or its world event is
missing:

```text
states: 'review': no edge reaches ['escalated']; a state nothing enters is either dead or missing its world event
```

**A funnel state with no way out must be terminal.** Overlays are exempt,
because an overlay may simply stay set until it clears. Here `approved`
lost its `terminal: true`:

```text
states: review.approved has no way out and is not terminal
```

**Only `system` leaves a `terminal: true` state.** Letting `staff.reopen`
leave `approved` as well as `declined`:

```text
states: review.approved is terminal but ['staff.reopen'] leave it
```

If people should be able to undo the ending, declare it
`terminal: reopenable`, as `declined` is. Another machine's edge that
moves this machine through `also:` needs a `when:` that rules the terminal
state out.

**No two machines share a state name.** Status holds their union, so a
value must name its machine on its own:

```text
states: state 'received' is declared by both 'review' and 'blocker'; the Status vocabulary is their union
```

**Staff edges do something, and land somewhere definite.** A button that
moves only a derived machine would be undone by the next derivation, so it
must write a fact, launch a flow, or declare an effect. A staff edge lands
on one state unless a `flow:` decides. And only a `staff` edge carries a
button:

```text
states: staff edge 'staff.dismiss' moves only the derived machine 'blocker' and writes nothing; add writes, a flow, a then or an effect
states: staff edge 'staff.decline' must land on one state unless a flow decides the outcome
states: 'world.info_missing' carries a cta but is not a staff event
```

**One `cta.kind`, one event.** Two edges may share a kind only when they
fire on the same event:

```text
states: cta kind 'approve' is used by both 'staff.approve' and 'staff.reopen'
```

**A `same` edge does not write its own column**, because the row would move
while the edge claims it does not:

```text
states: 'staff.snooze' is a `same` edge but writes its own column 'Stage'; say where it lands
```

**`also:` names other machines.** The edge's own machine moves by `to:`:

```text
states: transition on 'staff.decline': also names its own machine 'review'; that is what to: is for
```

**Transition flows must be in the bundle.** Every `flow:` and `then:` has to
name a flow the bundle installs. Otherwise the row would move and then
launch nothing:

```text
states: transitions name flows ['notify_requester'] that this bundle does not install (flows: ['cta_apply'])
```

**`states:` needs `tables:`**, and the table it names must declare every
column the tier reads or writes. That means the status, CTAs and Why
columns, every stored machine column, every `writes` and `payload_writes`
column, and every column a predicate reads. Otherwise the tier would write
columns the table lacks, or read blanks:

```text
states: a tables: section declaring its table is required
states: table 'tracker' lacks columns ['Decision'] the states tier writes
states: predicates read columns ['Owner'] that table 'tracker' does not declare
```

The predicate check exists because a missing column reads blank on every
row, which would quietly make `has_owner` never hold.

**Drop hand-written `display:` hints.** The tier renders them from the
spec. A column that already carries a different one fails:

```text
states: column 'Stage' carries display hint 'status:received,in_review,approved,declined' but the states tier renders 'status:received,in_review,approved,declined;labels=received:Received|in_review:In review|approved:Approved|declined:Declined;tone=approved:green|declined:gray'; drop the literal or change the spec
```

A graph that moves from hand-kept hints onto the tier deletes those
literals. There is no need to copy the rendered value back in.

## 4. Guards

A guard is a named condition a transition lists under `guard:`. It is
`all:` or `any:` of predicates, and a bare list means `all:`. Each predicate
names exactly one subject and one operator:

| Subject | Operators |
|---|---|
| `column: X` | `empty: true` or `false`, `equals:`, `in:`, `not_in:` (case-insensitive) |
| `machine: M` | `is:`, `in:`, `not_in:` (states or groups), `group:` |
| `guard: G` | none; add `holds: false` to negate |
| `shown: true` | `is:`, `in:`, `not_in:` against the displayed Status |

```yaml
guards:
  has_owner: [{column: Owner, empty: false}]
  unowned:
    all: [{guard: has_owner, holds: false}]
  decided:
    any:
      - {column: Decision, in: [approve, decline]}
      - {machine: review, is: approved}
```

A guard may build on another guard, but not on itself through a cycle. A
guard can carry `code:` and `message:`, and a refusal it causes reports
them, so a client can key its copy on the code. Without them, a refusal
reads `staff.approve is not legal here: guard has_owner refused`.

**`shown:` belongs only on a button's `when:`.** What a row displays may
decide what a person is offered. It may not decide what is legal:

```text
states: guard 'shows_hold': a shown predicate belongs on a cta's when: only what a row displays decides what a person is offered
```

**External guards** are rules only the bundle's code can answer: a budget
lookup, a document check. Declare one so the graph still shows it:

```yaml
guards:
  has_owner: [{column: Owner, empty: false}]
  budget_ok: {external: true, description: The bundle checks the budget}
```

List it under `guard:` like any other. The platform never evaluates it. The
caller **vouches** for it per row, by passing
`guards: {"12": [budget_ok]}` to `feature.state.transition` or
`feature.state.project`. An edge behind an external guard that was not
vouched for is refused for that row (`external guard budget_ok was not
vouched for`), and a row's buttons leave it out. A result that relied on a
vouched guard carries `delegated: true`. Vouching for a guard the platform
evaluates itself fails with
`guards: ['has_owner'] are not external guards of this graph`. A predicate
cannot name an external guard at all:

```text
states: guard 'can_approve': predicate names external guard 'budget_ok'; only the bundle can evaluate it — vouch for it instead
```

## 5. Wire the flows

The graph does nothing until a flow calls it. There are three places.

**Buttons.** A deterministic button starts the bundle flow named
`cta_apply` with `action`, `record_ids` and `payload`. That flow fires the
event through `feature.state.transition`. The activity does **not** start
the flows that `flow:` edges and `then:` entries name. It returns them as
`launches`, and the flow must start them:

```yaml
name: cta_apply
version: 1
description: >
  Apply one button: fire its event on the targeted rows, start whatever
  the edges launch, and fail by name when nothing applied.
inputs:
  action: { type: string }
  record_ids: { type: array }
  payload: { type: object, default: {} }
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
outputs:
  applied: $steps.apply.output.applied
  results: $steps.apply.output.results
```

The `derive` step exists because this graph has a derived machine. The
transition recomposes Status after the edge lands, and a `blocker` left out
of `machines` reads as `none`, so a click would clear a warning the facts
still support. A graph whose machines are all stored skips that step and
passes no `machines`.

**Events from the world.** A webhook, schedule or turn that learns
something fires the event the same way. `payload` feeds `payload_writes`:

```yaml
- id: land
  activity: feature.state.transition
  args:
    event: world.withdrawn
    record_ids: [$inputs.record_id]
    payload: { note: $inputs.note }
```

**The sweep.** `feature.state.project` recomposes rows from their tuple.
With no `record_ids` it projects every row and reconciles the whole
worklist. A tick usually ends with it, so the derived machines follow the
facts:

```yaml
- id: derive
  activity: foundation.code.execute
  args:
    code_name: request_rules
    reads:
      - { type: list_rows, name: rows, table_name: tracker, all_pages: true }
    inputs: { op: machines }
- id: project
  activity: feature.state.project
  args:
    machines: $steps.derive.output.machines
    why: $steps.derive.output.why
    results: warn
```

**What an applied edge writes**, in one patch at the row's read-time
revision:

- the edge's `writes` and `payload_writes`
- the landing state's value in its machine's column, and each `also` machine's
- the `detail` stamp
- the recomposed `Status`, `CTAs`, `Why`, mirrors and policy

A row that changed since it was read comes back `refused` with `StaleRev`,
and nothing overwrites it. Each applied edge also records a change on the
row: `cta_applied` for a staff event, `state_transition` for any other,
with the old and new Status. The bundle's own `writes` input may not touch
the projection columns:

```text
writes for record 12 touch projection columns ['Status']; the engine writes them from the tuple
```

That is the rule from the concept, enforced: change a row's status by firing
an event, never by writing the column.

## 6. Check it

A publish that passes proves **structure**. Every reference resolves, every
state is reachable and has an expected way in, no funnel state is a dead
end, terminals hold, and the table declares what the tier touches.

It does not prove **intent**, which is still yours to check:

- **States no event fires in practice.** `world.info_missing` passes the
  checks whether or not any flow ever fires it. Search the bundle's flows
  for each non-staff event name, and for a derived machine, check that the
  code actually produces every state.
- **Terminals reached too early.** A `from: open` that should have been
  `from: in_review` publishes fine and lets a request be approved unread.
  Read each terminal's incoming edges as a list of every way a row can end
  there.
- **Buttons that never show.** A guard on a column nothing writes, or a
  button `when:` that cannot hold, publishes fine and offers nothing.

`feature.state.spec` returns the resolved graph from the version the
channel is bound to. It includes a Mermaid diagram per machine, and a
`spine` of the expected edges alone, which is quick to read against what
you meant. For the rows themselves, `feature.state.check` holds every row
to the graph. Each stored value must be a declared state, each mirror must
agree with the value the bundle supplies, and each Status must be what its
tuple composes to. With `fail_step: true`, any offender fails the step as
`StatesOutsideGraph`, which makes it a test flow's assertion.
