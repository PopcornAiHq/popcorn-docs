---
id: extract-or-derive
title: Extracting fields or deriving them
order: 13
group: How a flow runs
summary: >
  To read fields off an object input, a flow needs an activity that declares
  its output schema. `foundation.fields.extract` names fields by path, uses no
  model, and fails on a missing path. `foundation.agent.transform` derives what
  the payload does not state, and given junk it invents a plausible object.
  Extract whatever the input states; derive only the rest.
concepts: [references, on-error]
applies_to: [cli, mcp, human]
source: [ExtractInput, extract]
---

The DSL cannot reach sub-fields of an `object` input — `$inputs.payload.name`
is statically unreachable, because an input declaration has no way to
describe an object's properties. To read fields off a webhook payload a flow
must first obtain a **typed** shape, and the only mechanism is an activity
that declares its output schema at the call site. Two of those exist, and the
choice between them is the most consequential one in a webhook-backed
bundle. **Reach for the deterministic one first.**

The dividing line is worth applying literally: extraction reads what is
there, derivation invents what is not. A CloudWatch alarm body has no
`severity` and no `env` key at all, so those must be derived; its `AlarmName`
and `NewStateValue` are right there and should not be.

## `foundation.fields.extract` — when the fields are simply there

Names fields by path. No model, no prompt, and an absent path is an error
rather than a guess:

```yaml
  - id: fields
    activity: foundation.fields.extract
    args:
      data: $inputs.payload
      mapping:
        alarm: AlarmName
        service: Trigger.Dimensions.1.value    # dots for nesting AND indices
      defaults:
        note: ""                               # only for genuinely optional fields
      output_schema:
        type: object
        required: [alarm, service]
        properties:
          alarm: { type: string }
          service: { type: string }
```

`$steps.fields.output.alarm` then resolves statically, so `flow validate`
checks it.

- **An unresolvable path fails the step** (`ExtractPathNotFound`), listing
  every bad path at once. That is how a flow *requires* a field to be present
  rather than accepting something invented in its place:

  ```
  ExtractPathNotFound: fields.extract could not resolve: alerts <- alerts
  ```

- **`null` is a value, not an absence.** A stored null passes through; only a
  genuinely missing path errors.
- **The result is validated against `output_schema`**
  (`ExtractSchemaViolation`), so a value contradicting the type you declared
  fails here rather than in whichever later step consumes it.

The shipped `alerttracker` app is built this way: a single producer
(Alertmanager), every field read by path, and not one model call in it.

## `foundation.agent.transform` — when the answer must be derived

The right tool when the payload does not *state* what you need — one flow
normalising several unrelated producers, a severity no field carries, a
human-readable title, prose. Judgement, not lookup.

| | extract (`alerttracker`) | derive (several producers) |
|---|---|---|
| producers | one (Alertmanager) | several, unrelated |
| identity | Alertmanager's `fingerprint`, stated | composed from fields that differ per producer |
| environment | the `cluster` label, stated | absent from a CloudWatch body — derived |
| tool | `fields.extract` | `agent.transform` |
| cost | none | one LLM call per delivery |
| junk input | fails, names every missing path | invents a plausible alert unless a `recognized` guard stops it |

Narrowing a bundle to one producer is therefore not just a scope decision —
it is what makes the deterministic tool available at all. When you do need
the model, three rules, each paid for in a live failure:

1. **A required output schema is a formatting contract, not a validation
   gate.** Given junk, the model *invents* a plausible object to satisfy
   `required`, and `enum` merely constrains which lie it tells. Add an
   explicit recognition flag and hard-stop on it:

   ```yaml
     - id: guard
       activity: foundation.workflow.fail
       when: $steps.normalize.output.recognized == false
       args: { reason: ..., code: UnrecognizedPayload }
   ```

2. **Every property you dereference must be in `required:`.** A declared but
   optional property is genuinely optional — the model returned `details` on
   one run and omitted it on the next, and a missing key is a hard failure:
   `ReferenceError: $steps.normalize.output.details: key not found`.
3. **Keep the prompt and the schema consistent.** Telling the model to blank a
   field whose `enum` excludes `""` is a contradiction, and it does not fail
   cleanly — the model reasons about the conflict *in its output* and breaks
   JSON parsing.

Finally, know which kind of transform you are writing. Mapping fields is
risky; **writing prose is not**. A digest whose wording drifts costs nothing,
because nothing downstream parses it.
