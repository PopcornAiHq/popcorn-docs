---
id: state-machine
title: State Machines in a Bundle
order: 13
group: Tables and Status
summary: >
  A Routine's Status and Actions come from State Machines its template
  declares — States, Transitions, and the button on each edge — which the
  platform runs. Status is a projection, so it changes by firing an Event; a
  value written to the Column lasts until the next projection. The graph is
  a Manifest `states:` section or a `recipe.yaml` each Routine can replace.
  Publish proves structure only.
lede: >
  How a template defines the Status and Actions of a Routine's Items, as
  States and the Transitions between them.
concepts: [manifest-keys, versions, states-authoring, app-bundle]
---

An Item's Status, and the Actions it offers, are not one flat field.
Underneath, a Row of the Table the machines run over is a **tuple of small
machines**, and the single chip a user sees is a projection of that tuple.

A Bundle declares the machines, their States, and the Transitions between them
in its Manifest's `states:` section, or in a Recipe the Routine can replace
(the last section below). The platform ships the engine and runs the graph; the Bundle
ships the graph and the vocabulary. The platform knows none of your State
names — only its own few words: `none`, `same`, and the `system` and `staff`
Event families.

`states:` needs a `tables:` section, and the Table it names must declare every
Column the tier reads or writes — here `Status`, `CTAs`, `Stage`,
`Tracking Mode`, `Decision`, and `Why`, where the reason for the last
Transition is written unless `status.why_column` names another. A `states:`
graph is read at run time from the Version the Routine is bound to; Install
writes only the display hints it adds to those Columns.

```yaml
states:
  table: tracker
  status: {column: Status, ctas_column: CTAs}
  machines:
    funnel:
      column: Stage
      states:
        new_lead: {label: New lead}
        retained: {label: Retained, tone: black, terminal: true}
      groups: {undecided: [new_lead]}
    tracking:
      column: Tracking Mode
      overlay: true
      states:
        paused: {label: Paused, tone: gray}
  events:
    staff: [retain, pause, resume]
  transitions:
    - on: staff.retain
      from: undecided
      to: funnel.retained
      expected: true
      writes: {Decision: retain}
      cta: {kind: retain, label: Retain}
    - on: staff.pause
      from: tracking.none
      to: tracking.paused
      expected: true
      cta: {kind: pause, label: Pause}
    - on: staff.resume
      from: tracking.paused
      to: tracking.none
      cta: {kind: resume, label: Resume}
```

## Funnel, Overlay, derived

A **Funnel** machine carries the milestone the Row has data for — the thing
that moves forward. **Overlay** machines say what is true alongside it: what is
blocking, whether the Row is parked, what a side document is doing. An Overlay
has an implicit `none` State, because "nothing is blocking" is the common case
and should not need declaring.

A machine with a `column:` is **stored** — its value lives in that Column. A
machine without one is **derived**: the Bundle's own code decides its value from
the Row's facts and passes it to the engine when it projects or transitions a
Row. `derive: true` with a Column is both — the Bundle decides the value and the
engine mirrors it into the Column. That is the seam between the two halves.
Turning facts into machine values is the Bundle's job; everything after — values to Status, Event
to legality, what a Transition writes — belongs to the engine.

## Status is a projection, not a Column somebody writes

The Status chip is composed from the tuple by a precedence rule: the first
`status.compose` rule whose `when` holds; otherwise the first Overlay, in
declaration order, that is not `none`; otherwise the first non-overlay machine.
Nothing should hand-write it — a Transition's own writes may not touch the
projection Columns, though a plain store write is not refused — which is why changing a Row's Status means firing an Event
rather than setting a value: set the value and the next projection overwrites
it.

Because the Status vocabulary is the union of every machine's States, **two
machines may not share a State name.** A value has to identify which machine it
came from, on its own.

## Every button is an edge

In the product, the Status chip is an Item's **Status** and each button is an
**Action**.

