---
id: mcp/tools/read-reference
title: read_reference
order: 342
group: MCP
parent: mcp/tools
updated: 2026-11-04
summary: >
  One of a Routine's References: its text, or a download link for a file that
  isn't text, such as a PDF.
concepts: [reference-documents]
used_with: [mcp/tools/list-references]
---

[read-only]

```
read_reference(routine, reference)
```

A long text is cut, and the download link gives the whole file. A link works for a limited time; call again for a fresh one. On a workspace that guards personal data, neither the text nor a link is returned: Popcorn shows the file.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `reference` [required] | `str` | The Reference, as list_references names it. |

**Example** — “Show me the questions #intake sends.”

```text
→ read_reference(routine="#intake", reference="questions")

Routine: #intake (c7d2…5b)
Reference: Questions and first email (questions)
Used for: The questions, validation instructions and email wording for intake.
Added 2026-10-02 12:05 by Dana Reyes · file Intake questions.txt · text
Text:
Subject: Your claim with Acme

Hi {first_name},

Thanks for reaching out. To get your claim started, please reply with:
1. The date of the loss
2. Your policy number
3. Photos of the damage
```

The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool
shares: the Workspace a call runs in, dry runs and `confirm=true`,
`routine` and `routine_id`, and paging with `next_cursor`.
