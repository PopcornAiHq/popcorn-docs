---
id: mcp/tools/run-code-block
title: run_code_block
order: 349
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  Run one code block of a Routine's template on Popcorn's code runner, with
  inputs you give, and return what its run(inputs) returns, without publishing
  anything.
concepts: [template-authoring]
used_with: [mcp/tools/list-routine-files, mcp/tools/create-routine-version, mcp/tools/read-doc]
---

[writes]

```
run_code_block(routine_id, block=None, inputs=None, changes=None, base_version=None, tests=False, timeout_seconds="DEFAULT_TIMEOUT_SECONDS", run=None)
```

What runs: the block at code/<block>/ (main.py or index.js) of the version edits are based on, the one [`list_routine_files`](https://docs.popcorn.ai/mcp/tools/list-routine-files.md) lists, with your changes applied for this run only. It runs on the same runner, in the same sandbox, as a Flow step that calls it with code.execute, so its output is what that step's output would be. With `tests=true` it runs the block's tests/ under pytest instead (Python blocks only), and inputs is their `step_inputs` fixture.

What it can't touch: nothing is published, installed or written. The block can't read or write the Routine's tables, gets no workspace secrets (a step's `env`) and posts no message; give it as inputs what a step's `reads` would. It can reach the public internet, as a published block can. Workspace admins only; one run at a time per Routine.

Next: change the block and run it again until its output is right, then publish the same changes with [`create_routine_version`](https://docs.popcorn.ai/mcp/tools/create-routine-version.md) and have a Flow call the block with code.execute. [`read_doc`](https://docs.popcorn.ai/mcp/tools/read-doc.md) with `activities` covers code.execute's reads, writes and env.

A run waits up to 20 seconds. One still going answers with a run id: call again with `routine_id` and run alone to keep waiting.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `block` | `str` | The block's name, the directory under code/ ("rules" for code/rules/). |
| `inputs` | `dict[str, Any]` | The dict run(inputs) is called with (at most 256 KiB as JSON). |
| `changes` | `list[dict[str, Any]]` | Unpublished changes to the block's files, in `create_routine_version`'s format: each to a path under code/<block>/, with the sha256 it was read at for a file that exists. ops, create, delete and rename only. |
| `base_version` | `int \| str` | The version to read the block from, as `list_routine_files`' header shows it. Omit for the version edits are based on. |
| `tests` | `bool` | true to run the block's tests/ instead of run(). Default `False`. |
| `timeout_seconds` | `int` | Seconds the runner gives run() (and, separately, installing requirements.txt), at most 120. Default `DEFAULT_TIMEOUT_SECONDS`. |
| `run` | `str` | A run id an earlier call answered with, to wait for that run. Goes alone with `routine_id`. |

**Example** — “Before I publish, check that #supplier-survey's questionnaire block reads "14 November" as a reply-by date.”

```text
→ run_code_block(routine_id="3d6a…28", block="questionnaire", inputs={"operation": "reply_by", "value": "14 November", "now": "2026-11-10T09:00:00+00:00"})

Routine: #supplier-survey (3d6a…28)
Ran code/questionnaire from version 0.2.3, on the code runner.
code/questionnaire ran. run(inputs) returned:
```json
{
  "ok": true,
  "date": "2026-11-14",
  "shown": "14 November 2026"
}
```
Nothing was published or written. To try an edit, call again with changes; to publish the block as it ran, pass create_routine_version the changes it ran with.
```
