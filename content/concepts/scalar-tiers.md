---
id: scalar-tiers
title: Scalar tiers and Routine Settings
order: 4
group: What a bundle holds
summary: >
  Many Routine Settings are scalars, and a manifest writes them in one of two
  tiers. `scalars:` are written on first install and fast-forwarded on update
  unless the Routine changed them. `default_scalars:` write once, only if
  absent — the tier for an operator-owned switch and for `popcorn.*` keys such
  as the send mode. Never declare a value a flow writes at runtime.
concepts: [manifest-keys]
layer: platform
product_terms: [Routine Settings]
---

Scalars are one source of a Routine's
[Routine Settings](https://docs.popcorn.ai/product/concepts/routine-settings.md).
The `default_scalars:` tier, `popcorn.*` keys included, is where a Routine's
switch-type settings come from; the `scalars:` tier is configuration the
template owns, not a setting. Channel parameters and the `prompts/` and
`templates/` files are the other sources of settings, outside this page. Many
of a Routine's Settings — its switches and its send modes — are scalars
underneath. A scalar is a named string on a Routine — always a string on the
wire, unlike a channel parameter, which keeps its declared type. Two
manifest tiers write them, a third family of keys is reserved by the
platform, and choosing the wrong one is how a setting resets.

| Tier | Written | Use it for |
|---|---|---|
| `scalars:` | on install; on an update, only where the Routine still holds the old bundle's value | install-time configuration the bundle owns |
| `default_scalars:` | on the **first** install only, and only if absent | an operator-owned switch that ships with an opinion |
| platform (`popcorn.*`) | only through `default_scalars:` | reserved — see below |

## What an update does to a declared scalar

An update — the install a publish starts, `app apply`, and the daily
auto-update — compares each declared key three ways: the Routine's current
value, the value the old version declared, and the value the new one declares.

- current is missing → the new value is written
- current equals the old declared value → the new value is written
- anything else → the Routine's value is kept

So a member's edit survives an update. A fresh install into a Routine, or an
install by the Routine Template's name rather than by version, writes every
declared scalar unconditionally.

## Runtime state belongs in none of them

A flow-written value — a cursor, a last-swept timestamp — declared under
`scalars:` is still owned by install. A fresh install resets it. An update
keeps it only because it has drifted from the declared value, and overwrites
it whenever it has not — a cursor that is still at its declared starting value
is reset to whatever the new version declares.

Declare only what install should own. Let flows create their own keys; nothing
requires a scalar to be declared before it is written. `app validate` warns
with `runtime-state-in-scalars` when a flow sets a scalar the manifest also
declares.

## `popcorn.*` is reserved

Keys beginning `popcorn.` are a platform convention, not something a template defines. Every
Routine Template reads the same keys with the same meaning, so an operator learns one
set of switches rather than one per template.

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
convention, for a template whose mail and binding documents need separate
consent.

`popcorn.app_mode: test` runs a logical day in one wall-clock minute, so a
multi-week process can be exercised in minutes; `off` is dormant. A template's
own `set_app_mode` flow, where it has one, also retunes the Routine's schedules
for `test` and pauses them for `off`. `popcorn.app_gate` restricts only what
a template that defines rollout levels initiates, and `popcorn.app_agent: off`
stops agent runs only in the `app.*` activities that honour it. The last two fail
open, the send modes fail closed.

Declare none of them under `scalars:`.

The convention is not enforced, which is why it matters: nothing refuses a
`popcorn.*` key under `scalars:`, and declaring one there makes install the
owner of a switch that belongs to the operator. Where a bundle wants to ship
an opinion about one, `default_scalars:` is the sanctioned way — it cannot move
a Routine that already has a value.

A Routine's scalars that a person sets, from `default_scalars:`, and its
channel parameters are its **Routine Settings**; over MCP, `list_routine_settings` lists them. What a
template *shows* in its settings panel is a separate, deliberately smaller
choice: the bundle promotes candidates into the panel through `strings.yaml`,
and anything unpromoted stays readable in the developer view.
