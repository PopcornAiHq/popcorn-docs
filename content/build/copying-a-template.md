---
id: copying-a-template
title: Copying a template
order: 2
group: How a Version ships
summary: >
  Customizing a Routine beyond what its settings reach gives it a Copy that
  the Workspace owns (`popcorn app fork`). A Copy comes before any Publish,
  and a change published there reaches every Routine on it by their Daily
  Update, not only the one you changed. It is one-way: nothing undoes a Copy
  or moves a Routine back to Popcorn's version.
lede: >
  A Copy of a template is your Workspace's own. A change to it reaches every
  Routine on it, and a Copy can't be undone.
concepts: [customizing-a-routine, versions, app-bundle]
---

A Routine made from a Routine Template runs Popcorn's own version of it,
which every Workspace can install. To change what the
Routine is built from, the Workspace makes a Copy of the template (the CLI
calls it a *fork line*): a series of Versions the Workspace owns, which it
publishes to. Which changes need a Copy, and which stay with one Routine
without one, is in
[customizing a Routine](https://docs.popcorn.ai/customizing-a-routine.md).
This page is what a Copy costs and how to make one.

## Making one

| To | Over MCP | With the CLI |
|---|---|---|
| copy the template a Routine runs | `copy_routine_template(routine_id, name)` | `popcorn app fork --channel <routine> --name <copy>`, or `popcorn app checkout --channel <routine> --fork=<copy>`, which copies and checks out in one step |
| move a Routine onto a Copy the Workspace already has | `install_routine(routine_id, copy=<name>)` | `popcorn app fork --channel <routine> --name <copy>` with the existing Copy's name |
| see what a Routine runs | `get_routine`, whose **Updates from** says Popcorn or this Workspace's own Copy; `list_routines` says it for every Routine (`· Popcorn's` or `· copy "<name>"`) | `popcorn app list --channel <routine>` |
| list the Routines on a Copy | `list_routines(template=<template>, copy=<name>)`, the ones you can see | |
| list the Workspace's Copies | | `popcorn app lines` |

`copy_routine_template` is a dry run until it is called again with
`confirm=true`: the dry run names the Version being copied, the new Copy,
and any other Copies of the template the Workspace already has. It only
ever starts a new Copy; joining an existing one is `install_routine` with
`copy`, which is a dry run too.

The Copy starts byte-identical to the Version the Routine runs, and the
Routine moves onto it, so nothing it runs changes at that moment. Copying
needs a Routine Role of `member` or above, or a Workspace admin, so a guest
of the Routine is refused, and so is a Copy of an archived Routine;
publishing to the Copy afterwards needs a Workspace admin (see
[Versions](https://docs.popcorn.ai/versions.md)).

A Copy comes first. A Publish lands on a Copy the Workspace owns, so a
Publish based on Popcorn's version is refused. Over MCP, a Routine still on
Popcorn's version can dry-run a change with `create_routine_version`, which
is the way to check an edit before copying, since the Copy is the step that
cannot be undone.

## A Copy reaches every Routine on it

A Workspace has one Copy of a template unless it names more, and **every
Routine on a Copy is brought to the Copy's newest Version**: the one you
published from by an Install that starts at once, and each of the others by
its own Daily Update, within a day. The Daily Update runs as the Workspace,
not as the person who published, so whether that person is a Member of the
other Routines does not matter. A change tested on one Routine reaches the
others on the Copy. The exceptions are in
[installing](https://docs.popcorn.ai/versions.md#installing):
the Install on the Routine you published from can be blocked, and the Daily
Update skips some Routines. `create_routine_version`'s dry run counts the
other Routines a new Version will update, and `list_routines` with
`template` and `copy` names the Routines on the Copy that you can see.

A Routine already on a Copy can never move to another one. So a change
meant to reach some Routines and not their siblings needs a second, named
Copy, started from a different Routine that is still on Popcorn's version;
a second Copy can only be started from such a Routine. Once a Workspace has
two Copies of a template, a Routine still on Popcorn's version is refused
as ambiguous when it is copied or installed without naming one: the CLI's
`popcorn app fork` without `--name`, or an Install that names no Copy. A
Routine already on a Copy is unaffected; an Install there catches it up to
its own Copy's Head.

## A Copy is one-way

There is no undoing a Copy. A Routine on a Copy no longer receives the
template's improvements from Popcorn, and it cannot be moved back to
Popcorn's version or across to another Copy: the only move there is, is from
Popcorn's version onto a Copy. An earlier Version of the Copy can be read
back, but a Routine cannot be put back on it; the way back to old content is
to publish it forward as a new Version.

A Routine can also join a Copy without anyone meaning it to. Installing onto
a Routine still on Popcorn's version, in a Workspace that owns exactly one
Copy of its template, moves it onto that Copy, which is how a mistyped
Routine turns one in use into an edited Copy. Over MCP that Install is a dry
run first, and says so.

So copying is a decision about the Workspace, not a step in an edit. Check
the Routine's settings first, with `list_routine_settings` (in the CLI,
`popcorn channel-config params` and `popcorn table scalar`): a setting
reaches one Routine, can be set back, and survives the template's updates.
