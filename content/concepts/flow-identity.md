---
id: flow-identity
title: A flow's identity is its name
summary: >
  A flow is identified by the name inside the YAML, not by its filename.
  Install upserts by that name and prunes flows the bundle no longer declares,
  so renaming it reads as one delete plus one create.
concepts: [app-bundle]
applies_to: [cli, mcp, human]
source: [FLOW_NAME_RE, flow_index]
---

<!-- BODY TODO: rename semantics; why a stray .yaml becomes a flow and
     fixtures must be .json; the slug rule the name must satisfy. -->
