---
id: mcp/tools/get-user
title: get_user
order: 323
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Look up a person by handle: yourself, a member of this workspace, or someone
  from another workspace you share a Routine or DM with.
concepts: []
used_with: [mcp/tools/list-workspace-members]
---

[read-only]

```
get_user(user="me")
```

For a member: ID, username, display name, email, workspace role, whether they're active (no once deactivated or removed) and whether they're a bot. For someone from another workspace: display name, username and bot only. To find someone by name, use list_workspace_members.

Someone from another workspace is found by user ID only, and so is a deactivated member: usernames and emails are looked up among this workspace's active members, since a username is unique only within one workspace.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `user` | `str` | "me" (the default) for yourself, or a user ID, email, or username ("@name" works too). "me" always means you, even if someone's username is "me"; look them up by email or ID. Other spellings such as "self" are refused. |

**Example** — “What's Jordan Lee's email, and are they still active?”

```text
→ get_user(user="@jlee")

ID: 5d33…0c
Username: jlee
Display name: Jordan Lee
Email: jordan@acme.example
Workspace role: member
Active: yes
Bot: no
```
