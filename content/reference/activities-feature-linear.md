---
id: activities-feature-linear
title: feature.linear
order: 134
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.linear activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.linear` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.linear.check_configured`

*Beta.*

Is a Linear API key set for this workspace, and whose is it?

Reads the LINEAR_API_KEY workspace secret (Settings → Secrets) the way
every feature.linear step does and answers configured / key_status
plus the account and organization the key acts as. No key, or a key
Linear rejects, is configured: false — a value, not an error.

```yaml
- id: <step>
  activity: feature.linear.check_configured
```

Takes no arguments of its own.

**Returns**

| Field | Type | Notes |
|---|---|---|
| `configured` | boolean | True when a key is set and Linear accepted it. |
| `key_status` | string | none (no LINEAR_API_KEY set) / valid / rejected (revoked, expired or never valid). |
| `viewer_name` | string | The person the key acts as. Issues it creates name them as creator. |
| `viewer_email` | string |  |
| `organization` | string | The Linear workspace's name. |
| `organization_url_key` | string | The slug in linear.app/<url_key>/… links. |
| `rate_limit_remaining` | integer | Requests left this hour; -1 if Linear did not say. The budget is per Linear user, shared by all their keys. |
| `rate_limit_resets_at` | string |  |

### `feature.linear.comment`

*Beta.*

Comment on a Linear issue — exactly once per step.

Markdown body, posted as the key's owner. A Temporal retry returns the
comment already posted (created: false); pass idempotency_key to make
that hold across runs. A missing issue is LinearNotFound. Needs
LINEAR_API_KEY (Settings → Secrets).

```yaml
- id: <step>
  activity: feature.linear.comment
  args:
    issue: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `issue` | string | yes | Issue id, identifier (<TEAM>-<number>) or linear.app issue URL. |
| `body` | string | yes | Markdown. |
| `idempotency_key` | string | no | Names this comment across runs: a later step with the same key returns the comment already posted (created: false). Retries of one step are covered without it. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `comment` | LinearComment |  |
| `issue_identifier` | string | The team key and number, <TEAM>-<number>. |
| `created` | boolean | False when the comment already existed under this step's id (a retry, or a reused idempotency_key). |

`LinearComment`:

| Field | Type | Notes |
|---|---|---|
| `id` | string |  |
| `author` | string | The commenter's name, or the integration's. |
| `author_email` | string |  |
| `body` | string | Markdown, capped at 4000 chars. |
| `body_truncated` | boolean |  |
| `created_at` | string |  |
| `url` | string |  |

### `feature.linear.create_issue`

*Beta.*

File a Linear issue — exactly once per step.

Names (team, state, assignee, project, labels) resolve to ids before
anything is written; a miss is LinearNotFound, a tie LinearAmbiguous.
A Temporal retry returns the issue already filed (created: false);
pass idempotency_key to make that hold across runs. Needs
LINEAR_API_KEY (Settings → Secrets); the issue is filed as its owner.

```yaml
- id: <step>
  activity: feature.linear.create_issue
  args:
    team: <string>
    title: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `team` | string | yes | Team key (ENG), name, or id. |
