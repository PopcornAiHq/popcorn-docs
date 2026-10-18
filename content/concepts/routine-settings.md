---
id: routine-settings
title: Routine Settings
order: 8
group: How it behaves
summary: >
  Routine Settings tune one Routine without changing what it does: switches
  such as a sending mode, values such as how many days it waits between
  reminders or a schedule's cadence, and the wording of its emails and
  prompts. A setting reaches only its own Routine, can be set back, and
  survives the template's improvements. list_routine_settings finds one;
  update_routine_setting changes it.
concepts: [customizing-a-routine, change-how-a-routine-behaves, triggers]
layer: product
---

Routine Settings are the values that tune a Routine without changing what it
does: switches that turn a behaviour on or off, values such as a reminder
interval, a follow-up limit or a schedule's cadence, and the prompts and email
wording its agent uses. They are the first place to look when a Routine
should behave differently.

A setting:

- reaches this Routine only, never the others made from the same template;
- can be set back, by setting it to the template's default;
- is kept through the template's improvements.

## Reading them

`list_routine_settings` lists every setting the Routine's template offers,
set or not. Each row shows its value; an unset one says what unset means, and
one changed from the template's default says so. A `query` narrows the list
by key or label ("chase", "reminder"). A secret shows only whether it is set.

`get_routine_setting` shows one setting in full: its whole value — a prompt
or email's whole text — the template's default, what it accepts, its options
with the warning each carries, and who may change it.

## Changing one

`update_routine_setting` changes one setting on one Routine. The first call
is a dry run that shows the old and new value and what the setting does;
`confirm=true` makes the change. A switch takes one of its options; any other
setting keeps the shape of its default, so a list stays a list. A long text is
changed with edits to the current text rather than resent whole. Work already
under way keeps the value it started with.

Secrets, and the Routine's [Instructions](https://docs.popcorn.ai/product/concepts/instructions.md),
are not changed here; they change in Popcorn. The walkthrough is
[changing how a Routine behaves](https://docs.popcorn.ai/product/guides/change-how-a-routine-behaves.md).

> **Platform note** — Many settings are a channel's *scalars* or *channel
> parameters*, and the prompts and email templates are files the template
> seeds. See [the three scalar tiers](https://docs.popcorn.ai/platform/concepts/scalar-tiers.md).
