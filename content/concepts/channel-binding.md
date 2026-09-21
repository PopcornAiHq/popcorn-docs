---
id: channel-binding
title: How a channel runs a version
summary: >
  A channel points at exactly one bundle version, and that single reference is
  the whole binding — flows and code are resolved through it at run start and
  pinned for the run, so an upgrade mid-run never mixes versions.
concepts: [bundle-version, fork-line]
applies_to: [cli, mcp, human]
source: [bind_version_internal, get_flow_bytes_pinned]
---

<!-- BODY TODO: the binding is a reference, never a copy; the run-start pin
     and why replays stay consistent; upgrading is one write. -->
