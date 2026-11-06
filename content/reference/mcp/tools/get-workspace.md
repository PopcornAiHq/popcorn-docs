---
id: mcp/tools/get-workspace
title: get_workspace
order: 323
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-05
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

The [Tools](https://docs.popcorn.ai/mcp/tools.md) page has what every tool
shares: `routine` and `routine_id`, dry runs and `confirm=true`, and paging
with `next_cursor`.