| `title` | string | yes |  |
| `description` | string | no | Markdown. Default `""`. |
| `assignee` | string | no | 'me' (the key's owner), an email, a name, or a user id. Default `""`. |
| `project` | string | no | Project name or id. Default `""`. |
| `labels` | list of string | no | Label names (workspace or team labels) or ids. |
| `priority` | string or integer, optional | no | urgent / high / medium / low / none, or 0–4 (1 urgent … 4 low). Unset leaves Linear's default. |
| `state` | string | no | Workflow state name or type word ('todo', 'started'). Unset is the team's default state. Default `""`. |
| `idempotency_key` | string | no | Names this issue across runs: a later step with the same key returns the issue already filed (created: false) instead of filing another. Retries of one step are covered without it. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `issue` | LinearIssue |  |
| `created` | boolean | False when the issue already existed under this step's id (a retry, or a reused idempotency_key). |

`LinearIssue`:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Linear's UUID for the issue. |
| `identifier` | string | Team key and number: <TEAM>-<number>. |
| `title` | string |  |
| `url` | string |  |
| `state` | string | Workflow state name. |
| `state_type` | string | backlog / unstarted / started / completed / canceled / triage. Stable across teams, unlike state names. |
| `assignee` | string | Assignee's name; '' if none. |
| `assignee_email` | string |  |
| `team` | string | Team key, e.g. ENG. |
| `team_name` | string |  |
| `project` | string | Project name; '' if none. |
| `priority` | integer | 0 none, 1 urgent, 2 high, 3 medium, 4 low. |
| `priority_label` | string |  |
| `labels` | list of string |  |
| `created_at` | string |  |
| `updated_at` | string |  |

### `feature.linear.get_issue`

*Beta.*

Read one Linear issue with its description and recent comments.

`issue` is an id, an identifier (<TEAM>-<number>) or a linear.app issue URL.
A missing issue is found: false. Description and comments are capped;
*_truncated flags say when. Needs LINEAR_API_KEY (Settings → Secrets).

```yaml
- id: <step>
  activity: feature.linear.get_issue
  args:
    issue: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `issue` | string | yes | Issue id, identifier (<TEAM>-<number>) or linear.app issue URL. |
| `comments_limit` | integer | no | Most recent comments to include; 0 for none. Default `10`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `found` | boolean | False when the issue does not exist or the key cannot see it. |
| `issue` | LinearIssueDetail, optional |  |

`LinearComment`:

| Field | Type | Notes |
|---|---|---|
| `id` | string |  |
| `author` | string | The commenter's name, or the integration's. |
| `author_email` | string |  |
| `body` | string | Markdown, capped at 4000 chars. |
| `body_truncated` | boolean |  |
| `created_at` | string |  |
| `url` | string |  |

`LinearIssueDetail`:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Linear's UUID for the issue. |
| `identifier` | string | Team key and number: <TEAM>-<number>. |
| `title` | string |  |
| `url` | string |  |
| `state` | string | Workflow state name. |
| `state_type` | string | backlog / unstarted / started / completed / canceled / triage. Stable across teams, unlike state names. |
| `assignee` | string | Assignee's name; '' if none. |
| `assignee_email` | string |  |
| `team` | string | Team key, e.g. ENG. |
| `team_name` | string |  |
| `project` | string | Project name; '' if none. |
| `priority` | integer | 0 none, 1 urgent, 2 high, 3 medium, 4 low. |
| `priority_label` | string |  |
| `labels` | list of string |  |
| `created_at` | string |  |
| `updated_at` | string |  |
| `description` | string | Markdown, capped at 20000 chars. |
| `description_truncated` | boolean |  |
| `comments` | list of LinearComment | Most recent first. |
| `comments_truncated` | boolean | True when the issue has more comments than returned. |

### `feature.linear.search_issues`

*Beta.*

Find Linear issues by text and/or filters.

Compact records (identifier, title, state, assignee, team, project,
priority, url, updated_at). Team, project and assignee names resolve
exactly — a miss is LinearNotFound, a tie LinearAmbiguous. No matches
is issues: []. Needs LINEAR_API_KEY (Settings → Secrets).

```yaml
- id: <step>
  activity: feature.linear.search_issues
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `query` | string | no | Full-text search over titles and descriptions. Empty lists issues by the filters alone, most recently updated first. Default `""`. |
| `team` | string | no | Team key (ENG), name, or id. Default `""`. |
| `project` | string | no | Project name or id. Default `""`. |
| `state` | string | no | Workflow state name ('In Review') or type word ('todo', 'started', 'done', 'canceled'); a type word matches every state of that type. With `team`, a word naming none of the team's states is an error. Default `""`. |
| `assignee` | string | no | 'me' (the key's owner), 'none' for unassigned, an email, a name, or a user id. Default `""`. |
| `labels` | list of string | no | Label names; an issue must carry every one. |
| `limit` | integer | no | Default `20`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `issues` | list of LinearIssue |  |
| `count` | integer |  |
| `truncated` | boolean | True when more issues matched than `limit`. |

`LinearIssue`:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Linear's UUID for the issue. |
| `identifier` | string | Team key and number: <TEAM>-<number>. |
| `title` | string |  |
| `url` | string |  |
| `state` | string | Workflow state name. |
| `state_type` | string | backlog / unstarted / started / completed / canceled / triage. Stable across teams, unlike state names. |
| `assignee` | string | Assignee's name; '' if none. |
| `assignee_email` | string |  |
| `team` | string | Team key, e.g. ENG. |
| `team_name` | string |  |
| `project` | string | Project name; '' if none. |
| `priority` | integer | 0 none, 1 urgent, 2 high, 3 medium, 4 low. |
| `priority_label` | string |  |
| `labels` | list of string |  |
| `created_at` | string |  |
| `updated_at` | string |  |

### `feature.linear.update_issue`

*Beta.*

Change fields of a Linear issue.

Only fields set change; an empty string leaves a field alone.
Clearing is explicit (unassign, remove_from_project, labels: []).
Names resolve against the issue's own team. Retry-safe. A missing
issue is LinearNotFound. Needs LINEAR_API_KEY (Settings → Secrets).

```yaml
- id: <step>
  activity: feature.linear.update_issue
  args:
    issue: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `issue` | string | yes | Issue id, identifier (<TEAM>-<number>) or linear.app issue URL. |
| `title` | string | no | Default `""`. |
| `description` | string | no | Markdown; replaces the description. Default `""`. |
| `state` | string | no | Workflow state name or type word ('started', 'done') in the issue's team. Default `""`. |
| `assignee` | string | no | 'me' (the key's owner), an email, a name, or a user id. Default `""`. |
| `unassign` | boolean | no | Clear the assignee. Default `false`. |
| `priority` | string or integer, optional | no | urgent / high / medium / low / none, or 0–4. |
| `project` | string | no | Project name or id. Default `""`. |
| `remove_from_project` | boolean | no | Default `false`. |
| `labels` | list of string, optional | no | Replaces the issue's labels; [] clears them. Omit to leave them alone. |
| `add_labels` | list of string | no |  |
| `remove_labels` | list of string | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `issue` | LinearIssue |  |
| `changed` | list of string | The fields this step set, e.g. ['state', 'assignee']. Empty when the step set nothing. |

`LinearIssue`:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Linear's UUID for the issue. |
| `identifier` | string | Team key and number: <TEAM>-<number>. |
| `title` | string |  |
| `url` | string |  |
| `state` | string | Workflow state name. |
| `state_type` | string | backlog / unstarted / started / completed / canceled / triage. Stable across teams, unlike state names. |
| `assignee` | string | Assignee's name; '' if none. |
| `assignee_email` | string |  |
| `team` | string | Team key, e.g. ENG. |
| `team_name` | string |  |
| `project` | string | Project name; '' if none. |
| `priority` | integer | 0 none, 1 urgent, 2 high, 3 medium, 4 low. |
| `priority_label` | string |  |
| `labels` | list of string |  |
| `created_at` | string |  |
| `updated_at` | string |  |
