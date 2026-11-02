---
id: activities-feature-esign-document
title: feature.esign.document
order: 130
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.esign.document activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `feature.esign.document` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.esign.document.claim_send`

Take the row for this run's send and freeze what will be sent: the
merged file, the signers, the fields.

```yaml
- id: <step>
  activity: feature.esign.document.claim_send
  args:
    now: <string>
    run_id: <string>
    refuse_when: <array>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `send_intent_column` | string | no | Where a claim freezes its send intent. Default `"Send Intent"`. |
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `run_id` | string | yes | This run's identity, normally $trigger.run_id: the claim holder and the intent's owner. |
| `project_states` | boolean | no | Compose the pinned graph's projection into the patch. Default `true`. |
| `recompute_on_stale` | integer | no | Re-reads and recomputations after the row moved under the patch, before failing CodeRevisionConflict. Default `3`. |
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose envelope ended unsigned (Signing Status declined/expired/voided) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `signers` | list of any, optional | no | Override for the row's Signers, [{role, email, name?}]; null uses the row's, [] is refused. |
| `connection` | object, optional | no | feature.esign.check_configured's answer: a channel that is not connected is refused SigningNotConfigured in the connection's own reason and action, one whose sending is off SigningSendModeOff. Null: the flow vouches for it. |
| `link_column` | string | no | The row column holding the address whose signer gets `delivery: link` (the bundle emails them the link itself); every other signer gets the provider's email. Blank: the provider emails everyone. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `document_status` | string | The document machine's state. |
| `document_why` | string |  |
| `changed` | boolean |  |
| `applied` | object | {count, patched, stale, projected, worklist}. |
| `skipped` | boolean | The row no longer named what the step expected. |
| `claimed` | boolean |  |
| `sending` | string |  |
| `file_key` | string |  |
| `document_name` | string |  |
| `signers` | list of EsignSigner | The frozen signers, as feature.esign.send takes them. |
| `fields` | list of EsignField | The frozen boxes, as feature.esign.send takes them. |

`EsignField`:

| Field | Type | Notes |
|---|---|---|
| `name` | string |  |
| `role` | string | Which signer fills it; a signers[].role. |
| `type` | string | signature / initials / date_signed / date / text / checkbox ('datenow' is accepted for date_signed). date_signed is stamped by the provider when that signer finishes and never carries a value. |
| `required` | boolean |  |
| `page` | integer | 1-based page number. |
| `area` | EsignFieldArea |  |
| `value` | string | A starting value the signer can still edit (text, date, checkbox). Values you want fixed belong merged into the PDF. |

`EsignFieldArea`:

| Field | Type | Notes |
|---|---|---|
| `x` | number | Left edge, 0.0–1.0 of page width. |
| `y` | number | Top edge, 0.0–1.0 of page height. |
| `w` | number | Width, 0.0–1.0 of page width. |
| `h` | number | Height, 0.0–1.0 of page height. |

`EsignSigner`:

| Field | Type | Notes |
|---|---|---|
| `role` | string | The slot this person fills, e.g. 'Client'. |
| `email` | string | Where the request (or our email) goes. |
| `name` | string | Full name. Required by some providers (capabilities.signer_name_required). |
| `order` | integer | Signing order, 1-based. Equal numbers sign in parallel where the provider supports groups. |
| `delivery` | string | provider_email (the provider emails them) / link (the flow hands them the link, e.g. in its own email) / embedded. |

`StoreClaimCondition`:

| Field | Type | Notes |
|---|---|---|
| `column` | string |  |
| `test` | `set` / `unset` / `equals` / `not_equals` / `in` / `not_in` |  |
| `value` | string or list of string, optional |  |

`StoreClaimRefusal`:

| Field | Type | Notes |
|---|---|---|
| `code` | string | Error type the run fails with. |
| `message` | string | What the refusal tells the caller. |
| `when` | list of StoreClaimCondition |  |

### `feature.esign.document.derive`

Publish facts onto the row — a provider answer, a release, a merge —
only while the row still names what the step expects.

