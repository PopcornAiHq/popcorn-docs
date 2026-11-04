---
id: mcp/tools/change-routine
title: change_routine
order: 303
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  Change a Routine's Steps by describing the change in words, previewed before
  anything is installed, or put back an earlier version of its Steps.
concepts: [steps]
used_with: [mcp/tools/update-routine-setting, mcp/tools/get-routine-change]
---

[writes] [destructive] [dry run]

```
change_routine(routine_id, request=None, change_id=None, confirm=False, revert_to=None, run_key=None, plan_id=None)
```

Only a Routine whose template keeps its Steps with the Routine can be changed this way; any other is refused with what changes it instead (a Routine Setting, or a copy of its template of its own). For a change that is only a Routine Setting, update_routine_setting is quicker. Three calls: - request: starts drafting the change and returns a change_id. Drafting takes minutes; get_routine_change shows the proposal, as the Steps before and after. Nothing is installed. One change drafts at a time per Routine. - change_id with confirm=true: installs that proposal, once the person has read it. Sent again, it finds the install it started. - revert_to: "previous", "template" or a version, as get_routine_change names them. Without confirm it checks the revert against the Routine's items and gives a run_key; with confirm=true and that run_key it installs it.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `request` | `str` | The change, in the person's words ("after the retainer is signed, ask for their insurance card"). |
| `change_id` | `str` | The change_id change_routine returned, with confirm=true, to install its proposal. |
| `confirm` | `bool` | true to install. Show the person the proposal (or the revert's check) first. Default `False`. |
| `revert_to` | `str` | "previous", "template", or a version (sha) to go back to. |
| `run_key` | `str` | The run_key a revert's check gave, with confirm=true. |
| `plan_id` | `str` | The plan_id get_routine_change or the revert's check gave, with confirm=true; it stands in for the run_key. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “In #intake, once a claimant signs the retainer, have them book the interview straight away.”

```text
→ change_routine(routine_id="c7d2…5b", request="Once a claimant signs the retainer, ask them to book the interview straight away, and remind them after 2 days, then 5.")

Routine: #intake (c7d2…5b)
Drafting the change. change_id: 8c1f3a52…
Nothing is installed: the Routine's agent drafts the new Steps and checks them against this Routine's items, which takes a few minutes. get_routine_change with this change_id shows the proposal, as the Steps before and after, for the person to read before it goes in.

→ get_routine_change(routine="#intake", change_id="8c1f3a520d4e4b7a9f216a0c5d7b31e2-c7d20b9e5f134a8cb6e29d41f0a7c35b-recipe_build-req-Rv3kQ8pLm2Wx7Tz5a0d439dec3cde555", wait_seconds=20)

Routine: #intake (c7d2…5b)
Waited 2s: the change moved on.
Change 8c1f3a52…: proposed. Nothing is installed yet.
Asked for: "Once a claimant signs the retainer, ask them to book the interview straight away, and remind them after 2 days, then 5."
Steps, before → after (- before, + after):
  3. Signature — Getting signatures (Status value: signing)
+    - on its own: The claimant signed the standard retainer agreement and is asked to book the interview → Scheduling meeting (step 5)
On install it also sets, per Step:
- Scheduling meeting (interview): reminders 2, then 5 days after the last email; its email's wording: subject
  This part is a Routine Setting: update_routine_setting chase_days changes it for every Step without settings of its own, and leaves the Steps as they are.
The author assumed:
- The booking email goes out as soon as the agreement is signed; the team no longer decides on the interview first.
Questions it left open:
- Should claimants who already had their interview skip the booking email?
Checks: passed against this Routine's items and template; no item is left at a Step that would go (recipe version 45f7332bb200).
To install it: change_routine with change_id="8c1f3a52…" and confirm=true, once the person has read it. An open question above may change it; a new request starts a new change.

→ change_routine(routine_id="c7d2…5b", change_id="8c1f3a520d4e4b7a9f216a0c5d7b31e2-c7d20b9e5f134a8cb6e29d41f0a7c35b-recipe_build-req-Rv3kQ8pLm2Wx7Tz5a0d439dec3cde555", confirm=true)

Routine: #intake (c7d2…5b)
Installing change 8c1f3a52…. It checks the proposal once more against the Routine's items and puts it in only if it is unchanged; get_routine_change shows when it's done.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
