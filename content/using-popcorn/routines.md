---
id: routines
title: Routines and Routine Templates
order: 5
group: How a Routine works
summary: >
  A Routine is one piece of ongoing work Popcorn runs for you, such as claims
  intake, made from a Routine Template. An assistant finds Routines with
  list_routines, reads one with get_routine — its template, the Version it
  runs, whether the latest Install landed, its Connections — starts a new
  one from a template with create_routine, and makes a copy of one with
  duplicate_routine.
lede: >
  A Routine is a piece of ongoing work Popcorn runs for you, such as claims
  intake, made from a Routine Template.
concepts: [customizing-a-routine, connections, set-up-a-routine]
---

A Routine is one piece of ongoing work that Popcorn runs for you: claims
intake, order follow-up, renewals chasing. It reads across email, messages and
files, catches every update and decision, and keeps its
[Items](https://docs.popcorn.ai/work-a-routines-items.md) current. People
talk to its [Agent](https://docs.popcorn.ai/agent.md) like a member of the
team, and a person's assistant works
with it through the
[Popcorn MCP server](https://docs.popcorn.ai/add-the-mcp-server.md).

Every Routine is made from a **Routine Template**, the starting point that
says what kind of work it is: a claims coordinator, an order follow-up. One
template can start many Routines, and each keeps receiving the template's
improvements unless it has been given a
[Copy](https://docs.popcorn.ai/copying-a-template.md) of its own (see
[customizing a Routine](https://docs.popcorn.ai/customizing-a-routine.md)).

> [!NOTE] Another name in the CLI and API
> The CLI and the API call a Routine a *channel*, with the same `#name` and
> IDs, and a template's files are its
> [App Bundle](https://docs.popcorn.ai/app-bundle.md).

## Finding one

> "Which Routines are made from the claims coordinator template?"

> [!TIP] MCP tool call
> Your assistant calls `list_routines`, with a `query` for a name or a
> `template` for a template.

Your assistant lists the Routines you can see in the Workspace:

- the ones you're in, including Routines shared in from another Workspace;
- ones you can view without joining, marked `[not joined]`;
- archived ones, when you ask for them.

Each row names the Routine's template and whose version of it it runs. A
Routine whose template needs an account nobody has connected is marked
`[missing a connection]`.

> [!NOTE] Names aren't unique
> Your assistant can read a Routine by its `#name` or its ID, and when more
> than one Routine has the name it lists the candidates. Changing a Routine
> takes its ID only, so a change never lands on the wrong one by name.

## Reading one

> "What state is #team-offsite in?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine`.

Your assistant shows one Routine in full:

| Field | What it says |
|---|---|
| Template | the Routine Template it is made from |
| Updates from | Popcorn, or this Workspace's own Copy of the template |
| Version | the template [Version](https://docs.popcorn.ai/versions.md) it runs, and whether it is the latest |
| Install | whether the latest Version has finished installing |
| Connections | each account or Webhook the template needs, and whether it is [connected](https://docs.popcorn.ai/connections.md) |
| Steps | for a template with [Steps](https://docs.popcorn.ai/steps.md), each in order, and which version of them is installed |
| Copied from | for a duplicate, the Routine it copies and how far the copy has got |

Only the Routine's [Members](https://docs.popcorn.ai/members.md) and Workspace
admins see its Connections. A
Routine shared in from another Workspace shows no Version, Connections or
Steps, because its home Workspace manages them.

> [!TIP] Waiting for an Install
> Your assistant can wait up to 20 seconds for an Install in progress to
> land before it answers. That is how it follows a new Routine until it is
> ready.

## Starting one

> "Which templates can I start a Routine from?"

> [!TIP] MCP tool call
> Your assistant calls `list_routine_templates`, then `create_routine`.

Your assistant lists the templates this Workspace can start a Routine from,
each with what it does and the Connections it needs. It creates the Routine
at once, private or open to the whole Workspace, and names the Version that
installs and the Connections someone has to set up. The walkthrough is
[setting up your first Routine](https://docs.popcorn.ai/set-up-a-routine.md).

## Copying one

> "Make a copy of #team-offsite for the spring offsite, called spring-offsite."

> [!TIP] MCP tool call
> Your assistant calls `duplicate_routine`, then calls it again with
> `confirm=true`.

Your assistant makes a new Routine that starts as a copy of an existing one.
First it shows you what it copies and what it leaves out:

| Copied | Not copied |
|---|---|
| its template, from the same place | its Connections, which sign in as a person, so someone sets them up again |
| its [Routine Settings](https://docs.popcorn.ai/routine-settings.md) changed from the template's | credentials among its Routine Settings |
| its own Steps, as they are now | [References](https://docs.popcorn.ai/reference-documents.md) picked from Google Drive, picked again once the copy has a Google Drive Connection |
| its Agent's guidelines | what people told its Agent |
| References added from a file | its Items, [History](https://docs.popcorn.ai/history.md), messages and Members |

Once you agree, it creates the Routine without the original's Members:
open to the whole Workspace unless you ask for it private, even when the
original is private. The template installs in the background, and
the copy runs once it lands. The Routine's **Copied from** field shows each
part as it lands, and names any part that didn't, with what to do about it.

> [!CAUTION] A copy of a Copy follows it for good
> A Routine on this Workspace's own Copy of its template makes a duplicate
> on that same Copy, and the duplicate can't go back to Popcorn's template.

> [!NOTE] What a copy usually needs
> The templates Popcorn ships keep most of their References in Google
> Drive. So a copy usually starts with its settings, Steps and guidelines,
> and someone connects its accounts and picks its References again in
> Popcorn.
