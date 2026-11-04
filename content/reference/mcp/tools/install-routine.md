---
id: mcp/tools/install-routine
title: install_routine
order: 323
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  Install the newest version of a Routine's copy of its template, or move it
  onto a copy the workspace already has.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/create-routine, mcp/tools/create-routine-version, mcp/tools/get-routine, mcp/tools/list-routine-settings, mcp/tools/copy-routine-template]
---

[writes] [destructive] [dry run]

```
install_routine(routine_id, copy=None, confirm=False, plan_id=None)
```

It installs the Routine Template the Routine already runs, never another one: a Routine runs another template only by creating a new Routine with create_routine(template=…). Without copy, this is a catch-up (as `popcorn app apply`): a Routine on its own copy installs that copy's newest version. It runs without confirm, because the daily update would install the same version. Use it after a create_routine_version whose install was blocked, or when get_routine shows the Routine behind its copy. With copy, or when a Routine on Popcorn's template would join the workspace's only copy, the Routine moves onto that copy, one-way, and installs its newest version. A move is a dry run that changes nothing unless confirm=true. It doesn't put a template on a Routine that has none, and Popcorn's new versions reach Routines on Popcorn's template through the daily update, not through this tool. To change how one Routine behaves, check list_routine_settings first; a move onto a copy is one-way.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `copy` | `str` | The name of a copy of this Routine's template to move onto, as copy_routine_template named it. |
| `confirm` | `bool` | true to make the move. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id a move's dry run gave, with confirm=true and the same copy. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Move #intake onto our acme-west version of the claims app.”

```text
→ install_routine(routine_id="c7d2…5b", copy="acme-west")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Install: #intake moves from Popcorn's Claim Coordinator (claimcoordinator) 0.15.1 onto copy "acme-west", at its newest version 0.16.0 (version 913).
- This changes which copy of the template the Routine follows. It installs 0.16.0, which isn't what the Routine runs now.
- One-way: a Routine on its own copy of a template never goes back to Popcorn's. From then on it follows copy "acme-west", and new versions of that copy reach it within a day.
- Reach: this Routine only.

Call again with `confirm=true` to move #intake onto copy "acme-west".
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
