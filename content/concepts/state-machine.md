---
id: state-machine
title: State machines in a bundle
summary: >
  A bundle declares its own state machine — states, legal transitions, and
  which action fires from where — and the platform runs it. Nothing in the
  platform knows an app's state names, so what a status means is the app's to
  state and is read from the version a channel runs.
concepts: [manifest-keys, channel-binding]
applies_to: [cli, mcp, human]
source: [StatesSpec, parse_states, project_row]
---

A tracker row is not one flat status. It is a **tuple of small machines**, and
the single chip a user sees is a projection of that tuple.

A bundle declares the machines, their states, and the transitions between them
in its manifest. The platform ships the engine and runs the graph; the bundle
ships the graph and the vocabulary. Nothing in the platform knows a single one
of your state names.

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
        not_tracking: {label: Not tracking, tone: gray}
  events:
    staff: [retain]
  transitions:
    - on: staff.retain
      from: undecided
      to: funnel.retained
      writes: {Decision: retain}
      cta: {kind: retain, label: Retain}
```

## Funnel, overlay, derived

A **funnel** machine carries the milestone the row has data for — the thing
that moves forward. **Overlay** machines say what is true alongside it: what is
blocking, whether the row is parked, what a side document is doing. An overlay
has an implicit `none` state, because "nothing is blocking" is the common case
and should not need declaring.

A machine with a `column:` is **stored** — its value lives in that column. A
machine without one is **derived**: the bundle's own code decides its value from
the row's facts. That is the seam between the two halves. Turning facts into
machine values is the bundle's job; everything after — values to status, event
to legality, what a transition writes — belongs to the engine.

## Status is a projection, not a column somebody writes

The status chip is composed from the tuple by a precedence rule. Nothing
hand-writes it, which is why changing a row's status means firing an event
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

**Guards** are conditions an edge requires. Most are simple column predicates
the platform evaluates itself. An edge whose rule only the bundle's own code can
answer is marked external: it still appears in the graph, and a legality check
reports it as delegated rather than deciding it. The predicate language is
deliberately small.

## An illegal graph fails at publish, not at runtime

The whole spec is resolved when the bundle is parsed. A transition naming a
state, group, event or guard that does not exist fails. So does a state nothing
can reach, a non-terminal state with no way out, and the shared-state-name
clash above.

This is worth knowing because it inverts the usual authoring risk: you cannot
publish a graph that strands a row. What you *can* still publish is a graph that
is well-formed and wrong — reachable states that no event ever fires in
practice, a terminal state reached too early. The checks prove structure, not
intent.
