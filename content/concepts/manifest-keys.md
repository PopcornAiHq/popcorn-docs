---
id: manifest-keys
title: Manifest keys and what install does to them
summary: >
  Each manifest key has its own install semantics, and an absent key is not the
  same as an empty one — omitting schedules leaves them alone, while declaring
  an empty list deletes every one. Scalars upsert on every install; runtime
  state must never be declared there.
concepts: [scalar-tiers, merge-policy, app-bundle]
applies_to: [cli, mcp, human]
source: [ParsedTemplateConfig, ChannelTemplateInstaller]
---

<!-- BODY TODO: the per-key table (additive reconcile / upsert / replace /
     create-if-missing / write-once); the declared-vs-absent rule; that an
     untyped bundle clears the channel's app type. -->
