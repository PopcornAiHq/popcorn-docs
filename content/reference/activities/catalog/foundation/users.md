---
id: activities/catalog/foundation/users
title: foundation.users
order: 124
group: Activities
parent: activities/catalog/foundation
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-11-25
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.users activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.users` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.users.find`

*Beta.*

Find workspace members by name or username and return their ids.

Matches `query` case-insensitively against each member's username and
display name, as a prefix or anywhere inside: "shaun", "Shaun Smith" and
"smith" all find Shaun Smith. Best match first: exact username, exact
display name, a name that starts with the query, a later word that
does, then the rest. Active members of the flow's own workspace only.
Each entry has the same fields `foundation.users.get` returns: no
email, no avatar. No match is an empty list. Read-only: safe to retry.

```yaml
- id: <step>
  activity: foundation.users.find
  args:
    query: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `query` | string | yes | The name or handle to look up, e.g. 'Shaun' or '@shaun'. A leading '@' is ignored. Must not be blank. |
| `limit` | integer | no | Most members to return (1-50). Default `10`. |
| `include_bots` | boolean | no | Also match agent and bot accounts. Off by default, so a name resolves to a person. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `users` | list of UserIdentity | Matching members, best match first; empty when none match. Every entry has found=true. |
| `count` | integer | How many entries `users` holds. |

`UserIdentity`:

| Field | Type | Notes |
|---|---|---|
| `user_id` | string | The requested id (echoed). |
| `found` | boolean | False when the id is unknown, in another workspace, or not a UUID. The other fields are then null. |
| `display_name` | string, optional | The user's chosen name; null if unset (fall back to `username`). |
| `username` | string, optional | Login handle. |
| `is_bot` | boolean, optional | True for agent / bot accounts. |
| `timezone` | string, optional | The IANA timezone the user chose, e.g. 'America/New_York'. Null when they left it on 'auto' (the device's clock decides, so the server knows no zone) or it is unknown: fall back, e.g. to the workspace's or UTC. |
| `role` | string, optional | Workspace role: owner, admin, member, guest or workspace_agent. Null when unknown. A guest is an outside collaborator; leave them out of anything about members. |

### `foundation.users.get`

Look up workspace users by id and return their display identity.

Give exactly one of `user_id` or `user_ids`. Ids that do not resolve
come back with `found: false` rather than failing the step. Returns
names, the bot flag, the user's chosen timezone and workspace role
(either null when unknown): no email, no avatar. Read-only: safe to
retry.

```yaml
- id: <step>
  activity: foundation.users.get
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `user_id` | string, optional | no | One workspace user id, e.g. $trigger.user_id. The result is in `user` (and as the single entry of `users`). |
| `user_ids` | list of string, optional | no | Up to 100 workspace user ids, e.g. a `display: user` column. Empty strings are ignored; duplicates collapse. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `user` | UserIdentity, optional | The `user_id` form's entry (found or not); null in the `user_ids` form. |
| `users` | list of UserIdentity | One entry per distinct requested id, in request order, including the ones that did not resolve. |
| `requested` | integer | Distinct non-empty ids asked for. |
| `found` | integer | How many entries have found=true. |

`UserIdentity`:

| Field | Type | Notes |
|---|---|---|
| `user_id` | string | The requested id (echoed). |
| `found` | boolean | False when the id is unknown, in another workspace, or not a UUID. The other fields are then null. |
| `display_name` | string, optional | The user's chosen name; null if unset (fall back to `username`). |
| `username` | string, optional | Login handle. |
| `is_bot` | boolean, optional | True for agent / bot accounts. |
| `timezone` | string, optional | The IANA timezone the user chose, e.g. 'America/New_York'. Null when they left it on 'auto' (the device's clock decides, so the server knows no zone) or it is unknown: fall back, e.g. to the workspace's or UTC. |
| `role` | string, optional | Workspace role: owner, admin, member, guest or workspace_agent. Null when unknown. A guest is an outside collaborator; leave them out of anything about members. |

### `foundation.users.link_account`

*Beta.*

Record an account a flow learned for a workspace member.

Sets `value` as the member's learned (auto) account on `provider`,
with `evidence` saying how it was learned. Never replaces a value the
member set themselves and never re-links one they removed; `outcome`
says what happened. GitHub only. Safe to retry.

```yaml
- id: <step>
  activity: foundation.users.link_account
  args:
    member_id: <string>
    value: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `member_id` | string | yes | The member's user id, e.g. a `member_id` from `foundation.users.find` or the scan's own people table. |
| `provider` | string | no | The service. Only 'github' today. Default `"github"`. |
| `value` | string | yes | The member's login on the service, e.g. 'octocat' (an '@' or a github.com profile URL is accepted). |
| `evidence` | string, optional | no | How it was learned, shown to the member after 'Learned from': name the app, then the evidence, e.g. 'GitHub scan: 3 PRs announced by your agent'. One line, at most 200 characters. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | `linked` / `unchanged` / `kept_self` / `removed` | 'linked': now the member's learned value. 'unchanged': it already was, with this evidence. 'kept_self': the member set their own value, which stays. 'removed': the member or an admin removed this value, so it is not linked again. |
| `account` | LinkedAccount, optional | The member's account on the provider after the call, whoever set it; null when they have none. |
| `removed` | list of string | Values removed for this provider, which no flow may link again. |

`LinkedAccount`:

| Field | Type | Notes |
|---|---|---|
| `value` | string |  |
| `source` | string | 'self' (the member's) or 'auto'. |
| `evidence` | string, optional |  |
| `updated_at` | string |  |
