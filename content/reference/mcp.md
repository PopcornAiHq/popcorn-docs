---
id: mcp
title: MCP
order: 3
layout: lookup
deployed: 2026-10-16
summary: >
  The tools the hosted Popcorn MCP server gives a person's assistant —
  people, Routines, their Triggers, Actions, settings and tables, and a
  Routine's app — with their arguments, generated from the server's own
  definitions.
concepts: [app-bundle, publish-and-apply, fork-line]
layer: product
---

The hosted MCP server gives a person's assistant 27 tools. With them it
can find people and Routines, list the Routine Templates a new Routine can
be made from, create a Routine (optionally from a template), see whether a
Routine's Connections are made, see what starts its work and run a
schedule now, list and take the Actions on its items, read and change its
settings, read its tables and rows and add, change or delete rows, and read
the files of the app a Routine runs, fork it onto the workspace's own line,
publish changes to a fork line, and bring a Routine on a fork line to its
line's head or move it onto another line. They work on Routines only; a
Routine's messages and runs are read in Popcorn.

A Routine is what the CLI and the API call a channel, and its Routine
Template's code is what they call an app (an app bundle); the `#name` and
the IDs are the same.

Every call runs as the person who connected the server, with that person's
permissions, in the one workspace the connection is bound to; every
response starts with that workspace's name. To use another workspace,
reconnect. Read tools accept a Routine's `#name` or its ID as `routine`;
tools that write into a Routine take `routine_id`, the ID only. A listing
returns one page and a `next_cursor` to pass back with the same arguments.
A fork, a publish, an install that moves a Routine onto another line,
creating a Routine from a template, running a Trigger, taking an Action,
changing a setting and deleting rows are a dry run until called again with
`confirm=true`. An
install that brings a Routine to its own line's head starts at once, and
so does creating a Routine with no template.

This page is generated from the server's tool definitions by
`scripts/sync-mcp.py` after each prod deploy and never edited by hand; a
date beside the title is the day of the deploy that last changed it. The
badges under each tool are the access hints the server declares to the
host — `[read-only]`, or `[writes]` with `[destructive]` or `[idempotent]`
— and a host may use them to decide what to ask before calling. An argument
marked `[required]` must be passed; every other one may be left out.

Under some tools is an example: a request a person might make, then each
call an assistant makes for it, marked `→`, followed by what the tool
returns. The response is the server's real output for sample data — the
workspace Acme — produced by running the tool in the server's tests, so it
changes when the tool's output does. Examples leave out the workspace line
every response opens with. IDs are shortened, as `8c1f…e2`, a cursor keeps
its first characters, and a long listing keeps its first rows.

## Workspace and people

### `get_workspace`

[read-only]

The Popcorn workspace this connection is bound to.

Every tool acts in this one workspace. It was chosen when the user connected Popcorn and can't be changed from here: to use a different workspace, the user reconnects Popcorn.

**Example** — “Which Popcorn workspace are you connected to?”

```text
→ get_workspace()

Name: Acme
ID: 8c1f…e2
Slug: acme
Your role: member

This connection is bound to this workspace. To use a different one, the user reconnects Popcorn.
```

### `get_user`

[read-only]

Look up a person by handle: yourself, a member of this workspace, or someone from another workspace you share a Routine or DM with.

For a member: ID, username, display name, email, workspace role, whether they're active (no once deactivated or removed) and whether they're a bot. For someone from another workspace: display name, username and bot only. To find someone by name, use list_workspace_members. Someone from another workspace is found by user ID only, and so is a deactivated member: usernames and emails are looked up among this workspace's active members, since a username is unique only within one workspace.

| Argument | Type | Notes |
|---|---|---|
| `user` | `str` | "me" (the default) for yourself, or a user ID, email, or username ("@name" works too). "me" always means you, even if someone's username is "me"; look them up by email or ID. Other spellings such as "self" are refused. |

**Example** — “What's Jordan Lee's email, and are they still active?”

```text
→ get_user(user="@jlee")

ID: 5d33…0c
Username: jlee
Display name: Jordan Lee
Email: jordan@acme.example
Workspace role: member
Active: yes
Bot: no
```

### `list_workspace_members`

[read-only]

List the members of this workspace, alphabetically by name.

This workspace's members only: someone from another workspace who is in a shared Routine isn't listed here, and deactivated members never are. To look up one person by ID, email or @username (a bot included), use get_user.

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive text to find in a username, display name or email, e.g. "dana". A leading "@" also matches the username after it ("@dsmith"), and still matches inside emails, so "@acme.example" finds everyone at that domain. |
| `include_bots` | `bool` | Also list bots. Default `False`. |
| `cursor` | `str` | The next_cursor of the previous page, to continue. Pass the same query and include_bots as that call. |

**Example** — “Who on the Acme team is named Lee?”

```text
→ list_workspace_members(query="lee")

2 of 2 members matching "lee":
- Jordan Lee  @jlee  jordan@acme.example  member  (id: 5d33…0c)
- Sam Lee  @slee  sam@acme.example  admin  (id: 7a41…d2)
```

## Routines

### `list_routines`

[read-only]

List the Routines you can see in this workspace: the ones you're in (including Routines shared in from another workspace) and the ones you can view without joining (marked [not joined]).

Direct messages are not listed. Each row shows the Routine's name, its Routine Template, your unread count and mentions, and its ID; [missing a connection] marks one whose template needs an account nobody has connected. get_routine shows one Routine's version, install state and Connections.

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive substring of the Routine name. |
| `template` | `str` | Only Routines made from this Routine Template, by its slug (e.g. "claimcoordinator"). |
| `include_archived` | `bool` | Also list archived Routines (marked [archived]). Default `False`. |
| `sort` | one of `name`, `recent` | "name" (default), or "recent": pinned first, then by last message. |
| `cursor` | `str` | The next_cursor from the previous page, with the same other arguments. |

