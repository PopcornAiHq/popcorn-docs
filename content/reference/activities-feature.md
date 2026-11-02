---
id: activities-feature
title: Feature activities
order: 103
group: Activities
parent: activities-catalog
layout: lookup
updated: 2026-10-31
summary: >
  The feature tier: operations that build on the foundation tier for one
  product capability each, with the Step that calls each, its arguments and
  what it returns.
lede: >
  Operations for one product capability each, with their arguments and
  results.
concepts: [activities, flow-grammar]
---

The 162 `feature` activities at `release` or `beta` status, by
domain. `beta` ones are marked. Each also takes the optional
`integration_id` and `integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains with the
rest of what every activity shares.

## feature.chase

### `feature.chase.agent_apply`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_apply
  args:
    conversation_id: <string>
    record_id: <integer>
    expected_revision: <integer>
    fingerprint: <string>
    turn_key: <string>
    plan: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |
| `expected_revision` | integer | yes |  |
| `fingerprint` | string | yes |  |
| `turn_key` | string | yes |  |
| `plan` | object | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `sent` | boolean |  |

### `feature.chase.agent_deliver`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_deliver
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `sent` | boolean |  |

### `feature.chase.agent_due`

`agent_prepare`'s arguments for every lead of a tick: the policy,
columns and guidance `claim_turn` hands prepare, over `record_ids`.
They must be the same arguments, or the fingerprint differs and every
lead launches (the bundle's tests hold the two steps together).

```yaml
- id: <step>
  activity: feature.chase.agent_due
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | no | Default `0`. |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |
| `record_ids` | list of integer | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `record_ids` | list of integer |  |
| `candidates` | integer |  |
| `launched` | integer |  |
| `skipped` | map of integer |  |
| `uncertain` | integer |  |
| `seeded` | integer |  |

### `feature.chase.agent_ingest`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_ingest
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `record_ids` | list of integer |  |
| `ingested` | integer |  |
| `skipped_other_channel` | integer |  |

### `feature.chase.agent_prepare`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_prepare
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `min_spacing_seconds` | integer | no | Default `86400`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `excluded_lead_columns` | list of string | no | Operational columns omitted from agent context and its input fingerprint. |
| `outbound_blocking_columns` | list of string | no | Current row facts that fence outbound while another operation owns contact. |
| `agent_names` | list of string | no |  |
| `guidance` | map of string | no |  |
| `guidance_override` | map of string or string | no | Default `""`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ready` | boolean |  |
| `needs_agent` | boolean |  |
| `context` | object |  |
| `plan` | object |  |
| `expected_revision` | integer |  |
| `fingerprint` | string |  |
| `turn_key` | string |  |
| `channel_notes` | map of string |  |
| `bundle_guidance` | map of string |  |
| `guidance_rev` | string |  |

### `feature.chase.agent_timed_out`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.agent_timed_out
  args:
    conversation_id: <string>
    record_id: <integer>
    error: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `turn_key` | string | no | Default `""`. |
| `error` | object | yes |  |
| `agent_steps` | list of string | no |  |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `timeouts` | integer |  |

## feature.chase.forward

### `feature.chase.forward.carry`

On the channel a lead was forwarded TO: which of the answers the
hand-over carries (`forwarded`, as `forward_lead`'s check built it)
match the questions of the stage the row is on, as `answers_entry`
records them (`carry_answers`). Read-only: the stage from the run's
pinned graph, its questions from its items scalar. A hand-over that
says `wrong_company`, onto a chase channel, matches across the two
companies' wording too (`match_answers`).

```yaml
- id: <step>
  activity: feature.chase.forward.carry
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `stage` | string | no | The row's `Stage` cell. Blank on a row no edge has moved yet, as every row a forward just added is: that row stands on this channel's first state, read from its own recipe. Default `""`. |
| `forwarded` | object | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `stage` | string |  |
| `stage_label` | string |  |
| `items` | string | The stage's items scalar. |
| `answers` | list of object |  |
| `matched` | list of object |  |
| `unmatched` | list of object |  |
| `count` | integer |  |
| `total` | integer |  |
| `carries` | boolean | Something carries over (`count > 0`). |
| `member` | map of string | Who the answers are entered as: the member who forwarded them, under the channel they came from. |
| `how` | string |  |
| `reason` | string | Why nothing carries, when nothing does. |

### `feature.chase.forward.check`

Everything a forward must satisfy before anything is written, and
what it would write. Read-only: refuses by name (`NoRequester`,
`NoContact`, `RecipientOptedOut`, `ForwardNotInRecipe`,
`NotForwardable`, `DocumentSendInProgress`, `ForwardTargetNotFound`,
`ForwardTargetNoAccess`, `ForwardTargetNotChase`,
`ForwardTargetAmbiguous`, `ForwardTargetIsSelf`,
`ForwardEntryNotTaken`, `ForwardEntryNotOffered`).

```yaml
- id: <step>
  activity: feature.chase.forward.check
  args:
    conversation_id: <string>
    record_id: <integer>
    target: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `target` | string | yes | The channel's id, or its name. |
| `note` | string | no | The member's own note. Default `""`. |
| `today` | string | no | The run's clock (ISO); its date goes on the note. Default `""`. |
| `target_apps` | list of `chase` / `claimcoordinator3` | no | The apps whose channels the run may forward into, among chase and claimcoordinator3. Chase alone when not given. Default `["chase"]`. |
| `source_app` | `chase` / `claimcoordinator3` / `claimcoordinator2` | no | The app THIS channel runs, which says how its row is read (`answer_boards`, `source_signings`). Chase and Claim Coordinator 3 read alike. Default `"chase"`. |
| `entry` | string | no | A later state of B's recipe to start the person on (one of the target's `entries`); empty for B's first stage. Default `""`. |
| `wrong_company` | boolean | no | The person was here meaning another company: their answers carry onto B's questions about B's company. A row held on Needs routine review for `wrong_company` is one without it. Chase or Claim Coordinator 3 on both sides; from a Claim Coordinator 2 routine it is ignored. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `name` | string |  |
| `email` | string |  |
| `phone` | string |  |
| `source_channel_id` | string |  |
| `source_name` | string |  |
| `target_channel_id` | string |  |
| `target_name` | string |  |
| `target_label` | string | `#name (id)`: `Forwarded To`. |
| `target_semver` | string |  |
| `accepts_forward_note` | boolean |  |
| `note_on` | string | forwarded_from / details |
| `forwarded_from` | string | The note B receives. |
| `accepts_forward_context` | boolean | B's intake takes the structured hand-over (`forwarded`) and records the answers that match. |
| `forwarded` | object | The structured hand-over (`forwarded_context`): sent to B only when it takes it. |
| `carry_over` | object | What would carry over onto B's first stage (`match_answers`, with `checked`, `stage`, `stage_label`); `checked: false` when B takes no hand-over or its questions could not be read. |
| `carry_message` | string | The carry-over in a sentence (`carry_message`). |
| `carry_clause` | string | `carry_message` after a space, "" when there is none: what the flow's message appends. |
| `entry` | string | The state B starts the person on; "" for its first. |
| `entry_label` | string | Its label on B. |
| `entry_clause` | string | " on <label>" when there is an entry, "" otherwise: what the flow's message appends to B's name. |
| `hand_over` | boolean | B does not hold the person: its `intake_add` runs. |
| `intake_inputs` | object |  |
| `existing` | boolean | B already holds the person. |
| `forwarded_by_us` | boolean | B's row came from this channel's forward (a re-run). |
| `target_record_id` | integer, optional |  |
| `target_stage` | string |  |
| `target_status` | string |  |
| `outcome` | string | forwarded / already_in_target |
| `close_why` | string | What this row's Forwarded card says (`Forward Note`) when B already held the person and nothing was added there; "" otherwise, and the state's own Why shows. |

### `feature.chase.forward.confirm`

Wait for the person to be on the target's tracker: B's intake runs
after `start_flow` returns. Read-only.

```yaml
- id: <step>
  activity: feature.chase.forward.confirm
  args:
    target_channel_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `target_channel_id` | string | yes |  |
| `email` | string | no | Default `""`. |
| `phone` | string | no | Default `""`. |
| `entry` | string | no | The state B was asked to start them on: wait for the row to stand there, not just to exist. Default `""`. |
| `attempts` | integer | no | Default `12`. |
| `interval_seconds` | number | no | Default `5.0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `found` | boolean |  |
| `target_record_id` | integer, optional |  |
| `target_stage` | string |  |
| `target_status` | string |  |
| `entered` | boolean | The row stands on `entry` (always true without one). False when it is there but was not moved within the wait: B's intake left it parked (`ForwardEntryRefused`), or is still carrying its answers. |
| `attempts` | integer |  |

### `feature.chase.forward.refused`

`forward_lead`'s failure, reported on the row and in the channel
when the run was launched to report it (`report_refusal`). Nothing is
written for any other run, a dry run, or a row no longer on the
routine-review card (the team decided while the forward ran).

```yaml
- id: <step>
  activity: feature.chase.forward.refused
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `target` | string | no | Default `""`. |
| `report` | boolean | no | Default `false`. |
| `dry_run` | boolean | no | Default `false`. |
| `error_type` | string | no | Default `""`. |
| `error_message` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `reported` | boolean |  |
| `reason` | string |  |

### `feature.chase.forward.replies`

The mail forwarded rows' own threads received since the forward
(and since the last note), as one channel note. Reads every forwarded
row and every own-thread inbound message on them, page by page.
Read-only: the tick posts the note and then stamps `Forwarded Reply
Noted At`.

```yaml
- id: <step>
  activity: feature.chase.forward.replies
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |
| `stamps` | list of ForwardReplyStamp |  |
| `count` | integer |  |

`ForwardReplyStamp`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `noted_at` | string |  |

### `feature.chase.forward.targets`

The channels the person behind this run may forward this channel's
leads into: every channel of the workspace running one of
`target_apps` (chase alone by default) they are a member of or can
view as an open channel, this one left out. Read-only.

```yaml
- id: <step>
  activity: feature.chase.forward.targets
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `target_apps` | list of `chase` / `claimcoordinator3` | no | The apps whose channels the run may forward into, among chase and claimcoordinator3. Chase alone when not given. Default `["chase"]`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `targets` | list of ForwardTarget |  |
| `count` | integer |  |

`ForwardTarget`:

| Field | Type | Notes |
|---|---|---|
| `channel_id` | string |  |
| `name` | string |  |
| `app` | string | The app the channel runs (`target_apps`). |
| `semver` | string | The version of its app the channel runs. |
| `line` | string | 'product', or the fork line's name. |
| `joined` | boolean | The requester is a member; else it is an open channel of the workspace they can view. |
| `accepts_forward_note` | boolean | The channel's intake takes the `forwarded_from` note (chase 0.96.0, Claim Coordinator 3 1.5.0 or later); else the note goes in Details. |
| `accepts_forward_context` | boolean | The channel's intake takes the structured hand-over (`forwarded`: the person's answers, signings and thread) and records the answers that match its own questions (chase 0.99.0, Claim Coordinator 3 1.6.0 or later); else it takes the note alone. |
| `entries` | list of map of string | The later states a forwarded lead may start on there (`entry`), each `{state, label}`, from its recipe's `world.forwarded_in` edge; [] when it takes them on its first stage only. |

## feature.chase.stage

### `feature.chase.stage.apply`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.apply
  args:
    conversation_id: <string>
    record_id: <integer>
    expected_revision: <integer>
    fingerprint: <string>
    turn_key: <string>
    plan: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `weekdays_only` | boolean | no | Default `false`. |
| `excluded_columns` | list of string | no |  |
| `hashed_only_columns` | list of string | no |  |
| `outbound_blocking_columns` | list of string | no |  |
| `author_voice_scalar` | string | no | Default `""`. |
| `author_column` | string | no | Default `""`. |
| `guidance` | map of string | no |  |
| `notes_alias` | map of string | no |  |
| `guidance_override` | map of string | no |  |
| `force` | boolean | no | Default `false`. |
| `start_ends_reminders` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |
| `expected_revision` | integer | yes |  |
| `fingerprint` | string | yes |  |
| `turn_key` | string | yes |  |
| `plan` | object | yes |  |
| `write_call_column` | boolean | no | Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `sent` | boolean |  |
| `event` | string |  |
| `payload` | object |  |
| `guards` | map of list of string |  |
| `why` | map of string |  |
| `stage` | string |  |
| `action` | string |  |
| `turn_key` | string |  |
| `stats` | object |  |

### `feature.chase.stage.board`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.board
  args:
    context: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `context` | object | yes |  |
| `validation` | object, optional | no |  |
| `eval_case` | object, optional | no |  |
| `deadlines` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `answers` | object, optional |  |
| `closed_items` | list of string |  |
| `open_items` | list of object |  |
| `complete` | boolean, optional |  |
| `summary` | string |  |
| `unverified` | integer |  |
| `held` | integer |  |
| `failed` | object, optional |  |
| `deadline` | object |  |
| `plan` | object, optional |  |
| `needs_writer` | boolean |  |

### `feature.chase.stage.booking_page_check`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.booking_page_check
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `accounts` | list of object | no | The channel's integrations, normally $channel.integration_list (name / id / provider_account). |
| `calendar` | string | no | The integration name of the calendar the booking stage reads. Default `"gcal"`. |
| `title` | string | no | The booking page's title; empty takes the title from `page`. Default `""`. |
| `page` | string | no | The booking page envelope as stored (the chase.booking scalar, JSON): its title, and the verdict stored with it. Default `""`. |
| `connected` | boolean, optional | no | feature.email.check_connected's answer for the calendar; null when the probe did not answer. |
| `events` | list of any, optional | no | Events read off the connected calendar (events, or pages of them). Null when nothing was read: the stored verdict is reported. |
| `read` | boolean | no | The caller read (or tried to read) the calendar: no `events` then means the read failed. Default `false`. |
| `lookup_error` | string, optional | no | The error type of a calendar read that failed ($steps.<read>.error.type; null when it did not fail). |
| `schedule_id` | string | no | The page's schedule_id when it is not in `page` (a link being set): cal.com/<path> reads the page's bookings as Cal.com's. Default `""`. |
| `others` | list of any | no | The recipe's other booking pages (feature.chase.stage.booking_pages' `pages`, or their titles): bookings that carry one of their titles too are told apart by the longest. |
| `shared_title` | boolean | no | The page being set replaces another page of the same title (feature.chase.stage.booking_pages' `replaces`): bookings with the title may be the old page's, so other_account warns of that and gives no `refusal`. Default `false`. |
| `pages` | list of object, optional | no | Several pages at once, as feature.chase.stage.booking_pages lists them (key / stage / title / envelope): each is judged as `page` would be, into `results`; the top-level verdict is the first page's. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `status` | string | verified / other_account / unverified / not_connected / lookup_failed / no_page. |
| `account` | string | The account the calendar is connected as; empty when none is, or its address is not known. |
| `owner` | string | other_account: the account the page's bookings are organized by. |
| `seen` | integer | Bookings of the page among the events. |
| `warning` | string | What the member should check, in words fit to show them; empty when verified. |
| `refusal` | string | other_account: why the page is refused, naming its owner and the connected account, in words fit to show the member; empty otherwise, and when the bookings may be another page's with the same title (`shared_title`). |
| `check` | object | The verdict as the envelope's `calendar_check` holds it: status / account / owner / warning, and `shared_title: true` on an other_account verdict the bookings of a page with the same title may account for. |
| `changed` | boolean | The events prove a verdict (verified or other_account) the envelope does not hold yet: write `check`. |
| `results` | list of object | With `pages`: one verdict per page (key / stage / title / status / account / owner / warning / check / changed). |
| `changed_pages` | list of object | With `pages`: the pages whose verdict the events changed, each `{key, patch}` for the envelope's merge (calendar_account / calendar_check). |

### `feature.chase.stage.booking_pages`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.booking_pages
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `title` | string | no | A title about to be stored: `taken_by` names the page that already has it, if any other does. Default `""`. |
| `stage` | string | no | With `resolve`: the booking stage whose page is being set; blank is the recipe's one booking stage. Default `""`. |
| `start` | boolean | no | With `resolve`: the start page is being set. Default `false`. |
| `schedule_id` | string | no | The schedule about to be stored with `title`: `replaces` says whether the page being set holds another schedule under the same title. Default `""`. |
| `resolve` | boolean | no | Also answer the page being set (`target_*`): the stage's `items` key or the start's `link`, and the checklist step `booking_link_set` marks. Refuses a stage that is not a booking stage, a blank stage on a recipe with none or several, and `start` on a recipe that does not start by a booking. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `pages` | list of BookingPage | Every page with a titled envelope, the booking stages' in graph order and then the start's. |
| `keys` | list of string | Every scalar key the recipe names a page with, set or not. |
| `any` | boolean | At least one page has a title. |
| `taken_by` | string | The stage (or `start`) whose page already carries `title`; empty when no other page does. |
| `replaces` | boolean | The page being set holds another schedule under `title`: the link replaces it, and bookings with that title may be the old page's. |
| `start_kind` | string |  |
| `start_key` | string | A calendar start's page scalar key. |
| `target_stage` | string | With `resolve`: the stage being set, or `start`. |
| `target_key` | string | With `resolve`: the envelope key to write. |
| `target_step` | string | With `resolve`: the checklist step to mark. |
| `target_label` | string | With `resolve`: the stage's label. |

`BookingPage`:

| Field | Type | Notes |
|---|---|---|
| `stage` | string | The booking stage that books on this page; `start` for the page a booking on which starts a chase. |
| `key` | string | The scalar key holding the envelope. |
| `title` | string | The page's title. |
| `link` | string | The page's share link. |
| `envelope` | string | The envelope as stored (JSON). |

### `feature.chase.stage.bookings`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.bookings
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `rows` | list of object, optional | no | The tracker's rows, with `_record_id`. Omitted: the activity reads the whole tracker itself (`channel_rows`), so no row list rides in the flow's history. |
| `events` | list of any | no | Changed calendar events as feature.gcal.list_changes (or list_events) returns them: events, or pages of events (lists; a skipped page's null is ignored). |
| `page` | string | no | ONE booking page envelope as stored (JSON), shared by every booking stage; `pages` names a page per stage instead. Default `""`. |
| `pages` | list of object | no | The recipe's pages as feature.chase.stage.booking_pages lists them (stage / key / title / link); `start` is the page a chase starts from. |
| `ledger` | list of object, optional | no | The `bookings` ledger's rows, so a change to a folded meeting is kept there. Omitted: the activity reads the ledger itself, as it does the tracker. |
| `watch_start` | boolean | no | Match changes to each row's `Start Event` before the intake: a start meeting cancelled or moved comes back in `start_patches` / `start_returns`, never as an intake. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `patches` | list of StageBookingsPatch | Each row's booking columns that changed. |
| `cancelled` | list of integer | Rows whose meeting was cancelled after their booking stage completed, or on a reminder stage: fire world.meeting_cancelled on them. |
| `returns` | list of StageBookingsReturn | The same rows, each with the payload its world.meeting_cancelled carries (`booked_in_stage`, the stage the meeting was booked in, for an edge that returns the row there). |
| `superseded` | list of string | Older meetings a rebooking on the same page replaced that are still live on the calendar: the sync cancels them, since nobody will attend a meeting the row no longer holds. |
| `folded` | list of object | Meetings an earlier stage booked that a later stage's booking took the row's slot from, as `bookings` ledger rows for the sync to upsert. They stay on the calendar. |
| `ledger_patches` | list of object | Ledger rows whose meeting changed on the calendar (cancelled, or moved), each a partial row keyed `booking_key` for the sync to upsert. |
| `intakes` | list of object | Bookings of the start page, one intake payload each (email, name, start_event) for the bundle's `intake_row` block. |
| `start_patches` | list of StageBookingsPatch | With watch_start: rows whose start meeting was cancelled or moved, each patch the whole `Start Event`, for the sync to write after the intake's writes. |
| `start_returns` | list of StageBookingsReturn | With watch_start: rows whose start meeting is cancelled that world.meeting_cancelled (payload `booked_in_stage: start`, `event_id`) moves from where they are now. |
| `booked` | integer | Rows newly booked or moved. |
| `by_name` | integer | Of those, rows matched by name, not email. |
| `unmatched` | integer | Bookings of a stage's page that match no row. |
| `pages` | integer | Titled pages read. |

`StageBookingsPatch`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `patch` | object |  |

`StageBookingsReturn`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `payload` | object |  |

### `feature.chase.stage.check`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.check
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `resolve_scalars` | boolean | no | Default `false`. |
| `fail_step` | boolean | no | Default `false`. |
| `chase_days` | list of number, optional | no |  |
| `chase_grace_days` | number, optional | no |  |
| `max_followups` | integer, optional | no |  |
| `max_age_days` | integer, optional | no |  |
| `window_start` | integer, optional | no |  |
| `window_end` | integer, optional | no |  |
| `window_timezone` | string, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `stages` | list of string |  |
| `gates` | map of string |  |
| `types` | map of list of string |  |
| `needed_by` | map of list of string |  |
| `problems` | list of map of string |  |
| `warnings` | list of map of string |  |
| `summary` | string |  |

### `feature.chase.stage.configure`

One `stage_configure` call: the stage, and any of its settings
(merged onto what is stored, a null key back to the channel's; with
`reset` they replace it whole), copy fields (`copy_fields`, merged into
the stage's layer or, with `copy_layer: shared`, the shared copy) and
note (replaced). The stored settings and the channel-wide mechanics
come along so the output can say what the stage runs on.

```yaml
- id: <step>
  activity: feature.chase.stage.configure
  args:
    stage: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `stage` | string | yes |  |
