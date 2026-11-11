---
id: on-error
title: Errors and retries
order: 21
group: How a Flow runs
summary: >
  Retry is the Flow's job: a Step with no `on_error` gets up to 4 attempts, so
  a Step whose side effect must not repeat, such as Questionnaire's email
  send, sets `retry: 0`. `policy: skip` continues with a null output and the
  error at `$steps.<id>.error`; `fallback` is accepted but runs as `fail`. A
  missing reference fails before the Activity runs, so no policy catches it.
lede: >
  How a Flow retries a failed Step, and how to stop a Step with side effects
  from running twice.
concepts: [flow-grammar, references, debugging-a-failed-run]
---

A [Step](https://docs.popcorn.ai/flow-grammar.md)'s `on_error:` decides what
its failure does to the [Run](https://docs.popcorn.ai/history.md) and how
often it is tried first.

```yaml
on_error: { policy: skip, retry: 1, backoff_seconds: 5 }
```

**No `on_error` means up to 4 attempts**, with a backoff between them.
`retry: N` means N retries after the first attempt, capped at 10, and
`backoff_seconds:` sets the wait before the first retry; each later wait
doubles. It needs a `retry` of 1 or more. A retryable error arrives after
the retries ran out. A non-retryable one — `foundation.workflow.fail`, or an
Activity's typed refusal such as a claim on a Row another Run holds — fails
on the first attempt.

## The policies

| `policy` | After the last attempt fails |
|---|---|
| `fail` (default) | the Run fails with the Step's error |
| `skip` | the Run continues; the Step's output is null and the failure is at `$steps.<id>.error`, as `type` and `message` |
| `fallback` | accepted by the grammar, but runs as `fail` — nothing is invoked in its place |

A Step skipped this way reads as null to every later reference, so a later
Step can gate on its output or pass it to `foundation.workflow.coalesce`;
see [value references](https://docs.popcorn.ai/references.md). `skip` keeps
the error readable too, so a later Step can still fail by the original error
once cleanup has run. A Run whose Step was skipped ends `succeeded`.

`on_error.retry` is refused on a block — retrying a group would repeat its
inner side effects, so put retries on the inner Steps — and on `call_flow`,
whose child runs exactly once and is bounded by `call_flow.timeout_seconds`.

## How Questionnaire chooses

The [Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md)
sets `on_error` by what a second attempt would do:

| Step | `on_error` | Why |
|---|---|---|
| `send`, `draft` in `ask_recipient`; `send_follow_up` in `check_recipient` | `{ policy: skip, retry: 0 }` | a send that timed out may still have gone, and a retry would email the recipient twice |
| `compose`, `decide`, `found`, `compose_follow_up`: code-block calls in the child Flows | `{ policy: skip, retry: 0 }` | a failure is the block refusing, which another attempt would repeat |
| `thread` (`feature.email.get_thread`), `read` (`foundation.agent.transform`) | `{ policy: skip }` | a read is safe to retry, and a failed one leaves the Row to be read on the next pass |
| `claim` (`foundation.store.claim_row`) in both child Flows | none | a refused claim is a typed refusal, which fails at once |
| `record` in both child Flows, `record_follow_up` (`foundation.store.patch_row`) | none | writing the same cells again changes nothing, and a write that still fails must fail the Run, so the Row is held or freed as the next section says |
| `ask`, `check`, `adopt`: the tick's `foreach` Steps | `{ policy: skip }` | one recipient's failure is a null item, and the rest of the pass carries on |
| `plan` in the tick | `{ retry: 0 }` | with no plan there is nothing to do, so the pass fails |
| `project`, `latch_onboarding`, `probe`, the `kick` that starts a pass | `{ policy: skip, retry: 1 }` | the next pass or Run repeats them |
| `apply` in `cta_apply` | `{ policy: fail, retry: 0 }` | an Action is applied once; when no Row took it, the Run fails by the first refusal |

```yaml title="ask_recipient.yaml"
  # No retry: a send that timed out may still have gone, and a second
  # attempt would email the recipient twice. A send that fails is skipped,
  # which commits nothing, so the Run frees the row and the next pass
  # asks again.
  - id: send
    when: $inputs.send_mode == 'send'
    activity: feature.email.send
    on_error: { policy: skip, retry: 0 }
    commits_leases: true
```

A send that fails here is not lost. `record` writes `Stage: waiting` only
when a thread came back, so the Run ends with the recipient still unasked,
and the [Row lease](https://docs.popcorn.ai/row-leases.md) its `claim` took
is freed when it ends. The next pass, fifteen minutes on, asks them. A
retry inside the Run could not know whether the first attempt's email
went; a later pass reads the Row and does.

## Skip before the send, fail after it

`ask_recipient` and `check_recipient` claim the Row's `Sending` Column as a
lease, and while it is held the tick passes the Row by and every Action on
it is refused. The platform frees it when the Run ends, so no Step has to
release it, and what `on_error` decides is which way the Run ends:

- **Before an email goes out**, a failure frees the Row whether the Run
  fails or succeeds. The Steps that reach outside the Run (the code block,
  the thread, the model) are skipped on error, so one recipient's bad read
  ends their Run quietly and the next pass tries again.
- **Once an email has gone**, the Run's lease is committed: `send`,
  `draft` and `send_follow_up` carry `commits_leases: true`. The Steps
  that record the send have no `on_error`, so a write that fails fails the
  Run, and a failed Run that committed keeps the Row held rather than free
  it to be emailed again. A skipped `record` would let the Run succeed and
  free the Row with the send unrecorded.

`check_recipient` writes what it found before it follows up, for the same
reason. Its `record` has no `on_error` either, and when it fails, nothing
has been sent: the Run fails by `record`'s own error, the lease frees the
Row, and the next pass checks the recipient again.

```yaml title="check_recipient.yaml"
  - id: record
    when: $steps.decide.output.patch
    activity: foundation.store.patch_row
    args:
      conversation_id: $inputs.conversation_id
      table_name: recipients
      record_id: $inputs.record_id
      patch: $steps.decide.output.patch
      change_kind: questionnaire_reply
      change_action: Checked for the recipient's reply

  - id: follow_up
    when: $steps.decide.output.follow_up
    steps:
      # … compose_follow_up, send_follow_up (commits_leases: true),
      # and record_follow_up, which has no on_error
```

> [!WARNING] A skipped record frees what it should hold
> On a Step that records a committed send, `on_error: { policy: skip }`
> lets the Run succeed, and a Run that succeeds frees its Rows, so the
> next pass sends again. Leave `on_error` off it. See
> [Row leases](https://docs.popcorn.ai/row-leases.md) for what a committed
> lease does on each outcome.

> [!TIP] A lease frees the Row for you
> A `claim_row` with no `holder:` is a lease the platform frees when the
> Run ends, however it ends, so no release Step is needed, and
> `commits_leases` keeps the hold once a send has gone. See
> [Row leases](https://docs.popcorn.ai/row-leases.md).

To see which recipients a pass skipped, ask for the failed Runs:

> "Did any of #team-offsite's recipients fail on the last pass?"

> [!TIP] MCP tool call
> Your assistant calls `list_runs` with `status: failed`, then `get_run`.

Each failed recipient is an `ask_recipient` or `check_recipient` Run of its
own, listed as started by another Run, while the pass that started it
succeeded.

## What no policy catches

A reference that names a key the value lacks raises `ReferenceError` while
the Step's arguments are resolved, before the Activity is invoked, so
`on_error` never sees it and a retry cannot fix it. Guarantee the key
upstream: in an `output_schema`'s `required`, or with `$exists: true` in the
query that produced the Rows. See
[value references](https://docs.popcorn.ai/references.md).

A `when:` that cannot be evaluated (`PredicateError`) is likewise an
authoring bug that fails the Run at once. Reading a failure end to end is
[debugging a failed Run](https://docs.popcorn.ai/debugging-a-failed-run.md).
