---
id: app-bundle
title: App Bundles
order: 4
group: What a Bundle holds
summary: >
  A Routine Template is an App Bundle: a directory of YAML plus optional code
  that gives an empty Routine its Tables, Flows, Schedules and Webhooks.
  Every non-reserved YAML file at the Bundle's root is a Flow, so a sample
  payload left there installs as one; keep payloads outside the Bundle.
  A Manifest with a Version is what makes it publishable.
lede: >
  A Routine Template is an App Bundle: a directory of YAML, plus optional
  code, that gives a Routine its Tables, Flows, Schedules and Webhooks.
concepts: [versions, manifest-keys, flow-grammar]
part: build
---

A Routine Template is, underneath, an App Bundle: a directory. Installing it
into an empty Routine (the CLI and the API call a Routine a *channel*) gives
that Routine Tables to hold state, Flows to do work, and Schedules and
Webhooks to start them.

```
myapp/
├── manifest.yaml      tables, scalars, schedules, webhooks, states, …
├── AGENT.md           notes the channel agent reads on demand
├── README.md          human documentation, installed as a file in the Routine
├── strings.yaml       user-facing copy, locale-sectioned
├── recipe.yaml        the state graph, when the manifest declares recipe:
├── some_flow.yaml     one flow per file, at the root
├── prompts/           seeded as Routine Settings
├── templates/         seeded as Routine Settings
├── code/<block>/      custom Python or Node the flows call
└── agents/<name>/     an app agent: agent.yaml, prompt.md, schemas/*.json — nothing else
```

A Bundle needs a Manifest carrying `version:` to be published. Everything
else is optional.

## Reserved names, and every other root YAML is a Flow

`manifest.yaml`, `AGENT.md`, `README.md` and `strings.yaml` are read for what
they are. `config.yaml` is the legacy name for the Manifest and is reserved
too — a Flow saved under that name becomes the Manifest instead.

`recipe.yaml`, and its legacy name `process.yaml`, are reserved for the
[Recipe](https://docs.popcorn.ai/build/concepts/state-machine.md): a
State graph each Routine can replace. Publish requires one when the Manifest
declares `recipe:` (or `process:`), and refuses one when it does not, rather
than installing it as a Flow. A Bundle that ships both names is refused.

**Every other `.yaml` or `.yml` file at the Bundle's root is a Flow.** A
scratch copy or a sample payload left at the root installs, quietly. A YAML
file in a subdirectory is never a Flow.

`AGENT.md` is stored on the Routine as the `agent_docs` Scalar; the Agent
reads it when it needs it rather than carrying it in every prompt. An explicit
`agent_docs` under `scalars:` wins over the file.

## The tree has a fixed shape

`prompts/` and `templates/` are descended one level and seeded as
Routine Settings, into the platform's *channel config*, as
`$channel.prompts.<stem>` and `$channel.templates.<stem>`. `code/` holds one
directory per block, each with exactly one entrypoint — `main.py` or
`index.js`, never both — and is not seeded anywhere: `foundation.code.execute`
reads a block by name at run time. A block is descended to any depth, so it
may be a small package. Block files must be UTF-8 text, may carry any
extension (a `.yaml` there is block source, not a Flow), and a block has a
file-count and a size cap, which the refusal names.

The block name is a slug, because it rides inside Flow YAML as `code_name:`,
and every segment below it must be visible: the server refuses a hidden entry
there, while `app publish` drops dotfiles under `code/` before upload, so from
the CLI a hidden file is silently left behind. `app validate` reports
`code-file-outside-block` for a loose file directly under `code/` and
`code-block-name-invalid` for a name that is not a slug.

`agents/<name>/` holds an App Agent's definition: `agent.yaml` and
`prompt.md` directly inside it, and JSON schemas under `schemas/`. It
publishes like the rest of the Bundle — a Checkout writes the served agent
files, and `app publish` sends what you add, edit or delete there. Any other
file under `agents/` is not part of the Bundle, and the server parses each
agent at Publish and refuses one it could not run.

Anything outside that shape is not part of the Bundle. The server refuses a
Publish containing an unrecognised path; the CLI leaves such paths behind
before uploading and lists what it left. `app validate` reports them as
`path-not-published`, which fails `--strict`. Only dotfiles and `__pycache__`
are dropped without comment.

So sample payloads live **outside** the Bundle directory. A `fixtures/`
folder inside it is an unrecognised path whatever its files are called.
