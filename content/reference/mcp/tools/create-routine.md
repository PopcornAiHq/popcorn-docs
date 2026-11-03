---
id: mcp/tools/create-routine
title: create_routine
order: 306
group: MCP
parent: mcp/tools
updated: 2026-11-03
summary: >
  Create a Routine in this workspace, optionally from a Routine Template.
concepts: [set-up-a-routine]
used_with: [mcp/tools/get-routine, mcp/tools/list-routine-templates]
---

[writes] [dry run]

```
create_routine(name, template=None, private=None, members=None, confirm=False, plan_id=None)
```

Without `template` the Routine is created at once (for Popcorn's channel agent it is a dry run first, like any other). With `template` the first call is a dry run that changes nothing: it shows the version that will install and the connections someone sets up before it runs. Call again with confirm=true to create it. The template installs in the background after the Routine exists; get_routine's Install: field shows when it lands. A name already used in this workspace is refused, with the ID of the Routine that has it.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `name` [required] | `str` | The Routine's name, e.g. "claims-west". Spaces become hyphens; the response shows the name it got. |
| `template` | `str` | A Routine Template's slug from list_routine_templates, e.g. "claimcoordinator". |
| `private` | `bool` | true for a private Routine, joined only by you and `members`. A Routine that isn't private adds everyone in the workspace. |
| `members` | `list[str]` | People to add to a private Routine: "@username", email or user ID, all members of this workspace. You're always a member. |
| `confirm` | `bool` | true to create a Routine from a template. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true. It stands in for template, private and members: leave them out and the create takes the dry run's, or send them and they must be the same. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Set up a private #new-clients Routine from the claims template, with Jordan in it.”

```text
→ create_routine(name="new-clients", template="claimcoordinator", private=true, members=["@jlee"])

**Dry run.** Nothing was changed.

Create: #new-clients, a private Routine in Acme, running Claim Coordinator (claimcoordinator).
- Installs: claimcoordinator 0.15.1, the latest version.
- Members: you, @jlee.
- Connections to set up in the Routine before it runs: Gmail, Google Calendar, Google Drive.
- The install runs in the background once the Routine exists, typically in seconds; get_routine's Install: field shows when it lands.

Call again with `confirm=true` to create #new-clients running claimcoordinator.

→ create_routine(name="new-clients", template="claimcoordinator", private=true, members=["@jlee"], confirm=true)

Created #new-clients (id: 569f…5c), a private Routine in Acme.
Members: you, @jlee.
Claim Coordinator (claimcoordinator) is installing in the background. Watch get_routine("569f…5c")'s Install: field until it says installed.
Before the Routine runs, someone sets up in it: Gmail, Google Calendar, Google Drive.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
