---
id: connections
title: Connections
order: 8
group: How a Routine works
summary: >
  A Connection is an account Popcorn uses on a Routine's behalf, such as the
  mailbox it reads or the calendar it books into. list_connections names
  each one the Routine needs, whose account it uses, and what stops without
  it. With make_connection an assistant connects an account the person
  signed in to, at once when they asked for it, or makes a Webhook. For
  Google it can hand them the sign-in link.
lede: >
  A Connection is an account Popcorn uses on a Routine's behalf, such as the
  mailbox it reads or the calendar it books into.
concepts: [routines, set-up-a-routine]
---

A Connection is an account Popcorn uses on a
[Routine](https://docs.popcorn.ai/routines.md)'s behalf: the mailbox it
reads new claims from, the calendar it books into, the drive it files
documents in. The Routine's template says which Connections it needs.

## Finding what is missing

> "Why hasn't #intake booked any inspections?"

> [!TIP] MCP tool call
> Your assistant calls `list_connections`.

Your assistant lists every Connection the Routine needs:

```text
2 Connections, 1 not connected:
- Claims inbox (email): connected
  Uses: claims@acme.example (google), connected by Dana Smith
  Without it: the Routine's automations are paused, and claim intake can't run.
- Adjuster calendar (calendar): NOT CONNECTED
  Without it: book inspection can't run; the rest of the Routine keeps working.
```

Each Connection says whose account it uses, who connected it, and what
stops while it is missing. The response ends with how to make the missing
ones.

> [!WARNING] A missing Connection stops work
> Work that uses a missing Connection can't run. Some Connections hold back
> the whole Routine, and Popcorn pauses its automations until they're
> connected; others stop only the work that uses them.

> [!TIP] Other places it shows
> - A template's listing names the Connections it needs before any Routine
>   exists, and creating a Routine names them again.
> - The list of Routines marks one with an unconnected Connection as
>   `[missing a connection]`.
> - A Routine's details show each Connection as connected, with the account
>   it uses, or **NOT CONNECTED**.

## Making one

> "Connect my work calendar to #intake as the adjuster calendar."

> [!TIP] MCP tool call
> Your assistant calls `make_connection`.

Your assistant connects an account you have already signed in to, or makes
the Webhook another system posts to. When you ask to connect your own
account to a Connection you name, as here, it connects at once and says
which account it used. Otherwise it shows you what it would do first, and
makes the Connection once you agree:

- when you haven't named the Connection;
- when you have more than one account to choose from;
- when it would replace an account already connected;
- always, for a Webhook.

What it shows depends on the kind of Connection:

- **An account.** It names the account it would connect, the one it
  replaces, if any, and what runs after. The account also fills the
  Routine's other Connections that it can serve and that have none yet: one
  Google account serves the inbox, calendar and Drive together. Ask for the
  named Connection alone to connect just that one.
- **A Webhook.** It names the Webhook it replaces, if any, whose address
  then stops working. Once made, the answer gives the new address, once.

> [!WARNING] A Webhook's address is a credential
> Anyone who has the address can post to the Routine, and it isn't shown
> again. When the Routine's own [Agent](https://docs.popcorn.ai/agent.md)
> makes the Webhook, the address isn't
> posted in the Routine, where everyone would see it: read it on the
> Connection's card in Popcorn.

> [!NOTE] Only your own accounts
> A Connection signs in as the person who makes it, so you can connect only
> your own accounts; a teammate connects theirs. For a Google account you
> haven't signed in to, or whose sign-in lacks access, your assistant may
> give you a sign-in link. It works once, within minutes, and only for you;
> you finish it in Popcorn in the browser. Any other account is signed in to
> in Popcorn, and a
> [Signing Provider](https://docs.popcorn.ai/state-machine.md)'s keys are
> saved there by a Workspace admin or owner.

> [!NOTE] Who can make one
> Making a Connection needs a Workspace admin, or a
> [Member](https://docs.popcorn.ai/members.md) of the Routine.
> Replacing a Webhook someone else made needs an admin of the Routine or the
> Workspace.

## Connected, but without the access it needs

An account can be connected and still not have given this Routine what its
work needs, such as permission to send mail as well as read it. A Routine's
details and its list of Connections both check that, and show such a
Connection as **NEEDS MORE ACCESS**, naming what is missing. A person fixes
it the way they made it, in Popcorn.

> [!NOTE] Revoked sign-ins aren't checked
> A Connection whose account was since revoked, or whose sign-in expired,
> shows as connected until work that uses it fails, and the response says
> this isn't checked. When the access can't be read at all, the Connection
> is marked as not checked rather than counted as made.