**Example** — “Which of our Routines use the Claim Coordinator template?”

```text
→ list_routines(template="claimcoordinator")

50 of 137 Routines running claimcoordinator:
- #claims-central  claimcoordinator  (id: 2af4…0c)
- #claims-east  claimcoordinator  4 unread, 1 mention  (id: be23…ef)  [pinned]  [missing a connection]
- #claims-north  claimcoordinator  (id: bd7d…b9)  [not joined]
- … 47 more rows
next_cursor: eyJ2Ijox…
```

### `get_routine`

[read-only]

Show one Routine: its details, your membership, and its Routine Template, with the version it's on, the latest version, where its updates come from (Popcorn, or this workspace's own copy of the template), whether the latest install landed, and its Connections: each account or webhook the template needs, and whether it's connected.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | The Routine's ID, or its name ("#intake" or "intake"). Names aren't unique: if more than one Routine has it, the call lists them with their IDs; pass an ID instead. |
| `wait_seconds` | `int` | Wait up to this many seconds for an install in progress to land (installed, or failed for good), then answer; the answer says whether it landed or the wait ran out. At most 20 (more is read as 20); 0, the default, doesn't wait. |

**Example** — “Is #intake on the latest version of its template?”

```text
→ get_routine(routine="#intake")

ID: c7d2…5b
Name: #intake
Kind: Routine
Description: New claims, triaged and assigned
Archived: no
Members (incl. bots): 9
Joined: yes
Your role: admin
Unread: 4
Mentions: 1
Muted: no
Template: claimcoordinator
Updates from: Popcorn
Version: 0.15.1 (the latest)
Install: installed
Connections:
- Claims inbox (email): connected: claims@acme.example (google)
- Adjuster calendar (calendar): NOT CONNECTED; work that uses it can't run
- Carrier portal (webhook): connected: carrier-portal
Whether a connected account still has the access it needs isn't checked here. A Routine member connects these in the Routine's settings in Popcorn.
```

### `list_routine_templates`

[read-only]

List the Routine Templates a new Routine in this workspace can start from.

Each row shows the template's name, its slug (what create_routine's `template` takes), what it does, and the connections someone sets up before it runs. A template this workspace can't run isn't listed.

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive substring of the template's name or slug. |
| `cursor` | `str` | The next_cursor from the previous page, with the same query. |

**Example** — “What templates could a new Routine here start from?”

```text
→ list_routine_templates()

5 of 5 Routine Templates:
- Alert Tracker  alerttracker  Ingests Alertmanager alerts from a webhook and keeps one row per alert.  needs no connections
- Chat  chat  A Routine with a calendar. Ask when everyone's free and it checks every connected calendar.  needs Google Calendar
- Claim Coordinator  claimcoordinator  Imports arbitration leads, emails each one its questions, and tracks every answer until the claim is complete.  needs Gmail, Google Calendar, Google Drive
- … 2 more rows
```

### `create_routine`

[writes]

Create a Routine in this workspace, optionally from a Routine Template.

Without `template` the Routine is created at once. With `template` the first call is a dry run that changes nothing: it shows the version that will install and the connections someone sets up before it runs. Call again with confirm=true to create it. The template installs in the background after the Routine exists; get_routine's Install: field shows when it lands. A name already used in this workspace is refused, with the ID of the Routine that has it.

| Argument | Type | Notes |
|---|---|---|
| `name` [required] | `str` | The Routine's name, e.g. "claims-west". Spaces become hyphens; the response shows the name it got. |
| `template` | `str` | A Routine Template's slug from list_routine_templates, e.g. "claimcoordinator". |
| `private` | `bool` | true for a private Routine, joined only by you and `members`. A Routine that isn't private adds everyone in the workspace. Default `False`. |
| `members` | `list[str]` | People to add to a private Routine: "@username", email or user ID, all members of this workspace. You're always a member. |
| `confirm` | `bool` | true to create a Routine from a template. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same request. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Set up a private #claims-west Routine from the claims template, with Jordan in it.”

```text
→ create_routine(name="claims-west", template="claimcoordinator", private=true, members=["@jlee"])

**Dry run.** Nothing was changed.

Create: #claims-west, a private Routine in Acme, running Claim Coordinator (claimcoordinator).
- Installs: claimcoordinator 0.15.1, the latest version.
- Members: you, @jlee.
- Connections to set up in the Routine before it runs: Gmail, Google Calendar, Google Drive.
- The install runs in the background once the Routine exists, typically in seconds; get_routine's Install: field shows when it lands.

Call again with `confirm=true` to create #claims-west running claimcoordinator.

→ create_routine(name="claims-west", template="claimcoordinator", private=true, members=["@jlee"], confirm=true)

Created #claims-west (id: 0141…b3), a private Routine in Acme.
Members: you, @jlee.
Claim Coordinator (claimcoordinator) is installing in the background. Watch get_routine("0141…b3")'s Install: field until it says installed.
Before the Routine runs, someone sets up in it: Gmail, Google Calendar, Google Drive.
```

## Apps

### `list_app_files`

[read-only]

List the files of the app a Routine runs, with sizes and sha256.

