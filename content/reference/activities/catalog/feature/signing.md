---
id: activities/catalog/feature/signing
title: feature.signing
order: 139
group: Activities
parent: activities/catalog/feature
layout: lookup
generated: scripts/sync-activities.py
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.signing activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `feature.signing` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.signing.adopt_document`

Record a document id explicitly confirmed by an operator.

```yaml
- id: <step>
  activity: feature.signing.adopt_document
  args:
    conversation_id: <string>
    document_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `document_id` | string | yes | Provider document id confirmed by the operator. |
| `fingerprint` | string | no | The unconfirmed send's fingerprint, if known. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `document_id` | string |  |

### `feature.signing.check_configured`

Probe the channel's e-signature credentials and send mode.

```yaml
- id: <step>
  activity: feature.signing.check_configured
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `send_mode_scalar` | string | no | The channel scalar the send mode is read from — the same one the bundle's send_for_signature will name. Default `"popcorn.email_send_mode"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `configured` | boolean | True when the channel holds a usable e-signature account (an API key, and an https host for it). |
| `host` | string | The API host the key would be sent to (never the key). |
| `send_mode` | string | The channel's send mode from send_mode_scalar: off / draft / send. |
| `can_send` | boolean | configured and send_mode is 'send' — a real send would go out. |

### `feature.signing.execute_send`

Run feature.signing.send_document and report its outcome as a value.

```yaml
- id: <step>
  activity: feature.signing.execute_send
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_key` | string | yes |  |
| `document_name` | string | no | Default `""`. |
| `signers` | list of object | no |  |
| `fields` | list of object | no | Signature boxes to place explicitly, as the merge measured them for a [[signer N]] template. Empty for a {{...}} template, whose tags the provider reads out of the PDF. |
| `subject` | string | no | Default `""`. |
| `message` | string | no | Default `""`. |
| `correlation` | map of string | no |  |
| `max_attempts` | integer | no | The step's total attempts (on_error.retry + 1). On the last one a retryable failure is returned as unconfirmed rather than raised, so the flow can park the row. Default `4`. |
| `send_mode_scalar` | string | no | The channel scalar the send's consent is read from; handed to feature.signing.send_document unchanged. Default `"popcorn.email_send_mode"`. |
| `return_signing_links` | boolean | no | Handed to feature.signing.send_document unchanged: each output signer then carries its signing_link. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string | sent / draft / not_sent / unconfirmed |
| `document_id` | string |  |
| `status` | string |  |
| `provider_status` | string |  |
| `send_mode` | string |  |
| `delivered` | boolean |  |
| `document_verified` | boolean |  |
| `fields_detected` | integer, optional |  |
| `fingerprint` | string | The send fingerprint (the request's external_id at the provider); 'unknown' when it could not be computed. |
| `signers` | list of object |  |
| `error_type` | string |  |
| `error_summary` | string | For not_sent / unconfirmed: the failure, one line. |

### `feature.signing.fetch_signed_document`

Store the completed document as a permanent agent-store file.

```yaml
- id: <step>
  activity: feature.signing.fetch_signed_document
  args:
    conversation_id: <string>
    document_id: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (the durable copy lands in this conversation's agent store). |
| `document_id` | string | yes | Provider document id, from $steps.<send step>.output.document_id. |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'signed/retainer'. The extension is derived from the downloaded content type and any existing '<stem>.*' file is replaced. |
| `document_name` | string | no | Which file to store when the request produced several and the provider does not combine them. Leave empty when there is one; a SigningMultipleDocuments error lists the available names. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Final agent-store file key, e.g. 'signed/retainer.pdf'. |
| `size_bytes` | integer |  |
| `sha256` | string | Digest of the stored bytes, for later verification. |
| `content_type` | string |  |
| `document_id` | string |  |
| `provider` | string |  |
| `provider_status` | string | The provider's own status spelling. |

### `feature.signing.get_status`

Read a signature request's current state.

```yaml
- id: <step>
  activity: feature.signing.get_status
  args:
    document_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `document_id` | string | yes | Provider document id, from $steps.<send step>.output.document_id. |
| `return_signing_links` | boolean | no | Return each signer's signing_link. Off by default: the link is a bearer URL, so ask for it only when the flow is about to hand it to that signer. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `document_id` | string |  |
| `provider` | string |  |
| `status` | string | Normalized document status: created / sent / viewed / partial / completed / declined / expired / failed. 'partial' means at least one signer is done and the document is NOT final. |
| `provider_status` | string | The provider's own status spelling. |
| `completed` | boolean | True only when the document is fully signed. |
| `signers` | list of SigningStatusSigner |  |

`SigningStatusSigner`:

| Field | Type | Notes |
|---|---|---|
| `signer_id` | string |  |
| `role` | string | Role filled. |
| `email` | string |  |
| `status` | string | Normalized signer status: created / sent / viewed / completed / declined / failed. |
| `signed_at` | string | RFC3339 time this signer completed; '' if not yet. |
| `signing_link` | string | Where this signer signs. Empty unless the input set return_signing_links. |

### `feature.signing.inspect_send`

Inspect the recorded outcome of a signature send in this conversation.

```yaml
- id: <step>
  activity: feature.signing.inspect_send
  args:
    conversation_id: <string>
    fingerprint: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `fingerprint` | string | yes | Send fingerprint from execute_send; empty or 'unknown' leaves the outcome unresolved. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `resolved` | `sent` / `not_sent` / `` | Empty means the ledger cannot prove an outcome. |
| `document_id` | string |  |
| `fingerprint` | string |  |
