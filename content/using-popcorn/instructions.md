---
id: instructions
title: Instructions
order: 18
group: Customizing a Routine
summary: >
  A Routine's Instructions say in plain language what its Agent should do
  and how: how to word a follow-up, when to ask a person first, what each
  Step asks.
  get_instructions reads them all at once, each part with where it came from
  and what changes it: update_routine_setting for wording that is a setting,
  change_routine for its Steps, Popcorn for the rest.
lede: >
  A Routine's Instructions say in plain language what it should do and how,
  from the wording of a follow-up to when to ask a person.
concepts: [routine-settings, customizing-a-routine]
---

A [Routine](https://docs.popcorn.ai/routines.md)'s **Instructions** are what
it should do and how, in plain language: how to word a follow-up, when to ask
a person before acting, which deadlines matter, when to send a reminder. The
Routine's [Agent](https://docs.popcorn.ai/agent.md) follows them, and asks
before the Steps they say need a
person. Changing them changes how the Routine behaves from then on, for that
Routine only, and the change survives the template's improvements.

## Where they live

Instructions come from more than one place:

- **The template's own guidance**, which every Routine made from it starts
  with.
- **Wording that is a
  [Routine Setting](https://docs.popcorn.ai/routine-settings.md)** — the
  text of a reminder email, a prompt the Agent writes from.
- **What people tell the Routine's Agent** in the Routine itself — "always
  copy the adjuster", "ask me before sending anything to the carrier". The
  Agent keeps the preferences and decisions it is given.
- **Each [Step](https://docs.popcorn.ai/steps.md)'s own Instructions**, in a
  Routine that has Steps: the questions a Step asks and what a complete
  answer to each needs, the wording of its emails, and a note on how to
  handle it. These are the Instructions people change most, by telling the
  Routine's Agent: "ask when it happened, and accept a month if they don't
  know the day".

> [!NOTE] A Step's emails keep one voice
> A Step's first email uses the opening and closing of the sample email it
> was set up from, word for word, and its later emails keep that voice.

## Reading them

> "What instructions is #intake working from?"

> [!TIP] MCP tool call
> Your assistant calls `get_instructions`.

Your assistant reads all of a Routine's Instructions at once, grouped by
where they live. For each part it says whether it is the template's or was
changed for this Routine, and how to change it:

| Part | Changed by |
|---|---|
| Guidance for each of the Routine's Agents, kept with its Steps | a change to its Steps, or the Agent in Popcorn |
| Prompt and email wording that is a Routine Setting | a Routine Setting |
| Notes for an Agent | a Routine Setting |
| The Routine's own guidelines for its Agent | Popcorn |
| What people told the Agent | telling the Agent, in Popcorn |
| Each Step's note, wording, questions and deadlines | a change to its Steps, or the Agent in Popcorn |
| The template's guide | a Routine [Member](https://docs.popcorn.ai/members.md), in Popcorn |

> [!TIP] One Step in full
> Each Step is summarised. Name one Step, by its name or its Status value,
> to see its Instructions in full.

> [!NOTE] Personal data
> On a Workspace that guards personal data, what people told the Agent
> shows only its kind and date, not what was said, since it can name a
> client.

## Changing them

No single change rewrites the Instructions; each part changes its own way:

- **Wording that is a setting** — your assistant changes it with edits to
  its text: see
  [Change how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md).
- **A Routine's Steps, with their own Instructions** — your assistant
  drafts the change and shows it before anything is installed: see
  [Change its Steps](https://docs.popcorn.ai/change-how-a-routine-behaves.md#change-its-steps).
- **Everything else** — tell the Routine's Agent, in Popcorn.

> [!TIP] For template authors
> The template's guidance is its `AGENT.md` and the prompt files it seeds,
> which [App Bundles](https://docs.popcorn.ai/app-bundle.md) describes.
