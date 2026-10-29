---
id: routines
title: Routines and Routine Templates
order: 3
group: Routines
summary: >
  A Routine is one piece of ongoing work Popcorn runs for you, such as claims
  intake, made from a Routine Template. An assistant finds Routines with
  list_routines, reads one with get_routine — its template, the version it
  runs, whether the latest install landed, its Connections — starts a new
  one from a template with create_routine, and copies one with
  duplicate_routine.
lede: >
  A Routine is a piece of ongoing work Popcorn runs for you, such as claims
  intake, made from a Routine Template.
concepts: [customizing-a-routine, connections, set-up-a-routine]
part: use
---

A Routine is one piece of ongoing work that Popcorn runs for you: claims
intake, order follow-up, renewals chasing. It reads across email, messages and
files, catches every update and decision, and keeps its items current. People
talk to its agent like a member of the team, and a person's assistant works
with it through the Popcorn MCP server.

Every Routine is made from a **Routine Template**, the starting point that
says what kind of work it is: a claims coordinator, an order follow-up. One
template can start many Routines, and each keeps receiving the template's
improvements unless it has been given a copy of its own (see
[customizing a Routine](https://docs.popcorn.ai/use/concepts/customizing-a-routine.md)).
The CLI and the API call a Routine a *channel*, with the same `#name` and
IDs, and a template's files are its
[app bundle](https://docs.popcorn.ai/build/concepts/app-bundle.md).

## Finding one

`list_routines` lists the Routines you can see in the workspace: the ones
you are in, Routines shared in from another workspace, and ones you can view
without joining, marked `[not joined]`. It filters by name
(`query`), by template (`template`, the template's slug), and can include
archived Routines. A Routine whose template needs an account nobody has
connected is marked `[missing a connection]`.

Names are not unique. Read tools accept a `#name` or an ID, and when more
than one Routine has the name they list the candidates; tools that change a
Routine take its ID only, so a write never lands on the wrong one by name.

## Reading one

`get_routine` shows one Routine in full:

| Field | What it says |
|---|---|
| Template | the Routine Template it is made from |
| Updates from | Popcorn, or this workspace's own copy of the template |
| Version | the template version it runs, and whether it is the latest |
| Install | whether the latest version has finished installing |
| Connections | each account the template needs, and whether it is connected |
| Copied from | for a duplicate, the Routine it copies and how far the copy has got |

`wait_seconds` (up to 20) waits for an install in progress to land before
answering, which is how an assistant follows a new Routine until it is ready.

## Starting one

`list_routine_templates` lists the templates this workspace can start a
Routine from, each with what it does and the Connections it needs.
`create_routine` makes the Routine, private or open to the whole workspace.
From a template it is a dry run first, showing the version that will install
and the Connections someone has to set up; the walkthrough is
[setting up a Routine](https://docs.popcorn.ai/use/guides/set-up-a-routine.md).

## Copying one

> "Make a copy of #claims-west for the east office, called claims-east."

`duplicate_routine` makes a new Routine that starts as a copy of an existing
one. Like `create_routine` it is a dry run first, and the dry run lists both
what it copies and what it leaves out:

| Copied | Not copied |
|---|---|
| its template, on the same line: a copy of a Routine on this workspace's own copy of the template joins that copy too, which is one-way | its Connections, which sign in as a person, so someone sets them up again |
| its Routine Settings and agent notes | credentials among its Routine Settings |
| its own Steps, as they are now | References picked from Google Drive, which are picked again once the copy has a Google Drive Connection |
| its agent's guidelines | what people told its agent |
| References added from a file | its items, History, messages and members |

Called again with `confirm=true`, it creates the Routine, private or open
to the workspace as `create_routine` does, not with the original's members.
The template installs in the background, and the copy runs once it lands.
`get_routine`'s **Copied from** line shows each part as it lands, and names
any part that didn't, with what to do about it.

In practice the templates Popcorn ships keep most of their References in
Google Drive, so a copy usually starts with its settings, Steps and
guidelines, and someone connects its accounts and picks its References
again in Popcorn.
