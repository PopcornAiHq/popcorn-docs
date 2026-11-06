---
id: activities/catalog/foundation/contacts
title: foundation.contacts
order: 108
group: Activities
parent: activities/catalog/foundation
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.contacts activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.contacts` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.contacts.get`

Look up a workspace contact by id (e.g. a tracker cell's contact ref).

```yaml
- id: <step>
  activity: foundation.contacts.get
  args:
    contact_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `contact_id` | string | yes | Workspace contact id (from the contacts book). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `id` | string | The contact id (echoes the input). |
| `name` | string | Contact display name. |
| `phone` | string | Contact phone in E.164. |
| `email` | string, optional | Contact email, if set (else null). |
| `tags` | list of string | Free-form workspace labels. |
| `sms_status` | string | active / opted-out / unreachable. |

### `foundation.contacts.get_many`

Resolve many workspace contacts at once to `{sms_status, name, phone}`.

Ids that do not resolve are left out of the result rather than failing
the step. Read-only: safe to retry.

```yaml
- id: <step>
  activity: foundation.contacts.get_many
  args:
    contact_ids: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `contact_ids` | list of string | yes | Workspace contact ids (e.g. a tracker column). Empty strings are ignored; duplicates collapse. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `contacts` | map of ContactsGetManyRecord | contact_id -> record, for every id that resolved. An id missing here did not resolve (unknown, foreign, malformed). |
| `requested` | integer | Distinct non-empty ids asked for. |
| `found` | integer | len(contacts). |

`ContactsGetManyRecord`:

| Field | Type | Notes |
|---|---|---|
| `sms_status` | string | active / opted-out / unreachable, or '' when the contact has no status yet. |
| `name` | string | Contact display name ('' if unset). |
| `phone` | string | Contact phone in E.164 ('' if unset). |

### `foundation.contacts.upsert`

Create the workspace contact at `phone`, or return the existing one.

```yaml
- id: <step>
  activity: foundation.contacts.upsert
  args:
    name: <string>
    phone: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Display name for a NEW contact. |
| `phone` | string | yes | E.164 phone — the per-workspace unique key. A number already in the book resolves to that contact instead of erroring. |
| `email` | string | no | Optional email address. Default `""`. |
| `tags` | list of string | no | Optional tags. |
| `update_existing` | boolean | no | When the phone already exists: False (default) returns it untouched; True also applies name/email/tags to it. Never touches sms_status either way — that is the STOP/START handler's field. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `contact_id` | string | The contact's id. |
| `created` | boolean | True when this call created the contact. |
| `updated` | boolean | True when an existing contact was edited (update_existing). |
