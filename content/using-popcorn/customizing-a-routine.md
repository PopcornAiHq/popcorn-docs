---
id: customizing-a-routine
title: Customizing a Routine
order: 16
group: Customizing a Routine
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
---

Customizing a Routine is changing how one
[Routine](https://docs.popcorn.ai/routines.md) works without touching the
others made from the same Routine Template. There are two kinds of change,
and the difference decides whether the Routine keeps receiving the
template's improvements.

## Changes that stay with the Routine

Most changes belong to the Routine alone, and the template's improvements
leave them in place:

| Change | What it covers |
|---|---|
| [Routine Settings](https://docs.popcorn.ai/routine-settings.md) | a reminder interval, a sending mode, a [Schedule](https://docs.popcorn.ai/schedules.md)'s cadence, the wording of an email; each can be set back |
| [Connections](https://docs.popcorn.ai/connections.md) | the accounts it reads from and books into |
| [Instructions](https://docs.popcorn.ai/instructions.md) | what its Agent should do and how |
| [References](https://docs.popcorn.ai/reference-documents.md) | the documents it works from |
| [Steps](https://docs.popcorn.ai/steps.md), where its template keeps them with the Routine | what each Step asks for, their order, their wording, and where the Routine stops for a person's [Review](https://docs.popcorn.ai/reviews.md) |

A person changes the Steps by describing the change, to the Routine's Agent
in Popcorn or to an assistant, and an earlier
[Version](https://docs.popcorn.ai/versions.md), or the template's own, can
be put back. Popcorn refuses a change that would remove a Step Items are
still at.

> [!TIP] Check the settings first
> Most "can it do X differently" questions are a setting.
> [Change how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md)
> walks through finding and changing one.

## Changes that give it a Copy of its own

Some changes are to what the Routine is built from, and can't be a setting:

- a new [Table](https://docs.popcorn.ai/tables.md) or a new Column;
- a kind of Step its template doesn't offer;
- any change to the Steps of a template that doesn't keep them with the
  Routine.

Making one gives the Routine a
[Copy](https://docs.popcorn.ai/copying-a-template.md) of its own template.
The Copy is the Workspace's, and a change to it reaches every Routine on the
same Copy within a day.

> [!CAUTION] A Copy is for good
> From then on the Routine no longer receives the template's improvements,
> and it never returns to them.

Popcorn says which kind a change is before making it: a change that needs
a Copy of its own is always a dry run first, and the dry run says so.

> [!TIP] Which kind a Routine is today
> A Routine's details show it as **Updates from**: Popcorn, or this
> Workspace's own Copy.

A Copy of its own is the Workspace's own series of Versions of the template
(the CLI calls it a *fork line*), and a change reaches it by publishing a
new Version.
[Copying a template](https://docs.popcorn.ai/copying-a-template.md) says what a Copy costs and how to make one, and
[changing a Routine Template](https://docs.popcorn.ai/template-authoring.md)
how to make the change itself.
