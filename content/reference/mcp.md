---
id: mcp
title: MCP
order: 3
layout: lookup
updated: 2026-10-27
summary: >
  The tools the hosted Popcorn MCP server gives a person's assistant —
  people, Routines, their Triggers, Actions, settings and tables, and a
  Routine's app — with their arguments, generated from the server's own
  definitions.
concepts: [app-bundle, versions, copying-a-template]
---

The hosted MCP server gives a person's assistant 43 tools. With them it
can find people and Routines, list the Routine Templates a new Routine can
be made from, create a Routine (optionally from a template), see whether a
Routine's Connections are made and make one from an account already
signed in to or as a webhook, see what starts its work and run a
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
making a Connection, changing a setting and deleting rows are a dry run
until called again with
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
- #claims-central  Claim Coordinator (claimcoordinator)  (id: 2af4…0c)
- #claims-east  Claim Coordinator (claimcoordinator)  4 unread, 1 mention  (id: be23…ef)  [pinned]  [missing a connection]
- #claims-north  Claim Coordinator (claimcoordinator)  (id: bd7d…b9)  [not joined]
- … 47 more rows
next_cursor: eyJ2Ijox…
```

### `get_routine`

[read-only]

Show one Routine: its details, your membership, and its Routine Template, with the version it's on, the latest version, where its updates come from (Popcorn, or this workspace's own copy of the template), whether the latest install landed, and its Connections: each account or webhook the template needs, and whether it's connected.

A Routine made with duplicate_routine also shows how far its copy got, and any part that didn't copy, with why. A Routine whose template has Steps also lists them in order, with which version of them is installed: each Step's kind (Answers, Signature, Booking, Reminder, Delivery, or Review, where a person decides), its name and the Status value an item at it holds (what list_rows filters on), the ways an item leaves it on its own, and each Review's reason and choices with where each leads. A choice marked [in Popcorn] opens a form there; take_action takes the others.

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
Template: Claim Coordinator (claimcoordinator)
Updates from: Popcorn
Version: 0.15.1 (the latest)
Install: installed
Connections:
- Claims inbox (email): connected: claims@acme.example (google)
- Adjuster calendar (calendar): NOT CONNECTED; work that uses it can't run
- Carrier portal (webhook): connected: carrier-portal
Whether a connected account has since been revoked or its sign-in has expired isn't checked here. A Routine member connects these in the Routine's settings in Popcorn.
list_connections says whose account each one uses and what stops without it.
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

Without `template` the Routine is created at once (for Popcorn's channel agent it is a dry run first, like any other). With `template` the first call is a dry run that changes nothing: it shows the version that will install and the connections someone sets up before it runs. Call again with confirm=true to create it. The template installs in the background after the Routine exists; get_routine's Install: field shows when it lands. A name already used in this workspace is refused, with the ID of the Routine that has it.

| Argument | Type | Notes |
|---|---|---|
| `name` [required] | `str` | The Routine's name, e.g. "claims-west". Spaces become hyphens; the response shows the name it got. |
| `template` | `str` | A Routine Template's slug from list_routine_templates, e.g. "claimcoordinator". |
| `private` | `bool` | true for a private Routine, joined only by you and `members`. A Routine that isn't private adds everyone in the workspace. |
| `members` | `list[str]` | People to add to a private Routine: "@username", email or user ID, all members of this workspace. You're always a member. |
| `confirm` | `bool` | true to create a Routine from a template. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true. It stands in for template, private and members: leave them out and the create takes the dry run's, or send them and they must be the same. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

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

### `duplicate_routine`

[writes]

Create a new Routine in this workspace that copies an existing one's setup: its Routine Template, on the same line, its Routine Settings and agent notes, its own Steps, its guidelines, and the References it has added.

Nothing is copied that belongs to the work or the people: not its items, History, messages or members, not what people told its agent, and not its Connections or credentials, which sign in as someone. A Reference picked from Google Drive is picked again in Popcorn once the new Routine has a Google Drive connection. The first call is a dry run that changes nothing: it lists every part that will be copied and every part left out. Call again with confirm=true to create the Routine. The template installs in the background, then the copy runs; get_routine's Copied from: field shows each part as it lands, and any that didn't, with why. A name already used in this workspace is refused, with the ID of the Routine that has it. You need to be a workspace admin or a member of the Routine you copy, and able to create Routines here.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The ID of the Routine to copy (not its name). |
| `name` [required] | `str` | The new Routine's name, e.g. "claims-east". Spaces become hyphens; the response shows the name it got. |
| `private` | `bool` | true for a private Routine, joined only by you and `members`. A Routine that isn't private adds everyone in the workspace. The original's members aren't copied. |
| `members` | `list[str]` | People to add to a private Routine: "@username", email or user ID, all members of this workspace. You're always a member. |
| `confirm` | `bool` | true to create the Routine. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true. It stands in for private and members: leave them out and the copy takes the dry run's, or send them and they must be the same. A Routine's own agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Make a copy of #claims-west for the east office, called claims-east.”

```text
→ duplicate_routine(routine_id="0141…b3", name="claims-east")

**Dry run.** Nothing was changed.

