---
id: activities-foundation-memory
title: foundation.memory
order: 114
group: Activities
parent: activities-foundation
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The foundation.memory activities, with how a Step calls each and its
  arguments.
concepts: [activities, flow-grammar]
---

The `foundation.memory` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `foundation.memory.delete`

Delete a memory by id, or every memory at (category, key).

Pass `memory_id` (from `memory.list`), or `category` + `key`. An
id is checked to belong to this step's scope before deletion — a channel
step will not delete a workspace memory, or the reverse; a key match
deletes every row at that key so a raced duplicate goes too. An
absent memory is not an error — `deleted` is 0 — because a cleanup
step re-run must not fail the flow. Safe to retry for the same reason,
and `deleted` counts the logical operation, not the attempt: a delete
that committed before its response was lost is carried into the retry
via heartbeat details, so the count does not reset to 0.

```yaml
- id: <step>
  activity: foundation.memory.delete
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation). Required at every scope. |
| `scope` | `channel` / `workspace` | no | Who the memory belongs to. 'channel' (default) is this conversation's own memory — the entity the memory panel lists and the workflow and App Builder personas recall. 'workspace' is memory every channel in the workspace shares, written against the run's own workspace. 'workspace' is NOT private to the flow: the channel and dm agents mount that same entity read-write and unconfined, so an agent can rewrite or delete what a flow put there. Every workspace member can read it, none can delete it from a product surface, and concurrent writers from different channels are normal — use it for standing facts a flow can afford to rewrite, not for state it relies on. Default `"channel"`. |
| `memory_id` | string, optional | no | Id of the memory to delete. Exclusive with category + key. |
| `category` | string, optional | no | With `key`: the category to delete from. |
| `key` | string, optional | no | With `category`: the key whose memories to delete. |
| `key_field` | string | no | Metadata field that holds the key (see memory.upsert). Default `"key"`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `deleted` | integer | Rows this step deleted across all its attempts: 0 when nothing matched, >1 only when raced duplicates existed at the key. |

### `foundation.memory.list`

List memories at this scope, by exact category or by prefix.

Returns each memory's `id`, `category`, `key` (the value at
`key_field` in its metadata, or null), `content`, `extra_metadata`
and `updated_at`, in the API's listing order. Pages are walked for you;
`limit` bounds how many rows come back and a 1 MiB serialized-output
budget bounds their size (the output rides workflow history), and
`has_more` says whether either truncated. A single memory too large for
the budget fails the step non-retryably — narrow the filter or set
`include_content: false`. An exact
`category` is filtered by the API; `category_prefix` — and no filter
at all — lists every memory at the scope and filters worker-side, so a
scope holding thousands of memories pays for all of them on each call.
Budget that against the right denominator: the workspace entity is the
largest in the system, because the default `/memories` mount puts every
channel's free-form member learnings there, while a channel entity only
ever holds one channel's. Prefer an exact `category` at
`scope: workspace`. Set `include_content: false` for
a cheap key/category browse. `key` / `keys` are filtered by the API
too: reading a few keys out of a large category costs those rows, not
the category.

Read-only: safe to retry.

```yaml
- id: <step>
  activity: foundation.memory.list
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation; other conversations' memories are not readable). Required at every scope. |
| `scope` | `channel` / `workspace` | no | Who the memory belongs to. 'channel' (default) is this conversation's own memory — the entity the memory panel lists and the workflow and App Builder personas recall. 'workspace' is memory every channel in the workspace shares, written against the run's own workspace. 'workspace' is NOT private to the flow: the channel and dm agents mount that same entity read-write and unconfined, so an agent can rewrite or delete what a flow put there. Every workspace member can read it, none can delete it from a product surface, and concurrent writers from different channels are normal — use it for standing facts a flow can afford to rewrite, not for state it relies on. Default `"channel"`. |
| `category` | string, optional | no | Exact category to list, e.g. 'kb:page'. Exclusive with category_prefix. |
| `category_prefix` | string, optional | no | List every category starting with this prefix, e.g. 'kb:'. Exclusive with category. Filtered worker-side after listing everything at the scope. |
| `key` | string, optional | no | Only the memory (or memories, if duplicates raced) whose metadata key_field equals this value. Exclusive with keys. |
| `keys` | list of string, optional | no | Only memories whose metadata key_field is one of these (at most 200), in one call. Rows come back in listing order, not in the order of `keys`; a key with no memory is simply absent, and an empty list returns nothing. Exclusive with key. |
| `key_field` | string | no | Metadata field that holds a memory's key. Default 'key'; the app stores use 'fact_id' and 'page_key'. Default `"key"`. |
| `include_content` | boolean | no | When false, `content` is null on every row — a cheap way to see which keys and categories exist. Default `true`. |
| `limit` | integer | no | Maximum rows returned (1..500), applied after filtering. Fewer come back when the 1 MiB output budget fills first; `has_more` reports truncation by either. Default `100`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `memories` | list of MemoryRecord | Matching memories in listing order, at most `limit`. |
| `count` | integer | len(memories). |
| `has_more` | boolean | True when more memories matched than `limit` or the 1 MiB output budget allowed. |

