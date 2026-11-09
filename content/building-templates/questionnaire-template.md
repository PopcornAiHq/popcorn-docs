---
id: questionnaire-template
title: The Questionnaire template
order: 2
group: Making a change
summary: >
  The Questionnaire Bundle, read part by part: a Gmail Connection, a
  questionnaire Reference, one Table and one Schedule, whose pass asks,
  reads replies and follows up. A code block holds every rule (plan,
  compose, replies, decide), and a States tier makes No response a Review
  with Ask again, Mark answered and Close.
lede: >
  How Popcorn's starter template is built: its parts, what one pass does,
  and the rules that keep it from asking anyone twice.
concepts: [app-bundle, states-authoring, copying-a-template]
---

Questionnaire is the template behind `#team-offsite` in
[Set up your first Routine](https://docs.popcorn.ai/set-up-a-routine.md):
it emails each recipient the questions in a questionnaire, records their
answers from the replies, and follows up until they have answered. It is
small on purpose, so it is the template to read before you
[copy one](https://docs.popcorn.ai/copying-a-template.md) and change it.

To read its files, use `list_routine_files` and `read_routine_file` on a
[Routine](https://docs.popcorn.ai/routines.md) made from it, or `popcorn app checkout --channel <routine>`.

## Its parts

| Part | Where |
|---|---|
| Gmail, which holds the Routine back while missing | `manifest.yaml` `connections:` |
| The questionnaire [Reference](https://docs.popcorn.ai/reference-documents.md), required | `manifest.yaml` `documents:`, read by the `questionnaire_load` [Flow](https://docs.popcorn.ai/flow-grammar.md) |
| `recipients`, one Row per address, in a [Table](https://docs.popcorn.ai/tables.md) | `manifest.yaml` `tables:` |
| One [Schedule](https://docs.popcorn.ai/triggers.md), every fifteen minutes | the `questionnaire_tick` Flow |
| The reply-by date, required | the `reply_by_set` Flow |
| One [Review](https://docs.popcorn.ai/reviews.md), with three [Actions](https://docs.popcorn.ai/actions-and-status.md) | `manifest.yaml` `states:`, taken by the `cta_apply` Flow |
| Every rule: who to ask, what to send, what a reply answered | the `questionnaire` code block: `plan`, `compose`, `replies` and `decide` |
| What the Routine's [Agent](https://docs.popcorn.ai/agent.md) knows about it | `AGENT.md` |

The Flows only read, call the code block, and write what it returns, so
every rule can be tested without sending an email.

## How a pass works

```
questionnaire_tick
  ├── plan (code block)            Rows + questionnaire → who to ask, who to check
  ├── ask_recipient   × new        claim the Row → compose → send or draft → waiting
  ├── check_recipient × waiting    the thread → new replies → read the answers
  │                                → decide (code block) → record → follow up?
  └── project                      every Row's Status, Why and Actions from its Stage
```

Each recipient is a [Run](https://docs.popcorn.ai/history.md) of its own, so one failed send or unreadable thread
skips that recipient and leaves the rest of the pass alone. Nothing fires
when a Row is added: a recipient added by your assistant is asked on the
next pass, and has no Status or Actions until then. Adding or replacing
the questionnaire, and connecting Gmail, start a pass at once.

## A recipient's Stage

A recipient's state is the `Stage` Column, which the Flows write. `Status`,
`Why` and the Actions are worked out from it by the template's
[States tier](https://docs.popcorn.ai/states-authoring.md), so they can't
disagree:

```
"" (new) ──asked──▶ waiting ──answered──▶ answered
                     │  ├──gave up──▶ no_response ──Ask again──▶ waiting
                     │  └──Email corrected──▶ new        └──Close──▶ closed
                     └──Close──▶ closed      (new ──Close──▶ closed too)

Mark answered: new, waiting or no_response ──▶ answered
```

The moves a pass makes are `world` Transitions, declared so the graph is
whole. The three Actions are `staff` Transitions, each a button:

| Action | From | What it writes |
|---|---|---|
| **Ask again** | `no_response` | `Follow Ups` back to 0 and `Last Asked` blank, so the next pass follows up at once |
| **Mark answered** | `new`, `waiting`, `no_response` | Nothing else: `Answers` keeps what the replies gave |
| **Close** | `new`, `waiting`, `no_response` | Nothing else |

*No response* is the template's one Review: the State that warns.

## Rules worth knowing

- **One email per recipient.** `ask_recipient` and `check_recipient` claim
  the Row's `Sending` Column first, so two passes that overlap can't both
  send a first email or the same follow-up.
- **An Action never lands under a pass.** Each Action has the guard
  `not_held`, so it is refused while `Sending` is held: the pass writes
  `Stage` from the Row as its claim read it, and would overwrite it.
- **Answers are never overwritten.** A later reply fills only the questions
  still open.
- **An edited Email starts the recipient over.** Replies are read from
  `Asked Address`, where the first email went; a check that finds `Email`
  changed clears the thread and asks the new address afresh, keeping the
  answers given.
- **The reply-by date ends the chase.** Nobody is asked until it is set,
  and once it has passed, a recipient still waiting goes to *No response*,
  whatever their follow-ups.
- **`popcorn.email_send_mode`** is `send` on a new Routine. `draft` leaves
  each email in Gmail's Drafts and never follows up; `off` asks nobody but
  still reads replies.

## Changing it

How often it follows up, and how many times, are
[Routine Settings](https://docs.popcorn.ai/routine-settings.md)
(`follow_up_days` and `max_follow_ups`), and the questions are the
questionnaire Reference: neither needs a Copy. Anything else, such as a
second Review or another Table, does: see
[customizing a Routine](https://docs.popcorn.ai/customizing-a-routine.md).
