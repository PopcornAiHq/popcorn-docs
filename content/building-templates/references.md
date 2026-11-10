---
id: references
title: Value references
order: 18
group: How a Flow runs
summary: >
  A `$` reference reads a value — `$inputs`, `$steps.<id>.output`, `$channel`,
  `$trigger` or a `foreach` alias — and computes nothing. A skipped or
  gated-out Step reads as null all the way down, but a key a real value lacks
  is a hard ReferenceError that on_error cannot catch, and a malformed
  reference is a literal string. Index arrays with dots.
lede: >
  How a Flow reads a value from its inputs, earlier Steps or the Routine, and
  what happens when the value isn't there.
concepts: [flow-grammar, on-error, table-columns]
---

A [Step](https://docs.popcorn.ai/flow-grammar.md)'s `args`, `when:` and
`foreach:`, a `call_flow`'s `inputs:` and a
[Flow](https://docs.popcorn.ai/flow-grammar.md)'s `outputs:` read values
through references. The
[Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md)'s
`check_recipient` reads from every root:

| Root | Reads | In `check_recipient` |
|---|---|---|
| `$inputs.*` | the Run's declared inputs | `$inputs.record_id`, the Row to check |
| `$steps.<id>.output.*` | a prior Step's result | `$steps.claim.output.row`, the Row as the claim read it |
| `$steps.<id>.<collect>` | a `foreach` Step's collected list, under the name `collect:` gave it | (in the tick: `$steps.check.checked`) |
| `$steps.<id>.error` | a Step skipped under `on_error: skip`: its `type` and `message` | — |
| `$channel.*` | the Routine's channel parameters, its prompts and its Connections | `$channel.integrations.inbox.id`, `$channel.prompts.read_answers` |
| `$trigger.*` | what started the Run | `$trigger.run_id`, the claim's holder |
| `as:` name | the current item inside a `foreach` | (in the tick: `$recipient.record_id`) |

## What `$channel` holds

`$channel` is the Routine's *channel config*: its
[Routine Settings](https://docs.popcorn.ai/routine-settings.md)' channel
parameters by name, plus what the Bundle seeds into it and the Connections
seeded at run time.

- **Channel parameters.** Questionnaire's Manifest declares
  `follow_up_days` and `max_follow_ups`, and the tick passes them to each
  check as `$channel.follow_up_days` and `$channel.max_follow_ups`.
- **Prompts.** Each file in the Bundle's `prompts/` folder is seeded as
  `$channel.prompts.<stem>`, so `prompts/read_answers.md.j2` is
  `$channel.prompts.read_answers`, which `check_recipient` hands to
  `foundation.agent.transform` with `prompt_format: jinja`.
- **Connections**, as `integrations` and `integration_list`. A Connection is
  keyed by its Manifest `config_name`: Questionnaire's Gmail is `inbox`, so
  every send reads `$channel.integrations.inbox.id`.

[Scalars](https://docs.popcorn.ai/scalar-tiers.md), including the switches
among Routine Settings, are not in `$channel`: Questionnaire reads
`popcorn.email_send_mode` with `foundation.store.get_scalar`, and its
questionnaire and reply-by date through the code block's `reads`.

`$channel` is not closed: its keys come from each Routine's own parameters
and Connections, which the Bundle cannot see, so an unrecognized one is a
warning offline and a `ReferenceError` at run time when the Routine lacks
it.

## What `$trigger` holds

`$trigger` carries exactly `thread_id`, `message_id`, `user_id`,
`conversation_id`, `thread_root`, `contact_id`, `workflow_id` and `run_id` —
a closed set, so a typo in it is caught offline. Every key is always
present; one that does not apply to the Run's Trigger kind (`user_id` on a
scheduled Run, say) resolves to null rather than erroring.

`run_id` identifies this one Run, which is why Questionnaire's claims use it
as the holder: `ask_recipient` and `check_recipient` write
`$trigger.run_id` into the Row's `Sending` Column, and a retry of the same
claim recognises its own id. `cta_apply` passes it as `operation_key`, and,
with only `action`, `record_ids` and `payload` as its inputs, reads the
Routine as `$trigger.conversation_id`. `workspace_id` is never an
input; it rides the auth context.

**A `foreach` alias shadows `$channel` and `$trigger`**, deliberately, so
`as: channel` or `as: trigger` keeps working. It does not shadow `$inputs` or
`$steps` — those resolve before aliases are consulted.

## A skipped Step reads as null

A Step that was gated out by its `when:`, or failed and was skipped under
`on_error: skip`, has a null output, and a path through a null resolves to
null however deep it goes. Questionnaire leans on this. In
`ask_recipient`, exactly one of `send` and `draft` runs, by `send_mode`, and
either may fail and be skipped; the next Step takes whichever produced a
thread:

```yaml title="ask_recipient.yaml"
  - id: thread
    activity: foundation.workflow.coalesce
    args:
      values:
        - $steps.send.output.thread_id
        - $steps.draft.output.thread_id
        - none
```

`$steps.send.output.thread_id` is null when `send` did not run, so
`coalesce` passes over it. The trailing `none` gives the two gates after it,
`record` and `release`, a word to compare against when nothing was written.
`check_recipient` does the same with its `decide` Step, and its `read` Step
is gated on `$steps.found.output.count`, which is null when the code block
failed.

## A missing key fails the Run

A key that a real value does not have is different: it is a hard
`ReferenceError` (`$steps.claim.output.row.Stage: key not found`), and only a
null partway along the path resolves to null. It is raised while the Step's
arguments are resolved, before the Activity is called, so `on_error` never
sees it and a retry cannot fix it.

> [!IMPORTANT] Guarantee the key upstream
> Make the property `required` in the `output_schema` that produced it, as
> `check_recipient` does for `answers`, or select Rows with
> `$exists: true`. Or hand the whole value to a code block, which can look
> inside it without failing the Run: Questionnaire passes
> `$steps.claim.output.row` to `compose` and `decide`, and reads no
> Column of it by reference.

**Permissive output schemas validate any path.** Many Activities declare
results with `additionalProperties: true`. For those,
`$steps.x.output.anything` passes `flow validate`, and at runtime a key the
response lacks is the same `ReferenceError`. Verify against the real
response, not the catalog. The code block's output is one of these: every
key `decide` returns, such as `patch`, `follow_up` and `settled`, is one its
`run()` always sets.

**The DSL cannot reach sub-fields of an `object` input.**
`$inputs.payload.name` is statically unreachable, because an input
declaration has no way to describe an object's properties. Get a typed shape
first: see
[extracting fields or deriving them](https://docs.popcorn.ai/extract-or-derive.md).

## The syntax, and what a near miss does

**A reference path is `[A-Za-z_][A-Za-z0-9_.]*` — no spaces.** The root and
the first segment after it start with a letter or underscore, and the whole
reference carries only letters, digits, underscores and dots. `$a.`, `$a..b`
and `$a.1b` are not references at all. `flow validate` flags one that starts
with a real root (`$steps.x.`, say) as a malformed reference; a Flow that
ships one anyway resolves it as a literal string at runtime, which is a
silently wrong value rather than an error.

**Index arrays with dots, never brackets**: `$steps.x.output.ids.0`. Later
segments may be numeric, which means an array index. Brackets are rejected as
malformed and would be treated as a literal string.

So a [Column](https://docs.popcorn.ai/table-columns.md) a Flow dereferences,
as `$row.<Column>`, needs a name with no spaces. Questionnaire's `Last Asked`
and `Follow Ups` have spaces, and no Flow reads them by reference: the claim
hands the whole Row to the code block, which reads them by name. A Column
name with a space is fine as a key a Flow writes, as in
`patch: { Last Asked: $steps.now.output.iso }`.

## Nothing in a reference computes

You cannot write `$a + $b`, and you cannot even negate a reference —
`-$channel.minutes` is parsed as a literal string and fails type validation.
Arithmetic is `foundation.math.calculate`: one binary operation per Step
(`left`, `operation: add | subtract | multiply | divide`, `right`), chained
through `$steps.<id>.output.value`. Questionnaire has none: the next
follow-up count, `$steps.decide.output.next_follow_ups`, is worked out in
the code block. Consequences:

- **A counter belongs to the store or to the code block, not to a
  read-add-write pair of Steps.** `merge: increment_on_change` counts
  transitions under the Row lock; two Runs doing their own read and `add`
  can lose an increment. Questionnaire's `Follow Ups` is safe because only
  the Run holding the Row's claim writes it.
- **Prefer an Activity that names the direction.** A signed value is easy to
  get backwards, which is why `math.offset` takes `direction: subtract`
  rather than a negative duration.

**Time windows have their own Activity.** `foundation.math.offset` shifts a
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
Questionnaire takes `now` once per Run, from `foundation.workflow.now`, and
passes its `iso` to every code-block call, so the block's date checks all
use the same instant.
