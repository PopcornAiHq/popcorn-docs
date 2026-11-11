---
id: app-bundle
title: App Bundles
order: 5
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
---

A Routine Template is, underneath, an App Bundle: a directory. Installing it
into an empty [Routine](https://docs.popcorn.ai/routines.md) (the CLI and
the API call a Routine a *channel*) gives that Routine
[Tables](https://docs.popcorn.ai/tables.md) to hold state,
[Flows](https://docs.popcorn.ai/flow-grammar.md) to do work, and
[Schedules](https://docs.popcorn.ai/schedules.md) and Webhooks to start
them.

> "List the files in #team-offsite's template."

> [!TIP] MCP tool call
> Your assistant calls `list_routine_files`, then `read_routine_file` for
> any file you want to read.

The [Questionnaire](https://docs.popcorn.ai/questionnaire-template.md)
template that `#team-offsite` runs is this Bundle:

```
questionnaire/
├── manifest.yaml              Connection, Reference, Table, Schedule, states, …
├── AGENT.md                   what the Routine's Agent reads about it, on demand
├── README.md                  human documentation, installed as a file in the Routine
├── strings.yaml               setup checklist, setting labels, copy
├── questionnaire_tick.yaml    the Schedule's Flow: one pass
├── ask_recipient.yaml         a Flow per root YAML file
├── check_recipient.yaml
├── cta_apply.yaml
├── on_auth_change.yaml
├── questionnaire_load.yaml
├── reply_by_set.yaml
├── prompts/
│   ├── read_answers.md.j2         seeded as the setting prompts.read_answers
│   └── read_questionnaire.md.j2   seeded as prompts.read_questionnaire
└── code/questionnaire/        the code block that holds every rule
    ├── main.py
    └── tests/test_questionnaire.py
```

A Bundle can also hold a `templates/` directory, seeded as settings like
`prompts/`; a `recipe.yaml`, when the Manifest declares `recipe:`; and
`agents/<name>/` for an App Agent (`agent.yaml`, `prompt.md` and
`schemas/*.json`, nothing else). Questionnaire has none of these.

A Bundle needs a Manifest carrying `version:` to be published. Everything
else is optional.

## Reserved names, and every other root YAML is a Flow

`manifest.yaml`, `AGENT.md`, `README.md` and `strings.yaml` are read for what
they are. `config.yaml` is the legacy name for the Manifest and is reserved
too — a Flow saved under that name becomes the Manifest instead.

`recipe.yaml`, and its legacy name `process.yaml`, are reserved for the
[Recipe](https://docs.popcorn.ai/state-machine.md): a
State graph each Routine can replace. Publish requires one when the Manifest
declares `recipe:` (or `process:`), and refuses one when it does not, rather
than installing it as a Flow. A Bundle that ships both names is refused.

**Every other `.yaml` or `.yml` file at the Bundle's root is a Flow.**
That is all that makes Questionnaire's seven Flows Flows. A scratch copy or
a sample payload left at the root installs, quietly. A YAML
file in a subdirectory is never a Flow.

`AGENT.md` is stored on the Routine as the `agent_docs` Scalar; the
[Agent](https://docs.popcorn.ai/agent.md) reads it when it needs it rather than carrying it in every prompt. An explicit
`agent_docs` under `scalars:` wins over the file.

## The tree has a fixed shape

`prompts/` and `templates/` are descended one level and seeded as
[Routine Settings](https://docs.popcorn.ai/routine-settings.md), into the
platform's *channel config*, as `$channel.prompts.<stem>` and
`$channel.templates.<stem>`. The stem drops a known suffix, so
Questionnaire's `prompts/read_questionnaire.md.j2` is the setting
`prompts.read_questionnaire`, which `questionnaire_load` reads as
`$channel.prompts.read_questionnaire`. `code/` holds one
directory per block, each with exactly one entrypoint — `main.py` or
`index.js`, never both — and is not seeded anywhere: `foundation.code.execute`
reads a block by name at run time, as Questionnaire's pass and its
`reply_by_set` Flow do with `code_name: questionnaire`. A block is descended to any depth, so it may be
a small package, or carry its tests as Questionnaire's does. Block files must be UTF-8 text, may carry any
extension (a `.yaml` there is block source, not a Flow), and a block has a
file-count and a size cap, which the refusal names.

The block name is a slug, because it rides inside Flow YAML as `code_name:`,
and every segment below it must be visible: the server refuses a Publish
with a hidden entry there.

`agents/<name>/` holds an App Agent's definition (see
[platform tools](https://docs.popcorn.ai/platform-tools.md)): `agent.yaml` and
`prompt.md` directly inside it, and JSON schemas under `schemas/`. It
publishes like the rest of the Bundle. Any other
file under `agents/` is not part of the Bundle, and the server parses each
agent at Publish and refuses one it could not run.

Anything outside that shape is not part of the Bundle, and the server
refuses a Publish containing an unrecognised path.

> [!WARNING] Keep sample payloads outside the Bundle
> A sample reply saved as `questionnaire/reply.yaml` installs as a Flow, and
> a `fixtures/` folder inside the Bundle is an unrecognised path whatever
> its files are called. Keep them outside the Bundle.

## With the CLI

The CLI works on the Bundle as files on disk, and its offline checks have
no MCP equivalent today.

`popcorn app checkout --channel team-offsite` writes the Bundle's files to
disk; a Checkout includes the served agent files, and `app publish` sends
what you add, edit or delete there. Keep sample payloads beside the
Checkout, not in it.

The CLI filters a Bundle before upload. `app publish` drops dotfiles under
`code/`, so from the CLI a hidden file is silently left behind rather than
refused. It leaves an unrecognised path behind and lists what it left; only
dotfiles and `__pycache__` are dropped without comment.

`app validate` reports `code-file-outside-block` for a loose file directly
under `code/`, `code-block-name-invalid` for a block name that is not a
slug, and `path-not-published` for a path outside the Bundle's shape, which
fails `--strict`.
