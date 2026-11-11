---
id: row-leases
title: Row leases
order: 22
group: How a Flow runs
summary: >
  foundation.store.claim_row holds a Row by writing a holder into a Column,
  so no two passes email the same recipient. With no holder: it is a lease:
  the platform frees it when the Run ends, a later claim takes over an
  abandoned lease, and commits_leases keeps the hold once a send has gone,
  even if recording it fails, so it is never repeated. when_legal claims only where the State Machine
  allows.
lede: >
  Stop two Runs working on the same Row, and free it again however the Run
  ends.
concepts: [flow-grammar, on-error, states-authoring, state-machine]
---

A [Flow](https://docs.popcorn.ai/flow-grammar.md) that emails someone, or
does any other work that must happen once per Row, needs the
Row to itself while it works:
a second [Run](https://docs.popcorn.ai/history.md) started on the same Row, by the next Schedule tick or by a
person pressing an Action, must be turned away rather than do the work
again. `foundation.store.claim_row` does this by writing the Run into a
Column of the Row, and refusing every other Run while it is there.

## A lease

```yaml title="ask.yaml"
steps:
  - id: claim
    activity: foundation.store.claim_row
    args:
      conversation_id: $inputs.conversation_id
      table_name: recipients
      record_id: $inputs.record_id
      column: Sending
      when_legal: world.asked
      held_code: RecipientBeingAsked
      held_message: Another run is emailing this recipient.
```

With no `holder:`, the claim is a **lease** that the Run owns:

- **Taking it.** The claim reads the Row, refuses with `held_code` if
  another Run is in the Column, and writes this Run into it. The write is
  conditional on the Row as it was read, so of two Runs claiming at once
  exactly one wins.
- **Freeing it.** When the Run ends, however it ends (succeeded, failed or
  stopped), the platform empties the Column. It empties it only if this Run
  still holds it, so a Row the Flow already freed, or one another Run has
  claimed since, is left alone. The Flow writes no release Step.
- **Taking it over.** A Run that never got to free the Row, because it
  timed out or was terminated, leaves the Column set. The next claim reads
  that Run's state, and when it has ended, takes the Row over and records
  the change as `lease_lapsed` in the Row's
  [History](https://docs.popcorn.ai/history.md).

The holder written into the Column is the Run's own identity, prefixed
`lease:`. Leave the Column out of every `writes:` and patch: only the claim
and the platform write it.

## Keep the hold once an email has gone, even if recording it fails

Freeing the Row on failure is right until the Flow has done the thing that
must not happen twice. After an email has gone, a freed Row whose record of
the send failed to save would look unasked, and the next pass would email
again. Mark the Step after which a failure must keep the hold:

```yaml title="ask.yaml"
  - id: send
    activity: feature.email.send
    on_error: { policy: skip, retry: 0 }
    commits_leases: true
    args:
      integration_id: $channel.integrations.inbox.id
      to: [$steps.compose.output.to]
      subject: $steps.compose.output.subject
      body: $steps.compose.output.body

  - id: record
    activity: foundation.store.patch_row
    args:
      conversation_id: $inputs.conversation_id
      table_name: recipients
      record_id: $inputs.record_id
      patch: { Stage: waiting, Last Asked: $steps.now.output.iso }
```

Once `send` succeeds, the Run's leases are **committed**:

| The Run then | The Row |
|---|---|
| succeeds | is freed, as always |
| fails or is stopped | stays held; a later claim is refused as held |
| times out | stays held; it is not taken over |

A Step that is skipped, by `when:` or by `on_error: { policy: skip }`,
commits nothing, so a send that failed and was skipped leaves the Row to be
freed and asked again on the next pass.

> [!WARNING] The Step that records the work must fail, not skip
> A Run that succeeds frees its Rows. If `record` above were
> `on_error: { policy: skip }`, a failed write would let the Run succeed
> with the send unrecorded, the Row would be freed, and the next pass would
> send again. Leave `on_error` off the Steps that record a committed Step's
> work, so their failure fails the Run and the hold stays.

`commits_leases` goes on one Activity Step or one `call_flow` Step, not on a
`foreach` or a block, so that "succeeded" means one thing. A held Row that
was committed stays held until someone looks: frees it, or presses an
Action whose `writes:` empty the Column.

## Claim only where the graph allows

`when_legal: <event>` names an Event of the Table's
[State Machine](https://docs.popcorn.ai/state-machine.md). The claim is
refused, with the graph's own refusal code, unless a Transition for that Event
leaves from the State the Row is in, judged with the holder Column empty.
`when_legal: world.asked` takes a recipient only while it can still be
asked, so the Flow needs no hand-written rule for "already asked".

`refuse_when:` rules still work beside it, for a check the graph can't
express or a Table with no graph; each rule is a list of Column conditions
that refuse with its own `code` when they all hold.

## Actions while a Row is held

A lease stops other Runs, not people. To refuse an
[Action](https://docs.popcorn.ai/actions-and-status.md) while a pass holds
the Row, guard its Transition on the Column being empty, as
[authoring a States tier](https://docs.popcorn.ai/states-authoring.md)
shows with `not_held`. Since every write to a State Column reprojects the
Row, the Actions disappear when the claim lands and come back when the
lease is freed.

## A hold meant to outlive the Run

`release: manual`, or naming `holder:` with no `release:`, is the claim as
it was before leases: the Column holds what `holder:` says (usually
`$trigger.run_id`), nothing frees it but the Flow's own write, and no later
claim takes it over. Use it for a hold that should stay after the Run, such
as one kept for a person to inspect. Every Flow written before leases
existed uses this form, so it keeps working unchanged.

| | Lease (no `holder:`) | Manual (`holder:` or `release: manual`) |
|---|---|---|
| Holder | the Run, `lease:…` | the value given |
| Freed when the Run ends | yes, unless committed and the Run failed | no; the Flow frees it |
| Taken over after a timeout | yes, unless committed | never |
| `commits_leases` | applies | ignored |

> "Is anything holding recipient 12 in #team-offsite, and since when?"

> [!TIP] MCP tool call
> Your assistant calls `get_row`, then `list_history` for that Row.

The holder Column says which Run holds the Row, and the Row's History shows
the claim, the release, and any `lease_lapsed` takeover.