The header names the app, its line and the version listed. By default that's the version edits are based on, and its version_id is the publish base: on a fork line, the line's head; on the product line, the version the Routine runs, which is what a fork copies. Each row's sha256 is exact: copy it, don't retype it. Read a file's content with read_app_file. To change how one Routine behaves, check list_routine_settings first: a fork is one-way, and a publish reaches every Routine on the line.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `version_id` | `int` | Another version of the Routine's own line, to read history. Omit for the publish base. |
| `paths` | `list[str]` | Only files matching any of these: an exact path or a glob ("flows/*", "code/**"). |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What files make up the app #intake runs?”

```text
→ list_app_files(routine="#intake")

Routine: #intake (c7d2…5b)
App: claimcoordinator · line: product · version 0.15.1 (version_id: 812) · head: yes
6 of 6 files:
- AGENT.md  53 B  sha256: f7834927…
- flows/chase_estimate.yaml  21 B  sha256: 42def0cb…
- flows/daily_summary.yaml  20 B  sha256: 802c3a2f…
- … 3 more rows
```

### `read_app_file`

[read-only]

Read one file of the app a Routine runs, exactly as stored.

The content is never cut. A file too big for one response comes in byte ranges: the header says which bytes this is, and next_cursor reads the next range. Join the ranges in order to get the file, whose sha256 the header gives. Everything after the "Content:" line is the file's text, verbatim.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `path` [required] | `str` | The file's path, as list_app_files shows it. |
| `version_id` | `int` | Another version of the Routine's own line. Omit for the publish base. |
| `cursor` | `str` | next_cursor from the previous range. |

**Example** — “Show me #intake's app manifest.”

```text
→ read_app_file(routine="#intake", path="manifest.yaml")

Routine: #intake (c7d2…5b)
App: claimcoordinator · line: product · version 0.15.1 (version_id: 812) · head: yes
File: manifest.yaml  75 B  sha256: 4331d221…
Whole file.
Content:
app_type: claimcoordinator
display_name: Claim Coordinator
version: 0.15.1
```

### `fork_app`

[writes] [destructive]

Fork the app a Routine runs into a new, named fork line.

The line starts as a byte-identical copy of the product version the Routine runs, and the Routine moves onto it. That's one-way: the Routine never returns to the product line, stops receiving product updates, and from then on gets only what's published to its line. Only a fork line can be published to, with publish_app. To change how one Routine behaves, check list_routine_settings first: a setting reaches one Routine and can be set back. Fork only for what settings can't express. Validate an edit before forking with publish_app's dry run, since the fork is the step that can't be undone. Without confirm=true this is a dry run that changes nothing.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `name` [required] | `str` | The new line's name: lowercase letters, digits, "-" and "_", starting with a letter or digit. Fork only creates a line; to move a Routine onto a line that exists, use install_app(line=...). |
| `confirm` | `bool` | true to fork. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same request. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Give #intake its own copy of the claims app, called acme-intake, so we can change its intake form.”

```text
→ fork_app(routine_id="c7d2…5b", name="acme-intake")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Fork: claimcoordinator 0.15.1 (product line, version_id: 812) → new fork line "acme-intake".
- The line starts as a byte-identical copy of 0.15.1. Nothing the Routine runs changes now.
- #intake moves onto the line. Product updates stop reaching it.
- One-way: a Routine on a fork line never returns to the product line. From then on it follows "acme-intake", and versions published there reach it within a day.
- Reach: this Routine only. Other Routines running claimcoordinator stay where they are.
- Other fork lines of claimcoordinator in this workspace: "acme-west" (to join one instead: install_app(line=…)).

Call again with `confirm=true` to fork the app into line "acme-intake".
```

### `install_app`

[writes] [destructive]

Install the newest version of a Routine's line on the Routine.

It installs the app the Routine already runs, never another one: a Routine runs another app only by creating a new Routine with create_routine(template=…). Without line, this is a catch-up (as `popcorn app apply`): a Routine on a fork line installs its line's head. It runs without confirm, because the daily update would install the same version. Use it after a publish whose install was blocked, or when get_routine shows the Routine behind its line. With line, or when a product-line Routine would join the workspace's only fork line, it's an adoption: the Routine moves onto that fork line, one-way, and installs its head. An adoption is a dry run that changes nothing unless confirm=true. It doesn't put an app on a Routine that has none, and product versions reach product-line Routines through the daily update, not through this tool. To change how one Routine behaves, check list_routine_settings first; a move between lines is one-way.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `line` | `str` | A fork line of this Routine's app to move onto. |
| `confirm` | `bool` | true to make an adoption. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id an adoption's dry run gave, with confirm=true and the same line. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Move #intake onto our acme-west version of the claims app.”

```text
→ install_app(routine_id="c7d2…5b", line="acme-west")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Install: #intake moves from claimcoordinator 0.15.1 (product line) onto fork line "acme-west", at its head 0.16.0 (version_id: 913).
- This changes which line the Routine is on. It installs 0.16.0, which isn't what the Routine runs now.
- One-way: a Routine on a fork line never returns to the product line. From then on it follows "acme-west", and versions published there reach it within a day.
- Reach: this Routine only.

Call again with `confirm=true` to move #intake onto line "acme-west".
```

### `publish_app`

[writes] [destructive]

Publish changes to a Routine's app as the next version of its line.

