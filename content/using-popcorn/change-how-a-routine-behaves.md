---
id: change-how-a-routine-behaves
title: Change how a Routine behaves
order: 13
group: Customizing a Routine
summary: >
  Changing how one Routine behaves: find the Routine Setting that covers it
  with list_routine_settings, read it in full with get_routine_setting, and
  change it with update_routine_setting. A setting stays with that Routine
  and can be set back. Otherwise: its Steps, with change_routine after
  reading the proposal; its other Instructions, in Popcorn; or a Copy of its
  own.
lede: >
  Change how one Routine behaves, starting with the settings that affect it
  alone.
concepts: [routine-settings, customizing-a-routine, instructions]
---

This guide starts from a request such as "follow up every day instead of
every three days" and ends with one
[Routine](https://docs.popcorn.ai/routines.md) behaving the new way, and
every other Routine made from the same template unchanged.

Start from the outcome, in your own words, and name the Routine it's for:
*follow up every day*, *send reminders from the claims team*, *run the
morning digest at 7*. Each step below starts with a prompt you might give
your assistant.

## Find the setting

> "What can I change about how #team-offsite follows up?"

> [!TIP] MCP tool call
> Your assistant calls `list_routine_settings` with a `query`.

Your assistant lists the
[Routine Settings](https://docs.popcorn.ai/routine-settings.md) that match:
each one's value, and whether it was changed from the template's default.
Most "can it do X differently" requests are one of these:

- a reminder interval or a follow-up limit;
- whether emails are sent or saved as drafts;
- a [Schedule](https://docs.popcorn.ai/schedules.md)'s cadence;
- the wording of an email or a prompt.

If nothing matches, skip to
[When no setting covers it](#when-no-setting-covers-it).

## Read it in full

> "Show me the follow-up setting on #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `get_routine_setting`.

Your assistant shows the whole value, the template's default, what the
setting accepts, and its options with the warning each one carries.

## Change it

> "The offsite is next week. Follow up every day on #team-offsite."

> [!TIP] MCP tool call
> Your assistant calls `update_routine_setting`.

You named the setting and its new value, so your assistant changes it
straight away. Otherwise it shows you the old and new values first, and
changes the setting once you agree.

> [!WARNING] Sending without review
> Switching from drafts to sending means emails go out without anyone
> reading them first. Your assistant always shows you this change before
> making it.

How a value changes depends on its kind:

- **A switch** takes one of its options.
- **A value** keeps the shape of its default: a list stays a list.
- **A long text**, such as an email's wording, is changed with edits to the
  current text, so the rest of it stays exactly as it was.

Work already under way keeps the value it started with; the next Run uses
the new one.

> [!NOTE] Who can change a setting
> Any Member of the Routine can change a switch, such as whether emails are
> sent. Any other setting, prompts and email wording included, needs a
> Workspace admin who is also a Member.

> [!TIP] Setting it back
> To undo the change, set the setting back to the template's default.

## When no setting covers it

Three other kinds of change remain:

- **How the Routine's Agent acts** — "ask me before sending anything to the
  carrier", "always copy the adjuster". That is its
  [Instructions](https://docs.popcorn.ai/instructions.md), which you give
  the Routine's Agent in Popcorn.
- **Its [Steps](https://docs.popcorn.ai/steps.md)** — another question
  before the agreement goes out, a
  [Review](https://docs.popcorn.ai/reviews.md) before a meeting is booked.
  When the template keeps its Steps with the Routine, your assistant can
  change them: see [Change its Steps](#change-its-steps). The change stays
  with this Routine.
- **What the Routine is built from** — a new
  [Table](https://docs.popcorn.ai/tables.md), a new kind of
  [Trigger](https://docs.popcorn.ai/triggers.md), a kind of Step its
  template doesn't offer. That means building on the template itself: see
  [changing a Routine Template](https://docs.popcorn.ai/template-authoring.md).

> [!CAUTION] A Copy is for good
> Building on the template gives the Routine a
> [Copy](https://docs.popcorn.ai/copying-a-template.md) of its own, which no
> longer receives the template's improvements. That can't be undone; read
> [customizing a Routine](https://docs.popcorn.ai/customizing-a-routine.md)
> before agreeing to it.

## Change its Steps

> "In #intake, once a claimant signs, ask them to book the interview
> straight away."

> [!TIP] MCP tool call
> Your assistant calls `change_routine` with your request, then
> `get_routine_change` to read the proposal, then `change_routine` again
> with `confirm=true` to install it.

1. **Your assistant starts the draft.** It passes on your request in your
   words. Nothing is installed yet; the Routine's Agent takes a few minutes
   to draft the change.
2. **It reads you the proposal.** The proposal shows the Steps before and
   after, what it sets on each Step, what the Agent assumed, any questions
   it left open, and the checks against the Routine's Items. If part of it
   is a Routine Setting, it says which, so that part can be changed as a
   setting instead.
3. **You agree, and it installs.** Your assistant installs the proposal
   once you agree. The install is refused if the Steps changed since the
   draft. Your assistant can then show the
   [Version](https://docs.popcorn.ai/versions.md) the Routine ran before it.

One change drafts at a time: a new request while one is drafting is refused.
To answer a proposal's open questions, make a new request.

> [!TIP] Going back
> Ask your assistant to put back the previous Version, or the template's
> Steps. It shows you the Steps it would restore and the checks against
> the Routine's Items before you agree.
