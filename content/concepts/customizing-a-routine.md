---
id: customizing-a-routine
title: Customizing a Routine
order: 4
group: Routines
summary: >
  Customizing a Routine changes it alone. Its Routine Settings, Connections,
  Instructions, References and, where its template allows, its Steps stay
  with it and survive the template's improvements. A new Table or a kind of
  Step the template does not offer gives it a Copy of its own, which no
  longer receives those improvements and cannot be undone.
lede: >
  What you can change about one Routine without affecting any other, and what
  takes a Copy of its template.
concepts: [routine-settings, instructions, routines, copying-a-template]
part: use
---

Customizing a Routine is changing how one Routine works without touching the
others made from the same Routine Template. There are two kinds of change, and
the difference decides whether the Routine keeps receiving the template's
improvements.

## Changes that stay with the Routine

Most changes belong to the Routine alone, and the template's improvements
leave them in place:

- **[Routine Settings](https://docs.popcorn.ai/use/concepts/routine-settings.md)** — a reminder
  interval, a sending mode, a Schedule's cadence, the wording of an email.
  Each reaches this Routine only and can be set back.
- **[Connections](https://docs.popcorn.ai/use/concepts/connections.md)** — the accounts it
  reads from and books into.
- **[Instructions](https://docs.popcorn.ai/use/concepts/instructions.md)** — what its Agent
  should do and how.
- **[References](https://docs.popcorn.ai/use/concepts/reference-documents.md)** — the
  documents it works from.
- **Its Steps**, where its template keeps them with the Routine: what each
  Step asks for, their order, their wording, and where the Routine stops for
  a person's Review. A person changes them by describing the change, to the
  Routine's Agent in Popcorn or to an assistant with `change_routine`, and
  an earlier Version, or the template's own, can be put back. Popcorn
  refuses a change that would remove a Step Items are still at.

Check the settings first. Most "can it do X differently" questions are a
setting, and `list_routine_settings` with a `query` finds it.

## Changes that give it a Copy of its own

A change to what the Routine is built from — a new Table, a new Column, a
kind of Step its template does not offer, or any change to the Steps of a
template that does not keep them with the Routine — cannot be a setting. Making it gives the Routine
a Copy of its own template. From then on:

- it no longer receives the template's improvements;
- the Copy is the Workspace's, and a change to it reaches every Routine on the
  same Copy, within a day;
- it cannot be undone: a Routine never returns to receiving the template's
  improvements.

Popcorn says which kind a change is before making it: every change an
assistant makes is a dry run first, and the dry run for a Copy of its own says
so. `get_routine` shows which kind a Routine is today, as **Updates from**:
Popcorn, or this Workspace's own Copy.

A Copy of its own is the Workspace's own series of Versions of the template
(the CLI calls it a *fork line*), and a change reaches it by publishing a new
Version. [Copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md)
says what a Copy costs and how to make one, and
[authoring an App Bundle](https://docs.popcorn.ai/build/guides/template-authoring.md)
how to make the change itself.
