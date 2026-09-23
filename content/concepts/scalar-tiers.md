---
id: scalar-tiers
title: The three scalar tiers
summary: >
  Declared scalars are written on first install and fast-forwarded on update
  unless the channel changed them. Default scalars write once, only if absent —
  the tier for an operator-owned switch. Platform `popcorn.*` keys, such as the
  outbound send mode, ship only through default scalars. Never declare a value a
  flow writes at runtime: declaring it hands it to install, which can reset it.
concepts: [manifest-keys]
applies_to: [cli, mcp, human]
source: [PLATFORM_SETTINGS, candidate_settings, filter_update_scalar_pairs]
---

A scalar is a named string on a channel. Two manifest tiers write them, a
third family of keys is reserved by the platform, and choosing the wrong one is
how a setting resets.

| Tier | Written | Use it for |
|---|---|---|
| `scalars:` | on install; on an update, only where the channel still holds the old bundle's value | install-time configuration the bundle owns |
| `default_scalars:` | on the **first** install only, and only if absent | an operator-owned switch that ships with an opinion |
| platform (`popcorn.*`) | only through `default_scalars:` | reserved — see below |

## What an update does to a declared scalar

An update — the install a publish starts, `app apply`, and the daily
auto-update — compares each declared key three ways: the channel's current
value, the value the old version declared, and the value the new one declares.

- current is missing → the new value is written
- current equals the old declared value → the new value is written
- anything else → the channel's value is kept

So a member's edit survives an update. A fresh install into a channel, or an
install by app name rather than by version, writes every declared scalar
unconditionally.

## Runtime state belongs in none of them

A flow-written value — a cursor, a last-swept timestamp — declared under
`scalars:` is still owned by install. A fresh install resets it. An update
keeps it only because it has drifted from the declared value, and overwrites
it whenever it has not — a cursor that is still at its declared starting value
is reset to whatever the new version declares.

Declare only what install should own. Let flows create their own keys; nothing
requires a scalar to be declared before it is written. `template check` warns
with `runtime-state-in-scalars` when a flow sets a scalar the manifest also
declares.

## `popcorn.*` is reserved

Keys beginning `popcorn.` are a platform convention, not app state. Every app
reads the same keys with the same meaning, so an operator learns one set of
switches rather than one per app. The outbound send modes — email and
signing — are the ones to know: each is `off` unless set to `draft` or
`send`, and any other value, unset included, reads as `off`.

The convention is not enforced, which is why it matters: nothing refuses a
`popcorn.*` key under `scalars:`, and declaring one there makes install the
owner of a switch that belongs to the operator. Where a bundle wants to ship
an opinion about one, `default_scalars:` is the sanctioned way — it cannot move
a channel that already has a value.

What an app *shows* in its settings panel is a separate, deliberately smaller
choice: the bundle promotes candidates into the panel through `strings.yaml`,
and anything unpromoted stays readable in the developer view.
