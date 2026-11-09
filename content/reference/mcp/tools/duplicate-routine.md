---
id: mcp/tools/duplicate-routine
title: duplicate_routine
order: 312
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-09
summary: >
  Create a new Routine in this workspace that copies an existing one's setup.
concepts: [set-up-a-routine]
used_with: [mcp/tools/get-routine, mcp/tools/create-routine]
---

[writes] [dry run]

```
duplicate_routine(routine_id, name, private=None, members=None, confirm=False, plan_id=None)
```

**What it copies.** It copies the original's Routine Template at its latest version from the same place (Popcorn, or this workspace's same copy, which the new Routine then follows for good), the Routine Settings changed from the template's, its own Steps, its guidelines for its agent, and the References it has added.

**What it doesn't.** Nothing is copied that belongs to the work or the people: not its items, History, messages or members, not what people told its agent, and not its Connections or credentials, which sign in as someone. A Reference picked from Google Drive is picked again in Popcorn once the new Routine has a Google Drive connection.

**Dry run.** The first call is a dry run that changes nothing: it lists every part that will be copied and every part left out. Call again with `confirm=true` to create the Routine. The template installs in the background, then the copy runs; [`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md)'s Copied from: field shows each part as it lands, and any that didn't, with why.

**Refused.** A name already used in this workspace is refused, with the ID of the Routine that has it. A Routine that runs no Routine Template (use [`create_routine`](https://docs.popcorn.ai/mcp/tools/create-routine.md)), one whose template new Routines here can't start from, and one shared in from another workspace can't be duplicated. You need to be a workspace admin or a member of the Routine you copy, and able to create Routines here.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The ID of the Routine to copy (not its name). |
| `name` [required] | `str` | The new Routine's name, e.g. "claims-east". Spaces become hyphens; the response shows the name it got. |
| `private` | `bool` | true for a private Routine, joined only by you and `members`; default false. A Routine that isn't private adds everyone in the workspace. The original's members aren't copied. |
| `members` | `list[str]` | People to add to a private Routine: "@username", email or user ID, all active members of this workspace (anyone else is refused). You're always a member. |
| `confirm` | `bool` | true to create the Routine. Confirm straight away when the person asked to duplicate this Routine; otherwise show them the dry run first. Default `False`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true`. It stands in for private and members: leave them out and the copy takes the dry run's, or send them and they must be the same. A Routine's own agent in Popcorn must pass it, from a dry run in an earlier run; an assistant connected from outside Popcorn is given none and needn't. |

**Example** — “Make a copy of #new-clients for the east office, called new-clients-east.”

```text
→ duplicate_routine(routine_id="569f…5c", name="new-clients-east")

**Dry run.** Nothing was changed.

Duplicate: #new-clients-east, a Routine in Acme, copied from #new-clients.
- Template: Claim Coordinator (claimcoordinator), fork line "acme" at 0.15.1-acme.2, as #new-clients is.
- Joins fork line "acme", this workspace's own copy of the template. One-way: a Routine on its own copy of a template never goes back to Popcorn's. From then on it follows copy "acme", and new versions of that copy reach it within a day.
- Members: everyone in the workspace (a Routine that isn't private adds every member).
Copied:
- Routine Settings and agent notes: 2 changed from the template's (chase_days, popcorn.agent_notes.intake).
- Steps: the Routine's own ("Claims intake", installed 2026-10-12, sha256 3f9c1a0b2d4e).
- Guidelines for its agent: 1.
- References: questions, each read into the copy as it was first added.
Not copied:
- References picked from Google Drive: standard_retainer. The new Routine starts with no Google Drive connection, so these are picked again in Popcorn once someone connects it.
- Credentials among its Routine Settings: crm_api_key. Set them in the new Routine in Popcorn.
- Connections: Gmail, Google Calendar, Google Drive. Someone sets them up in the new Routine before it runs.
- What people told its agent, and its items, History, messages and members.
The template installs in the background once the Routine exists, then the copy runs, typically within a few minutes; get_routine's Copied from: field shows each part as it lands.

Call again with `confirm=true` to create #new-clients-east as a copy of #new-clients.

→ duplicate_routine(routine_id="569f…5c", name="new-clients-east", confirm=true)

Created #new-clients-east (id: e75f…53), a Routine in Acme, copied from #new-clients.
Members: everyone in the workspace (a Routine that isn't private adds every member).
Claim Coordinator (claimcoordinator) is installing in the background, and the copy runs once it lands. Watch get_routine("e75f…53")'s Copied from: field until every part is in.
Before the Routine runs, someone sets up in it: Gmail, Google Calendar, Google Drive.
Pick again in Popcorn once Google Drive is connected: standard_retainer.
```
