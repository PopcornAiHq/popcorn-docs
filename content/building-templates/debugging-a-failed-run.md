---
id: debugging-a-failed-run
title: Debug a failed Run
order: 22
group: How a Flow runs
summary: >
  When a Routine's work goes wrong: find the failed Run with list_runs, read
  its error, inputs and Steps with get_run, or an Item's History with
  list_history; check Connections and the Install with get_routine; fix with
  create_routine_version and run it again. Also Runs that succeed doing
  nothing. The CLI adds Webhook Deliveries, the full timeline and the
  Version a Run pinned.
lede: >
  Find out why a Routine's work went wrong, fix it, and run it again.
concepts: [versions, flow-grammar, template-authoring, on-error]
---

This guide starts from a Run that did the wrong thing, or one you expected
and cannot find, and ends with a fixed
[Version](https://docs.popcorn.ai/versions.md) running. Its example is
`#team-offsite`, the [Routine](https://docs.popcorn.ai/routines.md) from
[Set up your first Routine](https://docs.popcorn.ai/set-up-a-routine.md),
whose [Flows](https://docs.popcorn.ai/flow-grammar.md) are those of the
[Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md).
Editing and publishing are the loop in
[changing a Routine Template](https://docs.popcorn.ai/template-authoring.md);
this page is the reading half of it.

A Routine's Runs are part of its
[History](https://docs.popcorn.ai/history.md). Each step below starts with
a prompt you might give your assistant. What only the CLI can show, and the
CLI form of each step, is in [With the CLI](#with-the-cli) at the end.

## Find the failed Run

> "Why did #team-offsite's last Run fail?"

> [!TIP] MCP tool call
> Your assistant calls `list_runs` with `status: failed`, then `get_run`
> with the newest one's reference.

`list_runs` lists the Routine's Runs, newest first, whatever started them:
each pass of the Schedule, each recipient's child Run, and each Action a
person took. Each line names the Flow the Run is doing, how it ended and
what started it. `get_run` shows one: what started it, its inputs and
outputs, its newest Steps and the error it failed with. Here is one from a
Copy whose Ask again Transition wrote `Last Asked: ""`, a mistake easy to
make in your own Copy:

```
- cta apply: failed · started by a person's button
Failed with: StoreApplyFailed: store write 0 (patch_rows from
  'state_patches') failed after 0 write(s) applied: agent_store 422
  validation_failed: Last Asked: not a valid ISO 8601 datetime
Inputs: {"action": "ask_again", "payload": {}, "record_ids": [1292020]}
Steps, newest first:
- apply · failed · 0.2s · StoreApplyFailed: …
```

Read it from the bottom up. The Flow is `cta_apply`, the
[Action](https://docs.popcorn.ai/actions-and-status.md) is `ask_again`,
and the failed Step is `apply`, which calls `feature.state.transition`. The
store refused one Cell: `Last Asked` is a `datetime`
[Column](https://docs.popcorn.ai/table-columns.md), and something wrote a
value to it that is not a date. Besides `Stage` and the Status, Why and Actions
projected from it, `apply` writes only what the Transition's `writes:`
names, so that is where to look. Questionnaire's own Transition empties
the Column the way the store takes:

```yaml title="manifest.yaml"
    - on: staff.ask_again
      from: no_response
      to: waiting
      writes: {Follow Ups: 0, Last Asked: null}
```

A datetime Column is emptied with `null`; the store refuses `""`, so a
`writes:` with `Last Asked: ""` fails every Ask again this way. `apply` is `{ policy: fail, retry: 0 }`, so the Run
failed on its first attempt and changed nothing.

> [!NOTE] A pass that succeeds can hide a failed recipient
> The tick runs one `ask_recipient` or `check_recipient` per recipient,
> under `on_error: skip`, so a recipient whose Run failed leaves the pass
> `succeeded`. `list_runs` lists that child Run as failed, started by
> another Run. See [errors and retries](https://docs.popcorn.ai/on-error.md).

## Read why it failed

`get_run` shows what it can read of one Run:

- **`Failed with:`** the error that ended the Run, at the bottom of its
  chain of causes. Only a Run that failed records one; a Run that was
  stopped has none.
- **`Now:`** on a Run still going, the Activity in flight, its attempt
  against its maximum, and why the last attempt failed. This is why a Run
  is stuck. Pass `wait_seconds` to have the call wait for the Run to end.
- **`Inputs:`** what the Run was started with. A child started by
  `call_flow` may lack a large input it reads from its parent's history
  instead.
- **Outputs**, on a Run that ended: the Flow's declared `outputs:`. Ones
  too long to show together are listed by name, and your assistant reads
  one whole by naming it.
- **Steps, newest first:** the newest of them, each with its Step id, how
  it ended, how long it took, its attempt when it was retried, and a failed
  Step's message.

The failures you will meet most:

- **`ReferenceError`** — `$steps.normalize.output.details: key not found`. A
  reference named a key the value did not have. It is raised while the Step's
  arguments are resolved, before the Activity is called, so `on_error` never
  sees it and a retry cannot fix it. Guarantee the key upstream: make the
  property `required` in the `output_schema` that produced it, or select Rows
  with `$exists: true`. The one place a missing key does not fail the Run is
  the Flow's top-level `outputs:`: resolved after the last Step, it is retried
  by the engine and the Run stays running with nothing in flight — stop it
  and fix the reference. A `$channel.<name>` reference to a parameter the
  Routine has not set in its Routine Settings fails the same way; a
  `create_routine_version` dry run warns of those before a Run meets one.
- **An Activity's own error.** The Activity fails with its own error type
  and message. A retryable error arrives after the Step's retries ran out:
  without `on_error.retry` a Step gets up to 4 attempts, and `retry: N`
  means N retries after the first. A non-retryable error —
  `foundation.workflow.fail`, or an Activity's typed refusal — fails on the
  first attempt. A non-idempotent Step should set `retry: 0`, or a partial
  failure repeats its side effect.
- **`PredicateError`** — a `when:` expression that could not be evaluated,
  such as an ordered comparison between mismatched types. Like a reference
  error it is an authoring bug, and it fails the Run at once.
- **`ChildFlowMissingIntegrations`** — a `call_flow` Step with `mode: wait`
  whose child ended without running because its required Integrations are not
  connected (see "A Run that succeeded and did nothing"). The parent fails rather than read empty outputs.

`on_error: {policy: skip}` turns a Step's failure into a null output and puts
the error at `$steps.<id>.error`, as `type` and `message`, so a later Step
can still fail by the original error once cleanup has run. `policy: fallback`
is accepted but runs as `fail`.

## Read what a pass did

> "What did #team-offsite's last pass do?"

> [!TIP] MCP tool call
> Your assistant calls `list_runs` with `status: ended`, then `get_run` on
> the newest `questionnaire tick`.

The pass's outputs say what it did, one item per child Run that finished:

```
Outputs: {"asked": [],
  "checked": [{"flow_name": "check_recipient",
               "outputs": {"followed_up": null, "record_id": 1292020,
                           "replies": 0, "status": "waiting"},
               "workflow_id": "…-questionnaire_tick-…-check[0]"}, …],
  "ready": true, "waiting": 0}
```

- **`ready: false`** means the code block's `plan` found no questions, or
  Gmail could not send, and asked and checked nobody.
- **`asked` and `checked`** hold one item per child that finished; a
  recipient whose child failed is missing from them, not listed as null.
- **`waiting`** counts recipients past this pass's cap of first emails, who
  are asked on the next pass.
- A child's `workflow_id` is the pass's, then the Step id and the item's
  index: `check[0]` is the first recipient `check` ran.

## Read one Item's History

> "What happened to Jane in #team-offsite?"

> [!TIP] MCP tool call
> Your assistant calls `list_rows` to find Jane's Row, `list_history` with
> its `row_id`, then `read_history_entry` on the change it wants to show.

- **`list_history`**, with the `routine` and an Item's `row_id`, lists that
  Item's changes newest first, each with who or what made it and its
  `entry_id`, and under them the Runs that changed it and how each ended.
  Questionnaire names each change: "Started emailing the questionnaire",
  "Sent the questionnaire", "Couldn't email the questionnaire; will try
  again".
- **`read_history_entry`**, with an `entry_id`, shows that one change in
  full: every field it changed, before and after, and, when a Run made it,
  what the Run did, step by step in order, each with its outcome and any
  failure message, and how the Run ended.
- **`list_history` with `run`** in place of `row_id` follows one Run: how it
  is going or how it ended, with its failure message, and the Items it
  changed, or what it did when it changed none. It takes the Run reference
  `run_trigger` and `list_runs` return.

> [!NOTE] Where History stops
> A Run is listed under an Item only when it wrote to that Item, so a Run
> that failed before writing anything is in no Item's History, though
> `list_runs` finds it. In a Workspace that guards personal data, a failure
> shows only that a Step failed, not its message. And the MCP tools name a
> Run by a reference of their own, never by its `workflow_id`, which is how
> the CLI addresses a Run.

## A Run that succeeded and did nothing

`succeeded` means the Run finished without an error. It does not mean the
Flow did its work. These are the ways it can succeed having done nothing.

**A Step failed and was skipped.** Under `on_error: skip` the Run goes on
with the Step's output null, and ends `succeeded`. `get_run` still lists
the Step as failed, with its message, among the newest Steps. In
`ask_recipient`, a `send` that failed is skipped, `release` empties
`Sending`, and the Row's History says "Couldn't email the questionnaire;
will try again": the next pass asks the recipient again.

**A child failed under the pass.** The tick's `ask` and `check` Steps skip
a failed child, so the pass succeeds without it; see "Read what a pass did"
above. `list_runs` with `status: failed` lists the child, named
`ask recipient` or `check recipient`.

**The code block decided there was nothing to do.** Questionnaire's
`plan` asks nobody while the questionnaire has no questions or Gmail cannot
send, and reports `ready: false`; it asks nobody new before the reply-by
date is set or after it has passed, or while `popcorn.email_send_mode` is
`off`. Those are the template's rules, not failures, and
[the Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md)
lists them.

**A required Integration is not connected.** A Flow's
`required_integrations:` is checked when a Run starts. When one is not among
the Routine's [Connections](https://docs.popcorn.ai/connections.md) — or is
connected to an account of a different provider than the Flow declares —
the Run stops before its first Step and ends `succeeded`, with empty
outputs. That is deliberate: a scheduled tick on a Routine nobody has
configured yet must not fail every interval. The Run does not say why it
did nothing, so ask the Routine:

> "Is anything #team-offsite needs not connected?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine`, then `list_connections`, and
> `make_connection` for one that is missing.

`get_routine` lists each account or Webhook the template needs, and whether
it is connected; `list_connections` says whose account each uses and what
stops while it is missing. A `create_routine_version` dry run also warns
when the Bundle's Flows use an Integration or a `$channel.*` parameter the
Routine lacks, or an account of the wrong provider.

A Run started by a person or an agent is refused at the start instead,
naming the missing Integrations. So this quiet ending belongs to Schedules,
Webhooks, Message Triggers and Flows started by other Flows.

> [!NOTE] Questionnaire checks Gmail itself
> Questionnaire's Flows declare no `required_integrations`: the tick's
> `probe` Step asks `feature.email.check_connected` whether Gmail can send,
> and `plan` reports `ready: false` when it cannot. So a pass on a Routine
> without Gmail runs its Steps and asks nobody.

**It launched a Run and finished.** `foundation.workflow.start_flow` starts a
separate Run and returns at once, so the parent succeeds whatever the child
does; so does a `call_flow` Step with `mode: detach`. `questionnaire_load`
ends this way, by starting a pass with its `kick` Step. Find the child in
`list_runs`. When the parent needs the child's result, a `call_flow` Step
with `mode: wait` fails with it.

## A Run that never started

**From a Schedule.**

> "Is #team-offsite's schedule running?"

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, then `get_routine`.

`list_triggers` shows each Schedule's cadence and the Flow it starts, and
says when one is paused. Questionnaire's tick is `overlap: skip`, so a pass
that runs past fifteen minutes skips the next fire. A Schedule whose Flow
was renamed is dropped at Install, with no error — see
[a Flow's identity is its name](https://docs.popcorn.ai/flow-grammar.md#a-flow-s-identity-is-its-name) —
so a Schedule missing from the list is one the Manifest no longer installs.

> "Run #team-offsite's Schedule now."

> [!TIP] MCP tool call
> Your assistant calls `list_triggers`, then `run_trigger`.

`run_trigger` runs the Schedule once now, with the inputs it runs with on
schedule, and only a Schedule the Routine's template declares. When a Run
of the Schedule is already going, nothing new starts. A started Run comes
back with its reference, for `get_run`.

**From a Webhook.** Questionnaire has none. For a template that does,
`list_triggers` lists its Webhooks and the Flow each starts, and
`list_runs` marks a Run a Webhook started `by a webhook`. A
Delivery that started no Run at all is read only in the CLI.

A body byte-identical to one the same Webhook accepted less than five
minutes earlier is answered `{"status": "ok", "deduplicated": true}` and
leaves no Run and no Delivery, so it appears nowhere. The window runs from
the first accepted copy, and repeats do not extend it. When replaying a
payload, change a field that is not part of the identity your Flow merges
on.

**From anything.** `list_triggers` lists everything that starts work in
the Routine: its Schedules, Webhooks, messages and documents, each with the
Flow it starts. A Flow none of them starts runs only when something runs it
directly, or from a State or another Flow.

## Which Version the Run ran

A Run reads the Routine's bound Version once, when it starts, and keeps it to
the end. Its `call_flow` children share that Version; a Run started with
`start_flow` reads the binding afresh — see
[a Run keeps the Version it started on](https://docs.popcorn.ai/versions.md#a-run-keeps-the-version-it-started-on).
A fix published while a Run is going does not reach that Run, and a Run that
started before the Install landed ran the old Version.

> "Is #team-offsite on the version I just published?"

> [!TIP] MCP tool call
> Your assistant calls `get_routine`, with `wait_seconds` to wait for an
> Install that is running.

`get_routine` names the Version the Routine runs, where its updates come
from, and whether its latest Install landed. `Install: installed` means new
Runs get the latest Version. Every other state means the Routine still runs
an older one, and says why:

| State | What it means |
|---|---|
| `installing` | an Install is running, on its first attempt |
| `retrying` | the running Install has failed at least once; the last error follows |
| `locked` | its template's updates are locked on the Routine, so nothing will move it |
| `failed` | the last Install failed, with its error |
| `skipped` | the last Install was skipped, with its reason |
| `behind` | nothing explains it: no Install was started, or it is gone from history |

`locked`, `failed`, `skipped` and `behind` say what moves the Routine on;
`installing` and `retrying` do not, since the Install is still running. A
failure inside the platform, which no edit or Publish fixes, also names the
Install's workflow, to report it with. When the Install could not be read
live, the answer says it comes from the database alone, and a running
Install does not show. See [Versions](https://docs.popcorn.ai/versions.md).

The Version one Run pinned is read only in the CLI.

## Fix it and run it again

1. Stop what is still running, if it should not finish:

   > "Stop that run in #team-offsite."

   > [!TIP] MCP tool call
   > Your assistant calls `list_runs`, then `stop_run`.

   The Run stops at its next Step; a Step already under way finishes, and
   what the Run already did stays done.
2. Fix the Bundle and check it:

   > "Fix the Ask again Transition on #team-offsite's copy to write
   > `Last Asked: null`, and check it."

   > [!TIP] MCP tool call
   > Your assistant calls `read_routine_file`, then
   > `create_routine_version` without `confirm`, which is a dry run.

   The dry run shows the diff and every check the Version would fail, and
   warns of a changed Flow that fails validation. It does not catch a
   reference that is absent only at runtime, or a value the store refuses,
   such as the `""` above — that is what the Run just told you.
3. Publish:

   > "Publish it."

   > [!TIP] MCP tool call
   > Your assistant calls `create_routine_version` with `confirm=true` and
   > the `plan_id` from its dry run.

   A Publish reaches every Routine on the Copy, not only this one.
4. Wait until `get_routine` says `Install: installed`, so the next Run gets
   the fix. `failed`, `skipped`, `locked` or `behind` will not clear by
   waiting: follow what it says moves the Routine on (see "Which Version
   the Run ran").
5. Run it again the way it failed. For an Action, take it again:

   > "Ask Jane again in #team-offsite."

   > [!TIP] MCP tool call
   > Your assistant calls `list_actions`, then `take_action`.

   For a scheduled Flow, run the Schedule now (see "A Run that never
   started"). A direct Run with the failed Run's inputs, and a Webhook
   payload, are sent from the CLI.
6. Confirm the effect, not the Outcome: read the Rows the Run should have
   written. For Ask again, Jane's Row should be back at *Waiting*, with
   `Follow Ups` at 0, and the next pass should follow up. A Run can succeed
   without writing any; see "A Run that succeeded and did nothing".

   > [!TIP] MCP tool call
   > Your assistant calls `get_row`, or `list_history` for what changed.

## With the CLI

Webhook Deliveries, sending a Webhook a payload, running a Flow directly
with chosen inputs, a Run's full timeline and Activity failures, the
Version one Run pinned and a Schedule's fire counts have no MCP equivalent
today; the rest is the CLI form of the steps above.

The CLI calls a Routine a *channel*: its commands take one as `--channel`, a
`#name` or a UUID, and the examples write `<channel>`.

### Find the Run in the CLI

A Run is addressed by its `workflow_id`. Where you get one depends on what
started it:

| Started by | Where its `workflow_id` is |
|---|---|
| `popcorn flow run` | printed as `workflow_id:`. With `--wait` nothing is printed until the Run succeeds; a failure or timeout names the id in its error, and stderr shows `Waiting for <workflow-id>...` unless `--quiet` or agent mode |
| a Webhook Delivery | `wh-<delivery id>` — the `id` that `popcorn webhook deliveries` lists |
| a `call_flow` Step | the parent's `workflow_id`, then `-<step id>`, and under `foreach` the item's index: `…-check[0]` |
| anything else | `popcorn flow runs list` |

```bash
popcorn flow runs list --channel <channel> --flow check_recipient           # newest first
popcorn flow runs list --channel <channel> --flow cta_apply --status failed --json
```

`--flow` takes the Flow's `name:`, which is also what the list prints last on
each line. `--status` filters by Outcome (see "Read the Outcome, not the status"): `failed` is every Run whose
Outcome is `failed`, whether it failed, timed out, was terminated or was
cancelled, and `closed` is every Run that finished either way. A
`ContinuedAsNew` Run is in neither, and not in `running` either: its work
carries on in the new Run, which `running` lists.

The text output has no `outcome` column; it prints the raw status. `--json`
carries `outcome` on every Run, beside `trigger_source` (who asked for it:
`app_user`, `agent`, `message`, `webhook`, … — a scheduled fire has none) and
`task_queue`.

### Read the Outcome, not the status

Every Run carries two fields. `status` is the raw engine status; `outcome` is
the platform's answer to "has it finished, and did it work". Branch on
`outcome` — `popcorn flow run --wait` does.

| `status` | `outcome` |
|---|---|
| `Completed` | `succeeded` |
| `Failed`, `TimedOut`, `Terminated`, `Canceled` | `failed` |
| `Running`, `ContinuedAsNew` | `still_running` |
| anything else | `still_running` |

`ContinuedAsNew` is in flight: the Run carries on as a new Run under the same
`workflow_id`, and reading the id again follows it. A status with no mapping
reads as `still_running` on purpose, so a caller keeps polling rather than
acting on an ending nobody proved.

`--wait` exits 1 when the Run's Outcome is `failed`, and 6 when its deadline
(`--timeout-run`, in seconds) passes while the Run is still going — a
timeout, not a failure; the Run may yet succeed.

### Read why it failed in the CLI

```bash
popcorn flow runs get <workflow-id> --channel <channel> --include-errors
```

Without `--include-errors` a `Failed` Run still shows its `failure`; the flag
adds the Activity failures that led to it, and on a Run that succeeded it
lists a Step that failed and was skipped, however far back. A Run that timed
out, was terminated or was cancelled has `failure: null` — only a `Failed`
Run records one. `details` and `outputs` are in `--json` only; the text
output omits them. What each part says:

| Field | What it is |
|---|---|
| `failure` | The error that ended the Run: `type`, `message`, and a `cause` chain the text output prints as `caused by:` lines. When the Flow failed itself with `foundation.workflow.fail`, the `details:` map it passed is in that chain as `details`. An Activity's own error has no `type` at the top; its `cause` carries the Activity's error type and message. |
| `error_history` | The Activities that failed, most recent last, each with its `activity_type`, `attempt` and `message`. Capped to the newest entries. An Activity that timed out rather than failed is not listed. |
| `current_activities` | On a live Run only: what is in flight, its attempt against its maximum, and `last_failure`, the error behind the current retry. This is why a Run is stuck. |
| `outputs` | On a completed Run only: the Flow's declared `outputs:`. |
| `inputs` | The inputs the Run was started with — what to pass to run it again. A child started by `call_flow` may lack a large input it reads from its parent's history instead. |
| `version_id` | The Version of the template the Run pinned, printed as `version:`. Null (`-`) until the Run has pinned, and on Runs older than the field. |

The detail names **Activities, not Step ids** — `foundation.store.patch_row`,
not `record` or `release`, which in `check_recipient` call the same one. The timeline names both:

```bash
popcorn flow runs timeline <workflow-id> --channel <channel>
```

It lists every Activity, timer and signal in the Run, newest first, one per
line: the event id, when it was scheduled, its kind and outcome, how long it
took, the attempt, the Activity or timer name and — last — the Step id (`-`
when there is none), with a failed Step's message under it. The Run's own status and Outcome head the page. A
page holds 50 entries unless `--limit` (up to 200) says otherwise; when older
ones remain, the last line gives the `--before <n> --run-id <id>` flags that
fetch them, and `--json` carries the same flags as `pagination.next`. Keep
the Run id on every page: without it the command reads the workflow's latest
Run.

### A Routine missing an Integration or a setting

```bash
popcorn channel-config show --channel <channel> --strict
```

It compares every Flow's `$channel.*` references and required Integrations
with what the Routine has. `missing_integrations`, `missing_parameters` and
`provider_mismatches` are the findings that break a Run, and `--strict` exits
5 on any of them. Connect the account with
`popcorn channel-config integrations set`. A Run that stopped this way reads
`Completed`, `succeeded`, with empty `outputs`. A `popcorn flow run` refused
for a missing Integration gets HTTP 409 `missing_integrations` with the
names, which the CLI exits 3 on.

### Schedules, Webhooks and Trigger Reports

```bash
popcorn schedule list --channel <channel>
popcorn schedule get questionnaire-tick --channel <channel>
popcorn app status --channel <channel>
```

`schedule get` shows whether the Schedule is paused, its next and last Run,
and counts of fires skipped because the previous Run was still going
(`skipped (overlap)`) and fires missed (`missed (catchup)`). Its `note` is
written by whatever last rewrote the Schedule, and is usually the only
explanation of a cadence that differs from the Manifest. `app status`
compares the Routine's armed Schedules with the Manifest's. It prints a
difference the platform explains — a `set_app_mode` retune, a spread
offset — as a `note`, and exits non-zero only on one it cannot: a cadence
or a pause nothing explains, or a declared Schedule that was never
installed.

`popcorn schedule trigger questionnaire-tick --channel <channel>` runs the
Schedule once now, with the inputs the Schedule stores. It takes the same
slug, Flow id or `schedule_id` as `schedule get`, and runs only a Schedule
the Routine's bound Manifest declares. It prints the Run's `workflow_id`
and the `flow runs get` command to follow it. When a Run is already in
flight and the Schedule's overlap policy drops this one, it says `Not run`;
`--overlap-policy allow_all` runs it anyway. `Triggered …, but no run was
seen starting yet` is not a failure: the Run may be deferred behind a
running one, or slow to record.

```bash
popcorn webhook deliveries --channel <channel> --status failed --json
popcorn webhook deliveries --channel <channel> --include payload_raw --limit 5
```

The text output lists each Delivery's `id`, Webhook and time; its `status`
and `error_message` are in `--json`.

A `trigger_workflow` Delivery is `processing` until a periodic reconcile
reads its Run's ending, then `completed` or `failed`, with the Run's error in
`error_message`. So a Delivery can read `processing` for a while after its Run
has ended, and the Run itself (`wh-<delivery id>`) is the faster read. A
Delivery is also `failed`, with no Run at all, when its Flow could not be
resolved — the Webhook names no Flow, or a Flow the Routine no longer has —
or its body yields no Flow inputs, with the parse error in `error_message`.
One whose Run aged out of retention before the reconcile read it is `failed`
too.

`popcorn flow get <name> --channel <channel>` prints the Trigger Report:
every Schedule, Webhook, Message Trigger, document, State and Flow that
starts this one. An empty report means only a direct Run — `flow run`, or
an agent running it — starts this Flow.

### Which Version in the CLI

`popcorn flow runs get` names the Version the Run pinned, as `version:`
(`version_id` in `--json`). `popcorn flow run` prints the same number in its
first line — `Started flow '<name>' (v<version_id>)`, printed with `--wait`
only once the Run succeeds. `app status` tells you whether the Routine is on
its line's Head yet:

```bash
popcorn app status --channel <channel>    # run outside a checkout
```

It prints the Install states above in capitals: `Install: CURRENT` means
new Runs get the Head, and `INSTALLING`, `RETRYING`, `LOCKED`, `FAILED`,
`SKIPPED` and `BEHIND` mean what the lowercase states do. A failed Install
also shows its error code and attempt count.

A `Next:` line says what moves the Routine on: on a Copy of its template
(the CLI calls it a *fork line*), usually `app apply`, followed by the full
`popcorn app apply --channel '<channel>'`; for a locked Routine, unlocking it
first; on a Routine still on Popcorn's own template, the Daily Update. `INSTALLING` and `RETRYING` have no `Next:`, since the Install is
still running. When the Install workflow could not be read, the report says the
answer comes from the database alone, and a running Install does not show.
A failed or retrying Install whose error the server classified also prints a
`Code:` line under `Error:`; for `internal`, a further line says the failure is
inside the platform, not in the Bundle, and names the Install workflow.

In `--json`, branch on `install.state`, one of the lowercase names above; the
`install` block carries the error, `error_code`, attempt counts, reason and
`retry_hint` as the server sent them. For a `failed` Install, `error_code` says
what kind of failure it was: `invalid_manifest`, `invalid_schedule` and
`bundle_rejected` are the Bundle's own and are fixed by publishing a corrected
Head; `app_mismatch` and `fork_line_conflict` mean the Install targeted the wrong
thing — another template, or Popcorn's own template or another Copy — and on
a Copy `app apply` moves the Routine to its own Head;
`bundle_unavailable` means no published Version was available; `internal` is a
platform failure that no edit or Publish fixes: report it with `workflow_id`.
`retry_hint` already follows the code. `install_state` is only `current` or
`pending`, and `channel_behind` is `false` only when `install.state` is
`current`.

Run from a Checkout, `popcorn app status` prints the same Install lines
whenever the state is not `current`, after its own line: `Channel runs the
same version`, `Channel still runs …`, `Fork line moved to …` or `A past
version …`. Its `--json` carries the same `install` block, but no
`install_state`.

### Fix it and run it again in the CLI

1. Stop what is still running:

   ```bash
   popcorn flow runs cancel <workflow-id> --channel <channel>
   popcorn flow runs cancel --flow <name> --channel <channel>   # every running run of it
   ```

   A cancel lands at the Run's next Activity boundary; `--force` terminates on
   the spot, for a Run that will not cancel.
2. Check the Bundle: `popcorn app validate .` and
   `popcorn flow validate <flow>.yaml`.
3. Publish: `popcorn app publish . --bump patch -m "..." --yes`.
4. Wait until `install.state` is `current` — `Install: CURRENT` from
   `popcorn app status --channel <channel>`.
5. For a direct Run, pass the failed Run's `inputs` from
   `flow runs get --json` to
   `popcorn flow run <name> --channel <channel> --inputs '...'` — without
   `--wait` it prints the Version at once; then read the Run with
   `flow runs get` and check its `version:` is the one you just published.
   For a Webhook Flow, `popcorn webhook send <webhook>
   @payload.json --channel <channel>` with a body that differs from the
   last one.