```yaml
- id: <step>
  activity: feature.esign.document.derive
  args:
    now: <string>
    run_id: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `send_intent_column` | string | no | Where a claim freezes its send intent. Default `"Send Intent"`. |
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `run_id` | string | yes | This run's identity, normally $trigger.run_id: the claim holder and the intent's owner. |
| `project_states` | boolean | no | Compose the pinned graph's projection into the patch. Default `true`. |
| `recompute_on_stale` | integer | no | Re-reads and recomputations after the row moved under the patch, before failing CodeRevisionConflict. Default `3`. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `facts` | object | no |  |
| `change_kind` | string, optional | no |  |
| `change_action` | string, optional | no |  |
| `merged_values` | object, optional | no |  |
| `expect_envelope_id` | string, optional | no |  |
| `progress` | list of any, optional | no | feature.esign.status's `signers`: each role's status lands in `Signer Progress` (no address, no link), and a partly signed envelope's Why names who has signed. |
| `expect_sending` | string, optional | no |  |
| `expect_regenerating` | string, optional | no |  |
| `stamp_facts` | list of string | no | Facts written only alongside a change (`Checked At`): when every other fact already holds its value, the derive publishes nothing and the row is not written. |
| `retire_previous` | boolean | no | On document_merged, queue the row's previous Merged and Preview Keys for deletion (documents/<record_id>/ only). Default `false`. |
| `retire_file_keys` | list of any, optional | no | Keys to queue instead (documents/<record_id>/ only). |
| `cleanup_table` | string, optional | no | The queue retired files go to, upserted on file_key. |
| `derived_columns` | list of string | no | The projection's columns: a fact naming one is refused. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `document_status` | string | The document machine's state. |
| `document_why` | string |  |
| `changed` | boolean |  |
| `applied` | object | {count, patched, stale, projected, worklist}. |
| `skipped` | boolean | The row no longer named what the step expected. |
| `send_now` | boolean | A client's pending Send Requested is due: launch the send. |
| `merge_again` | boolean | The fields moved during the merge: rebuild once more. |

### `feature.esign.document.envelope`

The row's open envelope, for a member's reminder or cancel. Writes
nothing.

```yaml
- id: <step>
  activity: feature.esign.document.envelope
  args:
    table_name: <string>
    record_id: <integer>
    action: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `action` | `remind` / `void` | yes | What the member asked for: remind the signers who have not signed, or void (cancel) the request. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `envelope_id` | string |  |
| `provider` | string |  |
| `signing_status` | string |  |
| `document_status` | string |  |

### `feature.esign.document.filing_due`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.esign.document.filing_due
  args:
    signings_table: <string>
    now: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<Envelope Id>`): where each round's filing state lives. |
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `cap` | integer | no | Default `10`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `blocked` | string | The channel cause rounds wait on, or ''. |
| `rounds` | list of object | [{signing_key, record_id, envelope_id}] to file now. |

### `feature.esign.document.filing_mark`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.esign.document.filing_mark
  args:
    signings_table: <string>
    table_name: <string>
    record_id: <integer>
    envelope_id: <string>
    now: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `issues_table` | string | no | The worklist the filing items go to, keyed by `cause` (`drive_filing:<cause>`, `drive_filing:round:<signing_key>`). Default `"issues"`. |
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<Envelope Id>`): where each round's filing state lives. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `document_of_column` | string | no | The seed's `{stage, prepared_at}` stamp: the stage the row's current document is for. Default `"Document Of"`. |
| `envelope_id` | string | yes | The request whose signing just completed. |
| `now` | string | yes | The run's fixed clock, ISO 8601. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `marked` | boolean |  |
| `reason` | string |  |
| `filing` | string | pending / off / failed |
| `signing_key` | string |  |
| `launch` | boolean | File it now: start the filing flow. |

### `feature.esign.document.filing_plan`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.esign.document.filing_plan
  args:
    signings_table: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<Envelope Id>`): where each round's filing state lives. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `document_of_column` | string | no | The seed's `{stage, prepared_at}` stamp: the stage the row's current document is for. Default `"Document Of"`. |
| `envelope_id` | string | no | The round to file; blank is the row's latest signed one. Default `""`. |
| `auto` | boolean | no | A launch the flows made (the completion, the tick): files only a round stamped pending or a failure the tick retries. False is a person filing a round by hand, whatever its stamp. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file` | boolean |  |
| `reason` | string | Why not: off, not_signed, already_filed, not_pending, needs_attention. |
| `signing_key` | string |  |
| `envelope_id` | string |  |
| `record_id` | integer, optional |  |
| `stage` | string |  |
| `name` | string |  |
| `signed_key` | string |  |
| `signed_at` | string |  |
| `client_key` | string |  |
| `upload_tag` | string |  |

