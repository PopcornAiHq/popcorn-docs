---
id: fork-line
title: Fork lines
summary: >
  A fork line is a workspace's own version series of an app, forked from the
  shared product version. Publishing to it moves every channel on that line,
  not only the one you edited — siblings catch up on their own daily tick.
concepts: [publish-and-apply, bundle-version, channel-binding]
applies_to: [cli, mcp, human]
source: [fork_for_channel, publish_fork_version, ChannelForkRegressionError]
---

An app ships as a **product version** that every workspace can install. To
change it for your workspace, you fork: the platform mints a version series
your workspace owns, starting from byte-identical content to what your channel
already runs, and binds the channel to it. From then on your channel follows
your line and product releases no longer reach it.

Forking is required before publishing. A publish lands on a line the workspace
owns, so publishing from a channel still bound to the shared product version
is refused.

## A fork line is wider than the channel you edited

This is the part that surprises people, and the tooling has historically
understated it.

A workspace has one fork line per app by default, and **every channel on that
line converges to the line's head** — each on its own daily update tick,
whether or not the person who published is a member of that channel. So a
change tested on one channel reaches all of them within a day.

Publishing is a *line* operation, not a channel one. The server anchors on the
version your edits were computed against and checks nothing about what any
particular channel runs. A channel that cannot take the new version yet is
reported separately from whether the publish succeeded — the version publishes
either way.

If you want a change that does not reach siblings, you need a second named
line, not a second channel.

## A fork is a one-way door

There is no unfork. A channel cannot be moved back to the product line, and
no version-addressed read exists to recover the tree a channel ran before —
reads serve the bound version or the line's head, never an arbitrary earlier
one. Adoption also happens by accident: applying an update to a
product-bound channel in a workspace that owns exactly one fork line of that
app moves the channel onto the fork.

Treat forking as a decision about the workspace, not a step in an edit.

## Head versus bound

Two different versions, and using the wrong one is silent:

- **bound** — what this channel is running right now. Right for reading what
  is live.
- **head** — the newest version on the line. Right as a publish base, because
  a diff computed against an older version would silently overwrite whatever
  the versions in between changed.

They differ only while an install has not landed. That window is exactly when
getting it wrong costs the most.