A Transition names the Event that fires it, the States it is legal from, the
facts it writes, and the State it lands on. The button a user sees is declared
on the Transition, so the graph and the interface cannot disagree — there is no
second place where buttons are configured.

**Guards** are conditions an edge requires. Most are Column or machine-state
predicates the platform evaluates itself, combined with `all`, `any` and
negation. An edge whose rule only the Bundle's own code can answer is marked
external: it still appears in the graph, and the edge is refused unless the
caller vouches that the Guard holds. The predicate language is deliberately
small.

## An illegal graph fails at Publish, not at runtime

The whole spec is resolved when the Bundle is parsed. It fails when:

- a Transition names a State, group, Event, Guard or Flow that does not exist
- a State is unreachable, or has no **expected** edge into it — every State but
  the initial one marks the edge that is its normal way in with `expected:`
- a non-terminal State of a Funnel machine has no way out
- a terminal State is left by anything but a `system` Event
- two machines share a State name, or a Column the tier needs is not declared

This inverts the usual authoring risk, but not completely. Overlay States are
exempt from the no-way-out rule, so an Overlay can still hold a Row. And what
you can always publish is a graph that is well-formed and wrong — reachable
States that no Event fires in practice, a terminal State reached too early.
The checks prove structure, not intent.

## The Recipe: a graph each Routine can replace

A `states:` graph belongs to the template's Version (the platform calls it a
*bundle version*), so every Routine on that Version runs the same one, and
changing it means publishing a new Version.
The **Recipe** tier ships the same graph as a document of its own,
`recipe.yaml` at the Bundle's root, and lets each Routine install a revision
of its own. A Routine with [Steps](https://docs.popcorn.ai/steps.md)
of its own is running one.

```yaml
# manifest.yaml
recipe:
  document: recipe   # the channel-config document key an installed revision lives under; the default
  contract: chase    # optional: an engine contract the graph must also satisfy
```

`recipe.yaml` holds the keys a `states:` section would, and the same engine
parses and runs it, so everything above applies unchanged, Publish checks
included. What differs is where the graph lives:

- **A Bundle declares `states:` or `recipe:`, never both.** `recipe:` needs a
  `tables:` section, as `states:` does. Publish refuses a `recipe:` with no
  `recipe.yaml`, and a `recipe.yaml` with no `recipe:`.
- **The Bundle's own Recipe is in force until the Routine installs one.** An
  installed revision is stored in the Routine's configuration (the
  *channel config*), and the sha256 of its text is its identity. Earlier
  revisions stay readable, so a Routine can go back to one, or to the
  Bundle's own. An assistant does this with
  `change_routine`; a Flow, with `feature.recipe.install`.
- **An Install refuses a revision the Rows cannot follow**: one whose graph
  does not declare a value a stored machine Column holds, or that moves a
  machine to another Column or Table. Moving stored State is a migration,
  not an Install.
- **A Run pins the revision in force when it starts**, with the Routine's
  configuration, so it judges every Row by one graph whatever is installed
  meanwhile.
- **A Bundle update keeps the Routine's revision**, and first checks it
  against the new Version — the Flows its edges launch, the Tables, the
  contract. When it no longer fits, the whole update is refused before
  anything is written.

Beside the graph, a Recipe may carry sections of its own that the engine
does not read as States. `vocabulary:` sets the nouns for the Bundle's
generic words (`document: contract`), from the terms the Bundle's
`strings.yaml` declares, and they are rendered into its client copy.
`guidance:` adds the Recipe author's instructions per agent. Both are pinned
with the revision, so changing either is a new revision. A contract may read
sections of its own, such as `chase`'s `start:` and `rejection:`.

The tier was first called **process**. A Manifest's `process:` block and a
root `process.yaml` still read as `recipe:` and `recipe.yaml` (a `process:`
block's document key defaults to `process`). A Bundle that declares both
blocks, or ships both files, is refused.
