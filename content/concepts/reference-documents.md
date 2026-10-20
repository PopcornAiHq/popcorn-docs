---
id: reference-documents
title: References
order: 5
group: How work arrives
summary: >
  A Reference is a document a Routine works from: a policy, a price list, a
  form to fill, an example of good work. It informs the Routine and is not one
  of its items. list_references names the ones a Routine has and the ones
  it is still waiting for, and read_reference returns one's text or a
  download link. People add References in Popcorn; adding some starts work,
  which list_triggers lists.
concepts: [triggers, customizing-a-routine]
layer: product
---

A **Reference** is a document a Routine works from: the agreement it sends
for signature, the sample email a Step's questions and wording come from,
the policy it checks claims against, an example of a good reply. A Reference informs the Routine. It is not one of the
items the Routine tracks, which live in its
[Tables](https://docs.popcorn.ai/product/concepts/tables.md).

A Routine's template says which References it expects, and the Routine works
without one it is still waiting for until someone adds it. A Reference belongs
to its Routine: adding or replacing one changes that Routine only, and survives
the template's improvements.

## Where they live today

People add and replace References in the Routine, in Popcorn. Adding some
documents also starts work, and `list_triggers` shows those under
**Documents** (see [Triggers](https://docs.popcorn.ai/product/concepts/triggers.md)). In a
claims intake Routine, adding the sample email sets up the first Step's
questions and its first email, and adding the agreement, a Google Doc or a
Word file, makes it the one sent for signature. The sample email is the one Reference
that Routine requires.

## Which References a Routine has

> "What documents does #intake work from?"

`list_references` lists every Reference the Routine's template expects:

```text
3 References: 2 added, 1 still waiting.
- Questions and first email  reference "questions"  [required]
  Used for: The questions, validation instructions and email wording for intake.
  Added 2026-10-02 12:05 by Dana Reyes · file Intake questions.txt · text
- Fee schedule  reference "fee_schedule"
  Used for: The fees quoted when a claimant asks what it costs.
  Still waiting: nobody has added it yet.
```

Each one says what the Routine uses it for, whether the Routine requires
it, and, once added, when and by whom, with its file. A Reference picked
from Google Drive shows when it was picked, but not who picked it: Popcorn
doesn't record that. In a claims intake Routine, whose agreement is always
a Drive pick, most listings say so.

## Reading one

`read_reference` takes a Reference as `list_references` names it. A text
document comes back as its text, cut if it is long, with a link to the
whole file; any other file, such as a PDF, comes back as a download link
that works for a limited time.

## Adding or replacing one

A person adds or replaces a Reference in the Routine, in Popcorn. An
assistant can't yet: `add_reference` is among the MCP reference's
[proposed tools](https://docs.popcorn.ai/product/reference/mcp.md), and nothing depends on it
arriving.

## On a workspace that guards personal data

A Reference is free text, which no Column marking can vouch for. So on a
workspace that guards personal data, `list_references` leaves out file
names, and `read_reference` returns neither the text nor a link: it says
when the Reference was added and by whom, and that Popcorn shows it.

> **Platform note** — The References a template expects are its manifest's
> `documents:` key, and a document that starts work names the flow it starts.
> See [manifest keys](https://docs.popcorn.ai/platform/concepts/manifest-keys.md).
