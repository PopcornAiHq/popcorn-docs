---
id: copying-a-template
title: Copying a template
order: 3
group: Making a change
summary: >
  Customizing a Routine beyond its Routine Settings gives it a Copy that the
  Workspace owns (`popcorn app fork`). A change published to the Copy
  reaches every Routine on it by their Daily Update, not only the one you
  changed. It is one-way: nothing undoes a Copy or
  moves a Routine back to Popcorn's version.
lede: >
  A Copy of a template is your Workspace's own. A change to it reaches every
  Routine on it, and a Copy can't be undone.
concepts: [customizing-a-routine, versions, app-bundle]
---

A Routine made from a Routine Template runs Popcorn's own version of it,
which every Workspace can install. To change what the Routine is built
from, the Workspace makes a Copy of the template (the CLI calls it a
*fork line*): a series of [Versions](https://docs.popcorn.ai/versions.md)
the Workspace owns, which it publishes to.

This guide gives `#team-offsite`, the
[Questionnaire](https://docs.popcorn.ai/questionnaire-template.md)
[Routine](https://docs.popcorn.ai/routines.md) from
[Set up your first Routine](https://docs.popcorn.ai/set-up-a-routine.md),
a Copy of its template named `offsite`, so that a later Version can add a
`Team` Column to its `recipients` Table. Each step starts with a prompt you
might give your assistant.

## Check its settings first

> "Can I change how #team-offsite follows up without copying its
> template?"

> [!TIP] MCP tool call
> Your assistant calls `list_routine_settings`.

Your assistant lists the Routine's
[Routine Settings](https://docs.popcorn.ai/routine-settings.md). On
Questionnaire they include `follow_up_days`, `max_follow_ups`,
`popcorn.email_send_mode`, and the two prompts that read the questionnaire
and the replies, `prompts.read_questionnaire` and `prompts.read_answers`.
The questions themselves are the questionnaire
[Reference](https://docs.popcorn.ai/reference-documents.md). A change any
of these covers needs no Copy: a setting reaches one Routine, can be set
back, and survives the template's updates. In the CLI, `popcorn
channel-config params` and `popcorn table scalar` read the same values.

A new Column is not a setting, so it needs a Copy. Which changes do, and
which stay with one Routine without one, is in
[customizing a Routine](https://docs.popcorn.ai/customizing-a-routine.md).

## Try the change before copying

> "Show me what adding a Team column to #team-offsite's recipients would
> change. Don't make it yet."

> [!TIP] MCP tool call
> Your assistant calls `list_routine_files` and `read_routine_file` for
> `manifest.yaml`, then `create_routine_version` without `confirm`.

On a Routine still on Popcorn's version, `create_routine_version` is a dry
run only: it shows each file's diff and every check the change would fail,
and says the Routine needs its own Copy before the change can be made.
That is the way to check an edit before copying, since the Copy is the
step that can't be undone.

## Make the Copy

> "Give #team-offsite its own copy of the Questionnaire template, called
> offsite."

> [!TIP] MCP tool call
> Your assistant calls `get_routine` for the Routine's ID, then
> `copy_routine_template` without `confirm`, and again with `confirm=true`
> once you agree.

The dry run names the Version being copied (Questionnaire 0.2.1), the new
Copy, and any other Copies of the template the Workspace already has. A
Copy's name is lowercase letters, digits, `-` and `_`.

With the CLI, copy and check out the Copy's files in one step:

```bash
popcorn app checkout --channel team-offsite --fork=offsite
```

`popcorn app fork --channel team-offsite --name offsite` copies without
checking out.

The Copy starts byte-identical to the Version the Routine runs, and the
Routine moves onto it, so nothing it runs changes at that moment. Copying
needs a Routine Role of `member` or above, or a Workspace admin, so a guest
of the Routine is refused, and so is a Copy of an archived Routine.
Publishing to the Copy afterwards needs a Workspace admin: see
[Versions](https://docs.popcorn.ai/versions.md), which takes the `Team`
Column from here.

> [!CAUTION] A Copy is one-way
> Once `#team-offsite` is on `offsite`, it no longer receives Popcorn's
> improvements to Questionnaire, and nothing moves it back.

## See what it runs

> "What does #team-offsite run now?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine`.

Its **Updates from** line now names this Workspace's Copy `offsite`
instead of Popcorn. `list_routines` says the same for every Routine
(`· Popcorn's` or `· copy "offsite"`), and `list_routines` with `template`
and `copy` lists the Routines on the Copy that you can see. In the CLI,
`popcorn app list --channel team-offsite` says what one Routine runs, and
`popcorn app lines` lists the Workspace's Copies.

## Moving another Routine onto the Copy

> "Put #board-offsite on the offsite copy too."

> [!TIP] MCP tool call
> Your assistant calls `install_routine` with `copy`, as a dry run first,
> then with `confirm=true`.

`copy_routine_template` only ever starts a new Copy. Joining one the
Workspace already has is an Install that names it, which is a dry run too.
With the CLI it is `popcorn app fork` with the existing Copy's name.

## A Copy reaches every Routine on it

A Workspace has one Copy of a template unless it names more, and **every
Routine on a Copy is brought to the Copy's newest Version**: the one you
published from by an Install that starts at once, and each of the others by
its own Daily Update, within a day. The Daily Update runs as the Workspace,
not as the person who published, so whether that person is a Member of the
other Routines does not matter. A `Team` Column tested on `#team-offsite`
reaches `#board-offsite` too. The exceptions are in
[installing](https://docs.popcorn.ai/versions.md#installing): the Install
on the Routine you published from can be blocked, and the Daily Update
skips some Routines. `create_routine_version`'s dry run counts the other
Routines a new Version will update.

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

> [!WARNING] Joining a Copy by accident
> Installing onto a Routine still on Popcorn's version, in a Workspace that
> owns exactly one Copy of its template, moves it onto that Copy. That is
> how a mistyped Routine turns one in use into an edited Copy. Over MCP
> that Install is a dry run first, and says so.

So copying is a decision about the Workspace, not a step in an edit.
