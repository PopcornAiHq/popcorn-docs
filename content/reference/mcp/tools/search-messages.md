---
id: mcp/tools/search-messages
title: search_messages
order: 350
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Search message text across the Routines you can see, ranked by relevance or
  newest first.
concepts: []
used_with: [mcp/tools/read-message, mcp/tools/list-messages]
---

[read-only]

```
search_messages(query, routine=None, author=None, after=None, before=None, sort="relevance", cursor=None)
```

Direct messages are never searched, and the Routine's own agent searches only its Routine.

Each result names its Routine, and its `thread_id` when it is a reply; [`read_message`](https://docs.popcorn.ai/mcp/tools/read-message.md) returns a result in full. To see what followed a result, call [`list_messages`](https://docs.popcorn.ai/mcp/tools/list-messages.md) with its Routine and `after` set to its ID, and `thread_id` too when it is a reply.

To page through one Routine in time order, use `list_messages`.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `query` [required] | `str` | Words to search for. |
| `routine` | `str` | Only this Routine (ID or "#name"). |
| `author` | `str` | Only messages from this person: "@username", email, user ID, or "me". |
| `after` | `str` | Only messages from this ISO timestamp on (inclusive), or from this message's time on, the message itself left out. |
| `before` | `str` | Only messages up to this ISO timestamp (inclusive), or up to this message's time, the message itself left out. |
| `sort` | one of `relevance`, `recent` | "relevance" (default) or "recent". |
| `cursor` | `str` | `next_cursor` from the previous page. |

**Example** — “Find where anyone mentioned Northside Auto this month.”

```text
→ search_messages(query="Northside Auto", after="2026-09-01T00:00:00Z")

2 messages matching "Northside Auto", most relevant first:
[2026-09-29 14:03] (id: 9a3c…19) #intake · Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension.
[2026-09-12 10:15] (id: e11b…9d) #claims-east · Dana Smith: Northside Auto says the parts arrive Monday.
```
