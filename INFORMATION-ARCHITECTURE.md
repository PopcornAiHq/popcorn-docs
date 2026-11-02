# Information architecture

There is one kind of hand-written page. A split into concepts and guides
blurs: a page about a thing grows the steps for reading and changing it, a
guide repeats them, and a writer cannot say which a new page is. So the only
choice a writer makes is a page's part.

Each section below states its audience, what belongs in it, and the one test
that decides a borderline case.

## Two parts, across every section

Every page but the glossary and the references is in a part, and its
directory says which: `content/use/` or `content/build/`.

- **`use`**, Using Popcorn — for a Popcorn user and their assistant, working
  with Routines. Popcorn is used both in its app and headless, from an
  assistant connected over MCP, so a page says where a thing is done when the
  two differ. This is also what that assistant reads first.
- **`build`**, Building Routine Templates — for someone building or changing
  a Routine Template without access to the backend.

The glossary and the reference pages serve both parts, so they have none.
They have the Reference tab to themselves, and are written in `content/glossary/`
and `content/reference/`.

**The test:** *would a Popcorn user who never builds a template need this?*
Then it is `use`.

Nothing internal has a part here. Backend symbols, services and why the
platform is built the way it is stay out of this public repository.

## One vocabulary

The part says what a page is about, not which words it uses. The person who
runs a Routine is usually the one who copies its template and changes it, and
the MCP tools already speak to them in the product's words:
`copy_routine_template`, `create_routine_version`, `install_routine`. Every
page uses the same words.

- **A name with a product word is written the product way**, and the other
  name is given once, in italics, where the reader will meet it: "a Copy of
  the template (the CLI calls it a *fork line*)". A Routine is not a
  channel, and a Routine Template is not an app, in prose on any page.
- **A file-level term with no product word is not renamed:** Manifest,
  Flow, Activity, `call_flow`, Merge Policy. The reader types these, and a
  page that renamed them would send the reader to translate it back. In
  prose they are capitalized like every other glossary term; spelled as
  code (`manifest`, `call_flow`) they stay code.
- **Code keeps its spelling.** A command, key or field is quoted exactly
  (`popcorn app fork`, `channel_parameters:`), whatever the prose around it
  calls the thing.

The glossary gives each name the CLI, the API and older copy use an entry of
its own, opening "Another name for" and the product's word.
`scripts/check-vocabulary.py --strict` reads those entries and fails a hand-written page that uses one of those names
in prose; the everyday words among them (*app*, *project*, *record*) are left
to review.

## Ids

A page's id is its URL, `/<id>`, and the handle everything else names it by.
Neither its part nor anything else about it is in the address, so a page that
moves between parts keeps it. It never changes meaning and is never reused for another page. When
pages are merged, the ids of the ones absorbed are retired: removed from every
`concepts:` list, eval question, generator and link that named them, in this
repository and in the ones that link it. Old addresses are not redirected.

## Pages: `content/use/` and `content/build/`

**Audience:** an agent answering a question mid-task, and a person who has
hit something surprising or has something to do.

**Contains:** one page per question. Most pages are about one thing, such as
a Step, a Routine Setting or a Merge Policy: what it is, then how to read it
and change it. Some pages are a task that crosses several things, start to
finish, such as setting up a Routine or debugging a failed Run.

**The test:** *is this about one thing, or a task across several?* About one
thing, it goes on that thing's page, including how to change it. A task gets
its own page only when it crosses several things, and links to each one's
page rather than repeating it. When a task page and a thing's page overlap,
the thing's page is authoritative.

**Shape:** frontmatter with a `summary` under 400 characters, then the body.
The summary is the answer; the body is the explanation. A page whose body is
three times its summary is probably two pages. A task page is ordered, with
the commands, and its title is imperative ("Set up a Routine"); a page about
one thing has a noun phrase for a title ("Steps").

## `content/glossary/`

One short entry per term, each naming its synonyms and collisions and
linking to the page that explains it. It is where a new term is defined
first. An entry that grows past three sentences is a page waiting to be
written, and the glossary should link to it instead.

## `content/reference/`

**Generated. Never hand-edited.**

**Audience:** an agent that needs exact argument names, and a person checking
one.

**Contains:** the activity catalog, the CLI's commands and the MCP server's
tools, each with the script that generates it (`sync-activities.py`,
`sync-cli.py`, `sync-mcp.py`). The flow rules, the `app validate` rule codes
and a per-app states rendering belong here too, and land here only once
something generates them — never hand-written in the meantime.

**The one exception** is the MCP page's "Proposed tools": tools that are
designed and not built, so nothing can generate them. The text lives in
`sync-mcp.py` rather than the page, so the page still has one writer, and it
says plainly that nothing depends on the tools arriving. Each tool leaves that
section when it ships and the generator starts finding it, or when its design
is dropped.

**The test:** *is there a symbol in the backend that already enforces this?*
Then it is generated, and hand-writing it creates a second source that will
disagree.

## What has no section, on purpose

**Rules a validator consumes.** Served by the API and vendored into the CLI.
Documented here only as prose about what they mean.

**One app's vocabulary.** The app declares its own states and labels;
`feature.state.spec` serves them per channel and per version. A page here
explains what a state machine *is* and then stops.

**Anything with a status field.** No roadmaps, no phase checklists. They are
wrong within a month and nobody re-reads them.