A publish reaches every Routine on the Routine's fork line: this Routine installs the new version now, and every other Routine on the line updates at its daily check. Workspace admins only. To change how one Routine behaves, check list_routine_settings first, and publish only what settings can't express. Without confirm=true it's a dry run that changes nothing: the version it would publish, each file's diff, every check it would fail, warnings and the reach, and a plan_id. To publish, call again with routine_id, confirm=true and that plan_id alone: the changes needn't be sent again, and every check runs again. A Routine on the product line can dry-run changes, but must fork_app before publishing them. Each change is one file. A change to a file that exists carries the sha256 it was read at: copy it exactly from list_app_files or read_app_file. {"path": "manifest.yaml", "expected_sha256": "…", "ops": […]} {"path": "flows/new.yaml", "create": "<whole file>"} {"path": "flows/old.yaml", "delete": true, "expected_sha256": "…"} {"path": "flows/a.yaml", "rename": "flows/b.yaml", "expected_sha256": "…"} {"path": "code/x/lib.js", "from_url": "https://unpkg.com/…", "sha256": "…"} {"path": "code/x/app.js", "from_upload": "<upload_id>"} Ops apply in order. To rewrite a whole file, delete it and create it again. Bump `version:` in manifest.yaml in every publish. Every op is a text op. The anchor is the file's exact text and must match once: {"op": "replace", "old_string": "cron: 0 9 * * *", "new_string": "cron: 0 8 * * *"}. Also insert_before and insert_after (anchor, text), prepend and append (text), and replace_range (from, to, new_string), which replaces from `from` up to `to`: `to` is not replaced and stays in the file, so never end new_string with it. from_url has Popcorn fetch a public UTF-8 text file, so you needn't send its content: unpkg.com, cdn.jsdelivr.net, registry.npmjs.org, raw.githubusercontent.com or a github.com release download; at most 10 files and 4 MiB per publish. Pin a version in the URL. To replace an existing file, add its expected_sha256. The dry run shows each file's sha256, and the publish takes exactly that content: a confirm by plan_id holds it, and a confirm that resends the changes must give each from_url change that sha256. Content that changed since the dry run is refused. from_upload takes a file you uploaded with create_app_upload, for this Routine and path. Its size and sha256 were fixed when you created it, so it needs no sha256 here. It counts toward the same 10 files and 4 MiB as from_url, and is published once.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). It installs the new version first. |
| `base_version_id` | `int` | The version_id the files were read from, as list_app_files' header shows it: the line's head. |
| `changes` | `list[Change]` | The changes, one per file, applied in order. |
| `changelog` | `str` | What changed and why, in a sentence or two. |
| `confirm` | `bool` | true to publish. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true, in place of base_version_id, changes and changelog. |
| `diff` | `DiffLevel` | How much of each file's diff the dry run shows: "full" (the default), "summary" (line counts) or "none". A deleted file is always one line. |

**Example** — “On #intake, chase estimates at 8 instead of 9, and publish it.”

```text
→ publish_app(routine_id="c7d2…5b", base_version_id=913, changes=[{"path": "manifest.yaml", "expected_sha256": "0454e71d37086e35e6b9e5e41daf6f5a7bf3f27835a897efcfb664edbe7b3d87", "ops": [{"op": "replace", "old_string": "version: 0.16.0", "new_string": "version: 0.16.1"}, {"op": "replace", "old_string": "cron: 0 9 * * 1-5", "new_string": "cron: 0 8 * * 1-5"}, {"op": "replace", "old_string": "# Chase open estimates before the adjusters' stand-up.", "new_string": "# Chase open estimates an hour before stand-up."}]}], changelog="Chase open estimates at 8, an hour before stand-up.")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Publish: claimcoordinator 0.16.0 (version_id: 913) → 0.16.1 on fork line "acme-intake".
Files:
- manifest.yaml: edited, 3 ops applied
  ```diff
  --- a/manifest.yaml
  +++ b/manifest.yaml
  @@ -1,8 +1,8 @@
   app_type: claimcoordinator
   display_name: Claim Coordinator
  -version: 0.16.0
  +version: 0.16.1
   schedules:
  -  # Chase open estimates before the adjusters' stand-up.
  +  # Chase open estimates an hour before stand-up.
     - slug: chase-estimates
       flow: chase_estimate
  -    cron: 0 9 * * 1-5
  +    cron: 0 8 * * 1-5
  ```
Reach: #intake would install it now. 2 other Routines on this line will update at their daily check.
plan_id: pL4nC0nf1rmByRef9xQ2a7 (lasts 30 minutes)

Call again with `confirm=true` to publish 0.16.1 to line "acme-intake": pass routine_id and plan_id="pL4nC0nf1rmByRef9xQ2a7" in place of base_version_id, changes and changelog.

→ publish_app(routine_id="c7d2…5b", confirm=true, plan_id="pL4nC0nf1rmByRef9xQ2a7")

Routine: #intake (c7d2…5b)
Published claimcoordinator 0.16.1 (version_id: 44) to fork line "acme-intake". It is now the line's head.
#intake is installing it now.
Reach: 2 other Routines on this line will update at their daily check.
Published is not installed: get_routine's Install: field shows when #intake has it.
Files now (the base for a next edit is version_id 44; use these sha256s as expected_sha256):
- manifest.yaml  sha256: d00a8443…
```

### `create_app_upload`

[writes]

Get a URL to upload one file you made, for publish_app to take.

For a file too large to send in a change, such as a bundled script or a generated data file. Works only where your organization allows uploads.popcorn.ai in claude.ai's network egress settings. Upload with the curl line this returns, then publish with the change {"path": …, "from_upload": "<upload_id>"}. If the upload fails or can't connect, don't retry it: use from_url for a public file, or send the content in the change. One file per upload, for this Routine and path only. The upload must be exactly `size` bytes with this `sha256`, or it is refused; UTF-8 text only, at most 4 MiB. The URL works for 15 minutes, and the upload can be published for most of a day. Workspace admins only, like publish_app.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name), as for publish_app. |
| `path` [required] | `str` | The bundle path the file will be published at, e.g. code/engine/lib.js. |
| `size` [required] | `int` | The file's size in bytes. |
| `sha256` [required] | `str` | The file's sha256, as 64 hex characters (`sha256sum FILE`). |

