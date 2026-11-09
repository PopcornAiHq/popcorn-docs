---
id: routine-settings
title: Routine Settings
order: 17
group: Customizing a Routine
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

Routine Settings are the values that tune a
[Routine](https://docs.popcorn.ai/routines.md) without changing what it
does. They are the first place to look when a Routine should behave
differently, and come in three kinds:

- **Switches** that turn a behaviour on or off, or pick one of a few modes.
- **Values** such as a reminder interval, a follow-up limit or a
  [Schedule](https://docs.popcorn.ai/triggers.md)'s cadence.
- **Wording**: the prompts and email text the Routine's
  [Agent](https://docs.popcorn.ai/agent.md) writes from.
  Each prompt or email is its own setting.

A setting:

- reaches this Routine only, never the others made from the same template;
- can be set back, by setting it to the template's default;
- is kept through the template's improvements.

## An example

`#team-offsite`'s settings include:

| Setting | What it decides |
|---|---|
| Email sending | *Off* (nobody is asked), *Draft* (each first email waits in Gmail's Drafts for a person to send) or *Send* |
| Days between follow-ups | how long it waits before following up, 3 by default |
| Follow-ups before giving up | how many follow-ups it sends before someone is *No response*, 3 by default |
| `prompts.read_questionnaire`, `prompts.read_answers` | the prompts it reads the questionnaire and each reply with |

A claims intake Routine has more, such as *Agreement sending* for the
Signing Provider, *Reply matching* for an inbox several Routines share, and
*Step forward* for moving an
[Item](https://docs.popcorn.ai/work-a-routines-items.md) past a Step done
outside Popcorn (see [Reviews](https://docs.popcorn.ai/reviews.md)).

The names follow the Routine's own words, so a Routine that sends a retainer
says "Retainer sending".

## Finding and changing one

Ask your assistant what you can change about a Routine, and it lists the
settings that match: each one's value, and whether it was changed from the
template's default. It can show one in full, with its options and the
warning each carries, and change it for you.
[Change how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md)
walks through it.

> [!TIP] MCP tool call
> `list_routine_settings` finds a setting, `get_routine_setting` shows one
> in full, and `update_routine_setting` changes one.

> [!NOTE] Not settings
> A secret shows only whether it is set, and is changed in Popcorn. The
> Routine's [Instructions](https://docs.popcorn.ai/instructions.md), apart
> from the wording that is a setting, change elsewhere: that page says
> where.

> [!TIP] In the template
> Many settings are the template's Scalars or its `channel_parameters:`,
> and the prompts and email templates are files the template seeds.
> [Scalar tiers and Routine Settings](https://docs.popcorn.ai/scalar-tiers.md)
> says which declarations become settings.
