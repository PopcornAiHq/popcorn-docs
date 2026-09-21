---
id: channel-binding
title: How a channel runs a version
summary: >
  A channel points at exactly one bundle version, and that single reference is
  the whole binding — flows and code are resolved through it at run start and
  pinned for the run, so an upgrade mid-run never mixes versions.
concepts: [bundle-version, fork-line]
applies_to: [cli, mcp, human]
source: [bind_version_internal, get_flow_bytes_pinned]
---

A channel points at exactly one bundle version. That single reference is the
entire binding: the channel stores no copy of the flows, the tables, or the
code. Upgrading a channel is one write.

## Resolved through the binding, pinned for the run

When a flow starts, the platform reads the channel's bound version once and
records it for that run. Everything the run needs — the flow definition, any
code block it calls — is then read from *that* version, and nothing resolves
through the channel again.

Two consequences worth holding on to:

- **A channel upgraded mid-run does not affect the run.** The old flow keeps
  pairing with the old code until it ends. A flow and the code it calls are
  published, versioned and upgraded together, and never mix.
- **A replay reads the same version.** The pin lives in the run's history, so
  re-executing an old run cannot silently pick up newer files.

## Bound is not always head

The version a channel runs is *bound*. The newest version available to it is
*head*. They differ whenever an install has not landed yet — and that window is
exactly when reading the wrong one is most expensive. Reads default to bound,
because that is what is live; a publish must be based on head.
