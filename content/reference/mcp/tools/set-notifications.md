---
id: mcp/tools/set-notifications
title: set_notifications
order: 361
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-24
summary: >
  Read or change when and how Popcorn's notifications reach the person you
  work for.
concepts: []
---

[writes] [destructive] [idempotent]

```
set_notifications(changes=None, timezone=None)
```

Popcorn decides what is a notification; each person decides when and how it reaches them, by telling you: "only 9 to 7", "nothing at the weekend", "pause until 3pm", "I'm back", "Slack me for Needs you", "Following once a day at 8". Change only what they asked for. These are their own settings and no one else's can be set. With no arguments nothing changes. The reply is every setting as it now stands, theirs marked "(yours)" and the rest Popcorn's defaults: tell them what it says, including whether Popcorn delivers by these settings yet.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `changes` | `Optional[dict[str, Any]]` | Only the keys to change. A key replaces what was saved under it whole, and a key set to null goes back to the default. "hours": `{"start": "09:00", "end": "19:00", "weekends": false}`, when notifications may arrive: 24-hour HH:MM in their timezone. "`urgent_outside_hours`": true or false, whether Urgent still arrives outside those hours. "`pause_until`": nothing arrives before this time, ISO 8601 with its UTC offset and in the future, e.g. "2026-11-23T15:00:00+01:00". null ends a pause. "`hold_minutes`": 0 or more, the minutes a notification waits before it is delivered, so their agent can answer first. "sections": an object keyed by "urgent", "`needs_you`" or "following". A section given replaces that section whole, one set to null goes back to the default, and one not named is untouched. A section's keys, all optional: "delivery" ("now", "hourly", "3h", "`twice_daily`", "daily" or "`email_cadence`"), "`daily_at`" ("HH:MM"), "`group_by`" ("thread", "person" or "topic"), "detail" ("lines" or "counts"), "channels" (a list of "slack" and "popup"; [] is the bell only) and "escalate" (`{"after_minutes": 30, "to": "slack"}`, where one still unread goes next). |
| `timezone` | `Optional[str]` | Their IANA timezone, e.g. "Europe/Amsterdam", which the hours and `daily_at` are read in. |

**Example** — “Only notify me 9 to 7 on weekdays, and Slack me for Needs you.”

```text
→ set_notifications(changes={"hours": {"start": "09:00", "end": "19:00", "weekends": false}, "sections": {"needs_you": {"channels": ["slack"]}}}, timezone="Europe/Amsterdam")

Saved. Your notification settings now:
- Timezone: Europe/Amsterdam (yours)
- Hours: 09:00 (yours) to 19:00 (yours), weekends off (yours)
- Urgent outside those hours: yes
- Pause: none
- Hold: 0 minutes
- Urgent: delivery now; channels Slack DM if your workspace connected Slack, otherwise a browser pop-up; escalate none
- Needs you: delivery now; channels slack (yours); escalate none
- Following: delivery email_cadence; group_by thread; detail lines; channels Slack DM if your workspace connected Slack, otherwise a browser pop-up; escalate none
Popcorn does not deliver notifications by these settings yet: they are saved, and nothing changes until it does.
```
