---
id: conditions
title: Conditions and filters
order: 11
group: How a flow runs
summary: >
  A `when:` string routes to one of two parsers. A bare `$ref` or one `==`/`!=`
  stays on the lenient legacy rail; anything with `&&`, `||`, `<`, `!` or
  parentheses goes to the strict, typed expression rail. Adding a second
  condition can therefore change how the first compares. To select rows, filter
  in the query instead of gating a step.
concepts: [flow-grammar, references]
part: build
---

`when:` gates a step, a block, or — on a `foreach` step — each item. Routing
is **legacy-first**: a string the legacy parser accepts stays legacy forever,
even if it contains new-syntax tokens.

| Form | Rail | Semantics |
|---|---|---|
| `$ref` | legacy | truth-tested |
| `$ref == value`, `$ref != value` | legacy | **lenient** equality; a skipped step is `None` and compares unequal |
| anything with `&&` `\|\|` `<` `<=` `>` `>=` `!` `(` `)`, or a second comparison | expression | **strict, typed** |
| a plain literal | legacy | truthy as-is |

The expression grammar is `!`, `&&`, `||`, `==`, `!=`, `<`, `<=`, `>`, `>=`,
parentheses; operands are `$ref`s, numbers, `true`/`false`, and quoted
strings. Precedence is parens → `!` → comparisons → `&&` → `||`. Bounds:
depth ≤ 8, ≤ 32 conditions, ≤ 8 terms per chain, literals ≤ 1024 chars. No
functions, no arithmetic, no `${}` interpolation.

## The seam between the rails

A standalone `$a == 1` is *lenient* legacy equality; the same comparison
inside `$a == 1 && $b != ''` is *strict and typed* on the expression rail.
Adding a second condition can therefore change how the first one compares.
And a string that routes to the expression rail but fails to parse is an
**error** — never a fallback to literal truthiness. An expression that cannot
be evaluated, such as an ordered comparison between mismatched types, fails
the run with `PredicateError`.

`app validate` does not police any of this: mirroring the routing rule
offline means reimplementing the predicate parser, and a near-miss
reimplementation reports valid clauses as broken. It checks the references
inside a `when:` and leaves the grammar to `flow validate`, which calls the
real parser.

## Select rows with a filter, not a gate

The filter DSL for a table's rows runs in the database rather than after the
fact:

```yaml
filter:
  Status: firing                                  # shorthand for $eq
  Last Seen: { $lt: $steps.cutoffs.output.iso }   # $gt $gte $lt $lte
  Nudged At: { $exists: false }                   # $ne, $in, $contains too
  "*": { $contains: acme }                        # the whole row; $contains only
```

Ordering comparisons on ISO-8601 strings are correct because they are
lexicographic — in a filter *or* on the expression rail. The difference is
where the work happens: a filter selects rows in the database, while a `when:`
gate can only skip a step you already decided to run.
