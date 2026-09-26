---
id: debugging-a-failed-run
title: Debugging a failed run
order: 3
summary: >
  The loop after a flow run goes wrong: find the run, read its `outcome`
  rather than its status, read the failure with `flow runs get
  --include-errors`, fix, publish, and run again once the install lands. Also
  the runs that end `succeeded` having done nothing (a missing required
  integration, a skipped step) and the ones that never start.
concepts: [channel-binding, publish-and-apply, flow-identity, template-authoring]
applies_to: [cli, human]
source: [run_outcome, get_workflow_execution_detail, missing_required_integrations, InterpreterOutput, OnError, derive_delivery_status, reconcile_inflight_trigger_workflows, check_exact_dedup]
---

This guide starts from a flow run that did the wrong thing, or from one you
expected and cannot find, and ends with a fixed version running. Editing and
publishing are the loop in
[authoring an app bundle](https://docs.popcorn.ai/guides/template-authoring.md);
this page is the reading half of it.

Every command takes the channel as `--channel`, a `#name` or a UUID. The
examples write `<id>` for it.

## 1. Find the run

A run is addressed by its `workflow_id`. Where you get one depends on what
started it:

| Started by | Where its `workflow_id` is |
|---|---|
| `popcorn flow run` | printed as `workflow_id:`; with `--wait`, also on stderr as `Waiting for <id>...` |
| a webhook delivery | `wh-<delivery id>` — the `id` that `popcorn webhook deliveries` lists |
| anything else | `popcorn flow runs list` |

```bash
popcorn flow runs list --channel <id> --flow <name>                  # newest first
popcorn flow runs list --channel <id> --flow <name> --status closed --json
```

`--flow` takes the flow's `name:`, which is also what the list prints last on
each line. Two things about the list are easy to get wrong:

- **`--status failed` misses failures.** It selects the one status
  `Failed`. A run that timed out, was terminated or was cancelled also ended
  `failed` (§2) and is not in it. To see every finished run, use
  `--status closed` and read each run's `outcome`.
- **The text output has no `outcome` column.** It prints the raw status.
  `--json` carries `outcome` on every run, beside `trigger_source` (who asked
  for it: `app_user`, `agent`, `message`, `webhook`, … — a scheduled fire has
  none) and `task_queue`.

## 2. Read the outcome, not the status

Every run carries two fields. `status` is the raw engine status; `outcome` is
the platform's answer to "has it finished, and did it work". Branch on
`outcome` — `popcorn flow run --wait` does.

| `status` | `outcome` |
|---|---|
| `Completed` | `succeeded` |
| `Failed`, `TimedOut`, `Terminated`, `Canceled` | `failed` |
| `Running`, `ContinuedAsNew` | `still_running` |
| anything else | `still_running` |

`ContinuedAsNew` is in flight: the run carries on as a new run under the same
`workflow_id`, and reading the id again follows it. A status with no mapping
reads as `still_running` on purpose, so a caller keeps polling rather than
acting on an ending nobody proved.

`--wait` exits 1 when the run's outcome is `failed`, and 6 when its deadline
(`--timeout-run`, in seconds) passes while the run is still going — a
timeout, not a failure; the run may yet succeed.

`succeeded` means the run finished without an error. It does not mean the
flow did its work — §4 is the list of ways it can succeed having done
nothing.

## 3. Read why it failed

```bash
popcorn flow runs get <workflow-id> --channel <id> --include-errors
```

Without `--include-errors` a failed run still shows its `failure`; the flag
adds the activity failures that led to it, and on a run that succeeded it is
the only way to see a step that failed and was skipped. What each part says:

| Field | What it is |
|---|---|
| `failure` | The error that ended the run: `type`, `message`, and a `cause` chain the text output prints as `caused by:` lines. When the flow failed itself with `foundation.workflow.fail`, the `details:` map it passed is in that chain as `details`. |
| `error_history` | The activities that failed, most recent last, each with its `activity_type`, `attempt` and `message`. Capped to the newest entries. |
| `current_activities` | On a live run only: what is in flight, its attempt against its maximum, and `last_failure`, the error behind the current retry. This is why a run is stuck. |
| `outputs` | On a completed run only: the flow's declared `outputs:`. |

The detail names **activities, not step ids** — `foundation.store.upsert_rows`,
not `record_alert`. When a flow calls the same activity from several steps,
the message is what tells them apart.

The failures you will meet most:

- **`ReferenceError`** — `$steps.normalize.output.details: key not found`. A
  reference named a key the value did not have. It is raised while the step's
  arguments are resolved, before the activity is called, so `on_error` never
  sees it and a retry cannot fix it. Guarantee the key upstream: make the
  property `required` in the `output_schema` that produced it, or select rows
  with `$exists: true`. A `$channel.<name>` reference to a parameter the
  channel has not set fails the same way; `channel-config show` (§4) finds
  those before a run does.
- **An activity's own error.** The top of the chain is the activity failing,
  with no `type`; its `cause` carries the activity's error type and message.
  It arrives after the step's retries
  ran out: with no `on_error`, a step gets up to 4 attempts, and
  `on_error.retry: N` means N retries after the first. A non-idempotent step
  should set `retry: 0`, or a partial failure repeats its side effect.
- **`PredicateError`** — a `when:` expression that could not be evaluated,
  such as an ordered comparison between mismatched types. Like a reference
  error it is an authoring bug, and it fails the run at once.
- **`ChildFlowMissingIntegrations`** — a `call_flow` step with `mode: wait`
  whose child ended without running because its required integrations are not
  connected (§4). The parent fails rather than read empty outputs.

`on_error: {policy: skip}` turns a step's failure into a null output and puts
the error at `$steps.<id>.error`, as `type` and `message`, so a later step
can still fail by the original error once cleanup has run. `policy: fallback`
is accepted but runs as `fail`.

## 4. A run that succeeded and did nothing

**A required integration is not connected.** A flow's
`required_integrations:` is checked when a run starts. When one is not in the
channel config — or is connected to an account of a different provider than
the flow declares — the run stops before its first step and ends `Completed`,
`succeeded`, with empty `outputs`. That is deliberate: a scheduled tick on a
channel nobody has configured yet must not fail every interval. The run
detail does not say why it did nothing, so ask the channel:

```bash
popcorn channel-config show --channel <id> --strict
```

It compares every flow's `$channel.*` references and required integrations
with what the channel has. `missing_integrations`, `missing_parameters` and
`provider_mismatches` are the findings that break a run, and `--strict` exits
5 on any of them. Connect the account with
`popcorn channel-config integrations set`.

A run started by a person or an agent — `popcorn flow run` among them — is
refused at the start instead, with `missing_integrations` and the names, so
this quiet ending belongs to schedules, webhooks, message triggers and flows
started by other flows.

**A step failed and was skipped.** Under `on_error: skip` the run goes on
with the step's output null. `--include-errors` lists the failure even though
the run succeeded.

**It launched a run and finished.** `foundation.workflow.start_flow` starts a
separate run and returns at once, so the parent succeeds whatever the child
does. Find the child in `flow runs list --flow <child>`. When the parent needs
the child's result, a `call_flow` step with `mode: wait` fails with it.

## 5. A run that never started

**From a schedule.**

```bash
popcorn schedule list --channel <id>
popcorn schedule get <slug> --channel <id>
popcorn app status --channel <id>
```

`schedule get` shows whether the schedule is paused, its next and last run,
and counts of fires skipped because the previous run was still going
(`skipped (overlap)`) and fires missed (`missed (catchup)`). Its `note` is
written by whatever last rewrote the schedule, and is usually the only
explanation of a cadence that differs from the manifest. `app status` compares
the channel's armed schedules with the manifest's and exits non-zero on
drift. A schedule whose flow was renamed is dropped at install, with no error
— see [a flow's identity is its name](https://docs.popcorn.ai/concepts/flow-identity.md).

**From a webhook.**

```bash
popcorn webhook deliveries --channel <id> --status failed --json
popcorn webhook deliveries --channel <id> --include payload_raw --limit 5
```

The text output lists each delivery's `id`, webhook and time; its `status`
and `error_message` are in `--json`.

A `trigger_workflow` delivery is `processing` until a periodic reconcile
reads its run's ending, then `completed` or `failed`, with the run's error in
`error_message`. So a delivery can read `processing` for a while after its run
has ended, and the run itself (`wh-<delivery id>`) is the faster read. A
delivery is also `failed`, with no run at all, when its flow could not be
resolved — the webhook names no flow, or a flow the channel no longer has.
One whose run aged out of retention before the reconcile read it is `failed`
too.

A delivery whose body is byte-identical to one received in the last five
minutes is answered `{"status": "ok", "deduplicated": true}` and leaves no
delivery row, so it appears nowhere. When replaying a payload, change a field
that is not part of the identity your flow merges on.

**From anything.** `popcorn flow get <name> --channel <id>` prints the
trigger report: every schedule, webhook, message trigger, document, state and
flow that starts this one. A flow nothing starts is not broken; nothing asks
for it.

## 6. Which version the run ran

A run reads the channel's bound version once, when it starts, and keeps it to
the end, including the flows it calls — see
[how a channel runs a version](https://docs.popcorn.ai/concepts/channel-binding.md).
A fix published while a run is going does not reach that run, and a run that
started before the install landed ran the old version.

The run detail does not name the version. `popcorn flow run` does, in its
first line — `Started flow '<name>' (v<version_id>)` — and `app status` tells
you whether the channel is on its line's head yet:

```bash
popcorn app status --channel <id>    # run outside a checkout
```

`Install: CURRENT` means new runs get the head. `Install: PENDING` means the
channel still runs an older version, and the API cannot tell an install still
running from one that failed. `popcorn app apply --channel <id>` retries it
either way — see [publish and apply](https://docs.popcorn.ai/concepts/publish-and-apply.md).
Run from a checkout, `popcorn app status` says the same in other words —
`Channel runs the same version`, or `Channel still runs …` — and also diffs
your working copy against the head. `--json` carries `channel_behind` in both
forms.

## 7. Fix it and run it again

1. Stop what is still running, if it should not finish:

   ```bash
   popcorn flow runs cancel <workflow-id> --channel <id>
   popcorn flow runs cancel --flow <name> --channel <id>   # every running run of it
   ```

   A cancel lands at the run's next activity boundary; `--force` terminates on
   the spot, for a run that will not cancel.
2. Fix the bundle, then run the offline checks:
   `popcorn template check .` and `popcorn flow validate <flow>.yaml`. Neither
   catches a reference that is absent only at runtime — that is what the run
   just told you.
3. Publish: `popcorn app publish . --bump patch -m "..." --yes`. A publish
   reaches every channel on the line, not only this one.
4. Wait until `popcorn app status --channel <id>` reports `Install: CURRENT`,
   so the next run gets the fix.
5. Run it again the way it failed. `popcorn flow run <name> --channel <id>
   --inputs '...' --wait` for a direct run — check the version in its first
   line. For a webhook flow, `popcorn webhook send <webhook> @payload.json
   --channel <id>` with a body that differs from the last one (§5).
6. Confirm the effect, not the outcome: read the rows the run should have
   written (`popcorn table rows <table> --channel <id>`), since §4 is a list of
   runs that succeeded without writing any.
