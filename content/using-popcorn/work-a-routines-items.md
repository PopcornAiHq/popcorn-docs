---
id: work-a-routines-items
title: Review what needs you
order: 3
group: Common tasks
summary: >
  Reviewing what needs you: see what is waiting and why with get_status; find
  the claims or other Items at a Review, or still open, with list_rows,
  filtering by Status; read one with get_row; see the choices it offers with
  list_actions and take one with take_action; stop tracking an
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
[Routine](https://docs.popcorn.ai/routines.md) whose main
[Table](https://docs.popcorn.ai/tables.md) holds one Row per potential
client.

Each step below starts with a prompt you might give your assistant.

## Find what is waiting

> "Who in #intake is waiting for us to review them?"

> [!TIP] MCP tool call
> Your assistant calls `get_status`.

Your assistant answers in one go: how many Items are at each
[Status](https://docs.popcorn.ai/actions-and-status.md), with the ones that
need a person marked, then what is waiting, newest first, each with its
reason and the Items it is about.

## List the Items at a Review

> "List everyone in #intake waiting for retainer review."

> [!TIP] MCP tool call
> Your assistant calls `list_tables`, then `list_rows` with a `filter` on
> the Status Column.

Your assistant lists the Items, newest first. You can narrow the list in
your request:

- **by Status** — one Review, several, or every Item still open;
- **by a name or any text** — "Dana Reyes" finds that Item whatever Column
  holds the name;
- **by what to show** — the order of the Rows, and which Columns each line
  shows.

> [!NOTE] A Status's label and its value
> Popcorn shows a Status by its label, and the Row holds its value:
> *Needs retainer review* is `retainer_review`, so the filter is
> `{"Status": "retainer_review"}`. For several, use `$in`. There is no "not
> in", so every Item still open is `$in` the Statuses that aren't an
> Outcome. The Status Column isn't always named "Status"; `get_table`
> names it.

## Read one

> "Show me everything on Dana Reyes."

> [!TIP] MCP tool call
> Your assistant calls `get_row`.

Your assistant shows the Row in full: every Column, its Status, and when it
was created and last changed.

> "What has happened with Dana so far?"

> [!TIP] MCP tool call
> Your assistant calls `list_history`.

Your assistant shows what happened to the Item, newest first: each change,
who or what made it and why, and the work that made it. See
[History](https://docs.popcorn.ai/history.md).

## See what it offers

> "What can I do with Dana's intake?"

> [!TIP] MCP tool call
> Your assistant calls `list_actions`.

Your assistant lists the Actions the Item offers now, given its Status, each
with the Status it moves the Item to. At the retainer Review those are
*Send retainer*, *Already signed* and *Do not send retainer*.

> [!NOTE] Taken in Popcorn
> *Send retainer* is taken in Popcorn, not by your assistant, because a
> person checks every field of the agreement before it goes.

## Make the call

> "Dana signed on paper. Mark Dana as already signed."

> [!TIP] MCP tool call
> Your assistant calls `take_action`, then `get_run` to see it applied.

Taking an Action is the same as pressing its button: anything it sends or
records happens. You named the Item and the Action, so your assistant takes
it straight away. Otherwise it shows you first what happens to each Item,
and acts once you agree.

*Stop tracking* works the same way on any Item, to stop its follow-ups
without closing it.

> [!NOTE] All or nothing
> If one of the Items you name doesn't offer the Action now, nothing is done
> to any of them.

## Fix what is wrong

> "Dana's phone number is wrong: it's 555-0142."

> [!TIP] MCP tool call
> Your assistant calls `update_row`, `create_rows` or `delete_rows`.

| What's wrong | What your assistant does |
|---|---|
| **A wrong value** | Changes the Columns you name. If someone changed the Row in the meantime, nothing is written and it shows you the Row as it is now. |
| **A missing Item** | Adds it: straight away for up to ten Rows you name, and otherwise once you agree to what it shows you. A Row that matches an existing one merges into it rather than adding a duplicate. |
| **A duplicate** | Deletes it, once you agree to what it shows you. |

None of these starts work by itself, and none can set a Status: that
changes only by an Action. See
[Tables, Rows and Columns](https://docs.popcorn.ai/tables.md).

> [!WARNING] A new Item is real work
> The Routine's next [Run](https://docs.popcorn.ai/history.md) picks up an
> added Item, and may send it an email.

> [!CAUTION] Deleting is permanent
> A deleted Row can't be restored with these tools.

## Run the Routine's work now

> "Send #intake's due follow-ups now, don't wait for the next check."

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, then `run_trigger`, then `get_run`.

Your assistant finds the Routine's
[Schedule](https://docs.popcorn.ai/triggers.md) and runs it now: straight
away when you asked for that Schedule, and otherwise once you agree. Its
next scheduled Run still happens, and your assistant can show how the Run
is going or how it ended.

> [!NOTE] One at a time
> If a Run of that Schedule is already going, nothing new starts.
