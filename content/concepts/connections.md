---
id: connections
title: Connections
order: 4
group: How work arrives
summary: >
  A Connection is an account Popcorn uses on a Routine's behalf, such as the
  mailbox it reads or the calendar it books into. get_routine shows each one
  the Routine needs and whether it is connected; work that needs a missing
  one cannot run. A person makes a Connection in the browser, because it
  signs in as them: an assistant can find what is missing, not connect it.
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

Work that uses a missing Connection cannot run, so a Routine with one is
partly idle until someone connects it.

## Making one

A Connection signs in as a person, so a person makes it, in the Routine's
settings in Popcorn, in a browser. An assistant cannot make or change one:
what it can do is say which are missing and who needs to connect them.

`get_routine` reports whether an account is connected, not whether it still
has the access the work needs. A Connection whose access was revoked shows
as connected until work that uses it fails.
