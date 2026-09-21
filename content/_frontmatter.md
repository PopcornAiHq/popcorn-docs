# Frontmatter contract

Every file under `content/` carries this block. The build reads it; so does
the MCP server. A file missing `id` or `summary` fails the build.

```yaml
---
id: fork-line                  # stable, kebab-case, citable, NEVER renamed
title: Fork lines              # a noun phrase, not a sentence
summary: >                     # THE PRODUCT — under 400 characters
  A fork line is a workspace's own version series of an app. Publishing to it
  moves every channel on that line, not just the one you edited.
concepts: [publish, channel-binding]   # other ids, for "see also" and search
applies_to: [cli, mcp, human]          # which renderings include it
source: [fork_for_channel, publish_fork_version]   # BARE SYMBOLS, never paths
---
```

## Field notes

**`id`** is a permanent address. It appears in MCP responses, in cross-links,
and in the CI comment that names which concepts a backend diff touched.
Renaming one breaks all three, so choose it as if it were a URL, because it is.

**`summary`** is what an agent gets back from `search_docs` and often the only
thing it ever reads. Three rules: state the fact, then its consequence; use the
platform's own nouns; never open with "This page describes."

The 400-character cap is not a style preference. Search returns many summaries
in one response, and the whole response lands in the model's context — a
neighbouring design measured one bundle at roughly 71,000 tokens to move
wholesale, which is what happens when nobody caps anything.

**`source`** lists bare symbols and is checked against a manifest the backend
publishes from its own CI. Paths are both a leak in a public repo and less
durable than the name — a symbol that moves file keeps its name.

Omit `source` when a concept describes a behaviour no single symbol owns; do
not invent one to satisfy the field.

**`applies_to`** drops a page from a rendering that should not carry it. A
concept about editing files on disk is `[cli, human]` — an MCP host with no
filesystem should not be told to do something it cannot.
