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

<!-- BODY TODO: immutability and the three-branch publish contract (new /
     identical digest / same semver different digest); why the version must
     advance; that a published version is inert until bound. -->
