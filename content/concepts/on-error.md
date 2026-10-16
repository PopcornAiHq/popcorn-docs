---
id: on-error
title: Errors and retries
order: 12
group: How a flow runs
summary: >
  Retry is the flow's job: a step with no `on_error` gets up to 4 attempts, so
  any step with a side effect that must not repeat sets `retry: 0`.
  `policy: skip` continues with a null output and the error at
  `$steps.<id>.error`; `fallback` is accepted but runs as `fail`. A missing
  reference fails before the activity runs, so no policy catches it.
concepts: [flow-grammar, references, debugging-a-failed-run]
layer: platform
product_terms: []
---

A step's `on_error:` decides what its failure does to the run and how often
it is tried first.

```yaml
on_error: { policy: skip, retry: 1, backoff_seconds: 5 }
```

**No `on_error` means up to 4 attempts.** A step that is not idempotent —
one that sends, posts or charges — must set `retry: 0`, or a partial failure
repeats its side effect. `retry: N` means N retries after the first attempt,
capped at 10, and `backoff_seconds:` sets the wait before the first retry (it
needs a `retry` of 1 or more). A retryable error arrives after the retries ran
out. A non-retryable one — `foundation.workflow.fail`, or an activity's typed
refusal — fails on the first attempt.

## The policies

| `policy` | After the last attempt fails |
|---|---|
| `fail` (default) | the run fails with the step's error |
| `skip` | the run continues; the step's output is null and the failure is at `$steps.<id>.error`, as `type` and `message` |
| `fallback` | accepted by the grammar, but runs as `fail` — nothing is invoked in its place |

`skip` keeps the error readable, so a later step can still fail by the
original error once cleanup has run. A run whose step was skipped ends
`succeeded`; `popcorn flow runs get --include-errors` is how to see it.

`on_error.retry` is refused on a block — retrying a group would repeat its
inner side effects, so put retries on the inner steps — and on `call_flow`,
whose child runs exactly once and is bounded by `call_flow.timeout_seconds`.

## What no policy catches

A reference that names a key the value lacks raises `ReferenceError` while
the step's arguments are resolved, before the activity is invoked, so
`on_error` never sees it and a retry cannot fix it. Guarantee the key
upstream: in an `output_schema`'s `required`, or with `$exists: true` in the
query that produced the rows. See
[references in a flow](https://docs.popcorn.ai/platform/concepts/references.md).

A `when:` that cannot be evaluated (`PredicateError`) is likewise an
authoring bug that fails the run at once. Reading a failure end to end is
[debugging a failed run](https://docs.popcorn.ai/platform/guides/debugging-a-failed-run.md).