`MemoryRecord`:

| Field | Type | Notes |
|---|---|---|
| `id` | string | The memory id (for memory.delete). |
| `scope` | `channel` / `workspace` | The scope this row was read at. Pass it back as the `scope` of a paired upsert or delete (`scope: $m.scope`) — a write-back that drops it silently targets the channel entity instead. |
| `category` | string, optional | The memory's category. |
| `key` | string, optional | Value of `key_field` in the memory's metadata, if any. |
| `content` | object, optional | The stored JSON object (a string upsert is stored as {text: …}); null when include_content is false. |
| `extra_metadata` | object | The memory's metadata. |
| `updated_at` | string | ISO-8601 last-write timestamp. |

### `foundation.memory.upsert`

Create or update the memory at (category, key); never a near-duplicate.

Looks the key up in `category` (or, with `match_category_prefix`,
under every category with that prefix — so a memory whose category
changed is moved rather than duplicated), then updates the first match in
place or creates the row when absent. Same `content` and same
`category` is a no-op: nothing is written and `updated_at` does not
move, so applying the same block output twice writes once. Metadata is
written as `extra_metadata` plus `{key_field: key}` plus the view
stamp `view: {app, version_id, view?}` (this run's app and version,
and `view` when the version lists it in `ui.memory.views`), and is
not part of the
unchanged check.

A string `content` is stored as `{"text": …}`. Safe to retry: a retry
that follows a create whose response was lost finds the row and updates.

```yaml
- id: <step>
  activity: foundation.memory.upsert
  args:
    conversation_id: <string>
    category: <string>
    key: <string>
    content: ...
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID (must match the run's conversation). Required at every scope. |
| `scope` | `channel` / `workspace` | no | Who the memory belongs to. 'channel' (default) is this conversation's own memory — the entity the memory panel lists and the workflow and App Builder personas recall. 'workspace' is memory every channel in the workspace shares, written against the run's own workspace. 'workspace' is NOT private to the flow: the channel and dm agents mount that same entity read-write and unconfined, so an agent can rewrite or delete what a flow put there. Every workspace member can read it, none can delete it from a product surface, and concurrent writers from different channels are normal — use it for standing facts a flow can afford to rewrite, not for state it relies on. Default `"channel"`. |
| `category` | string | yes | Category to write, e.g. 'quotes:vendor' or 'kb:page'. |
| `key` | string | yes | Caller-chosen identity of this memory within its category, stored in the metadata at key_field. |
| `key_field` | string | no | Metadata field that holds the key. Default 'key'; use 'fact_id' / 'page_key' to interoperate with the app stores. Default `"key"`. |
| `content` | object or string | yes | What to remember: a JSON object, or a string (stored as {text: …}). |
| `extra_metadata` | object | no | Additional metadata to store alongside the key, e.g. {derived: true}. |
| `view` | string, optional | no | The view of this app's that draws the memory on the workspace Memory tab: a name the manifest lists under `ui.memory.views`. Omit for the app's default memory view. Every write is stamped with this app and version whatever is passed; a name the version does not declare is dropped with a warning, never an error. |
| `match_category_prefix` | string, optional | no | Look the key up under every category with this prefix instead of `category` alone, and move a match to `category` if it differs. `category` must start with it. Use when one key can change category over time (the automation facts do). Costs a walk of every memory at the scope on each call that creates (the API has no prefix filter), which at scope: workspace means every channel's agent learnings too — avoid it inside a foreach there. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `memory_id` | string | Id of the memory written or kept. |
| `action` | `created` / `updated` / `unchanged` | created: new row; updated: content or category changed; unchanged: identical content and category, nothing written. |
