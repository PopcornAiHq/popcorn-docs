---
id: versions
title: "Versions: publishing and installing"
order: 15
group: How a version ships
summary: >
  A change reaches a Routine in two steps: publishing mints an immutable
  version of a Routine Template on its copy, and installing brings each
  Routine on the copy to it, the one published from at once and the rest on
  their daily update. `install_routine` (`popcorn app apply`) retries a
  blocked install. A run keeps its version, so a Routine upgraded mid-run
  never mixes code.
concepts: [copying-a-template, app-bundle, manifest-keys]
part: build
---

A Routine runs one version of its template at a time. A change to the
template reaches it in two steps that are easy to conflate: a **publish**
makes a new version on the workspace's copy of the template (see
[copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md)),
and an **install** brings one Routine onto it. A version can exist while no
Routine runs it, and that gap is where most confusion about "did my change
go out" lives.

| To | Over MCP | With the CLI |
|---|---|---|
| read the files edits are based on | `list_routine_files`, `read_routine_file` | `popcorn app checkout --channel <routine>` |
| publish the next version | `create_routine_version` | `popcorn app publish` |
| see what a Routine runs, and whether its install landed | `get_routine` (**Version** and **Install**) | `popcorn app status` |
| retry an install that did not land | `install_routine` | `popcorn app apply` |

## Publishing

A publish mints the next version on a copy and starts an install on the
Routine it names. It is an operation on the copy, not on one Routine: every
other Routine on the copy takes the new version on its own daily update. It
needs a workspace admin.

`create_routine_version` is a dry run first. It shows the version it would
publish, each file's diff, every check it would fail, and the reach: how
many other Routines on the copy will update. `confirm=true` with the dry
run's `plan_id` publishes, running every check again. `popcorn app publish`
asks before it publishes, naming the copy rather than a count, and reports
the count only once the version exists.

A publish is based on the copy's newest version, its **head**. A publish
whose base is not the head is refused, because a diff computed against an
older version would drop whatever the versions in between changed. A
Routine's own version lags the head while an install has not landed, and
for good on a Routine that takes no updates; that is why
`list_routine_files` and `popcorn app checkout` read the head of a copy by
default, and an edit based on what a lagging Routine runs has to be redone
on a fresh read.

### What a publish refuses

A publish is refused when:

- the caller is not a workspace admin
- the request carries no file changes and no deletions
- the base is not a copy the workspace can see, or is no longer its head
- the named Routine runs a different copy, or Popcorn's version
- the tree has a path outside the bundle shape, two files under `prompts/` or
  `templates/` that would install under the same key (`prompts/x.md` and
  `prompts/x.txt`), or a root YAML file whose top level is not a mapping
- a flow does not parse strictly — a misspelled key, a `call_flow` naming its
  own flow or one the bundle does not have, or a `foreach` asking for more
  `max_parallel` than the platform allows
- the manifest has no `version:`, a version that does not advance, or a
  different `app_type` from its copy
