---
id: mcp/tools/list-workspace-members
title: list_workspace_members
order: 334
group: MCP
parent: mcp/tools
updated: 2026-11-01
summary: >
  List the members of this workspace, alphabetically by name.
concepts: []
used_with: [mcp/tools/get-user]
---

[read-only]

```
list_workspace_members(query=None, include_bots=False, cursor=None)
```

This workspace's members only: someone from another workspace who is in a shared Routine isn't listed here, and deactivated members never are. To look up one person by ID, email or @username (a bot included), use get_user.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive text to find in a username, display name or email, e.g. "dana". A leading "@" also matches the username after it ("@dsmith"), and still matches inside emails, so "@acme.example" finds everyone at that domain. |
| `include_bots` | `bool` | Also list bots. Default `False`. |
| `cursor` | `str` | The next_cursor of the previous page, to continue. Pass the same query and include_bots as that call. |

**Example** — “Who on the Acme team is named Lee?”

```text
→ list_workspace_members(query="lee")

2 of 2 members matching "lee":
- Jordan Lee  @jlee  jordan@acme.example  member  (id: 5d33…0c)
- Sam Lee  @slee  sam@acme.example  admin  (id: 7a41…d2)
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
