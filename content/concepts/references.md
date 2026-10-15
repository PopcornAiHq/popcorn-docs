---
id: references
title: Value references
order: 10
group: How a flow runs
summary: >
  A `$` reference reads a value — `$inputs`, `$steps.<id>.output`, `$channel`,
  `$trigger` or a `foreach` alias — and computes nothing: no arithmetic, no
  negation. A malformed one is a literal string at runtime, and a key the value
  lacks is a hard ReferenceError that on_error cannot catch. Index arrays with
  dots, and keep spaces out of any column a flow dereferences.
concepts: [flow-grammar, on-error, table-columns]
applies_to: [cli, mcp, human]
source: [Ref, parse_ref, REFERENCE_PATTERN, Scope, resolve_value, ReferenceError, math_calculate]
---

A step's `args`, `when:` and `foreach:`, and a flow's `outputs:`, read values
through references.

| Root | Reads |
|---|---|
| `$inputs.*` | the run's declared inputs |
| `$steps.<id>.output.*` | a prior step's result |
| `$steps.<id>.<collect>` | a `foreach` step's collected list, under the name `collect:` gave it |
| `$steps.<id>.error` | a step skipped under `on_error: skip`: its `type` and `message` |
| `$channel.*` | channel config — `channel_parameters` plus the seeded `integrations` / `integration_list`; scalars are **not** here |
| `$trigger.*` | what triggered the run |
| `as:` name | the current item inside a `foreach` |

`$trigger` carries exactly `thread_id`, `message_id`, `user_id`,
`conversation_id`, `thread_root`, `contact_id`, `workflow_id`, `run_id` — a
closed set, so a typo in it is caught offline. Every key is always present;
one that does not apply to the run's trigger kind (`user_id` on a scheduled
run, say) resolves to null rather than erroring. `$channel` is not closed:
its keys come from a per-channel config the bundle cannot see, which is why
an unrecognized one is a warning. `workspace_id` is never an input; it rides
the auth context.

**A `foreach` alias shadows `$channel` and `$trigger`**, deliberately, so
`as: channel` or `as: trigger` keeps working. It does not shadow `$inputs` or
`$steps` — those resolve before aliases are consulted.

## The syntax, and what a near miss does

**A reference path is `[A-Za-z_][A-Za-z0-9_.]*` — no spaces.** The root and
the first segment after it start with a letter or underscore, and the whole
reference carries only letters, digits, underscores and dots. `$a.`, `$a..b`
and `$a.1b` are not references at all. `flow validate` flags one that starts
with a real root (`$steps.x.`, say) as a malformed reference; a flow that
ships one anyway resolves it as a literal string at runtime, which is a
silently wrong value rather than an error.

**Index arrays with dots, never brackets**: `$steps.x.output.ids.0`. Later
segments may be numeric, which means an array index. Brackets are rejected as
malformed and would be treated as a literal string.

A column a flow dereferences, as `$row.<Column>`, therefore needs a name with
no spaces; see [table columns](https://docs.popcorn.ai/concepts/table-columns.md).

## A missing key fails the run

A reference to a key the value does not have is a hard `ReferenceError`
(`$steps.normalize.output.details: key not found`) — only a null partway
along the path resolves to null. It is raised while the step's arguments are
resolved, before the activity is called, so `on_error` never sees it and a
retry cannot fix it. Guarantee the key upstream: make the property `required`
in the `output_schema` that produced it, or select rows with
`$exists: true`.

**Permissive output schemas validate any path.** Many activities declare
results with `additionalProperties: true`. For those,
`$steps.x.output.anything` passes `flow validate`, and at runtime a key the
response lacks is the same `ReferenceError`. Verify against the real
response, not the catalog.

**The DSL cannot reach sub-fields of an `object` input.**
`$inputs.payload.name` is statically unreachable, because an input
declaration has no way to describe an object's properties. Get a typed shape
first: see
[extracting fields or deriving them](https://docs.popcorn.ai/concepts/extract-or-derive.md).

## Nothing in a reference computes

You cannot write `$a + $b`, and you cannot even negate a reference —
`-$channel.minutes` is parsed as a literal string and fails type validation.
Arithmetic is `foundation.math.calculate`: one binary operation per step
(`left`, `operation: add | subtract | multiply | divide`, `right`), chained
through `$steps.<id>.output.value`. Consequences:

- **A counter belongs to the store, not to a read-add-write pair of steps.**
  `merge: increment_on_change` counts transitions under the row lock; two runs
  doing their own read and `add` can lose an increment.
- **Prefer an activity that names the direction.** A signed value is easy to
  get backwards, which is why `math.offset` takes `direction: subtract`
  rather than a negative duration.

**Time windows have their own activity.** `foundation.math.offset` shifts a
timestamp by a duration and returns `workflow.now`'s `{unix, unix_str, iso}`
shape, so its output drops straight into a filter:

```yaml
  - id: cutoff
    activity: foundation.math.offset
    args:
      iso: $steps.now.output.iso     # omit to shift from now
      direction: subtract            # durations stay non-negative
      hours: 6

  - id: stale
    activity: foundation.store.list_rows
    args:
      filter:
        Last Seen: { $lt: $steps.cutoff.output.iso }
```

Pass `iso` explicitly when several cutoffs must derive from the same instant.
