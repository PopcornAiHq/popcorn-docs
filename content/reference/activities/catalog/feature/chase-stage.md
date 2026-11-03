---
id: activities/catalog/feature/chase-stage
title: feature.chase.stage
order: 127
group: Activities
parent: activities/catalog/feature
layout: lookup
updated: 2026-11-03
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.chase.stage activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `feature.chase.stage` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

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
| `row_stage` | string |  |
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