| `settings` | object, optional | no |  |
| `reset` | boolean | no | Default `false`. |
| `stored_settings` | any | no |  |
| `copy_fields` | object, optional | no |  |
| `copy_layer` | string | no | Default `"stage"`. |
| `guidance` | any | no |  |
| `deadlines` | object, optional | no |  |
| `stored_items` | any | no |  |
| `stored_deadlines` | any | no |  |
| `recipe_document` | string, optional | no |  |
| `dry_run` | boolean | no | Default `false`. |
| `chase_days` | list of number, optional | no |  |
| `chase_grace_days` | number, optional | no |  |
| `max_followups` | integer, optional | no |  |
| `max_age_days` | integer, optional | no |  |
| `window_start` | integer, optional | no |  |
| `window_end` | integer, optional | no |  |
| `window_timezone` | string, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `stage` | string |  |
| `settings_key` | string |  |
| `settings` | object |  |
| `settings_value` | string |  |
| `write_settings` | boolean |  |
| `previous` | any |  |
| `effective` | object |  |
| `inherited` | list of string |  |
| `settings_problem` | string |  |
| `copy_key` | string |  |
| `copy_patch` | object |  |
| `write_copy` | boolean |  |
| `guidance_key` | string |  |
| `guidance` | string |  |
| `write_guidance` | boolean |  |
| `deadlines_key` | string |  |
| `items_key` | string |  |
| `standards_key` | string |  |
| `deadlines` | object |  |
| `deadlines_value` | string |  |
| `write_deadlines` | boolean |  |
| `deadlines_in_force` | object |  |
| `schedule` | list of map of string |  |

### `feature.chase.stage.crash_clear`

A turn that ran to its end: the row's crash count is reset
(`feature.chase.stage.crash_clear`).

```yaml
- id: <step>
  activity: feature.chase.stage.crash_clear
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `cleared` | boolean |  |

### `feature.chase.stage.crashed`

A turn flow's crash, from its `on_failure` hook
(`feature.chase.stage.crashed`).

```yaml
- id: <step>
  activity: feature.chase.stage.crashed
  args:
    conversation_id: <string>
    record_id: <integer>
    flow: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `flow` | string | yes |  |
| `error_type` | string | no | Default `""`. |
| `error_message` | string | no | Default `""`. |
| `failed_step` | string, optional | no |  |
| `limit` | integer | no | Default `3`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `count` | integer |  |
| `fatal` | boolean |  |
| `outcome` | string |  |

### `feature.chase.stage.decision`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.decision
  args:
    context: <object>
    board: <object>
    decision: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `context` | object | yes |  |
| `board` | object | yes |  |
| `decision` | object | yes |  |
| `revision` | object, optional | no |  |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `plan` | object, optional |  |
| `guard_findings` | list of object |  |
| `decision` | object, optional |  |
| `failed` | object, optional |  |

### `feature.chase.stage.deliver`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.deliver
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `weekdays_only` | boolean | no | Default `false`. |
| `excluded_columns` | list of string | no |  |
| `hashed_only_columns` | list of string | no |  |
| `outbound_blocking_columns` | list of string | no |  |
| `author_voice_scalar` | string | no | Default `""`. |
| `author_column` | string | no | Default `""`. |
| `guidance` | map of string | no |  |
| `notes_alias` | map of string | no |  |
| `guidance_override` | map of string | no |  |
| `force` | boolean | no | Default `false`. |
| `start_ends_reminders` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `sent` | boolean |  |
| `event` | string |  |
| `payload` | object |  |
| `guards` | map of list of string |  |
| `why` | map of string |  |
| `stage` | string |  |
| `action` | string |  |
| `turn_key` | string |  |
| `stats` | object |  |

### `feature.chase.stage.due`

`feature.chase.stage.prepare`'s arguments for every row of a tick:
the policy, columns and guidance the turn flow hands prepare, over the
routed `turns`. They must be the same arguments, or the fingerprint
differs and every row launches (the bundle's tests hold the two steps
together).

```yaml
- id: <step>
  activity: feature.chase.stage.due
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | no | Default `0`. |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `weekdays_only` | boolean | no | Default `false`. |
| `excluded_columns` | list of string | no |  |
| `hashed_only_columns` | list of string | no |  |
| `outbound_blocking_columns` | list of string | no |  |
| `author_voice_scalar` | string | no | Default `""`. |
| `author_column` | string | no | Default `""`. |
| `guidance` | map of string | no |  |
| `notes_alias` | map of string | no |  |
| `guidance_override` | map of string | no |  |
| `force` | boolean | no | Default `false`. |
| `start_ends_reminders` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |
| `turns` | list of object | no |  |
| `flows` | list of string | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `turns` | list of object |  |
| `candidates` | integer |  |
| `launched` | integer |  |
| `skipped` | map of integer |  |
| `uncertain` | integer |  |
| `seeded` | integer |  |

### `feature.chase.stage.eval`

The chase's half of the platform eval (`feature.evals.*`): `check`
holds a planned run's cases to the graph before it opens; `assess`
flattens one turn's plan into what the runner scores; `process` names
the revision the run is pinned to, for a turn the bundle scores;
`stages` summarises the pinned process's stages for the seed block.

```yaml
- id: <step>
  activity: feature.chase.stage.eval
  args:
    conversation_id: <string>
    operation: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `operation` | string | yes |  |
| `cases` | list of object | no |  |
| `case` | object, optional | no |  |
| `ready` | boolean | no | Default `true`. |
| `context` | object, optional | no |  |
| `plan` | object, optional | no |  |
| `models` | object, optional | no |  |
| `trace` | object, optional | no |  |
| `event` | string | no | Default `""`. |
| `payload` | object | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `count` | integer |  |
| `summary` | string |  |
| `model` | string |  |
| `actual` | object, optional |  |
| `problems` | list of string |  |
| `handled_keys` | list of string |  |
| `failures` | list of string |  |
| `trace` | object |  |
| `reason` | string |  |
| `extra_columns` | object |  |
| `event` | string |  |
| `landing` | string |  |
| `landing_detail` | string |  |
| `process` | string |  |
| `stages` | object |  |

### `feature.chase.stage.fatal_report`

The support team's email about a Fatal error row
(`feature.chase.stage.fatal_report`), composed for
`feature.email.send`.

```yaml
- id: <step>
  activity: feature.chase.stage.fatal_report
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `recipients` | list of string | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `to` | list of string |  |
| `subject` | string |  |
| `body` | string |  |

### `feature.chase.stage.fatal_retry`

Fatal rows given a fresh turn once a newer bundle version is
installed (`feature.chase.stage.fatal_retry`).

```yaml
- id: <step>
  activity: feature.chase.stage.fatal_retry
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `cap` | integer | no | Default `20`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `record_ids` | list of integer |  |

### `feature.chase.stage.hold`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.hold
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `record_id` | integer | no | Default `0`. |
| `turn_key` | string | no | Default `""`. |
| `event` | string | no | Default `""`. |
| `payload` | object | no |  |
| `enabled` | boolean | no | Default `true`. |
| `envelope_column` | string | no | Default `"DocumentId"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `held` | boolean |  |
| `stage` | string |  |
| `launches` | list of object |  |
| `release_at` | string |  |

### `feature.chase.stage.items`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.items
  args:
    stage: <string>
    source_text: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `stage` | string | yes |  |
| `source_text` | string | yes |  |
| `questions` | list of string | no |  |
| `validation` | list of object | no |  |
| `kind` | string | no | Default `"question"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `stage` | string |  |
| `item_set` | object |  |
| `scalar_key` | string |  |
| `standards_key` | string |  |
| `guidance_key` | string |  |
| `copy_key` | string |  |
| `shared_copy_key` | string |  |
| `settings_key` | string |  |
| `step_id` | string |  |
| `stage_type` | string |  |

### `feature.chase.stage.models`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.models
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `override` | string | no | Default `""`. |
| `chase_type` | string | no | Default `""`. |
| `stage_models` | map of string | no |  |
| `stage_settings` | any | no |  |
| `agent_model` | string | no | Default `""`. |
| `validator_model` | string | no | Default `""`. |
| `writer_model` | string | no | Default `""`. |
| `reviewer_model` | string | no | Default `""`. |
| `reader_model` | string | no | Default `""`. |
| `role_models` | map of string | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `validator` | string |  |
| `writer` | string |  |
| `reviewer` | string |  |
| `reader` | string |  |
| `by_role` | map of string |  |
| `requested` | list of string |  |
| `summary` | string |  |

### `feature.chase.stage.pregenerate`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.pregenerate
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `record_ids` | list of integer | no |  |
| `cap` | integer | no | Default `10`. |
| `envelope_column` | string | no | Default `"DocumentId"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `launches` | list of object |  |
| `considered` | integer |  |
| `releases` | list of integer |  |
| `next_release_at` | string |  |
| `skipped` | map of integer |  |

### `feature.chase.stage.prepare`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.prepare
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `max_followups` | integer | no | Default `10`. |
| `max_age_days` | integer | no | Default `30`. |
| `window_start` | integer | no | Default `8`. |
| `window_end` | integer | no | Default `18`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `chase_days` | list of number | no |  |
| `chase_grace_days` | number | no | Default `14.0`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `ignore_window` | boolean | no | Default `false`. |
| `weekdays_only` | boolean | no | Default `false`. |
| `excluded_columns` | list of string | no |  |
| `hashed_only_columns` | list of string | no |  |
| `outbound_blocking_columns` | list of string | no |  |
| `author_voice_scalar` | string | no | Default `""`. |
| `author_column` | string | no | Default `""`. |
| `guidance` | map of string | no |  |
| `notes_alias` | map of string | no |  |
| `guidance_override` | map of string | no |  |
| `force` | boolean | no | Default `false`. |
| `start_ends_reminders` | boolean | no | Default `false`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ready` | boolean |  |
| `crashes` | boolean |  |
| `needs_agent` | boolean |  |
| `context` | object |  |
| `plan` | object |  |
| `expected_revision` | integer |  |
| `fingerprint` | string |  |
| `turn_key` | string |  |
| `stage` | string |  |
| `event_kind` | string |  |
| `reason` | string |  |
| `bundle_guidance` | map of string |  |
| `process_guidance` | map of string |  |
| `stage_guidance` | map of string |  |
| `channel_notes` | map of string |  |
| `guidance_rev` | string |  |
| `pending_event` | string |  |
| `pending_payload` | object |  |
| `pending_why` | object |  |
| `pending_writes` | object |  |
| `chase_type` | string |  |
| `roles` | map of map of string |  |
| `validates` | boolean |  |
| `stage_models` | map of string |  |
| `deliver_pending` | boolean |  |
| `deadlines` | object, optional |  |
| `deadline` | object |  |

### `feature.chase.stage.readback`

The covered rows as they stand after their turns
(`feature.chase.stage.readback`).

