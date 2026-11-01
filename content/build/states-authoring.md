---
id: states-authoring
title: Author a States tier
order: 12
group: Tables and Status
summary: >
  Writing the State graph behind a Routine's Status and Actions, in
  `recipe.yaml` or `states:`: stored, derived and mirrored machines; States, Events, Transitions and buttons;
  Guards; and the Flows that fire an edge, which must start its `flow` and
  `then` launches themselves. Every Publish check is listed with its exact
  error — `no expected edge enters`, a terminal left by staff — and its fix.
lede: >
  Write the States and Transitions behind a Routine's Status and Actions, and
  get them past the Publish checks.
concepts: [state-machine, manifest-keys, app-bundle]
---

This guide takes one State graph from design to a published, wired graph.
What a State Machine *is* — the tuple, the projection, why a button is an
edge — is [the State Machine](https://docs.popcorn.ai/state-machine.md),
and where the two overlap that page is authoritative. In the product, the
projected Status is an Item's **Status**, and each staff edge's button is an
**Action** (see the [glossary](https://docs.popcorn.ai/glossary.md)).

A Routine Template ships its graph in one of two places. The keys and the
engine are the same for both, and so are the graph's Publish checks; a Recipe
adds a few checks of its own (see "The Publish checks that trip authors"). Everything after this section applies to
either:

- **A Recipe**: `recipe:` in `manifest.yaml`, and the graph as `recipe.yaml`
  at the Bundle's root. This is what gives a Routine Steps it can change on
  its own. The template's Recipe is in force until a Routine installs a
  revision of its own. Over MCP, an assistant changes a Routine's Steps with
  `change_routine`, which refuses a Routine whose template declares no
  `recipe:`. It drafts the change by starting the template's own
  `recipe_build` Flow as a dry run, installs it by starting `recipe_build`
  again for real, and goes back to an earlier revision through the
  template's `recipe_install` Flow.
- **A `states:` section** in `manifest.yaml`, holding the same keys. Its
  graph is fixed by the template Version: every Routine on that Version runs
  the same one, and changing it means publishing a new Version.

A template declares one or the other, never both. What else a Recipe carries,
and how a Routine's own revision is installed and kept, is in
[the State Machine](https://docs.popcorn.ai/state-machine.md)'s
last section.

The loop is the ordinary one from
[changing a Routine Template](https://docs.popcorn.ai/template-authoring.md):
edit the graph, check it, read the error, repeat. One thing is
different. The CLI's own checks do not look inside the graph, in
`recipe.yaml` or under `states:`; it is checked only when the server parses
the Bundle. `popcorn app validate`
sends it there when run logged in from a fork Checkout with edits, and
`app publish` (or `create_routine_version`'s dry run) always does. The check
stops at the first problem, so a new graph usually takes several rounds to
pass, one error at a time. Run those rounds with `app validate`, which mints no Version.

## The worked example

A Table of requests that someone reviews. Most graph blocks later in this
guide are changes to it, and every one was parsed by the engine. As a Recipe,
the Manifest declares the Table and `recipe:`:

```yaml
# manifest.yaml
tables:
  tracker:
    columns:
      - {name: Title, type: string}
      - {name: Owner, type: string}
      - {name: Decision, type: string}
      - {name: Decision Note, type: string}
      - {name: Stage, type: string}
      - {name: Hold, type: string}
      - {name: Tracking, type: string}
      - {name: Status, type: string}
      - {name: CTAs, type: json}
      - {name: Why, type: string}

recipe: {}   # the graph is recipe.yaml
```

and `recipe.yaml` holds the graph:

```yaml
# recipe.yaml
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
  tracking:
    column: Tracking
    overlay: true
    states:
      not_tracking: {label: Not tracking, tone: gray}
events:
  staff: [start_review, approve, decline, reopen, hold, release, stop_tracking]
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
  - on: staff.stop_tracking
    from: tracking.none
    to: not_tracking
    expected: true
    cta:
      kind: stop-tracking
      label: Stop tracking
      prominence: quiet
      direct_only: true
      when: [{shown: true, is: missing_info}]
```

As a `states:` section, the same graph is the Manifest's `states:` key, with
everything in `recipe.yaml` indented under it, in place of `recipe:`.

It has four machines. `review` is the Funnel, stored in `Stage`. `blocker`
is an Overlay with no Column, so the Bundle's own code decides it from the
Row's facts. `hold` is an Overlay stored in `Hold`. `tracking` is the one a
Recipe needs once its graph has a work item: `missing_info` warns, so a Row
showing it opens an action item, and a Recipe is refused unless that item
can stop tracking its Row (see "The Publish checks that trip authors"). Its button's `when:` keeps Stop tracking to
the Rows showing `missing_info`, which get it as action items anyway.
Publish renders display hints onto `Status`, `Stage`, `Hold` and `Tracking`.
The one on `Status` lists the whole vocabulary and marks `missing_info` as a
warning:

```text
status:received,in_review,approved,declined,missing_info,on_hold,not_tracking;warn=missing_info;labels=…;tone=…
```

A Row in review, with an owner and nothing blocking it, shows `in_review` and
offers Approve, Decline and Put on hold. Put it on hold and it shows `on_hold`.
Now Approve is still offered but Put on hold is not, because its edge leaves
only `hold.none`.

## Design the machines

**One Funnel, then Overlays.** The Funnel is the milestone that moves
forward. An Overlay is something true *alongside* it: blocked, parked,
waiting on a side document. An Overlay has an implicit `none` State, and you
never declare it. Test each candidate State against this: can it hold at the
same time as a Funnel State? If it can, it belongs in an Overlay. The first
machine with no `overlay: true` is the **primary**. When no Overlay is
active, Status shows the primary.

**Declaration order is precedence.** With no `status.compose` rules, Status
shows the first Overlay, in declaration order, that is not `none`. The
example declares `blocker` before `hold`, so a Row that is held *and* missing
information shows the warning, not the parking.

**Where each value comes from:**

| Shape | Declared as | Its value comes from | Moves by |
|---|---|---|---|
| stored | `column: Stage` | the Column | Events: the engine writes the Column when an edge lands |
| derived | no `column` | the Bundle's code, handed in per Row | the Bundle's derivation changing |
| mirror | `column:` plus `derive: true` | the Bundle's code; the engine writes it into the Column | the same, recorded in a Column clients can read |

A derived value reaches the engine as `machines`, keyed by each Row's id (its
`record_id`) as a string. That input goes to `feature.state.project`,
`feature.state.transition` and `feature.state.check`:

```yaml
machines: {"12": {blocker: missing_info}, "13": {blocker: none}}
```

A block can also carry the value on its own Row patch. In a
`patch_rows … project_states: true` write from `foundation.code.execute`,
each patch carries `states: {machines: {blocker: missing_info}}` for its own
Row. A machine you leave out reads as its Column, or as its initial State. A
stored machine cannot be supplied: its value is its Column, and a caller that
could hand one in could make an illegal edge legal. The Step fails with
`MachinesInvalid`:

```text
machines: stored machines ['review'] are read from their columns, not supplied
```

A mirror suits a value that is computed but must still be readable as a
Column, for filtering or for a client:

```yaml
machines:
  payment:
    column: Payment
    derive: true
    states:
      unpaid: {label: Unpaid}
      paid: {label: Paid, tone: green, terminal: true}
```

A mirror's Column belongs to the projection, the same as `Status`. A Bundle
patch that writes it is refused.

**A derived machine still needs edges.** The graph checks walk Transitions,
so `blocker` declares `world.info_missing` and `world.info_received` even
though nothing fires them. The Bundle simply starts supplying
`missing_info`. The edges say how the value moves, and they are what a
rendered graph draws.

**The initial State is the first one declared** unless `initial:` names
another. Put the entry State first, and keep that order in any tool that
rewrites YAML: one that sorts keys changes the initial State without a
word. An Overlay's initial State is `none`.

## States, Events, Transitions and Status

### States

| Key | Meaning |
|---|---|
| `label` | the chip text; the State name humanised when absent |
| `tone` | `green`, `red`, `gray` or `black` |
| `warn` | the chip is a warning, and a Row showing it is a work item |
| `terminal` | `true`: only a `system` Event may leave it. `reopenable`: an ending that a later Event may undo |
| `stored_as` | the Column value when it is not the State name |
| `why` | the default Why prose while a Row shows this State |
| `work_item` | overrides `warn` for the worklist: `true` opens an item without warning, `false` warns without one |
| `detail` | `{column, values, labels, tone}`: a qualifier Column for this State — one State, many reasons — that an edge landing here may stamp |

State names may not contain `,`, `;` or `|`, and labels may not contain `;`,
`:` or `|`. Hints are built from both, and those characters are the hint's
separators. `groups:` names sets of States. `from:` and the predicates accept
a group wherever they accept a State.

### Events

`events:` maps a **family** to its Event names. Two family names mean
something to the platform:

- `staff` Events are people's decisions. Only a `staff` edge may carry a
  `cta:`, so these are the buttons.
- `system` Events are the only ones allowed to leave a `terminal: true`
  State. Keep them for corrections the Bundle's own machinery makes, such as
  a failed Step that has to move a finished Row, never for a decision.

Every other family name is yours; `world` and `agent` are the usual ones. A
Transition names its Event as `family.event`. `feature.state.transition`
also accepts the bare Event name when only one family has it, which is how
a button's `action` arrives. A bare `on:` key is safe. YAML reads it as the
boolean `true`, and the parser turns it back.

### Transitions

| Key | Meaning |
|---|---|
| `on` | `family.event` |
| `from` | a State, a group, a list of them, or `*`; qualify as `hold.none` when the name is ambiguous |
| `to` | one State; several, when a Flow or a written value decides; or `same` |
| `expected` | `true`, or the list of `from` States it is the normal move out of |
| `writes` | Column → literal, written when the edge lands |
| `payload_writes` | Column → payload key, from the Event's `payload` |
| `also` | other machine → State, moved at the same time |
| `when` | predicates on the Row and the tuple; all must hold |
| `guard` | named Guards; all must hold |
| `cta` | the button, on `staff` edges only |
| `flow` | a Bundle Flow that *is* the edge; the edge writes nothing itself |
| `then` | Bundle Flows to launch per Row after the writes land |
| `effects` | names of Bundle-side work, echoed back per applied Row |
| `detail` / `detail_from` | the landing State's detail value, literal or read from that payload key; mutually exclusive, and the landing State must declare `detail:` |
| `importance` | 1–10, how loudly a client draws the edge, on one scale across every machine; display only. An int, or a map of source State to rank with an optional `default` |
| `description` | free text |

The machine is inferred. A qualified reference (`hold.none`) names it;
otherwise it is the one machine that owns every `from` reference. If that
is ambiguous, Publish says `cannot infer its machine … set machine:`, and a
`machine:` key settles it.

**`importance:` is all or nothing.** A spec ranks every edge or none. With
none, an expected edge draws at 6 and the rest at 3. Rank rarity with
`importance`, not by dropping `expected`: a rare failure can be the one way
into its State and still draw quietly.

**`expected:` marks the normal way in, not the likely one.** Every edge is
legal, and most are shortcuts. A client that draws only the expected edges
must still show every State, which is why every State but the initial needs
one (see "The Publish checks that trip authors"). `staff.decline` is `from: open` but `expected: [in_review]`:
declining from review is the normal path, and declining an unread request
is a shortcut.

**`to: same`** records something without moving the machine: a nudge, a
snooze. It may write other Columns, but not its own machine's.

```yaml
- on: staff.nudge
  from: open
  to: same
  writes: {Nudged At: now}
  cta: {kind: nudge, label: Nudge}
```

A `same` edge counts as neither a way in nor a way out, so it cannot
satisfy the reachability, expected or exit checks. This one also needs
`nudge` added to `events.staff` and a `Nudged At` Column.

**`flow:` and `then:`** hand work to the Bundle. A Flow edge is legal like
any other, but `feature.state.transition` writes nothing for it and returns
the Flow to launch. The Flow's own writes move the Row, which is how a
staff edge can land on more than one State. From a separate graph, a
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
may carry its own `when:`, judged against the Row after the writes.

### The button

`cta:` takes `kind` and `label`, which are required, and optional `ui`
(`button`, the default, `input`, `contact-picker`, `contact-form` or
`signing-modal`), `prominence` (`primary` or `quiet`), `route`
(`deterministic`, `agent` or `noop`), `message` and `when`. The `kind` names
the button, and one kind belongs to one Event. `route` defaults to
`deterministic`: a click runs your `cta_apply` Flow directly (see "Wire the Flows") and posts
nothing. `message` is the chat line, templated on Columns as
`{Title}` or `{Title|this request}`.

**Choose `ui` and `route` knowing who presses the button.** The Popcorn client
draws every one. An assistant over MCP can take only an Action that the press
completes: `route: deterministic` with `ui: button`. `list_actions` shows the
others marked "in the Popcorn app", and `take_action` refuses them. Both the
client and `take_action` start the Flow by the literal name `cta_apply`, so a
Bundle with buttons must ship a Flow by that name.

A button's `when` can offer *less* than the edge allows. Approve is legal
while a Row is on hold, but a held card should not invite it:

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

Held, the Row now offers Decline and Release. An Event with more than one
legal edge for a Row is not offered at all, because the click would be
refused as `Ambiguous`.

### Status

| Key | Default | Meaning |
|---|---|---|
| `column` | `Status` | the projected chip |
| `ctas_column` | `CTAs` | the offered buttons; `null` for none |
| `why_column` | `Why` | the reason prose; `null` for none |
| `sub` | none | a machine Column a client shows under the chip |
| `compose` | none | precedence rules, first match wins |
| `row_ctas` | `all` | `unless_warn` leaves a warning Row's buttons to its worklist item |
| `worklist` | none | an action-item Table the projection keeps |

The defaults are Columns too. A section with no `status:` key still needs
`Status`, `CTAs` and `Why` declared on the Table.

`compose` overrides the Overlay fall-through. A rule's `show:` names a
machine, meaning its current State, or a literal State, and a rule may carry
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

`worklist: {table: issues, key: cause}` keeps one open Row per `tracker` Row
whose shown Status is a work item. The worklist Table must declare every
Column the reconcile writes: `cause`, `Issue`, `Stage`, `Why`, `ctas`,
`Status`, `Opened`, `Resolved` and `affected_record_ids`, or the names you
set on `worklist:` instead.

## The Publish checks that trip authors

Each check refuses the Publish with one message. A check on the graph is
prefixed `states:`, in a Recipe too; a Recipe's own checks, last in this
section, name the block or the file they looked at. The wording is the
engine's, and these are the messages the example's variants produce.

**Every State but the initial needs an `expected:` edge in.** This is the
one new graphs hit first. Here `expected: true` was left off
`staff.start_review`:

```text
states: 'review': no expected edge enters ['in_review']; mark the edge that is the normal way in with expected: (an `also:` needs a when: [{machine: review, …}] naming where it leaves)
```

Mark the edge that is the State's normal way in. An `also:` counts only
when its Transition's `when:` names the machine and State it leaves from;
otherwise its source is unknown and no spine can draw it.

**Every State must be reachable** from the initial State, through edges or
through `also:`. A State nothing enters is dead, or its world Event is
missing:

```text
states: 'review': no edge reaches ['escalated']; a state nothing enters is either dead or missing its world event
```

**A Funnel State with no way out must be terminal.** Overlays are exempt,
because an Overlay may simply stay set until it clears. Here `approved`
lost its `terminal: true`:

```text
states: review.approved has no way out and is not terminal
```

**Only `system` leaves a `terminal: true` State.** Letting `staff.reopen`
leave `approved` as well as `declined`:

```text
states: review.approved is terminal but ['staff.reopen'] leave it
```

If people should be able to undo the ending, declare it
`terminal: reopenable`, as `declined` is. Another machine's edge that
moves this machine through `also:` needs a `when:` that rules the terminal
State out.

**No two machines share a State name.** Status holds their union, so a
value must name its machine on its own:

```text
states: state 'received' is declared by both 'review' and 'blocker'; the Status vocabulary is their union
```

**Staff edges do something, and land somewhere definite.** A button that
moves only a derived machine would be undone by the next derivation, so it
must write a fact, launch a Flow, or declare an effect. A staff edge lands
on one State unless a `flow:` decides. And only a `staff` edge carries a
button:

```text
states: staff edge 'staff.dismiss' moves only the derived machine 'blocker' and writes nothing; add writes, a flow, a then or an effect
states: staff edge 'staff.decline' must land on one state unless a flow decides the outcome
states: 'world.info_missing' carries a cta but is not a staff event
```

**One `cta.kind`, one Event.** Two edges may share a kind only when they
fire on the same Event:

```text
states: cta kind 'approve' is used by both 'staff.approve' and 'staff.reopen'
```

**A `same` edge does not write its own Column**, because the Row would move
while the edge claims it does not:

```text
states: 'staff.snooze' is a `same` edge but writes its own column 'Stage'; say where it lands
```

**`importance:` ranks every edge or none**, and a map must cover every
`from:` State or carry `default:`:

```text
states: importance ranks every edge or none; unranked: ['staff.reopen']
states: transition on 'staff.decline' ranks no importance from ['received']; name them or add default:
```

**A detail stamp needs a landing State that declares one:**

```text
states: transition on 'staff.decline' stamps a detail but its landing state declares none
```

**`also:` names other machines.** The edge's own machine moves by `to:`:

```text
states: transition on 'staff.decline': also names its own machine 'review'; that is what to: is for
```

**Transition Flows must be in the Bundle.** Every `flow:` and `then:` has to
name a Flow the Bundle installs. Otherwise the Row would move and then
launch nothing:

```text
states: transitions name flows ['notify_requester'] that this bundle does not install (flows: ['cta_apply'])
```

**The graph needs `tables:`**, and the Table it names must declare every
Column the tier reads or writes. That means the Status, CTAs and Why
Columns, every stored machine Column, every `writes` and `payload_writes`
Column, and every Column a predicate reads. Otherwise the tier would write
Columns the Table lacks, or read blanks:

```text
states: a tables: section declaring its table is required
states: table 'tracker' lacks columns ['Decision'] the states tier writes
states: predicates read columns ['Owner'] that table 'tracker' does not declare
```

The predicate check exists because a missing Column reads blank on every
Row, which would quietly make `has_owner` never hold.

**Drop hand-written `display:` hints.** The tier renders them from the
spec. A Column that already carries a different one fails:

```text
states: column 'Stage' carries display hint 'status:received,in_review,approved,declined' but the states tier renders 'status:received,in_review,approved,declined;labels=received:Received|in_review:In review|approved:Approved|declined:Declined;tone=approved:green|declined:gray'; drop the literal or change the spec
```

A graph that moves from hand-kept hints onto the tier deletes those
literals. There is no need to copy the rendered value back in.

**A Recipe has checks of its own**, on the Bundle around the graph. The
Manifest declares `recipe:` or `states:`, not both; `recipe:` needs
`recipe.yaml` at the Bundle's root, and `recipe.yaml` needs `recipe:`; and
`recipe:` needs `tables:`, as `states:` does:

```text
recipe: a bundle declares states: or recipe:, not both
recipe: the bundle ships no recipe.yaml at its root
recipe.yaml is present but the manifest declares no recipe: section
recipe: a tables: section declaring the graph's table is required
```

**A Recipe's action items must be able to stop tracking.** When the graph
has a work item, it needs a `staff.stop_tracking` edge from `tracking.none`
to `not_tracking` carrying a `cta` of kind `stop-tracking`, as the example's
`tracking` machine does. A `states:` section has no such check. Without the
edge:

```text
recipe.yaml: the recipe opens action items (missing_info) but declares no staff.stop_tracking transition with a `cta: {kind: stop-tracking}`; every action item must be able to stop tracking its row (e.g. `on: staff.stop_tracking`, `from: tracking.none`, `to: not_tracking`, `cta: {kind: stop-tracking, prominence: quiet, direct_only: true}`)
```

## Guards

A Guard is a named condition a Transition lists under `guard:`. It is
`all:` or `any:` of predicates, and a bare list means `all:`. Each predicate
names exactly one subject and one operator:

| Subject | Operators |
|---|---|
| `column: X` | `empty: true` or `false`, `equals:`, `in:`, `not_in:` (case-insensitive) |
| `machine: M` | `is:`, `in:`, `not_in:` (States or groups), `group:` |
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

A Guard may build on another Guard, but not on itself through a cycle. A
Guard can carry `code:` and `message:`, and a refusal it causes reports
them, so a client can key its copy on the code. Without them, a refusal
reads `staff.approve is not legal here: guard has_owner refused`.

**`shown:` belongs only on a button's `when:`.** What a Row displays may
decide what a person is offered. It may not decide what is legal:

```text
states: guard 'shows_hold': a shown predicate belongs on a cta's when: only what a row displays decides what a person is offered
```

**External Guards** are rules only the Bundle's code can answer: a budget
lookup, a document check. Declare one so the graph still shows it:

```yaml
guards:
  has_owner: [{column: Owner, empty: false}]
  budget_ok: {external: true, description: The bundle checks the budget}
```

List it under `guard:` like any other. The platform never evaluates it. The
caller **vouches** for it per Row, by passing
`guards: {"12": [budget_ok]}` to `feature.state.transition` or
`feature.state.project`. An edge behind an external Guard that was not
vouched for is refused for that Row (`external guard budget_ok was not
vouched for`), and a Row's buttons leave it out. A result that relied on a
vouched Guard carries `delegated: true`. Vouching for a Guard the platform
evaluates itself fails with
`guards: ['has_owner'] are not external guards of this graph`. A predicate
cannot name an external Guard at all:

```text
states: guard 'can_approve': predicate names external guard 'budget_ok'; only the bundle can evaluate it — vouch for it instead
```

## Wire the Flows

The graph does nothing until a Flow calls it. There are three places.

**Buttons.** A deterministic button starts the Bundle Flow named
`cta_apply` with `action`, `record_ids` and `payload`. That Flow fires the
Event through `feature.state.transition`. The Activity does **not** start
the Flows that `flow:` edges and `then:` entries name. It returns them as
`launches`, and the Flow must start them:

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

The `derive` Step exists because this graph has a derived machine. The
Transition recomposes Status after the edge lands, and a `blocker` left out
of `machines` reads as `none`, so a click would clear a warning the facts
still support. A graph whose machines are all stored skips that Step and
passes no `machines`.

**Events from the world.** A Webhook, Schedule or turn that learns
something fires the Event the same way. `payload` feeds `payload_writes`:

```yaml
- id: land
  activity: feature.state.transition
  args:
    event: world.withdrawn
    record_ids: [$inputs.record_id]
    payload: { note: $inputs.note }
```

**The sweep.** `feature.state.project` recomposes Rows from their tuple.
With no `record_ids` it projects every Row and reconciles the whole
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

**What an applied edge writes**, in one patch at the Row's read-time
revision:

- the edge's `writes` and `payload_writes`
- the landing State's value in its machine's Column, and each `also` machine's
- the `detail` stamp
- the recomposed `Status`, `CTAs`, `Why`, mirrors and policy

A Row that changed since it was read comes back `refused` with `StaleRev`,
and nothing overwrites it. Each applied edge also records a change on the
Row: `cta_applied` for a staff Event, `state_transition` for any other,
with the old and new Status. The Bundle's own `writes` input may not touch
the projection Columns:

```text
writes for record 12 touch projection columns ['Status']; the engine writes them from the tuple
```

That is the rule from the concept, enforced on the Transition path: change a
Row's Status by firing an Event. A plain store write to the Column is not
refused, but the next projection overwrites it.

## Check it

A Publish that passes proves **structure**. Every reference resolves, every
State is reachable and has an expected way in, no Funnel State is a dead
end, terminals hold, and the Table declares what the tier touches.

It does not prove **intent**, which is still yours to check:

- **States no Event fires in practice.** `world.info_missing` passes the
  checks whether or not any Flow ever fires it. Search the Bundle's Flows
  for each non-staff Event name, and for a derived machine, check that the
  code actually produces every State.
- **Terminals reached too early.** A `from: open` that should have been
  `from: in_review` publishes fine and lets a request be approved unread.
  Read each terminal's incoming edges as a list of every way a Row can end
  there.
- **Buttons that never show.** A Guard on a Column nothing writes, or a
  button `when:` that cannot hold, publishes fine and offers nothing.

`feature.state.spec` returns the resolved graph the Run judges Rows by. For
a `states:` section that is the Version the Routine is bound to; for a
Recipe it is the revision the Run pinned, which is the Routine's own once it
has installed one, and the template's otherwise. It includes a Mermaid diagram per machine, and a
`spine` of the expected edges alone, which is quick to read against what
you meant. For the Rows themselves, `feature.state.check` holds every Row
to the graph. Each stored value must be a declared State, each mirror must
agree with the value the Bundle supplies, and each Status must be what its
tuple composes to. With `fail_step: true`, any offender fails the Step as
`StatesOutsideGraph`, which makes it a test Flow's assertion.
