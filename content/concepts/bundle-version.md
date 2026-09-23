---
id: bundle-version
title: Bundle versions
summary: >
  Publishing mints an immutable, content-addressed version on a line —
  identified by its semver there — and installing it is a separate step that
  can be blocked. The same semver with different content is refused, and so
  is a new semver whose content matches an earlier version exactly.
concepts: [app-bundle, channel-binding, publish-and-apply]
applies_to: [cli, mcp, human]
source: [publish_tree, BundleImmutabilityError, BundleDigestCollisionError, bundle_digest]
---

A version is minted by a publish and never changes afterwards. Installing it
onto a channel is a separate operation: the CLI starts one for the channel you
published from, and other channels on the line follow on their own schedule
(see `fork-line`). An install can be blocked or can skip, and then the version
exists while no channel runs it. The gap between the two is where most
confusion about "did my change go out" lives.

## The version is identified two ways

By its **semver on its line**, which you choose, and by a **digest** of the
file tree, which you do not. A line is the shared product series, or one
workspace's named fork of it, so two lines can each hold a `1.0.1`. Both
identities are enforced, and a publish has four outcomes:

| What you send | What happens |
|---|---|
| a new semver, new content | published |
| the same semver, byte-identical content | no-op, reported as such |
| the same semver, different content | refused — versions are immutable |
| a new semver, content identical to an earlier version on the line | refused — the digest is taken |

A new semver must also be higher than the line's newest. The CLI checks that
before sending; the registry enforces it regardless.

## Immutable means immutable

A published version's files never change. This is what makes the run-time pin
meaningful: a flow that started against version *n* keeps reading version *n*'s
files for its whole life, including the code blocks it calls, even if the
channel upgrades underneath it.

It also means a mistake is corrected by publishing forward, never by editing.
Two consequences follow:

- **You cannot restore an old tree byte for byte.** Its digest is already
  taken. Bump the version and change something — the manifest's `changelog:`
  saying why is the honest change — and the digest differs.
- **You cannot read an old tree back.** There is no version-addressed read, so
  a bundle you publish and regret is not recoverable from the server — keep
  the working copy.
