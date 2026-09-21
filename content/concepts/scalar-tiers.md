---
id: scalar-tiers
title: The three scalar tiers
summary: >
  Declared scalars upsert on every install, default scalars write once on first
  install only, and platform scalars are reserved and belong in neither. Put a
  value a flow writes at runtime in the first tier and every reinstall resets
  it.
concepts: [manifest-keys]
applies_to: [cli, mcp, human]
source: [PLATFORM_SETTINGS, candidate_settings]
---

<!-- BODY TODO: the three tiers and which is safe for an operator switch; the
     reserved platform namespace and why it is never declared in a manifest;
     how an app promotes a setting into the client's panel. -->
