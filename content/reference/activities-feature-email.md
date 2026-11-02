---
id: activities-feature-email
title: feature.email
order: 129
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.email activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.email` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.email.check_connected`

Probe whether the channel has a usable account bound for mail reads,
without raising when it doesn't (see the module docstring for what
"usable" can and can't cover).

Carry `integration_id` or `integration_name` (inherited from
ActivityInput) so the identity binding swaps the auth to the account
before the check (same as email.list).

```yaml
- id: <step>
  activity: feature.email.check_connected
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `provider` | string | no | Canonical provider ('google' or 'microsoft'); pass $channel.integrations.<name>.provider. A value with no mail reader runtime -> connected=False. Default `"google"`. |
| `for_send` | boolean | no | Also require the scope a send or reply needs (Google: gmail.send); a grant without it -> connected=False, reason missing_scope. Lets a flow refuse a read-only mailbox before it shows a preview it could never send. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `connected` | boolean | True if the step has a bound account that can read mail as far as Popcorn knows. False when no account is bound, the account row is gone, its refresh token was rejected, or its grant lacks the read scope. Use as a `when:` guard before mail reads. |
| `reason` | string, optional | Why connected is False (None when True): not_bound, unsupported_provider, not_found, invalid_grant, missing_scope. |

### `feature.email.chunk_phases`

The `collect:`ed summaries of a `process_chunk` fan-out.

```yaml
- id: <step>
  activity: feature.email.chunk_phases
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `summaries` | list of object | no | The chunk step's collected ChunkSummary objects; pass $steps.<chunks step>.<collect name>. An empty list is valid and returns zeros — a run that listed no mail chunked nothing. |
| `extra_summaries` | list of object | no | A SECOND fan-out of the same activity, folded in with the first. A flow that sweeps the window once and then fetches a selected subset has two, and reading either alone misreports the run: the sweep's half has no bodies in it and the subset's is nothing but bodies, so a `cpu_pct_raw` off one of them describes neither. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `chunks` | integer | Chunks folded in. |
| `messages` | integer | Messages they processed in total. |
| `raw_fetched` | integer | Messages fetched as full RFC822 because something reads their body. |
| `metadata_fetched` | integer | Messages fetched as headers alone. |
| `phase_ms` | map of integer | Wall milliseconds per phase, summed over the chunks — so busy time, not the step's wall. Keys roll up on every dotted prefix: `fetch`, `decode`, `filter`, `extract`, `persist`, and the same names again under `raw.` and `meta.` for the two fetch halves. `total` is each chunk's whole op, summed. |
| `cpu_ms` | map of integer | CPU milliseconds over the same spans and the same keys. Against phase_ms this says which phases are waiting and which are work. |
| `cpu_pct` | integer | Local CPU as a percentage of total wall, over every chunk. Low means the step is dominated by round trips. |
| `cpu_pct_raw` | integer | The same percentage for the raw-fetched half's per-message work alone (decode, filter, extract, persist). |
| `cpu_pct_meta` | integer | The same for the header-only half's per-message work. |
| `invoke_wall_ms` | integer | Summed wall of the AgentCore invokes as the worker saw them. 0 when the chunks did not run in a runtime. |
| `agentcore_overhead_ms` | integer | Summed invoke wall MINUS the runtime's own total: AgentCore's per-invocation cost, measured. |
| `cold_invokes` | integer | Chunks that were the first invoke on their microVM, so paid a cold start. |
| `cold_overhead_ms` | integer | Their share of agentcore_overhead_ms. |
| `warm_overhead_ms` | integer | The rest. Divided by its invoke count against cold_overhead_ms over cold_invokes, the gap is the cold start. |

### `feature.email.create_draft`

Create a draft in the user's Gmail Drafts (does NOT send).

