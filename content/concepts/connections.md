---
id: connections
title: Connections
order: 6
group: How work arrives
summary: >
  A Connection is an account Popcorn uses on a Routine's behalf, such as the
  mailbox it reads or the calendar it books into. list_connections names
  each one the Routine needs, whose account it uses, and what stops without
  it. With make_connection an assistant makes one after a dry run, from an
  account the person signed in to, or as a webhook. For Google it can hand
  them the sign-in link.
concepts: [routines, set-up-a-routine]
part: use
---

A Connection is an account Popcorn uses on a Routine's behalf: the mailbox it
reads new claims from, the calendar it books into, the drive it files
documents in. The Routine's template says which Connections it needs.

## Finding what is missing

- `list_routine_templates` and `create_routine`'s dry run list the
  Connections a template needs, before any Routine exists.
- `list_routines` marks a Routine with an unconnected one as
  `[missing a connection]`.
- `get_routine` lists every Connection the Routine needs, each as connected
  — with the account it uses — or **NOT CONNECTED**.
- `list_connections` is the full read for one Routine:

> "Why hasn't #intake booked any inspections?"

```text
3 Connections, 1 not made:
- Claims inbox (email): made
  Uses: claims@acme.example (google), connected by Dana Smith
  Without it: Popcorn shows the Routine as not ready, and claim intake can't run.
- Adjuster calendar (calendar): NOT MADE
  Without it: book inspection can't run; the rest of the Routine keeps working.
```

Each Connection says whose account it uses, who connected it, and what
stops while it is missing: some hold the whole Routine back, and Popcorn
shows it as not ready; others stop only the work that uses them. The
response ends with how to make the missing ones.

Work that uses a missing Connection cannot run, so a Routine with one is
partly idle until someone connects it.

## Making one

`make_connection` makes one of a Routine's Connections: it connects an
account the person has already signed in to, or makes the webhook another
system posts to. It is a dry run first; called again with `confirm=true`, it
makes the Connection.

- **An account.** Called without one, it lists the person's own accounts
  that can serve the Connection, and whether each one's sign-in allows
  everything it needs. Called with one, the dry run says what it connects,
  which account it replaces, and what runs after. The account also fills the
  Routine's other Connections that it can serve and that have none yet (one
  Google account serves the inbox, calendar and Drive together);
  `only=true` connects the named one alone.
- **A webhook.** The dry run says which webhook it replaces, if any, whose
  address then stops working. The confirm answers with the new address,
  once: it is a credential, since anyone who has it can post to the Routine.
  When the Routine's own Agent makes it, the address isn't shown in the
  Routine, where everyone would see it; the person reads it on the
  Connection's card in Popcorn.

Signing in to an account is still a person's job, because a Connection signs
in as them: only their own accounts can be connected, and a teammate connects
theirs. For a Google account not yet signed in to, or one whose sign-in lacks
access, `make_connection` may hand back a sign-in link to pass on. It works
once, within minutes, and only for the person who asked, who finishes it in
Popcorn in the browser. Any other account is signed in to in the Routine's
settings in Popcorn, and a signing provider's keys are saved there by a
workspace admin or owner.

Making a Connection needs workspace admin, or membership of the Routine.
Replacing a webhook someone else made needs an admin of the Routine or the
workspace.

## Connected, but without the access it needs

An account can be connected and still not have given this Routine what its
work needs, such as permission to send mail as well as read it. Both
`get_routine` and `list_connections` check that, and show such a Connection
as **NEEDS MORE ACCESS**, naming what is missing. A person fixes it the way
they made it, in Popcorn.

Neither checks whether an account was since revoked or its sign-in expired:
such a Connection shows as connected until work that uses it fails, and the
response says this isn't checked. When the access can't be read at all, the
Connection is marked as not checked rather than counted as made.
