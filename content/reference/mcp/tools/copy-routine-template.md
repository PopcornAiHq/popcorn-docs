---
id: mcp/tools/copy-routine-template
title: copy_routine_template
order: 304
group: MCP
parent: mcp/tools
updated: 2026-11-01
summary: >
  Give a Routine its own named copy of the Routine Template it runs.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/create-routine-version, mcp/tools/list-routine-settings, mcp/tools/install-routine]
---

[writes] [destructive] [dry run]

```
copy_routine_template(routine_id, name, confirm=False, plan_id=None)
```

The copy starts byte-identical to the version of Popcorn's template the Routine runs, and the Routine moves onto it. That's one-way: the Routine never goes back to Popcorn's template, stops receiving Popcorn's improvements, and from then on gets only the new versions of its copy. Only a copy takes new versions, with create_routine_version. To change how one Routine behaves, check list_routine_settings first: a setting reaches one Routine and can be set back. Copy the template only for what settings can't express. Check an edit first with create_routine_version's dry run, since the copy is the step that can't be undone. Without confirm=true this is a dry run that changes nothing.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `name` [required] | `str` | The copy's name: lowercase letters, digits, "-" and "_", starting with a letter or digit. This only creates a copy; to move a Routine onto a copy that exists, use install_routine(copy=...). |
| `confirm` | `bool` | true to make the copy. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same request. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Give #intake its own copy of the claims app, called acme-intake, so we can change its intake form.”

```text
→ copy_routine_template(routine_id="c7d2…5b", name="acme-intake")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Copy: Popcorn's Claim Coordinator (claimcoordinator) 0.15.1 (version 812) → new copy "acme-intake".
- The copy starts byte-identical to 0.15.1. Nothing the Routine runs changes now.
- #intake moves onto the copy. Popcorn's improvements stop reaching it.
- One-way: a Routine on its own copy of a template never goes back to Popcorn's. From then on it follows copy "acme-intake", and new versions of that copy reach it within a day.
- Reach: this Routine only. Other Routines running Claim Coordinator (claimcoordinator) stay where they are.
- Other copies of Claim Coordinator (claimcoordinator) in this workspace: "acme-west" (to move onto one instead: install_routine(copy=…)).

Call again with `confirm=true` to make copy "acme-intake" of the template.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
