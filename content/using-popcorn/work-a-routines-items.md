---
id: work-a-routines-items
title: Review what needs you
order: 3
group: Common tasks
summary: >
  Reviewing what needs you: see what is waiting and why with get_status; find
  the recipients or other Items at a Review, or still open, with list_rows,
  filtering by Status; read one with get_row; see the choices it offers with
  list_actions and take one with take_action; correct Rows with update_row;
  and run a scheduled Trigger now with run_trigger.
lede: >
  See what is waiting on you in a Routine, make the call, and correct anything
  that's wrong.
concepts: [reviews, actions-and-status, tables]
---

This guide covers the day-to-day: finding the Items waiting for someone,
making the call at their [Review](https://docs.popcorn.ai/reviews.md), and
fixing what is wrong on them. The example works `#team-offsite`, the
[Routine](https://docs.popcorn.ai/routines.md) from
[Set up your first Routine](https://docs.popcorn.ai/set-up-a-routine.md),
whose `recipients` [Table](https://docs.popcorn.ai/tables.md) holds one Row
per person asked. Its one Review is *No response*: someone who stopped
answering, where a person decides what next.

Each step below starts with a prompt you might give your assistant.

## Find what is waiting

> "Who in #team-offsite needs us to decide what to do next?"

> [!TIP] MCP tool call
> Your assistant calls `get_status`.

Your assistant answers with how many Items are at each
[Status](https://docs.popcorn.ai/actions-and-status.md), with the ones that
need a person marked. A Routine that keeps a list of what is waiting, such
as a claims intake Routine, adds it, newest first, each with its reason and
the Items it is about. `#team-offsite` keeps none, so the next step lists
them.

## List the Items at a Review

> "List everyone in #team-offsite with no response."

> [!TIP] MCP tool call
> Your assistant calls `list_tables`, then `list_rows` with a `filter` on
> the Status Column.

Your assistant lists the Items, newest first. You can narrow the list in
your request:

- **by Status** — one Review, several, or every Item still open;
- **by a name or any text** — "Jane" finds that Item whatever Column
  holds the name;
- **by what to show** — the order of the Rows, and which Columns each line
  shows.

> [!NOTE] A Status's label and its value
> Popcorn shows a Status by its label, and the Row holds its value:
> *No response* is `no_response`, so the filter is
> `{"Status": "no_response"}`. For several, use `$in`. There is no "not
> in", so every Item still open is `$in` the Statuses that aren't an
> Outcome: in `#team-offsite`, `new`, `waiting` and `no_response`. The Status Column isn't always named "Status"; `get_table`
> names it.

## Read one

> "Show me everything on Jane."

> [!TIP] MCP tool call
> Your assistant calls `get_row`.

Your assistant shows the Row in full: every Column, its Status, and when it
was created and last changed.

> "What has happened with Jane so far?"

> [!TIP] MCP tool call
> Your assistant calls `list_history`.

Your assistant shows what happened to the Item, newest first: each change,
who or what made it and why, and the work that made it. See
[History](https://docs.popcorn.ai/history.md).

## See what it offers

> "What can I do about Jane?"

> [!TIP] MCP tool call
> Your assistant calls `list_actions`.

Your assistant lists the Actions the Item offers now, given its Status, each
with the Status it moves the Item to. At *No response* those are the
Review's three choices ([Reviews](https://docs.popcorn.ai/reviews.md)).

Someone not asked yet, or still *Waiting*, offers *Mark answered* and
*Close*. Someone just added shows *Not asked yet* and offers both as soon
as their Row is saved, or at the latest once the next
[Run](https://docs.popcorn.ai/history.md) has passed over
them.

> [!NOTE] Not while a Run holds it
> While a Run is emailing someone or reading their replies, they offer no
> Actions. Ask again once the Run has finished.

## Make the call

> "Jane answered at standup. Mark Jane as answered."

> [!TIP] MCP tool call
> Your assistant calls `take_action`, then `get_run` to see it applied.

Taking an Action is the same as pressing its button: anything it sends or
records happens. You named the Item and the Action, so your assistant takes
it straight away. Otherwise it shows you first what happens to each Item,
and acts once you agree.

If you ask again after the reply-by date has passed, the next Run marks
them *No response* again, so
[change the date](https://docs.popcorn.ai/set-up-a-routine.md#set-the-reply-by-date) first.

> [!NOTE] All or nothing
> If one of the Items you name doesn't offer the Action now, nothing is done
> to any of them.

## Fix what is wrong

> "Jane's email is wrong: it's jane.doe@example.com."

> [!TIP] MCP tool call
> Your assistant calls `update_row`, `create_rows` or `delete_rows`.

| What's wrong | What your assistant does |
|---|---|
| **A wrong value** | Changes the Columns you name. If someone changed the Row in the meantime, nothing is written and it shows you the Row as it is now. |
| **A missing Item** | Adds it: straight away for up to ten Rows you name, and otherwise once you agree to what it shows you. A Row that matches an existing one merges into it rather than adding a duplicate. |
| **A duplicate** | Deletes it, once you agree to what it shows you. |

None of these starts work by itself, and none can set a Status: the
Routine's work and its Actions change that. See
[Tables, Rows and Columns](https://docs.popcorn.ai/tables.md).

> [!NOTE] A new address starts over
> In `#team-offsite`, correcting the Email of someone *Waiting* starts them
> over: the Routine emails the new address the whole questionnaire as a
> new email, and keeps the answers already given.

> [!WARNING] A new Item is real work
> The Routine's next Run picks up an
> added Item, and may send it an email.

> [!CAUTION] Deleting is permanent
> A deleted Row can't be restored with these tools.

## Run the Routine's work now

> "Send #team-offsite's due follow-ups now, don't wait for the next check."

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, then `run_trigger`, then `get_run`.

Your assistant runs the Routine's Schedule now, as
[Triggers](https://docs.popcorn.ai/triggers.md#running-a-schedule-now)
describes.