### `feature.esign.document.filing_record`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.esign.document.filing_record
  args:
    signings_table: <string>
    table_name: <string>
    record_id: <integer>
    outcome: <string>
    envelope_id: <string>
    now: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `issues_table` | string | no | The worklist the filing items go to, keyed by `cause` (`drive_filing:<cause>`, `drive_filing:round:<signing_key>`). Default `"issues"`. |
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<Envelope Id>`): where each round's filing state lives. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `document_of_column` | string | no | The seed's `{stage, prepared_at}` stamp: the stage the row's current document is for. Default `"Document Of"`. |
| `outcome` | `attempt` / `result` | yes |  |
| `envelope_id` | string | yes |  |
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `template_envelope` | any, optional | no | The stage's signing template envelope (its `filename` names the document); null when it could not be read. |
| `vocabulary` | object, optional | no | The process's nouns ({document, recipient}). |
| `timezone` | string, optional | no | The channel's zone, for the signed date. Default `""`. |
| `filed` | boolean, optional | no |  |
| `cause` | string, optional | no | Default `""`. |
| `reason` | string, optional | no | Default `""`. |
| `file_id` | string, optional | no | Default `""`. |
| `web_view_link` | string, optional | no | Default `""`. |
| `file_name` | string, optional | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `attempted` | boolean |  |
| `file_name` | string |  |
| `folder_fallback` | string |  |
| `recorded` | boolean |  |
| `filing` | string |  |
| `cause` | string |  |
| `reason` | string |  |
| `fail_run` | boolean | The run should end failed: a defect of this file, or a failure nobody could name. |
| `issues_written` | integer |  |

### `feature.esign.document.inspect_reconcile`

Check an uncertain send may be reconciled, and name its fingerprint
and the document an operator says they found. Writes nothing.

```yaml
- id: <step>
  activity: feature.esign.document.inspect_reconcile
  args:
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `resolution` | string | no | Default `""`. |
| `envelope_id` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `fingerprint` | string |  |
| `sending` | string |  |
| `status` | string |  |
| `document_status` | string |  |
| `envelope_id` | string |  |
| `owned_envelope_id` | string | The envelope an operator confirmed, to adopt first. |
| `provider` | string | The provider the parked send was for. |

### `feature.esign.document.poll`

Read the row's signature request and stamp the attempt before any
provider I/O, so an uncertain request cannot monopolize the capped
oldest-first sweep.

```yaml
- id: <step>
  activity: feature.esign.document.poll
  args:
    now: <string>
    run_id: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `run_id` | string | yes | This run's identity, normally $trigger.run_id: the claim holder and the intent's owner. |
| `project_states` | boolean | no | Compose the pinned graph's projection into the patch. Default `true`. |
| `recompute_on_stale` | integer | no | Re-reads and recomputations after the row moved under the patch, before failing CodeRevisionConflict. Default `3`. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `stamp` | boolean | no | Stamp `Checked At` (a row write with its own audit entry) before the provider is asked. False for a bundle that schedules no sweep on it: the poll then only reads, and refuses as before. Default `true`. |
| `reason` | `tick` / `event` / `manual` | no | Who is asking, as feature.esign.status names it: a `tick` read is due only once the last read's `next_read_after` (`Next Check At`) has passed. Default `"manual"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `document_status` | string | The document machine's state. |
| `document_why` | string |  |
| `changed` | boolean |  |
| `applied` | object | {count, patched, stale, projected, worklist}. |
| `skipped` | boolean | The row no longer named what the step expected. |
| `data` | object | The row as read. |
| `envelope_id` | string |  |
| `sending` | string |  |
| `fingerprint` | string |  |
| `read_due` | boolean | The envelope is worth reading now: not over, and for a tick, past `next_check_at`. |
| `next_check_at` | string |  |

### `feature.esign.document.prefill`

Write a preparer's admitted values onto the fields still empty, each
only while its evidence still says what the preparer read.

