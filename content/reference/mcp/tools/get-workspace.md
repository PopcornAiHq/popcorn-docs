---
id: mcp/tools/get-workspace
title: get_workspace
order: 322
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  The Popcorn workspace this connection is bound to.
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

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
