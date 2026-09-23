---
id: flow-identity
title: A flow's identity is its name
summary: >
  A flow is identified by the name inside the YAML, not by its filename. A
  channel resolves flows by name from the version it runs, so changing
  `name:` is a delete plus a create — and a schedule still naming the old
  flow is dropped at install, with no error.
concepts: [app-bundle, manifest-keys]
applies_to: [cli, mcp, human]
source: [FLOW_NAME_RE, build_flow_index]
---

A flow is identified by the `name:` inside the YAML. The filename is not part
of its identity — any root-level `.yaml` or `.yml` name that is not reserved
will do. If `name:` is missing the filename stem stands in, which is why
`template check` treats a missing name as an error.

```yaml
name: nudge_stale_rows     # this is the identity
version: 1
steps: [...]
```

Two files resolving to the same name make the bundle unpublishable.

## Flows resolve by name from the bound version

A channel stores no copy of its flows. Each published version carries an index
of its flows by name, and the channel runs whatever the version it is bound to
declares. A flow the new version no longer declares simply stops existing for
that channel.

So changing `name:` is not a rename. It is a delete plus a create, and what
happens to the things that addressed the old name depends on what they are:

| Reference | After the old name disappears |
|---|---|
| a schedule in the manifest | skipped at install, then deleted as undeclared — a log line, no error |
| a webhook that already exists | never updated, so it keeps pointing at the old name |
| a trigger, document or state transition | the publish fails |

Rename the references in the same change, or don't rename. `template check`
reports `schedule-unknown-flow` and `webhook-unknown-flow` before you publish.

## The name is a slug

Lowercase letters, digits, hyphens and underscores; it starts with a letter
or digit, and it is at most 63 characters. Publish enforces it, and so does
building a schedule's id.
