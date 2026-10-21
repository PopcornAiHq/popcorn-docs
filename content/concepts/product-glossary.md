---
id: product-glossary
title: Product glossary
order: 1
layout: lookup
summary: >
  The product's nouns. A person manages one thing, a Routine (once called a
  project), made from a Routine Template; its Triggers bring work in, its Tables hold it, its Status
  says where each item stands, and its Actions move it on. How Popcorn builds
  a Routine stays behind these names. The platform glossary maps each one to
  the platform's terms.
concepts: [glossary]
layer: product
---

The words a person sees, and the words an assistant should use when it talks
to one. Ask for an outcome in these terms, such as "add a reminder to this
Routine" or "make me a copy of this Routine for the Denver office", and
Popcorn decides what has to change underneath.

Today's tools, the API and the CLI still use older and more technical names
for several of these. The
[platform glossary](https://docs.popcorn.ai/platform/glossary/glossary.md) gives each of
its terms the product term it belongs to.

## Routines

- **workspace** — Your organisation's space in Popcorn. It holds its
  Routines, its people and its Routine Templates, and an assistant connected
  to Popcorn works in one workspace at a time.
- **Routine** — One piece of ongoing work that Popcorn runs for you, such as
  claims intake or order follow-up, together with everything it needs: how
  work arrives, what it knows, what it holds and who takes part. A Routine is
  the one thing a person manages; ask for a change to it, and Popcorn works
  out how to make it.
- **Routine Template** — The starting point a Routine is made from, such as
  a claims coordinator. One template can start many Routines, and a Routine
  made from one keeps receiving the template's improvements unless it has been
  changed into a copy of its own (see *customizing a Routine*).
- **Inbox Scan** — The Routine Template that reads a mailbox, suggests
  Routines from the work it finds there, and shows how the team writes.
- **customizing a Routine** — Changing one Routine without changing the
  others made from the same template. Most changes stay with that one Routine
  and survive the template's improvements: its Routine Settings, its
  Connections, its Instructions and, where its template keeps them with the
  Routine, its steps and the Actions between them. A change to what the
  Routine is built from (a new Table, a kind of step its template does not
  offer) gives it a copy of its own instead. That copy no longer
  receives the template's improvements, which cannot be undone. Popcorn says
  which kind a change is before it makes it.

## How work arrives

- **Trigger** — How work arrives in a Routine: on a schedule, from a message
  in the Routine, from a document added to it, from a booking made through
  its calendar link, or from another system posting to it. A Routine can have
  several.
  *Not to be confused with* an Action, which is a person moving one item on.
- **Connection** — An account Popcorn uses on the Routine's behalf, such as a
  mailbox it reads from or a calendar it books into. It signs in as a person,
  so only their own accounts can be connected; an assistant can say which ones
  a Routine is missing and, after a dry run, connect an account the person has
  signed in to, or make a webhook.
- **Reference** — A document a Routine works from: a policy, a price list, a
  form to fill, an example of good work. A Reference informs the Routine; it
  is not one of the items the Routine tracks.
- **booking page** — The calendar link people book a meeting through. A
  booking made on it can start an item's work, or complete a booking Step.
- **signing provider** — The service an agreement is sent through for
  signature. Its account is set up per Routine, and Popcorn tracks who has
  signed.

## How it behaves

- **Instructions** — What the Routine should do and how, in plain language:
  how to word a follow-up, when to ask a person first, which deadlines matter,
  when to send a reminder. Changing them changes how the Routine behaves from
  then on.
- **Routine Settings** — The values that tune a Routine without changing
  what it does: switches that turn a behaviour on or off, and values such as a
  reminder interval or a sender name. A setting reaches only its own Routine,
  can be set back, and survives the template's improvements.
- **Agent** — The assistant inside a Routine that does its work and that
  people talk to. It follows the Routine's Instructions, and it asks before
  the steps the Instructions say need a person.

## What it does

- **Step** — One part of a Routine's work on each item, in order: what it
  asks for, what finishes it, and how it follows up until then. Not every
  Routine has Steps. *Not to be confused with* a Trigger, which brings an
  item in; Steps are what happens to it after.
- **Review** — The kind of Step where a person decides instead of Popcorn.
  The item waits, says why, and offers the Actions that decide where it goes
  next. *Not to be confused with* an Action: a Review is the Step that
  waits, and an Action is the button that ends it.
- **Approval** — One kind of Review, "should this go ahead?", and the
  outcome of a Review that passes.

## What it holds

- **item** — One thing a Routine works on, such as a potential client in an
  intake Routine or an order on its way to a customer. Each item is a Row in
  one of the Routine's Tables. An item is not always a person.

- **Table** — A set of items the Routine keeps, such as claims, orders or
  contacts, shown as rows and columns.
- **Row** — One item in a Table: one claim, one order.
- **Column** — One kind of information every Row in a Table has, such as a
  due date or an amount.
- **Cell** — One Row's value in one Column.
- **Status** — Where an item stands, such as *Waiting on documents* or
  *Approved*. Popcorn works it out from what has happened to the item, so it
  changes when an Action is taken or the Routine moves the item on, not by
  editing the Cell. *Not to be confused with* whether a single run of the
  Routine finished.
- **outcome** — The Status a finished item ends on, such as *Retained* or
  *Not retained*.

## What people do, and what happened

- **Action** — Something a person does to move an item on: approve, send,
  archive, retry. A Routine offers an item the Actions that make sense for
  where it stands, so the buttons and the Status cannot disagree.
- **History** — What has happened in a Routine: the work it ran and how each
  run ended, the conversation in it, and the changes to its items, with who or
  what made each one.
