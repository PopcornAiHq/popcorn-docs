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
part: use
---

A **Reference** is a document a Routine works from: the agreement it sends
for signature, the sample email a Step's questions and wording come from,
the policy it checks claims against, an example of a good reply. A Reference informs the Routine. It is not one of the
items the Routine tracks, which live in its
[Tables](https://docs.popcorn.ai/use/concepts/tables.md).

A Routine's template says which References it expects, and the Routine works
without one it is still waiting for until someone adds it. A Reference belongs
to its Routine: adding or replacing one changes that Routine only, and survives
the template's improvements. The References a template expects are its
manifest's `documents:` key, where a document that starts work names the flow
it starts (see
[manifest keys](https://docs.popcorn.ai/build/concepts/manifest-keys.md)).

## Where they live today

People add and replace References in the Routine, in Popcorn. Adding some
documents also starts work, and `list_triggers` shows those under
**Documents** (see [Triggers](https://docs.popcorn.ai/use/concepts/triggers.md)). In a
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

`add_reference` adds or replaces a Reference from text, or from a file sent
with `create_reference_upload`. It is a dry run first: it says whether this
is a first add or a replacement and what the Routine uses the document for,
and refuses a file the Reference doesn't take. Called again with
`confirm=true`, it starts the same work Popcorn's **Replace** button starts.
An assistant whose network access is restricted may not reach the upload,
and sends a text document as `text` instead.

Two kinds of Reference stay in Popcorn, and `list_references` marks each
one with why:

- **A Reference picked from Google Drive.** A person picks it in Popcorn.
- **The Routine's Steps.** `change_routine` changes them, with a preview
  and a way back; `add_reference` won't replace them wholesale.

In the templates Popcorn ships today, every Reference is one of these, so
in practice a person still adds them in Popcorn.

The same people can add a Reference as in Popcorn: a workspace admin, or a
member of the Routine who isn't a guest.

## On a workspace that guards personal data

A Reference is free text, which no Column marking can vouch for. So on a
workspace that guards personal data, `list_references` leaves out file
names, and `read_reference` returns neither the text nor a link: it says
when the Reference was added and by whom, and that Popcorn shows it.