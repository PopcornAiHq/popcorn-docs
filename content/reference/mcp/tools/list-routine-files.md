---
id: mcp/tools/list-routine-files
title: list_routine_files
order: 330
group: MCP
parent: mcp/tools
updated: 2026-11-05
summary: >
  List the files of the Routine Template version a Routine runs, with sizes
  and sha256.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/create-routine-version, mcp/tools/read-routine-file, mcp/tools/list-routine-settings]
---

[read-only]

```
list_routine_files(routine, version=None, paths=None, cursor=None)
```

The header names the template, whether it is Popcorn's or the workspace's own copy, and the version listed. By default that's the version edits are based on: on a copy, its newest version; on Popcorn's template, the version the Routine runs, which is what a copy starts from. That version is the base_version create_routine_version takes. Each row's sha256 is exact: copy it, don't retype it. Read a file's content with read_routine_file. To change how one Routine behaves, check list_routine_settings first: a copy of the template is one-way, and a new version reaches every Routine on that copy.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `version` | `int | str` | An older version of the Routine's template, to read its history. Pass its number ("0.15.1") or its version id. Omit for the base for edits. |
| `paths` | `list[str]` | Only files matching any of these: an exact path or a glob ("flows/*", "code/**"). |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What files make up the app #intake runs?”

```text
→ list_routine_files(routine="#intake")

Routine: #intake (c7d2…5b)
Template: Claim Coordinator (claimcoordinator) · Popcorn's · 0.15.1 (version 812) · newest: yes
6 of 6 files:
- AGENT.md  53 B  sha256: f7834927…
- flows/chase_estimate.yaml  21 B  sha256: 42def0cb…
- flows/daily_summary.yaml  20 B  sha256: 802c3a2f…
- … 3 more rows
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
