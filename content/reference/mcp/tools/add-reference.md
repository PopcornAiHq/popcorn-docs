---
id: mcp/tools/add-reference
title: add_reference
order: 302
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Add one of a Routine's References, or replace the one it has, as Replace on
  the Reference's card in Popcorn does.
concepts: [reference-documents]
used_with: [mcp/tools/create-reference-upload, mcp/tools/change-routine, mcp/tools/list-references]
---

[writes] [destructive] [dry run]

```
add_reference(routine_id, reference, text=None, upload_id=None, confirm=False, plan_id=None)
```

Pass exactly one of `text`, the Reference's whole text, or `upload_id`, a file uploaded with [`create_reference_upload`](https://docs.popcorn.ai/mcp/tools/create-reference-upload.md). Only the References the Routine's template expects can be added, and only with a file of a kind each takes. A Reference picked from Google Drive is picked in Popcorn instead, and one holding the Routine's Steps is changed with [`change_routine`](https://docs.popcorn.ai/mcp/tools/change-routine.md); [`list_references`](https://docs.popcorn.ai/mcp/tools/list-references.md) marks both.

Without `confirm=true` this is a dry run that changes nothing: it says whether this is a first add or a replace, what the Routine uses the Reference for, and, for a required one, what starts working once it's in. When the person asked to add this document as this Reference and it has none yet, confirm at once, without a dry run; otherwise show the dry run, and confirm once they agree. Replacing a document the Reference already has is confirmed only with its dry run's `plan_id`: a confirm without one is refused, and changes nothing. Once confirmed, Popcorn reads the file in the background and the Routine works from it from then on; `list_references` shows it once it's in. Each confirmed call with `text` adds it again, so don't repeat one that timed out: check `list_references` first. Workspace admins and members of the Routine only.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `reference` [required] | `str` | The Reference, as `list_references` names it. |
| `text` | `str` | The Reference's whole text, for a Reference that takes a plain text file. At most 1.5 MB. |
| `upload_id` | `str` | The `upload_id` `create_reference_upload` gave, once the file is uploaded. |
| `confirm` | `bool` | true to add it: at once when the person asked to add this document as this Reference, otherwise (a replace, or a Reference you chose) after they agree to the dry run. Default `False`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true` and the same request. Required to replace a document the Reference already has (that dry run gives every caller one). A Routine's own agent in Popcorn must pass it, from a dry run in an earlier run; an assistant connected from outside Popcorn is given none for a first add and needn't. |

**Example** — “Add a fourth question to #intake's questions: the claim number.”

```text
→ add_reference(routine_id="c7d2…5b", reference="questions", text="Subject: Your claim with Acme\n\nHi {first_name},\n\nThanks for reaching out. To get your claim started, please reply with:\n1. The date of the loss\n2. Your policy number\n3. Photos of the damage\n4. Your claim number, if you already have one\n")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Add: Questions and first email (reference "questions") on #intake.
- From the text given: 236 characters, added as a plain text file (questions.txt).
- Replaces the one in now. Added 2026-10-02 12:05 by Dana Reyes · file Intake questions.txt · text
- Used for: The questions, validation instructions and email wording for intake.
- Required: the template counts on it, and what it is used for starts working once it's in.
- Popcorn reads the file in the background, and the Routine works from it from then on.
- plan_id: pL4nR3pl4ceQu3st10ns7a (lasts 30 minutes). Confirm with it and the same request.

Call again with `confirm=true` to replace it.

→ add_reference(routine_id="c7d2…5b", reference="questions", text="Subject: Your claim with Acme\n\nHi {first_name},\n\nThanks for reaching out. To get your claim started, please reply with:\n1. The date of the loss\n2. Your policy number\n3. Photos of the damage\n4. Your claim number, if you already have one\n", confirm=true, plan_id="pL4nR3pl4ceQu3st10ns7a")

Routine: #intake (c7d2…5b)
Started replacing Questions and first email (reference "questions").
Popcorn reads the file in the background. list_references shows it once it's in, as added just now; if it isn't after a few minutes, the Reference's card in Popcorn says why.
```
