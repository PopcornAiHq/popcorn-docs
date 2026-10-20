---
id: connections
title: Connections
order: 4
group: How work arrives
summary: >
  A Connection is an account Popcorn uses on a Routine's behalf, such as the
  mailbox it reads or the calendar it books into. list_connections names
  each one the Routine needs, whose account it uses, and what stops without
  it. A person makes a Connection
  in the browser, because it signs in as them: an assistant can find what is
  missing, not connect it.
concepts: [routines, set-up-a-routine]
layer: product
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
response ends with where in Popcorn a person makes the missing ones.

Work that uses a missing Connection cannot run, so a Routine with one is
partly idle until someone connects it.

## Making one

A Connection signs in as a person, so a person makes it, in the Routine's
settings in Popcorn, in a browser. An assistant cannot make or change one:
what it can do is say which are missing and who needs to connect them.

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
