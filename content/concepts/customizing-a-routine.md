---
id: customizing-a-routine
title: Customizing a Routine
order: 2
group: Routines
summary: >
  Customizing a Routine changes it alone. Its Routine Settings, Connections,
  Instructions, References and, where its template allows, its steps stay
  with it and survive the template's improvements. A new Table or a kind of
  step the template does not offer gives it a copy of its own, which no
  longer receives those improvements and cannot be undone.
concepts: [routine-settings, instructions, routines]
layer: product
---

Customizing a Routine is changing how one Routine works without touching the
others made from the same Routine Template. There are two kinds of change, and
the difference decides whether the Routine keeps receiving the template's
improvements.

## Changes that stay with the Routine

Most changes belong to the Routine alone, and the template's improvements
leave them in place:

- **[Routine Settings](https://docs.popcorn.ai/product/concepts/routine-settings.md)** — a reminder
  interval, a sending mode, a schedule's cadence, the wording of an email.
  Each reaches this Routine only and can be set back.
- **[Connections](https://docs.popcorn.ai/product/concepts/connections.md)** — the accounts it
  reads from and books into.
- **[Instructions](https://docs.popcorn.ai/product/concepts/instructions.md)** — what its agent
  should do and how.
- **[References](https://docs.popcorn.ai/product/concepts/reference-documents.md)** — the
  documents it works from.
- **Its steps**, where its template keeps them with the Routine: what each
  step asks for, their order, their wording, and where the Routine stops for
  a person's review. A person changes them by telling the Routine's agent in
  Popcorn, and an earlier version, or the template's own, can be put back.
  Popcorn refuses a change that would remove a step items are still at. No
  assistant tool changes steps yet.

Check the settings first. Most "can it do X differently" questions are a
setting, and `list_routine_settings` with a `query` finds it.

## Changes that give it a copy of its own

A change to what the Routine is built from — a new Table, a new Column, a
kind of step its template does not offer, or any change to the steps of a
template that does not keep them with the Routine — cannot be a setting. Making it gives the Routine
a copy of its own template. From then on:

- it no longer receives the template's improvements;
- the copy is the workspace's, and a change to it reaches every Routine on the
  same copy, within a day;
- it cannot be undone: a Routine never returns to receiving the template's
  improvements.

Popcorn says which kind a change is before making it: every change an
assistant makes is a dry run first, and the dry run for a copy of its own says
so. `get_routine` shows which kind a Routine is today, as **Updates from**:
Popcorn, or this workspace's own copy.

> **Platform note** — A copy of its own is a *fork line*: the workspace's own
> version series of the template, changed by publishing to it. See
> [Fork lines](https://docs.popcorn.ai/platform/concepts/fork-line.md), and
> [authoring an app bundle](https://docs.popcorn.ai/platform/guides/template-authoring.md) for
> making the change itself.
