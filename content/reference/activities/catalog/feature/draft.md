---
id: activities/catalog/feature/draft
title: feature.draft
order: 128
group: Activities
parent: activities/catalog/feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.draft activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.draft` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.draft.item_key`

*Beta.*

Derive the deterministic selection key from focused record ids.

```yaml
- id: <step>
  activity: feature.draft.item_key
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `record_ids` | list of any | no | The focused row ids (ints or numeric strings). Sorted and joined with '-' into a stable key; same ids in any order → same key. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string | The derived key (sorted ids joined by '-'); '' for none. |

### `feature.draft.read_file`

*Beta.*

Read a composed message-draft blob and parse it into draft fields.

`conversation_file_key` is a `file_uploads` key for this conversation
(e.g. the `draft_file_key` output of `compose_message_draft`). The file
is read scoped to the workflow's own conversation (`auth.conversation_id`),
so a flow can only read drafts from its own channel.

```yaml
- id: <step>
  activity: feature.draft.read_file
  args:
    conversation_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_file_key` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `to` | list of string | Recipients parsed from the draft's To: header. |
| `subject` | string | Subject parsed from the draft's Subject: header. |
| `body` | string | The draft's plain-text body. |
| `is_email_recipient` | boolean | True iff `to` is non-empty AND every recipient parses to an email address. False for an SMS draft (the To: is a phone number, e.g. the deliverycoordinator compose flow with medium=sms) or an empty To:. Gate the Gmail create step on this. Truthy exactly when `problem` is empty. |
| `problem` | string | User-facing reason this draft can't be saved to Gmail Drafts ('' when fine) — set when the recipient isn't an email address (an SMS draft) or there's no recipient at all. Truthy exactly when `is_email_recipient` is False. |

### `feature.draft.resolve_target`

Resolve everything needed to draft a message to the focused row(s).

Given the focused `record_ids`, fetches the rows authoritatively and
returns a deterministic `item_key` (so revisions thread), the rows, and
the resolved `recipient` for `medium` (email/sms). Exactly one of
`recipient` / `problem` is truthy — `problem` carries a user-facing
reason when there's no usable recipient. Routing is per-channel via the
scalar source/column or a per-medium `recipient_routes` map.

```yaml
- id: <step>
  activity: feature.draft.resolve_target
  args:
    conversation_id: <string>
    table_name: <string>
    record_ids: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `table_name` | string | yes |  |
| `record_ids` | list of any | yes |  |
| `medium` | string | no | Default `"email"`. |
| `recipient_source` | string | no | Default `"contact"`. |
| `recipient_column` | string | no | Default `"Receiver"`. |
| `recipient_routes` | map of RecipientRoute | no |  |
| `require_uniform_recipient` | boolean | no | Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `item_key` | string | Deterministic key for this selection (sorted ids joined). |
| `rows` | list of object | The focused rows' data. |
| `recipient` | string | Resolved To: address for the medium; '' when none. |
| `recipient_display` | string | Contact/sender display name, for the card. |
| `receiver_contact_id` | string | The contact id the recipient came from (contact source). |
| `problem` | string | User-facing reason there is no usable recipient ('' when fine). Truthy exactly when `recipient` is empty. |

`RecipientRoute`:

| Field | Type | Notes |
|---|---|---|
| `source` | string |  |
| `column` | string |  |
