---
id: instructions
title: Instructions
order: 15
group: Changing a Routine
summary: >
  A Routine's Instructions say in plain language what it should do and how:
  how to word a follow-up, when to ask a person first, what each Step asks.
  get_instructions reads them all at once, each part with where it came from
  and what changes it: update_routine_setting for wording that is a setting,
  change_routine for its Steps, Popcorn for the rest.
lede: >
  A Routine's Instructions say in plain language what it should do and how,
  from the wording of a follow-up to when to ask a person.
concepts: [routine-settings, customizing-a-routine]
---

A Routine's **Instructions** are what it should do and how, in plain
language: how to word a follow-up, when to ask a person before acting, which
deadlines matter, when to send a reminder. The Routine's Agent follows them,
and asks before the Steps they say need a person. Changing them changes how
the Routine behaves from then on, for that Routine only, and the change
survives the template's improvements.

## Where they live

Instructions come from more than one place:

- **The template's own guidance**, which every Routine made from it starts
  with.
- **Wording that is a Routine Setting** — the text of a reminder email, a
  prompt the Agent writes from. `list_routine_settings` lists these, and
  `update_routine_setting` changes one with edits to its text (see
  [Routine Settings](https://docs.popcorn.ai/routine-settings.md)).
- **What people tell the Routine's Agent** in the Routine itself — "always
  copy the adjuster", "ask me before sending anything to the carrier". The
  Agent keeps the preferences and decisions it is given.
- **Each [Step](https://docs.popcorn.ai/steps.md)'s own Instructions**, in a
  Routine that has Steps: the questions a Step asks and what a complete
  answer to each needs, the wording of its emails, and a note on how to
  handle it. A Step's first email uses the opening and closing of the sample
  email it was set up from, word for word, and its later emails keep that
  voice. These are the Instructions people change most, by telling the
  Routine's Agent: "ask when it happened, and accept a month if they don't
  know the day".

## Reading them

> "What instructions is #intake working from?"

`get_instructions` reads a Routine's Instructions in one call, grouped by
where they live, and says for each part whether it is the template's or was
changed for this Routine, and what changes it:

| Part | Changed by |
|---|---|
| Guidance for each of the Routine's Agents, kept with its Steps | `change_routine`, or in Popcorn |
| Prompt and email wording that is a Routine Setting | `update_routine_setting` |
| Notes for an Agent | `update_routine_setting` |
| The Routine's own guidelines for its Agent | in Popcorn |
| What people told the Agent | in Popcorn, by telling the Agent |
| Each Step's note, wording, questions and deadlines | `change_routine`, or in Popcorn |
| The template's guide | a Routine Member, in Popcorn |

Without a `step`, each Step is summarised; `step` (its Status value or name)
shows one Step's in full. On a Workspace that guards personal data, what
people told the Agent shows only its kind and date, not what was said, since
it can name a client.

## Changing them

There is no single tool that rewrites the Instructions. Wording that is a
setting is changed with `update_routine_setting`, and a Routine's Steps, with
their own Instructions, are changed with `change_routine`, which shows the
change before anything is installed (see
[Steps](https://docs.popcorn.ai/steps.md)). The rest is changed in Popcorn, by
telling the Routine's Agent.

The template's guidance is its `AGENT.md` and the prompt files it seeds,
which [App Bundles](https://docs.popcorn.ai/app-bundle.md)
describes.