**Example** — “I bundled the chess engine into engine.js; publish it to #intake's app without pasting it.”

```text
→ create_app_upload(routine_id="c7d2…5b", path="code/engine/engine.js", size=48213, sha256="9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c")

Routine: #intake (c7d2…5b)
Upload for code/engine/engine.js: 48,213 bytes, sha256 9f2c9f2c….
upload_id: 3f6a…93
method: PUT
url: https://uploads.popcorn.ai/staging/8c1f…e2/3f6a…93?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=5e1d…
headers:
  x-amz-checksum-sha256: nyyfLJ8s…
URL expires: 2026-10-13T18:15:00Z. Publishable until 2026-10-14T17:00:00Z.

Run this with FILE replaced by the file's path; it prints nothing when the upload succeeds:
curl -fsS -T FILE -H 'x-amz-checksum-sha256: nyyfLJ8s…' 'https://uploads.popcorn.ai/staging/8c1f…e2/3f6a…93?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=5e1d…'

Then publish it with this change (add expected_sha256 to replace a file that exists):
{"path": "code/engine/engine.js", "from_upload": "3f6a…93"}
If curl can't connect to uploads.popcorn.ai, this organization doesn't allow it: use from_url for a public file, or send the content in the change.
```

## Routine settings

### `list_routine_settings`

[read-only]

List the settings of a Routine's Routine Template, set or not.

A setting changes how this Routine alone behaves: sending modes, schedules, limits, and the prompts and email templates its agents use. A changed setting reaches one Routine, can be set back, and is kept through template updates, so check here before giving the Routine its own copy of its template (fork_app). Each prompt or email template file is its own setting, so changing one leaves the others following template updates. Each row shows the value; an unset one says what unset means, and one changed from the template default says so. Secrets show only whether they're set. get_routine_setting shows one in full; update_routine_setting changes one.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `query` | `str` | Only settings whose key or label contains this. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What can I change about how #chase-renewals chases people, without giving it its own copy of its template?”

```text
→ list_routine_settings(routine="#chase-renewals", query="chase")

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
4 of 4 settings matching "chase":
- chase_days  [1, 3, 7]
- chase_max_followups  5  (changed; template default 10)
- chase_window_timezone  America/Los_Angeles
- prompts.chase_email  Hi {{ name }}, just following up on the documents we asked for last week. If you've already sent them, thank you, and pl… [truncated; get_routine_setting(key="prompts.chase_email") for the full text]
2 values set on this Routine are read by nothing and not shown.
```

### `get_routine_setting`

[read-only]

One of a Routine's settings in full: the whole value (a prompt or email template's whole text), the template default, what it accepts, its description, its options with the warning each one carries, and who may change it.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `key` [required] | `str` | The setting's key, as list_routine_settings shows it. |

**Example** — “Show me the email #chase-renewals sends when it chases someone.”

```text
→ get_routine_setting(routine="#chase-renewals", key="prompts.chase_email")

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
Setting: prompts.chase_email
Value:
Hi {{ name }}, just following up on the documents we asked for last week. If you've already sent them, thank you, and please ignore this note.

The {{ firm }} team

Template default: the same as the value
Accepts: text, the shape of the template default
Changed by: update_routine_setting, by a workspace admin who's also a member of the Routine.
```

### `update_routine_setting`

[writes] [destructive]

Change one of a Routine's settings, on this Routine only.

Without confirm=true this is a dry run that changes nothing: it shows the old and new value, what the setting does, and the warning the new option carries. For a long value it also gives a plan_id: to change it, call again with the key, confirm=true and that plan_id, and the value needn't be sent again. Setting the template default resets the setting. A switch takes one of its options; any other setting keeps the shape of the template default (a list stays a list, a number a number). Secrets and the Routine's Instructions aren't changed here. For a long text (a prompt, an email template, agent guidance), pass changes instead of value: text ops applied in order to the current text, as publish_app's ops are. The anchor is the text exactly and must match once: {"op": "replace", "old_string": "Hi {{name}},", "new_string": "Hello {{name}},"}. Also insert_before and insert_after (anchor, text), prepend and append (text), and replace_range (from, to, new_string). A value with credentials inside it shows them as [secret]. Keep [secret] exactly where a read shows it; the stored credential stays in place. Credentials, and what surrounds them, change in the app.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `key` [required] | `str` | The setting's key, as list_routine_settings shows it. |
| `value` | `Any` | The whole new value: text, a number, a list, a mapping, or null. Omit it to pass changes instead. Default `OMITTED`. |
| `changes` | `list[Op]` | Text ops on the current text, instead of value. |
| `confirm` | `bool` | true to change it. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true, in place of value and changes. |

**Example** — “Stop chasing after five follow-ups on #chase-renewals.”

```text
→ update_routine_setting(routine_id="4b0e…12", key="chase_max_followups", value=5)

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
**Dry run.** Nothing was changed.

Change: chase_max_followups on #chase-renewals.
- 10 → 5
- Reach: this Routine only. It can be set back with update_routine_setting. Template updates won't change the new value.

Call again with `confirm=true` to change chase_max_followups.

→ update_routine_setting(routine_id="4b0e…12", key="chase_max_followups", value=5, confirm=true)

Routine: #chase-renewals (4b0e…12) · template: chase 0.3.1
Changed chase_max_followups on #chase-renewals: 10 → 5.
Runs already under way keep the value they started with.
```