```yaml
- id: <step>
  activity: feature.esign.document.prefill
  args:
    now: <string>
    run_id: <string>
    refuse_when: <array>
    table_name: <string>
    record_id: <integer>
    evidence: ...
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `run_id` | string | yes | This run's identity, normally $trigger.run_id: the claim holder and the intent's owner. |
| `project_states` | boolean | no | Compose the pinned graph's projection into the patch. Default `true`. |
| `recompute_on_stale` | integer | no | Re-reads and recomputations after the row moved under the patch, before failing CodeRevisionConflict. Default `3`. |
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose envelope ended unsigned (Signing Status declined/expired/voided) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `fields` | object | no | key -> {value, sources, basis, note?}. |
| `left_blank` | list of any, optional | no |  |
| `dropped` | list of any, optional | no |  |
| `summary` | string, optional | no |  |
| `read_guidance` | string, optional | no | The digest of the instructions the preparer read. |
| `template_sha256` | string, optional | no | The template the proposals were read from; a row reseeded from another meanwhile skips the write whole. |
| `evidence` | EvidencePolicy | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `document_status` | string | The document machine's state. |
| `document_why` | string |  |
| `changed` | boolean |  |
| `applied` | object | {count, patched, stale, projected, worklist}. |
| `filled_keys` | list of string |  |
| `skipped` | list of object | The proposals not written, [{key, reason}]. |
| `values` | object |  |
| `template_changed` | boolean |  |

`EvidencePolicy`:

| Field | Type | Notes |
|---|---|---|
| `answers_column` | string |  |
| `recipient_excluded_columns` | list of string |  |
| `guidance` | GuidanceSources |  |
| `filled_from` | string |  |

`GuidanceSources`:

| Field | Type | Notes |
|---|---|---|
| `agent` | string |  |
| `notes_scalar` | string |  |
| `stage_note_scalar` | string |  |

`StoreClaimCondition`:

| Field | Type | Notes |
|---|---|---|
| `column` | string |  |
| `test` | `set` / `unset` / `equals` / `not_equals` / `in` / `not_in` |  |
| `value` | string or list of string, optional |  |

`StoreClaimRefusal`:

| Field | Type | Notes |
|---|---|---|
| `code` | string | Error type the run fails with. |
| `message` | string | What the refusal tells the caller. |
| `when` | list of StoreClaimCondition |  |

### `feature.esign.document.prepare`

Seed the row from a pinned template: its fields, the values the
seed can name by spelling, its signer roles and who each seats. A row
already prepared from this template keeps its values; only missing
preview pages are written onto it.

```yaml
- id: <step>
  activity: feature.esign.document.prepare
  args:
    now: <string>
    run_id: <string>
    refuse_when: <array>
    table_name: <string>
    record_id: <integer>
    seed: ...
    roles: ...
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `stage` | string, optional | no | The signing stage the document is for, as the process names it. With a `fold`, it is stamped on the row and decides whether a settled document is folded away. |
| `fold` | FoldPolicy, optional | no | Sign more than once on one row: stamp the document's stage and fold a settled document of a stage the row has left into the signings ledger. Unset: one document per row. |
| `send_intent_column` | string | no | Where a claim freezes its send intent. Default `"Send Intent"`. |
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `run_id` | string | yes | This run's identity, normally $trigger.run_id: the claim holder and the intent's owner. |
| `project_states` | boolean | no | Compose the pinned graph's projection into the patch. Default `true`. |
| `recompute_on_stale` | integer | no | Re-reads and recomputations after the row moved under the patch, before failing CodeRevisionConflict. Default `3`. |
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose envelope ended unsigned (Signing Status declined/expired/voided) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `already_prepared` | boolean | no | Default `false`. |
| `template_file_key` | string, optional | no |  |
| `template_sha256` | string, optional | no |  |
| `keys` | list of string, optional | no |  |
| `signer_roles` | list of string, optional | no |  |
| `signature_tags` | list of object, optional | no |  |
| `split_placeholders` | list of any, optional | no |  |
| `sender_email` | string, optional | no |  |
| `values` | object, optional | no |  |
| `template_html_file_key` | string, optional | no |  |
| `template_preview_file_keys` | list of string, optional | no |  |
| `guidance` | string, optional | no | The preparer's instructions now, for prefill_due. |
| `seed` | SeedPolicy | yes |  |
| `roles` | SignerRolePolicy | yes |  |
| `signings_table` | string, optional | no | The signings ledger a folded document goes to, upserted on signing_key after the seed's patch. Required with fold. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `document_status` | string | The document machine's state. |
| `document_why` | string |  |
| `changed` | boolean |  |
| `applied` | object | {count, patched, stale, projected, worklist}. |
| `skipped` | boolean | The row no longer named what the step expected. |
| `prepared` | boolean |  |
| `folded` | object, optional | The settled document folded into the signings ledger, {signing_key, outcome, stage}; null when nothing was folded. |
| `merge_underway` | boolean |  |
| `has_document` | boolean |  |
| `prefill_due` | boolean |  |
| `values` | object |  |
| `signers` | list of any |  |
| `keys` | list of any |  |
| `signer_roles` | list of any |  |
| `deadline_keys` | list of string |  |
| `template_file_key` | string, optional |  |
| `template_sha256` | string, optional |  |
| `template_html_file_key` | string, optional |  |

`FoldPolicy`:

| Field | Type | Notes |
|---|---|---|
| `document_of_column` | string |  |
| `ledger_document_columns` | map of string |  |
| `leaving` | string |  |

`SeedPolicy`:

| Field | Type | Notes |
|---|---|---|
| `spellings` | map of list of string |  |
| `dates` | list of string |  |
| `deadline_column` | string |  |
| `clear_columns` | list of string | The bundle's own columns of the document slot (a signing-link email's, say): a fresh seed blanks them with the request they belonged to. |

