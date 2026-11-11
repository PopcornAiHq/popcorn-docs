---
id: mcp/tools/get-workspace
title: get_workspace
order: 325
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  Show the Popcorn workspace this connection is bound to, and your role in it.
concepts: []
---

[read-only]

```
get_workspace()
```

Every tool acts in this one workspace. It was chosen when the user connected Popcorn and can't be changed from here: to use a different workspace, the user reconnects Popcorn.

**Example** — “Which Popcorn workspace are you connected to?”

```text
→ get_workspace()

Name: Acme
ID: 8c1f…e2
Slug: acme
Your role: member

This connection is bound to this workspace. To use a different one, the user reconnects Popcorn.
```
