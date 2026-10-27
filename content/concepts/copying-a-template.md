---
id: copying-a-template
title: Copying a template
order: 14
group: How a version ships
summary: >
  Customizing a Routine beyond what its settings reach gives it a copy that
  the workspace owns (`popcorn app fork`). A copy comes before any publish,
  and a change published there reaches every Routine on it by their daily
  update, not only the one you changed. It is one-way: nothing undoes a copy
  or moves a Routine back to Popcorn's version.
concepts: [customizing-a-routine, versions, app-bundle]
layer: platform
---

A Routine made from a Routine Template runs Popcorn's version of it, the
**product line**, which every workspace can install. To change what the
Routine is built from, the workspace makes a copy of the template (the CLI
calls it a *fork line*): a series of versions the workspace owns, which it
publishes to. Which changes need a copy, and which stay with one Routine
without one, is in
[customizing a Routine](https://docs.popcorn.ai/product/concepts/customizing-a-routine.md).
This page is what a copy costs and how to make one.

## Making one

| To | Over MCP | With the CLI |
|---|---|---|
| copy the template a Routine runs | `copy_routine_template(routine_id, name)` | `popcorn app fork --channel <routine> --name <copy>`, or `popcorn app checkout --channel <routine> --fork=<copy>`, which copies and checks out in one step |
| move a Routine onto a copy the workspace already has | `install_routine(routine_id, copy=<name>)` | `popcorn app fork --channel <routine> --name <copy>` with the existing copy's name |
| see what a Routine runs | `get_routine`, whose **Updates from** says Popcorn or this workspace's own copy | `popcorn app list --channel <routine>` |
| list the workspace's copies | | `popcorn app lines` |

`copy_routine_template` is a dry run until it is called again with
`confirm=true`: the dry run names the version being copied, the new copy,
and any other copies of the template the workspace already has. It only
ever starts a new copy; joining an existing one is `install_routine` with
`copy`, which is a dry run too.

The copy starts byte-identical to the version the Routine runs, and the
Routine moves onto it, so nothing it runs changes at that moment. Copying
needs only membership of the Routine; publishing to the copy afterwards needs
a workspace admin (see
[versions](https://docs.popcorn.ai/platform/concepts/versions.md)).

A copy comes first. A publish lands on a copy the workspace owns, so a
publish based on Popcorn's version is refused. Over MCP, a Routine still on
Popcorn's version can dry-run a change with `create_routine_version`, which
is the way to check an edit before copying, since the copy is the step that
cannot be undone.

## A copy reaches every Routine on it

A workspace has one copy of a template unless it names more, and **every
Routine on a copy takes the copy's newest version**: the one you published
from at once, and each of the others on its own daily update, within a day.
The daily update runs as the workspace, not as the person who published, so
whether that person is a member of the other Routines does not matter. A
change tested on one Routine reaches the others on the copy.

To change one Routine without its siblings, it needs a second, named copy,
not a second Routine on the same one. A second copy can only be started from
a Routine still on Popcorn's version. Once a workspace has two copies of a
template, a copy or an install that does not name one is refused as
ambiguous.

## A copy is one-way

There is no undoing a copy. A Routine on a copy no longer receives the
template's improvements from Popcorn, and it cannot be moved back to
Popcorn's version or across to another copy: the only move there is, is from
Popcorn's version onto a copy. An earlier version of the copy can be read
back, but a Routine cannot be put back on it; the way back to old content is
to publish it forward as a new version.

A Routine can also join a copy without anyone meaning it to. Installing onto
a Routine still on Popcorn's version, in a workspace that owns exactly one
copy of its template, moves it onto that copy, which is how a mistyped
Routine turns one in use into an edited copy. Over MCP that install is a dry
run first, and says so.

So copying is a decision about the workspace, not a step in an edit. Check
the Routine's settings first, with `list_routine_settings` (in the CLI,
`popcorn channel-config params` and `popcorn table scalar`): a setting
reaches one Routine, can be set back, and survives the template's updates.
