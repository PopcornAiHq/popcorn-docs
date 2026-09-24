---
id: app-bundle
title: App bundles
order: 1
summary: >
  An app bundle is a directory of YAML plus optional code that turns an empty
  channel into an application — tables, flows, schedules and webhooks. Every
  non-reserved YAML file at the bundle's root is a flow, so a sample payload
  left there installs as one; keep payloads outside the bundle. A manifest with
  a version is what makes it publishable.
concepts: [bundle-version, manifest-keys, flow-identity]
applies_to: [cli, mcp, human]
source: [ParsedTemplateConfig, bundle_file_tree, unrecognized_tree_paths]
---

An app bundle is a directory. Installing it into an empty channel gives that
channel tables to hold state, flows to do work, and schedules and webhooks to
start them.

```
myapp/
├── manifest.yaml      tables, scalars, schedules, webhooks, states, …
├── AGENT.md           notes the channel agent reads on demand
├── README.md          human documentation, installed as a channel file
├── strings.yaml       user-facing copy, locale-sectioned
├── some_flow.yaml     one flow per file, at the root
├── prompts/           seeded as channel config
├── templates/         seeded as channel config
├── code/<block>/      custom Python or Node the flows call
└── agents/<name>/     an app-scoped agent
```

A bundle needs a manifest carrying `version:` to be published. Everything
else is optional.

## Reserved names, and every other root YAML is a flow

`manifest.yaml`, `AGENT.md`, `README.md` and `strings.yaml` are read for what
they are. `config.yaml` is the legacy name for the manifest and is reserved
too — a flow saved under that name becomes the manifest instead.

**Every other `.yaml` or `.yml` file at the bundle's root is a flow.** A
scratch copy or a sample payload left at the root installs, quietly. A YAML
file in a subdirectory is never a flow.

`AGENT.md` is stored on the channel as the `agent_docs` scalar; the agent
reads it when it needs it rather than carrying it in every prompt. An explicit
`agent_docs` under `scalars:` wins over the file.

## The tree has a fixed shape

`prompts/` and `templates/` are descended one level and seeded into channel
config. `code/` holds one directory per block, each with exactly one
entrypoint — `main.py` or `index.js` — and is not seeded anywhere: a flow reads
a block by name at run time. `agents/<name>/` holds an app agent's definition;
the server accepts it, but the CLI does not upload it.

Anything outside that shape is not part of the bundle. The server refuses a
publish containing an unrecognised path; the CLI leaves such paths behind
before uploading and lists what it left. `template check` reports them as
`path-not-published`, which fails `--strict`.

So sample payloads live **outside** the bundle directory. A `fixtures/`
folder inside it is an unrecognised path whatever its files are called.
