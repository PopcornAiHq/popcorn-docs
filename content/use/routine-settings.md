---
id: routine-settings
title: Routine Settings
order: 14
group: Changing a Routine
summary: >
  Routine Settings tune one Routine without changing what it does: whether
  Popcorn sends its emails or writes them as drafts to check, the days between
  reminders, the wording of its emails and prompts. A setting reaches only its
  own Routine, can be set back, and survives the template's improvements.
  list_routine_settings finds one; update_routine_setting changes it.
lede: >
  Routine Settings tune one Routine, such as whether it sends emails or saves
  them as drafts, without changing what it does.
concepts: [customizing-a-routine, change-how-a-routine-behaves, triggers]
---

Routine Settings are the values that tune a Routine without changing what it
does: switches that turn a behaviour on or off, values such as a reminder
interval, a follow-up limit or a Schedule's cadence, and the prompts and email
wording its Agent uses. They are the first place to look when a Routine
should behave differently.

A setting:

- reaches this Routine only, never the others made from the same template;
- can be set back, by setting it to the template's default;
- is kept through the template's improvements.

A claims intake Routine's settings include:

| Setting | What it decides |
|---|---|
| Email sending | *Off*, *Draft* (each email is written for a person to send) or *Send* |
| Agreement sending | the same three, for sending agreements through the Signing Provider |
| Reply matching | whether a reply is matched to its Item by the sender's address, or by the email thread (for an inbox several Routines share) |
| Save signed agreements to Google Drive | whether each signed agreement is filed in a folder for its client |
| Booking confirmation | whether someone who books a meeting gets a short note confirming it |
| Step forward | whether people can move an Item past a Step done outside Popcorn (see [Reviews](https://docs.popcorn.ai/reviews.md)) |
| Reminder schedule, outreach hours | when follow-ups go out, and the hours emails may be sent in |

The names follow the Routine's own words, so a Routine that sends a retainer
says "Retainer sending".

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

Secrets, and the Routine's [Instructions](https://docs.popcorn.ai/instructions.md),
are not changed here; they change in Popcorn. The walkthrough is
[changing how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md).

In the template, many settings are the Routine's Scalars or its
`channel_parameters:`, and the prompts and email templates are files the template
seeds; [Scalar tiers and Routine Settings](https://docs.popcorn.ai/scalar-tiers.md)
says which declarations become settings.
