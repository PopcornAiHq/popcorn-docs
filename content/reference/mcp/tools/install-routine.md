---
id: mcp/tools/install-routine
title: install_routine
order: 325
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Install the newest version of a Routine's copy of its template, or move it
  onto a copy the workspace already has.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/create-routine, mcp/tools/get-routine, mcp/tools/create-routine-version, mcp/tools/list-routine-settings, mcp/tools/copy-routine-template]
---

[writes] [destructive] [dry run]

```
install_routine(routine_id, copy=None, confirm=False, plan_id=None)
```

It installs the Routine Template the Routine already runs, never another one: a Routine runs another template only by creating a new Routine with create_routine(template=…).

Without copy, this is a catch-up: a Routine on its own copy installs that copy's newest version. It runs without confirm, because the daily update would install the same version. The install runs in the background; [`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md) shows when it lands. Use it after a [`create_routine_version`](https://docs.popcorn.ai/mcp/tools/create-routine-version.md) whose install waited on another install, or when `get_routine` shows the Routine behind its copy.

With copy, or when a Routine on Popcorn's template would join the workspace's only copy, the Routine moves onto that copy, one-way, and installs its newest version. If the workspace has several copies, name one with copy. A move is a dry run that changes nothing unless `confirm=true`. Workspace admins and the Routine's members may call it.

It doesn't put a template on a Routine that has none, and Popcorn's new versions reach Routines on Popcorn's template through the daily update, not through this tool. It is refused while the Routine's template updates are locked, and when another install is still running on the Routine. To change how one Routine behaves, check [`list_routine_settings`](https://docs.popcorn.ai/mcp/tools/list-routine-settings.md) first; a move onto a copy is one-way.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `copy` | `str` | The name of a copy of this Routine's template to move onto, as [`copy_routine_template`](https://docs.popcorn.ai/mcp/tools/copy-routine-template.md) named it. |
| `confirm` | `bool` | true to make the move. With a person there, show them the dry run first. Default `False`. |
| `plan_id` | `str` | The `plan_id` a move's dry run gave, with `confirm=true` and the same copy. A Routine's own agent in Popcorn must pass it, from a dry run in an earlier run; an assistant connected from outside Popcorn is given none and needn't. |

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
