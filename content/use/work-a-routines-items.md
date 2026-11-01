---
id: work-a-routines-items
title: Review what needs you
order: 16
group: What people do, and what happened
summary: >
  Reviewing what needs you: see what is waiting and why with get_status; find
  the claims or other Items at a Review, or still open, with list_rows,
  filtering by Status; read one with get_row; see the choices it offers with
  list_actions and take one with take_action after a dry run; stop tracking an
  Item; correct Rows with update_row; and run a scheduled Trigger now with
  run_trigger.
lede: >
  See what is waiting on you in a Routine, make the call, and correct anything
  that's wrong.
concepts: [reviews, actions-and-status, tables]
---

This guide covers the day-to-day: finding the Items waiting for someone,
making the call at their [Review](https://docs.popcorn.ai/reviews.md), and
fixing what is wrong on them. The example works `#intake`, a claims intake
Routine whose main Table holds one Row per potential client.

## Find what is waiting

> "Who in #intake is waiting for us to review them?"

`get_status` answers in one call: how many Items are at each Status, with the
ones that need a person marked, then what is waiting, newest first, each with
its reason and the Items it is about. Each Status comes with its stored value,
which is what the next call filters on.

To see the Items at one Review in full, `list_tables` names the Routine's
Tables, and `list_rows` lists a Table's Rows, newest first, and narrows them:

- `filter` on the Status Column. Popcorn shows a Status by its label, and
  the Row holds its value: *Needs retainer review* is `retainer_review`. So
  `{"Status": "retainer_review"}` finds the Items at that Review, and
  `{"Status": {"$in": ["retainer_review", "interview_review"]}}` finds those
  at either. For every Item still open, `$in` the Statuses that are not an
  Outcome: there is no "not in".
- `query` for a text anywhere in a Row: "Dana Reyes" finds that Item
  whatever Column holds the name.
- `sort` and `columns` to order the Rows and choose what each line shows.

## Read one

> "Show me everything on Dana Reyes."

`get_row` shows the Row in full: every Column, its Status, when it was
created and last changed, and the revision `update_row` needs under "Fix what is wrong".

> "What has happened with Dana so far?"

`list_history` shows what happened to the Item, newest first: each change,
who or what made it and why, and the work that made it. See
[History](https://docs.popcorn.ai/history.md).

## See what it offers

> "What can I do with Dana's intake?"

`list_actions` lists the Actions the Item offers now, given its Status, each
with the Status it moves the Item to. At the retainer Review those are
*Send retainer*, *Already signed* and *Do not send retainer*. *Send retainer*
is marked `[in the Popcorn app]`, because a person checks every field of the
agreement before it goes, so it is taken in Popcorn rather than by the
assistant.

## Make the call

> "Dana signed on paper. Mark Dana as already signed."

`take_action` takes one Action on one or more Items, as a person pressing
its button would. *Stop tracking* works the same way on any Item, to stop
its follow-ups without closing it. The dry run says what happens to each
Item and gives a `run_key`; read it back, then call again with
`confirm=true` and that `run_key`. The Action is real — anything it sends or records happens — and
the `run_key` makes it act once even if the call is repeated. `get_row`
shows the new Status once it has applied.

## Fix what is wrong

- **A wrong value** — `update_row` with the Columns to change and the
  revision from `get_row`. If someone changed the Row in the meantime,
  nothing is written and the response shows the Row as it is now.
- **A missing Item** — `create_rows`, after its dry run. A Row that
  matches an existing one merges into it rather than adding a duplicate. An
  added Item is picked up by the Routine's next Run, which may send it an
  email, and the dry run says so.
- **A duplicate** — `delete_rows`, after its dry run. A deleted Row cannot
  be restored with these tools.

None of these start work by themselves, and none can set a Status: that changes only by an
Action. See [Tables, Rows and Columns](https://docs.popcorn.ai/tables.md).

## Run the Routine's work now

> "Send #intake's due follow-ups now, don't wait for the next check."

`list_triggers` names the Routine's Schedules, and `run_trigger` runs one
now, after a dry run. Its next scheduled Run still happens. How the Run ended
is shown in Popcorn.
