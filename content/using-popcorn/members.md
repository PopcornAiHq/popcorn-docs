---
id: members
title: Members and Roles
order: 12
group: How a Routine works
summary: >
  Who may do what in a Routine. A Workspace Role and a Routine Role are
  separate. Most changes need a Member of the Routine or a Workspace admin;
  changing a prompt or an email's wording needs a Workspace admin who is
  also a Member, and a switch any Member. Your assistant has your Roles, so
  what it's refused you are too. list_workspace_members shows Roles.
lede: >
  Who is in a Workspace and in each Routine, and what their Role lets them
  do.
concepts: [routines, connections, routine-settings]
---

People belong to Popcorn at two levels, and each level gives them a
**Role**:

| Level | A Member is | Roles |
|---|---|---|
| **Workspace** | a person in the Workspace | owner, admin, member, guest |
| **Routine** | a person who has joined one [Routine](https://docs.popcorn.ai/routines.md) | owner, admin, member, guest |

The two Roles are separate. A Workspace admin isn't a Member of every
Routine, and someone invited into a Routine from another Workspace is a
guest there, whatever their Role at home.

## Joining a Routine

Who is in a Routine depends on how it was created:

- **An open Routine** adds everyone in the Workspace.
- **A private Routine** is joined only by the person who created it and the
  people they named.

The person who creates a Routine is its owner.

## Seeing who is in a Workspace

> "Who's in our Workspace?"

> [!TIP] MCP tool call
> Your assistant calls `list_workspace_members`, or `get_user` for one
> person.

Your assistant lists the Workspace's Members, each with their name,
username, email and Workspace Role, and can look one person up by name,
email or @username.

> [!NOTE] People from another Workspace
> Someone from another Workspace who is in a shared Routine isn't listed,
> and shows only their name and username. A deactivated Member isn't listed
> either; both are found by their ID only.

## What each Role can do

Most changes to a Routine need a Member of that Routine or a Workspace
admin. Some need more:

| To | You need to be |
|---|---|
| see a Routine's [Connections](https://docs.popcorn.ai/connections.md) | a Member of the Routine, or a Workspace admin |
| make a Connection, add a [Reference](https://docs.popcorn.ai/reference-documents.md), run a [Schedule](https://docs.popcorn.ai/triggers.md), finish a setup step | a Member of the Routine, or a Workspace admin |
| change a switch, such as whether emails are sent | a Member of the Routine |
| change any other [Routine Setting](https://docs.popcorn.ai/routine-settings.md), prompts and email wording included | a Workspace admin who is also a Member of the Routine |
| replace a Webhook someone else made | an admin of the Routine, or a Workspace admin |
| post in a Routine set to announcements only | an admin of the Routine, or a Workspace admin |
| stop a [Run](https://docs.popcorn.ai/history.md) | a Member or admin of the Routine, not a guest |
| create a Routine | anyone in the Workspace but a guest |
| publish a [Version](https://docs.popcorn.ai/versions.md) of a template | a Workspace admin |

> [!NOTE] Your assistant has your Roles
> Your assistant acts as you, so it can do what your Roles allow and
> nothing more. A change it's refused is one you would be refused too.
