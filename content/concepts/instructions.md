---
id: instructions
title: Instructions
order: 9
group: How it behaves
summary: >
  A Routine's Instructions say in plain language what it should do and how:
  how to word a follow-up, when to ask a person first, which deadlines matter.
  Some of that wording — its email and prompt texts — is Routine Settings an
  assistant can read and change. The rest is shaped in Popcorn by telling the
  Routine's agent; no assistant tool reads or changes it yet.
concepts: [routine-settings, customizing-a-routine]
layer: product
---

A Routine's **Instructions** are what it should do and how, in plain
language: how to word a follow-up, when to ask a person before acting, which
deadlines matter, when to send a reminder. The Routine's agent follows them,
and asks before the steps they say need a person. Changing them changes how
the Routine behaves from then on, for that Routine only, and the change
survives the template's improvements.

## Where they live today

Instructions come from more than one place:

- **The template's own guidance**, which every Routine made from it starts
  with.
- **Wording that is a Routine Setting** — the text of a reminder email, a
  prompt the agent writes from. `list_routine_settings` lists these, and
  `update_routine_setting` changes one with edits to its text (see
  [Routine Settings](https://docs.popcorn.ai/product/concepts/routine-settings.md)).
- **What people tell the Routine's agent** in the Routine itself — "always
  copy the adjuster", "ask me before sending anything to the carrier". The
  agent keeps the preferences and decisions it is given.

## What an assistant can do with them

An assistant can read and change the wording that is a Routine Setting. It
cannot read the Instructions as a whole, or change the guidance that is not a
setting: `update_routine_setting` says so when asked. A person changes those
in Popcorn, by telling the Routine's agent.

## What the assistant tools would need to show

These pages describe the present, so this section is a design input, not a
promise: nothing depends on it arriving. A tool for Instructions would need
to show them as one plain-language text, say which parts are the template's
and which were changed for this Routine, take a change in the person's words
and preview the Instructions as they would read after it, and return a changed
part to the template's. The MCP reference's
[proposed tools](https://docs.popcorn.ai/product/reference/mcp.md) sketch `get_instructions` and
`update_instructions` along those lines.

> **Platform note** — The template's guidance is its `AGENT.md` and the
> prompt files it seeds. See [app bundles](https://docs.popcorn.ai/platform/concepts/app-bundle.md).
