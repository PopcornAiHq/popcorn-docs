---
id: scalar-tiers
title: The three scalar tiers
order: 4
summary: >
  `scalars:` are written on first install and fast-forwarded on update unless
  the channel changed them. `default_scalars:` write once, only if absent — the
  manifest tier for an operator-owned switch and for platform `popcorn.*` keys
  such as the outbound send mode. Never declare a value a flow writes at
  runtime: declaring it hands it to install, which can reset it.
concepts: [manifest-keys]
applies_to: [cli, mcp, human]
source: [PLATFORM_SETTINGS, candidate_settings, filter_update_scalar_pairs, parse_send_mode, parse_app_mode]
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
switches rather than one per app.

| Key | Values | Unset or unrecognised reads as |
|---|---|---|
| `popcorn.email_send_mode` | `off`, `draft`, `send` | `off` |
| `popcorn.sms_send_mode` | the same; reserved, nothing reads it | `off` |
| `popcorn.app_mode` | `prod`, `test`, `off` | `prod` |
| `popcorn.app_gate` | `0` (ungated) or a positive rollout level | `0` |
| `popcorn.app_agent` | `on`, `off` | `on` |

`popcorn.email_send_mode` is the one to know: only the exact strings `draft`
and `send` activate anything. E-signature requests read it too, unless the
signing step names a key of its own — `popcorn.signing_send_mode` is the
convention, for an app whose mail and binding documents need separate consent.

`popcorn.app_mode: test` runs a logical day in one wall-clock minute, so a
multi-week process can be exercised in minutes; `off` is dormant. An app's own
`set_app_mode` flow, where it has one, also retunes the channel's schedules
for `test` and pauses them for `off`. `popcorn.app_gate` restricts only what
an app that defines rollout levels initiates, and `popcorn.app_agent: off`
stops agent runs only in the app activities that honour it. The last two fail
open, the send modes fail closed.

Declare none of them under `scalars:`.

The convention is not enforced, which is why it matters: nothing refuses a
`popcorn.*` key under `scalars:`, and declaring one there makes install the
owner of a switch that belongs to the operator. Where a bundle wants to ship
an opinion about one, `default_scalars:` is the sanctioned way — it cannot move
a channel that already has a value.

What an app *shows* in its settings panel is a separate, deliberately smaller
choice: the bundle promotes candidates into the panel through `strings.yaml`,
and anything unpromoted stays readable in the developer view.
