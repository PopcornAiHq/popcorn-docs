---
id: steps
title: Steps
order: 10
group: How a Routine works
summary: >
  A Routine's Steps are its work on each Item, in order: what each one asks
  for by email, what finishes it, and how it follows up when no reply comes. A
  Review is the kind of Step where a person decides. Where a template has
  Steps, they stay with the Routine; get_routine lists them, and
  change_routine changes them from a description, showing the change before it
  goes in.
lede: >
  A Routine's Steps are its work on each Item, in order: what each asks for,
  what finishes it, and how it follows up.
concepts: [reviews, customizing-a-routine, routine-settings]
---

A Routine's **Steps** are the work it does on each
[Item](https://docs.popcorn.ai/work-a-routines-items.md), in order. Each Step
asks for one thing and follows up until it has it. Then the Item moves on to
the next Step, or stops at a [Review](https://docs.popcorn.ai/reviews.md)
for a person to decide.

> [!NOTE] Not every Routine has Steps
> One that follows deliveries or alerts tracks each Item as it changes, in
> no fixed order, and Popcorn shows no Steps for it.

## Kinds of Step

In a claims intake Routine, where each Item is a potential client:

- **Answers** — asks questions by email, checks each answer against what a
  complete one needs, and asks again only for what is missing.
- **Signature** — sends an agreement through the Signing Provider and waits
  until everyone has signed.
- **Booking** — shares the Booking Page and waits until a meeting is on the
  calendar.
- **Reminder** — reminds the person before a meeting they have booked.
- **Delivery** — follows a mailed letter with the carrier until it is
  delivered.
- **Review** — waits for a person on the team to decide what happens next.

> [!NOTE] Every Step works by email
> None collects files: a document is asked for as one of a Step's
> questions.

## Following up

A Step sends its first email, then follows up while nothing comes back:

- **When.** On a reminder schedule, within the Routine's sending hours. The
  schedule and the hours are
  [Routine Settings](https://docs.popcorn.ai/routine-settings.md), and a
  Step can have its own.
- **Until.** When the follow-ups run out, the Item closes with a reason,
  such as *No response*.
- **After.** A reply after that reopens the Step it went quiet on.

An Item's [Status](https://docs.popcorn.ai/actions-and-status.md) names the
Step it is at, such as *Collecting info* or *Getting signatures*. The Status
a finished Item ends on is its **Outcome**, such as *Retained* or *Not
retained*.

## Seeing them

> "What are the Steps in #intake, and how many claims are at each?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine`, then `get_status`.

Your assistant lists the Steps in order, as the **Routine steps** tab in
Popcorn does:

- each Step's kind and name, and the ways an Item leaves it on its own;
- each Review's reason and choices, where each leads, and which are made
  only in Popcorn;
- the Version of the Steps that is installed;
- how many Items are at each Step.

> [!TIP] Filtering by Step
> Each Step shows its Status value. Ask your assistant for the Items at a
> Step, and it filters on that value.

## Changing them

> "In #intake, check with me before the agreement goes out."

A person changes the Steps by describing the change: to the Routine's
[Agent](https://docs.popcorn.ai/agent.md)
in Popcorn, or to their assistant. The Agent takes a few minutes to draft
it, and the proposal shows the Steps before and after before anything is
installed. The walkthrough is
[changing a Routine's Steps](https://docs.popcorn.ai/change-how-a-routine-behaves.md#change-its-steps).

- The change stays with this Routine and survives the template's
  improvements (see
  [customizing a Routine](https://docs.popcorn.ai/customizing-a-routine.md)).
- An earlier [Version](https://docs.popcorn.ai/versions.md), or the
  template's own, can be put back.
- A change that would remove a Step Items are still at is refused.
- One change is drafted at a time on a Routine.

> [!NOTE] Only where the template allows it
> A Routine's Steps can be changed this way only when its template keeps
> its Steps with the Routine. Otherwise your assistant says what changes
> them instead: a Routine Setting, or a Copy of the template.

## In the template

A Routine's Steps are the States of its template's
[State Machine](https://docs.popcorn.ai/state-machine.md), and a Routine
with Steps of its own has them installed as a Recipe. A Step is not one of a
[Flow](https://docs.popcorn.ai/flow-grammar.md)'s `steps:`.
