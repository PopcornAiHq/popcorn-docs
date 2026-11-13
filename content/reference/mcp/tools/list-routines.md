---
id: mcp/tools/list-routines
title: list_routines
order: 339
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  List the Routines you can see in this workspace: the ones you're in, and the
  ones you can view without joining.
concepts: [routines]
used_with: [mcp/tools/get-routine]
---

[read-only]

```
list_routines(query=None, template=None, copy=None, include_archived=False, sort="name", cursor=None)
```

Routines shared in from another workspace are among the ones you're in, and the ones you haven't joined are marked [not joined]. Direct messages are not listed.

Each row shows the Routine's name, its Routine Template and whose version of it it runs (Popcorn's, or this workspace's copy by name), your unread count and mentions, and its ID. [missing a connection] marks one whose template needs an account nobody has connected; it is checked only on Routines you're in or, as a workspace admin, any here, so no marker isn't proof. [`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md) shows one Routine's version, install state and Connections.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive substring of the Routine name. |
| `template` | `str` | Only Routines made from this Routine Template, by its slug (e.g. "claimcoordinator"). |
| `copy` | `str` | Only Routines on this workspace's copy of that name: the Routines a new version of the copy reaches. A copy's name is unique per template, so pass template too when two templates have copies of the same name. |
| `include_archived` | `bool` | Also list archived Routines (marked [archived]). Default `False`. |
| `sort` | one of `name`, `recent` | "name" (default), or "recent": pinned first, then by last message. |
| `cursor` | `str` | The `next_cursor` from the previous page, with the same other arguments. |

**Example** — “Which of our Routines use the Claim Coordinator template?”

```text
→ list_routines(template="claimcoordinator")

50 of 137 Routines running claimcoordinator:
- #claims-central  Claim Coordinator (claimcoordinator) · Popcorn's  (id: 2af4…0c)
- #claims-east  Claim Coordinator (claimcoordinator) · copy "acme"  4 unread, 1 mention  (id: be23…ef)  [pinned]  [missing a connection]
- #claims-north  Claim Coordinator (claimcoordinator) · Popcorn's  (id: bd7d…b9)  [not joined]
- … 47 more rows
next_cursor: eyJ2Ijox…
```
