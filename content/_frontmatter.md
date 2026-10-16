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
platform: 2026-09-25           # optional, generated pages only: the deploy's date
summary: >                     # THE PRODUCT — under 400 characters
  A fork line is a workspace's own version series of an app. Publishing to it
  moves every channel on that line, not just the one you edited.
concepts: [publish, channel-binding]   # other ids, for "see also" and search
layer: platform                        # product | platform — which layer the page speaks
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

**`source` is refused.** Listing the backend symbols a page describes in its
own frontmatter would publish private names in a public repository. The list
for each page lives in a mapping kept in the private backend repository,
keyed by the page's `id`, where the backend's own CI fails when a listed
symbol loses its definition. `check-content.py` fails a page that carries the
field, so the names cannot drift back in one page at a time.

Writing a page that describes specific backend behaviour means adding its
entry to that mapping, in a backend PR; `scripts/drift.py` reads it from a
local backend checkout. Omit a page from it when no single symbol owns what
it describes; do not invent one.

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

**`platform`** is `version`'s counterpart for pages that describe the
deployed platform rather than a release — `sync-activities.py` and
`sync-mcp.py` write it from `--platform-version`, and it too is shown beside
the title. It holds only the date of the prod deploy the page was regenerated
from. The deploy's own id carries a commit hash from a private repository,
which cannot appear here, and the date is what tells a reader how fresh the
page is. It changes only when something else on the page does, so a deploy
that changes nothing leaves the page untouched; a hand run that changes the
page drops the line, since it does not know which deploy it read. A page has
`version` or `platform`, never both, and a hand-written page has neither.

**`layer`** says whose words the page is written in, and it is required.

- `product` — for a Popcorn user and their assistant: Routines, Routine
  Templates, Triggers, Actions, Status, Routine Settings, in the
  [product glossary](https://docs.popcorn.ai/concepts/product-glossary.md)'s
  terms. Such a page names a platform term only inside a **Platform note** —
  a blockquote that opens `> **Platform note** —` and links the platform page
  that explains the term. `scripts/check-layer.py` fails a product page that
  uses one anywhere else, taking the terms from the platform glossary.
- `platform` — for someone building a Routine Template: the bundle format,
  the CLI, flows, fork lines, in the
  [platform glossary](https://docs.popcorn.ai/concepts/glossary.md)'s terms.

The field describes the page, not its reader: someone building a template
reads both layers. A page that needs the CLI says so in its first paragraph;
the retired `applies_to:` field is refused.