`SignerRolePolicy`:

| Field | Type | Notes |
|---|---|---|
| `sender_words` | list of string |  |
| `recipient_words` | list of string |  |
| `recipient_email_column` | string |  |

`StoreClaimCondition`:

| Field | Type | Notes |
|---|---|---|
| `column` | string |  |
| `test` | `set` / `unset` / `equals` / `not_equals` / `in` / `not_in` |  |
| `value` | string or list of string, optional |  |

`StoreClaimRefusal`:

| Field | Type | Notes |
|---|---|---|
| `code` | string | Error type the run fails with. |
| `message` | string | What the refusal tells the caller. |
| `when` | list of StoreClaimCondition |  |

### `feature.esign.document.reconcile`

Settle an uncertain send from the send ledger or the operator's
answer, bound to the fingerprint and claim that were inspected.

```yaml
- id: <step>
  activity: feature.esign.document.reconcile
  args:
    now: <string>
    run_id: <string>
    table_name: <string>
    record_id: <integer>
    expected_fingerprint: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `run_id` | string | yes | This run's identity, normally $trigger.run_id: the claim holder and the intent's owner. |
| `project_states` | boolean | no | Compose the pinned graph's projection into the patch. Default `true`. |
| `recompute_on_stale` | integer | no | Re-reads and recomputations after the row moved under the patch, before failing CodeRevisionConflict. Default `3`. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `expected_fingerprint` | string | yes |  |
| `expected_sending` | string, optional | no |  |
| `resolution` | string | no | Default `""`. |
| `envelope_id` | string | no | Default `""`. |
| `provider` | string | no | The provider the operator's envelope is at; the ledger's answer names its own. Default `""`. |
| `ledger` | object | no | feature.esign.inspect_send's answer: {resolved, envelope_id, provider, fingerprint}. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `record_id` | integer, optional |  |
| `document_status` | string | The document machine's state. |
| `document_why` | string |  |
| `changed` | boolean |  |
| `applied` | object | {count, patched, stale, projected, worklist}. |
| `skipped` | boolean | The row no longer named what the step expected. |
| `resolved` | string | sent / not_sent / ''. |
| `parked` | boolean |  |
| `source` | string | ledger / operator / ''. |
| `envelope_id` | string |  |
| `fingerprint` | string |  |
| `detail` | string |  |

### `feature.esign.document.template_source`

Probe a row against the stage's picked template: the pick's file and
whether this row is already prepared from it (`warm`), refused when
the row may not be prepared at all. Writes nothing.

```yaml
- id: <step>
  activity: feature.esign.document.template_source
  args:
    refuse_when: <array>
    table_name: <string>
    record_id: <integer>
    template_scalar: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `stage` | string, optional | no | The signing stage the document is for, as the process names it. With a `fold`, it is stamped on the row and decides whether a settled document is folded away. |
| `fold` | FoldPolicy, optional | no | Sign more than once on one row: stamp the document's stage and fold a settled document of a stage the row has left into the signings ledger. Unset: one document per row. |
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose envelope ended unsigned (Signing Status declined/expired/voided) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RecordNotFound}. |
| `template_scalar` | string | yes | The scalar holding the pick's envelope ({store_file_key, sha256, filename, drive_file_id, source_mime_type}); read beside the row. Blank reads as no pick. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `refused` | boolean |  |
| `error_type` | string | The refusal's code. |
| `reason` | string |  |
| `file_key` | string |  |
| `filename` | string |  |
| `drive_file_id` | string |  |
| `source_mime_type` | string |  |
| `already_prepared` | boolean |  |
| `folding` | boolean | The row's settled document is folded away by the prepare: the row reads cold. |
| `merge_underway` | boolean |  |
| `has_document` | boolean |  |
| `needs_template_html` | boolean |  |
| `needs_template_previews` | boolean |  |
| `warm` | boolean |  |
| `needs_merge` | boolean |  |

`FoldPolicy`:

| Field | Type | Notes |
|---|---|---|
| `document_of_column` | string |  |
| `ledger_document_columns` | map of string |  |
| `leaving` | string |  |

`StoreClaimCondition`:

| Field | Type | Notes |
|---|---|---|
| `column` | string |  |
| `test` | `set` / `unset` / `equals` / `not_equals` / `in` / `not_in` |  |
| `value` | string or list of string, optional |  |

`StoreClaimRefusal`:

| Field | Type | Notes |
|---|---|---|
| `code` | string | Error type the run fails with. |
| `message` | string | What the refusal tells the caller. |
| `when` | list of StoreClaimCondition |  |
