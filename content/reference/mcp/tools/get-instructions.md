---
id: mcp/tools/get-instructions
title: get_instructions
order: 313
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-07
summary: >
  Show a Routine's Instructions, the guidance its agents work from,
  Routine-wide and for each Step.
concepts: [instructions]
used_with: [mcp/tools/list-memories, mcp/tools/get-memory, mcp/tools/get-routine]
---

[read-only]

```
get_instructions(routine, step=None, guide=False, cursor=None)
```

Each layer comes with where it came from (the template's, or changed for this Routine) and what changes it. A Routine shared in from another workspace is refused.

**Layers.** The Routine's guidance per agent, its prompt files, its agent notes, its guidelines for its agent, what people told the agent, each Step's note, copy, questions and deadlines, and the template's guide (AGENT.md). Without step, the Routine-wide layers are shown, each text cut past a few thousand characters with the call that shows it whole, and each Step is summarised; with step, that Step's are shown in full. The template's guide is shown as its size and first heading only. A Routine whose template has no Steps has no per-Step layers. What people told the agent shows the newest memories, each cut short; [`list_memories`](https://docs.popcorn.ai/mcp/tools/list-memories.md) and [`get_memory`](https://docs.popcorn.ai/mcp/tools/get-memory.md) read them all.

**Guide.** With `guide=true` it returns the template's guide instead: this Routine's AGENT.md, its text whole, a range at a time when it is long.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `step` | `str` | One Step, by its label or its Status value, as [`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md) lists the Steps. Omit for the whole Routine. |
| `guide` | `bool` | true for the text of this Routine's AGENT.md. Default `False`. |
| `cursor` | `str` | `next_cursor` from the previous range of AGENT.md, with `guide=true`. |

**Example** — “What instructions is #intake's agent following?”

```text
→ get_instructions(routine="#intake")

Routine: #intake (c7d2…5b) · template: chase 0.84.0
The Routine's Instructions, by layer: where each came from, and what changes it.

## Routine guidance per agent (from this Routine's Steps, "Acme intake", installed 2026-10-12, sha256 1a2b3c4d5e6f)
Changed by: with change_routine (describe the change), or in Popcorn by telling the Routine's agent.
- chasewriter:
  Write as a person on the Acme claims team.
  Never promise when a claim will be paid.
- chasevalidator:
  An answer that names a month and a year is a date.
- chasewriter, at Booking Steps only:
  Offer the adjuster call link before anything else.

## Prompt files
Changed by: update_routine_setting, by a workspace admin who's also a member of the Routine.
- prompts.validator (the template's):
  Judge each answer against its question.
- prompts.writer (changed for this Routine):
  You write the claims team's emails.
  Be brief.
  Use the claimant's first name.

## Agent notes
Changed by: update_routine_setting, by a member of the Routine.
- popcorn.agent_notes.chasewriter (set for this Routine):
  Copy the adjuster on anything about money.
- None set: popcorn.agent_notes.chasevalidator.

## The Routine's guidelines for its agent
Changed by: in Popcorn.
- Claims intake:
  Answer in plain English; never quote policy clauses.

## What people told the agent (2, newest first)
Changed by: in Popcorn, by telling the agent.
- preferences/00000014  2026-10-14: Mrs. Ortiz prefers a call after 5pm.
- decisions/00000009  2026-10-09: Water damage under $2,000 skips the adjuster call.

## Each Step's note, copy, questions and deadlines
Changed by: with change_routine (describe the change), or in Popcorn by telling the Routine's agent.
1. Answers — Collecting claim details (Status value: intake):
   note "Ask for the policy number before anything else.", set for this Routine, chase.intake.guidance; 3 questions; subject "A few questions about your claim"; deadlines: the recipe's table is in force: 1 period(s) from item q2.
2. Review — Needs adjuster review (Status value: review): a Review, decided by a person; no instructions of its own.
3. Booking — Booking the adjuster call (Status value: interview):
   note "Keep it to two sentences." (+1 more), in this Routine's Steps; a booking page.
get_instructions(routine="#intake", step="<Status value>") shows one Step's in full.

## The template's guide
Changed by: a member of the Routine, in Popcorn. A template update keeps a change made to this Routine's copy.
- AGENT.md (the template's): 1,475 characters, first heading "Claims intake agent". How the Routine's agent talks and what it knows about the template. get_instructions with guide=true reads its text.
```
