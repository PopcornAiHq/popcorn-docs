---
id: versions
title: Versions: publishing and installing
order: 3
group: How a Version ships
summary: >
  A change reaches a Routine in two steps: publishing mints an immutable
  Version of a Routine Template on its Copy, and installing brings each
  Routine on the Copy to it, the one published from at once and the rest on
  their Daily Update. `install_routine` (`popcorn app apply`) retries a
  blocked Install. A Run keeps its Version, so a Routine upgraded mid-run
  never mixes code.
lede: >
  How a change to a template reaches its Routines: publishing creates a
  Version, and installing brings each Routine up to it.
concepts: [copying-a-template, app-bundle, manifest-keys]
---

A Routine runs one Version of its template at a time. A change to the
template reaches it in two steps that are easy to conflate: a **Publish**
makes a new Version on the Workspace's Copy of the template (see
[copying a template](https://docs.popcorn.ai/copying-a-template.md)),
and an **Install** brings one Routine onto it. A Version can exist while no
Routine runs it, and that gap is where most confusion about "did my change
go out" lives.

| To | Over MCP | With the CLI |
|---|---|---|
| read the files edits are based on | `list_routine_files`, `read_routine_file` | `popcorn app checkout --channel <routine>` |
| publish the next Version | `create_routine_version` | `popcorn app publish` |
| see what a Routine runs, and whether its Install landed | `get_routine` (**Version** and **Install**) | `popcorn app status` |
| retry an Install that did not land | `install_routine` | `popcorn app apply` |

## Publishing

A Publish mints the next Version on a Copy and starts an Install on the
Routine it names. It is an operation on the Copy, not on one Routine: every
other Routine on the Copy takes the new Version on its own Daily Update. It
needs a Workspace admin.

`create_routine_version` is a dry run first. It shows the Version it would
publish, each file's diff, every check it would fail, and the reach: how
many other Routines on the Copy will update. `confirm=true` with the dry
run's `plan_id` publishes, running every check again. `popcorn app publish`
asks before it publishes, naming the Copy rather than a count, and reports
the count only once the Version exists.

A Publish is based on the Copy's newest Version, its **Head**. A Publish
whose base is not the Head is refused, unless the files it would publish
are identical to the Head's, which is how a retried Publish succeeds; a diff
computed against an older Version would drop whatever the Versions in
between changed. A
Routine's own Version lags the Head while an Install has not landed, and
for good on a Routine that takes no updates; that is why
`list_routine_files` and `popcorn app checkout` read the Head of a Copy by
default, and an edit based on what a lagging Routine runs has to be redone
on a fresh read.

### What a Publish refuses

A Publish is refused when:

- the caller is not a Workspace admin
- the request carries no file changes and no deletions
- the base is not a Copy the Workspace can see, or is no longer its Head
  and the files it would publish differ from the Head's
- the named Routine runs a different Copy, or Popcorn's version
- the tree has a path outside the Bundle shape, two files under `prompts/` or
  `templates/` that would install under the same key (`prompts/x.md` and
  `prompts/x.txt`), or a root YAML file whose top level is not a mapping
- a Flow does not parse strictly — a misspelled key, a `call_flow` naming its
  own Flow or one the Bundle does not have, or a `foreach` asking for more
  `max_parallel` than the platform allows
- the Manifest has no `version:`, a Version that does not advance, or a
  different `app_type` from its Copy
- a Flow name is not a slug, or a Flow declares its own `trigger:`
- a `tables:` entry would be refused by the store at Install — an unknown
  `type` or `display` kind, a `format` that does not suit its type, a merge
  setting without the policy it belongs to, and the other Column rules in
  [adding a Table](https://docs.popcorn.ai/adding-a-table.md). The
  refusal names each Table and Column
- the Version or its content already exists (below)

A Manifest with **no** `app_type:` is not refused: Publish treats it as the
Copy's own template. Every Install of that Version then clears `app_type`
and `channel_agent` on each Routine it reaches, which is every Routine on the
Copy. Keep both keys in every Version, and treat `app validate`'s
`clears-app-type` warning as an error.

Every one of those checks asks *is this allowed and well-formed*. None asks
**did you mean to do this to every Routine on the Copy**, and none refuses a
Publish for its reach.

### A Version never changes

A Version is identified two ways: by its **semver on its Copy**, the
Manifest's `version:`, which you choose, and by a **digest** of its files,
which you do not. Popcorn's version and each Copy are separate series, so two
Copies can each hold a `1.0.1`. The number the CLI and MCP print as a
Version's id (`version: 913`) is a third handle, assigned by Popcorn. A
Publish has four outcomes:

| What you send | What happens |
|---|---|
| a new semver, new content | published |
| the same semver, byte-identical content | no-op, reported as such |
| the same semver, different content | refused — Versions are immutable |
| a new semver, content identical to an earlier Version on the Copy | refused — the digest is taken |

A new semver must also be higher than the Copy's newest. The CLI checks that
before sending; the server enforces it regardless.

So a mistake is corrected by publishing forward, never by editing, and
nothing moves a Routine back to an earlier Version. An old Version cannot be
republished byte for byte, because its digest is taken: bump the Version and
change something — the Manifest's `changelog:` saying why is the honest
change. An old Version can be read back by its id, with `list_routine_files`
and `read_routine_file`'s `version`, or `popcorn app checkout --version <id>`,
which checks it out read-only: publishing from that Checkout is refused.
Version ids are the numbers a Publish and `popcorn app status` print; nothing
lists a Copy's past Versions. To make old content current again, take a
fresh read of the Head, put the old files over it — deleting any file the old
Version lacked — and publish forward with a bump.

## Installing

An Install brings one Routine to one Version: it reconciles its Tables,
Scalars, Schedules, Webhooks and configuration (the *channel config*, which
holds its parameters and Connections), and moves the Routine onto the Version
last. Installs follow creating a Routine from a template, a Publish, a retry
and each Daily Update.

**The Daily Update** installs the Head of each Routine's Copy once a day,
which is how a Publish reaches the Routines you did not publish from, and how
a Routine on Popcorn's version reaches the newest Version its Workspace's
Release Track offers. It runs as the Workspace, not as the person who
published. It never moves a Routine onto a Copy, and it skips archived
Routines, Routines locked against template updates, and Routines with no
update schedule.

An Install can be blocked — another Install may be in progress, or the
Routine locked against template updates — and that is reported separately
from whether the Publish succeeded, because the Version publishes either way.
An Install reported as started has not necessarily landed either: it
re-checks when it runs, and can still skip. `get_routine`'s **Install** line
and `popcorn app status` show what the Routine actually runs; `app status`
says whether an Install is running, retrying, failed, skipped or locked,
with a failed Install's error, a skipped one's reason, and a `Next:` line
saying what moves the Routine on.

**`install_routine` (`popcorn app apply`) is the retry.** It brings one
Routine on a Copy up to the Copy's Head, takes no Version from you — there
is no argument through which one Routine's content reaches another — and
says there is nothing to install (in the CLI's JSON, `already_current`) when
the Routine already runs the Head. It works from the
server's state alone, so it still works after the session that published has
ended, which re-running the Publish cannot cover. On a locked Routine it is
refused rather than queued. It needs a Routine Role of `member` or above,
or a Workspace admin. A Routine on Popcorn's version takes new Versions
through its Daily Update, not through a retry; an Install there in a
Workspace that owns exactly one Copy moves it onto that Copy instead, and
with two or more is refused as ambiguous unless it names one (see
[copying a template](https://docs.popcorn.ai/copying-a-template.md)).

## A Run keeps the Version it started on

When a Flow starts, it reads the Version its Routine runs once and records
it for that Run. Everything the Run needs — the Flow, any code block it
calls, the Routine's parameters and Connections — is then read from *that*
Version, and nothing is looked up through the Routine again. A Flow started
with `call_flow` inherits its parent's Version.

- **An Install mid-run does not affect the Run.** The old Flow keeps pairing
  with the old code until it ends. A Flow and the code it calls are
  published, versioned and installed together, and never mix.
- **A replay reads the same Version.** The Version is recorded in the Run's
  history, so re-executing an old Run cannot pick up newer files.
- **Data is not pinned.** Table Rows and Scalars are read live, so a Run that
  outlives an Install sees Rows the new Version wrote. The parameters and
  Connections behind `$channel.*` are pinned with the Run, so a parameter
  edited mid-run is seen only by later Runs. So is a Routine's installed
  [Recipe](https://docs.popcorn.ai/state-machine.md): a Run
  already going keeps judging Rows by the graph it started with.
- **Only `call_flow` inherits the Version.** `foundation.workflow.start_flow`
  starts a separate Run, which reads the Routine's Version when it starts: if
  an Install lands in between, a parent on Version *n* can launch a child on
  *n+1*. An App Agent's Flow tools are pinned to the Version of the turn that
  called them.
