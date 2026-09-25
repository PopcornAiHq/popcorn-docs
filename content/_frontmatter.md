# Frontmatter contract

Every file under `content/` carries this block. The build reads it; so does
the MCP server. A file missing `id` or `summary` fails the build.

```yaml
---
id: fork-line                  # stable, kebab-case, citable, NEVER renamed
title: Fork lines              # a noun phrase, not a sentence
order: 9                       # reading position within its section
group: How a version ships     # optional: sidebar group within the section
layout: lookup                 # optional: the page's own entries index the rail
version: 0.57.0                # optional, generated pages only: the release described
summary: >                     # THE PRODUCT — under 400 characters
  A fork line is a workspace's own version series of an app. Publishing to it
  moves every channel on that line, not just the one you edited.
concepts: [publish, channel-binding]   # other ids, for "see also" and search
applies_to: [cli, mcp, human]          # which renderings include it
source: [fork_for_channel, publish_fork_version]   # BARE SYMBOLS, never paths
---
```

## Field notes

**`id`** is a permanent address. It is the page's URL, the handle MCP
responses and `get_doc` use, and what another page's `concepts:` names.
Renaming one breaks all three, so choose it as if it were a URL, because it is.

**`summary`** is what an agent gets back from `search_docs` and often the only
thing it ever reads. Three rules: state the fact, then its consequence; use the
platform's own nouns; never open with "This page describes."

The 400-character cap is not a style preference. Search returns many summaries
in one response, and the whole response lands in the model's context, so an
uncapped summary is a cost every caller pays.

**`source`** lists bare symbols — the backend names a reader would search for
to check the page. Paths are both a leak in a public repo and less durable than
the name: a symbol that moves file keeps its name.

`scripts/drift.py sources` verifies that each one still has a definition in
the backend. It runs locally only, against a backend checkout, because the
backend is private and CI cannot read it — so run it before a content PR.
Nothing verifies behaviour: a symbol can exist and do the opposite of what the
page says. Treat a page's `source` as a pointer, not a proof.

Omit `source` when a concept describes a behaviour no single symbol owns; do
not invent one to satisfy the field.

**`order`** is the page's place in its section's reading path, starting at 1:
the landing page, the previous/next links on every page, and `llms.txt` all
follow it. Filenames sort alphabetically, which is no reading order at all —
it once put an advanced guide ahead of the one it builds on. Number by what a
reader needs first; a page with no `order:` goes after the ordered ones.
Renumbering is cheap, because nothing links to a position.

**`group`** clusters pages under a collapsible heading in the site sidebar,
inside their section. A group sits where its first page does in reading
order, so it needs no order of its own. Pages without one sit directly under
the section. Spell a group identically on every page in it — the label is the
key.

**`layout: lookup`** is for a page read by looking something up in it rather
than top to bottom — the glossary and the reference pages. Its own entries
replace the rail's contents list, with a filter: each `##` heading is a
group, and each `###` heading or bold-led bullet (`- **term** — …`) is an
entry, so prose on such a page that needs bold-led points uses a numbered
list. It is the only value; omit the field for every other page.

**`version`** is written by a generator whose page describes one release of
something — `sync-cli.py` records the `popcorn` version it read — and is shown
beside the title. A hand-written page never sets it.

**`applies_to`** records which readers a page is written for — `cli`, `mcp`,
`human`. Nothing reads it: the build and the MCP server serve every page to
every reader. It is still worth setting honestly: a page marked
`[cli, human]` — editing files on disk, say — tells a reviewer it asks for
something an MCP host with no filesystem cannot do.
