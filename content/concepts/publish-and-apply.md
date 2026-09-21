---
id: publish-and-apply
title: Publish and apply
summary: >
  Publish mints the next version on a fork line; apply brings one channel up to
  its line's head. Publish is ungated and reaches every channel on the line;
  apply takes no version and is the durable retry when an install was blocked.
concepts: [fork-line, bundle-version]
applies_to: [cli, mcp, human]
source: [publish_fork_version, apply_app]
---

Two operations people conflate, doing different jobs.

**Publish** mints the next version on a line. It is a line operation: it checks
the base your edits were computed against and nothing about what any channel is
running.

**Apply** brings one channel up to its own line's head. It takes no version
from you — there is no parameter through which one channel's content reaches
another — and reports that there was nothing to do if the channel is already
current.

## Publish's guards are all about validity

A publish is checked for: workspace-admin rights, a non-empty change, a base
that still matches the line's head, a tree that parses and validates as a
bundle, and a manifest version that advances.

Every one of those asks *is this well-formed*. None of them asks **did you mean
to do this to everyone** — and a publish reaches every channel on the line. If
you want the answer to that question, you have to ask it yourself.

## Apply is the durable retry

An install can be blocked — another install may be in progress, or the channel
may be locked. That is reported separately from whether the publish succeeded,
because the version publishes either way.

Apply is how you finish the job afterwards. It works from server state alone,
so it survives the conversation or session that published ending, which is the
case a re-run of the publish cannot cover.

One sharp edge: applying to a channel still on the shared product version, in a
workspace that owns exactly one fork line of that app, moves that channel onto
the fork. That is adoption working as designed, and it is also how a mistyped
channel converts a production channel to an edited fork.