## Tables

### `list_tables`

[read-only]

List the tables in a Routine, with each one's row count.

A Routine's tables hold the rows its template, agents and people keep. get_table shows a table's columns; list_rows reads its rows.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What does #intake keep track of?”

```text
→ list_tables(routine="#intake")

Routine: #intake (c7d2…5b)
2 of 2 tables:
- claims  212 rows
- Contacts  3 rows
```

### `get_table`

[read-only]

A table's columns, in order: each one's name, type, label and merge policy, the table's merge key, and its state machine if the Routine runs one on it.

A merge policy says what a write that merges into an existing row does to that column: replace (the default), keep the first value, concat (append), or increment_on_change (a counter the store keeps). Columns marked as state change only when one of the state machine's transitions fires, so create_rows and update_row refuse them.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |

**Example** — “What columns does #intake's claims table have?”

```text
→ get_table(routine="#intake", table="claims")

Routine: #intake (c7d2…5b) · table: claims
Table: claims  (schema version 3)
Merge key: none; create_rows merges only on the columns its merge_on names.
Columns (11), in order:
- claim_no  string  label "Claim #"
- claimant  string  [personal data]
- amount  number
- Status  string  [state: changed only by transitions]
- Stage  string  [state: changed only by transitions]
- Decision  string  [fact a transition writes]
- Notes  string  merge: concat
- First seen  string  merge: keep
- api_token  string  [credential: never shown or written]
- home_address  string  [personal data]
- summary  string  [personal data]
State machine:
- Status column: Status · Actions: CTAs · sub: Stage
- funnel (column Stage): open, closed
```

### `list_rows`

[read-only]

List a table's rows, newest first unless sort says otherwise.

Each row shows its ID, a few columns (long values are cut and marked; get_row shows a row in full) and when it last changed.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `query` | `str` | Text to find in any column, case-insensitively: "4471" finds the row whatever column holds it. Only rows where it appears in a value you can see are listed, so with query (or filter["*"]) a page can come back short, there's no total, and next_cursor goes on to the rest. |
| `filter` | `dict[str, Any]` | Conditions on columns, all of which must hold: {"Status": "open"} or {"Status": {"$eq": "open"}}, {"amount": {"$gt": 1000}}, {"claimant": {"$contains": "ortiz"}}, {"Status": {"$in": ["open", "waiting"]}}, {"closed_at": {"$exists": false}}. Operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $exists, $contains. There's no $or. Text compares case-insensitively. |
| `columns` | `list[str]` | The columns to show, by name. By default, the first few in the table's order (get_table lists them). |
| `sort` | `str` | "column:asc" or "column:desc". By default, newest first. On a workspace that guards personal data, a column whose values are hidden can't be sorted on. |
| `cursor` | `str` | next_cursor from the previous page, with the same other arguments. When the rows end exactly at a page's end, the last page comes back empty. |

**Example** — “Find claim 4471 in #intake.”

```text
→ list_rows(routine="#intake", table="claims", query="4471")

Routine: #intake (c7d2…5b) · table: claims
Columns shown: claim_no, claimant, amount, Status, Stage (of 11; columns=[…] picks others). Empty values are left out.
2 rows matching "4471", newest first, shown on this page:
- row 91  claim_no: 44710  claimant: Lee  amount: 900  (updated 2026-09-29 14:05)
- row 88  claim_no: 4471  claimant: Ortiz  amount: 12400  Status: open  Stage: open  (updated 2026-09-29 14:05)
```

### `get_row`

[read-only]

One row in full: every column, its rev (update_row needs it as expected_rev), when it was created and last changed, and its state if the Routine's state machine runs on the table.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_id` [required] | `int` | The row's ID, as list_rows shows it ("row 88" is 88). |

**Example** — “Show me everything on row 88 of #intake's claims.”

```text
→ get_row(routine="#intake", table="claims", row_id=88)

Routine: #intake (c7d2…5b) · table: claims
Row: 88  rev: 4  created 2026-09-01 10:00  updated 2026-09-29 14:05
State: Status = open · Stage = open
- claim_no: 4471
- claimant: Ortiz
- amount: 12400
- Status: open
- Stage: open
- Decision: (empty)
- Notes: (empty)
- First seen: (empty)
- api_token: [hidden: holds a credential]
- home_address: 12 Elm St
- summary: Ortiz called about the roof
```

### `create_rows`

[writes]

Add rows to one of a Routine's tables.