```yaml
- id: <step>
  activity: feature.chase.stage.readback
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `turns` | list of object | no |  |
| `ran` | list of object, optional | no |  |
| `results` | map of list of any, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `checked` | list of object |  |
| `not_finished` | list of integer |  |
| `turn` | object, optional |  |
| `row_now` | string, optional |  |

### `feature.chase.stage.recipients`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.recipients
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `show` | string | no | Default `"wants_call"`. |
| `stage` | string, optional | no | Default `""`. |
| `items` | any | no |  |
| `question` | string, optional | no | Default `""`. |
| `include_closed` | boolean | no | Default `false`. |
| `limit` | integer | no | Default `50`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `refusal` | object, optional |  |
| `show` | string |  |
| `stage` | string |  |
| `question` | object, optional |  |
| `total` | integer |  |
| `shown` | integer |  |
| `rows` | list of object |  |
| `summary` | string |  |

### `feature.chase.stage.record`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.record
  args:
    conversation_id: <string>
    record_id: <integer>
    turn_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `turn_key` | string | yes |  |
| `stage` | string | no | Default `""`. |
| `mode` | string | no | Default `"prod"`. |
| `event_kind` | string | no | Default `""`. |
| `fingerprint` | string | no | Default `""`. |
| `guidance_rev` | string | no | Default `""`. |
| `models` | object | no |  |
| `started_at` | string | no | Default `""`. |
| `case_name` | string | no | Default `""`. |
| `trace` | object, optional | no |  |
| `apply` | object, optional | no |  |
| `transition` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `turn_row` | string |  |
| `decisions` | integer |  |
| `pending_cleared` | boolean |  |
| `transition_outcome` | string |  |

### `feature.chase.stage.reject`

`feature.chase.stage.reject`: send the recipe's rejection email to
one row that stands on a rejecting state. `outbound_blocking_columns`
is the turn's list, so a row the stage would not email is not emailed
here either.

```yaml
- id: <step>
  activity: feature.chase.stage.reject
  args:
    conversation_id: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `record_id` | integer | yes |  |
| `outbound_blocking_columns` | list of string | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `outcome` | string |  |
| `sent` | boolean |  |
| `sent_at` | string |  |
| `subject` | string |  |
| `message_id` | string |  |
| `reason` | string |  |

### `feature.chase.stage.release`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.release
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `record_id` | integer | no | Default `0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `held` | boolean |  |
| `stage` | string |  |
| `due` | boolean |  |
| `flow` | string |  |

### `feature.chase.stage.reminders`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.reminders
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `rows` | list of object, optional | no | The tracker's rows, with `_record_id`, the stored machine columns, the booking columns and `Agent Intake`. Omitted: the activity reads the whole tracker itself (`channel_rows`), so no row list rides in the flow's history. |
| `app_mode` | string | no | Default `""`. |
| `test_day_seconds` | integer | no | Default `60`. |
| `min_ahead_seconds` | integer | no | Default `60`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `due` | list of integer | Rows with a reminder due now, in row order. |
| `next` | string | The earliest instant the tick should fire again (RFC3339): the floor while a reminder is due unsent, else the next one ahead; "" when none is due or ahead. |
| `on_stage` | integer | Rows on a reminder stage with a meeting. |

### `feature.chase.stage.resolve`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.resolve
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `stage` | string | no | Default `""`. |
| `chase_type` | string | no | Default `""`. |
| `optional` | boolean | no | Default `false`. |
| `record_id` | integer | no | Default `0`. |
| `from_row` | boolean | no | Default `false`. |
| `with_copy` | boolean | no | Default `false`. |
| `envelope_column` | string | no | Default `"DocumentId"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `stage` | string |  |
| `chase_type` | string |  |
| `label` | string |  |
| `chase` | object |  |
| `keys` | map of string |  |
| `step_id` | string |  |
| `roles` | map of string |  |
| `leaving` | string |  |
| `stage_from` | string |  |
| `retire` | boolean |  |
| `row_rev` | integer |  |
| `stage_copy` | map of string |  |
| `vocabulary` | map of string |  |

### `feature.chase.stage.review`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.review
  args:
    context: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `operation` | string | no | Default `"review"`. |
| `context` | object | yes |  |
| `decision` | object, optional | no |  |
| `plan` | object, optional | no |  |
| `review` | object, optional | no |  |
| `guard_findings` | list of object | no |  |
| `rounds` | list of object | no |  |
| `candidates` | list of object | no |  |
| `attempt` | integer | no | Default `1`. |
| `max_attempts` | integer | no | Default `4`. |
| `eval_case` | object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `verdict` | string, optional |  |
| `blocking` | integer |  |
| `findings` | list of object |  |
| `rounds` | list of object |  |
| `candidates` | list of object |  |
| `approved_plan` | object, optional |  |
| `revision` | object, optional |  |
| `plan` | object, optional |  |
| `failed` | object, optional |  |

### `feature.chase.stage.select`

The rows a "check now" run covers (`feature.chase.stage.select`):
named by record id, or by one of `feature.chase.stage.recipients`'
shows over the tracker. Both blank covers no row.

```yaml
- id: <step>
  activity: feature.chase.stage.select
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `record_id` | integer, optional | no | Default `0`. |
| `record_ids` | list of any, optional | no |  |
| `show` | string, optional | no | Default `""`. |
| `stage` | string, optional | no | Default `""`. |
| `items` | any | no |  |
| `question` | string, optional | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `refusal` | object, optional |  |
| `mode` | string |  |
| `ids` | list of integer |  |
| `turns` | list of object |  |
| `by_flow` | map of integer |  |
| `missing` | list of integer |  |
| `summary` | string |  |

### `feature.chase.stage.setting`

One recipe setting's value for the channel
(`feature.chase.stage.setting`): checked against the declaration in
the recipe's `settings:`, stored in its own `chase.setting.<name>`.

```yaml
- id: <step>
  activity: feature.chase.stage.setting
  args:
    name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `name` | string | yes |  |
| `value` | any | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `name` | string |  |
| `previous` | any |  |
| `value` | any |  |
| `text` | string |  |
| `scalar` | string |  |
| `declared` | object |  |
| `step_id` | string |  |

### `feature.chase.stage.setup`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.setup
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `mode` | `ensure` / `compose` | no | Default `"ensure"`. |
| `force` | boolean | no | Default `false`. |
| `resolve_scalars` | boolean | no | Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `steps` | list of object |  |
| `required` | list of string |  |
| `satisfied` | list of string |  |
| `marked` | list of string |  |
| `unmapped` | list of string |  |
| `documents` | list of object |  |
| `deadlines` | list of object |  |
| `key` | object |  |
| `cached` | boolean |  |
| `written` | boolean |  |
| `summary` | string |  |

### `feature.chase.stage.stamp`

Lay a row's declared dates on its stages as `apply` would after a
commit (`feature.chase.stage.stamp`): for a row whose stages' state
was written by something other than a commit (a seeded test
recipient). With `stage`, `date_name` and `at`, a date a person gave
is recorded on that stage first (the day a notice the carrier never
scanned was mailed), and the declared dates are worked out from it.

```yaml
- id: <step>
  activity: feature.chase.stage.stamp
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `record_id` | integer | no | Default `0`. |
| `stage` | string | no | Default `""`. |
| `date_name` | string | no | Default `""`. |
| `at` | string | no | Default `""`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `stamped` | map of list of string |  |
| `given` | string |  |
| `written` | boolean |  |
| `wait` | object |  |

### `feature.chase.stage.standards`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.standards
  args:
    operation: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `operation` | string | yes |  |
| `item_set` | any | no |  |
| `existing` | any | no |  |
| `drafts` | any | no |  |
| `ids` | list of string | no |  |
| `effective_from` | string | no | Default `""`. |
| `item` | string | no | Default `""`. |
| `date_precision` | string, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `questions` | list of string |  |
| `ids` | list of string |  |
| `count` | integer |  |
| `skipped` | string |  |
| `patch` | object |  |
| `drafted` | integer |  |
| `gaps` | integer |  |
| `precision_before` | string |  |
| `precision` | string |  |

### `feature.chase.stage.start`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.start
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `kind` | string | webhook or calendar. |
| `link` | string | A calendar start's page scalar key. |
| `declared` | boolean | The document declares a `start:`; False means the webhook default. |
| `step_id` | string | The checklist step that offers the start. |
| `webhook` | boolean | The recipe starts by webhook. |

### `feature.chase.stage.stats`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.stats
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `write` | boolean | no | Default `true`. |
| `record_id` | integer, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `stats` | object |  |
| `lead` | list of object, optional |  |
| `changed` | boolean |  |
| `written` | boolean |  |
| `summary` | string |  |

### `feature.chase.stage.turns`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.turns
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `rows` | list of object, optional | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `turns` | list of object |  |
| `by_flow` | map of integer |  |
| `lapsed_park` | list of integer |  |
| `lapsed_park_writes` | object |  |
| `lapsed_release` | list of integer |  |

### `feature.chase.stage.types`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.types
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `types` | list of object |  |
| `in_use` | map of list of string |  |

### `feature.chase.stage.unhold`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.chase.stage.unhold
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `record_ids` | list of integer | no |  |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `cleared` | list of integer |  |

### `feature.chase.stage.wait`

One row's wait (`feature.chase.stage.wait`): the date its wait
stage names, read against the row; or, with `ref`, any date rule
(`notice.demand_date`) read against the row, for a flow that writes
the date somewhere (`due_date_set`); or, with `key`, the rule the
row's stage keeps under that key (`shipment_turn`'s `deliver_by`).

```yaml
- id: <step>
  activity: feature.chase.stage.wait
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `record_id` | integer | no | Default `0`. |
| `ref` | string | no | Default `""`. |
| `key` | string | no | Default `""`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `applies` | boolean |  |
| `reason` | string |  |
| `stage` | string |  |
| `status` | string |  |
| `reading` | string |  |
| `until` | string |  |
| `until_at` | string |  |
| `certainty` | string |  |
| `why` | string |  |
| `commit` | boolean |  |
| `evidence` | object |  |
| `patch` | object |  |
| `write_until` | boolean |  |
| `rev` | integer |  |
| `why_by_row` | map of string |  |

### `feature.chase.stage.waits`

Every row on a wait stage (`feature.chase.stage.waits`), for the
tick's projection.

```yaml
- id: <step>
  activity: feature.chase.stage.waits
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `window_timezone` | string | no | Default `"America/Los_Angeles"`. |
| `app_mode` | string | no | Default `"prod"`. |
| `test_day_seconds` | integer | no | Default `60`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `why` | map of string |  |
| `rows` | integer |  |

## feature.draft

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

## feature.email

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

## feature.esign.document

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

## feature.evals

### `feature.evals.launched`

After the turns: record which of the planned turns the driver got
away, and write the terminal history row of every turn that failed
before it could score.

```yaml
- id: <step>
  activity: feature.evals.launched
  args:
    conversation_id: <string>
    run_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `run_id` | string | yes |  |
| `keys` | list of string | no | `$steps.<open>.output.keys`. |
| `cases` | list of object | no | `$steps.<open>.output.rows`: one `{Name, Rep}` per turn, all this step reads. The cases whole work too, at their weight beside every turn's output in one payload. |
| `started` | any | no | `$steps.<turns>.output`: one slot per case in the plan's order, null where the turn was skipped. |
| `error` | any | no | `$steps.<turns>.error`: the first failure the foreach absorbed. |
| `groups` | list of object | no | Further `{keys, cases, started}` triples, one per foreach the driver ran beside the first (a bundle with several kinds of case); read as one run. |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `run_id` | string |  |
| `started` | integer |  |
| `not_started` | list of string |  |
| `summary` | string |  |

### `feature.evals.mark`

