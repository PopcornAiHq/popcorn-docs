---
id: publish-and-apply
title: Publish and apply
order: 10
summary: >
  Publish mints the next version on a fork line and reaches every channel on
  it; its guards check permission and validity, never whether you meant to
  reach everyone, and a manifest missing `app_type` is not refused — it clears
  the app on every channel. Apply brings one channel up to its line's head,
  takes no version, and is the durable retry when an install was blocked.
concepts: [fork-line, bundle-version]
applies_to: [cli, mcp, human]
source: [publish_fork_version, apply_app]
---

Two operations people conflate, doing different jobs.

**Publish** mints the next version on a line and starts an install on the
channel it names. It is a line operation: every other channel on the line
converges to the new head on its own.

**Apply** brings one channel up to its own line's head. It takes no version
from you — there is no parameter through which one channel's content reaches
another — and reports `already_current` if there is nothing to do.

Publishing needs workspace-admin rights. Forking and applying need only
membership of the channel.

## Publish's guards are all about validity

A publish is refused when:

- the caller is not a workspace admin
- the request carries no file changes and no deletions
- the base is not a fork line the workspace can see, or is no longer its head
- the named channel runs a different line, or the product version
- the tree has a path outside the bundle shape, two files under `prompts/` or
  `templates/` that would install under the same key (`prompts/x.md` and
  `prompts/x.txt`), or a root YAML file whose top level is not a mapping
- a flow does not parse strictly — a misspelled key, a `call_flow` naming its
  own flow or one the bundle does not have, or a `foreach` asking for more
  `max_parallel` than the platform allows
- the manifest has no `version:`, a version that does not advance, or a
  different `app_type` from its line
- a flow name is not a slug, or a flow declares its own `trigger:`
- the version or its content already exists (see `bundle-version`)

A manifest with **no** `app_type:` is not refused: publish treats it as the
line's own app. Every install of that version then clears `app_type` and
`channel_agent` on each channel it reaches — every channel on the line. Keep
both keys in every version, and treat `template check`'s `clears-app-type`
warning as an error when publishing to a fork.

Every one of those asks *is this allowed and well-formed*. None of them asks
**did you mean to do this to everyone** — and a publish reaches every channel
on the line. The response says how many other channels will converge, after
the version exists. If you want the answer before, you have to ask it
yourself.

## Apply is the durable retry

An install can be blocked — another install may be in progress, or the channel
may be locked against app updates. That is reported separately from whether
the publish succeeded, because the version publishes either way. An install
reported as started has not necessarily landed either: it re-checks when it
runs, and can still skip. `popcorn app status` shows what the channel actually
runs.

Apply is how you finish the job afterwards. It works from server state alone,
so it survives the conversation or session that published ending, which is the
case a re-run of the publish cannot cover. On a locked channel it is refused
rather than queued.

Apply follows fork lines only. On a channel still on the product version in a
workspace with no fork line of the app, it reports `already_current` — product
channels take releases through their daily update, not through apply.

One sharp edge: applying to a channel still on the shared product version, in a
workspace that owns exactly one fork line of that app, moves that channel onto
the fork. That is adoption working as designed, and it is also how a mistyped
channel converts a production channel to an edited fork. With two or more
lines it is refused as ambiguous.
