---
id: reviews
title: Reviews
order: 10
group: Day to day
summary: >
  A Review is the kind of Step where a person makes the call instead of
  Popcorn: the Item waits, says why, and gives a few choices of where it goes
  next. Approval is one kind of Review, and its passing Outcome. get_status
  lists what is waiting and why; take_action takes a choice, except one that
  opens a form in Popcorn.
lede: >
  A Review is where a person, not Popcorn, makes the call: the Item waits,
  says why, and offers a few choices of where it goes next.
concepts: [steps, actions-and-status, routine-settings]
---

A **Review** is a [Step](https://docs.popcorn.ai/steps.md) where the
[Routine](https://docs.popcorn.ai/routines.md) stops and waits for a person.
The Item says why it is waiting and offers a few choices, each an
[Action](https://docs.popcorn.ai/actions-and-status.md) that leads somewhere:

- on to the next Step;
- straight to an Outcome;
- or past work already done.

In a claims intake Routine, the Review after the questions says: "Intake is
done. Send the document for signature, record it as already signed, or do
not send the retainer." Its choices are:

| Choice | What happens |
|---|---|
| **Send retainer** | A person checks every field of the agreement before it goes; once it is sent, the Item moves on to signing. |
| **Already signed** | For an agreement signed outside Popcorn: the Item moves on as a signature would have moved it. |
| **Do not send retainer** | The Item ends as *Not retained*, and the person is sent a short, neutral email saying the firm can't take it further. |

**Approval** is one kind of Review, "should this go ahead?", and also what a
Review that passes ends in. A Review can end in other ways too, such as "not
a fit" or "already done".

## What is waiting

> "Who in #intake is waiting for us to review them?"

> [!TIP] MCP tool call
> Your assistant calls `get_status`, then `list_rows` with a filter on the
> Status Column for the Items at one Review in full.

Your assistant counts the Items at each Status, marks the Statuses that need
a person, and lists what is waiting, newest first, with why and which Items.

> [!TIP] In Popcorn
> Items at a Review show as needing review. Each one's Status names its
> Review, such as *Needs retainer review*.

## Making the choice

> "Dana signed on paper. Mark Dana as already signed."

> [!TIP] MCP tool call
> Your assistant calls `list_actions` to see the choices, then
> `take_action`.

Your assistant makes the choice as pressing its button would: straight away
when you named the Item and the choice, and otherwise once you agree to what
it shows you.

> [!NOTE] Some choices are made in Popcorn
> A choice that opens a form, such as sending an agreement whose fields a
> person checks first, is made in Popcorn. Your assistant lists it and says
> so.

## Work done outside Popcorn

Some work happens without the Routine: an answer given on the phone, a call
already held. When the Routine's **Step forward**
[setting](https://docs.popcorn.ai/routine-settings.md) is on, an Item offers
choices such as *Already answered* or *Call already held*, which move it
past a Step without waiting for it.

## Adding or removing a Review

A Review is a Step, so you add or remove one the way you change any Step:
by asking your assistant or telling the Routine's Agent in Popcorn, for
example "check with me before booking the meeting" (see
[changing its Steps](https://docs.popcorn.ai/change-how-a-routine-behaves.md)).
The change stays with this Routine and survives the template's
improvements; it doesn't give the Routine a Copy of its own. Without a
Review, the Routine moves the Item on by itself.

> [!TIP] Building a template
> In the template, a Review is a State that warns, with the Transitions
> people can take from it (see
> [State Machines in a Bundle](https://docs.popcorn.ai/state-machine.md)).
> It is not a Flow's `await_approval`, which pauses one Run until someone
> replies.
