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

<!-- BODY TODO: the two are different operations people conflate; publish's
     guards are all about validity, none about intent; apply converges a
     channel to its OWN lineage head and cannot reach across channels. -->
