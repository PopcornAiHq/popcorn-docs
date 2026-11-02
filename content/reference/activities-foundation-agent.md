---
id: activities-foundation-agent
title: foundation.agent
order: 104
group: Activities
parent: activities-foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.agent activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.agent` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.agent.invoke`

No description in the catalog.

```yaml
- id: <step>
  activity: foundation.agent.invoke
  args:
    agent_name: <string>
    data: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `agent_name` | string | yes |  |
| `data` | object | yes |  |
| `timeout_seconds` | integer | no | Default `180`. |
| `channel_notes` | string | no | Default `""`. |
| `bundle_guidance` | string or list of string | no | Default `""`. |
| `stage_guidance` | string | no | Default `""`. |
| `process_guidance` | string | no | Default `""`. |
| `model` | string | no | Default `""`. |
| `reply` | `json` / `text` | no | Default `"json"`. |
| `act_as` | `agent` / `member` | no | `agent` (default): the workspace agent. `member`: a person, for an agent whose tools are Popcorn's MCP server. That is the person the run was started for ($trigger.user_id): who pressed Run, or the member whose message the channel agent was answering when it started the run. A call_flow child carries its parent's. A run started for nobody (a schedule, a webhook) is refused (ActAsRefused), except in a call_flow child, which acts as the channel's first admin member (NoChannelAdmin if there is none). That person's own role decides what the tools may do. Default `"agent"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | object |  |
| `model` | string |  |
| `model_source` | string |  |
| `model_requested` | string |  |
| `acted_as_user_id` | string |  |

### `foundation.agent.transform`

Transform arbitrary data with an LLM and return the parsed JSON result.

Sends `prompt` plus `data` to Claude and returns the model's JSON
output as `$steps.<id>.output`. When `output_schema` is set the result
is validated against it and a violation fails the step non-retryably.
Provider defaults to Anthropic; a `us.anthropic.*` model id (or
`CLAUDE_PROVIDER=bedrock`) routes to Bedrock.

The prompt may be supplied inline (`prompt`) or sourced from an
agent-store file (`prompt_file_key`) — exactly one is required; the file
key wins if both are set.

Two prompt styles:
  * Plain (default) — the prompt is instructions; `data` is sent as a
    separate JSON block. The (stable) instructions are sent as their own
    content block and automatically prompt-cached when they clear the
    model's minimum cacheable size, with the volatile `data` after.
  * Jinja — when `prompt_format` is `"jinja"` or the file key ends in
    `.j2`/`.jinja`, the prompt is a Jinja2 template rendered against
    `data` to produce the whole message (no separate JSON block). The
    rendered text is volatile, so it is not cached.

```yaml
- id: <step>
  activity: foundation.agent.transform
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string, optional | no |  |
| `prompt_file_key` | string, optional | no |  |
| `prompt_format` | string, optional | no |  |
| `data` | any | no |  |
| `model` | string | no | Default `"claude-sonnet-4-6"`. |
| `output_schema` | object, optional | no |  |
| `max_tokens` | integer | no | Default `4096`. |
