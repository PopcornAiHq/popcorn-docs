---
id: fork-line
title: Fork lines
summary: >
  A fork line is a workspace's own version series of an app, forked from the
  shared product version. Publishing to it moves every channel on that line —
  the others converge on their daily update. A channel never changes line, so
  isolating a change means forking a second named line from a channel still on
  the product version. A fork cannot be undone.
concepts: [publish-and-apply, bundle-version, channel-binding]
applies_to: [cli, mcp, human]
source: [fork_for_channel, publish_fork_version, ChannelForkRegressionError, AmbiguousForkLineError]
---

An app ships as a **product version** that every workspace can install. To
change it for your workspace, you fork: the platform mints a version series
your workspace owns, starting from byte-identical content to what your channel
already runs, and binds the channel to it. From then on your channel follows
your line and product releases no longer reach it.

Forking is required before publishing. A publish lands on a line the workspace
owns, so a publish whose base is the shared product version is refused with
"fork first".

## A fork line is wider than the channel you edited

A workspace has one fork line per app unless it names more, and **every channel
on that line converges to the line's head** — each on its own daily update,
run as the workspace rather than as the person who published, so membership of
the channel is irrelevant. A change tested on one channel reaches the others
within a day.

The exceptions are channels that never take updates: archived, locked against
app updates, or with no update schedule. The publish reports how many other
channels will converge, and the CLI prints that count — after the fact.

Publishing is a *line* operation. The server anchors on the version your edits
were computed against: it must be the line's head, or have content identical to
it, which is how a retried publish succeeds. The one channel check is
consistency, not consent — a publish that names a channel running a different
line, or still on the product version, is refused whole and nothing publishes.
The CLI always names the channel it checked out from.

If you want a change that does not reach siblings, you need a second named
line, not a second channel. Once a workspace has two lines of an app, a fork
or apply that does not name a line is refused as ambiguous, and a second line
can only be started from a channel still on the product version.

## A fork is a one-way door

There is no unfork. A channel cannot be moved back to the product line or
across to another line, and no version-addressed read exists to recover the
tree a channel ran before — reads serve the bound version or the line's head,
never an arbitrary earlier one. Adoption also happens by accident: applying an
update to a product-bound channel in a workspace that owns exactly one fork
line of that app moves the channel onto the fork.

Treat forking as a decision about the workspace, not a step in an edit.

## Head versus bound

Two different versions, and each is right for one job:

- **bound** — what this channel is running right now. Right for reading what
  is live.
- **head** — the newest version on the line. The only publish base the server
  accepts: a publish whose base is not the head is refused, because a diff
  computed against an older version would drop whatever the versions in
  between changed. `popcorn app checkout` takes head unless told otherwise.

They differ while an install has not landed, and for good on a channel that
never takes updates. Reading bound in that window is right for what is live
and wrong as a base — the publish is refused, and the edit has to be redone
on a fresh checkout.
