---
id: mcp/tools/save-memory
title: save_memory
order: 357
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-21
summary: >
  Keep something about the person you work for, for every later session of
  yours to read: your own memory in this workspace, under the name
  category/key.
concepts: []
used_with: [mcp/tools/get-memory, mcp/tools/catch-up]
---

[writes] [destructive] [idempotent]

```
save_memory(category, key, text, scope="me")
```

Save only what they asked you to remember — "remember this", "from now on …" — never something you worked out yourself. Working habits and preferences belong here. Secrets and credentials don't, and neither does anything about someone else.

A save replaces that entry whole, so read it first ([`get_memory`](https://docs.popcorn.ai/mcp/tools/get-memory.md)), fold the new line into it and write the lot back; nothing is appended for you, and a note that no longer holds is yours to drop. One entry holds 1,375 characters; a longer save is refused, never cut short.

Agent Chat notes: a standing rule for how your person works in Agent Chat Routines ("keep my posts to five lines") goes under category "agentchat:notes", one rule per entry under its own key. [`catch_up`](https://docs.popcorn.ai/mcp/tools/catch-up.md) shows them in every Agent Chat Routine they're in. Show your person the exact line first and save it only once they agree: never your own guess at how they work. One note holds 200 characters and all of them 4,000; a save over either is refused, saying which and by how much, never cut.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `category` [required] | `str` | What kind of entry this is, e.g. "preferences": the part before the "/" in its name. |
| `key` [required] | `str` | Its name within that category, e.g. "style". Saving to the same category and key replaces that entry. |
| `text` [required] | `str` | The whole entry, as it should read from now on. |
| `scope` | `Scope` | "me", your own memory, which is the only one this writes. Default `me`. |

**Example** — “Remember that I want short answers, and the numbers before the prose.”

```text
→ save_memory(category="preferences", key="style", text="Keep answers to three lines unless I ask for more. Put the numbers first, then what they mean.")

Your own memory in this workspace
Saved preferences/style, 94 characters (replacing what was there).
get_memory("preferences/style", scope="me") reads it back, saving it again replaces it, and delete_memory("preferences", "style", scope="me") drops it.
```
