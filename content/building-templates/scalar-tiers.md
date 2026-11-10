---
id: scalar-tiers
title: Scalar tiers and Routine Settings
order: 8
group: What a Bundle holds
summary: >
  Many Routine Settings are Scalars, written by a Manifest in two tiers.
  `scalars:` are written on first Install and fast-forwarded on update
  unless the Routine changed them. `default_scalars:` write once, only if
  absent: the tier for an operator-owned switch and `popcorn.*` keys such as
  the send mode, which Questionnaire seeds `send`. Never declare a value a
  Flow writes at runtime.
lede: >
  How a template sets a Routine's settings when it installs, and which values
  a later update can change.
concepts: [manifest-keys, routine-settings]
---

A Scalar is a named string on a Routine — always a string on the wire,
unlike a channel parameter, which keeps its declared type. Two Manifest
tiers write them, a third family of keys is reserved by the platform, and
choosing the wrong one is how a setting resets.

A Routine's [Routine Settings](https://docs.popcorn.ai/routine-settings.md)
come from three places: its switches, which are Scalars; its channel
parameters; and its `prompts/` and `templates/` files, one setting each.

> "List #team-offsite's settings."

> [!TIP] MCP tool call
> Your assistant calls `list_routine_settings`.

For `#team-offsite`, a Routine made from the
[Questionnaire](https://docs.popcorn.ai/questionnaire-template.md)
template, that is:

| Setting | Comes from |
|---|---|
| `follow_up_days`, `max_follow_ups` | `channel_parameters:` in the [Manifest](https://docs.popcorn.ai/manifest-keys.md) |
| `popcorn.email_send_mode` | `default_scalars:`, and labelled *Email sending* in `strings.yaml` |
| the other `popcorn.*` keys | the platform: every Routine has them, set or not (below) |
| `prompts.read_answers`, `prompts.read_questionnaire` | the `prompts/` files |

Questionnaire's `scalars:` tier, `coordinator_name`, `agent_runnable_flows`
and `agent_summary`, is configuration the template owns, and not a
setting.

> [!NOTE] Who can change one
> A Member of the Routine can change a switch such as
> `popcorn.email_send_mode`. A channel parameter or a prompt, such as
> `follow_up_days`, needs a Workspace admin who is also a Member.

## The tiers

| Tier | Written | Use it for | In Questionnaire |
|---|---|---|---|
| `scalars:` | on Install; on an update, only where the Routine still holds the old Bundle's value | Install-time configuration the Bundle owns | `agent_summary`, the Agent's brief on the Routine |
| `default_scalars:` | on the **first** Install only, and only if absent | an operator-owned switch that ships with an opinion | `popcorn.email_send_mode: send` |
| platform (`popcorn.*`) | only through `default_scalars:` | reserved — see below | |

```yaml title="manifest.yaml"
# Seeded on first install only. The platform's own default is `off`; this
# template's whole job is sending email, so a new Routine sends.
default_scalars:
  popcorn.email_send_mode: send
```

So a new `#team-offsite` sends, and one switched to `draft` stays on
`draft` through every later Version of the template.

## What an update does to a declared Scalar

An update — the Install a Publish starts, `app apply`, and the Daily Update
— compares each declared key three ways: the Routine's current value, the
value the old Version declared, and the value the new one declares.

- current is missing → the new value is written
- current equals the old declared value → the new value is written
- anything else → the Routine's value is kept

So a Member's edit survives an update. A Copy that rewrites
`agent_summary` reaches every Routine on it that still holds the old text,
and none that changed it. A fresh Install into a Routine, or an Install by
the Routine Template's name rather than by Version, writes every declared
Scalar unconditionally.

## Runtime state belongs in none of them

A Flow-written value — a cursor, a last-swept timestamp — declared under
`scalars:` is still owned by Install. A fresh Install resets it. An update
keeps it only because it has drifted from the declared value, and overwrites
it whenever it has not — a cursor that is still at its declared starting value
is reset to whatever the new Version declares.

Declare only what Install should own. Let Flows create their own keys;
nothing requires a Scalar to be declared before it is written.
Questionnaire's Flows write three Scalars its Manifest never declares:
`questionnaire`, the questions read from the Reference; `questionnaire_file`,
where that Reference is stored; and `questionnaire.reply_by`, the reply-by
date. None of them is a Routine Setting: the reply-by date changes when its
`reply_by_set` Flow runs again. `app validate` warns with
`runtime-state-in-scalars` when a Flow sets a Scalar the Manifest also
declares.

## `popcorn.*` is reserved

Keys beginning `popcorn.` are a platform convention, not something a
template defines. Every Routine Template reads the same keys with the same
meaning, so an operator learns one set of switches rather than one per
template. Every Routine lists them among its settings, whether its template
reads them or not.

| Key | Values | Unset or unrecognised reads as | Questionnaire reads it |
|---|---|---|---|
| `popcorn.email_send_mode` | `off`, `draft`, `send` | `off` | yes |
| `popcorn.sms_send_mode` | the same; reserved, nothing reads it | `off` | no |
| `popcorn.app_mode` | `prod`, `test`, `off` | `prod` | no |
| `popcorn.app_gate` | `0` (ungated) or a positive rollout level | `0` | no |
| `popcorn.app_agent` | `on`, `off` | `on` | no |
| `popcorn.agent_reply_placement` | `inline`, `thread` | the Routine's default | no; the platform does |
| `popcorn.agent_reply_mode` | `mentions`, `strict`, `eager` | the Routine's default | no; the platform does |

`popcorn.email_send_mode` is the one to know: only `draft` and `send`
activate anything. In Questionnaire, `draft` leaves each first email in
Gmail's Drafts and never follows up, and `off` asks nobody but still reads
replies. E-signature requests read it too, unless the signing Step names a
key of its own — `popcorn.signing_send_mode` is the convention, for a
template whose mail and binding documents need separate consent.

`popcorn.app_mode: test` runs a logical day in one wall-clock minute, in
the templates whose Activities honour it, so a multi-week process can be
exercised in minutes; `off` is dormant. A template's own `set_app_mode`
Flow, where it has one, also retunes the Routine's Schedules for `test` and
pauses them for `off`. `popcorn.app_gate` restricts only what a template
that defines rollout levels initiates, and `popcorn.app_agent: off` stops
Agent Runs only in the `app.*` Activities that honour it. The last two fail
open, the send modes fail closed. The two `agent_reply_*` keys decide
where the Routine's Agent answers a top-level message, and whether it
answers one that does not mention it.

> [!NOTE] Questionnaire ignores `popcorn.app_mode`
> Its follow-up days are real days whatever `popcorn.app_mode` says, and
> it has no `set_app_mode` Flow. To try it quickly, run its Schedule now
> instead.

Declare none of them under `scalars:`.

The convention is not enforced, which is why it matters: nothing refuses a
`popcorn.*` key under `scalars:`, and declaring one there makes Install the
owner of a switch that belongs to the operator. Where a Bundle wants to ship
an opinion about one, `default_scalars:` is the sanctioned way — it cannot
move a Routine that already has a value.

## Which settings a template shows

What a template *shows* in its settings panel is a separate, deliberately
smaller choice: the Bundle promotes switches into the panel under
`settings.fields` in `strings.yaml`, with a label, a description, its
options and a warning on any of them, and anything unpromoted stays
readable in the developer view. Questionnaire promotes one:

```yaml title="strings.yaml"
en:
  settings:
    fields:
      - key: popcorn.email_send_mode
        label: Email sending
        input: mode
        options:
          - value: "off"
            label: "Off"
          - value: draft
            label: Draft
          - value: send
            label: Send
            note: Real emails are sent to recipients from the connected Gmail.
```

Its `description` is left out here. The Send option's `note` is why
`update_routine_setting` shows a change to `send` before making it.
