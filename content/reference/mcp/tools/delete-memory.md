---
id: mcp/tools/delete-memory
title: delete_memory
order: 314
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Drop one entry of your own memory in this workspace, by the name it is
  listed under.
concepts: []
used_with: [mcp/tools/list-memories]
---

[writes] [destructive] [idempotent]

```
delete_memory(category, key, scope="me")
```

Only when the person asks for it. It takes that one entry and nothing else of theirs; [`list_memories`](https://docs.popcorn.ai/mcp/tools/list-memories.md) shows what they keep.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `category` [required] | `str` | The entry's category, e.g. "agentchat". |
| `key` [required] | `str` | Its key, e.g. "style", or the short ID `list_memories` shows for an entry saved without one. |
| `scope` | `Scope` | "me", your own memory, which is the only one this deletes. Default `me`. |

**Example** — “Forget what I told you about how I like answers.”

```text
→ delete_memory(category="preferences", key="style")

Your own memory in this workspace
Deleted preferences/style. Nothing else changed.
```
