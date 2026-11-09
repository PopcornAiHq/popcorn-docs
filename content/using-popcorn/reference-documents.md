---
id: reference-documents
title: References
order: 6
group: How a Routine works
summary: >
  A Reference is a document a Routine works from: a policy, a price list, a
  form to fill, an example of good work, not one of its Items.
  list_references names the ones a Routine has and is waiting for,
  read_reference returns one's text or a download link, and add_reference
  adds one, as Popcorn does; adding some starts work, which list_triggers
  lists.
lede: >
  A Reference is a document a Routine works from, such as a policy, a price
  list or an example of good work.
concepts: [triggers, customizing-a-routine]
---

A **Reference** is a document a
[Routine](https://docs.popcorn.ai/routines.md) works from:

- the agreement it sends for signature;
- the sample email a [Step](https://docs.popcorn.ai/steps.md)'s questions
  and wording come from;
- the policy it checks claims against;
- an example of a good reply.

A Reference informs the Routine. It is not one of the Items the Routine
tracks, which live in its [Tables](https://docs.popcorn.ai/tables.md).

A Routine's template says which References it expects, and the Routine works
without one it is still waiting for until someone adds it. A Reference
belongs to its Routine: adding or replacing one changes that Routine only,
and survives the template's improvements.

> [!TIP] In the template
> The References a template expects are its Manifest's `documents:` key,
> where a document that starts work names the Flow it starts. See
> [Manifest keys](https://docs.popcorn.ai/manifest-keys.md).

## Adding one can start work

Adding some documents also starts work, and a Routine's
[Triggers](https://docs.popcorn.ai/triggers.md) list those under
**Documents**. In a claims intake Routine:

- adding the sample email sets up the first Step's questions and its first
  email;
- adding the agreement, a Google Doc or a Word file, makes it the one sent
  for signature.

The sample email is the one Reference that Routine requires.

## Which References a Routine has

> "What documents does #intake work from?"

> [!TIP] MCP tool call
> Your assistant calls `list_references`.

Your assistant lists every Reference the Routine's template expects:

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
it, and, once added, when and by whom, with its file.

> [!NOTE] Drive picks don't say who
> A Reference picked from Google Drive shows when it was picked, but not who
> picked it: Popcorn doesn't record that. In a claims intake Routine, whose
> agreement is always a Drive pick, most listings say so.

## Reading one

> "Show me #intake's fee schedule."

> [!TIP] MCP tool call
> Your assistant calls `read_reference`.

A text document comes back as its text, cut if it is long, with a link to
the whole file. Any other file, such as a PDF, comes back as a download link
that works for a limited time.

## Adding or replacing one

> "Add a fourth question to #intake's questions: the claim number."

> [!TIP] MCP tool call
> Your assistant calls `add_reference`, with the text or with a file it
> sent with `create_reference_upload`.

A first add you asked for happens at once. Replacing a document the
Reference already has shows you first what the Routine uses it for and what
it replaces; once you agree, it starts the same work Popcorn's **Replace**
button starts. A file the Reference doesn't take is refused either way.

> [!TIP] No upload access
> An assistant whose network access is restricted may not reach the upload,
> and sends a text document as text instead.

Two kinds of Reference stay in Popcorn, and the listing marks each one with
why:

- **A Reference picked from Google Drive.** A person picks it in Popcorn.
- **The Routine's Steps.** They change by describing the change, with a
  preview and a way back (see
  [Change how a Routine behaves](https://docs.popcorn.ai/change-how-a-routine-behaves.md)),
  not by replacing the document wholesale.

Your assistant adds any other Reference, such as the Questionnaire
template's questionnaire in
[Set up your first Routine](https://docs.popcorn.ai/set-up-a-routine.md).

> [!NOTE] Who can add one
> The same people as in Popcorn: a Workspace admin, or a Member of the
> Routine who isn't a guest.

## On a Workspace that guards personal data

A Reference is free text, which no Column marking can vouch for. So on a
Workspace that guards personal data, the listing leaves out file names, and
reading a Reference returns neither the text nor a link: it says when the
Reference was added and by whom, and that Popcorn shows it.