The step must carry `integration_id`
($channel.integrations.<name>.id) — the identity binding swaps the
auth to the configured account before the token is minted. Supply
`original_message_id` (the Gmail message id of the email being replied to,
e.g. a tracker row's `message_id`) to thread the draft under that message;
omit it for a standalone draft.

```yaml
- id: <step>
  activity: feature.email.create_draft
  args:
    to: <array>
    subject: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `provider` | string | no | Canonical mailbox provider. The step MUST also pass integration_id ($channel.integrations.<name>.id) so the draft is created in the channel's configured Gmail account. Default `"google"`. |
| `to` | list of string | yes | Recipient email addresses (at least one). |
| `subject` | string | yes | Subject line. |
| `body` | string | yes | Email body, plain text or HTML. Write HTML whenever the email carries a link, so the link sits on words (<a href="https://...">this calendar</a>) instead of showing a bare URL: wrap each paragraph in <p>...</p> and break lines inside one with <br>. The body is sent as HTML only when it contains <p>, <div>, <body> or <html> — an <a> or <br> alone ships as literal tags in a plain-text email. The 'Powered by Popcorn' footer is appended automatically (with 'Popcorn' linked in HTML mail), so do not write one. Escape interpolated values in HTML templates ({{ name / e }}). |
| `cc` | list of string | no | Cc addresses. |
| `bcc` | list of string | no | Bcc addresses. |
| `original_message_id` | string, optional | no | The message being replied to: its Gmail API id, or its RFC822 Message-ID header (e.g. a Matched Emails row's message_id) — the proxy auto-detects the form by the '@' only the header contains. When set, the draft threads under that message (threadId + In-Reply-To); unresolvable → a standalone draft. |
| `send_mode` | string | no | The channel's `popcorn.email_send_mode` (read it with a foundation.store.get_scalar step and pass it here). `off` writes NOTHING to the mailbox and returns skipped=True; `draft` / `send` both create the draft (this activity never sends). Defaults to `draft` so a caller that hasn't adopted the switch keeps its current behavior — the PLATFORM default is off, so a flow that wants the strict contract must read the scalar with default "off" and pass it in. Default `"draft"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `skipped` | boolean | True when send_mode was `off`: nothing was written to the mailbox. draft_id stays empty, so a downstream `when:` gated on it treats this exactly like a failed create. |
| `draft_id` | string, optional | Gmail id of the created draft. |
| `message_id` | string, optional | Gmail id of the draft's message. |
| `thread_id` | string, optional | Thread the draft landed in. |

### `feature.email.extract`

Pull structured fields out of one email message with an LLM.

Given a single `message` (one entry from `email.list`) and a JSON
`schema`, asks Claude to extract the requested fields and returns a dict
conforming to `schema` (absent fields come back null). A schema violation
fails the step non-retryably.

```yaml
- id: <step>
  activity: feature.email.extract
  args:
    message: <object>
    schema: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message` | object | yes |  |
| `schema` | object | yes |  |
| `model` | string | no | Default `"claude-haiku-4-5-20251001"`. |

### `feature.email.fetch_repair_source`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.email.fetch_repair_source
  args:
    conversation_id: <string>
    message_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `message_id` | string | yes |  |
| `include_thread` | boolean | no | Default `true`. |
| `provider` | `google` / `gmail` | no | Default `"gmail"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `message_id` | string |  |
| `gone` | boolean |  |
| `body` | string |  |
| `fields` | map of string |  |

### `feature.email.fetch_to_rows`

Fetch Gmail messages by id and upsert them as channel tracker rows.

The generic mail→rows ingest for the emailreader channel: fetches each
message's body inside the activity (so full RFC822 never crosses a Temporal
payload boundary) and writes one row per message via `message_to_row`.

`message_ids` come from `email.search` (a small list — ids only); bodies
are fetched here (via the gmail_reader runtime), never passed in.

Inherits `StatusProgressArgs` (`progress_kind` / `progress_pct_start`
/ `progress_pct_end`) so a flow can drive the `email_backfill_progress`
widget across the body-fetch — the whole id list is fetched in this one
activity, so `len(message_ids)` is the denominator (no per-chunk total to
thread in, unlike `mbox.replay_chunk`). Dormant when `progress_kind` is
unset (the hourly tail tick leaves it unset).

```yaml
- id: <step>
  activity: feature.email.fetch_to_rows
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes |  |
| `message_ids` | list of string | no |  |
| `provider` | string | no | Canonical mailbox provider. The step MUST also pass integration_id ($channel.integrations.<name>.id) so gmail_reader runs against the channel's configured Gmail account. Default `"google"`. |
| `table_name` | string | no | Default `"tracker"`. |
| `snippet_chars` | integer | no | Default `200`. |
| `upsert_batch_size` | integer | no | Default `100`. |
| `extra_fields` | object | no | Constant columns stamped onto EVERY row before the upsert (e.g. {'search_id': ...} so an investigator can tell one search's hits from another's). Merged after message_to_row, so a key that collides with a row column wins. Empty for the emailreader tick + backfill, which write the plain row contract. |
| `read_attachments` | boolean | no | Default `false`. |
| `max_attachment_reads` | integer | no | Default `3`. |
| `attachment_text_chars` | integer | no | Default `4000`. |
| `ai_provider` | string | no | Default `"anthropic"`. |
| `ai_model` | string | no | Default `""`. |
| `extract_candidates` | boolean | no | Default `false`. |
| `max_link_resolves` | integer | no | Default `4`. |
| `merge_on` | list of string | no | Dedup key for the upsert. Defaults to the Gmail message id (one row per message — the emailreader contract). Pass a composite (e.g. ['message_id', 'search_id']) when the same message may legitimately appear under several tags and each pairing needs its own row, instead of the later write overwriting the earlier one's extra_fields. |
| `with_rfc822_id` | boolean | no | Also write each message's RFC822 `Message-ID` header onto its row as `rfc822_message_id` (RFC822_ID_COLUMN), beside the Gmail id in `message_id`. For a caller whose other table knows the message by that header. Empty when the message carries none. Default `false`. |

**Returns**

Per-run counters (the DSL collects nothing — the write is the effect).

| Field | Type | Notes |
|---|---|---|
| `total` | integer |  |
| `written` | integer |  |
| `skipped` | integer |  |
| `attachment_reads` | integer |  |
| `attachment_read_failures` | integer |  |
| `link_resolves` | integer |  |
| `link_resolve_failures` | integer |  |

### `feature.email.filter_extract`

Filter and extract identifiers from one raw email, deterministically.

Runs the pure `Tier0to3Filter` + `Extractor` over a single message and
returns the canonical `ExtractedIdentifiers` payload that
`shipment.resolve` consumes (no LLM — unlike `email.extract`).

`raw_b64` is a standard-base64-encoded RFC822 message (what
`email.history_since` emits — already normalized from Gmail's base64url).
`my_domains` lets the watcher drop work-domain correspondence (e.g.
`jlinteriors.design`) at Tier 0; matches the eTLD+1 of the From address.

```yaml
- id: <step>
  activity: feature.email.filter_extract
  args:
    raw_b64: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `raw_b64` | string | yes |  |
| `my_emails` | list of string | no |  |
| `my_domains` | list of string | no |  |

**Returns**

Per-message verdict.

`dropped` = filtered out (tier 0-3). `extracted` is the JSON payload
`shipment.resolve` consumes; `has_join_key` lets a foreach gate
resolve with `when:` instead of always firing.

| Field | Type | Notes |
|---|---|---|
| `dropped` | boolean |  |
| `has_join_key` | boolean |  |
| `extracted` | object |  |

### `feature.email.get`

Fetch one Gmail message by id and return its full content (subject,
sender, date, and plain-text body). Use after email.list when you have
a message id and need the body — e.g. to extract fields from it with
email.extract.

```yaml
- id: <step>
  activity: feature.email.get
  args:
    message_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message_id` | string | yes | Gmail message id, e.g. from $steps.<list-step>.output.messages.0.id. |
| `provider` | string | no | Mailbox backend (Gmail only). Pass integration_id ($channel.integrations.<name>.id) to select the account read. Default `"google"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `message` | EmailMessage | The fetched message. Reference its body as $steps.<id>.output.message.body. |

`EmailMessage`:

| Field | Type | Notes |
|---|---|---|
| `id` | string |  |
| `thread_id` | string, optional |  |
| `subject` | string |  |
| `from` | string, optional |  |
| `received_at` | string, optional |  |
| `body` | string |  |

### `feature.email.get_thread`

Fetch every message in a Gmail thread (the full reply chain) by
thread id, oldest first. Use when you need the whole back-and-forth
conversation rather than a single message — e.g. summarizing a thread
email.list surfaced.

```yaml
- id: <step>
  activity: feature.email.get_thread
  args:
    thread_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `thread_id` | string | yes | Gmail thread id, e.g. from $steps.<list-step>.output.messages.0.thread_id. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `thread_id` | string | The thread id that was fetched. |
| `messages` | list of EmailMessage | All messages in the thread, oldest first. Reference them as $steps.<id>.output.messages[*].body. |

`EmailMessage`:

| Field | Type | Notes |
|---|---|---|
| `id` | string |  |
| `thread_id` | string, optional |  |
| `subject` | string |  |
| `from` | string, optional |  |
| `received_at` | string, optional |  |
| `body` | string |  |

### `feature.email.history_since`

Fetch new Gmail message ids since a `historyId` cursor (incremental).

The watcher's go-forward tail: given an access token and a Gmail
`history_id`, returns the new message ids and the advanced cursor. Ids
only — bodies are fetched per-message downstream so a large delta can't
blow the Temporal result limit.

A blank `history_id` causes a baseline (`profile` call) — no messages
returned, but the mailbox's current historyId becomes the cursor for the
next call. The watcher shell normally has a non-blank cursor by the time
this activity runs (it arms a baseline before entering the loop).

```yaml
- id: <step>
  activity: feature.email.history_since
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `provider` | string | no | Selects the channel connector so the gmail_reader runtime runs as the channel's CLAIMED Gmail subject. The flow step MUST pass this explicitly — an activity-side default is not remapped by the connector override (lib.temporal.channel_config). Default `"gmail"`. |
| `history_id` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `message_ids` | list of string |  |
| `new_history_id` | string |  |
| `total_messages` | integer |  |

### `feature.email.list`

Search the workflow user's Gmail inbox and return matching messages
(subject, sender, date, and plain-text body for each).

Use `filter` to narrow by sender, recipient, subject, date range,
labels, read/unread, or attachments — combine fields freely (they are
AND-ed). For criteria the structured fields don't cover, pass a raw
Gmail query in `filter.raw_query`. Set `ai_prompt` to additionally
keep only messages a Claude pass judges to match a natural-language
description (e.g. "invoices over $500"). To read one message's full
body or a whole reply thread, take an id/thread_id from the result and
call email.get / email.get_thread.

```yaml
- id: <step>
  activity: feature.email.list
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `provider` | string | no | Canonical provider that picks the reader runtime ('google' or 'microsoft'); pass $channel.integrations.<name>.provider alongside integration_id so both come from the same configured integration. Default `"google"`. |
| `filter` | GmailFilterInput | no |  |
| `ai_prompt` | string, optional | no | Natural-language criterion. When set, gmail_reader runs a Bedrock pass over the standard-filter result and keeps only messages matching this prompt. |
| `max_results` | integer | no | Default `100`. |
| `ai_filter_candidate_cap` | integer | no | Default `200`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `messages` | list of EmailMessage | Matching messages, newest first. Reference one in a later step as $steps.<id>.output.messages.0 (dotted index). |
| `query` | string | The Gmail `q` expression actually run. |
| `candidates_examined` | integer | How many messages the filter examined before truncating to max_results. |

`EmailMessage`:

| Field | Type | Notes |
|---|---|---|
| `id` | string |  |
| `thread_id` | string, optional |  |
| `subject` | string |  |
| `from` | string, optional |  |
| `received_at` | string, optional |  |
| `body` | string |  |

`GmailFilterInput`:

| Field | Type | Notes |
|---|---|---|
| `senders` | list of string | Match the From: header. Each entry is an email address or domain (e.g. 'alerts@stripe.com' or 'stripe.com'). |
| `recipients` | list of string | Match the To: header (email address or domain). |
| `subject_contains` | string, optional | Phrase that must appear in the subject line. |
| `after` | string, optional | Only mail on/after this date. Gmail date YYYY/MM/DD or relative ('7d' = last 7 days, '24h', '30m'). |
| `before` | string, optional | Only mail before this date (YYYY/MM/DD or relative). |
| `labels` | list of string | Gmail label names the message must carry (e.g. 'INBOX', 'IMPORTANT', or a user label). |
| `is_unread` | boolean, optional | true → only unread, false → only read, omit → both. |
| `has_attachment` | boolean, optional | true → only messages with attachments. |
| `raw_query` | string, optional | Escape hatch: a raw Gmail search expression (e.g. 'has:userlabels older_than:1y'), AND-combined with the structured fields above. |

### `feature.email.list_message_ids`

Enumerate a date window's Gmail message ids for a per-chunk backfill.

Lists only the message ids (cheap) for the `after`/`before` window —
oldest-first — and stores them as a small JSON file; each
`email.process_chunk` then fetches just its slice live. Avoids
materializing a multi-GB mbox. Returns the `ids_file_key` + total count.

`provider` only drives the connector override (routing the reader to the
channel's claimed subject); identity comes from the auth context.

```yaml
- id: <step>
  activity: feature.email.list_message_ids
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `after` | string | no | Default `""`. |
| `before` | string | no | Default `""`. |
| `lookback_days` | integer | no | Relative lower bound: when `after` is blank and this is >0, the window starts `lookback_days` ago (computed at activity time, since the interpreter workflow body can't read the clock). An explicit `after` always wins; 0 leaves the lower bound open. Default `0`. |
| `provider` | string | no | Mailbox backend; present so the channel connector override routes this step onto the channel's claimed Gmail user. Default `"gmail"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ids_file_key` | string |  |
| `total_messages` | integer |  |

### `feature.email.persist_body`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.email.persist_body
  args:
    conversation_id: <string>
    file_key: <string>
    filename: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_key` | string | yes |  |
| `filename` | string | yes |  |
| `body` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string |  |

### `feature.email.popcorn_threads`

Fetch `message_ids` and return the threads they belong to that were
sent to the mailbox's +popcorn address, one per thread.

`mailbox` is the connected account's address
($channel.integrations.<name>.provider_account); the Popcorn address is
derived from it (name+popcorn@domain). The step MUST pass integration_id
($channel.integrations.<name>.id) so the mail is read from that mailbox.

```yaml
- id: <step>
  activity: feature.email.popcorn_threads
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `message_ids` | list of string | no |  |
| `mailbox` | string | no | The connected mailbox's address, e.g. $channel.integrations.feedback_inbox.provider_account. Default `""`. |
| `senders` | list of string | no | Who may add the Popcorn address to a thread: addresses or domains (e.g. popcorn.ai), counted only when Gmail's DMARC check passed for that domain. Empty means the mailbox's own domain, or nobody for a gmail.com mailbox. |
| `provider` | string | no | Canonical mailbox provider. The step MUST also pass integration_id so gmail_reader reads the channel's Gmail account. Default `"google"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `threads` | list of PopcornThread |  |
| `checked` | integer |  |

`PopcornThread`:

| Field | Type | Notes |
|---|---|---|
| `thread_id` | string |  |
| `message_id` | string | The thread's newest new message. |
| `subject` | string |  |
| `sender` | string |  |

### `feature.email.process_chunk`

Run the watcher pipeline over one chunk of a Gmail backfill.

The Gmail counterpart to `mbox.process_chunk`: fetches only this chunk's
`[start, end)` slice of message ids live from Gmail (streaming one raw at
a time, so memory is bounded by chunk size) and runs the same filter +
extract + resolve core. Re-resolves the token per chunk since a large
backfill outlives a token's ~1h lifetime.

Reuses every pipeline knob from `BaseProcessChunkInput`; the
source-specific bits are the id-list file and the connector `provider`.

```yaml
- id: <step>
  activity: feature.email.process_chunk
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation that owns the source + the target table. |
| `chunk` | MboxChunk, optional | no | The [start, end) slice of the ids_file_key id list to process. With ids_file_key it slices the file's id list; with message_ids it slices the inline delta. Omitted → the whole list. |
| `my_emails` | list of string | no |  |
| `my_domains` | list of string | no |  |
| `keep_tiers` | list of string | no | Soft filter tiers to keep-and-tag instead of dropping. Only tier2/tier3 are overridable; empty preserves delivery behavior. |
| `pool_self_sent` | boolean | no | Pool Tier-0 self-sent mail as outbound metadata while still dropping it from normal processing. Default `false`. |
| `detections_mode` | boolean | no | Write metadata-only detection pool records and bypass shipment resolution/AI. Used only by Automation Coordinator. Default `false`. |
| `table_name` | string | no | Target agent-store table. `tracker` for the PDF flow's table; `shipments` for the watcher's own (legacy). Default `"shipments"`. |
| `seed_only` | boolean | no | When true (production), the resolver drops unmatched emails instead of creating fresh shipments. Default `false`. |
| `ai_provider` | string | no | anthropic / bedrock. Maps to AIExtractor's provider. Default `"anthropic"`. |
| `ai_model` | string, optional | no | Model id. Falls back to provider default (claude-haiku-4-5-20251001) when unset. |
| `ai_batch_size` | integer | no | Per-flush batch size. The LLM-first validation found 15 produced per-email AI dropout; 5 is the safer default. Default `5`. |
| `enable_semantic_match` | boolean | no | Tracker mode only: enable the LLM-adjudicated semantic match tier (2.5) for emails that fall through the deterministic + fuzzy tiers on a vendor/designer vocabulary gap. Default `false`. |
| `semantic_shadow` | boolean | no | When the semantic tier is enabled, run it in shadow mode: log the would-be bind + confidence, persist nothing. Flip to false to enable writes once validated. Default `true`. |
| `semantic_threshold` | number | no | Minimum LLM confidence for a semantic match to bind. Default `0.8`. |
| `enable_vendor_match` | boolean | no | Tracker mode only: enable the vendor-confirmed match tier (2.4) — an email whose sender domain belongs to a row's PDF 'Vendor Id' binds on a lower description threshold (recovers VOCAB_GAP) — AND the cross-vendor gate that vetoes a fuzzy bind whose sender vendor isn't the row's. On by default. Default `true`. |
| `progress_total_messages` | integer, optional | no | Total messages across all chunks (the source's total count) — the denominator for the overall replay percentage. Paired with progress_kind to drive the status-widget progress bar. |
| `ids_file_key` | string, optional | no | Backfill source: key under /v1/files for the JSON id list written by email.list_message_ids ({'message_ids': [...]}, oldest-first); this chunk processes its [start, end) slice. Mutually exclusive with message_ids — exactly one must be set. |
| `message_ids` | list of string, optional | no | Live-tick source: the message ids to process passed inline (the watch tick's history_since delta). When set, ids_file_key is ignored; `chunk` may slice the delta and defaults to [0, len(message_ids)). Mutually exclusive with ids_file_key. |
| `provider` | string | no | Drives the connector override so the per-chunk token re-resolution targets the channel's claimed Gmail user. Default `"gmail"`. |
| `body_window_after` | string | no | ISO-8601 instant. Fetch full RFC822 bodies only for mail dated at or after it; older mail in the slice is fetched as headers alone (Gmail format=metadata), which is every column of the detection pool but the body-derived scalars and the body half of asks_question. For a flow whose window is far wider than the stretch of it anything reads a body from. Empty (default) fetches the whole slice raw. Default `""`. |
| `headers_only` | boolean | no | Fetch NO bodies for this slice — every message comes back as headers alone, whatever body_window_after says. For a caller whose body selection is not a date at all: inbox-scan needs the bodies of inbound mail on threads live in its short window, which no chunk can know because a later chunk can revive a thread. Such a caller takes the window as headers here and names the bodies it wants in a second pass over the pooled rows. Default `false`. |

**Returns**

Per-chunk counters. Aggregated by the DSL flow's collect step.

(Formerly `MboxProcessChunkOutput` in the activities layer; relocated to
the pure domain so both the worker and the runtime return the same shape.)

| Field | Type | Notes |
|---|---|---|
| `chunk_start` | integer |  |
| `chunk_end` | integer |  |
| `total` | integer |  |
| `dropped` | integer |  |
| `ai_queued` | integer |  |
| `ai_resolved` | integer |  |
| `kept_deterministic` | integer |  |
| `parse_errors` | integer |  |
| `ai_failed` | integer |  |
| `ai_no_key` | integer |  |
| `raw_fetched` | integer |  |
| `metadata_fetched` | integer |  |
| `phase_ms` | map of integer |  |
| `cpu_ms` | map of integer |  |
| `runtime_invoke_seq` | integer |  |
| `runtime_uptime_ms` | integer |  |
| `invoke_wall_ms` | integer |  |
| `agentcore_overhead_ms` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.email.reply`

Reply to a message within its thread. Get `thread_id` (and the
recipient/subject to reply to) from a prior email.list or email.get
step. Prefix the subject with 'Re: ' so Gmail threads it correctly.

```yaml
- id: <step>
  activity: feature.email.reply
  args:
    thread_id: <string>
    to: <array>
    subject: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `thread_id` | string | yes | Gmail thread id to reply within, e.g. $steps.<get-step>.output.message.thread_id. |
| `to` | list of string | yes | Recipient email addresses (at least one). |
| `subject` | string | yes | Subject line, typically 'Re: <original subject>'. |
| `body` | string | yes | Email body, plain text or HTML. Write HTML whenever the email carries a link, so the link sits on words (<a href="https://...">this calendar</a>) instead of showing a bare URL: wrap each paragraph in <p>...</p> and break lines inside one with <br>. The body is sent as HTML only when it contains <p>, <div>, <body> or <html> — an <a> or <br> alone ships as literal tags in a plain-text email. The 'Powered by Popcorn' footer is appended automatically (with 'Popcorn' linked in HTML mail), so do not write one. Escape interpolated values in HTML templates ({{ name / e }}). |
| `cc` | list of string | no | Cc addresses. |
| `bcc` | list of string | no | Bcc addresses. |
| `in_reply_to` | string, optional | no | Original message's RFC822 Message-Id, for In-Reply-To header threading. Optional. |
| `footer` | boolean | no | False sends `body` without the 'Powered by Popcorn' footer, exactly as given (a member's own reply, previewed byte for byte). True, the default, keeps it. Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `id` | string | Gmail id of the sent reply. |
| `thread_id` | string, optional | Thread the reply landed in. |
| `rfc822_message_id` | string, optional | The Message-ID header Gmail stamped on this reply. Keep it with the send so the next reply can pass it as in_reply_to. Null when it could not be read back. |

### `feature.email.search`

List the Gmail message ids matching a date-range query.

The date-range counterpart to `email.history_since`. Returns ids only
(bodies are fetched later by `email.fetch_to_rows`) plus `next_after`,
today's date cursor for the next tick.

`after` / `before` accept a Gmail `YYYY/MM/DD` date or a relative
form (`"30d"`, `"24h"`) — the emailreader cursor defaults to `"30d"`
and the backfill passes `"90d"`, so the same cursor values `email.list`
consumed keep working.

```yaml
- id: <step>
  activity: feature.email.search
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `provider` | string | no | Selects the channel connector so the gmail_reader runtime runs as the channel's CLAIMED Gmail subject. The flow step MUST pass this explicitly — an activity-side default is not remapped by the connector override (lib.temporal.channel_config). Default `"gmail"`. |
| `after` | string | no | Default `""`. |
| `before` | string | no | Default `""`. |
| `labels` | list of string | no |  |
| `query` | string | no | Default `""`. |
| `max_results` | integer | no | Default `1000`. |
| `after_floor` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `message_ids` | list of string |  |
| `next_after` | string |  |

### `feature.email.send`

Send a new email from the workflow user's mailbox. To
reply within an existing conversation, use email.reply instead.

```yaml
- id: <step>
  activity: feature.email.send
  args:
    to: <array>
    subject: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `to` | list of string | yes | Recipient email addresses (at least one). |
| `subject` | string | yes | Subject line. |
| `body` | string | yes | Email body, plain text or HTML. Write HTML whenever the email carries a link, so the link sits on words (<a href="https://...">this calendar</a>) instead of showing a bare URL: wrap each paragraph in <p>...</p> and break lines inside one with <br>. The body is sent as HTML only when it contains <p>, <div>, <body> or <html> — an <a> or <br> alone ships as literal tags in a plain-text email. The 'Powered by Popcorn' footer is appended automatically (with 'Popcorn' linked in HTML mail), so do not write one. Escape interpolated values in HTML templates ({{ name / e }}). |
| `cc` | list of string | no | Cc addresses. |
| `bcc` | list of string | no | Bcc addresses. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `id` | string | Gmail id of the sent message. |
| `thread_id` | string, optional | Thread the sent message landed in. |
| `rfc822_message_id` | string, optional | The Message-ID header Gmail stamped on the sent copy. Keep it with the send: a later email.reply to this message passes it as in_reply_to so the recipient's mailbox threads the reply. Null when it could not be read back. |

### `feature.email.sender_identity`

Resolve the configured sender's name + connected address.

Carry `integration_id` ($channel.integrations.<name>.id) so the
identity binding swaps the auth to the configured account before the
lookup (same as `email.list`); `provider` selects which connected
vendor address to return.

```yaml
- id: <step>
  activity: feature.email.sender_identity
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `provider` | string | no | Mailbox backend the draft sends through, as the canonical user_integrations provider ('google', 'microsoft'); pass $channel.integrations.<name>.provider. An unknown value degrades to an empty identity. Default `"google"`. |
| `medium` | string | no | The draft's medium. A From: line and a mailbox sign-off only make sense for an email draft, so any non-'email' medium (e.g. 'sms') short-circuits to an EMPTY identity — leave this at 'email' to resolve one. Default `"email"`. |
| `sign_as_user_id` | string, optional | no | Optional user to SIGN the draft as — pass $trigger.user_id so the body is signed with the name of whoever asked for the draft, not the connected mailbox's owner. The address/From: line still belongs to the bound mailbox account. Best-effort: empty/None or an unresolvable user keeps the mailbox owner's name. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `email` | string | The connected mailbox address (e.g. the claimed Gmail account). Empty when not connected / never resolved. |
| `display_name` | string | The sender's Popcorn display name. Empty when unset. |
| `from_header` | string | Ready-to-inline draft header line ending in a newline: 'From: Name <addr>\n' (or 'From: addr\n' with no name). EMPTY string when there's no address — inline it directly ahead of the To: line so an unknown sender leaves no dangling 'From:' label. |
| `from_display` | string | The sender as 'Name <addr>' (or bare 'addr'), WITHOUT the 'From:' label or newline — for card media_metadata. Empty when no address. |

### `feature.email.to_rows`

Shape decoded Gmail messages into emailreader tracker rows.

Maps each `email.list` message into the table's row shape (From / Subject
/ Date / Snippet / Body / message_id) and emits `next_after` (today's
Gmail date cursor) so the next tick lists only the current day's mail.
Takes the decoded `messages` plus the snippet character cap.

```yaml
- id: <step>
  activity: feature.email.to_rows
  args:
    messages: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `messages` | list of EmailMessage | yes |  |
| `snippet_chars` | integer | no | Default `200`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows` | list of object |  |
| `next_after` | string |  |

`EmailMessage`:

| Field | Type | Notes |
|---|---|---|
| `id` | string |  |
| `thread_id` | string, optional |  |
| `subject` | string |  |
| `from` | string, optional |  |
| `received_at` | string, optional |  |
| `body` | string |  |
