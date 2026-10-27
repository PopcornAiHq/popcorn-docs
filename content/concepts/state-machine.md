---
id: state-machine
title: State machines in a bundle
order: 8
group: What a bundle holds
summary: >
  A Routine's Status and Actions come from state machines its template
  declares — states, transitions, and the button on each edge — which the
  platform runs. Status is a projection, so it changes by firing an event; a
  value written to the column lasts until the next projection. The graph is
  a manifest `states:` section or a `recipe.yaml` each Routine can replace.
  Publish proves structure only.
concepts: [manifest-keys, channel-binding, states-authoring, app-bundle]
layer: platform
product_terms: [Status, Action]
---

An item's Status, and the Actions it offers, are not one flat field.
Underneath, a row of the table the machines run over is a **tuple of small
machines**, and the single chip a user sees is a projection of that tuple.

A bundle declares the machines, their states, and the transitions between them
in its manifest's `states:` section, or in a recipe the Routine can replace
(the last section below). The platform ships the engine and runs the graph; the bundle
ships the graph and the vocabulary. The platform knows none of your state
names — only its own few words: `none`, `same`, and the `system` and `staff`
event families.

`states:` needs a `tables:` section, and the table it names must declare every
column the tier reads or writes — here `Status`, `CTAs`, `Stage`,
`Tracking Mode`, `Decision`, and `Why`, where the reason for the last
transition is written unless `status.why_column` names another. A `states:`
graph is read at run time from the version the Routine is bound to; install
writes only the display hints it adds to those columns.

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

## Funnel, overlay, derived

A **funnel** machine carries the milestone the row has data for — the thing
that moves forward. **Overlay** machines say what is true alongside it: what is
blocking, whether the row is parked, what a side document is doing. An overlay
has an implicit `none` state, because "nothing is blocking" is the common case
and should not need declaring.

A machine with a `column:` is **stored** — its value lives in that column. A
machine without one is **derived**: the bundle's own code decides its value from
the row's facts and passes it to the engine when it projects or transitions a
row. `derive: true` with a column is both — the bundle decides the value and the
engine mirrors it into the column. That is the seam between the two halves.
Turning facts into machine values is the bundle's job; everything after — values to status, event
to legality, what a transition writes — belongs to the engine.

## Status is a projection, not a column somebody writes

The status chip is composed from the tuple by a precedence rule: the first
`status.compose` rule whose `when` holds; otherwise the first overlay, in
declaration order, that is not `none`; otherwise the first non-overlay machine.
Nothing should hand-write it — a transition's own writes may not touch the
projection columns, though a plain store write is not refused — which is why changing a row's status means firing an event
rather than setting a value: set the value and the next projection overwrites
it.

Because the status vocabulary is the union of every machine's states, **two
machines may not share a state name.** A value has to identify which machine it
came from, on its own.

## Every button is an edge

In the product, the status chip is an item's **Status** and each button is an
**Action**.

A transition names the event that fires it, the states it is legal from, the
facts it writes, and the state it lands on. The button a user sees is declared
on the transition, so the graph and the interface cannot disagree — there is no
second place where buttons are configured.

**Guards** are conditions an edge requires. Most are column or machine-state
predicates the platform evaluates itself, combined with `all`, `any` and
negation. An edge whose rule only the bundle's own code can answer is marked
external: it still appears in the graph, and the edge is refused unless the
caller vouches that the guard holds. The predicate language is deliberately
small.

## An illegal graph fails at publish, not at runtime

The whole spec is resolved when the bundle is parsed. It fails when:

- a transition names a state, group, event, guard or flow that does not exist
- a state is unreachable, or has no **expected** edge into it — every state but
  the initial one marks the edge that is its normal way in with `expected:`
- a non-terminal state of a funnel machine has no way out
- a terminal state is left by anything but a `system` event
- two machines share a state name, or a column the tier needs is not declared

This inverts the usual authoring risk, but not completely. Overlay states are
exempt from the no-way-out rule, so an overlay can still hold a row. And what
you can always publish is a graph that is well-formed and wrong — reachable
states that no event fires in practice, a terminal state reached too early.
The checks prove structure, not intent.

## The recipe: a graph each Routine can replace

A `states:` graph belongs to the template's version (the platform calls it a
*bundle version*), so every Routine on that version runs the same one, and
changing it means publishing a new version.
The **recipe** tier ships the same graph as a document of its own,
`recipe.yaml` at the bundle's root, and lets each Routine install a revision
of its own. A Routine with [Steps](https://docs.popcorn.ai/product/concepts/steps.md)
of its own is running one.

```yaml
# manifest.yaml
recipe:
  document: recipe   # the channel-config document key an installed revision lives under; the default
  contract: chase    # optional: an engine contract the graph must also satisfy
```

`recipe.yaml` holds the keys a `states:` section would, and the same engine
parses and runs it, so everything above applies unchanged, publish checks
included. What differs is where the graph lives:

- **A bundle declares `states:` or `recipe:`, never both.** `recipe:` needs a
  `tables:` section, as `states:` does. Publish refuses a `recipe:` with no
  `recipe.yaml`, and a `recipe.yaml` with no `recipe:`.
- **The bundle's own recipe is in force until the Routine installs one.** An
  installed revision is stored in the Routine's configuration (the
  *channel config*), and the sha256 of its text is its identity. Earlier
  revisions stay readable, so a Routine can go back to one, or to the
  bundle's own. An assistant does this with
  `change_routine`; a flow, with `feature.recipe.install`.
- **An install refuses a revision the rows cannot follow**: one whose graph
  does not declare a value a stored machine column holds, or that moves a
  machine to another column or table. Moving stored state is a migration,
  not an install.
- **A run pins the revision in force when it starts**, with the Routine's
  configuration, so it judges every row by one graph whatever is installed
  meanwhile.
- **A bundle update keeps the Routine's revision**, and first checks it
  against the new version — the flows its edges launch, the tables, the
  contract. When it no longer fits, the whole update is refused before
  anything is written.

Beside the graph, a recipe may carry sections of its own that the engine
does not read as states. `vocabulary:` sets the nouns for the bundle's
generic words (`document: contract`), from the terms the bundle's
`strings.yaml` declares, and they are rendered into its client copy.
`guidance:` adds the recipe author's instructions per agent. Both are pinned
with the revision, so changing either is a new revision. A contract may read
sections of its own, such as `chase`'s `start:` and `rejection:`.

The tier was first called **process**. A manifest's `process:` block and a
root `process.yaml` still read as `recipe:` and `recipe.yaml` (a `process:`
block's document key defaults to `process`). A bundle that declares both
blocks, or ships both files, is refused.
