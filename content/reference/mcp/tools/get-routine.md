---
id: mcp/tools/get-routine
title: get_routine
order: 319
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Show one Routine: its details, your membership, its Routine Template and the
  version it's on, and its Connections.
concepts: [routines]
used_with: [mcp/tools/duplicate-routine, mcp/tools/list-rows, mcp/tools/take-action]
---

[read-only]

```
get_routine(routine, wait_seconds=0)
```

It also shows the latest version, where its updates come from (Popcorn, or this workspace's own copy of the template), whether the latest install landed, and each account or webhook the template needs, with whether it's connected. A Routine made with [`duplicate_routine`](https://docs.popcorn.ai/mcp/tools/duplicate-routine.md) also shows how far its copy got, and any part that didn't copy, with why.

Connections are shown only to the Routine's members and workspace admins. A Routine shared in from another workspace shows no version, Connections or Steps: its home workspace manages them.

A Routine whose template has Steps also lists them in order, with which version of them is installed. A Step's Status value is what [`list_rows`](https://docs.popcorn.ai/mcp/tools/list-rows.md) filters on. A choice marked [in Popcorn] opens a form there; [`take_action`](https://docs.popcorn.ai/mcp/tools/take-action.md) takes the others.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | The Routine's ID, or its name ("#intake" or "intake"). Names aren't unique: if more than one Routine has it, the call lists them with their IDs; pass an ID instead. |
| `wait_seconds` | `int` | Wait up to this many seconds for an install in progress to land (installed, or failed for good), then answer; the answer says whether it landed or the wait ran out. At most 20 (more is read as 20); 0, the default, doesn't wait. |

**Example** — “Is #intake on the latest version of its template?”

```text
→ get_routine(routine="#intake")

ID: c7d2…5b
Name: #intake
Kind: Routine
Description: New claims, triaged and assigned
Archived: no
Members (incl. bots): 9
Joined: yes
Your role: admin
Unread: 4
Mentions: 1
Muted: no
Template: Claim Coordinator (claimcoordinator)
Updates from: Popcorn
Version: 0.15.1 (the latest)
Install: installed
Connections:
- Claims inbox (email): connected: claims@acme.example (google)
- Adjuster calendar (calendar): NOT CONNECTED; work that uses it can't run
- Carrier portal (webhook): connected: carrier-portal
Whether a connected account has since been revoked or its sign-in has expired isn't checked here. A Routine member connects these with make_connection, or in the Routine's settings in Popcorn.
list_connections says whose account each one uses and what stops without it.
```
