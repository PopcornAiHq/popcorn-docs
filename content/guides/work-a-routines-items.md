---
id: work-a-routines-items
title: Working a Routine's items
order: 4
summary: >
  Working a Routine's items: find them in its Tables with list_rows, filtering
  by Status; read one with get_row; see the Actions it offers with
  list_actions and take one with take_action after a dry run; correct or add
  Rows with update_row and create_rows; and run a scheduled Trigger now with
  run_trigger.
concepts: [tables, actions-and-status, triggers]
layer: product
---

This guide covers the day-to-day: finding the items that need someone,
moving them on, and fixing what is wrong on them. The example works
`#intake`, a claims Routine whose `claims` Table holds one Row per claim.

## 1. Find the items

> "Which claims in #intake are still open?"

`list_tables` names the Routine's Tables. `list_rows` lists a Table's
Rows, newest first, and narrows them:

- `filter` on the Status Column — `{"Status": "open"}` — for the items in
  one state, or `{"Status": {"$in": ["open", "waiting"]}}` for several.
- `query` for a text anywhere in a Row: "4471" finds that claim whatever
  Column holds it.
- `sort` and `columns` to order the Rows and choose what each line shows.

There is no count per Status yet; a filtered list is the way to see one
state's items.

## 2. Read one

> "Show me everything on claim 4471."

`get_row` shows the Row in full: every Column, its Status, when it was
created and last changed, and the revision `update_row` needs in step 5.

## 3. See what it offers

> "What can I do with claim 4471?"

`list_actions` lists the Actions the item offers now, given its Status, each
with the Status it moves the item to. An Action marked
`[in the Popcorn app]` needs a form, a signature or the Routine's agent, and
is taken in Popcorn rather than by the assistant.

## 4. Move it on

> "Close claim 4471."

`take_action` takes one Action on one or more items, as a person pressing
its button would. The dry run says what happens to each item and gives a
`run_key`; read it back, then call again with `confirm=true` and that
`run_key`. The Action is real — anything it sends or records happens — and
the `run_key` makes it act once even if the call is repeated. `get_row`
shows the new Status once it has applied.

## 5. Fix what is wrong

- **A wrong value** — `update_row` with the Columns to change and the
  revision from `get_row`. If someone changed the Row in the meantime,
  nothing is written and the response shows the Row as it is now.
- **A missing item** — `create_rows`. A Row that matches an existing one
  merges into it rather than adding a duplicate.
- **A duplicate** — `delete_rows`, after its dry run. A deleted Row cannot
  be restored with these tools.

None of these start work, and none can set a Status: that changes only by an
Action. See [Tables, Rows and Columns](https://docs.popcorn.ai/product/concepts/tables.md).

## 6. Run the Routine's work now

> "Send #intake's morning digest now."

`list_triggers` names the Routine's schedules, and `run_trigger` runs one
now, after a dry run. Its next scheduled run still happens. How the run ended
is shown in Popcorn.
