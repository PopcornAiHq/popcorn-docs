---
id: extract-or-derive
title: Extracting fields or deriving them
order: 20
group: How a Flow runs
summary: >
  `foundation.fields.extract` reads fields by path, uses no model, and fails
  on a missing path. `foundation.agent.transform` derives what the input does
  not state, and given junk it invents a plausible answer, so guard it: fail
  on an empty result and check its keys in code, as Questionnaire does.
  Extract whatever the input states; derive only the rest.
lede: >
  When a Flow should read fields straight from its input, and when it should
  have a model work them out.
concepts: [references, on-error, questionnaire-template]
---

A [Flow](https://docs.popcorn.ai/flow-grammar.md) reads a value it can
name by [reference](https://docs.popcorn.ai/references.md). When the value
is inside something the Flow cannot name — a field of an `object` input, or
an answer inside an email — it needs an
[Activity](https://docs.popcorn.ai/activities.md) that returns a typed
shape, and two of them do. The dividing line is worth applying literally:
**extraction reads what is there, derivation works out what is not.**
Reach for the deterministic one first.

| | extract | derive |
|---|---|---|
| Activity | `foundation.fields.extract` | `foundation.agent.transform` |
| reads | named paths in structured data | prose, or several unrelated shapes |
| cost | none | one model call |
| junk input | fails, naming every missing path | invents a plausible answer unless something stops it |
| example | `alerttracker`, one Webhook producer | Questionnaire, a questionnaire document and email replies |

## `foundation.fields.extract`: when the fields are simply there

The [Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md)
reads only prose, so it never extracts. The example here is Popcorn's
`alerttracker` template, whose one producer, Alertmanager, sends a JSON body
with every field it needs. The DSL cannot reach sub-fields of an `object`
input — `$inputs.payload.name` is statically unreachable — so a
[Webhook](https://docs.popcorn.ai/triggers.md)'s `payload` is read through
this Activity:

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

- **An unresolvable path fails the Step** (`ExtractPathNotFound`), listing
  every bad path at once. That is how a Flow *requires* a field to be present
  rather than accepting something invented in its place:

  ```
  ExtractPathNotFound: fields.extract could not resolve: alerts <- alerts
  ```

- **`null` is a value, not an absence.** A stored null passes through; only a
  genuinely missing path errors.
- **The result is validated against `output_schema`**
  (`ExtractSchemaViolation`), so a value contradicting the type you declared
  fails here rather than in whichever later Step consumes it.

## `foundation.agent.transform`: when the answer must be derived

The right tool when the input does not *state* what you need: a list of
questions inside a sample email, which question a reply answers, a severity
no field carries, one Flow normalising several unrelated producers.
Questionnaire derives twice, each with a prompt from its `prompts/` folder.

`questionnaire_load` reads the questions out of the Reference a person
added, which may be a plain list or a sample email:

```yaml title="questionnaire_load.yaml"
  - id: extract
    activity: foundation.agent.transform
    args:
      prompt: $channel.prompts.read_questionnaire
      prompt_format: jinja
      data:
        text: $steps.read.output.text
      max_tokens: 4096
      output_schema:
        type: object
        required: [questions, subject, intro, closing]
        additionalProperties: false
        properties:
          questions:
            type: array
            items: { type: string }
          subject: { type: string }
          intro: { type: string }
          closing: { type: string }

  - id: fail_no_questions
    when: "!$steps.extract.output.questions"
    activity: foundation.workflow.fail
    args:
      reason: >-
        No questions found in the document. Add a document that lists the
        questions to ask, or a sample email with them in it.
      code: NoQuestionsFound
```

`check_recipient` reads which questions a reply answers, into an object
keyed by question:

```yaml title="check_recipient.yaml"
  - id: read
    when: $steps.found.output.count
    activity: foundation.agent.transform
    on_error: { policy: skip }
    args:
      prompt: $channel.prompts.read_answers
      prompt_format: jinja
      data:
        questions: $steps.found.output.questionnaire.questions
        reply: $steps.found.output.text
      max_tokens: 2048
      output_schema:
        type: object
        required: [answers]
        additionalProperties: false
        properties:
          answers:
            type: object
            additionalProperties: { type: string }
```

Each rule below is how those two Steps are kept honest.

1. **A required output schema is a formatting contract, not a validation
   gate.** Given junk, the model *invents* a plausible object to satisfy
   `required`, and `enum` merely constrains which lie it tells. Give it a
   way to say "nothing here" and hard-stop on it.
   `read_questionnaire` tells the model to return an empty `questions` list
   and never invent one, and `fail_no_questions` fails the Run on it before
   anything is stored, so the Reference is refused rather than turned into
   made-up questions.
2. **Check what the model returns in code.** `read_answers` asks for keys
   "copied exactly from the list above", and the code block's `decide`
   takes an answer only under a key that equals one of the questions, and
   only for a question still open. A key the model reworded is dropped, and
   an answer already recorded is never overwritten.
3. **Every property you dereference must be in `required:`.** A declared
   but optional property is genuinely optional: the model may return it on
   one Run and omit it on the next, and a missing key is a hard failure
   such as `ReferenceError: $steps.extract.output.intro: key not found`.
   That is why all four of `questionnaire_load`'s properties are required,
   with `""` for one the document lacks.
4. **Keep the prompt and the schema consistent.** Telling the model to blank
   a field whose `enum` excludes `""` is a contradiction, and it does not
   fail cleanly: the model reasons about the conflict *in its output* and
   breaks JSON parsing.

> [!NOTE] A failed read is read again
> `read` is skipped on error, and `decide` treats a reply it could not read
> as unread: it leaves the Row as it was, so the next pass reads the same
> reply again rather than following up past it.

Finally, know which kind of transform you are writing. Mapping fields is
risky; **writing prose is not**. A digest whose wording drifts costs nothing,
because nothing downstream parses it. Questionnaire's emails are not
written by a model at all: the code block's `compose` builds them from the
stored questions.
