---
id: conditions
title: Conditions and filters
order: 19
group: How a Flow runs
summary: >
  A `when:` string routes to one of two parsers. A bare `$ref` or one `==`/`!=`
  stays on the lenient legacy rail; anything with `&&`, `||`, `<`, `!` or
  parentheses goes to the strict, typed expression rail. Adding a second
  condition can therefore change how the first compares. To select Rows, filter
  in the query; to check a Row you write, check it in the claim.
lede: >
  How a Flow decides whether a Step runs, and why adding a second condition
  can change how the first one compares.
concepts: [flow-grammar, references]
---

`when:` gates a [Step](https://docs.popcorn.ai/flow-grammar.md), a block,
or — on a `foreach` Step — each item. The
[Questionnaire template](https://docs.popcorn.ai/questionnaire-template.md)'s
Flows gate on every form there is:

```yaml title="ask_recipient.yaml"
  - id: send
    when: $inputs.send_mode == 'send'
    activity: feature.email.send

  - id: record
    when: $steps.thread.output.value != 'none'
    activity: foundation.store.patch_row
```

```yaml title="check_recipient.yaml"
  - id: read
    when: $steps.found.output.count        # truth-tested: 0 or null skips it
    activity: foundation.agent.transform
```

```yaml title="questionnaire_load.yaml"
  - id: fail_no_questions
    when: "!$steps.extract.output.questions"
    activity: foundation.workflow.fail
```

Routing is **legacy-first**: a string the legacy parser accepts stays
legacy forever, even if it contains new-syntax tokens.

| Form | Rail | Semantics | In Questionnaire |
|---|---|---|---|
| `$ref` | legacy | truth-tested | `$steps.decide.output.follow_up` |
| `$ref == value`, `$ref != value` | legacy | **lenient** equality; a skipped Step is null and compares unequal | `$steps.apply.output.applied == 0`, `$steps.parse.output.ok == false` |
| anything with `&&` `\|\|` `<` `<=` `>` `>=` `!` `(` `)`, or a second comparison | expression | **strict, typed** | `!$steps.extract.output.questions` |
| a plain literal | legacy | truthy as-is | — |

The expression grammar is `!`, `&&`, `||`, `==`, `!=`, `<`, `<=`, `>`, `>=`,
parentheses; operands are `$ref`s, numbers, `true`/`false`, and quoted
strings. Precedence is parens → `!` → comparisons → `&&` → `||`. Bounds:
depth ≤ 8, ≤ 32 conditions, ≤ 8 terms per chain, literals ≤ 1024 chars. No
functions, no arithmetic, no `${}` interpolation.

A `when:` that starts with `!` must be quoted in YAML, as must one that
starts with any character YAML reads as syntax. `cta_apply` and
`reply_by_set` quote their comparisons too, which is harmless.

## The seam between the rails

A standalone `$a == 1` is *lenient* legacy equality; the same comparison
inside `$a == 1 && $b != ''` is *strict and typed* on the expression rail.
The differences:

| | Legacy rail | Expression rail |
|---|---|---|
| right-hand side | a reference, a quoted string, `true`/`false`/`null`, a number, or a bare word read as a string | a reference, a number, `true`/`false` or a quoted string |
| `true == 1` | equal | unequal: a boolean is never a number |
| a list or object operand | compared as a value | `PredicateError`: containers are not comparison operands, so test them bare |
| `<`, `>` on mismatched types | — | `PredicateError` |

Adding a second condition can therefore change how the first one compares.
And a string that routes to the expression rail but fails to parse is an
**error** — never a fallback to literal truthiness. An expression that cannot
be evaluated fails the Run with `PredicateError`.

> [!TIP] Stay on the legacy rail when one comparison will do
> `ask_recipient` and `check_recipient` gate their `record` and `release`
> Steps on one comparison each against the word `none`, the last value
> they hand `foundation.workflow.coalesce`, which it returns when nothing
> before it has a value. Exactly one of the two runs.

`app validate` does not police any of this: mirroring the routing rule
offline means reimplementing the predicate parser, and a near-miss
reimplementation reports valid clauses as broken. It checks the references
inside a `when:` and leaves the grammar to `flow validate`, which calls the
real parser.

## Select Rows with a filter, not a gate

The filter DSL for a [Table](https://docs.popcorn.ai/tables.md)'s Rows runs
in the database rather than after the fact:

```yaml
filter:
  Status: firing                                  # shorthand for $eq
  Last Seen: { $lt: $steps.cutoffs.output.iso }   # $gt $gte $lt $lte
  Nudged At: { $exists: false }                   # $ne, $in, $contains too
  "*": { $contains: acme }                        # the whole row; $contains only
```

Ordering comparisons on ISO-8601 strings are correct because they are
lexicographic — in a filter *or* on the expression rail. The difference is
where the work happens: a filter selects Rows in the database, while a `when:`
gate can only skip a Step you already decided to run.

Questionnaire's tick uses neither to pick its recipients. It reads every
`recipients` Row into the code block's `plan`, which returns who to ask and
who to check, and those lists are what its `foreach` Steps iterate. A rule
that needs the reply-by date, the send mode and the Row together is easier
to test there than to express as a filter.

## Check a Row you write in the claim, not in a gate

A `when:` reads the values the Run already has, which may be older than the
Row. Questionnaire's plan is read at the start of a pass, and another pass
may have asked the same recipient since. So `ask_recipient` checks the Row
inside the claim that takes it:

```yaml title="ask_recipient.yaml"
  - id: claim
    activity: foundation.store.claim_row
    args:
      # …
      column: Sending
      holder: $trigger.run_id
      refuse_when:
        - code: RecipientAlreadyAsked
          message: This recipient has already been asked.
          when:
            - { column: Stage, test: set }
```

`refuse_when` is checked against exactly the Row the claim reads and then
writes, so two passes cannot both find `Stage` blank and both send. Its
rules are column tests, not `when:` expressions; see
[`foundation.store`](https://docs.popcorn.ai/activities/catalog/foundation/store.md)
in the Activity reference.
`check_recipient` refuses the same way when `Stage` is no longer `waiting`.