A turn's first act: stamp the case's row `running` under the
turn's Run Id and repetition, and open the turn's own row in
`eval_results`. A board row that already carries a finished result
of this run is left as it is (the board keeps the run's worst).

```yaml
- id: <step>
  activity: feature.evals.mark
  args:
    conversation_id: <string>
    case: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `case` | object | yes |  |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `guidance_rev` | string | no | Default `""`. |
| `extra_columns` | object | no | The bundle's own columns to clear on the board row, e.g. where the LAST run's decision landed. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `result_id` | string |  |
| `started_at` | string |  |
| `summary` | string |  |

### `feature.evals.open`

Open the run `feature.evals.plan` planned: rebuild the seeds
from the bundle's cases against the board as it is now and write
them with the error stamps, open the run's row in `eval_runs`, and
delete the history rows the plan named. Refuses a bundle whose eval
tables lack the runner's core columns, naming them.

```yaml
- id: <step>
  activity: feature.evals.open
  args:
    conversation_id: <string>
    plan: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `plan` | object | yes | `$steps.<plan>.output.opening`. The whole plan output is accepted too, at the cost of carrying the selection twice. |
| `cases` | list of object, optional | no | The cases the bundle ships (`$steps.seed.output.cases`, the same list `plan` took): the seeds are rebuilt here, not carried over from the plan. Left out only by a driver pinned before its bundle passed them, whose plan carries `launch`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `run_id` | string |  |
| `seeded` | integer |  |
| `skipped` | list of string | Launch rows left alone because a newer run claimed the case between the plan and this open. |
| `edited` | list of string | Seeds left alone because the firm edited the row between the plan and this open (a reseeding run writes anyway). |
| `pruned` | integer |  |
| `cases` | list of object | The run to drive: the selected cases from the board as it is now, one per repetition, with their Run Id and Rep. Empty when the plan named `kinds`: the run is then under `by_kind`, and only there, so the result carries each case once. |
| `keys` | list of string | One key per case, `Name` or `Name#rep`; empty when the plan named `kinds`, like `cases`. |
| `rows` | list of object | One `{Name, Rep}` per turn, in `cases` order: what `launched` takes as its `cases`, so the corpus does not ride through that step beside every turn's output. Empty when the plan named `kinds`, like `cases`. |
| `by_kind` | map of object | `{kind: {cases, keys, rows}}` for every kind the plan named, so a driver runs `$steps.<open>.output.by_kind.<kind>.cases` and accounts with `.keys` and `.rows`; empty when it named none. |
| `names` | list of string |  |
| `count` | integer |  |
| `turns` | integer |  |
| `payload_bytes` | integer | The size of this result on the wire, against the runner's PAYLOAD_BUDGET. |
| `summary` | string |  |

### `feature.evals.plan`

Plan one eval run, writing nothing: seed the bundle's cases the
channel lacks, refresh the shipped rows nobody edited when the bundle
moved, select by `only` and multiply by `reps`, and name the
history rows a later `open` prunes. Hand the output to
`feature.evals.open` once the bundle's own check has passed the
selection.

```yaml
- id: <step>
  activity: feature.evals.plan
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `cases` | list of object | no | The cases the bundle ships (its seed block's output). Every key a case carries is a fixture column of `eval_cases`. |
| `run_id` | string | no | `$trigger.run_id`: the workflow's Temporal run id, of which eight hex make the launch time unique. Default `""`. |
| `only` | string | no | A substring of a case's Name or Section, or a comma-separated list of them; every case any term matches runs. Default `""`. |
| `reseed` | boolean | no | Replace the rows the firm edited with the bundle's shipped cases too. Default `false`. |
| `reps` | integer | no | Run every selected case this many times under one Run Id, at most ten. Default `1`. |
| `kinds` | list of string | no | The flows the bundle runs its cases as, by the row's `Kind`; the output groups the cases under `by_kind`, every kind present. Leave empty when every case runs as one flow. |
| `default_kind` | string | no | What a blank `Kind` reads as, e.g. `intake`. Default `""`. |
| `stamp_columns` | list of string | no | The bundle's own result columns on `eval_cases` (where a decision landed, e.g. `Event`, `Funnel State`): never handed to a turn as fixture. |

**Returns**

One copy of the selection (`cases`, for the bundle's check) and
the small `opening` that `feature.evals.open` takes. The rows to
seed are not here: `open` rebuilds them from the bundle's seeds and
the board. A plan's result is one Temporal payload, and the corpus
goes through it once (`payload_bytes` says how much of the budget).

| Field | Type | Notes |
|---|---|---|
| `run_id` | string |  |
| `cases` | list of object | The selection, one per repetition, for the bundle's check; the driver runs `open`'s. |
| `opening` | object | What `feature.evals.open` takes as `plan`: the run id and row, the names, the prune, the settings. Never the cases. |
| `run_row` | object |  |
| `prune` | list of integer |  |
| `keys` | list of string |  |
| `launch` | list of object | Only for a driver pinned before its bundle passed the seeds to `open` (SEEDS_TO_OPEN_SINCE): the rows to seed, as that driver's `open` reads them from the plan. Empty otherwise. |
| `by_kind` | map of object | Only for such a driver, likewise: the selection by kind. Empty otherwise; a current driver runs `open`'s. |
| `reseed` | boolean |  |
| `fields` | list of string |  |
| `stamp_columns` | list of string |  |
| `kinds` | list of string |  |
| `default_kind` | string |  |
| `names` | list of string |  |
| `count` | integer |  |
| `turns` | integer |  |
| `reps` | integer |  |
| `seeded` | integer |  |
| `refreshed` | list of string |  |
| `stale` | list of string |  |
| `unfinished` | list of string |  |
| `payload_bytes` | integer | The size of this result on the wire, against the runner's PAYLOAD_BUDGET; the plan refuses over it, naming the count that fits. |
| `summary` | string |  |

### `feature.evals.reconcile`

The run's own pass over its roll-up once every turn is done: the
same merge the turns make, with no turn of its own, so a run with a
lost turn still reads complete.

```yaml
- id: <step>
  activity: feature.evals.reconcile
  args:
    conversation_id: <string>
    run_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `run_id` | string | yes |  |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `recompute_on_stale` | integer | no | Default `5`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `run_id` | string |  |
| `rollup` | object |  |
| `summary` | string |  |

### `feature.evals.rollup`

Fold this turn's result into the run's row in `eval_runs`, under
the revision it read, re-reading on a conflict: the counts, the
rounds, the flaky cases, the handoffs, and the run before it.

```yaml
- id: <step>
  activity: feature.evals.rollup
  args:
    conversation_id: <string>
    case: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `case` | object | yes |  |
| `result` | string | no | Default `""`. |
| `rounds` | integer | no | Default `0`. |
| `reason` | string | no | Default `""`. |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `guidance_rev` | string | no | Default `""`. |
| `recompute_on_stale` | integer | no | Default `5`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `run_id` | string |  |
| `rollup` | object |  |
| `summary` | string |  |

### `feature.evals.score`

A turn's last act: compare `actual` with the row's `Expect`,
fold in the problems the bundle's own scorer found, and write the
verdict twice: to the turn's row in `eval_results` (never
overwritten) and to the case's row on the board (this run's worst).
A turn a newer run overtook is `superseded` and writes only its
history row, `Counted: false`.

```yaml
- id: <step>
  activity: feature.evals.score
  args:
    conversation_id: <string>
    case: <object>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `now` | string | no | The flow's clock (`foundation.workflow.now`), so a run's rows agree on the instant. The wall clock when blank. Default `""`. |
| `case` | object | yes |  |
| `ready` | boolean | no | Default `true`. |
| `actual` | object, optional | no | The decision, flat: every key `Expect` may name, plus `rounds` and `body`. Stored as Decision (minus `body`) and Draft. |
| `problems` | list of string | no | What the bundle's own scorer found wrong. |
| `handled_keys` | list of string | no | The `Expect` keys the bundle's scorer compared itself; any other key the runner does not know fails the case. |
| `failures` | list of string | no | Steps that failed softly in the turn; any makes the case an error with them as its Detail. |
| `trace` | object, optional | no |  |
| `reason` | string | no | Why the case's row would land on a person, blank otherwise; what the run's Handoff Reasons count. Default `""`. |
| `extra_columns` | object | no | The bundle's own columns for the board and history rows, e.g. where the decision would land. |
| `model` | string, optional | no | The model the turn ran on, for the row; null (a skipped models step) reads as blank. Default `""`. |
| `guidance_rev` | string | no | Default `""`. |
| `started_at` | string | no | Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `result` | string |  |
| `result_id` | string |  |
| `rounds` | integer |  |
| `problems` | list of string |  |
| `summary` | string |  |

## feature.gcal

### `feature.gcal.cancel_event`

Cancel an event on the bound Google account's calendar.

Carry `integration_id` (inherited from ActivityInput, normally
`$channel.integrations.gcal.id`) so the identity binding swaps
the auth to the bound Google account before the write.

```yaml
- id: <step>
  activity: feature.gcal.cancel_event
  args:
    event_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `event_id` | string | yes | Calendar event id to cancel. |
| `calendar_id` | string | no | Calendar holding the event. Empty means the bound account's primary calendar. Default `""`. |
| `send_updates` | string | no | Who Google emails the cancellation: all / externalOnly / none. Default `"all"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `event_id` | string | Cancelled event id. |
| `cancelled` | boolean | True when the cancel succeeded. |
| `message` | string | Provider confirmation. |

### `feature.gcal.format_availability`

Render slots/candidates into a message body.

Carries no `integration_id`: this step touches no account.

```yaml
- id: <step>
  activity: feature.gcal.format_availability
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `candidates` | list of object, optional | no | Ranked candidates from merge_free_times ({start, preferred}). Preferred ones are called out first. |
| `slots` | list of object, optional | no | Free ranges, used only when there are no discrete candidates (granularity_minutes: 0). |
| `calendars_checked` | list of string, optional | no | Calendars backing the answer — named in the message so the reader knows whose availability this is. |
| `unknown` | list of string, optional | no | Calendars that couldn't be read; each is caveated. |
| `note` | string | no | A reason there is no answer at all (e.g. no calendar connected). When set it REPLACES the times — there is nothing to list — so it must be fit to show a user. Default `""`. |
| `timezone` | string | no | IANA zone the times are written in. Default `"UTC"`. |
| `duration_minutes` | integer | no | Meeting length, named in the header. Default `30`. |
| `granularity_minutes` | integer | no | The policy's start-time alignment. Non-zero means the answer IS the candidate list: free ranges are then working material, not offers, and are never shown. 0 means slicing is off and the ranges are all there is. Default `0`. |
| `heading` | string | no | First line of the message. Default `"Open times"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `text` | string | Message body, plain text. |
| `listed` | integer | How many times the message names. |

### `feature.gcal.list_changes`

Read what changed on a calendar the bound account can read.

Carry `integration_id` (inherited from ActivityInput, normally
`$channel.integrations.gcal.id`) so the identity binding swaps
the auth to the bound Google account before the read.

```yaml
- id: <step>
  activity: feature.gcal.list_changes
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `calendar_id` | string | no | Calendar to watch (email address / calendar id). Empty means the bound account's primary calendar. Keep it the same for every call with one cursor. Default `""`. |
| `cursor` | string | no | The cursor the previous call returned. Empty primes: no events come back, only a cursor to start from. Default `""`. |
| `max_results` | integer | no | Most changed events one call returns; `more` is set when there are others to read now. Default `100`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `events` | list of GcalEventSummary | Events created, updated or cancelled since the cursor. |
| `count` | integer | Number of events returned. |
| `cursor` | string | Store this and pass it on the next call. |
| `more` | boolean | True when further changes are ready now: call again with `cursor` before waiting. |
| `primed` | boolean | True when this call started a new cursor (empty input cursor, or `reset`); it returns no events. |
| `reset` | boolean | True when the input cursor had expired and a new one was primed: changes since the old cursor are lost, reconcile from a read of your own. |

`GcalAttachment`:

| Field | Type | Notes |
|---|---|---|
| `file_id` | string | Drive file id. |
| `title` | string | File title (capped at 200 chars), e.g. '… - Notes by Gemini' or '… - Transcript'. |
| `mime_type` | string | The file's MIME type. |

`GcalAttendee`:

| Field | Type | Notes |
|---|---|---|
| `email` | string | Attendee email. |
| `display_name` | string | Attendee name, if set. |
| `response_status` | string | needsAction / declined / tentative / accepted. |
| `organizer` | boolean | True for the event's organizer. |

`GcalBookedBy`:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Booker's name as entered. |
| `email` | string | Booker's email as entered. |
| `source` | string | calcom for a booking Cal.com wrote onto the calendar; empty for a Google appointment schedule's. |

`GcalEventSummary`:

| Field | Type | Notes |
|---|---|---|
| `event_id` | string | Calendar event id. |
| `summary` | string | Event title. |
| `start` | string | RFC3339 dateTime, or YYYY-MM-DD for all-day events. |
| `end` | string | RFC3339 dateTime, or YYYY-MM-DD for all-day events. |
| `html_link` | string | Link to the event. |
| `status` | string | confirmed / tentative / cancelled. |
| `organizer` | string | Organizer email. |
| `description` | string | Event description (capped at 2000 chars). |
| `location` | string | Event location. |
| `creator` | string | Creator email. |
| `created` | string | RFC3339 time the event was created. |
| `updated` | string | RFC3339 time the event last changed. |
| `recurring_event_id` | string | The series id when this is one instance of a recurring event. |
| `conference_url` | string | Video call link (Google Meet), if any. |
| `conference_id` | string | The call's id apart from its link: a Google Meet meeting code, or the id a conferencing add-on (Teams, Zoom) gives it. |
| `attachments` | list of GcalAttachment | Files attached to the event (the first 5): Gemini notes, transcripts, recordings, agendas. |
| `attendees` | list of GcalAttendee | Invited attendees (the first 10 on list and change reads; see attendee_count). |
| `attendee_count` | integer | How many attendees the event has in all. |
| `booked_by` | GcalBookedBy, optional | Set when the event was booked through a Google appointment schedule: the booker's name and email from the 'Booked by' block Google writes into the description. |
| `visibility` | string | default / public / private / confidential. Empty when the proxy did not say: treat the event as private. |
| `transparency` | string | opaque (blocks time) / transparent (shows as free). Empty when the proxy did not say. |
| `event_type` | string | default / outOfOffice / focusTime / workingLocation / … (Google's eventType). Empty when the proxy did not say. |

### `feature.gcal.list_events`

List events on a calendar the bound Google account can read.

Carry `integration_id` (inherited from ActivityInput, normally
`$channel.integrations.gcal.id`) so the identity binding swaps
the auth to the bound Google account before the read.

```yaml
- id: <step>
  activity: feature.gcal.list_events
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `calendar_id` | string | no | Calendar to read (email address / calendar id). Empty means the bound account's primary calendar. Default `""`. |
| `time_min` | string | no | RFC3339 lower bound (inclusive). Empty = unbounded. Default `""`. |
| `time_max` | string | no | RFC3339 upper bound (exclusive). Empty = unbounded. Default `""`. |
| `max_results` | integer | no | Maximum events to return. Default `50`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `events` | list of GcalEventSummary | Events in the window. |
| `count` | integer | Number of events returned. |

`GcalAttachment`:

| Field | Type | Notes |
|---|---|---|
| `file_id` | string | Drive file id. |
| `title` | string | File title (capped at 200 chars), e.g. '… - Notes by Gemini' or '… - Transcript'. |
| `mime_type` | string | The file's MIME type. |

`GcalAttendee`:

| Field | Type | Notes |
|---|---|---|
| `email` | string | Attendee email. |
| `display_name` | string | Attendee name, if set. |
| `response_status` | string | needsAction / declined / tentative / accepted. |
| `organizer` | boolean | True for the event's organizer. |

`GcalBookedBy`:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Booker's name as entered. |
| `email` | string | Booker's email as entered. |
| `source` | string | calcom for a booking Cal.com wrote onto the calendar; empty for a Google appointment schedule's. |

`GcalEventSummary`:

| Field | Type | Notes |
|---|---|---|
| `event_id` | string | Calendar event id. |
| `summary` | string | Event title. |
| `start` | string | RFC3339 dateTime, or YYYY-MM-DD for all-day events. |
| `end` | string | RFC3339 dateTime, or YYYY-MM-DD for all-day events. |
| `html_link` | string | Link to the event. |
| `status` | string | confirmed / tentative / cancelled. |
| `organizer` | string | Organizer email. |
| `description` | string | Event description (capped at 2000 chars). |
| `location` | string | Event location. |
| `creator` | string | Creator email. |
| `created` | string | RFC3339 time the event was created. |
| `updated` | string | RFC3339 time the event last changed. |
| `recurring_event_id` | string | The series id when this is one instance of a recurring event. |
| `conference_url` | string | Video call link (Google Meet), if any. |
| `conference_id` | string | The call's id apart from its link: a Google Meet meeting code, or the id a conferencing add-on (Teams, Zoom) gives it. |
| `attachments` | list of GcalAttachment | Files attached to the event (the first 5): Gemini notes, transcripts, recordings, agendas. |
| `attendees` | list of GcalAttendee | Invited attendees (the first 10 on list and change reads; see attendee_count). |
| `attendee_count` | integer | How many attendees the event has in all. |
| `booked_by` | GcalBookedBy, optional | Set when the event was booked through a Google appointment schedule: the booker's name and email from the 'Booked by' block Google writes into the description. |
| `visibility` | string | default / public / private / confidential. Empty when the proxy did not say: treat the event as private. |
| `transparency` | string | opaque (blocks time) / transparent (shows as free). Empty when the proxy did not say. |
| `event_type` | string | default / outOfOffice / focusTime / workingLocation / … (Google's eventType). Empty when the proxy did not say. |

### `feature.gcal.merge_free_times`

Intersect the collected per-account busy reads into open slots.

Pass `reads` the `collect:`ed output of the read_busy fan-out and
`policy` the resolved rules. Carries no `integration_id`: this
step touches no account.

```yaml
- id: <step>
  activity: feature.gcal.merge_free_times
  args:
    time_min: <string>
    time_max: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `reads` | list of object | no | Collected feature.gcal.read_busy outputs — each carries `busy` and `calendars`. |
| `policy` | SchedulePolicy | no | Resolved scheduling rules from feature.gcal.resolve_schedule_policy. |
| `time_min` | string | yes | RFC3339 window start — the SAME frozen bound the reads used (plan_availability's output). |
| `time_max` | string | yes | RFC3339 window end. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `slots` | list of GcalMergedSlot | Maximal free ranges (>= duration_minutes) where every calendar read is free and no policy rule applies, earliest first. |
| `candidates` | list of GcalCandidate | Discrete offerable start times sliced from those ranges, preferred hours first then chronological. Empty when granularity_minutes is 0. |
| `calendars_checked` | list of string | Calendars whose busy data backs these slots. |
| `unknown` | list of string | Calendars that came back unreadable (only possible from a read_busy with require_all False). These availabilities are NOT accounted for. |
| `all_visible` | boolean | True if every calendar read was visible. When False, caveat proposed times. |

`GcalCandidate`:

| Field | Type | Notes |
|---|---|---|
| `start` | string | Offerable meeting start, RFC3339. |
| `preferred` | boolean | True when this start falls inside one of the policy's preferred_hours windows. Preferred candidates are listed first. |

`GcalMergedSlot`:

| Field | Type | Notes |
|---|---|---|
| `start` | string | Free range start, RFC3339. |
| `end` | string | Free range end, RFC3339. |

`SchedulePolicy`:

| Field | Type | Notes |
|---|---|---|
| `timezone` | string | IANA zone every time-of-day rule below is read in, and the zone all-day events are localized in. |
| `weekdays` | list of string | Days that can hold a meeting (mon…sun). Days left out are blocked whole. |
| `working_hours` | TimeWindow | The daily window meetings may fall in. HARD. |
| `blocked_times` | list of TimeWindow | Recurring daily windows never to book (lunch, a standing stand-up). HARD. |
| `preferred_hours` | list of TimeWindow | Windows to offer FIRST when available. SOFT — ranking only, never a filter. |
| `duration_minutes` | integer | Meeting length. |
| `granularity_minutes` | integer | Start times are aligned to this many minutes past the local hour (30 -> :00 and :30). 0 disables slicing, leaving only the free ranges. |
| `buffer_minutes` | integer | Padding kept either side of an EXISTING meeting, so a call never starts the minute another ends. Not applied to the working-hours or blocked-time edges — no one needs recovery time from the start of the day. |
| `minimum_notice_minutes` | integer | How far ahead the first offerable time must be (60 = an hour, 1440 = a day). Moves the window start. |
| `window_days` | integer | How far ahead to search. |
| `max_slots` | integer | Cap on free ranges returned. |
| `max_candidates` | integer | Cap on discrete start times returned. |

`TimeWindow`:

| Field | Type | Notes |
|---|---|---|
| `start` | string | Local start time, "HH:MM". |
| `end` | string | Local end time, "HH:MM" (exclusive). |
| `label` | string | Optional name, used in the posted explanation (e.g. "Lunch"). |

### `feature.gcal.plan_availability`

Select the connected calendar accounts and freeze the window.

Pass `accounts: $channel.integration_list` — the interpreter
publishes every named integration the channel config connects.
Carries no `integration_id`: this step touches no account.

```yaml
- id: <step>
  activity: feature.gcal.plan_availability
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `accounts` | list of object | no | Channel integrations to filter, normally $channel.integration_list. Entries carry name/id/provider/provider_account. |
| `name_prefix` | string | no | Integration-name family to keep: an exact match or a repeatable instance of it ('gcal' keeps gcal, gcal_2, …). Default `"gcal"`. |
| `time_min` | string | no | RFC3339 start of the search window (offset required). Empty → now. Default `""`. |
| `time_max` | string | no | RFC3339 end of the search window (offset required). Empty → time_min + the policy's window_days. Default `""`. |
| `policy` | SchedulePolicy | no | Resolved scheduling rules from feature.gcal.resolve_schedule_policy. Only window_days and minimum_notice_minutes shape the window here; the rest apply at merge time. Validated in full so a malformed rule fails BEFORE any calendar is read. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `accounts` | list of GcalPlannedAccount | Calendar accounts to read, name-sorted. Fan out with `foreach` and bind each item's `id`. EMPTY means no calendar is connected — gate the rest of the rail on this (an empty list is falsy in `when:`) and report `note`. |
| `note` | string | Why there are no accounts, in words fit to show a user. Empty when accounts were found. |
| `time_min` | string | Frozen window start, RFC3339. |
| `time_max` | string | Frozen window end, RFC3339. |

`GcalPlannedAccount`:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Channel-config integration name (gcal, gcal_2, …). |
| `id` | string | Connected account id — feed to read_busy's integration_id so the step runs AS this account. |
| `label` | string | Human-facing account handle (the connected email when known, else the name). Used in error messages so an operator knows which calendar to reconnect. |

`SchedulePolicy`:

| Field | Type | Notes |
|---|---|---|
| `timezone` | string | IANA zone every time-of-day rule below is read in, and the zone all-day events are localized in. |
| `weekdays` | list of string | Days that can hold a meeting (mon…sun). Days left out are blocked whole. |
| `working_hours` | TimeWindow | The daily window meetings may fall in. HARD. |
| `blocked_times` | list of TimeWindow | Recurring daily windows never to book (lunch, a standing stand-up). HARD. |
| `preferred_hours` | list of TimeWindow | Windows to offer FIRST when available. SOFT — ranking only, never a filter. |
| `duration_minutes` | integer | Meeting length. |
| `granularity_minutes` | integer | Start times are aligned to this many minutes past the local hour (30 -> :00 and :30). 0 disables slicing, leaving only the free ranges. |
| `buffer_minutes` | integer | Padding kept either side of an EXISTING meeting, so a call never starts the minute another ends. Not applied to the working-hours or blocked-time edges — no one needs recovery time from the start of the day. |
| `minimum_notice_minutes` | integer | How far ahead the first offerable time must be (60 = an hour, 1440 = a day). Moves the window start. |
| `window_days` | integer | How far ahead to search. |
| `max_slots` | integer | Cap on free ranges returned. |
| `max_candidates` | integer | Cap on discrete start times returned. |

`TimeWindow`:

| Field | Type | Notes |
|---|---|---|
| `start` | string | Local start time, "HH:MM". |
| `end` | string | Local end time, "HH:MM" (exclusive). |
| `label` | string | Optional name, used in the posted explanation (e.g. "Lunch"). |

### `feature.gcal.read_busy`

Read one connected account's busy blocks over a fixed window.

Carry `integration_id` (inherited from ActivityInput) so the
identity binding swaps the auth to that account before the read —
in the fan-out that's the planned account's `$acct.id`.

```yaml
- id: <step>
  activity: feature.gcal.read_busy
  args:
    time_min: <string>
    time_max: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `calendar_ids` | list of string | no | Calendars to read through the bound account. Defaults to that account's own primary calendar; pass attendee email addresses to check calendars it can see. |
| `time_min` | string | yes | RFC3339 window start (offset required). Required — the window is frozen upstream by plan_availability so every account is read over the SAME window. |
| `time_max` | string | yes | RFC3339 window end (offset required). |
| `timezone` | string | no | IANA timezone all-day events are localized in. Default `"UTC"`. |
| `account_label` | string | no | Human-facing name for the bound account, used in error messages so an operator knows which calendar to reconnect. Default `""`. |
| `require_all` | boolean | no | True (the firm's own connected calendars): an unreadable calendar fails the run. False (external attendees): it comes back as status 'unknown'. Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `busy` | list of GcalBusyPeriod | Busy blocks across every readable calendar in this read, unordered. |
| `calendars` | list of GcalCalendarStatus | Per-calendar visibility for this account. |

`GcalBusyPeriod`:

| Field | Type | Notes |
|---|---|---|
| `start` | string | Busy block start, RFC3339. |
| `end` | string | Busy block end, RFC3339. |

`GcalCalendarStatus`:

| Field | Type | Notes |
|---|---|---|
| `calendar_id` | string | Calendar as queried. |
| `label` | string | The account this calendar was read through. |
| `status` | `ok` / `unknown` | 'ok' = busy data returned; 'unknown' = not readable (only possible when require_all is False). |
| `detail` | string | Error reason when status is 'unknown' (e.g. notFound, forbidden). |

### `feature.gcal.resolve_booking_link`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.gcal.resolve_booking_link
  args:
    link: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `link` | string | yes | A Google appointment schedule link (the calendar.app.google share link or the booking page URL) or a Cal.com event link (cal.com/<user>/<event>). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `schedule_id` | string | The appointment schedule's id (AcZssZ…), stable across renames; for Cal.com, cal.com/<user>/<event>. |
| `title` | string | The schedule's title, which prefixes the title of every event it books. Empty when the schedule has none. |
| `booking_url` | string | The booking page the link resolved to. |

### `feature.gcal.resolve_schedule_policy`

Merge the channel's scheduling config with per-run overrides.

Carries no `integration_id`: this step touches no account.

```yaml
- id: <step>
  activity: feature.gcal.resolve_schedule_policy
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `settings` | object, optional | no | The channel's scheduling config map, normally $channel.scheduling. Null/empty takes every default. |
| `overrides` | object | no | Per-run overrides keyed the same as the config (duration_minutes, timezone, …). A null or empty-string value counts as unset, since flow inputs can't express 'absent'. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `policy` | SchedulePolicy | The effective rules: defaults < channel config < overrides, every field populated. |

`SchedulePolicy`:

| Field | Type | Notes |
|---|---|---|
| `timezone` | string | IANA zone every time-of-day rule below is read in, and the zone all-day events are localized in. |
| `weekdays` | list of string | Days that can hold a meeting (mon…sun). Days left out are blocked whole. |
| `working_hours` | TimeWindow | The daily window meetings may fall in. HARD. |
| `blocked_times` | list of TimeWindow | Recurring daily windows never to book (lunch, a standing stand-up). HARD. |
| `preferred_hours` | list of TimeWindow | Windows to offer FIRST when available. SOFT — ranking only, never a filter. |
| `duration_minutes` | integer | Meeting length. |
| `granularity_minutes` | integer | Start times are aligned to this many minutes past the local hour (30 -> :00 and :30). 0 disables slicing, leaving only the free ranges. |
| `buffer_minutes` | integer | Padding kept either side of an EXISTING meeting, so a call never starts the minute another ends. Not applied to the working-hours or blocked-time edges — no one needs recovery time from the start of the day. |
| `minimum_notice_minutes` | integer | How far ahead the first offerable time must be (60 = an hour, 1440 = a day). Moves the window start. |
| `window_days` | integer | How far ahead to search. |
| `max_slots` | integer | Cap on free ranges returned. |
| `max_candidates` | integer | Cap on discrete start times returned. |

`TimeWindow`:

| Field | Type | Notes |
|---|---|---|
| `start` | string | Local start time, "HH:MM". |
| `end` | string | Local end time, "HH:MM" (exclusive). |
| `label` | string | Optional name, used in the posted explanation (e.g. "Lunch"). |

## feature.gdrive

### `feature.gdrive.check_folder`

Check a picked Drive folder before it is saved as a destination.

Carry `integration_name` (normally `gdrive`) so the step runs as
the bound Google account.

```yaml
- id: <step>
  activity: feature.gdrive.check_folder
  args:
    conversation_id: <string>
    folder: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `folder` | string | yes | Folder id or Drive URL — normally the id the person picked in the Google Picker. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `folder_id` | string |  |
| `name` | string |  |
| `web_view_link` | string |  |
| `drive_id` | string | The shared drive holding the folder; empty in a My Drive. |

### `feature.gdrive.download_to_store`

Download a picked Drive file into a permanent agent-store file.

Carry `integration_id` / `integration_name` (inherited from
ActivityInput, normally `integration_name: gdrive`) so the identity
binding swaps the auth to the bound Google account first. Prior files
under the same stem are replaced — but never before the replacement's
bytes are durably stored.

```yaml
- id: <step>
  activity: feature.gdrive.download_to_store
  args:
    conversation_id: <string>
    file: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (the durable copy lands in this conversation's agent store). |
| `file` | string | yes | Drive file id or Docs/Drive URL — normally the id the user picked via the client-side Google Picker. |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'onboarding/standard-retainer'. The activity appends '.<ext>' derived from the downloaded filename (then content type, then 'bin') and replaces any existing '<stem>.*' file. |
| `accept` | list of string, optional | no | Allowed kinds in the file.detect taxonomy (pdf, xlsx, csv, image, docx, text). A download classifying outside the list fails non-retryably (UnsupportedFileType); omit to accept anything. |
| `export_format` | string, optional | no | Export target for Google-native files (Docs/Sheets/Slides). Defaults to pdf so a native Doc satisfies accept: [pdf]; set null for the type's plain export (Docs→text, Sheets→csv). Non-native files always download verbatim. Default `"pdf"`. |
| `require_source_mime_type` | string, optional | no | Require the picked file's OWN Drive mime type to be this — 'application/vnd.google-apps.document' for a retainer that will be filled in Google Docs. Checked before anything is stored; a mismatch fails non-retryably by name (GdriveSourceNotGoogleDoc / GdriveSourceNotAccepted). None accepts any type the accept list allows. |
| `convert_word_to_doc` | boolean | no | Convert a picked Word file (.docx/.doc) to a native Google Doc before downloading, in the Word file's own folder (My Drive when that folder won't take it), named like it without the extension. Any other file is downloaded as picked. Default `false`. |
| `max_bytes` | integer | no | Hard cap on the payload. Enforced by the proxy against Drive's declared size before any content moves, and again here after decoding (Google-native exports declare no size). Either way an oversized file fails non-retryably (FileTooLarge). Default `26214400`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Final agent-store file key, e.g. 'onboarding/standard-retainer.pdf'. |
| `size_bytes` | integer |  |
| `sha256` | string |  |
| `content_type` | string, optional |  |
| `filename` | string, optional | Download filename from Drive (export target included), for display/record use. |
| `drive_file_id` | string | The Drive file the bytes came from, for provenance records: the id/URL as passed, or the converted Doc's id when convert_word_to_doc turned a Word pick into one. |
| `converted_from_file_id` | string | The picked Word file's id when it was converted to the Doc in drive_file_id; empty otherwise. |
| `source_mime_type` | string | The picked file's own Drive mime type ('application/vnd.google-apps.document' for a native Doc), as distinct from content_type, the export's. Recorded in the document envelope so a later step knows what the pick was. |

### `feature.gdrive.ensure_folder`

The app's folder carrying `tag`, made in `parent_id` (My Drive's
root when omitted) if none does.

```yaml
- id: <step>
  activity: feature.gdrive.ensure_folder
  args:
    conversation_id: <string>
    name: <string>
    tag: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `name` | string | yes | The folder's name when it has to be made. |
| `tag` | string | yes | What identifies the folder across runs, renames and moves, e.g. `signed_documents:<conversation_id>`. |
| `parent_id` | string, optional | no | The folder to make it in when no live folder carries the tag, e.g. another ensure_folder's `folder_id`; My Drive's root when omitted. A folder that already carries the tag is returned wherever it now lives, so a folder the firm moved is followed, never duplicated — unless `by_name_in_parent` is set. |
| `by_name_in_parent` | boolean | no | Find the folder by `name` directly inside `parent_id` (My Drive's root when omitted) instead of by tag anywhere: a folder moved elsewhere, renamed or on a shared drive is not reused, and a new one is made in `parent_id`. Only folders the app made or the Picker granted are visible. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `folder_id` | string |  |
| `name` | string |  |
| `web_view_link` | string |  |
| `drive_id` | string | The shared drive holding the folder; empty in a My Drive. |
| `created` | boolean | True when this call made the folder; False when a live folder already carried the tag. |

### `feature.gdrive.file_metadata`

Look up a picked Drive file's name and type.

Carry `integration_name` (normally `gdrive`) so the step runs as
the bound Google account.

```yaml
- id: <step>
  activity: feature.gdrive.file_metadata
  args:
    conversation_id: <string>
    file: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file` | string | yes | Drive file id or Docs/Drive URL — normally the id the person picked in the Google Picker. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_id` | string |  |
| `name` | string |  |
| `mime_type` | string | The file's own Drive mime type: 'application/vnd.google-apps.document' for a native Doc, 'application/pdf' for a PDF, and so on. |
| `web_view_link` | string |  |

### `feature.gdrive.file_to_client_folder`

File one agent-store file into its client's folder in the firm's
Drive. Carry `integration_name` (normally `gdrive`) so the step runs
as the bound Google account.

```yaml
- id: <step>
  activity: feature.gdrive.file_to_client_folder
  args:
    conversation_id: <string>
    file_key: <string>
    file_name: <string>
    upload_tag: <string>
    client_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | The agent-store file to upload (a PDF). |
| `file_name` | string | yes | The Drive file's name. |
| `upload_tag` | string | yes | What identifies this file across retries: a live file in the client's folder already carrying it is returned and nothing is uploaded. One per document filed (a signing round). |
| `person_name` | string | no | The client's full name; their folder is "Last, First" from it. Default `""`. |
| `client_key` | string | yes | The client's identity in this channel (the row's id): their folder's tag, so every document they sign shares it. |
| `client_folder_fallback` | string | no | The folder's name when person_name has nothing usable, e.g. `Recipient 412`. Blank: `Client <client_key>`. Default `""`. |
| `folder` | any, optional | no | The firm's pick, the `signed_documents_folder` scalar as stored ({folder_id, name, …} as JSON text or parsed); empty for the default "Active Clients". |
| `default_folder_name` | string | no | The default parent's name at the top of My Drive. Default `"Active Clients"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `filed` | boolean |  |
| `cause` | string | Why nothing was filed: not_connected, folder_missing, folder_not_writable (the channel's to fix), source_missing, too_large (this file's), filing_off. Blank when filed. |
| `error_type` | string |  |
| `reason` | string |  |
| `parent_mode` | string | picked / default |
| `parent_folder_id` | string |  |
| `routine_folder_id` | string | The channel's folder inside the parent. |
| `routine_folder_name` | string |  |
| `default_folder_id` | string |  |
| `default_folder_name` | string |  |
| `default_folder_link` | string |  |
| `default_drive_id` | string |  |
| `folder_id` | string | The client's folder. |
| `folder_name` | string |  |
| `file_id` | string |  |
| `file_name` | string |  |
| `web_view_link` | string |  |
| `created` | boolean | True when this call uploaded; False when the tagged file was already there. |

### `feature.gdrive.read_document`

Read a Google Drive document's content as markdown.

Carry `integration_id` (inherited from ActivityInput, normally
`$channel.integrations.gdrive.id`) so the identity binding swaps
the auth to the bound Google account before the read.

```yaml
- id: <step>
  activity: feature.gdrive.read_document
  args:
    file: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `file` | string | yes | Drive file id or Docs/Drive URL — normally the id the user picked via the client-side Google Picker. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `document_id` | string | Canonical Drive file id. |
| `title` | string | Document title. |
| `url` | string | Web link to the document. |
| `content` | string | Document content as markdown (plain text when the read fell back to Drive export). |
| `last_edited` | string | RFC3339 modifiedTime, '' when unavailable. |

### `feature.gdrive.template_html`

Export the pinned retainer's Google Doc as HTML, once per template.

Carry `integration_name: gdrive` so the identity binding swaps the
auth to the bound Google account — the export goes through the same
/v2 drive proxy the pick used.

```yaml
- id: <step>
  activity: feature.gdrive.template_html
  args:
    conversation_id: <string>
    template_file_key: <string>
    template_sha256: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `template_file_key` | string | yes | The pinned template PDF (feature.pdf.pin_template's file_key), whose text the Doc's is checked against. |
| `template_sha256` | string | yes | The pinned template's digest; the HTML is stored and recorded under it. |
| `drive_file_id` | string, optional | no | The picked template's Drive file id, as the pick recorded it; blank for a template that was uploaded rather than picked, which has no page to export. Default `""`. |
| `source_mime_type` | string, optional | no | The picked file's own Drive mime type; only a native Google Doc exports. Blank (an envelope from before the pick recorded it) is skipped rather than guessed. Default `""`. |
| `max_bytes` | integer | no | Cap on each export's payload; a Doc over it is skipped (the row shows the merge's pages as before). Default `10485760`. |
| `inline_images` | boolean | no | Fetch the export's googleusercontent images and inline them as data: URIs so the stored page is self-contained. Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `html_file_key` | string | templates/<sha256[:16]>.html, or blank when nothing was stored or recorded (see status / why). |
| `status` | `stored` / `cached` / `skipped` / `drifted` | stored: exported and recorded by this run; cached: an earlier run recorded it, no Drive call made; skipped: nothing to export (not a picked Google Doc, or over the cap); drifted: the Doc's text no longer matches the pinned PDF, nothing recorded. |
| `why` | string |  |
| `images_inlined` | integer |  |

### `feature.gdrive.upload_from_store`

Upload an agent-store file into a Drive folder.

```yaml
- id: <step>
  activity: feature.gdrive.upload_from_store
  args:
    conversation_id: <string>
    file_key: <string>
    folder_id: <string>
    name: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | The agent-store file to upload, e.g. the `file_key` feature.signing.fetch_signed_document returned. |
| `folder_id` | string | yes | The Drive folder to land it in (check_folder's or ensure_folder's `folder_id`). |
| `name` | string | yes | The Drive file's name. |
| `mime_type` | string | no | Default `"application/pdf"`. |
| `tag` | string, optional | no | With a tag, a live file in the folder already carrying it is returned (`created: false`) and nothing is uploaded — what makes a retry safe. Include the content's hash so a different document is never mistaken for the one already filed. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_id` | string |  |
| `name` | string |  |
| `web_view_link` | string |  |
| `created` | boolean |  |
| `size_bytes` | integer |  |
| `sha256` | string |  |

## feature.linear

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

## feature.mbox

### `feature.mbox.index`

*Beta.*

Download an mbox from the agent store and build its message index.

Materializes the mbox into the worker's local cache and builds a per-message
sidecar (offsets + ids + dates) so chunk processors can range-fetch their
slice without scanning the whole file. Returns the total message count and
local paths for `mbox.plan_chunks` and the chunk steps.

```yaml
- id: <step>
  activity: feature.mbox.index
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Conversation that owns the mbox file upload. |
| `file_key` | string | yes | Key under /v1/files where the mbox file lives. |
| `rebuild` | boolean | no | Force a fresh sidecar build, ignoring any cached sidecar. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `total_messages` | integer |  |
| `local_mbox_path` | string |  |
| `local_sidecar_path` | string |  |
| `mbox_file_key` | string |  |

### `feature.mbox.index_progression`

*Beta.*

Discover a numbered mbox progression from a base key and index each part.

`base_file_key` is the prefix the parts share (`something.mbox` for
`something.mbox.1` / `.2` / …). A lone file with no numbered parts is
processed as a single file, so this is back-compatible with the original
single-mbox backfill.

```yaml
- id: <step>
  activity: feature.mbox.index_progression
  args:
    conversation_id: <string>
    base_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Conversation that owns the mbox file uploads. |
| `base_file_key` | string | yes | Base key the numbered parts share under /v1/files. The parts `<base>.1`, `<base>.2`, … are discovered contiguously; a lone `<base>` with no parts is indexed as a single file. |
| `rebuild` | boolean | no | Force a fresh sidecar build for each part. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `total_messages` | integer |  |
| `files` | list of MboxFileIndex |  |
| `file_keys` | list of string |  |

`MboxFileIndex`:

| Field | Type | Notes |
|---|---|---|
| `file_key` | string |  |
| `total_messages` | integer |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.mbox.plan_chunks`

*Beta.*

Split a message index into contiguous `[start, end)` ranges.

Pure compute: given `total_messages` (from `mbox.index`) and a
`chunk_size`, returns the chunk ranges a flow can `foreach` over, each
then processed by `mbox.process_chunk`. The chunk — not the
individual email — is the unit of replay, keeping the Temporal event history
small for large mboxes.

```yaml
- id: <step>
  activity: feature.mbox.plan_chunks
  args:
    total_messages: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `total_messages` | integer | yes | Number of messages in the mbox (from mbox.index). |
| `chunk_size` | integer | no | Messages per chunk. 500 is a reasonable default for live AI extraction concurrency=8 with the per-message-id cache. Default `500`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `chunks` | list of MboxChunk |  |
| `chunk_count` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.mbox.plan_progression`

*Beta.*

Flatten `mbox.index_progression`'s per-file list into chunk ranges.

Each file is split into `[start, end)` ranges of `chunk_size` messages;
every chunk carries its file's `file_key` / `local_mbox_path` /
`progress_offset` so one `foreach` processes the whole progression.

```yaml
- id: <step>
  activity: feature.mbox.plan_progression
  args:
    files: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `files` | list of MboxFileIndex | yes | Per-file index output from mbox.index_progression. |
| `chunk_size` | integer | no | Messages per chunk (matches mbox.plan_chunks). Default `500`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `chunks` | list of MboxChunk |  |
| `chunk_count` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

`MboxFileIndex`:

| Field | Type | Notes |
|---|---|---|
| `file_key` | string |  |
| `total_messages` | integer |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

### `feature.mbox.process_chunk`

*Beta.*

Run the watcher pipeline over one `[start, end)` slice of an mbox.

The "fat" backfill activity: opens the local mbox + sidecar (from
`mbox.index`), iterates its range, and runs each message through the same
Tier0-3 filter + LLM extractor + agent-store resolver as the live watcher.
The chunk is the unit of replay; writes are idempotent under run-scoped
keys. `seed_only=True` (PDF-seeded) only patches existing rows and is
parallel-safe; `seed_only=False` (legacy) creates rows, so it runs serial.

Reads its slice from a materialized mbox.

```yaml
- id: <step>
  activity: feature.mbox.process_chunk
  args:
    conversation_id: <string>
    chunk: ...
    mbox_file_key: <string>
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
| `chunk` | MboxChunk | yes | One entry from mbox.plan_chunks.output.chunks. |
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
| `mbox_file_key` | string | yes | Key under /v1/files for the mbox. The activity materializes the mbox + sidecar into this worker's local cache from the agent store if absent, so it need NOT run on the same worker as mbox.index. |
| `local_mbox_path` | string | no | Same-worker fast-path hint from mbox.index. Ignored for correctness — the cache path is derived from mbox_file_key. Default `""`. |

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

### `feature.mbox.replay_chunk`

*Beta.*

Replay one mbox chunk into the channel's `tracker` table: one row per
message (`{From, Subject, Date, Snippet, Body, message_id}`), upserted
with `merge_on=[message_id]` so re-replay is idempotent. No Gmail /
AgentCore dependency — the local-testing companion to `email.list`.

Inherits `StatusProgressArgs` (`progress_kind` / `progress_pct_start`
/ `progress_pct_end`) so the replay flow can drive a status-widget
progress bar across the serial chunks; dormant when `progress_kind` is
unset.

```yaml
- id: <step>
  activity: feature.mbox.replay_chunk
  args:
    conversation_id: <string>
    mbox_file_key: <string>
    chunk: ...
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation that owns the mbox + the target table. |
| `mbox_file_key` | string | yes | Key under /v1/files for the mbox. The activity materializes the mbox + sidecar into this worker's local cache from the agent store if absent, so it need NOT run on the same worker as mbox.index. |
| `local_mbox_path` | string | no | Same-worker fast-path hint from mbox.index. Ignored for correctness — the cache path is derived from mbox_file_key. Default `""`. |
| `chunk` | MboxChunk | yes | One entry from mbox.plan_chunks.output.chunks. |
| `snippet_chars` | integer | no | Max characters of Body kept in the Snippet column. Default `200`. |
| `table_name` | string | no | Target agent-store table (the emailreader channel table; the platform-convention primary table name). Default `"tracker"`. |
| `upsert_batch_size` | integer | no | Rows per insert_records call. Sub-batched so a chunk of full bodies isn't one multi-MB request that trips the client timeout. Default `100`. |
| `progress_total_messages` | integer, optional | no | Total messages across all chunks (mbox.index.total_messages) — the denominator for the overall replay percentage. Paired with progress_kind to drive the status-widget progress bar. |

**Returns**

Per-chunk counters. Aggregated by the DSL flow's collect step; a gap in
`batch_number` across the collected list reveals a skipped chunk.

| Field | Type | Notes |
|---|---|---|
| `chunk_start` | integer |  |
| `chunk_end` | integer |  |
| `batch_number` | integer |  |
| `total` | integer |  |
| `rows_written` | integer |  |
| `no_id` | integer |  |
| `parse_errors` | integer |  |

`MboxChunk`:

| Field | Type | Notes |
|---|---|---|
| `start` | integer |  |
| `end` | integer |  |
| `batch_number` | integer |  |
| `file_key` | string, optional |  |
| `local_mbox_path` | string |  |
| `progress_offset` | integer |  |

## feature.onboarding

### `feature.onboarding.evaluate`

Evaluate the channel's onboarding signals and latch `setup_fulfilled`
/ `onboarding_complete` the moment they hold. One-way: already-latched
flags are never re-evaluated or rewritten.

```yaml
- id: <step>
  activity: feature.onboarding.evaluate
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `email_connected` | boolean, optional | no |  |
| `required_steps` | list of string | no |  |
| `ready_scalar` | string, optional | no |  |
| `fully_live` | boolean, optional | no |  |
| `client_owned_setup` | boolean | no | Let the client's Continue action own setup_fulfilled. Only latch the fully-live safety net here. Exclusive with required_steps and ready_scalar. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `setup_fulfilled` | boolean | The latch's value after this pass. |
| `onboarding_complete` | boolean | The latch's value after this pass. |
| `user_steps_done` | boolean | Whether the user-steps gate held this pass (independent of whether anything newly latched). |

### `feature.onboarding.mark_step`

Mark one onboarding checklist step done in the `onboarding_state`
envelope the Today view reads. Deep-merges, so other steps' entries are
preserved.

```yaml
- id: <step>
  activity: feature.onboarding.mark_step
  args:
    conversation_id: <string>
    step_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `step_id` | string | yes | The strings.yaml today.onboarding_steps id of the finished step, e.g. upload_questions. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `step_id` | string | The step just marked done. |
| `steps` | map of string | The post-merge steps map (every step's state so far). |

## feature.pdf

### `feature.pdf.extract_page_rows`

*Beta.*

Extract structured rows from rendered PDF page images with a vision LLM.

Reads the `pages` (rendered by `pdf.render_pages`) up to `max_pages`,
applies `instructions` to pull generic rows from each page, and stages the
result to an agent-store file (`rows_file_key`). Run in batches and
combined by `pdf.merge_page_rows`.

```yaml
- id: <step>
  activity: feature.pdf.extract_page_rows
  args:
    conversation_id: <string>
    source: ...
    pages: <array>
    instructions: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the page image uploads (must be the flow's own conversation). |
| `source` | PdfRenderSource | yes | Source PDF metadata. |
| `pages` | list of PdfPageImage | yes | Rendered page image refs from pdf.render_pages. |
| `max_pages` | integer, optional | no | Maximum number of page refs to inspect serially. Default `3`. |
| `instructions` | string | yes | Extraction instructions for the visible PDF page content. |
| `model` | string | no | Claude model id or Bedrock inference profile id. Default `"claude-sonnet-4-6"`. |
| `max_tokens` | integer | no | Maximum model output tokens per page. Default `4096`. |
| `progress_total_pages` | integer, optional | no | Total pages across all batches — the denominator for the overall completion percentage shown during extraction. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `row_count` | integer |  |
| `pages` | list of PdfExtractedPage |  |
| `rows` | list of PdfExtractedRow |  |
| `rows_file_key` | string, optional |  |
| `model` | string |  |

`PdfExtractedPage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `row_count` | integer |  |

`PdfExtractedRow`:

| Field | Type | Notes |
|---|---|---|
| `source_file_key` | string |  |
| `source_filename` | string, optional |  |
| `page_number` | integer |  |
| `page_image_file_key` | string |  |
| `page_image_storage` | string |  |
| `row_index` | integer |  |
| `extracted_text` | string |  |
| `summary` | string |  |
| `fields` | object |  |
| `row_data` | object |  |
| `confidence` | number, optional |  |
| `model` | string |  |

`PdfPageImage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `filename` | string |  |
| `mime_type` | string |  |
| `width_px` | integer |  |
| `height_px` | integer |  |
| `dpi` | integer |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

### `feature.pdf.extract_row_images`

*Beta.*

Crop per-row cell images from the source PDF and attach them to rows.

Loads the merged rows from `rows_file_key`, pulls each row's native or
raster-cropped image from the source PDF, uploads it, and writes the image
refs back onto the rows (re-staged as a new blob). Returns the new
`rows_file_key` plus the image list.

```yaml
- id: <step>
  activity: feature.pdf.extract_row_images
  args:
    conversation_id: <string>
    source: ...
    rows_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of image attachment. Default `70.0`. |
| `progress_pct_end` | number | no | Overall completion % when image attachment finishes. Default `90.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the source PDF and rows (must be the flow's own conversation). |
| `source` | PdfRenderSource | yes | Source PDF metadata. |
| `rows_file_key` | string | yes | Agent-store file of rows from pdf.merge_page_rows. |
| `max_pages` | integer, optional | no | Optional cap for attaching row images. |
| `dpi` | integer | no | DPI used when raster-cropping row images from PDF pages. Default `300`. |
| `progress_after_seconds` | number | no | Minimum elapsed time before the first progress update. Default `2.0`. |
| `progress_every_seconds` | number | no | Minimum elapsed time between progress updates. Default `2.0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `image_count` | integer |  |
| `rows_file_key` | string |  |
| `images` | list of PdfExtractedRowImage |  |
| `warnings` | list of string |  |

`PdfExtractedRowImage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `row_index` | integer |  |
| `file_key` | string |  |
| `filename` | string |  |
| `storage` | string |  |
| `mime_type` | string |  |
| `width_px` | integer, optional |  |
| `height_px` | integer, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string |  |
| `bbox` | PdfRowImageBBox |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

`PdfRowImageBBox`:

| Field | Type | Notes |
|---|---|---|
| `x0` | number |  |
| `y0` | number |  |
| `x1` | number |  |
| `y1` | number |  |
| `units` | string |  |

### `feature.pdf.inspect_fields`

List the placeholders and signature tags in an agent-store PDF.

```yaml
- id: <step>
  activity: feature.pdf.inspect_fields
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | Agent-store file key of the template PDF, e.g. 'templates/retainer.pdf' (the file_key that foundation.file.copy_to_store or feature.gdrive.download_to_store returned). Any text-layer PDF works, whatever produced it. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string |  |
| `sha256` | string | Digest of the template as read. |
| `page_count` | integer |  |
| `has_text_layer` | boolean |  |
| `keys` | list of string | Distinct placeholder keys, sorted — the values map merge_fields expects. |
| `placeholders` | list of PdfPlaceholder |  |
| `placeholder_count` | integer |  |
| `signature_tags` | list of PdfSignatureTag |  |
| `signer_roles` | list of string | Distinct roles across the signature tags, in the order the template means them (signer 2 before signer 10) — what feature.signing.send_document's signers must cover. A simple [[signer N date]] tag adds no role: it belongs to the signer it names. |
| `unknown_tokens` | list of PdfUnknownToken | [[...]] / «...» tokens that are neither a placeholder key nor a signer tag. The merge leaves them as written and counts them unresolved; fix the template. |
| `tag_formats` | list of string | The signature-tag spellings this template uses: 'tag', 'simple', or both — which is a template mixing them. |
| `split_placeholders` | list of PdfSplitPlaceholder | Placeholders that wrap across a line; the merge cannot fill these and the template should be fixed. |
| `fonts` | list of string | Font families the PDF uses. |
| `warnings` | list of string |  |

`PdfPlaceholder`:

| Field | Type | Notes |
|---|---|---|
| `key` | string | The name inside [[...]]. |
| `page` | integer | 1-based page number. |
| `bbox` | list of number | [x0, y0, x1, y1] in PDF points, origin top-left. |

`PdfSignatureTag`:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Field name: the text before the first ';' of a {{...}} tag; the role for [[signer N]]; '<role> date' for [[signer N date]]. |
| `role` | string | The role= attribute. |
| `type` | string | The type= attribute of a {{...}} tag; 'signature' for [[signer N]]; 'datenow' (the provider's read-only, stamped-on-completion date) for [[signer N date]]. |
| `page` | integer |  |
| `bbox` | list of number, optional |  |
| `format` | string | Which spelling the author used: 'tag' for {{Name;role=Role;type=signature}}, which the provider reads out of the PDF itself, or 'simple' for [[signer 1]] / «Signer_1», whose box merge_fields measures and reports instead. |

`PdfSplitPlaceholder`:

| Field | Type | Notes |
|---|---|---|
| `fragment` | string | The text after '[[' (or '«') on the line where it opened. |
| `page` | integer |  |
| `bbox` | list of number |  |

`PdfUnknownToken`:

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |
| `page` | integer |  |
| `bbox` | list of number, optional |  |

### `feature.pdf.merge_fields`

Fill [[key]] placeholders in an agent-store PDF and store the result.

Template-source-agnostic: any PDF with a text layer works, whether a
Google Docs export, a copied conversation upload or a vendor form.

```yaml
- id: <step>
  activity: feature.pdf.merge_fields
  args:
    conversation_id: <string>
    template_file_key: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `template_file_key` | string | yes | Agent-store file key of the immutable template PDF, e.g. 'templates/retainer.pdf'. Never modified. |
| `values` | map of string | no | Placeholder key -> text. Keys absent here are left as [[key]] in the output and counted in unresolved_count, and so is a key whose value is blank or whitespace. Values may not contain '{{' or the placeholder syntax '[[' / ']]'. |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'documents/retainer-42'. The merged PDF lands at '<stem>.pdf' and previews at '<stem>-p<N>.png'; any prior '<stem>.*' is replaced. |
| `placeholder_syntax` | string | no | Placeholder form. Only [[key]] is supported; it is named so a second syntax can be added without a rename. Default `"double_square"`. |
| `overflow_policy` | `shrink` / `flag` | no | When a merged line is wider than its column: 'shrink' reduces the font size down to min_font_size and reports 'overflowed'; 'flag' leaves the line unmerged and reports it. Default `"shrink"`. |
| `min_font_size` | number | no | Smallest font size shrink-to-fit may use. Default `8.0`. |
| `preview_dpi` | integer | no | Resolution of the per-page PNG previews rendered here from the merged bytes and uploaded concurrently; 0 renders none and leaves them to a fan-out of feature.pdf.render_preview_pages over preview_page_batches. Default `100`. |
| `preview_batch_size` | integer | no | Pages per entry of the reported preview_page_batches — how coarse a flow's render fan-out is. Does not affect the inline previews. Default `2`. |
| `inline_preview_pages` | integer, optional | no | How many pages to render and store INLINE, from page 1; the rest are reported under deferred_page_batches for a feature.pdf.render_preview_pages step (publish: true) to land after the row has published — so a reader sees page 1 the moment the document exists and the rest as each arrives. None (the default) renders every page inline, as before. Only with a non-zero preview_dpi. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Agent-store file key of the merged PDF. |
| `sha256` | string | Digest of the merged bytes. Deterministic for the same template, values and options. |
| `size_bytes` | integer |  |
| `page_count` | integer |  |
| `page_numbers` | list of integer | Ordered 1-based page numbers for workflow preview fan-out. |
| `template_sha256` | string | Digest of the template as read. |
| `preview_file_keys` | list of string | One PNG per page, in page order; empty when preview_dpi is 0. |
| `preview_page_batches` | list of PreviewPageBatch | Consecutive 1-based page ranges of at most preview_batch_size pages covering the whole merged PDF — what a flow hands a foreach over feature.pdf.render_preview_pages so the previews render concurrently instead of inline. Always reported; meaningful with preview_dpi 0. |
| `planned_preview_file_keys` | list of string | Every page's durable preview key, in page order, whether or not this call wrote it — what a row's Preview Keys should read when the pages beyond inline_preview_pages are still on their way. |
| `deferred_page_batches` | list of PreviewPageBatch | The pages NOT rendered inline (after inline_preview_pages), in ranges of at most preview_batch_size — for a feature.pdf.render_preview_pages step with publish: true. Empty when every page was rendered here. |
| `placements` | list of PdfMergePlacement |  |
| `resolved_count` | integer |  |
| `overflowed_count` | integer |  |
| `unresolved_count` | integer | Placeholders still in the document, counted by RESCANNING the merged PDF (no value, split across lines, or left unmerged under overflow_policy flag). Gate a signature send on this being 0. |
| `keys_without_value` | list of string |  |
| `unused_values` | list of string | Keys in `values` that the template does not carry. |
| `signature_fields` | list of PdfSignatureField | One per [[signer N]] tag, measured on the MERGED page and ordered by signer: pass these to feature.signing.send_document's `fields` so each signer's box lands on the line the tag marks — the underscores or rule beside the tag, or the one directly below it. Empty for a template that uses the {{...}} tags the provider reads itself. |
| `signer_roles` | list of string | Distinct roles across `signature_fields`, in order. |

`PdfMergePlacement`:

| Field | Type | Notes |
|---|---|---|
| `key` | string |  |
| `page` | integer | 1-based page number. |
| `bbox` | list of number | [x0, y0, x1, y1] of the placeholder in PDF points. |
| `status` | string | resolved / overflowed (written, shrunk to fit) / unresolved_no_value / unresolved_split / unresolved_overflow (policy flag: did not fit, placeholder left in the document) / unresolved_unknown_token (a [[...]] / «...» that is neither a placeholder key nor a signer tag; left as written). |
| `fitted_size` | number | Font size the value was set at. |
| `note` | string |  |

`PdfSignatureField`:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Field label the signer sees: the role for a signature box, '<role> date' for its date box. |
| `role` | string | Which signer fills it, e.g. 'signer 1'. |
| `type` | string | 'signature', or 'datenow' for a [[signer N date]] box — read-only, stamped by the provider with the date that signer completed. |
| `required` | boolean | True for a signature box. False for a date box: the provider fills it, there is nothing for the signer to do. |
| `page` | integer | 1-based page number. |
| `area` | PdfSignatureFieldArea |  |

`PdfSignatureFieldArea`:

| Field | Type | Notes |
|---|---|---|
| `x` | number | Left edge, 0.0-1.0 of page width. |
| `y` | number | Top edge, 0.0-1.0 of page height. |
| `w` | number | Width, 0.0-1.0 of page width. |
| `h` | number | Height, 0.0-1.0 of page height. |

`PreviewPageBatch`:

| Field | Type | Notes |
|---|---|---|
| `first_page` | integer |  |
| `last_page` | integer |  |

### `feature.pdf.merge_page_rows`

*Beta.*

Combine the per-batch outputs of `pdf.extract_page_rows` into one set.

Materializes every batch's staged rows, sorts them by page/row, and
re-stages the merged set as a single `rows_file_key`. `min_rows` turns
"the document had no extractable rows at all" into a hard failure instead
of a silent empty import. (Whether the rows look like a particular schema's
data is a downstream/channel concern, not this generic merge step's.)

```yaml
- id: <step>
  activity: feature.pdf.merge_page_rows
  args:
    batches: <array>
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `batches` | list of PdfExtractPageRowsOutput | yes | Outputs returned by batched pdf.extract_page_rows calls. |
| `conversation_id` | string | yes | Conversation UUID that owns the staged rows blobs. |
| `source` | PdfRenderSource, optional | no | Fallback source metadata when batches is empty. |
| `model` | string, optional | no | Fallback model name when batches is empty. |
| `min_rows` | integer | no | Fail (non-retryable, type PdfNoRowsExtracted) when the merged row count is below this. Lets a flow turn 'the document had no extractable data' into a hard failure instead of an empty silent-success import. 0 (default) keeps the legacy behavior. Default `0`. |
| `cleanup_file_keys` | list of string | no | Deprecated no-op. Scratch blobs are uploaded as workflow-lifetime agent-store files and are owned by the temp-file reaper. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `row_count` | integer |  |
| `rows_file_key` | string |  |
| `model` | string |  |

`PdfExtractPageRowsOutput`:

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `row_count` | integer |  |
| `pages` | list of PdfExtractedPage |  |
| `rows` | list of PdfExtractedRow |  |
| `rows_file_key` | string, optional |  |
| `model` | string |  |

`PdfExtractedPage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `row_count` | integer |  |

`PdfExtractedRow`:

| Field | Type | Notes |
|---|---|---|
| `source_file_key` | string |  |
| `source_filename` | string, optional |  |
| `page_number` | integer |  |
| `page_image_file_key` | string |  |
| `page_image_storage` | string |  |
| `row_index` | integer |  |
| `extracted_text` | string |  |
| `summary` | string |  |
| `fields` | object |  |
| `row_data` | object |  |
| `confidence` | number, optional |  |
| `model` | string |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

### `feature.pdf.pin_template`

Preserve a staged PDF as an immutable template in this conversation.

```yaml
- id: <step>
  activity: feature.pdf.pin_template
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_key` | string | yes | The staged agent-store PDF file key. |
| `preview_dpi` | integer | no | Render one PNG per page of the unfilled template at this resolution beside the pin ('templates/<sha256[:16]>-p<N>.png'), once per content digest; 0 (the default) renders none. Match the merge's preview_dpi so the template page and the first merged page are the same size on screen. Default `0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | templates/<sha256[:16]>.pdf |
| `sha256` | string |  |
| `size_bytes` | integer |  |
| `page_count` | integer | Pages rendered; 0 when preview_dpi was 0. |
| `preview_file_keys` | list of string | templates/<sha256[:16]>-p<N>.png, one per page: the UNFILLED template, for a row to show before its first merge. Empty when preview_dpi was 0. |

### `feature.pdf.render_pages`

*Beta.*

Render conversation uploads, or one stored page for workflow fan-out.

Conversation mode retains its original temporary outputs. Agent-store
mode requires a page, source digest and output stem and stores a durable
preview; callers choose workflow concurrency and publication policy.

```yaml
- id: <step>
  activity: feature.pdf.render_pages
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Conversation UUID that owns the source PDF and generated pages (must be the flow's own conversation). |
| `conversation_file_key` | string, optional | no | Conversation-level source PDF file key (file_uploads). |
| `agent_store_file_key` | string, optional | no | Stored PDF to render in single-page durable mode. |
| `page_number` | integer, optional | no |  |
| `source_sha256` | string, optional | no | Expected PDF digest in durable mode. |
| `store_file_key_stem` | string, optional | no | Durable mode writes <stem>-p<N>.png. |
| `dpi` | integer | no | Render resolution in dots per inch. Default `144`. |
| `max_pages` | integer, optional | no | Optional cap for early tests or previews. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `pages` | list of PdfPageImage |  |
| `page_file_keys` | list of string |  |

`PdfPageImage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `filename` | string |  |
| `mime_type` | string |  |
| `width_px` | integer |  |
| `height_px` | integer |  |
| `dpi` | integer |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

### `feature.pdf.render_preview_pages`

Render pages first_page..last_page of a stored PDF to scratch PNGs.

```yaml
- id: <step>
  activity: feature.pdf.render_preview_pages
  args:
    conversation_id: <string>
    file_key: <string>
    store_file_key_stem: <string>
    first_page: <integer>
    last_page: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | Agent-store file key of the PDF to render, e.g. the merged 'documents/42/run-1.pdf'. |
| `store_file_key_stem` | string | yes | Key stem the previews will be published under by collect_previews ('<stem>-p<N>.png'); here it only names the scratch keys. |
| `first_page` | integer | yes | 1-based, inclusive. |
| `last_page` | integer | yes | 1-based, inclusive. |
| `dpi` | integer | no | Resolution of the PNGs. 100 matches the inline render and the pinned template's own previews. Default `100`. |
| `publish` | boolean | no | Write each page to its DURABLE key (<stem>-p<N>.png, the one Preview Keys names) instead of workflow scratch — for the pages a merge left to land after the row published. Default `false`. |
| `progress` | PreviewProgress, optional | no | With publish: after each page lands, in page order, patch a row column with the highest contiguous page number now stored, so a reader's pane can promote pages one by one. Guarded: skipped once the row no longer carries guard_value in guard_column (another rebuild published meanwhile). Best effort. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `first_page` | integer |  |
| `last_page` | integer |  |
| `reported_through` | integer | With progress: the highest page number the row was told is stored; 0 when nothing was reported (no progress asked, or the guard failed before the first page). |
| `lifetime` | string | 'workflow': every key here is scratch the store reaps when the workflow chain closes. |
| `pages` | list of PdfRenderedPreview | One entry per page in the range, in page order. |
| `preview_file_keys` | list of string | The pages' SCRATCH keys, in page order — what collect_previews promotes. Not the row's Preview Keys. |

`PdfRenderedPreview`:

| Field | Type | Notes |
|---|---|---|
| `page` | integer | 1-based page number. |
| `file_key` | string | The SCRATCH key (lifetime=workflow) this page rendered to. Never publish it: collect_previews promotes it to the permanent '<stem>-p<N>.png'. |
| `sha256` | string |  |
| `size_bytes` | integer |  |

`PreviewProgress`:

| Field | Type | Notes |
|---|---|---|
| `table_name` | string |  |
| `record_id` | integer |  |
| `column` | string |  |
| `guard_column` | string |  |
| `guard_value` | string |  |

## feature.recipe

### `feature.recipe.check`

Check a recipe against an app's head, with no channel to install on.

Holds `document` to the version a new channel of `app` would
install in this workspace, with no channel and no dry run: the
graph, contract and section checks an install runs, for a caller with
no channel to run them on. Writes nothing. The checks that need a
channel — its live rows, stored columns and uploaded questions — are
not run, and a channel's install can still refuse a document that
passes here.

```yaml
- id: <step>
  activity: feature.recipe.check
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `document` | string | no | Default `""`. |
| `app` | string | no | Default `"chase"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `sha` | string |  |
| `stages` | list of string |  |
| `problems` | list of map of string |  |
| `warnings` | list of map of string |  |
| `summary` | string |  |
| `app` | string |  |
| `semver` | string |  |
| `bundle_version_id` | integer, optional |  |
| `label` | string |  |
| `skipped` | list of string |  |
| `note` | string |  |

### `feature.recipe.current`

Report which recipe is in force on the channel, and its text.

The recipe is the one the channel installed, or else the bundle's
own. Reads the channel's config live, so
`sha` is what is installed now and `pinned_sha` is the revision
this run judges rows by; they differ when a recipe was installed
after the run started. `include_document: false` leaves the text
out and reports only the revision, its stages and its sections.

```yaml
- id: <step>
  activity: feature.recipe.current
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `include_document` | boolean | no | Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `declared` | boolean |  |
| `document_key` | string |  |
| `contract` | string |  |
| `source` | string |  |
| `sha` | string |  |
| `pinned_sha` | string |  |
| `installed_at` | string |  |
| `installed_by` | string |  |
| `name` | string |  |
| `document` | string |  |
| `stages` | list of string |  |
| `machines` | map of list of string |  |
| `vocabulary` | map of string |  |
| `guidance` | map of string |  |
| `deadlines` | list of object |  |
| `summary` | string |  |

### `feature.recipe.install`

Check a recipe and install it on the channel, or roll one back.

Takes exactly one of: a new `document`, the `sha` of a revision
the channel already holds, or `revert_to_default` for the bundle's
own. The recipe is held to every check a `states:` section passes
at publish and to the manifest's `contract`, and is refused when a
live row holds a state it does not declare or when it moves a stored
machine to another column. An install then renders the graph's
display hints onto the live tables, renders the bundle's client copy
through the recipe's `vocabulary:`, seeds the scalar keys its
stages read, and writes the revision last: if an earlier write
fails, the previous revision stays in force. `dry_run` checks and
writes nothing; `fail_step: false` reports a refusal instead of
failing the step. Rows are re-projected by a later run, which pins
the new revision.

```yaml
- id: <step>
  activity: feature.recipe.install
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | no | Default `""`. |
| `document` | string | no | Default `""`. |
| `sha` | string | no | Default `""`. |
| `revert_to_default` | boolean | no | Default `false`. |
| `name` | string | no | Default `""`. |
| `installed_by` | string | no | Default `""`. |
| `dry_run` | boolean | no | Default `false`. |
| `fail_step` | boolean | no | Default `true`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `dry_run` | boolean |  |
| `source` | string |  |
| `sha` | string |  |
| `previous_sha` | string |  |
| `stages` | list of string |  |
| `problems` | list of map of string |  |
| `warnings` | list of map of string |  |
| `stranded` | list of object |  |
| `tables_patched` | list of string |  |
| `seeded` | list of string |  |
| `vocabulary` | map of string |  |
| `copy_rendered` | integer |  |
| `guidance_agents` | list of string |  |
| `deadlines` | list of object |  |
| `summary` | string |  |

## feature.signing

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

## feature.signing.document

### `feature.signing.document.claim_send`

Take the row for this run's send and freeze what will be sent: the
merged file, the signers, the fields.

```yaml
- id: <step>
  activity: feature.signing.document.claim_send
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
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose provider request ended (Signing Status declined/expired) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
| `signers` | list of any, optional | no | Override for the row's Signers, [{role, email}]; null uses the row's, [] is refused. |

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
| `signers` | list of object |  |
| `fields` | list of object |  |

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

### `feature.signing.document.derive`

Publish facts onto the row — a provider answer, a release, a merge —
only while the row still names what the step expects.

```yaml
- id: <step>
  activity: feature.signing.document.derive
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
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
| `facts` | object | no |  |
| `change_kind` | string, optional | no |  |
| `change_action` | string, optional | no |  |
| `merged_values` | object, optional | no |  |
| `expect_document_id` | string, optional | no |  |
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

### `feature.signing.document.filing_due`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.signing.document.filing_due
  args:
    signings_table: <string>
    now: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<DocumentId>`): where each round's filing state lives. |
| `now` | string | yes | The run's fixed clock, ISO 8601. |
| `cap` | integer | no | Default `10`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `blocked` | string | The channel cause rounds wait on, or ''. |
| `rounds` | list of object | [{signing_key, record_id, document_id}] to file now. |

### `feature.signing.document.filing_mark`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.signing.document.filing_mark
  args:
    signings_table: <string>
    table_name: <string>
    record_id: <integer>
    document_id: <string>
    now: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `issues_table` | string | no | The worklist the filing items go to, keyed by `cause` (`drive_filing:<cause>`, `drive_filing:round:<signing_key>`). Default `"issues"`. |
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<DocumentId>`): where each round's filing state lives. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `document_of_column` | string | no | The seed's `{stage, prepared_at}` stamp: the stage the row's current document is for. Default `"Document Of"`. |
| `document_id` | string | yes | The request whose signing just completed. |
| `now` | string | yes | The run's fixed clock, ISO 8601. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `marked` | boolean |  |
| `reason` | string |  |
| `filing` | string | pending / off / failed |
| `signing_key` | string |  |
| `launch` | boolean | File it now: start the filing flow. |

### `feature.signing.document.filing_plan`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.signing.document.filing_plan
  args:
    signings_table: <string>
    table_name: <string>
    record_id: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<DocumentId>`): where each round's filing state lives. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `document_of_column` | string | no | The seed's `{stage, prepared_at}` stamp: the stage the row's current document is for. Default `"Document Of"`. |
| `document_id` | string | no | The round to file; blank is the row's latest signed one. Default `""`. |
| `auto` | boolean | no | A launch the flows made (the completion, the tick): files only a round stamped pending or a failure the tick retries. False is a person filing a round by hand, whatever its stamp. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file` | boolean |  |
| `reason` | string | Why not: off, not_signed, already_filed, not_pending, needs_attention. |
| `signing_key` | string |  |
| `document_id` | string |  |
| `record_id` | integer, optional |  |
| `stage` | string |  |
| `name` | string |  |
| `signed_key` | string |  |
| `signed_at` | string |  |
| `client_key` | string |  |
| `upload_tag` | string |  |

### `feature.signing.document.filing_record`

No description in the catalog.

```yaml
- id: <step>
  activity: feature.signing.document.filing_record
  args:
    signings_table: <string>
    table_name: <string>
    record_id: <integer>
    outcome: <string>
    document_id: <string>
    now: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `issues_table` | string | no | The worklist the filing items go to, keyed by `cause` (`drive_filing:<cause>`, `drive_filing:round:<signing_key>`). Default `"issues"`. |
| `signings_table` | string | yes | The signings ledger, keyed by signing_key (`<record_id>:<DocumentId>`): where each round's filing state lives. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `document_of_column` | string | no | The seed's `{stage, prepared_at}` stamp: the stage the row's current document is for. Default `"Document Of"`. |
| `outcome` | `attempt` / `result` | yes |  |
| `document_id` | string | yes |  |
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

### `feature.signing.document.inspect_reconcile`

Check an uncertain send may be reconciled, and name its fingerprint
and the document an operator says they found. Writes nothing.

```yaml
- id: <step>
  activity: feature.signing.document.inspect_reconcile
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
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
| `resolution` | string | no | Default `""`. |
| `document_id` | string | no | Default `""`. |

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
| `document_id` | string |  |
| `owned_document_id` | string | The document an operator confirmed, to adopt first. |

### `feature.signing.document.poll`

Read the row's signature request and stamp the attempt before any
provider I/O, so an uncertain request cannot monopolize the capped
oldest-first sweep.

```yaml
- id: <step>
  activity: feature.signing.document.poll
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
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
| `stamp` | boolean | no | Stamp `Checked At` (a row write with its own audit entry) before the provider is asked. False for a bundle that schedules no sweep on it: the poll then only reads, and refuses as before. Default `true`. |

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
| `document_id` | string |  |
| `sending` | string |  |
| `fingerprint` | string |  |

### `feature.signing.document.prefill`

Write a preparer's admitted values onto the fields still empty, each
only while its evidence still says what the preparer read.

```yaml
- id: <step>
  activity: feature.signing.document.prefill
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
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose provider request ended (Signing Status declined/expired) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
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

### `feature.signing.document.prepare`

Seed the row from a pinned template: its fields, the values the
seed can name by spelling, its signer roles and who each seats. A row
already prepared from this template keeps its values; only missing
preview pages are written onto it.

```yaml
- id: <step>
  activity: feature.signing.document.prepare
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
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose provider request ended (Signing Status declined/expired) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
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

### `feature.signing.document.reconcile`

Settle an uncertain send from the send ledger or the operator's
answer, bound to the fingerprint and claim that were inspected.

```yaml
- id: <step>
  activity: feature.signing.document.reconcile
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
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
| `expected_fingerprint` | string | yes |  |
| `expected_sending` | string, optional | no |  |
| `resolution` | string | no | Default `""`. |
| `document_id` | string | no | Default `""`. |
| `ledger` | object | no |  |

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
| `document_id` | string |  |
| `fingerprint` | string |  |
| `detail` | string |  |

### `feature.signing.document.template_source`

Probe a row against the stage's picked template: the pick's file and
whether this row is already prepared from it (`warm`), refused when
the row may not be prepared at all. Writes nothing.

```yaml
- id: <step>
  activity: feature.signing.document.template_source
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
| `refuse_when` | list of StoreClaimRefusal | yes | The bundle's eligibility, claim_row's rule vocabulary: the first rule whose every condition holds on the row refuses with its code and message. A row whose provider request ended (Signing Status declined/expired) is refused before these, DocumentRequestEnded. [] for none. |
| `table_name` | string | yes | The table the document rides on, e.g. tracker. |
| `record_id` | integer | yes | The row. |
| `machine` | string | no | The derived machine the projection names. Default `"document"`. |
| `refusal_codes` | map of string | no | Rename a refusal's code for this bundle, e.g. {DocumentRecordNotFound: RetainerRecordNotFound}. |
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

## feature.signing

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

## feature.sms

### `feature.sms.send`

*Beta.*

Send an SMS to a workspace contact. The text goes out from the
workspace's own phone number; opted-out contacts are rejected.

```yaml
- id: <step>
  activity: feature.sms.send
  args:
    contact_id: <string>
    body: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `contact_id` | string | yes | Workspace contact id (from the contacts book). |
| `body` | string | yes | Message text (1600 chars max). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `message_id` | string | sms_messages row id of the send. |
| `to_phone` | string | Resolved contact number (E.164). |
| `status` | string | Provider status (queued / sent); pending when this retry found the original attempt still in flight. |
| `duplicate` | boolean | True when this was an activity retry of an already-sent message (idempotency hit) — nothing was re-sent. |

## feature.state

### `feature.state.check`

Hold every row to the graph: each stored machine column holds a
declared state, a derive mirror agrees with the value the bundle
supplies, and Status is what the row's tuple composes to. With
`machines` supplied the derived ones are checked too; without, a
Status that only a derived overlay could explain is not an offender.

```yaml
- id: <step>
  activity: feature.state.check
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `machines` | map of map of string | no | Derived machine values per record id (as a string): {record_id: {machine: state}}. |
| `why` | map of string | no | Why prose per record id; the shown state's declared default otherwise. |
| `machine_why` | map of map of string | no | Per record id, prose per derive machine, written to its why_column: {record_id: {machine: text}}. |
| `guards` | map of list of string | no | The EXTERNAL guards that hold, per record id (as a string): {record_id: [guard, …]}. The bundle evaluates them; an edge behind one not listed here is not legal for that row. |
| `messages` | map of string | no | Chat-rail message override per CTA kind; the cta's own templated message otherwise. |
| `issue_fields` | map of object | no | Extra worklist columns per record id (bundle prose: name, contact, context). |
| `page_limit` | integer | no | Default `1000`. |
| `record_ids` | list of integer | no |  |
| `fail_step` | boolean | no | Default `false`. |
| `allow_blank_status` | boolean | no | Let a blank Status pass. Off by default: every tuple composes to a state, so a blank is a row projection never reached. Default `false`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `ok` | boolean |  |
| `rows` | integer |  |
| `offenders` | list of StateOffender |  |
| `offender_count` | integer |  |
| `summary` | string |  |

`StateOffender`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `column` | string |  |
| `value` | any |  |
| `problem` | string |  |

### `feature.state.project`

Re-derive the projection for rows from their tuple.

With no `record_ids` every row of the table is projected (the tick's
sweep) and the whole worklist reconciled; with some, only their own
worklist items may resolve. `write: false` computes without
patching, for a flow that wants to look first. `results` narrows
the per-row report: `warn` is the rows that are work items.

```yaml
- id: <step>
  activity: feature.state.project
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `machines` | map of map of string | no | Derived machine values per record id (as a string): {record_id: {machine: state}}. |
| `why` | map of string | no | Why prose per record id; the shown state's declared default otherwise. |
| `machine_why` | map of map of string | no | Per record id, prose per derive machine, written to its why_column: {record_id: {machine: text}}. |
| `guards` | map of list of string | no | The EXTERNAL guards that hold, per record id (as a string): {record_id: [guard, …]}. The bundle evaluates them; an edge behind one not listed here is not legal for that row. |
| `messages` | map of string | no | Chat-rail message override per CTA kind; the cta's own templated message otherwise. |
| `issue_fields` | map of object | no | Extra worklist columns per record id (bundle prose: name, contact, context). |
| `page_limit` | integer | no | Default `1000`. |
| `record_ids` | list of integer | no |  |
| `write` | boolean | no | Default `true`. |
| `results` | `all` / `changed` / `warn` | no | Default `"all"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows` | integer |  |
| `results` | list of ProjectedRow |  |
| `projected` | integer | Rows whose projection changed. |
| `unknown` | integer | Rows holding a value outside the graph. |
| `patched` | integer |  |
| `stale` | list of object |  |
| `worklist` | object | {open, resolved, upserted}. |

`ProjectedRow`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `outcome` | string | projected / unchanged / unknown_state |
| `status` | string |  |
| `tuple` | map of string |  |
| `ctas` | list of object |  |
| `why` | string |  |
| `warn` | boolean |  |
| `policy` | object |  |
| `changed` | list of string |  |
| `reason` | string |  |

### `feature.state.spec`

No arguments: the graph is the pinned manifest's.

```yaml
- id: <step>
  activity: feature.state.spec
```

Takes no arguments of its own.

**Returns**

| Field | Type | Notes |
|---|---|---|
| `table` | string |  |
| `status_column` | string |  |
| `status_values` | list of string | The Status column's whole vocabulary, in order. |
| `labels` | map of string | Status value → label. |
| `warn` | list of string | Status values that warn. |
| `work_items` | list of string | Status values that open a worklist item: the reds, and any state declared `work_item: true`. |
| `tones` | map of string | Status value → tone. |
| `machines` | map of MachineSummary |  |
| `events` | map of list of string |  |
| `hints` | map of string | Column → display hint. |
| `mermaid` | map of string | Machine → stateDiagram-v2. |
| `spine` | map of string | Machine → stateDiagram-v2 of the EXPECTED edges only. Every edge in `mermaid` is legal and most are rare, so a graph that draws them alike shows a lead routinely going straight from its first state to archived; this is the path it actually takes. A machine that marks nothing expected has no entry. |
| `edges` | map of list of MachineEdgeOut | Machine → its arrows, for a client drawing its own graph. Includes edges another machine's transition moves this one through `also:`, which a walk over transitions by machine misses entirely — that is how a whole arm of a graph ends up rendered as unreachable floating states. |
| `spec` | object | The states: section as declared. |

`MachineEdgeOut`:

| Field | Type | Notes |
|---|---|---|
| `on` | string |  |
| `source` | string | The state the edge leaves. Empty when an `also:` edge's `when:` never says, which is honest rather than a guess. |
| `target` | string |  |
| `expected` | boolean | Is this the path a row is expected to take, or only one it may? |
| `importance` | integer | How loudly to draw it, 1–10 on one scale across every machine of the spec (10 is the spine through the firm's decisions, 1 an internal machine's bookkeeping). Display only. |
| `via` | string | The machine whose transition declared it, for an `also:` edge. |

`MachineSummary`:

| Field | Type | Notes |
|---|---|---|
| `column` | string, optional |  |
| `overlay` | boolean |  |
| `derive` | boolean |  |
| `internal` | boolean |  |
| `initial` | string |  |
| `states` | list of string |  |
| `groups` | map of list of string |  |

### `feature.state.transition`

Fire one event on some rows.

`event` is `family.name` or the bare name when unique (a CTA's
`action`). `payload` feeds the edge's `payload_writes`,
`detail_from` and `then` inputs. `operation_key` is recorded on
the change stamp so a retried flow can be told from a second click.
`writes` merges the bundle's own columns into each applied row's
one patch.

```yaml
- id: <step>
  activity: feature.state.transition
  args:
    event: <string>
    record_ids: <array>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `machines` | map of map of string | no | Derived machine values per record id (as a string): {record_id: {machine: state}}. |
| `why` | map of string | no | Why prose per record id; the shown state's declared default otherwise. |
| `machine_why` | map of map of string | no | Per record id, prose per derive machine, written to its why_column: {record_id: {machine: text}}. |
| `guards` | map of list of string | no | The EXTERNAL guards that hold, per record id (as a string): {record_id: [guard, …]}. The bundle evaluates them; an edge behind one not listed here is not legal for that row. |
| `messages` | map of string | no | Chat-rail message override per CTA kind; the cta's own templated message otherwise. |
| `issue_fields` | map of object | no | Extra worklist columns per record id (bundle prose: name, contact, context). |
| `page_limit` | integer | no | Default `1000`. |
| `event` | string | yes |  |
| `record_ids` | list of integer | yes |  |
| `payload` | object | no |  |
| `operation_key` | string | no | Default `""`. |
| `writes` | map of RowWrites | no | Bundle writes per record id (as a string): {record_id: {rev, data}}; merged into the row's patch when the edge applies, refused StaleRev when rev moved. |
| `conversation_id` | string | no | Resolves $conversation_id in then inputs. Default `""`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `event` | string |  |
| `results` | list of TransitionRow |  |
| `applied` | integer |  |
| `launch` | integer | Rows whose edge is a flow to start. |
| `refused` | integer |  |
| `not_found` | integer |  |
| `patched` | integer |  |
| `stale` | list of object |  |
| `launches` | list of Launch | Every flow to start, across rows: flow edges and then entries, inputs resolved. |
| `first_refusal` | Refusal, optional | The first refused row, for a flow that fails by name when nothing applied. |
| `worklist` | object |  |

`Launch`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `flow` | string |  |
| `inputs` | object |  |

`Refusal`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `code` | string |  |
| `reason` | string |  |

`RowWrites`:

| Field | Type | Notes |
|---|---|---|
| `rev` | integer |  |
| `data` | object |  |

`TransitionRow`:

| Field | Type | Notes |
|---|---|---|
| `record_id` | integer |  |
| `outcome` | string | applied / launch / refused / not_found / unknown_state |
| `reason` | string |  |
| `code` | string |  |
| `delegated` | boolean | An external guard on the edge was vouched for by the caller; its own check is what allowed it. |
| `from_status` | string |  |
| `landing_status` | string |  |
| `tuple` | map of string |  |
| `flow` | string | The flow that IS this edge, to launch per row. |
| `launches` | list of Launch | Flows the edge launches for this row after its writes, inputs resolved. |
| `effects` | list of string | Bundle-side effects the edge declares; the bundle runs them for this row. |

## feature.xlsx

### `feature.xlsx.attach_row_images`

*Beta.*

Attach an XLSX's embedded images to the rows parsed from it.

```yaml
- id: <step>
  activity: feature.xlsx.attach_row_images
  args:
    conversation_id: <string>
    conversation_file_key: <string>
    rows_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the source XLSX and images (must be the flow's own conversation). |
| `conversation_file_key` | string | yes | Conversation-level source XLSX file key (file_uploads). |
| `rows_file_key` | string | yes | Staged rows blob from feature.xlsx.parse. Rows must still carry the `_xlsx_sheet` / `_xlsx_row` anchor bookkeeping. |
| `progress_after_seconds` | number | no | Minimum elapsed time before the first progress update. Default `2.0`. |
| `progress_every_seconds` | number | no | Minimum elapsed time between progress updates. Default `2.0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `rows_file_key` | string |  |
| `row_count` | integer |  |
| `image_count` | integer |  |

### `feature.xlsx.parse`

*Beta.*

Parse an uploaded XLSX workbook into generic rows.

```yaml
- id: <step>
  activity: feature.xlsx.parse
  args:
    conversation_id: <string>
    conversation_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the source XLSX (must be the flow's own conversation). |
| `conversation_file_key` | string | yes | Conversation-level source XLSX file key (file_uploads). |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | XlsxParseSource |  |
| `sheet_count` | integer |  |
| `row_count` | integer |  |
| `rows_file_key` | string |  |

`XlsxParseSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |
