---
id: mcp/tools/read-routine-file
title: read_routine_file
order: 345
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-05
summary: >
  Read one file of the Routine Template version a Routine runs, exactly as
  stored.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/list-routine-files]
---

[read-only]

```
read_routine_file(routine, path, version=None, cursor=None)
```

The content is never cut. A file too big for one response comes in byte ranges: the header says which bytes this is, and next_cursor reads the next range. Join the ranges in order to get the file, whose sha256 the header gives. Everything after the "Content:" line is the file's text, verbatim.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `path` [required] | `str` | The file's path, as list_routine_files shows it. |
| `version` | `int | str` | An older version of the Routine's template: its number ("0.15.1") or its version id. Omit for the base for edits. |
| `cursor` | `str` | next_cursor from the previous range. |

**Example** — “Show me #intake's app manifest.”

```text
→ read_routine_file(routine="#intake", path="manifest.yaml")

Routine: #intake (c7d2…5b)
Template: Claim Coordinator (claimcoordinator) · Popcorn's · 0.15.1 (version 812) · newest: yes
File: manifest.yaml  75 B  sha256: 4331d221…
Whole file.
Content:
app_type: claimcoordinator
display_name: Claim Coordinator
version: 0.15.1
```

The [Tools](https://docs.popcorn.ai/mcp/tools.md) page has what every tool
shares: `routine` and `routine_id`, dry runs and `confirm=true`, and paging
with `next_cursor`.
