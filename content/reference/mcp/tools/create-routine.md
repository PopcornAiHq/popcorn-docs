---
id: mcp/tools/create-routine
title: create_routine
order: 307
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  Create a Routine in this workspace, optionally from a Routine Template.
concepts: [set-up-a-routine]
used_with: [mcp/tools/get-routine, mcp/tools/list-routine-templates, mcp/tools/create-routine-template]
---

[writes]

```
create_routine(name, template=None, private=None, members=None, confirm=False, plan_id=None)
```

The Routine is created at once, with or without `template`; only a Routine's own agent in Popcorn gets a dry run first, and confirms it. From a template, the answer names the version that installs, the connections someone sets up before it runs, and the optional ones. The template installs in the background after the Routine exists; [`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md)'s Install: field shows when it lands.

A name already used in this workspace is refused, with the ID of the Routine that has it. Workspace guests can't create Routines; community guests can create only ones that aren't private.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `name` [required] | `str` | The Routine's name, e.g. "claims-west". Spaces become hyphens; the response shows the name it got. |
| `template` | `str` | A Routine Template's slug from [`list_routine_templates`](https://docs.popcorn.ai/mcp/tools/list-routine-templates.md), e.g. "claimcoordinator", or one this workspace made with [`create_routine_template`](https://docs.popcorn.ai/mcp/tools/create-routine-template.md) ("ws_…"). |
| `private` | `bool` | true for a private Routine, joined only by you and `members`; default false. A Routine that isn't private adds everyone in the workspace. |
| `members` | `list[str]` | People to add to a private Routine: "@username", email or user ID, all active members of this workspace (anyone else is refused). You're always a member. |
| `confirm` | `bool` | For a Routine's own agent in Popcorn, true to create what its dry run showed. Any other caller creates without it. Default `False`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true`. It stands in for template, private and members: leave them out and the create takes the dry run's, or send them and they must be the same. A Routine's own agent in Popcorn must pass it, from a dry run in an earlier run; an assistant connected from outside Popcorn is given none and needn't. |

**Example** — “Set up a private #new-clients Routine from the claims template, with Jordan in it.”

```text
→ create_routine(name="new-clients", template="claimcoordinator", private=true, members=["@jlee"])

Created #new-clients (id: 569f…5c), a private Routine in Acme.
Members: you, @jlee.
Claim Coordinator (claimcoordinator) 0.15.1 is installing in the background. Watch get_routine("569f…5c")'s Install: field until it says installed.
Before the Routine runs, someone sets up in it: Gmail, Google Calendar, Google Drive.
```
