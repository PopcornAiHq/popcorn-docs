---
id: activities/catalog/feature/chase-forward
title: feature.chase.forward
order: 126
group: Activities
parent: activities/catalog/feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.chase.forward activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `feature.chase.forward` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

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
