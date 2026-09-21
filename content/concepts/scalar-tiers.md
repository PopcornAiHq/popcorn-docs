---
id: scalar-tiers
title: The three scalar tiers
summary: >
  Declared scalars upsert on every install, default scalars write once on first
  install only, and platform scalars are reserved and belong in neither. Put a
  value a flow writes at runtime in the first tier and every reinstall resets
  it.
concepts: [manifest-keys]
applies_to: [cli, mcp, human]
source: [PLATFORM_SETTINGS, candidate_settings]
---

A scalar is a named string on a channel. Three tiers write them, and choosing
the wrong one is how a setting silently resets.

| Tier | Written | Use it for |
|---|---|---|
| `scalars:` | on **every** install | install-time configuration the bundle owns |
| `default_scalars:` | on the **first** install only, and only if absent | an operator-owned switch that ships with an opinion |
| platform (`popcorn.*`) | never by a manifest | reserved — see below |

## Runtime state belongs in none of them

If a flow writes a scalar — a cursor, a last-swept timestamp, a counter of
sorts — and the manifest also declares it under `scalars:`, then **every
re-install resets it**, including the automatic ones that follow a publish.

Declare only what install should own. Let flows create their own keys; nothing
requires a scalar to be declared before it is written.

The offline checker warns when it sees a flow write a scalar the manifest also
declares, which is usually this mistake.

## `popcorn.*` is reserved

Keys beginning `popcorn.` are a platform convention, not app state. Every app
reads the same keys with the same meaning, so an operator learns one set of
switches rather than one per app — outbound send mode is the one to know, and
its default is off, so only an exact opt-in activates anything.

They are never declared under `scalars:`, because an upsert on every install
would reset a live channel's choice. Where a bundle wants to ship an opinion
about one, `default_scalars:` is the sanctioned way: it cannot move a channel
that already has a value.

What an app *shows* in its settings panel is a separate, deliberately smaller
choice than what it may read.
