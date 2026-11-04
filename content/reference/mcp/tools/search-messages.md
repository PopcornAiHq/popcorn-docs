---
id: mcp/tools/search-messages
title: search_messages
order: 345
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  Search message text across the Routines you can see, ranked by relevance (or
  newest first with sort="recent").
concepts: []
used_with: [mcp/tools/read-message, mcp/tools/list-messages]
---

[read-only]

```
search_messages(query, routine=None, author=None, after=None, before=None, sort="relevance", cursor=None)
```

Direct messages are never searched. Each result names its Routine; read_message returns a result in full, and list_messages(Routine, after=<id>) shows what followed it. To page through one Routine in time order, use list_messages.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `query` [required] | `str` | Words to search for. |
| `routine` | `str` | Only this Routine (ID or "#name"). |
| `author` | `str` | Only messages from this person: "@username", email, user ID, or "me". |
| `after` | `str` | Only messages from this ISO timestamp on (inclusive), or from this message's time on, the message itself left out. |
| `before` | `str` | Only messages up to this ISO timestamp (inclusive), or up to this message's time, the message itself left out. |
| `sort` | one of `relevance`, `recent` | "relevance" (default) or "recent". |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “Find where anyone mentioned Northside Auto this month.”

```text
→ search_messages(query="Northside Auto", after="2026-09-01T00:00:00Z")

2 messages matching "Northside Auto", most relevant first:
[2026-09-29 14:03] (id: 9a3c…19) #intake · Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension.
[2026-09-12 10:15] (id: e11b…9d) #claims-east · Dana Smith: Northside Auto says the parts arrive Monday.
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
