# Frontmatter contract

Every file under `content/` carries this block. The build reads it; so does
the MCP server. A file missing `id` or `summary` fails the build.

```yaml
---
id: copying-a-template         # kebab-case, citable; never reused for another page
title: Copying a template      # a noun phrase, not a sentence
order: 17                      # reading position within its part
group: How a version ships     # optional: sidebar topic within the part
layout: lookup                 # optional: the page's own entries index the rail
version: 0.57.0                # optional, generated pages only: the release described
updated: 2026-09-25            # optional, generated reference pages only: the deploy that last changed it
summary: >                     # THE PRODUCT — under 400 characters
  A copy of a Routine Template is the workspace's own version series of it.
  Publishing a version to it reaches every Routine on the copy, not just the
  one you edited.
concepts: [versions, customizing-a-routine]   # other ids, for "see also" and search
part: build                    # use | build — which half of the site; none on the glossary and references
---
```

## Field notes

**`id`** is the page's handle: the last part of its URL, what MCP responses
and `get_doc` use, and what another page's `concepts:` names. An id never
changes meaning and is never reused for another page. When a page is merged
into another, its id is retired: removed everywhere it is named, in this
repository and in the ones that link it, not redirected. Choose one as if it
were a URL, because it is.

**`summary`** is what an agent gets back from `search_docs` and often the only
thing it ever reads. Three rules: state the fact, then its consequence; use the
product's words, as every page does; never open with "This page describes."

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

**`order`** is the page's place in its part's reading path, starting at 1,
with concepts and guides numbered in one sequence so a guide sits beside the
concepts it puts to work: the sidebar, the previous/next links on every page,
and `llms.txt` all follow it, and the landing page opens each kind at its
first page in it. Filenames sort alphabetically, which is no reading order at all —
it once put an advanced guide ahead of the one it builds on. Number by what a
reader needs first; a page with no `order:` goes after the ordered ones.
Renumbering is cheap, because nothing links to a position.

**`group`** is the page's topic: a collapsible heading in the site sidebar,
inside its part, holding concepts and guides alike — the sidebar names topics,
never kinds. A group sits where its first page does in reading order, so it
needs no order of its own. Pages without one sit directly under the part. Spell a group identically on every page in it — the label is the
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

**`updated`** is `version`'s counterpart for pages that describe the
deployed platform rather than a release — `sync-activities.py` and
`sync-mcp.py` write it from `--platform-version`, and it is shown beside the
title as "updated 2026-10-26". It holds only the date of the prod deploy the
page was regenerated from. The deploy's own id carries a commit hash from a
private repository, which cannot appear here, and the date is what tells a
reader how fresh the page is. It changes only when something else on the page
does, so a deploy that changes nothing leaves the page untouched: the date is
that of the deploy that last changed what the generator writes. A hand edit to
the page does not move it, and a hand run that changes the page drops the
line, since it does not know which deploy it read. A page has `version` or
`updated`, never both. A hand-written page has neither, and `check-content.py`
refuses `updated:` on one: git knows when a hand-written page changed. The
field's old names, `deployed:` and `platform:`, are refused.

**`part`** says which half of the site the page is in, and it is required on
every page but the glossary and the reference pages.

- `use` — Using Popcorn: for a Popcorn user and their assistant, working with
  Routines, their Triggers, Actions, Status and Routine Settings.
- `build` — Building Routine Templates: for someone building or changing a
  template, its files, flows, copies and versions. It opens with the product
  idea before the mechanism ("A Routine's scheduled Triggers are schedules in
  its template's manifest").

The glossary and the reference pages serve both halves, so they carry no
`part:`, sit at `/glossary/…` and `/reference/…`, and are listed once, after
both, in the sidebar. Every page, in either half, is written in the product's
words: file-level terms the reader types (`manifest`, flow, activity) stay,
and a name the CLI or the API uses where the product has its own word is given
once, in italics, as the other name — "a copy of the template (the CLI calls it
a *fork line*)". The [glossary](https://docs.popcorn.ai/glossary/glossary.md)
pairs each such name with the product's word in its table "Names you'll see
elsewhere", and `scripts/check-vocabulary.py --strict` fails a page that uses
one in prose. `INFORMATION-ARCHITECTURE.md` has the rule in full.

The field describes the page, not its reader: someone building a template
reads both halves. A page that needs the CLI says so in its first paragraph.
Three retired fields are refused: `layer:` (the old name of `part:`),
`product_terms:` and `applies_to:`.
