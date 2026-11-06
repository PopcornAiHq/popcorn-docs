---
id: mcp/tools/list-references
title: list_references
order: 331
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  The documents a Routine works from (its References), each with what it is
  used for, when it was added and by whom, and the ones it is still waiting
  for.
concepts: [reference-documents]
used_with: [mcp/tools/read-reference, mcp/tools/add-reference]
---

[read-only]

```
list_references(routine)
```

A Reference marked required is one the template counts on; the Routine works without it until someone adds it. read_reference returns one's text, or a download link for a file that isn't text. A Reference add_reference can't take is marked with why. On a workspace that guards personal data, file names aren't listed.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What documents does #intake work from?”

```text
→ list_references(routine="#intake")

Routine: #intake (c7d2…5b)
3 References: 2 added, 1 still waiting.
- Questions and first email  reference "questions"  [required]
  Used for: The questions, validation instructions and email wording for intake.
  Added 2026-10-02 12:05 by Dana Reyes · file Intake questions.txt · text
- Standard retainer agreement  reference "standard_retainer"  [required]
  Used for: The retainer every retained claimant signs.
  Added 2026-10-09 08:53, picked from Google Drive; who picked it isn't recorded · file Retainer 2026.pdf · pdf
  add_reference can't add it: it is picked from Google Drive, in Popcorn.
- Fee schedule  reference "fee_schedule"
  Used for: The fees quoted when a claimant asks what it costs.
  Still waiting: nobody has added it yet.
read_reference(routine="#intake", reference="<name>") returns one's text or a download link.
add_reference adds or replaces a Reference not marked otherwise, as its card in Popcorn does; adding one starts work, which list_triggers shows.
```

The [Tools](https://docs.popcorn.ai/mcp/tools.md) page has what every tool
shares: `routine` and `routine_id`, dry runs and `confirm=true`, and paging
with `next_cursor`.
