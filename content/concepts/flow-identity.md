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

A flow is identified by the `name:` inside the YAML. The filename is not part
of its identity and can be anything.

```yaml
name: nudge_stale_rows     # this is the identity
version: 1
steps: [...]
```

## Install upserts by name, and prunes

Install matches the flows in the bundle against the flows on the channel **by
name**, updates the ones that match, adds the ones that are new, and removes
the ones the bundle no longer declares.

So changing `name:` is not a rename. It is a delete plus a create: the old flow
disappears, a new one arrives, and anything addressing the old name — a
schedule, a webhook, another flow that starts it — is now pointing at nothing.
Rename the references in the same change, or don't rename.

The name must be a slug: lowercase letters, digits and underscores. The same
rule is enforced at publish, at install, and when a schedule id is built from
it, so a name that violates it fails early rather than halfway through.

## Any stray `.yaml` becomes a flow

The tree reader treats every non-reserved YAML file as a flow, wherever it sits.
A sample payload, a scratch file, a copy you kept "just in case" — all of them
install. This is the reason fixtures are `.json`, and it is worth a glance at
the tree before publishing.
