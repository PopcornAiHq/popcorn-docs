---
id: state-machine
title: State Machines in a Bundle
order: 16
group: Tables and Status
summary: >
  A Routine's Status and Actions come from State Machines its template
  declares: States, Transitions, and the buttons a user sees on a Row, each
  configured on its staff edge, as in Questionnaire's Stage. Status is a
  projection, so it changes by firing an Event. Two machines may not share
  a State name. Publish proves structure only.
lede: >
  How a template defines the Status and Actions of a Routine's Items, as
  States and the Transitions between them.
concepts: [states-authoring, actions-and-status, manifest-keys, versions, app-bundle]
---

An [Item](https://docs.popcorn.ai/work-a-routines-items.md)'s
[Status](https://docs.popcorn.ai/actions-and-status.md), and the Actions it
offers, are not one flat field. Underneath, a Row of the Table the machines
run over is a **tuple of small machines**, and the single chip a person
sees is a projection of that tuple.

A Bundle declares the machines, their States, and the Transitions between
them in its [Manifest](https://docs.popcorn.ai/manifest-keys.md)'s
`states:` section, or in a Recipe the Routine can replace (the last section
below). The platform ships the engine and runs the graph; the Bundle ships
the graph and the vocabulary. The platform knows none of your State names,
only its own few words: `none`, `same`, the `staff` Event family whose
edges are buttons, and the `system` family, the only one that may leave a
terminal State. Writing one step by step is
[authoring a States tier](https://docs.popcorn.ai/states-authoring.md).

## Questionnaire's machine

The Questionnaire template has one machine, `recipient`, stored in the
`Stage` Column of its `recipients` Table:

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
    # A pass holds the row while it sends or checks, and writes Stage from
    # the row as it read it: an Action landing then would be overwritten.
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
      from: no_response
      to: answered
      guard: [not_held]
      expected: true
      description: Marked answered by a person
      cta:
        kind: mark-answered
        label: Mark answered
        message: "Mark {Name|this recipient} as answered."
    - on: staff.mark_answered
      from: [new, waiting]
      to: answered
      guard: [not_held]
      expected: true
      description: Marked answered by a person
      cta:
        kind: mark-answered
        label: Mark answered
        message: "Mark {Name|this recipient} as answered."
    - on: staff.close
      from: no_response
      to: closed
      guard: [not_held]
      expected: true
      description: Closed, so nobody follows up
      cta:
        kind: close
        label: Close
        prominence: quiet
        message: "Close {Name|this recipient}."
    - on: staff.close
      from: [new, waiting]
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

`states:` needs a `tables:` section, and the Table it names must declare
every Column the tier reads or writes: here `Status`, `CTAs`, `Why` and
`Stage`, the `Sending` Column the guard reads, and the `Follow Ups` and
`Last Asked` that Ask again writes. Without a `status:` block the Columns
default to `Status`, `CTAs` and `Why`. A `states:` graph is read at run
time from the Version the Routine is bound to; Install writes only the
display hints it adds to those Columns.

A blank `Stage` is the machine's `initial` State, which is how a recipient
just added shows *Not asked yet* before anything has written it.

## Funnel, Overlay, derived

A **Funnel** machine carries the milestone the Row has data for: the thing
that moves forward, as `recipient` does from `new` to `answered`.
**Overlay** machines (`overlay: true`) say what is true alongside it: what
is blocking, whether the Row is parked, what a side document is doing. An
Overlay has an implicit `none` State, because "nothing is blocking" is the
common case and should not need declaring.

A machine with a `column:` is **stored**: its value lives in that Column,
as `recipient`'s lives in `Stage`. A machine without one is **derived**:
the Bundle's own code decides its value from the Row's facts and passes it
to the engine when it projects or transitions a Row. `derive: true` with a
Column is both: the Bundle decides the value and the engine mirrors it into
the Column. Turning facts into machine values is the Bundle's job;
everything after (values to Status, Event to legality, what a Transition
writes) belongs to the engine.

> [!NOTE] Questionnaire has neither
> Questionnaire runs one stored Funnel machine. Overlays and derived
> machines belong to templates whose Items carry more than one state at
> once, such as a claim that is both at a milestone and paused.

## Status is a projection, not a Column somebody writes

The Status chip is composed from the tuple by a precedence rule: the first
`status.compose` rule whose `when` holds; otherwise the first Overlay, in
declaration order, that is not `none`; otherwise the first non-overlay
machine. With one machine, Questionnaire's `Status` is simply its `Stage`,
shown with the State's `label`, and `Why` is the State's `why`.

Nothing should hand-write it. A Transition's own writes may not touch the
projection Columns, and a Flow's patch that asks to be projected is refused
if it writes one, though a plain store write is not refused. That is why
changing a Row's Status means firing an Event rather than setting a value:
set the value and the next projection overwrites it.

> "Mark Ana as answered in #team-offsite. She told me her answers on a
> call."

> [!TIP] MCP tool call
> Your assistant calls `take_action` with `mark_answered`. `create_rows`
> and `update_row` refuse `Stage`, `Status`, `Why` and `CTAs`, the Columns
> only a Transition changes.

Because the Status vocabulary is the union of every machine's States,
**two machines may not share a State name.** A value has to identify which
machine it came from, on its own.

## World and staff Events

An Event is `family.event`, and `events:` lists each family's names.
`staff` Events are what a person fires; any other family is the world's,
named by the Bundle. Questionnaire's `world` Events (`asked`, `answered`,
`gave_up`, `restarted`) are the moves its
[Flows](https://docs.popcorn.ai/flow-grammar.md) make: `ask_recipient`
and `check_recipient` write `Stage` with `foundation.store.patch_row`, then
call `feature.state.project` to recompute `Status`, `Why` and the Actions.
The world edges are declared so the graph is whole: without `world.asked`,
nothing could reach `waiting` (Ask again starts from `no_response`, which
only `waiting` leads to), and Publish would refuse the graph.

## Every button is an edge

A Transition names the Event that fires it, the States it is legal from,
the facts it writes, and the State it lands on. The button a person sees,
the [Action](https://docs.popcorn.ai/actions-and-status.md), is the `cta:`
declared on a `staff` Transition, so the graph and the interface cannot
disagree: there is no second place where buttons are configured, and a
`cta:` on any other family is refused.

Questionnaire's three:

| Action | From | Writes |
|---|---|---|
| **Ask again** | `no_response` | `Follow Ups: 0`, `Last Asked: null`, so the next pass follows up at once |
| **Mark answered** | `no_response`; and `new`, `waiting` | nothing else |
| **Close** (`prominence: quiet`) | `no_response`; and `new`, `waiting` | nothing else |

A `cta:` takes a `kind`, unique across the graph, a `label`, and a
`message`: the line a chat posts, filled from the Row, where
`{Name|this recipient}` falls back to its text when `Name` is blank.

Mark answered and Close are each declared as two edges with the same
`cta:`, one from the Review and one from the States before it, so the
Steps list names them among the Review's choices (see
[Which States are Steps](#which-states-are-steps)). A person sees one
button either way.

> [!IMPORTANT] Empty a datetime with null
> Ask again writes `Last Asked: null`, not `""`: `Last Asked` is a
> `datetime` Column, and the store refuses an empty string for one. See
> [Table Columns](https://docs.popcorn.ai/table-columns.md).

A person's click and `take_action` both start the Bundle's `cta_apply`
Flow with the Action and the Rows. Questionnaire's `cta_apply` is one
`feature.state.transition` Step, which judges the edge from each Row's
`Stage`, applies the writes and re-projects the Row.

**Guards** are conditions an edge requires. Most are Column or
machine-state predicates the platform evaluates itself, combined with
`all`, `any` and negation. Questionnaire's `not_held` requires `Sending`
to be empty, so an Action is refused while a pass is emailing or checking
that recipient, whose Flow would otherwise write `Stage` over it. An edge
whose rule only the Bundle's own code can answer is marked external: it
still appears in the graph, and the edge is refused unless the caller
vouches that the Guard holds. The predicate language is deliberately
small.

## An illegal graph fails at Publish, not at runtime

The whole spec is resolved when the Bundle is parsed. It fails when:

- a Transition names a State, group, Event, Guard or Flow that does not
  exist
- a State is unreachable, or has no **expected** edge into it: every State
  but the initial one marks the edge that is its normal way in with
  `expected:`, as `world.asked` is for `waiting`
- a non-terminal State of a Funnel machine has no way out
- a terminal State is left by anything but a `system` Event: nothing
  leaves `answered` or `closed`
- two machines share a State name, a `cta.kind` is used twice, or a Column
  the tier needs is not declared

> [!WARNING] The checks prove structure, not intent
> Overlay States are exempt from the no-way-out rule, so an Overlay can
> still hold a Row. And what you can always publish is a graph that is
> well-formed and wrong: States that no Event fires in practice, or a
> terminal State reached too early. Questionnaire's world edges pass every
> check whether or not its Flows really write those values.

## Which States are Steps

A Routine's [Steps](https://docs.popcorn.ai/steps.md), as `get_routine`
and the **Routine steps** tab in Popcorn list them, are read off the
first machine's States in the order they are declared. Two kinds make a
row:

- **A Step** is a State whose `policy:` names a Step type: `questions`
  (shown as Answers), `signature`, `booking`, `reminder` or `shipment`
  (Delivery). Under `policy.chase`, the stage engine of a
  [Recipe](#the-recipe-a-graph-each-routine-can-replace) with the `chase`
  contract runs it, sending and following up. Under `policy.step`, the
  State is only named a Step, and the template's own Flows do the work.
- **A Review** is a State that warns, is not terminal, and is not a Step,
  such as `no_response`. Its choices are the buttons on its edges, each
  listed with the State it leads to.

Questionnaire's `waiting` carries the marker:

```yaml title="manifest.yaml"
        waiting:
          label: Waiting
          why: Asked, with questions still open.
          policy: {step: {type: questions}}
```

A Step's ways out are its edges that are not buttons. A button also
offered from a Step is one every open Item has, like an Archive, so it is
not listed among a Review's choices. That is why Questionnaire declares
Mark answered and Close twice. A graph with no Step lists no Steps, and
Popcorn hides the tab.

For `#team-offsite`, `get_routine` lists:

```text
Steps:
1. Answers — Waiting (Status value: waiting)
   - on its own: Every question is answered → Answered (outcome)
2. Review — No response (Status value: no_response): "No answer after the last follow-up, or the reply-by date passed."
   - Ask again → Waiting (step 1)
   - Mark answered → Answered (outcome)
   - Close → Closed (outcome)
```

> [!NOTE] A marker changes no behaviour
> `policy.step` changes the list and nothing a Run does. Because the Steps
> are part of the template's Version rather than a Recipe of the Routine's
> own, they can't be changed by describing the change: they change with a
> new Version, or a [Copy](https://docs.popcorn.ai/copying-a-template.md).

## The Recipe: a graph each Routine can replace

A `states:` graph belongs to the template's Version (the platform calls it
a *bundle version*), so every Routine on that Version runs the same one,
and changing it means publishing a new Version. Questionnaire works this
way. The **Recipe** tier ships the same graph as a document of its own,
`recipe.yaml` at the Bundle's root, and lets each Routine install a
revision of its own. A Routine with
[Steps](https://docs.popcorn.ai/steps.md) of its own is running one.

```yaml title="manifest.yaml"
recipe:
  document: recipe   # the channel-config document key an installed revision lives under; the default
  contract: chase    # optional: an engine contract the graph must also satisfy
```

`recipe.yaml` holds the keys a `states:` section would, and the same
engine parses and runs it, so everything above applies unchanged, Publish
checks included. What differs is where the graph lives:

- **A Bundle declares `states:` or `recipe:`, never both.** `recipe:`
  needs a `tables:` section, as `states:` does. Publish refuses a
  `recipe:` with no `recipe.yaml`, and a `recipe.yaml` with no `recipe:`.
- **The Bundle's own Recipe is in force until the Routine installs one.**
  An installed revision is stored in the Routine's configuration (the
  *channel config*), and the sha256 of its text is its identity. Earlier
  revisions stay readable, so a Routine can go back to one, or to the
  Bundle's own. An assistant does this with `change_routine`; a Flow, with
  `feature.recipe.install`.
- **An Install refuses a revision the Rows cannot follow**: one whose graph
  does not declare a value a stored machine Column holds, or that moves a
  machine to another Column or Table. Moving stored State is a migration,
  not an Install.
- **A Run pins the revision in force when it starts**, with the Routine's
  configuration, so it judges every Row by one graph whatever is installed
  meanwhile.
- **A Bundle update keeps the Routine's revision**, and first checks it
  against the new Version: the Flows its edges launch, the Tables, the
  contract. When it no longer fits, the whole update is refused before
  anything is written.

Beside the graph, a Recipe may carry sections of its own that the engine
does not read as States. `vocabulary:` sets the nouns for the Bundle's
generic words (`document: contract`), from the terms the Bundle's
`strings.yaml` declares, and they are rendered into its client copy.
`guidance:` adds the Recipe author's instructions per agent. Both are
pinned with the revision, so changing either is a new revision. A contract
may read sections of its own, such as `chase`'s `start:` and `rejection:`.

> [!NOTE] The tier's old name
> The tier was first called **process**. A Manifest's `process:` block and
> a root `process.yaml` still read as `recipe:` and `recipe.yaml` (a
> `process:` block's document key defaults to `process`). A Bundle that
> declares both blocks, or ships both files, is refused.
