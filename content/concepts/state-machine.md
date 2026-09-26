---
id: state-machine
title: State machines in a bundle
order: 6
group: What a bundle holds
summary: >
  A bundle declares its own state machines — states, transitions, and the
  button on each edge — and the platform runs them. A row's status is a
  projection of those machines, so it changes by firing an event; a value
  written to the column lasts until the next projection. Publish proves the graph's structure; its intent is the
  author's to check — states no event fires, terminals reached too early.
concepts: [manifest-keys, channel-binding, states-authoring]
applies_to: [cli, mcp, human]
source: [StatesSpec, parse_states, project_row]
---

A tracker row is not one flat status. It is a **tuple of small machines**, and
the single chip a user sees is a projection of that tuple.

A bundle declares the machines, their states, and the transitions between them
in its manifest. The platform ships the engine and runs the graph; the bundle
ships the graph and the vocabulary. The platform knows none of your state
names — only its own few words: `none`, `same`, and the `system` and `staff`
event families.

`states:` needs a `tables:` section, and the table it names must declare every
column the tier reads or writes — here `Status`, `CTAs`, `Stage`,
`Tracking Mode`, `Decision`, and `Why`, where the reason for the last
transition is written unless `status.why_column` names another. The graph is
read at run time from the version the channel is bound to; install writes
only the display hints it adds to those columns.

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
