---
id: mcp/tools/list-triggers
title: list_triggers
order: 339
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  List how work arrives in a Routine: each schedule with its cadence, each
  webhook another system posts to, each message or document that starts work.
concepts: [triggers]
used_with: [mcp/tools/run-trigger]
---

[read-only]

```
list_triggers(routine)
```

A Trigger that is paused or turned off says so. A webhook's address is never shown: it is a credential. run_trigger runs a schedule now.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What sets #intake working?”

```text
→ list_triggers(routine="#intake")

Routine: #intake (c7d2…5b) · template: claimcoordinator 0.15.1
Schedules:
- morning  cron '0 8 * * 1-5' (America/Los_Angeles)  starts daily digest
- tick  every 3 minutes  starts claim tick
Webhooks:
- carrier-portal  starts claim intake
Messages:
- a message posted in #intake  starts claim intake
Documents:
- uploading the 'policy' document  starts policy upsert
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
