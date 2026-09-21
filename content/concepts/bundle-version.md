---
id: bundle-version
title: Bundle versions
summary: >
  Publishing mints an immutable version — content-addressed, identified by
  (app, semver) — and nothing installs it until a channel binds to it.
  Publishing is not propagating.
concepts: [app-bundle, channel-binding, publish-and-apply]
applies_to: [cli, mcp, human]
source: [publish_tree, BundleImmutabilityError, bundle_digest]
---

Publishing does not change any channel. It mints an immutable, content-
addressed version and stops. Something must then bind a channel to it — that
is a separate operation, and the gap between the two is where most confusion
about "did my change go out" lives.

## The version is identified two ways

By `(app, semver)`, which you choose, and by a digest of the file tree, which
you do not. Both are enforced, and the three outcomes of a publish follow from
them:

| What you send | What happens |
|---|---|
| a new semver, new content | published |
| the same semver, byte-identical content | no-op, reported as such |
| the same semver, different content | refused — versions are immutable |

The version must also move forward. A reused or lower number is refused before
it reaches the registry.

## Immutable means immutable

A published version's files never change. This is what makes the run-time pin
meaningful: a flow that started against version *n* keeps reading version *n*'s
files for its whole life, including the code blocks it calls, even if the
channel upgrades underneath it.

It also means a mistake is corrected by publishing forward, never by editing.
There is no version-addressed read of an older tree, so a bundle you publish
and regret is not recoverable by reading it back — keep the working copy.