Duplicate: #claims-east, a Routine in Acme, copied from #claims-west.
- Template: Claim Coordinator (claimcoordinator), fork line "acme" at 0.15.1-acme.2, as #claims-west is.
- Joins fork line "acme", this workspace's own copy of the template. One-way: a Routine on its own copy of a template never goes back to Popcorn's. From then on it follows copy "acme", and new versions of that copy reach it within a day.
- Members: everyone in the workspace (a Routine that isn't private adds every member).
Copied:
- Routine Settings and agent notes: 2 changed from the template's (chase_days, popcorn.agent_notes.intake).
- Steps: the Routine's own ("Claims intake", installed 2026-10-12, sha256 3f9c1a0b2d4e).
- Guidelines for its agent: 1.
- References: questions, each read into the copy as it was first added.
Not copied:
- References picked from Google Drive: standard_retainer. The new Routine starts with no Google Drive connection, so these are picked again in Popcorn once someone connects it.
- Credentials among its Routine Settings: crm_api_key. Set them in the new Routine in Popcorn.
- Connections: Gmail, Google Calendar, Google Drive. Someone sets them up in the new Routine before it runs.
- What people told its agent, and its items, History, messages and members.
The template installs in the background once the Routine exists, then the copy runs, typically within a few minutes; get_routine's Copied from: field shows each part as it lands.

Call again with `confirm=true` to create #claims-east as a copy of #claims-west.

→ duplicate_routine(routine_id="0141…b3", name="claims-east", confirm=true)

Created #claims-east (id: be23…ef), a Routine in Acme, copied from #claims-west.
Members: everyone in the workspace (a Routine that isn't private adds every member).
Claim Coordinator (claimcoordinator) is installing in the background, and the copy runs once it lands. Watch get_routine("be23…ef")'s Copied from: field until every part is in.
Before the Routine runs, someone sets up in it: Gmail, Google Calendar, Google Drive.
Pick again in Popcorn once Google Drive is connected: standard_retainer.
```

### `change_routine`

[writes] [destructive]

Change a Routine's Steps by describing the change in words, previewed before anything is installed, or put back an earlier version of its Steps.

Only a Routine whose template keeps its Steps with the Routine can be changed this way; any other is refused with what changes it instead (a Routine Setting, or a copy of its template of its own). For a change that is only a Routine Setting, update_routine_setting is quicker. Three calls: - request: starts drafting the change and returns a change_id. Drafting takes minutes; get_routine_change shows the proposal, as the Steps before and after. Nothing is installed. One change drafts at a time per Routine. - change_id with confirm=true: installs that proposal, once the person has read it. Sent again, it finds the install it started. - revert_to: "previous", "template" or a version, as get_routine_change names them. Without confirm it checks the revert against the Routine's items and gives a run_key; with confirm=true and that run_key it installs it.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `request` | `str` | The change, in the person's words ("after the retainer is signed, ask for their insurance card"). |
| `change_id` | `str` | The change_id change_routine returned, with confirm=true, to install its proposal. |
| `confirm` | `bool` | true to install. Show the person the proposal (or the revert's check) first. Default `False`. |
| `revert_to` | `str` | "previous", "template", or a version (sha) to go back to. |
| `run_key` | `str` | The run_key a revert's check gave, with confirm=true. |
| `plan_id` | `str` | The plan_id get_routine_change or the revert's check gave, with confirm=true; it stands in for the run_key. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “In #intake, once a claimant signs the retainer, have them book the interview straight away.”

```text
→ change_routine(routine_id="c7d2…5b", request="Once a claimant signs the retainer, ask them to book the interview straight away, and remind them after 2 days, then 5.")

Routine: #intake (c7d2…5b)
Drafting the change. change_id: 8c1f3a52…
Nothing is installed: the Routine's agent drafts the new Steps and checks them against this Routine's items, which takes a few minutes. get_routine_change with this change_id shows the proposal, as the Steps before and after, for the person to read before it goes in.

→ get_routine_change(routine="#intake", change_id="8c1f3a520d4e4b7a9f216a0c5d7b31e2-c7d20b9e5f134a8cb6e29d41f0a7c35b-recipe_build-req-Rv3kQ8pLm2Wx7Tz5a0d439dec3cde555", wait_seconds=20)

Routine: #intake (c7d2…5b)
Waited 2s: the change moved on.
Change 8c1f3a52…: proposed. Nothing is installed yet.
Asked for: "Once a claimant signs the retainer, ask them to book the interview straight away, and remind them after 2 days, then 5."
Steps, before → after (- before, + after):
  3. Signature — Getting signatures (Status value: signing)
+    - on its own: The claimant signed the standard retainer agreement and is asked to book the interview → Scheduling meeting (step 5)
On install it also sets, per Step:
- Scheduling meeting (interview): reminders 2, then 5 days after the last email; its email's wording: subject
  This part is a Routine Setting: update_routine_setting chase_days changes it for every Step without settings of its own, and leaves the Steps as they are.
The author assumed:
- The booking email goes out as soon as the agreement is signed; the team no longer decides on the interview first.
Questions it left open:
- Should claimants who already had their interview skip the booking email?
Checks: passed against this Routine's items and template; no item is left at a Step that would go (recipe version 1bf13eb70563).
To install it: change_routine with change_id="8c1f3a52…" and confirm=true, once the person has read it. An open question above may change it; a new request starts a new change.

→ change_routine(routine_id="c7d2…5b", change_id="8c1f3a520d4e4b7a9f216a0c5d7b31e2-c7d20b9e5f134a8cb6e29d41f0a7c35b-recipe_build-req-Rv3kQ8pLm2Wx7Tz5a0d439dec3cde555", confirm=true)

Routine: #intake (c7d2…5b)
Installing change 8c1f3a52…. It checks the proposal once more against the Routine's items and puts it in only if it is unchanged; get_routine_change shows when it's done.
```

### `get_routine_change`

[read-only]

Where a change to a Routine's Steps stands: still drafting, the proposal as Steps before and after, refused and why, or installed.

A proposal shows the Steps that change, what it would set on each Step (saying which part is a Routine Setting the person could change directly), the author's assumptions and open questions, and the checks it passed. An installed change names the version before it, which change_routine's revert_to puts back.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `change_id` [required] | `str` | The change_id change_routine returned. |
| `wait_seconds` | `int` | Wait up to this many seconds for a change that is drafting or installing to move on, then answer. At most 20 (more is read as 20); 0, the default, doesn't wait. |
| `detail` | `str` | "recipe" adds the recipe's own text diff to a proposal, for people who author templates. |

**Example** — “Did the change to #intake's Steps go in?”

```text
→ get_routine_change(routine="#intake", change_id="wf-draft")

Routine: #intake (c7d2…5b)
Change wf-draft: installed 2026-10-19T09:06:00+00:00 (version 1bf13eb70563).
Steps, before → after (- before, + after):
  3. Signature — Getting signatures (Status value: signing)
+    - on its own: The claimant signed the standard retainer agreement and is asked to book the interview → Scheduling meeting (step 5)
get_routine shows all 16 Steps.
Set:
- `interview`: reminders 2, then 5 days after our last email; copy subject
Before it: version 0096e731db97. To go back: change_routine with revert_to="0096e731…".
```

## Apps

### `list_routine_files`

[read-only]

List the files of the Routine Template version a Routine runs, with sizes and sha256.

The header names the template, whether it is Popcorn's or the workspace's own copy, and the version listed. By default that's the version edits are based on: on a copy, its newest version; on Popcorn's template, the version the Routine runs, which is what a copy starts from. That version is the base_version create_routine_version takes. Each row's sha256 is exact: copy it, don't retype it. Read a file's content with read_routine_file. To change how one Routine behaves, check list_routine_settings first: a copy of the template is one-way, and a new version reaches every Routine on that copy.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `version` | `int | str` | An older version of the Routine's template, to read its history. Pass its number ("0.15.1") or its version id. Omit for the base for edits. |
| `paths` | `list[str]` | Only files matching any of these: an exact path or a glob ("flows/*", "code/**"). |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What files make up the app #intake runs?”

```text
→ list_routine_files(routine="#intake")

Routine: #intake (c7d2…5b)
Template: Claim Coordinator (claimcoordinator) · Popcorn's · 0.15.1 (version 812) · newest: yes
6 of 6 files:
- AGENT.md  53 B  sha256: f7834927…
- flows/chase_estimate.yaml  21 B  sha256: 42def0cb…
- flows/daily_summary.yaml  20 B  sha256: 802c3a2f…
- … 3 more rows
```

### `read_routine_file`

[read-only]

Read one file of the Routine Template version a Routine runs, exactly as stored.

The content is never cut. A file too big for one response comes in byte ranges: the header says which bytes this is, and next_cursor reads the next range. Join the ranges in order to get the file, whose sha256 the header gives. Everything after the "Content:" line is the file's text, verbatim.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `path` [required] | `str` | The file's path, as list_routine_files shows it. |
| `version` | `int | str` | An older version of the Routine's template: its number ("0.15.1") or its version id. Omit for the base for edits. |
| `cursor` | `str` | next_cursor from the previous range. |

**Example** — “Show me #intake's app manifest.”

```text
→ read_routine_file(routine="#intake", path="manifest.yaml")

Routine: #intake (c7d2…5b)
Template: Claim Coordinator (claimcoordinator) · Popcorn's · 0.15.1 (version 812) · newest: yes
File: manifest.yaml  75 B  sha256: 4331d221…
Whole file.
Content:
app_type: claimcoordinator
display_name: Claim Coordinator
version: 0.15.1
```

### `copy_routine_template`

[writes] [destructive]

Give a Routine its own named copy of the Routine Template it runs.

The copy starts byte-identical to the version of Popcorn's template the Routine runs, and the Routine moves onto it. That's one-way: the Routine never goes back to Popcorn's template, stops receiving Popcorn's improvements, and from then on gets only the new versions of its copy. Only a copy takes new versions, with create_routine_version. To change how one Routine behaves, check list_routine_settings first: a setting reaches one Routine and can be set back. Copy the template only for what settings can't express. Check an edit first with create_routine_version's dry run, since the copy is the step that can't be undone. Without confirm=true this is a dry run that changes nothing.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `name` [required] | `str` | The copy's name: lowercase letters, digits, "-" and "_", starting with a letter or digit. This only creates a copy; to move a Routine onto a copy that exists, use install_routine(copy=...). |
| `confirm` | `bool` | true to make the copy. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same request. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Give #intake its own copy of the claims app, called acme-intake, so we can change its intake form.”

```text
→ copy_routine_template(routine_id="c7d2…5b", name="acme-intake")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Copy: Popcorn's Claim Coordinator (claimcoordinator) 0.15.1 (version 812) → new copy "acme-intake".
- The copy starts byte-identical to 0.15.1. Nothing the Routine runs changes now.
- #intake moves onto the copy. Popcorn's improvements stop reaching it.
- One-way: a Routine on its own copy of a template never goes back to Popcorn's. From then on it follows copy "acme-intake", and new versions of that copy reach it within a day.
- Reach: this Routine only. Other Routines running Claim Coordinator (claimcoordinator) stay where they are.
- Other copies of Claim Coordinator (claimcoordinator) in this workspace: "acme-west" (to move onto one instead: install_routine(copy=…)).

Call again with `confirm=true` to make copy "acme-intake" of the template.
```

### `install_routine`

[writes] [destructive]

Install the newest version of a Routine's copy of its template, or move it onto a copy the workspace already has.

It installs the Routine Template the Routine already runs, never another one: a Routine runs another template only by creating a new Routine with create_routine(template=…). Without copy, this is a catch-up (as `popcorn app apply`): a Routine on its own copy installs that copy's newest version. It runs without confirm, because the daily update would install the same version. Use it after a create_routine_version whose install was blocked, or when get_routine shows the Routine behind its copy. With copy, or when a Routine on Popcorn's template would join the workspace's only copy, the Routine moves onto that copy, one-way, and installs its newest version. A move is a dry run that changes nothing unless confirm=true. It doesn't put a template on a Routine that has none, and Popcorn's new versions reach Routines on Popcorn's template through the daily update, not through this tool. To change how one Routine behaves, check list_routine_settings first; a move onto a copy is one-way.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `copy` | `str` | The name of a copy of this Routine's template to move onto, as copy_routine_template named it. |
| `confirm` | `bool` | true to make the move. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id a move's dry run gave, with confirm=true and the same copy. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Move #intake onto our acme-west version of the claims app.”

```text
→ install_routine(routine_id="c7d2…5b", copy="acme-west")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Install: #intake moves from Popcorn's Claim Coordinator (claimcoordinator) 0.15.1 onto copy "acme-west", at its newest version 0.16.0 (version 913).
- This changes which copy of the template the Routine follows. It installs 0.16.0, which isn't what the Routine runs now.
- One-way: a Routine on its own copy of a template never goes back to Popcorn's. From then on it follows copy "acme-west", and new versions of that copy reach it within a day.
- Reach: this Routine only.

Call again with `confirm=true` to move #intake onto copy "acme-west".
```

### `create_routine_version`

[writes] [destructive]

Save changes as the next version of the Routine's own copy of its Routine Template.

A new version reaches every Routine on that copy: this Routine installs it now, and every other Routine on the copy updates at its daily check. Workspace admins only. To change how one Routine behaves, check list_routine_settings first, and make a version only for what settings can't express. Without confirm=true it's a dry run that changes nothing: the version it would create, each file's diff, every check it would fail, warnings and the reach, and a plan_id. To create it, call again with routine_id, confirm=true and that plan_id alone: the changes needn't be sent again, and every check runs again. A Routine on Popcorn's template can dry-run changes, but needs its own copy (copy_routine_template) before they can be made. Each change is one file. A change to a file that exists carries the sha256 it was read at: copy it exactly from list_routine_files or read_routine_file. {"path": "manifest.yaml", "expected_sha256": "…", "ops": […]} {"path": "flows/new.yaml", "create": "<whole file>"} {"path": "flows/old.yaml", "delete": true, "expected_sha256": "…"} {"path": "flows/a.yaml", "rename": "flows/b.yaml", "expected_sha256": "…"} {"path": "code/x/lib.js", "from_url": "https://unpkg.com/…", "sha256": "…"} {"path": "code/x/app.js", "from_upload": "<upload_id>"} Ops apply in order. To rewrite a whole file, delete it and create it again. Bump `version:` in manifest.yaml in every new version. Every op is a text op. The anchor is the file's exact text and must match once: {"op": "replace", "old_string": "cron: 0 9 * * *", "new_string": "cron: 0 8 * * *"}. Also insert_before and insert_after (anchor, text), prepend and append (text), and replace_range (from, to, new_string), which replaces from `from` up to `to`: `to` is not replaced and stays in the file, so never end new_string with it. from_url has Popcorn fetch a public UTF-8 text file, so you needn't send its content: unpkg.com, cdn.jsdelivr.net, registry.npmjs.org, raw.githubusercontent.com or a github.com release download; at most 10 files and 4 MiB per version. Pin a version in the URL. To replace an existing file, add its expected_sha256. The dry run shows each file's sha256, and the confirm takes exactly that content: a confirm by plan_id holds it, and a confirm that resends the changes must give each from_url change that sha256. Content that changed since the dry run is refused. from_upload takes a file you uploaded with create_routine_file_upload, for this Routine and path. Its size and sha256 were fixed when you created it, so it needs no sha256 here. It counts toward the same 10 files and 4 MiB as from_url, and goes into one version only.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). It installs the new version first. |
| `base_version` | `int | str` | The version the files were read from, as list_routine_files' header shows it: the copy's newest version. Its number ("0.16.0") or its version id. Just after copy_routine_template, the Popcorn version the copy was made from works too. |
| `changes` | `list[Change]` | The changes, one per file, applied in order. |
| `changelog` | `str` | What changed and why, in a sentence or two. |
| `confirm` | `bool` | true to create the version. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true, in place of base_version, changes and changelog. |
| `diff` | `DiffLevel` | How much of each file's diff the dry run shows: "full" (the default), "summary" (line counts) or "none". A deleted file is always one line. |

**Example** — “On #intake, chase estimates at 8 instead of 9, and publish it.”

```text
→ create_routine_version(routine_id="c7d2…5b", base_version=913, changes=[{"path": "manifest.yaml", "expected_sha256": "0454e71d37086e35e6b9e5e41daf6f5a7bf3f27835a897efcfb664edbe7b3d87", "ops": [{"op": "replace", "old_string": "version: 0.16.0", "new_string": "version: 0.16.1"}, {"op": "replace", "old_string": "cron: 0 9 * * 1-5", "new_string": "cron: 0 8 * * 1-5"}, {"op": "replace", "old_string": "# Chase open estimates before the adjusters' stand-up.", "new_string": "# Chase open estimates an hour before stand-up."}]}], changelog="Chase open estimates at 8, an hour before stand-up.")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

New version: Claim Coordinator (claimcoordinator) 0.16.0 (version 913) → 0.16.1 on copy "acme-intake".
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
Reach: #intake would install it now. 2 other Routines on this copy will update at their daily check.
plan_id: pL4nC0nf1rmByRef9xQ2a7 (lasts 30 minutes)

Call again with `confirm=true` to create version 0.16.1 of copy "acme-intake": pass routine_id and plan_id="pL4nC0nf1rmByRef9xQ2a7" in place of base_version, changes and changelog.

→ create_routine_version(routine_id="c7d2…5b", confirm=true, plan_id="pL4nC0nf1rmByRef9xQ2a7")

Routine: #intake (c7d2…5b)
Created version 0.16.1 (version 44) of Claim Coordinator (claimcoordinator), copy "acme-intake". It is now the copy's newest version.
#intake is installing it now.
Reach: 2 other Routines on this copy will update at their daily check.
Created is not installed: get_routine's Install: field shows when #intake has it.
Files now (the base for a next edit is version 44; use these sha256s as expected_sha256):
- manifest.yaml  sha256: d00a8443…
```

### `create_routine_file_upload`

[writes]

Get a URL to upload one file you made, for create_routine_version to take.

For a file too large to send in a change, such as a bundled script or a generated data file. Works only where your organization allows uploads.popcorn.ai in claude.ai's network egress settings. Upload with the curl line this returns, then create the version with the change {"path": …, "from_upload": "<upload_id>"}. If the upload fails or can't connect, don't retry it: use from_url for a public file, or send the content in the change. One file per upload, for this Routine and path only. The upload must be exactly `size` bytes with this `sha256`, or it is refused; UTF-8 text only, at most 4 MiB. The URL works for 15 minutes, and the upload can go into a version for most of a day. Workspace admins only, like create_routine_version.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name), as for create_routine_version. |
| `path` [required] | `str` | The path the file will have in the template, e.g. code/engine/lib.js. |
| `size` [required] | `int` | The file's size in bytes. |
| `sha256` [required] | `str` | The file's sha256, as 64 hex characters (`sha256sum FILE`). |

**Example** — “I bundled the chess engine into engine.js; publish it to #intake's app without pasting it.”

```text
→ create_routine_file_upload(routine_id="c7d2…5b", path="code/engine/engine.js", size=48213, sha256="9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c9f2c")

Routine: #intake (c7d2…5b)
Upload for code/engine/engine.js: 48,213 bytes, sha256 9f2c9f2c….
upload_id: 3f6a…93
method: PUT
url: https://uploads.popcorn.ai/staging/8c1f…e2/3f6a…93?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=5e1d…
headers:
  x-amz-checksum-sha256: nyyfLJ8s…
URL expires: 2026-10-13T18:15:00Z. Usable in a version until 2026-10-14T17:00:00Z.

Run this with FILE replaced by the file's path; it prints nothing when the upload succeeds:
curl -fsS -T FILE -H 'x-amz-checksum-sha256: nyyfLJ8s…' 'https://uploads.popcorn.ai/staging/8c1f…e2/3f6a…93?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=5e1d…'

Then pass it to create_routine_version with this change (add expected_sha256 to replace a file that exists):
{"path": "code/engine/engine.js", "from_upload": "3f6a…93"}
If curl can't connect to uploads.popcorn.ai, this organization doesn't allow it: use from_url for a public file, or send the content in the change.
```

## Setup

### `get_setup`

[read-only]

Show a Routine's setup checklist, the steps on its Today tab in Popcorn, in order: each done or not, which are required, and what each one left still needs (a Connection, a document, a booking page, a value).

A step that keeps a value shows what is set. It only reads. A Routine whose template builds its checklist from its Steps says when that hasn't happened yet, and lists the template's own steps meanwhile. A Routine with no checklist says so.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What's left to set up on #intake?”

```text
→ get_setup(routine="#intake")

Routine: #intake (c7d2…5b)
Setup: 4 of 6 steps done; 1 required left.
- [done] Connect your company email (step: connect_email)
- [left] Connect the adjusters' calendar (step: connect_calendar)
  Needs a Connection: make_connection makes it, and list_connections shows what it needs.
- [done, required] Intake: choose the questions document (step: document_questions)
- [done] Add your booking page (step: connect_booking_link) · set: "Consult with Acme"
  Warning: No booking of this page yet, so whose calendar it is can't be told until its first booking.
- [left, required] Days to wait for a reply (step: setting_wait_days)
  Needs a value for Days to wait for a reply (days, 1–30); it is set in the Routine's Today tab.
- [done] Connect your intake form (step: connect_intake_webhook)
Also needed, with no step Popcorn shows: secret:portal_token.
```

## Routine settings

### `list_routine_settings`

[read-only]

List the settings of a Routine's Routine Template, set or not.

A setting changes how this Routine alone behaves: sending modes, schedules, limits, and the prompts and email templates its agents use. A changed setting reaches one Routine, can be set back, and is kept through template updates, so check here before giving the Routine its own copy of its template (copy_routine_template). Each prompt or email template file is its own setting, so changing one leaves the others following template updates. Each row shows the value; an unset one says what unset means, and one changed from the template default says so. Secrets show only whether they're set. get_routine_setting shows one in full; update_routine_setting changes one.

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

Without confirm=true this is a dry run that changes nothing: it shows the old and new value, what the setting does, and the warning the new option carries. For a long value it also gives a plan_id: to change it, call again with the key, confirm=true and that plan_id, and the value needn't be sent again. Setting the template default resets the setting. A switch takes one of its options; any other setting keeps the shape of the template default (a list stays a list, a number a number). Secrets and the Routine's Steps aren't changed here. For a long text (a prompt, an email template, agent guidance), pass changes instead of value: text ops applied in order to the current text, as create_routine_version's ops are. The anchor is the text exactly and must match once: {"op": "replace", "old_string": "Hi {{name}},", "new_string": "Hello {{name}},"}. Also insert_before and insert_after (anchor, text), prepend and append (text), and replace_range (from, to, new_string). A value with credentials inside it shows them as [secret]. Keep [secret] exactly where a read shows it; the stored credential stays in place. Credentials, and what surrounds them, change in the app.

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

## Instructions

### `get_instructions`

[read-only]

A Routine's Instructions in one read: the guidance its agents work from, Routine-wide and for each Step, each with where it came from (the template's, or changed for this Routine) and what changes it.

The layers: the Routine's guidance per agent, its prompt files, its agent notes, its guidelines for its agent, what people told the agent, each Step's note, copy, questions and deadlines, and the template's guide (AGENT.md). Without step, the Routine-wide layers are shown in full and each Step is summarised; with step, that Step's are shown in full. A Routine whose template has no Steps has no per-Step layers. On a workspace that guards personal data, what people told the agent shows each memory's category and date, not its text.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `step` | `str` | One Step, by its label or its Status value, as get_routine lists the Steps. Omit for the whole Routine. |

**Example** — “What instructions is #intake's agent following?”

```text
→ get_instructions(routine="#intake")

Routine: #intake (c7d2…5b) · template: chase 0.84.0
The Routine's Instructions, by layer: where each came from, and what changes it.

## Routine guidance per agent (from this Routine's Steps, "Acme intake", installed 2026-10-12, sha256 1a2b3c4d5e6f)
Changed by: with change_routine (describe the change), or in Popcorn by telling the Routine's agent.
- chasewriter:
  Write as a person on the Acme claims team.
  Never promise when a claim will be paid.
- chasevalidator:
  An answer that names a month and a year is a date.
- chasewriter, at Booking Steps only:
  Offer the adjuster call link before anything else.

## Prompt files
Changed by: update_routine_setting, by a workspace admin who's also a member of the Routine.
- prompts.validator (the template's):
  Judge each answer against its question.
- prompts.writer (changed for this Routine):
  You write the claims team's emails.
  Be brief.
  Use the claimant's first name.

## Agent notes
Changed by: update_routine_setting, by a member of the Routine.
- popcorn.agent_notes.chasewriter (set for this Routine):
  Copy the adjuster on anything about money.
- None set: popcorn.agent_notes.chasevalidator.

## The Routine's guidelines for its agent
Changed by: in Popcorn.
- Claims intake:
  Answer in plain English; never quote policy clauses.

## What people told the agent (2, newest first)
Changed by: in Popcorn, by telling the agent.
- preferences  2026-10-14: Mrs. Ortiz prefers a call after 5pm.
- decisions  2026-10-09: Water damage under $2,000 skips the adjuster call.

## Each Step's note, copy, questions and deadlines
Changed by: with change_routine (describe the change), or in Popcorn by telling the Routine's agent.
1. Answers — Collecting claim details (Status value: intake):
   note "Ask for the policy number before anything else.", set for this Routine, chase.intake.guidance; 3 questions; subject "A few questions about your claim"; deadlines: the recipe's table is in force: 1 period(s) from item q2.
2. Review — Needs adjuster review (Status value: review): a Review, decided by a person; no instructions of its own.
3. Booking — Booking the adjuster call (Status value: interview):
   note "Keep it to two sentences." (+1 more), in this Routine's Steps; a booking page.
get_instructions(routine="#intake", step="<Status value>") shows one Step's in full.

## The template's guide
Changed by: a member of the Routine, in Popcorn. A template update keeps a change made to this Routine's copy.
- AGENT.md (the template's): 1,475 characters, first heading "Claims intake agent". How the Routine's agent talks and what it knows about the template. Popcorn shows its text.
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

Without confirm=true this is a dry run that adds nothing: it says which rows would be added and which would merge into an existing row, and what an added row starts. A new row on the table the Routine's Statuses run on is a new item, and the Routine's work acts on it for real (on a Routine that sends email, its first email goes out on the next run). Show the person the dry run, and confirm only once they agree. Popcorn's channel agent adds the rows a member asked for at once, with no dry run, as it does update_row. A row whose merge key matches an existing row merges into it instead of adding another: the table's own merge key if it has one (get_table shows it), else the columns merge_on names. A merge on merge_on changes only the columns the row carries, each by the column's merge policy. A merge on the table's own key follows that key's setting: merge works the same way, but replace overwrites the matched row whole, emptying every column the new row leaves out (refused where that would erase the row's state or a credential). The confirmed response says which rows were added and which merged. Columns the Routine's Statuses own are refused (they change only by an Action), and so are credential columns. Each confirm adds its rows: if one timed out, check with list_rows before sending it again.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `rows` [required] | `list[dict[str, Any]]` | The rows, each an object of column: value. At most 50. |
| `merge_on` | `list[str]` | Columns that identify an existing row to merge into, for a table with no merge key of its own. |
| `confirm` | `bool` | true to add the rows, sending the same rows and merge_on as the dry run. Show the user the dry run first. Default `False`. |

**Example** — “Add claim 5002 for Kim, $900, to #intake, and update 4471's amount to 13,000 while you're at it.”

```text
→ create_rows(routine_id="c7d2…5b", table="claims", rows=[{"claim_no": "5002", "claimant": "Kim", "amount": 900}, {"claim_no": "4471", "amount": 13000}], merge_on=["claim_no"])

Routine: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Add 2 rows to claims; each row sent, in order:
- 1: added
- 2: merges into row 88 (on claim_no)
- Each added row is a new item: it starts at its first Status, and the Routine's own work picks it up on its next run (list_triggers shows what runs and when). What that work does with it is real: on a Routine that sends email, the item's first email.
- A merge changes an existing item's columns; its Status changes only by an Action or the Routine's own work.

Call again with `confirm=true` to add them, sending the same rows.

→ create_rows(routine_id="c7d2…5b", table="claims", rows=[{"claim_no": "5002", "claimant": "Kim", "amount": 900}, {"claim_no": "4471", "amount": 13000}], merge_on=["claim_no"], confirm=true)

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

Its schedule is unchanged: the next scheduled run still happens. The run does what the schedule's work does, for real. Without confirm=true this is a dry run that starts nothing and says what will run. Each confirmed call starts a run, so don't repeat one that timed out: the run may have started. A started run comes back with its reference, which list_history's run follows.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `trigger` [required] | `str` | The schedule's name, as list_triggers shows it. |
| `confirm` | `bool` | true to start the run. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same request. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Send #intake's morning digest now; don't wait.”

```text
→ run_trigger(routine_id="c7d2…5b", trigger="morning")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Run: the morning schedule's work on #intake, now.
- Schedule: cron '0 8 * * 1-5' (America/Los_Angeles); unchanged by this run.
- It runs as it would on schedule, in the background: posts, emails and row changes are real.

Call again with `confirm=true` to run it now.

→ run_trigger(routine_id="c7d2…5b", trigger="morning", confirm=true)

Routine: #intake (c7d2…5b)
Started the morning schedule's work.
Run: run_WzEs…
It runs in the background. list_history with that run shows how it is going or how it ended, and the items it changed; each of those items' own History lists it too.
```

## Connections

### `list_connections`

[read-only]

List the Connections a Routine needs: the accounts and other services its template works through.

For each, whether it is made, whose account it uses, and what stops while it is missing. A Connection whose account is connected but hasn't given the Routine all the access it needs counts as not made. Whether an account has since been revoked isn't checked. make_connection makes one from an account you have already signed in to, or makes its webhook. Signing in to a new account is a person's job, done in Popcorn in the browser; the response says where. Seeing a Routine's Connections needs workspace admin, or membership of the Routine.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “Why hasn't #intake booked any inspections?”

```text
→ list_connections(routine="#intake")

Routine: #intake (c7d2…5b)
3 Connections, 1 not made:
- Claims inbox (email): made
  Uses: claims@acme.example (google), connected by Dana Smith
  Without it: Popcorn shows the Routine as not ready, and claim intake can't run.
- Adjuster calendar (calendar): NOT MADE
  Without it: book inspection can't run; the rest of the Routine keeps working.
- Carrier portal (webhook): made
  Uses: webhook carrier-portal
  Without it: Popcorn shows the Routine as not ready, and nothing from the other system starts claim intake.
Whether a connected account has since been revoked or its sign-in has expired isn't checked here.
make_connection makes a Connection from an account the person has already signed in to, or makes its webhook. For a Google account not yet signed in to, or one whose sign-in lacks access, make_connection gives a sign-in link to pass on when it can. Any other account is signed in to in Popcorn, in the browser: open #intake (https://app.popcorn.ai/ws/acme/conversation/c7d2…5b), then its settings, then Automations, which lists its Connections.
```

### `make_connection`

[writes] [destructive]

Make one of a Routine's Connections: connect an account you have signed in to, or make the webhook another system posts to.

For an email, calendar, files or documents (Notion) Connection, call it without account first: it lists your accounts that can serve it, each with whether its sign-in allows everything the Connection needs. Then call it with account, an address or ID from that list: a dry run of what it will connect, what it replaces and what runs after. With confirm=true it connects the account, gives the Routine the access it needs, and runs the template's on_auth_change step if it has one, all in one call. The answer is each Connection made, as list_connections shows it. Only your own accounts can be connected; a teammate connects theirs. Connecting an account to a Connection that has none also connects it to the Routine's other Connections of its provider that have none yet and that its sign-in allows (one Google account serves the inbox, calendar and Drive together); the dry run names each one, and the answer says which were connected. Pass only=true to connect the named Connection alone. Replacing a Connection's account changes no other. A Google sign-in is done from here: when you have no Google account that can serve, or yours is signed out or lacks access, the answer (or the refusal) carries a sign-in link, asking for everything the Routine's unconnected Google Connections need. Pass the link to the person as it is, and nothing else from it: it works once, within minutes, and only for the person who asked, who finishes it signed in to Popcorn in the browser it opens. Once they say they have, call make_connection again (without account, to see the account, then with it). An account of another provider is signed in to in Popcorn; the answer says where. For a webhook Connection, call it without account: a dry run of the webhook it makes, and of the one it replaces if one serves it already, whose address then stops working. With confirm=true it makes the webhook and answers with its address, once. The address is a credential: anyone who has it can post to the Routine. Give it only to whoever sets up the other system; nothing here shows it again. Popcorn's channel agent is never given it, since its answers reach the whole Routine: the answer says [secret] in its place, and the person reads it on the Connection's card in Popcorn. An e-signature Connection isn't made here: its keys are workspace secrets a workspace admin or owner saves in Popcorn, and the refusal names them. Never pass a key or a password to this tool. It takes routine_id, the Routine's ID, as every tool that writes does. Making a Connection needs workspace admin, or membership of the Routine, and an archived Routine can't be changed.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `connection` [required] | `str` | The Connection's id or label, as list_connections shows it. |
| `account` | `str` | Your account's address or ID, for an email, calendar, files or documents Connection. Omit it to list your accounts. |
| `confirm` | `bool` | true to make it. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true. |
| `only` | `bool` | true to connect the account to this Connection alone, not to the Routine's other unconnected ones it can serve. Default `False`. |

**Example** — “Connect the adjusters' calendar account to #intake so it can book inspections.”

```text
→ make_connection(routine_id="c7d2…5b", connection="Adjuster calendar")

Routine: #intake (c7d2…5b)
- Adjuster calendar (calendar): NOT MADE
  Without it: book inspection can't run; the rest of the Routine keeps working.
It needs: https://www.googleapis.com/auth/calendar.events
Your accounts that can serve it:
- adjusters@acme.example (google), id 9a3e…71: allows everything it needs
- dana.smith@gmail.com (google), id 1c7d…94: its sign-in doesn't allow https://www.googleapis.com/auth/calendar.events; a person reconnects it in Popcorn to add that
To connect one, call make_connection again with account set to its address or id, for a dry run.
To connect an account not listed, a person signs in to it in Popcorn, in the browser: open #intake (https://app.popcorn.ai/ws/acme/conversation/c7d2…5b), then its settings, then Automations, then Connect on the Adjuster calendar card. That can't be done from here. Only your own accounts are listed; a teammate connects theirs.

→ make_connection(routine_id="c7d2…5b", connection="gcal", account="adjusters@acme.example")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

- Connection: Adjuster calendar (calendar)
- Account: adjusters@acme.example (google), yours
- Connects it as gcal
- Lets this Routine use it for: https://www.googleapis.com/auth/calendar.events
- Then runs on_auth_change, the template's own check after a Connection changes

Call again with `confirm=true` to connect adjusters@acme.example (google) as Adjuster calendar.

→ make_connection(routine_id="c7d2…5b", connection="gcal", account="adjusters@acme.example", confirm=true)

Routine: #intake (c7d2…5b)
Connected adjusters@acme.example (google) as Adjuster calendar.
- Bound: gcal
- Started on_auth_change (workflow_id: member-run:on_auth_change)
- Adjuster calendar (calendar): made
  Uses: adjusters@acme.example (google), connected by Dana Smith
  Without it: book inspection can't run; the rest of the Routine keeps working.
```

## References

### `list_references`

[read-only]

The documents a Routine works from (its References), each with what it is used for, when it was added and by whom, and the ones it is still waiting for.

A Reference marked required is one the template counts on; the Routine works without it until someone adds it. read_reference returns one's text, or a download link for a file that isn't text. A Reference add_reference can't take is marked with why. On a workspace that guards personal data, file names aren't listed.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What documents does #intake work from?”

```text
→ list_references(routine="#intake")

Routine: #intake (c7d2…5b)
3 References: 2 added, 1 still waiting.
- Questions and first email  reference "questions"  [required]
  Used for: The questions, validation instructions and email wording for intake.
  Added 2026-10-02 12:05 by Dana Reyes · file Intake questions.txt · text
- Standard retainer agreement  reference "standard_retainer"  [required]
  Used for: The retainer every retained claimant signs.
  Added 2026-10-09 08:53, picked from Google Drive; who picked it isn't recorded · file Retainer 2026.pdf · pdf
  add_reference can't add it: it is picked from Google Drive, in Popcorn.
- Fee schedule  reference "fee_schedule"
  Used for: The fees quoted when a claimant asks what it costs.
  Still waiting: nobody has added it yet.
read_reference(routine="#intake", reference="<name>") returns one's text or a download link.
add_reference adds or replaces a Reference not marked otherwise, as its card in Popcorn does; adding one starts work, which list_triggers shows.
```

### `read_reference`

[read-only]

One of a Routine's References: its text, or a download link for a file that isn't text, such as a PDF.

A long text is cut, and the download link gives the whole file. A link works for a limited time; call again for a fresh one. On a workspace that guards personal data, neither the text nor a link is returned: Popcorn shows the file.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `reference` [required] | `str` | The Reference, as list_references names it. |

**Example** — “Show me the questions #intake sends.”

```text
→ read_reference(routine="#intake", reference="questions")

Routine: #intake (c7d2…5b)
Reference: Questions and first email (questions)
Used for: The questions, validation instructions and email wording for intake.
Added 2026-10-02 12:05 by Dana Reyes · file Intake questions.txt · text
Text:
Subject: Your claim with Acme

Hi {first_name},

Thanks for reaching out. To get your claim started, please reply with:
1. The date of the loss
2. Your policy number
3. Photos of the damage
```

### `create_reference_upload`

[writes]

Get a URL to upload one file for one of a Routine's References, for add_reference to take.

Nothing changes in the Routine until add_reference is confirmed. Upload with the curl line this returns, then call add_reference with the upload_id. The upload goes straight to Popcorn's file storage host, which an assistant whose network access is restricted (such as claude.ai's sandbox) may not reach. In that case, pass a text Reference to add_reference as `text` instead, or add the file in Popcorn. One file per upload, for this Routine and Reference only. The upload must be exactly `size` bytes with this `sha256`, or it is refused; at most 50 MiB (a text file 1.5 MB), and of a kind the Reference takes (the refusal says which). The URL works for 15 minutes. Not for a Reference picked from Google Drive, or one holding the Routine's Steps; list_references marks both. Workspace admins and members of the Routine only.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `reference` [required] | `str` | The Reference, as list_references names it. |
| `filename` [required] | `str` | The file's name with its extension, e.g. fees.pdf; the extension decides what kind of file it is. |
| `size` [required] | `int` | The file's size in bytes. |
| `sha256` [required] | `str` | The file's sha256, as 64 hex characters (`sha256sum FILE`). |

**Example** — “Here's our 2026 fee schedule PDF; give it to #intake.”

```text
→ create_reference_upload(routine_id="c7d2…5b", reference="fee_schedule", filename="Fee schedule 2026.pdf", size=48211, sha256="5d41402abc4b2a76b9719d911017c5925d41402abc4b2a76b9719d911017c592")

Routine: #intake (c7d2…5b)
Upload for Fee schedule (reference "fee_schedule"): 48,211 bytes, sha256 5d41402a….
upload_id: 4e1a9c07….pdf
method: PUT
url: https://acme-uploads.s3.us-west-2.amazonaws.com/4e1a….pdf?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bcontent-type%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=8a3f…
headers:
  Content-Type: application/pdf
  x-amz-checksum-sha256: XUFAKrxL…
The URL works for 15 minutes.

Run this with FILE replaced by the file's path; it prints nothing when the upload succeeds:
curl -fsS -T FILE -H 'Content-Type: application/pdf' -H 'x-amz-checksum-sha256: XUFAKrxL…' 'https://acme-uploads.s3.us-west-2.amazonaws.com/4e1a….pdf?X-Amz-Al…&X-Amz-Expires=900&X-Amz-Si…%3Bcontent-type%3Bhost%3Bx-amz-checksum-sha256&X-Amz-Signature=8a3f…'

Then add it: add_reference(routine_id="c7d2…5b", reference="fee_schedule", upload_id="4e1a9c07….pdf") shows what it changes first.
If curl can't connect to acme-uploads.s3.us-west-2.amazonaws.com, this organization doesn't allow it: add the Reference in Popcorn instead.

→ add_reference(routine_id="c7d2…5b", reference="fee_schedule", upload_id="4e1a9c07b2d35f68/0000000000000001/7c2e91d04f3b4a6e8d5c1b0a9f7e6d51.pdf")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Add: Fee schedule (reference "fee_schedule") on #intake.
- From upload 4e1a9c07….pdf: a PDF (.pdf), 48,211 bytes, file Fee schedule 2026.pdf.
- First add: nobody has added it yet.
- Used for: The fees quoted when a claimant asks what it costs.
- Popcorn reads the file in the background, and the Routine works from it from then on.

Call again with `confirm=true` to add it.
```

### `add_reference`

[writes] [destructive]

Add one of a Routine's References, or replace the one it has, as Replace on the Reference's card in Popcorn does.

Pass exactly one of `text`, the Reference's whole text, or `upload_id`, a file uploaded with create_reference_upload. Only the References the Routine's template expects can be added, and only with a file of a kind each takes. A Reference picked from Google Drive is picked in Popcorn instead, and one holding the Routine's Steps is changed with change_routine; list_references marks both. Without confirm=true this is a dry run that changes nothing: it says whether this is a first add or a replace, what the Routine uses the Reference for, and, for a required one, what starts working once it's in. Once confirmed, Popcorn reads the file in the background and the Routine works from it from then on; list_references shows it once it's in. Each confirmed call with `text` adds it again, so don't repeat one that timed out: check list_references first. Workspace admins and members of the Routine only.

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `reference` [required] | `str` | The Reference, as list_references names it. |
| `text` | `str` | The Reference's whole text, for a Reference that takes a plain text file. At most 1.5 MB. |
| `upload_id` | `str` | The upload_id create_reference_upload gave, once the file is uploaded. |
| `confirm` | `bool` | true to add it. Show the user the dry run first. Default `False`. |
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same request. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

**Example** — “Add a fourth question to #intake's questions: the claim number.”

```text
→ add_reference(routine_id="c7d2…5b", reference="questions", text="Subject: Your claim with Acme\n\nHi {first_name},\n\nThanks for reaching out. To get your claim started, please reply with:\n1. The date of the loss\n2. Your policy number\n3. Photos of the damage\n4. Your claim number, if you already have one\n")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Add: Questions and first email (reference "questions") on #intake.
- From the text given: 236 characters, added as a plain text file (questions.txt).
- Replaces the one in now. Added 2026-10-02 12:05 by Dana Reyes · file Intake questions.txt · text
- Used for: The questions, validation instructions and email wording for intake.
- Required: the template counts on it, and what it is used for starts working once it's in.
- Popcorn reads the file in the background, and the Routine works from it from then on.

Call again with `confirm=true` to replace it.

→ add_reference(routine_id="c7d2…5b", reference="questions", text="Subject: Your claim with Acme\n\nHi {first_name},\n\nThanks for reaching out. To get your claim started, please reply with:\n1. The date of the loss\n2. Your policy number\n3. Photos of the damage\n4. Your claim number, if you already have one\n", confirm=true)

Routine: #intake (c7d2…5b)
Started replacing Questions and first email (reference "questions").
Popcorn reads the file in the background. list_references shows it once it's in, as added just now; if it isn't after a few minutes, the Reference's card in Popcorn says why.
```

## Status

### `get_status`

[read-only]

Where a Routine's items stand: how many are at each Status, and what is waiting for a person, with why.

Each Status shows its label (what Popcorn shows) and its stored value. list_rows shows the items at one Status, filtered on the value: filter={"Status": "<value>"}. list_actions shows what can be done with an item and take_action does it.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “What needs my attention in #intake?”

```text
→ get_status(routine="#intake")

Routine: #intake (c7d2…5b) · table: claims
212 items, by Status (label: count, then the stored value):
- Open: 182  value "open"
- Needs adjuster review: 3  value "review"  [needs a person]
- Paid: 27  value "paid"
None at: Closed.
Waiting for a person (3, newest first, from table issues):
- Needs adjuster review  row 88  opened 2026-10-15
  Why: The roof photos show water damage the estimate leaves out.
- Needs adjuster review  row 91  opened 2026-10-14
  Why: Repair quote is above the $10,000 auto-approve limit.
- Needs adjuster review  row 97  opened 2026-10-09
  Why: Claimant disputes the deductible.
list_rows shows the items; list_actions and take_action act on one.
```

## Actions

### `list_actions`

[read-only]

List the Actions a person can take on one of a Routine's items now, given where it stands: the buttons Popcorn shows on it, each with the Status it moves the item to. take_action takes one.

Some Actions are taken only in Popcorn (a form to fill in, a document to sign, a request to the Routine's agent); they're listed and marked.

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
- Ask for documents  action: ask_docs  [in Popcorn]
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
| `plan_id` | `str` | The plan_id the dry run gave, with confirm=true and the same items and action. Popcorn's channel agent must pass it; an OAuth client is given none and needn't. |

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

## History

### `list_history`

[read-only]

What happened to one item: each change with who or what made it and why, the runs that changed it and how they ended, and its email turns.

Newest first, a page at a time. Each change shows when, who made it (a person by name; Popcorn and the work it was doing, for a run), the Status it moved to and its Why, and the other fields it changed. A run is listed only when it wrote to the item, and one a person's button started shows as Popcorn, for a person. History goes back as far as Popcorn keeps an item's changes; the last page says how far. With run instead of row_id, it follows one run: how it is going or how it ended, and the items it changed (or, if it changed none, what it did).

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `row_id` | `int` | The item's row ID, as list_rows shows it ("row 88" is 88). |
| `cursor` | `str` | next_cursor from the previous page, with the same other arguments. |
| `run` | `str` | A run's reference, as run_trigger gives it, in place of row_id. |

**Example** — “What happened with row 88 in #intake?”

```text
→ list_history(routine="#intake", row_id=88)

Routine: #intake (c7d2…5b) · table: clients
Item: row 88
8 entries, newest first:
- 2026-10-18 10:20 · Popcorn (signing webhook): Retainer signed (entry_id 9)
  Status: Retainer sent → Signed
  1 other field changed: Why: Retainer sent; waiting for the signature. → —
- 2026-10-17 16:10 · Dana Smith: Matter updated (entry_id 7)
  1 field changed: Matter: Car accident → Car accident, rear-ended
- 2026-10-17 15:00 · Popcorn, for a person (cta apply): Send retainer (entry_id 6)
  Status: Needs review → Retainer sent
  Why: Retainer sent; waiting for the signature.
  1 other field changed: Retainer Sent At: 2026-10-17T15:00:00+00:00
- 2026-10-16 11:30 · Popcorn (chase turn): Answered all 5 intake questions (entry_id 4)
  Status: Waiting on answers → Needs review
  Why: Answers are in; check them before the retainer goes out.
  1 other field changed: Answers: {"injured": "yes", "insurer": "Acme Mutual"}
- 2026-10-16 11:29 · Popcorn: Email turn at intake: assess reply
  verdict: complete · reason: all_answered
  Summary: Ben Garrett answered all five questions.
- 2026-10-14 09:05 · Popcorn (chase turn): Sent the questions to Ben (entry_id 2)
  Status: New → Waiting on answers
  Why: Waiting on answers to 5 intake questions.
  1 other field changed: Questions Sent: 5
- 2026-10-14 09:04 · Popcorn: Email turn at intake: send questions
  verdict: approve · reason: first_contact
  Email: subject "Your intake questions, Ben Garrett", sent 2026-10-14 09:05
  Summary: Asked Ben Garrett the 5 intake questions.
- 2026-10-14 09:00 · Popcorn (intake): Created as New (entry_id 1)
read_history_entry with an entry_id shows that change in full, with what the run that made it did.
Runs that changed it on this page:
- signing webhook: succeeded · started 2026-10-18 10:19 by a webhook · ended 2026-10-18 10:20
- cta apply: succeeded · started 2026-10-17 14:59 by a person's button · ended 2026-10-17 15:00
- chase turn: succeeded · started 2026-10-16 11:29 by a message · ended 2026-10-16 11:30
- chase turn: succeeded · started 2026-10-14 09:04 by another run · ended 2026-10-14 09:05
- intake: succeeded · started 2026-10-14 08:59 by a webhook · ended 2026-10-14 09:00
A run a person's button started shows as Popcorn, for a person: runs don't record who pressed it.
Only runs that wrote to this item are listed; a run that only read it isn't.
History goes back 30 days; older changes aren't kept.
```

### `read_history_entry`

[read-only]

One change from an item's History, in full: every field it changed, before and after, who or what made it and why, and, when Popcorn's work made it, what that run did, in order, and how it ended.

Only the fields the change touched are shown, not the whole item. Email content isn't part of History.

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |
| `entry_id` [required] | `int` | The entry's ID, as list_history shows it ("entry_id 6" is 6). |

**Example** — “Show me entry 6 of row 88's history in #intake in full: what changed and what the run did.”

```text
→ read_history_entry(routine="#intake", entry_id=6)

Routine: #intake (c7d2…5b) · table: clients
Item: row 88
- 2026-10-17 15:00 · Popcorn, for a person (cta apply): Send retainer (entry_id 6)
  Status: Needs review → Retainer sent
  Why: Retainer sent; waiting for the signature.
Each field it changed, before → after:
- Status: Needs review → Retainer sent
- Why: Answers are in; check them before the retainer goes out. → Retainer sent; waiting for the signature.
- Retainer Sent At: 2026-10-17T15:00:00+00:00
The run that made it:
- cta apply: succeeded · started 2026-10-17 14:59 by a person's button · ended 2026-10-17 15:00
  What it did, in order:
  - load item: completed · 0.4s
  - send retainer: completed · 0.8s · attempt 2 · the signing provider didn't answer in time
  - apply: completed · 1.2s
A run a person's button started shows as Popcorn, for a person: runs don't record who pressed it.
```

## Docs

### `search_docs`

[read-only]

Search the Popcorn docs (docs.popcorn.ai) and get the best pages' titles, ids and summaries.

Search before building or changing a Routine Template: the docs cover manifest keys, flow activities, table columns and merge policy, schedules, state machines, and copying a template and publishing its versions, which these tools' descriptions don't. Also search when a term or an error names a concept you can't define exactly. read_doc reads a page in full.

| Argument | Type | Notes |
|---|---|---|
| `query` [required] | `str` | What you want to know, in your own words or by name. |
| `limit` | `int` | How many pages to return, 1 to 10. Default `5`. |

**Example** — “If I publish a change to our copy of the intake template, which Routines does it reach?”

```text
→ search_docs(query="publish a version to a copy")

2 docs page(s) for 'publish a version to a copy':

## Versions: publishing and installing (id: versions)
A change reaches a Routine in two steps: publishing mints an immutable version of a Routine Template on its copy, and installing brings each Routine on the copy to it, the one published from at once and the rest on their daily update.

## Copying a template (id: copying-a-template)
Customizing a Routine beyond what its settings reach gives it a copy that the workspace owns (`popcorn app fork`). A copy comes before any publish, and a change published there reaches every Routine on it by their daily update, not only the one you changed. It is one-way: nothing undoes a copy or moves a Routine back to Popcorn's version.

Read one with read_doc(doc_id).
```

### `read_doc`

[read-only]

Read one page of the Popcorn docs by its id (search_docs gives it), or one section of it.

A page too long to return whole (the activity and MCP references) comes back as an outline of its sections; read one with `section`.

| Argument | Type | Notes |
|---|---|---|
| `doc_id` [required] | `str` | The page's id, e.g. "manifest-keys" or "activities". |
| `section` | `str` | A heading on the page, e.g. "foundation.http.request"; the first heading that matches is read, with what's under it. |

**Example** — “Do I have to fork the template before I publish?”

```text
→ read_doc(doc_id="copying-a-template")

# Copying a template (id: copying-a-template)
https://docs.popcorn.ai/build….md

Customizing a Routine beyond what its settings reach gives it a copy that the workspace owns (`popcorn app fork`). A copy comes before any publish, and a change published there reaches every Routine on it by their daily update, not only the one you changed. It is one-way: nothing undoes a copy or moves a Routine back to Popcorn's version.

A Routine made from a Routine Template runs Popcorn's own version of it.
To change what the Routine is built from, the workspace makes a copy of the
template: a series of versions the workspace owns, which it publishes to.

Related: customizing-a-routine, versions.
```

## Proposed tools

**None of these tools exist yet, and nothing depends on them arriving.** They
are a design for the tools a person's assistant uses to run Routines, named
in the [glossary](https://docs.popcorn.ai/glossary/glossary.md)'s
terms rather than the platform's. They are listed so an author can see what is
being considered; names and arguments may change before any ships.

The message, flow, run and stored-value tools have already left this
surface: a Routine's work starts from its Triggers and Actions, a switch is a
Routine Setting, an item's runs are read with `list_history`, and its
conversation is read in Popcorn. Changing a Routine Template itself is not
part of this design.

Three rules run through it:

1. **Ask for the outcome; Popcorn picks the mechanism.** A tool takes what
   the person wants changed, in product terms, and Popcorn decides which
   setting, document or step has to change to get it.
2. **Every write is a dry run until `confirm=true`**, and the dry run says
   whether the change stays with this Routine or gives it a copy of its own,
   which stops receiving its template's improvements.
3. **Reads take `routine`** (its ID or `#name`); **writes take `routine_id`**,
   since a write is the worst place to resolve a name to the wrong Routine.

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
