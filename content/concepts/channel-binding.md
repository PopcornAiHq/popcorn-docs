---
id: channel-binding
title: How a channel runs a version
summary: >
  A channel points at exactly one bundle version. A run reads it once at start
  and is pinned for its whole life, including the flows it calls, so an upgrade
  mid-run never mixes versions; table data stays live. Base edits on the
  line's newest version (head): when a channel lags behind it, a publish based
  on the version the channel runs is refused.
concepts: [bundle-version, fork-line]
applies_to: [cli, mcp, human]
source: [bind_version_internal, get_flow_bytes_pinned]
---

A channel points at exactly one bundle version. The channel stores no copy of
the flows or the code: they are read from that version when they are needed.
The binding itself is a single write, but an upgrade is more than the bind —
the install reconciles tables, schedules and webhooks first, and binds last.

## Resolved through the binding, pinned for the run

When a flow starts, the platform reads the channel's bound version once and
records it for that run. Everything the run needs — the flow definition, any
code block it calls, the channel config — is then read from *that* version,
and nothing resolves through the channel again. A flow started with
`call_flow` inherits its parent's pin.

Three consequences worth holding on to:

- **A channel upgraded mid-run does not affect the run.** The old flow keeps
  pairing with the old code until it ends. A flow and the code it calls are
  published, versioned and upgraded together, and never mix.
- **A replay reads the same version.** The pin lives in the run's history, so
  re-executing an old run cannot silently pick up newer files.
- **Data is not pinned.** Table rows and channel state are read live. A run
  that outlives an upgrade sees rows the new version wrote.

## Bound is not always head

The version a channel runs is *bound*. The newest version on its line is
*head*. They differ while an install has not landed — and indefinitely when
an install failed, when the channel has app updates locked, or when it has no
update schedule. That window is exactly when reading the wrong one is most
expensive.

The server's reads default to bound, because that is what is live. `popcorn
app checkout` defaults to head, because a checkout is the base for a publish
and a publish must be based on head.
