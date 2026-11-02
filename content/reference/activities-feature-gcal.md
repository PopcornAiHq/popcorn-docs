---
id: activities-feature-gcal
title: feature.gcal
order: 132
group: Activities
parent: activities-feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.gcal activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.gcal` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

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