- a flow name is not a slug, or a flow declares its own `trigger:`
- a `tables:` entry would be refused by the store at install — an unknown
  `type` or `display` kind, a `format` that does not suit its type, a merge
  setting without the policy it belongs to, and the other column rules in
  [adding a table](https://docs.popcorn.ai/build/guides/adding-a-table.md). The
  refusal names each table and column
- the version or its content already exists (below)

A manifest with **no** `app_type:` is not refused: publish treats it as the
copy's own template. Every install of that version then clears `app_type`
and `channel_agent` on each Routine it reaches, which is every Routine on the
copy. Keep both keys in every version, and treat `app validate`'s
`clears-app-type` warning as an error.

Every one of those checks asks *is this allowed and well-formed*. None asks
**did you mean to do this to every Routine on the copy**, and none refuses a
publish for its reach.

### A version never changes

A version is identified two ways: by its **semver on its copy**, the
manifest's `version:`, which you choose, and by a **digest** of its files,
which you do not. Popcorn's version and each copy are separate series, so two
copies can each hold a `1.0.1`. The number the CLI and MCP print as a
version's id (`version: 913`) is a third handle, assigned by Popcorn. A
publish has four outcomes:

| What you send | What happens |
|---|---|
| a new semver, new content | published |
| the same semver, byte-identical content | no-op, reported as such |
| the same semver, different content | refused — versions are immutable |
| a new semver, content identical to an earlier version on the copy | refused — the digest is taken |

A new semver must also be higher than the copy's newest. The CLI checks that
before sending; the server enforces it regardless.

So a mistake is corrected by publishing forward, never by editing, and
nothing moves a Routine back to an earlier version. An old version cannot be
republished byte for byte, because its digest is taken: bump the version and
change something — the manifest's `changelog:` saying why is the honest
change. An old version can be read back by its id, with `list_routine_files`
and `read_routine_file`'s `version`, or `popcorn app checkout --version <id>`,
which checks it out read-only: publishing from that checkout is refused.
Version ids are the numbers a publish and `popcorn app status` print; nothing
lists a copy's past versions. To make old content current again, take a
fresh read of the head, put the old files over it — deleting any file the old
version lacked — and publish forward with a bump.

## Installing

An install brings one Routine to one version: it reconciles its tables,
scalars, schedules, webhooks and configuration (the *channel config*, which
holds its parameters and Connections), and moves the Routine onto the version
last. Installs follow creating a Routine from a template, a publish, a retry
and each daily update.

**The daily update** installs the head of each Routine's copy once a day,
which is how a publish reaches the Routines you did not publish from, and how
a Routine on Popcorn's version reaches the newest version its workspace's
release track offers. It runs as the workspace, not as the person who
published. It never moves a Routine onto a copy, and it skips archived
Routines, Routines locked against template updates, and Routines with no
update schedule.

An install can be blocked — another install may be in progress, or the
Routine locked against template updates — and that is reported separately
from whether the publish succeeded, because the version publishes either way.
An install reported as started has not necessarily landed either: it
re-checks when it runs, and can still skip. `get_routine`'s **Install** line
and `popcorn app status` show what the Routine actually runs; `app status`
says whether an install is running, retrying, failed, skipped or locked,
with a failed install's error, a skipped one's reason, and a `Next:` line
saying what moves the Routine on.

**`install_routine` (`popcorn app apply`) is the retry.** It brings one
Routine on a copy up to the copy's head, takes no version from you — there
is no argument through which one Routine's content reaches another — and
says there is nothing to install (in the CLI's JSON, `already_current`) when
the Routine already runs the head. It works from the
server's state alone, so it still works after the session that published has
ended, which re-running the publish cannot cover. On a locked Routine it is
refused rather than queued. A Routine on Popcorn's version takes new versions
through its daily update, not through a retry; an install there in a
workspace that owns exactly one copy moves it onto that copy instead (see
[copying a template](https://docs.popcorn.ai/build/concepts/copying-a-template.md)).

## A run keeps the version it started on

When a flow starts, it reads the version its Routine runs once and records
it for that run. Everything the run needs — the flow, any code block it
calls, the Routine's parameters and Connections — is then read from *that*
version, and nothing is looked up through the Routine again. A flow started
with `call_flow` inherits its parent's version.

- **An install mid-run does not affect the run.** The old flow keeps pairing
  with the old code until it ends. A flow and the code it calls are
  published, versioned and installed together, and never mix.
- **A replay reads the same version.** The version is recorded in the run's
  history, so re-executing an old run cannot pick up newer files.
- **Data is not pinned.** Table rows and scalars are read live, so a run that
  outlives an install sees rows the new version wrote. The parameters and
  Connections behind `$channel.*` are pinned with the run, so a parameter
  edited mid-run is seen only by later runs. So is a Routine's installed
  [recipe](https://docs.popcorn.ai/build/concepts/state-machine.md): a run
  already going keeps judging rows by the graph it started with.
- **Only `call_flow` inherits the version.** `foundation.workflow.start_flow`
  starts a separate run, which reads the Routine's version when it starts: if
  an install lands in between, a parent on version *n* can launch a child on
  *n+1*. An app agent's flow tools are pinned to the version of the turn that
  called them.
