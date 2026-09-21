---
id: app-bundle
title: App bundles
summary: >
  An app bundle is a directory of YAML plus optional Python that turns an empty
  channel into an application — tables for state, flows for work, schedules and
  webhooks to start them. The manifest is the only file meaningful on its own.
concepts: [bundle-version, manifest-keys, flow-identity]
applies_to: [cli, mcp, human]
source: [ParsedTemplateConfig, bundle_file_tree]
---

An app bundle is a directory. Installing it into an empty channel gives that
channel tables to hold state, flows to do work, and schedules and webhooks to
start them.

```
myapp/
├── manifest.yaml      tables, scalars, schedules, webhooks, connections
├── AGENT.md           notes injected into the channel agent's prompt
├── README.md          human documentation, installed as nothing
├── strings.yaml       user-facing copy, locale-sectioned
├── some_flow.yaml     one flow per file
├── prompts/           seeded as channel config
├── code/<block>/      custom Python or Node the flows call
└── fixtures/*.json    sample payloads — NOT installed
```

Only the manifest is meaningful on its own. A bundle with one flow and no
manifest is legal.

## Four reserved names, and everything else is a flow

`manifest.yaml`, `AGENT.md`, `README.md` and `strings.yaml` are read for what
they are. **Every other `.yaml` or `.yml` file in the tree is installed as a
flow** — which is why sample payloads must be `.json`. A fixture named `.yaml`
becomes a flow, quietly.

`prompts/` and `templates/` are descended one level and seeded into channel
config. `code/` is descended to any depth, one directory per block, and its
files are *not* seeded anywhere — a flow reads a block by name at run time.
Everything else, including dotfiles, is skipped without comment.

## Keep it flat

Two readers exist for a bundle tree and they disagree about nesting: one
ignores a flow in a subdirectory, the other flattens it to its basename. Both
do it silently. Keep flows at the top level and the disagreement never arises;
the offline checker flags the nesting if you forget.