A row whose merge key matches an existing row merges into it instead of adding another: the table's own merge key if it has one (get_table shows it), else the columns merge_on names. A merge on merge_on changes only the columns the row carries, each by the column's merge policy. A merge on the table's own key follows that key's setting: merge works the same way, but replace overwrites the matched row whole, emptying every column the new row leaves out (refused where that would erase the row's state or a credential). The response says which rows were added and which merged. Adding rows starts no work. Columns the Routine's state machine owns are refused (they change only by a transition), and so are credential columns. Each call adds its rows: if a call timed out, check with list_rows before sending it again.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `rows` [required] | `list[dict[str, Any]]` | The rows, each an object of column: value. At most 50. |
| `merge_on` | `list[str]` | Columns that identify an existing row to merge into, for a table with no merge key of its own. |

**Example** — “Add claim 5002 for Kim, $900, to #intake, and update 4471's amount to 13,000 while you're at it.”

```text
→ create_rows(routine_id="c7d2…5b", table="claims", rows=[{"claim_no": "5002", "claimant": "Kim", "amount": 900}, {"claim_no": "4471", "amount": 13000}], merge_on=["claim_no"])

Routine: #intake (c7d2…5b) · table: claims
Added 1 row and merged 1 into existing rows:
- row 301  added
- row 88  merged into the existing row
get_row shows one in full.
```

### `update_row`

[writes] [idempotent]

Change some columns of one row.

Only the columns in data change; the rest stay as they are. Each changes by its merge policy, and the response names any column where that policy, not the value sent, decided what's stored. expected_rev is the rev get_row shows. If the row has changed since (its rev moved on), nothing is written and the response shows the row as it is now, with its new rev, so you can decide again. Changing a row starts no work. Columns the Routine's state machine owns are refused (they change only by a transition), and so are credential columns.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_id` [required] | `int` | The row's ID ("row 88" is 88). |
| `data` [required] | `dict[str, Any]` | The columns to change, as column: value. |
| `expected_rev` [required] | `int` | The row's rev, from get_row. |

**Example** — “Add a note to claim 4471 in #intake that the adjuster called back.”

```text
→ update_row(routine_id="c7d2…5b", table="claims", row_id=88, data={"Notes": "Adjuster called back 10/6."}, expected_rev=4)

Routine: #intake (c7d2…5b) · table: claims
Changed row 88: rev 4 → 5.
Where the table's merge policy decided what's stored:
- Notes: the value sent was appended to the stored text (merge: concat).
The row as stored:
- claim_no: 4471
- claimant: Ortiz
- amount: 12400
- Status: open
- Stage: open
- Decision: (empty)
- Notes: Claimant called 9/28.
  Adjuster called back 10/6.
- First seen: (empty)
- api_token: [hidden: holds a credential]
- home_address: 12 Elm St
- summary: Ortiz called about the roof
```

### `delete_rows`

[writes] [destructive] [idempotent]

Delete rows from one of a Routine's tables, by ID.

Without confirm=true this is a dry run that deletes nothing: it lists the rows it would delete. Show the person the dry run, and confirm only once they agree. A deleted row can't be restored with these tools. Rows are deleted one at a time, and the response says which were deleted, which were already gone and which failed.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_ids` [required] | `list[int]` | The rows' IDs ("row 88" is 88). At most 50. |
| `confirm` | `bool` | true to delete. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same table and row_ids. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Delete the duplicate row 91 from #intake's claims.”

```text
→ delete_rows(routine_id="c7d2…5b", table="claims", row_ids=[91])

Routine: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Delete 1 row from claims:
- row 91  claim_no: 44710  claimant: Lee  amount: 900  (updated 2026-09-29 14:05)
- Warning: the Routine's state machine runs on this table; a deleted row leaves the Routine's tracker and its open items.
- A deleted row can't be restored with these tools. Deleting starts no work.

Call again with `confirm=true` to delete this row.

→ delete_rows(routine_id="c7d2…5b", table="claims", row_ids=[91], confirm=true)

Routine: #intake (c7d2…5b) · table: claims
Deleted 1 of 1 rows: row 91.
```

## Triggers

### `list_triggers`

[read-only]

List how work arrives in a Routine: each schedule with its cadence, each webhook another system posts to, each message or document that starts work.

A Trigger that is paused or turned off says so. A webhook's address is never shown: it is a credential. run_trigger runs a schedule now.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What sets #intake working?”

```text
→ list_triggers(routine="#intake")

Routine: #intake (c7d2…5b) · template: claimcoordinator 0.15.1
Schedules:
- morning  cron '0 8 * * 1-5' (America/Los_Angeles)  starts daily digest
- tick  every 180s  starts claim tick
Webhooks:
- carrier-portal  starts claim intake
Messages:
- a message posted in #intake  starts claim intake
Documents:
- uploading the 'policy' document  starts policy upsert
```

### `run_trigger`

[writes] [destructive]

Run one of a Routine's schedules now, with the inputs it runs with on schedule.

Its schedule is unchanged: the next scheduled run still happens. The run does what the schedule's work does, for real. Without confirm=true this is a dry run that starts nothing and says what will run. Each confirmed call starts a run, so don't repeat one that timed out: the run may have started.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `trigger` [required] | `str` | The schedule's name, as list_triggers shows it. |
| `confirm` | `bool` | true to start the run. Show the user the dry run first. Default `False`. |

**Example** — “Send #intake's morning digest now; don't wait.”

```text
→ run_trigger(routine_id="c7d2…5b", trigger="morning")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Run: the morning schedule's work (daily digest) on #intake, now.
- Schedule: cron '0 8 * * 1-5' (America/Los_Angeles); unchanged by this run.
- It runs as it would on schedule, in the background: posts, emails and row changes are real.

Call again with `confirm=true` to run it now.

→ run_trigger(routine_id="c7d2…5b", trigger="morning", confirm=true)

Routine: #intake (c7d2…5b)
Started morning (daily digest).
It runs in the background; the Routine's runs in Popcorn show how it ended.
```

## Actions

### `list_actions`

[read-only]

List the Actions a person can take on one of a Routine's items now, given where it stands: the buttons Popcorn shows on it, each with the Status it moves the item to. take_action takes one.

Some Actions need the Popcorn app (a form to fill in, a document to sign, a request to the Routine's agent); they're listed and marked.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `row_id` [required] | `int` | The item's row ID in the Routine's main table, as list_rows shows it ("row 88" is 88). |

**Example** — “What can I do with claim 4471 in #intake?”

```text
→ list_actions(routine="#intake", row_id=88)

Routine: #intake (c7d2…5b) · table: claims
Row 88 · Status: open
Actions offered now:
- Close claim  action: close  moves it to: Closed
- Ask for documents  action: ask_docs  [in the Popcorn app]
```

### `take_action`

[writes] [destructive]

Take one Action on one or more of a Routine's items, as a person pressing its button in Popcorn would.

Refused for an item the Action isn't offered on now. Without confirm=true this is a dry run: it says what happens to each item and gives a run_key. To act, call again with the same items and action, confirm=true and that run_key. A run_key acts once: calling again with it finds the run it started.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `row_ids` [required] | `list[int]` | The items' row IDs in the Routine's main table. |
| `action` [required] | `str` | The Action, as list_actions names it (its "action"). |
| `confirm` | `bool` | true to act. Show the user the dry run first. Default `False`. |
| `run_key` | `str` | The run_key the dry run gave, with confirm=true. |

**Example** — “Close claim 4471 in #intake.”

```text
→ take_action(routine_id="c7d2…5b", row_ids=[88], action="close")

Routine: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Take: close on 1 item(s), now.
- row 88: open → Closed (Close claim)
- It runs as the workspace's agent, for you, as the button would: what the Action sends or records is real.
- run_key: Hc4pW8sN…

Call again with `confirm=true` to take it, with run_key="Hc4pW8sN…" and the same items.

→ take_action(routine_id="c7d2…5b", row_ids=[88], action="close", confirm=true, run_key="Hc4pW8sNz1bVq6Tj20d155d5c65bdaaa")

Routine: #intake (c7d2…5b) · table: claims
Taking close on 1 item(s).
It applies in the background; get_row shows each item's new Status once it has.
```

## Proposed tools

**None of these tools exist yet, and nothing depends on them arriving.** They
are a design for the tools a person's assistant uses to run Routines, named
in the [product glossary](https://docs.popcorn.ai/product/glossary/product-glossary.md)'s
terms rather than the platform's. They are listed so an author can see what is
being considered; names and arguments may change before any ships.

The message, flow, run and stored-value tools have already left this
surface: a Routine's work starts from its Triggers and Actions, a switch is a
Routine Setting, and its conversation and runs are read in Popcorn until
History arrives here. Changing a Routine Template itself is not part of this
design.

Three rules run through it:

1. **Ask for the outcome; Popcorn picks the mechanism.** A tool takes what
   the person wants changed, in product terms, and Popcorn decides which
   setting, document or step has to change to get it.
2. **Every write is a dry run until `confirm=true`**, and the dry run says
   whether the change stays with this Routine or gives it a copy of its own,
   which stops receiving its template's improvements.
3. **Reads take `routine`** (its ID or `#name`); **writes take `routine_id`**,
   since a write is the worst place to resolve a name to the wrong Routine.

### `duplicate_routine`

Makes a new Routine that starts as a copy of an existing one: its template,
Routine Settings, Instructions and References, but none of its items or
History. Connections are not copied, because they sign in as a person.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | The Routine to copy |
| `name` | | The new Routine's name |
| `confirm` | `false` | Create the previewed copy |

### `change_routine`

Changes how a Routine works, from a plain-language request such as "remind
the client every three days instead of weekly" or "add an approval before
anything is sent". Without `confirm`, returns the plan: what will change, in
product terms, and whether the change stays with this Routine or gives it a
copy of its own. The confirming call carries the plan's ID, so only the
previewed plan is applied.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | Routine ID |
| `request` | | What should change, in the person's words |
| `plan_id` | | From the dry run; required with `confirm` |
| `confirm` | `false` | Apply the previewed plan |

### `list_connections`

Read-only. The Connections a Routine needs, each with whether it is made,
whose account it uses, and what stops while it is missing. Making one is a
person's job, in the browser; the result says where.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |

### `list_references`

Read-only. The documents a Routine works from, each with what it is used for,
when it was added and by whom, and the ones the Routine is still waiting for.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |

### `read_reference`

Read-only. One Reference's text, or a download link for a file that is not
text.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `reference` | | As `list_references` names it |

### `add_reference`

Adds a document to a Routine, or replaces one, from text or a file the
caller uploaded. Without `confirm`, says what the Routine will do with it.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | Routine ID |
| `reference` | | Which document this is, as `list_references` names it |
| `text` | | The document as text |
| `upload_id` | | A file uploaded for this Routine, in place of `text` |
| `confirm` | `false` | Add the previewed document |

### `get_instructions`

Read-only. A Routine's Instructions in plain language: how it words its
messages, what it asks a person about first, its deadlines and reminders.
Each part says whether it is the template's or was changed for this Routine.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |

### `update_instructions`

Changes a Routine's Instructions. Takes the change in plain language or as
an edit to the text `get_instructions` returned. Without `confirm`, shows the
Instructions as they would read after the change.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | Routine ID |
| `request` | | The change, in the person's words |
| `edits` | | Or exact edits to the text, in place of `request` |
| `confirm` | `false` | Apply the previewed change |
| `reset` | `false` | Return a changed part to the template's |

### `get_status`

Read-only. Where a Routine's items stand: a count per Status, the items
waiting on a person, and the stages an item moves through. One item's Status
is on its Row.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `table` | | The Table to count; the Routine's main one by default |

### `list_history`

Read-only. What has happened in a Routine, newest first: work it ran and how
each ended, its conversation, and changes to its items, each with who or what
made it.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `kind` | all | `work`, `conversation` or `changes` |
| `row_id` | | Only what happened to this item |
| `since` | | ISO-8601 time |
| `cursor` | | From the previous page |

### `read_history_entry`

Read-only. One entry from `list_history` in full: a run's steps and result, a
message and its replies, or a change's before and after.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `entry_id` | | From `list_history` |
