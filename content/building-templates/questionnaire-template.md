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

## Read its files

> "List the files #team-offsite's template is made of, and read its
> `manifest.yaml`."

> [!TIP] MCP tool call
> Your assistant calls `list_routine_files`, then `read_routine_file` for
> `manifest.yaml`.

Your assistant lists the
[Version](https://docs.popcorn.ai/versions.md) of the template the
[Routine](https://docs.popcorn.ai/routines.md) runs, whether it is
Popcorn's or your Workspace's own Copy, and each file with its size.
Reading needs no Copy. With the CLI, a Checkout writes the same files to
disk:

```bash
popcorn app checkout --channel '#team-offsite'
```

```
questionnaire/
├── manifest.yaml                 the Connection, Reference, Table, Schedule and states
├── strings.yaml                  the setup checklist and the Email sending setting's labels
├── AGENT.md                      what the Routine's Agent knows about it
├── README.md                     the template's own notes
├── questionnaire_tick.yaml       one pass, run by the Schedule
├── ask_recipient.yaml            the first email to one recipient
├── check_recipient.yaml          one recipient's replies and follow-up
├── cta_apply.yaml                the three Actions
├── questionnaire_load.yaml       reads the questionnaire Reference
├── reply_by_set.yaml             the reply-by date setup step
├── on_auth_change.yaml           runs when Gmail is connected
├── prompts/
│   ├── read_questionnaire.md.j2  pulls the questions out of the Reference
│   └── read_answers.md.j2        matches a reply to the questions
└── code/questionnaire/
    ├── main.py                   every rule: plan, compose, replies, decide
    └── tests/
```

## Its parts

| Part | Where |
|---|---|
| Gmail, without which nothing is asked or read | `manifest.yaml` `connections:` |
| The questionnaire [Reference](https://docs.popcorn.ai/reference-documents.md), required | `manifest.yaml` `documents:`, read by the `questionnaire_load` [Flow](https://docs.popcorn.ai/flow-grammar.md) |
| `recipients`, one Row per address, in a [Table](https://docs.popcorn.ai/tables.md) | `manifest.yaml` `tables:` |
| One [Schedule](https://docs.popcorn.ai/schedules.md), every fifteen minutes | `manifest.yaml` `schedules:`, running `questionnaire_tick` |
| The reply-by date, required | the `reply_by_set` Flow, from the setup checklist in `strings.yaml` |
| One [Review](https://docs.popcorn.ai/reviews.md), with three [Actions](https://docs.popcorn.ai/actions-and-status.md) | `manifest.yaml` `states:`, taken by the `cta_apply` Flow |
| Every rule: who to ask, what to send, what a reply answered | the `questionnaire` code block: `plan`, `compose`, `replies` and `decide` |
| What the Routine's [Agent](https://docs.popcorn.ai/agent.md) knows about it | `AGENT.md`, and `agent_summary` under `scalars:` |

The Flows only read, call the code block, and write what it returns, so
every rule can be tested without sending an email.

## How a pass works

```
questionnaire_tick
  ├── plan (code block)            Rows + questionnaire → who to ask, who to check
  ├── ask_recipient   × new        claim the Row → compose → send or draft → waiting
  ├── check_recipient × waiting    claim the Row → the thread → new replies
  │                                → read_answers prompt → decide (code block)
  │                                → record → follow up?
  └── project                      every Row's Status, Why and Actions from its Stage
```

Each recipient is a [Run](https://docs.popcorn.ai/history.md) of its own,
so one failed send or unreadable thread skips that recipient and leaves the
rest of the pass alone. A pass sends at most 25 first emails; the rest are
asked on the next one, so a long list goes out over several passes rather
than in one burst from your Gmail.

Nobody is asked until the questionnaire is in, Gmail can send and the
reply-by date is set, and nobody new is asked once that date has passed.
Recipients already waiting are still checked.

> [!NOTE] Nothing fires when a Row is added
> A recipient added by your assistant is asked on the next pass, and has
> no Status or Actions until then. Adding or replacing the questionnaire,
> setting the reply-by date and connecting Gmail each start a pass at
> once.

## A recipient's Stage

A recipient's state is the `Stage`
[Column](https://docs.popcorn.ai/table-columns.md), which the Flows write.
`Status`, `Why` and the Actions are worked out from it by the template's
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
| **Ask again** | `no_response` | `Follow Ups` back to 0 and `Last Asked` empty, so the next pass follows up at once |
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
- **The reply-by date ends the chase.** Once it has passed, a recipient
  still waiting goes to *No response*, whatever their follow-ups.
- **`popcorn.email_send_mode`** is `send` on a new Routine. `draft` leaves
  each first email in Gmail's Drafts and never follows up; `off` asks
  nobody but still reads replies.

> [!NOTE] A draft has no Message-ID
> A follow-up threads in the recipient's mailbox by the last email's
> Message-ID, which a first email left as a draft doesn't have. A recipient
> asked in `draft` mode and followed up after switching to `send` may see
> the follow-up as a new conversation; your own mailbox threads it either
> way.

## Changing it

Most changes need no Copy. These are
[Routine Settings](https://docs.popcorn.ai/routine-settings.md), which
reach one Routine and can be set back:

| To change | Setting |
|---|---|
| How often it follows up, and how many times | `follow_up_days`, `max_follow_ups` |
| Whether emails are sent, drafted or not sent | `popcorn.email_send_mode` |
| How a reply is matched to the questions | `prompts.read_answers` |
| How the questions are pulled out of the questionnaire | `prompts.read_questionnaire` |

The questions, the subject and the wording around them are the
questionnaire Reference, which you replace with new text; the reply-by
date is changed by asking for a new one. Anything else, such as how often
the pass runs, a second Review or another Table, needs a Copy: see
[changing a Routine Template](https://docs.popcorn.ai/template-authoring.md),
whose example is exactly that.
