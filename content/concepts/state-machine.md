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

<!-- BODY TODO — THE FIRST COMMISSION. This tier shipped with a substantial
     engine and no authoring documentation at all; the authoring guide does
     not mention it.
     Cover: machine, overlay, derived machine, projection, guard, and edge;
     that a row's status is a projection of a tuple of machines rather than a
     column somebody writes; that the graph is checked at parse time
     (unreachable states, dead ends, ambiguous edges) so an illegal graph
     fails at publish; and that a per-app rendering — including the generated
     diagram — is reference, not concept. -->
