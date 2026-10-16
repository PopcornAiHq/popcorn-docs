---
id: reference-documents
title: References
order: 5
group: How work arrives
summary: >
  A Reference is a document a Routine works from: a policy, a price list, a
  form to fill, an example of good work. It informs the Routine and is not one
  of its items. People add References in Popcorn; adding some, such as a
  policy, starts work, which list_triggers shows. No assistant tool reads or
  adds a Reference yet.
concepts: [triggers, customizing-a-routine]
layer: product
---

A **Reference** is a document a Routine works from: the policy it checks
claims against, the price list it quotes from, the form it fills in, an
example of a good reply. A Reference informs the Routine. It is not one of the
items the Routine tracks, which live in its
[Tables](https://docs.popcorn.ai/product/concepts/tables.md).

A Routine's template says which References it expects, and the Routine works
without one it is still waiting for until someone adds it. A Reference belongs
to its Routine: adding or replacing one changes that Routine only, and survives
the template's improvements.

## Where they live today

People add and replace References in the Routine, in Popcorn. Adding some
documents also starts work — a new policy is read and its terms recorded —
and `list_triggers` shows those under **Documents**, for example "uploading
the 'policy' document starts policy upsert" (see
[Triggers](https://docs.popcorn.ai/product/concepts/triggers.md)).

## What an assistant can do with them

An assistant can see which documents start work, through `list_triggers`. It
cannot yet list a Routine's References, read one, or add one: a person does
that in Popcorn.

## What the assistant tools would need to show

These pages describe the present, so this section is a design input, not a
promise: nothing depends on it arriving. A tool for References would need to
list each one with what it is used for, when it was added and by whom, and
the ones the Routine is still waiting for; read one's text, or give a download
link for a file that is not text; and add or replace one, saying first what
the Routine will do with it. The MCP reference's
[proposed tools](https://docs.popcorn.ai/product/reference/mcp.md) sketch `list_references`,
`read_reference` and `add_reference`.

> **Platform note** — The References a template expects are its manifest's
> `documents:` key, and a document that starts work names the flow it starts.
> See [manifest keys](https://docs.popcorn.ai/platform/concepts/manifest-keys.md).
