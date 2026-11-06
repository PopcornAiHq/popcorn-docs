---
id: mcp/tools/list-history
title: list_history
order: 328
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  What happened to one item: each change with who or what made it and why, the
  runs that changed it and how they ended, and its email turns.
concepts: [history]
used_with: [mcp/tools/list-runs, mcp/tools/list-rows, mcp/tools/run-trigger, mcp/tools/take-action]
---

[read-only]

```
list_history(routine, row_id=None, cursor=None, run=None)
```

Newest first, a page at a time. Each change shows when, who made it (a person by name; Popcorn and the work it was doing, for a run), the Status it moved to and its Why, and the other fields it changed. A run is listed only when it wrote to the item, and one a person's button started shows as Popcorn, for a person. History goes back as far as Popcorn keeps an item's changes; the last page says how far. With run instead of row_id, it follows one run: how it is going or how it ended, and the items it changed (or, if it changed none, what it did). list_runs lists the Routine's runs still going.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `row_id` | `int` | The item's row ID, as list_rows shows it ("row 88" is 88). |
| `cursor` | `str` | next_cursor from the previous page, with the same other arguments. |
| `run` | `str` | A run's reference, in place of row_id: run_trigger and take_action give it, and list_runs and list_history show it beside a run still going. |

**Example** — “What happened with row 88 in #intake?”

```text
→ list_history(routine="#intake", row_id=88)

Routine: #intake (c7d2…5b) · table: clients
Item: row 88
8 entries, newest first:
- 2026-10-18 10:20 · Popcorn (signing webhook): Retainer signed (entry_id 9)
  Status: Retainer sent → Signed
  1 other field changed: Why: Retainer sent; waiting for the signature. → —
- 2026-10-17 16:10 · Dana Smith: Matter updated (entry_id 7)
  1 field changed: Matter: Car accident → Car accident, rear-ended
- 2026-10-17 15:00 · Popcorn, for a person (cta apply): Send retainer (entry_id 6)
  Status: Needs review → Retainer sent
  Why: Retainer sent; waiting for the signature.
  1 other field changed: Retainer Sent At: 2026-10-17T15:00:00+00:00
- 2026-10-16 11:30 · Popcorn (chase turn): Answered all 5 intake questions (entry_id 4)
  Status: Waiting on answers → Needs review
  Why: Answers are in; check them before the retainer goes out.
  1 other field changed: Answers: {"injured": "yes", "insurer": "Acme Mutual"}
- 2026-10-16 11:29 · Popcorn: Email turn at intake: assess reply
  verdict: complete · reason: all_answered
  Summary: Ben Garrett answered all five questions.
- 2026-10-14 09:05 · Popcorn (chase turn): Sent the questions to Ben (entry_id 2)
  Status: New → Waiting on answers
  Why: Waiting on answers to 5 intake questions.
  1 other field changed: Questions Sent: 5
- 2026-10-14 09:04 · Popcorn: Email turn at intake: send questions
  verdict: approve · reason: first_contact
  Email: subject "Your intake questions, Ben Garrett", sent 2026-10-14 09:05
  Summary: Asked Ben Garrett the 5 intake questions.
- 2026-10-14 09:00 · Popcorn (intake): Created as New (entry_id 1)
read_history_entry with an entry_id shows that change in full, with what the run that made it did.
Runs that changed it on this page:
- signing webhook: succeeded · started 2026-10-18 10:19 by a webhook · ended 2026-10-18 10:20
- cta apply: succeeded · started 2026-10-17 14:59 by a person's button · ended 2026-10-17 15:00
- chase turn: succeeded · started 2026-10-16 11:29 by a message · ended 2026-10-16 11:30
- chase turn: succeeded · started 2026-10-14 09:04 by another run · ended 2026-10-14 09:05
- intake: succeeded · started 2026-10-14 08:59 by a webhook · ended 2026-10-14 09:00
A run a person's button started shows as Popcorn, for a person: runs don't record who pressed it.
Only runs that wrote to this item are listed; a run that only read it isn't.
History goes back 30 days; older changes aren't kept.
```

The [Tools](https://docs.popcorn.ai/mcp/tools.md) page has what every tool
shares: `routine` and `routine_id`, dry runs and `confirm=true`, and paging
with `next_cursor`.
