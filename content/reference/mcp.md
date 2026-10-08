---
id: mcp
title: MCP
order: 3
layout: lookup
platform: 2026-10-08
summary: >
  The tools the hosted Popcorn MCP server exposes — people, projects,
  messages and a project's app — with their arguments, generated from the
  server's own definitions. They list apps and create a project, read an
  app's files, fork it, publish changes to a fork line and install a version,
  and start, follow and stop a project's flows, and read its settings and
  tables.
concepts: [app-bundle, publish-and-apply, fork-line]
applies_to: [cli, mcp, human]
---

The hosted MCP server exposes 37 tools. They cover people, projects,
messages and a project's app: find people and projects, list the apps a
new project can run, create a project (optionally running an app), read
and search a project's messages, send messages and reactions, read the
files of the app a project runs, fork it onto the workspace's own line,
publish changes to a fork line, bring a project on a fork line to its
line's head, or move it onto another line, list a project's flows, run
one, and follow or stop its runs, read and change a project's settings,
and read a project's agent store (its tables, rows and stored values)
and add, change or delete its rows. They work on projects only;
direct messages are out of reach.

A project is what the CLI and the API call a channel, and an app is what
they call an app bundle; the `#name` and the IDs are the same.

Every call runs as the person who connected the server, with that person's
permissions, in the one workspace the connection is bound to; every
response starts with that workspace's name. To use another workspace,
reconnect. Read tools accept a project's `#name` or its ID; tools that
write into a project take `project_id`, the ID only. A listing returns one
page and a `next_cursor` to pass back with the same arguments. A fork, a
publish, an install that moves a project onto another line, creating a
project that runs an app, running a flow, changing a setting and
deleting rows are a dry run until called again with `confirm=true`. An
install that brings a project to its own line's head starts at once, and
so does creating a project with no app.

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

Look up a person by handle: yourself, a member of this workspace, or someone from another workspace you share a project or DM with.

For a member: ID, username, display name, email, workspace role, whether they're active (no once deactivated or removed) and whether they're a bot. For someone from another workspace: display name, username and bot only. To find someone by name, use list_workspace_members. Someone from another workspace is found by user ID only, and so is a deactivated member: usernames and emails are looked up among this workspace's active members, since a username is unique only within one workspace. list_project_members shows the IDs.

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

This workspace's members only: someone from another workspace who is in a shared project isn't listed here, and deactivated members never are. To look up one person by ID, email or @username (a bot included), use get_user.

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

## Projects

### `list_projects`

[read-only]

List the projects you can see in this workspace: the ones you're in (including projects shared in from another workspace) and the ones you can view without joining (marked [not joined]).

Direct messages are not listed. Each row shows the project's name, the app it runs, your unread count and mentions, and its ID. get_project shows one project's version and install state.

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive substring of the project name. |
| `app` | `str` | Only projects running this app, by its slug (e.g. "claimcoordinator"). |
| `include_archived` | `bool` | Also list archived projects (marked [archived]). Default `False`. |
| `sort` | one of `name`, `recent` | "name" (default), or "recent": pinned first, then by last message. |
| `cursor` | `str` | The next_cursor from the previous page, with the same other arguments. |

**Example** — “Which of our projects run the claims coordinator app?”

```text
→ list_projects(app="claimcoordinator")

50 of 137 projects running claimcoordinator:
- #claims-central  claimcoordinator  (id: 2af4…0c)
- #claims-east  claimcoordinator  4 unread, 1 mention  (id: be23…ef)  [pinned]
- #claims-north  claimcoordinator  (id: bd7d…b9)  [not joined]
- … 47 more rows
next_cursor: eyJ2Ijox…
```

### `get_project`

[read-only]

Show one project: its details, your membership, and the app it runs, with the version it's on, the head of its line, and whether the latest install landed. list_project_members lists who's in it.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | The project's ID, or its name ("#intake" or "intake"). Names aren't unique: if more than one project has it, the call lists them with their IDs; pass an ID instead. |

**Example** — “Is #intake on the latest version of its app?”

```text
→ get_project(project="#intake")

ID: c7d2…5b
Name: #intake
Kind: project
Description: New claims, triaged and assigned
Archived: no
Members (incl. bots): 9
Joined: yes
Your role: admin
Unread: 4
Mentions: 1
Muted: no
App: claimcoordinator
Line: product
Version: 0.15.1 (the line's head)
Version ID: 812
Install: installed
```

### `list_project_members`

[read-only]

List the people in a project, with each one's role in it.

Includes people from other workspaces in a shared project (marked [other workspace], shown without email), whom list_workspace_members doesn't list.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | The project's ID, or its name ("#intake" or "intake"). |
| `include_bots` | `bool` | Also list bots (marked [bot]). Default `False`. |
| `cursor` | `str` | The next_cursor from the previous page, with the same other arguments. |

**Example** — “Who's in #partners-acme?”

```text
→ list_project_members(project="#partners-acme")

Project: #partners-acme (dddb…f2)
3 of 3 members:
- Dana Smith  @dsmith  dana@acme.example  admin  (id: 2b7e…a1)
- Jordan Lee  @jlee  jordan@acme.example  member  (id: 5d33…0c)
- Priya Nair  @pnair  member  (id: e019…3b)  [other workspace]
```

### `list_apps`

[read-only]

List the apps a new project in this workspace can run.

Each row shows the app's name, its slug (what create_project's `app` takes), what it does, and the connections someone sets up before it runs. An app this workspace can't run isn't listed.

| Argument | Type | Notes |
|---|---|---|
| `query` | `str` | Case-insensitive substring of the app's name or slug. |
| `cursor` | `str` | The next_cursor from the previous page, with the same query. |

**Example** — “What apps could a new project here run?”

```text
→ list_apps()

5 of 5 apps:
- Alert Tracker  alerttracker  Ingests Alertmanager alerts from a webhook and keeps one row per alert.  needs no connections
- Chat  chat  A project with a calendar. Ask when everyone's free and it checks every connected calendar.  needs Google Calendar
- Claim Coordinator  claimcoordinator  Imports arbitration leads, emails each one its questions, and tracks every answer until the claim is complete.  needs Gmail, Google Calendar, Google Drive
- … 2 more rows
```

### `create_project`

[writes]

Create a project in this workspace, optionally running an app.

Without `app` the project is created at once. With `app` the first call is a dry run that changes nothing: it shows the version that will install and the connections someone sets up before the app runs. Call again with confirm=true to create it. The app installs in the background after the project exists; get_project's Install: field shows when it lands. A name already used in this workspace is refused, with the ID of the project that has it.

| Argument | Type | Notes |
|---|---|---|
| `name` [required] | `str` | The project's name, e.g. "claims-west". Spaces become hyphens; the response shows the name it got. |
| `app` | `str` | An app's slug from list_apps, e.g. "claimcoordinator". |
| `private` | `bool` | true for a private project, joined only by you and `members`. A project that isn't private adds everyone in the workspace. Default `False`. |
| `members` | `list[str]` | People to add to a private project: "@username", email or user ID, all members of this workspace. You're always a member. |
| `confirm` | `bool` | true to create a project that runs an app. Show the user the dry run first. Default `False`. |

**Example** — “Set up a private #claims-west project running the claims app, with Jordan in it.”

```text
→ create_project(name="claims-west", app="claimcoordinator", private=true, members=["@jlee"])

**Dry run.** Nothing was changed.

Create: #claims-west, a private project in Acme, running Claim Coordinator (claimcoordinator).
- Installs: claimcoordinator 0.15.1 (version_id: 812), the head of the product line.
- Members: you, @jlee.
- Connections to set up in the project before the app runs: Gmail, Google Calendar, Google Drive.
- The install runs in the background once the project exists, typically in seconds; get_project's Install: field shows when it lands.

Call again with `confirm=true` to create #claims-west running claimcoordinator.

→ create_project(name="claims-west", app="claimcoordinator", private=true, members=["@jlee"], confirm=true)

Created #claims-west (id: 0141…b3), a private project in Acme.
Members: you, @jlee.
Claim Coordinator (claimcoordinator) is installing in the background. Watch get_project("0141…b3")'s Install: field until it says installed.
Before the app runs, someone sets up in the project: Gmail, Google Calendar, Google Drive.
```

## Messages

### `list_messages`

[read-only]

A project's messages, newest first, or one thread's replies.

Each row is a timestamp (UTC), the message ID, the author, the text (long text is cut and marked; read_message returns it whole), one bracketed line per attachment, tool run or other part, and the reply count with the thread_id that lists the replies. Listing doesn't mark anything read. To read the project's agent's answer to a top-level message you sent, pass that message's ID as `thread_id`: in a project the agent answers in a thread under the message that asked. For a message you sent inside a thread, pass the thread's ID as `thread_id` and your message's ID as `after`. A project set to reply outside threads posts top-level instead, so if the thread stays empty, list the project with `after=<your message's ID>`. Replies arrive asynchronously, so if nothing is there yet, call again shortly.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project ID or "#name". |
| `thread_id` | `str` | List this thread's replies instead. A thread's ID is its first message's ID; a reply's ID finds its thread too. |
| `after` | `str` | Only messages after this ISO timestamp or message ID. |
| `before` | `str` | Only messages before this ISO timestamp or message ID. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What's happened in #intake today?”

```text
→ list_messages(project="#intake", after="2026-09-29T00:00:00Z")

Project: #intake (c7d2…5b)
3 of 3 messages, newest first:
[2026-09-29 16:40] (id: 9400…a5) Intake agent: New claim 4480 from the web form: water damage, Riverside Ave. Assigned to Jordan.
[2026-09-29 14:01] (id: 7e1a…47) Dana Smith: What's still open on claim 4471?
  ↳ 1 reply (thread_id: 7e1a…47)
[2026-09-29 09:00] (id: e769…47) Intake agent: Morning summary: 3 new claims overnight, 2 waiting on a repair estimate.
```

### `read_message`

[read-only]

One message in a project, in full: its whole text, a line per attachment or other part, the reply count and thread_id, and its reactions (marking yours).

| Argument | Type | Notes |
|---|---|---|
| `message_id` [required] | `str` | The message's ID. |
| `include_parts` | `bool` | Also list every part's kind and fields, including tool calls with their arguments and integration payloads: what an agent actually did. Large; leave off unless needed. The parts are paged: a response ends with next_cursor when more follow. Default `False`. |
| `cursor` | `str` | next_cursor from the previous page of parts. A later page holds only the parts, not the message text again. |

**Example** — “Show me Dana's question about claim 4471 in full.”

```text
→ read_message(message_id="7e1a…47")

Project: #intake (c7d2…5b)
Message: 7e1a…47
Author: Dana Smith
Sent: 2026-09-29 14:01 UTC
Replies: ↳ 1 reply (thread_id: 7e1a…47)
Reactions: 👀 1

What's still open on claim 4471?
```

### `send_message`

[writes]

Post a message in a project, as you, visible to its members.

Whether the project's agent answers: an @mention of the agent gets an answer. A plain message goes to a classifier; a tracker or app project's agent answers most messages, other project agents only those that need it. To be surer of an answer, put the agent's handle (the bot in the project's member list) in `mentions`. There is no answer in a project homed in another workspace, and while the agent is already running a task in the project, your message joins that task instead of getting its own reply. Replies arrive asynchronously, in a thread under a top-level message (unless the project is set to reply outside threads). The response gives the new message's ID and the list_messages call that reads the answer.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (get_project returns it). |
| `text` | `str` | Message text (markdown). Optional with an attachment. |
| `thread_id` | `str` | Reply in this thread (its first message's ID). |
| `mentions` | `list[str]` | People to mention and notify: "@username", email, user ID, or "me". Only these are mentioned; "@name" in the text is not parsed. |
| `attachment` | `Attachment` | A text file to attach. |

**Example** — “Ask the agent in #intake what's still open on claim 4471, and tell me what it says.”

```text
→ send_message(project_id="c7d2…5b", text="What's still open on claim 4471?")

Message sent to #intake (id: 7e1a…47).
Replies arrive asynchronously: the project's agent typically answers within seconds to a few minutes. To read them: list_messages(project="c7d2…5b", thread_id="7e1a…47"). A project set to reply outside threads posts its answer top-level instead; if the thread stays empty, check list_messages(project="c7d2…5b", after="7e1a…47").

→ list_messages(project="c7d2…5b", thread_id="7e1a…47")

Project: #intake (c7d2…5b) · thread: 7e1a…47
1 of 1 replies, newest first:
[2026-09-29 14:03] (id: 9a3c…19) Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension. Everything else is closed.
```

### `add_reaction`

[writes] [idempotent]

Add your emoji reaction to a project message.

Adding one that's already there succeeds and changes nothing.

| Argument | Type | Notes |
|---|---|---|
| `message_id` [required] | `str` | The message's ID. |
| `emoji` [required] | `str` | A Unicode emoji, e.g. "👍". |

**Example** — “Give the agent's answer on claim 4471 a thumbs up.”

```text
→ add_reaction(message_id="9a3c…19", emoji="👍")

Reacted 👍 to message 9a3c…19.
```

### `remove_reaction`

[writes] [idempotent]

Remove your emoji reaction from a project message.

Removing one that isn't there succeeds and changes nothing.

| Argument | Type | Notes |
|---|---|---|
| `message_id` [required] | `str` | The message's ID. |
| `emoji` [required] | `str` | The emoji to remove, e.g. "👍". |

**Example** — “Take my 👀 off the 4471 question.”

```text
→ remove_reaction(message_id="7e1a…47", emoji="👀")

Removed your 👀 from message 7e1a…47.
```

### `search_messages`

[read-only]

Search message text across the projects you can see, ranked by relevance (or newest first with sort="recent").

Direct messages are never searched. Each result names its project; read_message returns a result in full, and list_messages(project, after=<id>) shows what followed it. To page through one project in time order, use list_messages.

| Argument | Type | Notes |
|---|---|---|
| `query` [required] | `str` | Words to search for. |
| `project` | `str` | Only this project (ID or "#name"). |
| `author` | `str` | Only messages from this person: "@username", email, user ID, or "me". |
| `after` | `str` | Only messages from this ISO timestamp on (inclusive), or from this message's time on, the message itself left out. |
| `before` | `str` | Only messages up to this ISO timestamp (inclusive), or up to this message's time, the message itself left out. |
| `sort` | one of `relevance`, `recent` | "relevance" (default) or "recent". |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “Find where anyone mentioned Northside Auto this month.”

```text
→ search_messages(query="Northside Auto", after="2026-09-01T00:00:00Z")

2 messages matching "Northside Auto", most relevant first:
[2026-09-29 14:03] (id: 9a3c…19) #intake · Intake agent: Two things are open on claim 4471: the repair estimate from Northside Auto, requested on Sept 24, and Dana's sign-off on the rental extension.
[2026-09-12 10:15] (id: e11b…9d) #claims-east · Dana Smith: Northside Auto says the parts arrive Monday.
```

## Apps

### `list_app_files`

[read-only]

List the files of the app a project runs, with sizes and sha256.

The header names the app, its line and the version listed. By default that's the version edits are based on, and its version_id is the publish base: on a fork line, the line's head; on the product line, the version the project runs, which is what a fork copies. Each row's sha256 is exact: copy it, don't retype it. Read a file's content with read_app_file. To change how a tracker behaves on one project, check list_project_settings first: a fork is one-way, and a publish reaches every project on the line.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `version_id` | `int` | Another version of the project's own line, to read history. Omit for the publish base. |
| `paths` | `list[str]` | Only files matching any of these: an exact path or a glob ("flows/*", "code/**"). |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What files make up the app #intake runs?”

```text
→ list_app_files(project="#intake")

Project: #intake (c7d2…5b)
App: claimcoordinator · line: product · version 0.15.1 (version_id: 812) · head: yes
6 of 6 files:
- AGENT.md  53 B  sha256: f7834927…
- flows/chase_estimate.yaml  21 B  sha256: 42def0cb…
- flows/daily_summary.yaml  20 B  sha256: 802c3a2f…
- … 3 more rows
```

### `read_app_file`

[read-only]

Read one file of the app a project runs, exactly as stored.

The content is never cut. A file too big for one response comes in byte ranges: the header says which bytes this is, and next_cursor reads the next range. Join the ranges in order to get the file, whose sha256 the header gives. Everything after the "Content:" line is the file's text, verbatim.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `path` [required] | `str` | The file's path, as list_app_files shows it. |
| `version_id` | `int` | Another version of the project's own line. Omit for the publish base. |
| `cursor` | `str` | next_cursor from the previous range. |

**Example** — “Show me #intake's app manifest.”

```text
→ read_app_file(project="#intake", path="manifest.yaml")

Project: #intake (c7d2…5b)
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

Fork the app a project runs into a new, named fork line.

The line starts as a byte-identical copy of the product version the project runs, and the project moves onto it. That's one-way: the project never returns to the product line, stops receiving product updates, and from then on gets only what's published to its line. Only a fork line can be published to, with publish_app. To change how a tracker behaves on one project, check list_project_settings first: a setting reaches one project and can be set back. Fork only for what settings can't express. Validate an edit before forking with publish_app's dry run, since the fork is the step that can't be undone. Without confirm=true this is a dry run that changes nothing.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `name` [required] | `str` | The new line's name: lowercase letters, digits, "-" and "_", starting with a letter or digit. Fork only creates a line; to move a project onto a line that exists, use install_app(line=...). |
| `confirm` | `bool` | true to fork. Show the user the dry run first. Default `False`. |

**Example** — “Give #intake its own copy of the claims app, called acme-intake, so we can change its intake form.”

```text
→ fork_app(project_id="c7d2…5b", name="acme-intake")

Project: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Fork: claimcoordinator 0.15.1 (product line, version_id: 812) → new fork line "acme-intake".
- The line starts as a byte-identical copy of 0.15.1. Nothing the project runs changes now.
- #intake moves onto the line. Product updates stop reaching it.
- One-way: a project on a fork line never returns to the product line. From then on it follows "acme-intake", and versions published there reach it within a day.
- Reach: this project only. Other projects running claimcoordinator stay where they are.
- Other fork lines of claimcoordinator in this workspace: "acme-west" (to join one instead: install_app(line=…)).

Call again with `confirm=true` to fork the app into line "acme-intake".
```

### `install_app`

[writes] [destructive]

Install the newest version of a project's line on the project.

It installs the app the project already runs, never another one: a project runs another app only by creating a new project with create_project(app=…). Without line, this is a catch-up (as `popcorn app apply`): a project on a fork line installs its line's head. It runs without confirm, because the daily update would install the same version. Use it after a publish whose install was blocked, or when get_project shows the project behind its line. With line, or when a product-line project would join the workspace's only fork line, it's an adoption: the project moves onto that fork line, one-way, and installs its head. An adoption is a dry run that changes nothing unless confirm=true. It doesn't put an app on a project that has none, and product versions reach product-line projects through the daily update, not through this tool. To change how a tracker behaves on one project, check list_project_settings first; a move between lines is one-way.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `line` | `str` | A fork line of this project's app to move onto. |
| `confirm` | `bool` | true to make an adoption. Show the user the dry run first. Default `False`. |

**Example** — “Move #intake onto our acme-west version of the claims app.”

```text
→ install_app(project_id="c7d2…5b", line="acme-west")

Project: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

Install: #intake moves from claimcoordinator 0.15.1 (product line) onto fork line "acme-west", at its head 0.16.0 (version_id: 913).
- This changes which line the project is on. It installs 0.16.0, which isn't what the project runs now.
- One-way: a project on a fork line never returns to the product line. From then on it follows "acme-west", and versions published there reach it within a day.
- Reach: this project only.

Call again with `confirm=true` to move #intake onto line "acme-west".
```

### `publish_app`

[writes] [destructive]

Publish changes to a project's app as the next version of its line.

A publish reaches every project on the project's fork line: this project installs the new version now, and every other project on the line updates at its daily check. Workspace admins only. To change how a tracker behaves on one project, check list_project_settings first, and publish only what settings can't express. Without confirm=true it's a dry run that changes nothing: the version it would publish, each file's diff, every check it would fail, warnings and the reach. A project on the product line can dry-run changes, but must fork_app before publishing them. Each change is one file. A change to a file that exists carries the sha256 it was read at: copy it exactly from list_app_files or read_app_file. {"path": "manifest.yaml", "expected_sha256": "…", "ops": […]} {"path": "flows/new.yaml", "create": "<whole file>"} {"path": "flows/old.yaml", "delete": true, "expected_sha256": "…"} {"path": "flows/a.yaml", "rename": "flows/b.yaml", "expected_sha256": "…"} Ops apply in order. To rewrite a whole file, delete it and create it again. Bump `version:` in manifest.yaml in every publish. Every op is a text op. The anchor is the file's exact text and must match once: {"op": "replace", "old_string": "cron: 0 9 * * *", "new_string": "cron: 0 8 * * *"}. Also insert_before and insert_after (anchor, text), prepend and append (text), and replace_range (from, to, new_string), which replaces from `from` up to `to`: `to` is not replaced and stays in the file, so never end new_string with it.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). It installs the new version first. |
| `base_version_id` [required] | `int` | The version_id the files were read from, as list_app_files' header shows it: the line's head. |
| `changes` [required] | `list[Change]` | The changes, one per file, applied in order. |
| `changelog` [required] | `str` | What changed and why, in a sentence or two. |
| `confirm` | `bool` | true to publish. Show the user the dry run first. Default `False`. |

**Example** — “On #intake, chase estimates at 8 instead of 9, and publish it.”

```text
→ publish_app(project_id="c7d2…5b", base_version_id=913, changes=[{"path": "manifest.yaml", "expected_sha256": "0454e71d37086e35e6b9e5e41daf6f5a7bf3f27835a897efcfb664edbe7b3d87", "ops": [{"op": "replace", "old_string": "version: 0.16.0", "new_string": "version: 0.16.1"}, {"op": "replace", "old_string": "cron: 0 9 * * 1-5", "new_string": "cron: 0 8 * * 1-5"}, {"op": "replace", "old_string": "# Chase open estimates before the adjusters' stand-up.", "new_string": "# Chase open estimates an hour before stand-up."}]}], changelog="Chase open estimates at 8, an hour before stand-up.")

Project: #intake (c7d2…5b)
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
Reach: #intake would install it now. 2 other projects on this line will update at their daily check.

Call again with `confirm=true` to publish 0.16.1 to line "acme-intake".
```

## Flows

### `list_flows`

[read-only]

List the flows of the app a project runs: the updating it does for itself.

Each row shows the flow's name, what it does, its inputs (a ? marks an optional one) and the schedules that run it. get_flow gives one flow's inputs in full and everything that starts it; run_flow runs one; list_flow_runs shows what ran.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What does #intake do on its own?”

```text
→ list_flows(project="#intake")

Project: #intake (c7d2…5b) · app: claimcoordinator 0.15.1
3 of 3 flows:
- claim_tick  Move every open claim one step along, chasing what's overdue.  schedules: every 180s
- daily_digest  Post the morning summary of new, stuck and closed claims.  inputs: window_hours?  schedules: cron '0 8 * * 1-5' (America/Los_Angeles)
- send_reminder  Email a claimant a reminder of what their claim still needs.  inputs: claim_id, tone?
```

### `get_flow`

[read-only]

One flow of the app a project runs: what it does, the inputs run_flow takes, the integrations it needs, and everything that starts it (schedules, webhooks, messages, documents, row states, other flows).

Each schedule is shown with the inputs it runs with: to run a scheduled flow now, pass those to run_flow. The flow's steps are its file, read with read_app_file(path="flows/<flow>.yaml").

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `flow` [required] | `str` | The flow's name, as list_flows shows it. |

**Example** — “What starts #intake's daily digest, and what does it take?”

```text
→ get_flow(project="#intake", flow="daily_digest")

Project: #intake (c7d2…5b) · app: claimcoordinator 0.15.1
Flow: daily_digest  (file: flows/daily_digest.yaml)
Description: Post the morning summary of new, stuck and closed claims.
Inputs:
- window_hours  integer  optional  default 24 — How far back the summary looks.
Required integrations: gmail
What starts it:
- schedule: schedule 'morning' — cron '0 8 * * 1-5' (America/Los_Angeles), next 2026-10-07T15:00:00Z
  schedule 'morning' runs with inputs: {"window_hours": 24}
```

### `run_flow`

[writes] [destructive]

Run one of a project's flows now, with the given inputs.

A run does what the flow does, for real: it can post messages, send email and change the project's rows. Without confirm=true this is a dry run that starts nothing: it checks the inputs against the flow's declared inputs and its required integrations against the project, and gives a run_key. To run, call again with the same flow and inputs, confirm=true and that run_key. A run starts in the background and returns its workflow_id; get_flow_run follows it. A run_key starts one run. Calling again with it (after a timeout, say) finds the run it started rather than starting another. get_flow shows the inputs a flow takes. To run a scheduled flow now, pass the inputs its schedule runs with.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `flow` [required] | `str` | The flow's name, as list_flows shows it. |
| `inputs` | `dict[str, Any]` | The flow's inputs by name. Omit an optional input to use its default. |
| `confirm` | `bool` | true to start the run. Show the user the dry run first. Default `False`. |
| `run_key` | `str` | The run_key the dry run gave, with confirm=true. |

**Example** — “Send the claimant on C-1042 in #intake a reminder now.”

```text
→ run_flow(project_id="c7d2…5b", flow="send_reminder", inputs={"claim_id": "C-1042"})

Project: #intake (c7d2…5b) · app: claimcoordinator 0.15.1
**Dry run.** Nothing was changed.

Run: send_reminder on #intake, now.
- Inputs: {"claim_id": "C-1042"}
- Defaults that apply: {"tone": "friendly"}
- It runs as the workspace's agent, for you, in the background, and does what the flow does: posts, emails and row changes are real.
- run_key: Qm7xT2vL…

Call again with `confirm=true` to run send_reminder, with run_key="Qm7xT2vL…" and the same inputs.

→ run_flow(project_id="c7d2…5b", flow="send_reminder", inputs={"claim_id": "C-1042"}, confirm=true, run_key="Qm7xT2vLp9aRk4Ne3d121b61c6573b4a")

Project: #intake (c7d2…5b) · app: claimcoordinator 0.15.1
Started send_reminder. workflow_id: 8c1f3a52…
It runs in the background: get_flow_run with this workflow_id shows its steps and how it ended.
```

### `list_flow_runs`

[read-only]

List a project's flow runs, newest first: which flow, how each ended (succeeded, failed, still_running), when, and what started it. get_flow_run shows one run's steps, inputs and failure.

Each row ends with the run's workflow_id, the ID get_flow_run and cancel_flow_run take.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `flow` | `str` | Only this flow's runs, by its name. |
| `status` | `str` | "all", "running", "failed" or "closed". Default `all`. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “Has #intake's daily digest failed lately?”

```text
→ list_flow_runs(project="#intake", flow="daily_digest", status="failed")

Project: #intake (c7d2…5b)
2 runs of "daily_digest", failed, newest first:
- daily_digest  failed  started 2026-10-05T15:00:00Z  ended 2026-10-05T15:00:41Z  (workflow_id: channel:c7d2…5b:flow:daily_digest:morning-2026-10-05T15:00:00Z)
- daily_digest  failed  started 2026-10-02T15:00:00Z  ended 2026-10-02T15:00:38Z  started by a person  (workflow_id: acme-int…)
```

### `get_flow_run`

[read-only]

One flow run: how it ended (or what it's doing now), its inputs, its outputs, the error it failed with, and its newest steps.

A run still going shows the step it's on; call again to follow it.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `workflow_id` | `str` | Required. The run's workflow ID, as run_flow returns it and list_flow_runs shows it. Not the Temporal run ID (a UUID). |
| `run_id` | `str` | Optional. The Temporal run ID (a UUID) of one execution of the workflow, to read that execution rather than the newest. Sent without workflow_id it is read as the workflow ID, a deprecated alias. |

**Example** — “Why did this morning's digest in #intake fail?”

```text
→ get_flow_run(project="#intake", workflow_id="channel:c7d2…5b:flow:daily_digest:morning-2026-10-05T15:00:00Z")

Project: #intake (c7d2…5b)
Run: workflow_id channel:c7d2…5b:flow:daily_digest:morning-2026-10-05T15:00:00Z  flow: daily_digest  failed  started 2026-10-05T15:00:00Z  ended 2026-10-05T15:00:41Z
Temporal run_id 0199…13: this execution of the workflow. The flow-run tools take the workflow_id; pass run_id beside it only to pin this execution.
Inputs: {"window_hours": 24}
Failed with: IntegrationAuthError: gmail: the connected account's token was revoked
Steps, newest first:
- email_digest  integrations.gmail.send  failed  2.1s  attempt 3  gmail: the connected account's token was revoked
- post_summary  foundation.channel.post  completed  0.6s
- collect  foundation.table.query  completed  0.3s
```

### `cancel_flow_run`

[writes] [destructive] [idempotent]

Stop one flow run that's still going.

The run stops at its next step, so a step already under way finishes, and what earlier steps did (messages posted, rows changed) stays done. A run that already ended is left as it was. One run per call.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `workflow_id` | `str` | Required. The run's workflow ID, as run_flow returns it and list_flow_runs shows it. Not the Temporal run ID (a UUID). |
| `run_id` | `str` | Optional. The Temporal run ID (a UUID) of one execution of the workflow, to stop only that execution rather than the newest. Sent without workflow_id it is read as the workflow ID, a deprecated alias. |

**Example** — “Stop the claim tick that's running in #intake.”

```text
→ cancel_flow_run(project_id="c7d2…5b", workflow_id="acme-intake-claim_tick-2026-10-06T091200Z-c3d4")

Project: #intake (c7d2…5b)
Stopping run workflow_id acme-int… (Temporal run_id 0199…75): it stops at its next step. get_flow_run with the workflow_id shows when it has.
```

## Project settings

### `list_project_settings`

[read-only]

List the settings of the app a project runs, set or not.

A setting changes how the tracker behaves on this project alone: sending modes, schedules, limits, and the prompts and email templates its agents use. A changed setting reaches one project, can be set back, and is kept through app updates, so check here before forking the app. Each prompt or template file is its own setting, so changing one leaves the others following app updates. Each row shows the value; an unset one says what unset means, and one changed from the app's default says so. Secrets show only whether they're set. get_project_setting shows one in full; update_project_setting changes one.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `query` | `str` | Only settings whose key or label contains this. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What can I change about how #chase-renewals chases people, without forking its app?”

```text
→ list_project_settings(project="#chase-renewals", query="chase")

Project: #chase-renewals (4b0e…12) · app: chase 0.3.1
4 of 4 settings matching "chase":
- chase_days  [1, 3, 7]
- chase_max_followups  5  (changed; app default 10)
- chase_window_timezone  America/Los_Angeles
- prompts.chase_email  Hi {{ name }}, just following up on the documents we asked for last week. If you've already sent them, thank you, and pl… [truncated; get_project_setting(key="prompts.chase_email") for the full text]
2 values set on this project are read by nothing and not shown.
```

### `get_project_setting`

[read-only]

One of a project's settings in full: the whole value (a prompt or template's whole text), the app's default, what it accepts, its description, its options with the warning each one carries, and who may change it.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `key` [required] | `str` | The setting's key, as list_project_settings shows it. |

**Example** — “Show me the email #chase-renewals sends when it chases someone.”

```text
→ get_project_setting(project="#chase-renewals", key="prompts.chase_email")

Project: #chase-renewals (4b0e…12) · app: chase 0.3.1
Setting: prompts.chase_email
Value:
Hi {{ name }}, just following up on the documents we asked for last week. If you've already sent them, thank you, and please ignore this note.

The {{ firm }} team

App default: the same as the value
Accepts: text, the shape of the app's default
Changed by: update_project_setting, by a workspace admin who's also a member of the project.
```

### `update_project_setting`

[writes] [destructive]

Change one of a project's settings, on this project only.

Without confirm=true this is a dry run that changes nothing: it shows the old and new value, what the setting does, and the warning the new option carries. Setting the app's default value resets the setting. A switch takes one of its options; any other setting keeps the shape of the app's default (a list stays a list, a number a number). Secrets and the recipe aren't changed here. For a long text (a prompt, an email template, agent guidance), pass changes instead of value: text ops applied in order to the current text, as publish_app's ops are. The anchor is the text exactly and must match once: {"op": "replace", "old_string": "Hi {{name}},", "new_string": "Hello {{name}},"}. Also insert_before and insert_after (anchor, text), prepend and append (text), and replace_range (from, to, new_string). A value with credentials inside it shows them as [secret]. Keep [secret] exactly where a read shows it; the stored credential stays in place. Credentials, and what surrounds them, change in the app.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `key` [required] | `str` | The setting's key, as list_project_settings shows it. |
| `value` | `Any` | The whole new value: text, a number, a list, a mapping, or null. Omit it to pass changes instead. Default `OMITTED`. |
| `changes` | `list[Op]` | Text ops on the current text, instead of value. |
| `confirm` | `bool` | true to change it. Show the user the dry run first. Default `False`. |

**Example** — “Stop chasing after five follow-ups on #chase-renewals.”

```text
→ update_project_setting(project_id="4b0e…12", key="chase_max_followups", value=5)

Project: #chase-renewals (4b0e…12) · app: chase 0.3.1
**Dry run.** Nothing was changed.

Change: chase_max_followups on #chase-renewals.
- 10 → 5
- Reach: this project only. It can be set back with update_project_setting. App updates won't change the new value.

Call again with `confirm=true` to change chase_max_followups.

→ update_project_setting(project_id="4b0e…12", key="chase_max_followups", value=5, confirm=true)

Project: #chase-renewals (4b0e…12) · app: chase 0.3.1
Changed chase_max_followups on #chase-renewals: 10 → 5.
Runs already under way keep the value they started with.
```

## Agent store

### `list_tables`

[read-only]

List the tables in a project's agent store, with each one's row count.

The agent store is the project's storage: tables of rows the app, agents and people keep. get_table shows a table's columns; list_rows reads its rows.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `cursor` | `str` | next_cursor from the previous page. |

**Example** — “What does #intake keep track of?”

```text
→ list_tables(project="#intake")

Project: #intake (c7d2…5b)
2 of 2 tables:
- claims  212 rows
- Contacts  3 rows
```

### `get_table`

[read-only]

A table's columns, in order: each one's name, type, label and merge policy, the table's merge key, and its state machine if the project's app runs one on it.

A merge policy says what a write that merges into an existing row does to that column: replace (the default), keep the first value, concat (append), or increment_on_change (a counter the store keeps). Columns marked as state change only when one of the app's transitions fires, so create_rows and update_row refuse them.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |

**Example** — “What columns does #intake's claims table have?”

```text
→ get_table(project="#intake", table="claims")

Project: #intake (c7d2…5b) · table: claims
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
- Status column: Status · CTAs: CTAs · sub: Stage
- funnel (column Stage): open, closed
```

### `list_rows`

[read-only]

List a table's rows, newest first unless sort says otherwise.

Each row shows its ID, a few columns (long values are cut and marked; get_row shows a row in full) and when it last changed.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `query` | `str` | Text to find in any column, case-insensitively: "4471" finds the row whatever column holds it. Only rows where it appears in a value you can see are listed, so with query (or filter["*"]) a page can come back short, there's no total, and next_cursor goes on to the rest. |
| `filter` | `dict[str, Any]` | Conditions on columns, all of which must hold: {"Status": "open"} or {"Status": {"$eq": "open"}}, {"amount": {"$gt": 1000}}, {"claimant": {"$contains": "ortiz"}}, {"Status": {"$in": ["open", "waiting"]}}, {"closed_at": {"$exists": false}}. Operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $exists, $contains. There's no $or. Text compares case-insensitively. |
| `columns` | `list[str]` | The columns to show, by name. By default, the first few in the table's order (get_table lists them). |
| `sort` | `str` | "column:asc" or "column:desc". By default, newest first. On a workspace that guards personal data, a column whose values are hidden can't be sorted on. |
| `cursor` | `str` | next_cursor from the previous page, with the same other arguments. When the rows end exactly at a page's end, the last page comes back empty. |

**Example** — “Find claim 4471 in #intake.”

```text
→ list_rows(project="#intake", table="claims", query="4471")

Project: #intake (c7d2…5b) · table: claims
Columns shown: claim_no, claimant, amount, Status, Stage (of 11; columns=[…] picks others). Empty values are left out.
2 rows matching "4471", newest first, shown on this page:
- row 91  claim_no: 44710  claimant: Lee  amount: 900  (updated 2026-09-29 14:05)
- row 88  claim_no: 4471  claimant: Ortiz  amount: 12400  Status: open  Stage: open  (updated 2026-09-29 14:05)
```

### `get_row`

[read-only]

One row in full: every column, its rev (update_row needs it as expected_rev), when it was created and last changed, and its state if the app's state machine runs on the table.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_id` [required] | `int` | The row's ID, as list_rows shows it ("row 88" is 88). |

**Example** — “Show me everything on row 88 of #intake's claims.”

```text
→ get_row(project="#intake", table="claims", row_id=88)

Project: #intake (c7d2…5b) · table: claims
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

### `list_scalars`

[read-only]

List the single values a project's agent store keeps (scalars), by key: the app's runtime state, values people or agents keep, and the values behind its settings.

This is the raw storage; long values are cut and marked, and get_scalar shows one whole. Credentials are never shown. Stored values that are settings read better through list_project_settings, which says what each one does and what changing it would do. These values are read-only here.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `query` | `str` | Text to find in the key, case-insensitively. |
| `cursor` | `str` | next_cursor from the previous page, with the same query. |

**Example** — “What values does #intake keep?”

```text
→ list_scalars(project="#intake")

Project: #intake (c7d2…5b)
4 of 4 stored values:
- copy:claims.settings.fields  = [{"key": "popcorn.portal_pin", "label": "Portal PIN", "input": "secret"}]  (updated 2026-09-01 10:00)
- popcorn.crm_api_key  = [hidden: holds a credential]  (updated 2026-09-01 10:00)
- popcorn.portal_pin  = [hidden: holds a credential]  (updated 2026-09-01 10:00)
- project status  = On track  (updated 2026-09-02 10:00)
Stored values that are settings read better through list_project_settings, which says what each one does.
```

### `get_scalar`

[read-only]

One value a project's agent store keeps (a scalar), whole, as stored.

A credential is never shown. If the key is a setting, get_project_setting reads it better: it says what the setting does and what its options are. Stored values are read-only here.

| Argument | Type | Notes |
|---|---|---|
| `project` [required] | `str` | Project name ("#intake") or ID. |
| `key` [required] | `str` | The value's key, as list_scalars shows it. |

**Example** — “What's the project status note on #intake?”

```text
→ get_scalar(project="#intake", key="project status")

Project: #intake (c7d2…5b)
Key: project status
Updated: 2026-09-02 10:00
Value:
On track
Stored values that are settings read better through list_project_settings, which says what each one does.
```

### `create_rows`

[writes]

Add rows to one of a project's tables.

A row whose merge key matches an existing row merges into it instead of adding another: the table's own merge key if it has one (get_table shows it), else the columns merge_on names. A merge on merge_on changes only the columns the row carries, each by the column's merge policy. A merge on the table's own key follows that key's setting: merge works the same way, but replace overwrites the matched row whole, emptying every column the new row leaves out (refused where that would erase the app's state or a credential). The response says which rows were added and which merged. Adding rows starts no flow. Columns the app's state machine owns are refused (they change only by a transition), and so are credential columns. Each call adds its rows: if a call timed out, check with list_rows before sending it again.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `rows` [required] | `list[dict[str, Any]]` | The rows, each an object of column: value. At most 50. |
| `merge_on` | `list[str]` | Columns that identify an existing row to merge into, for a table with no merge key of its own. |

**Example** — “Add claim 5002 for Kim, $900, to #intake, and update 4471's amount to 13,000 while you're at it.”

```text
→ create_rows(project_id="c7d2…5b", table="claims", rows=[{"claim_no": "5002", "claimant": "Kim", "amount": 900}, {"claim_no": "4471", "amount": 13000}], merge_on=["claim_no"])

Project: #intake (c7d2…5b) · table: claims
Added 1 row and merged 1 into existing rows:
- row 301  added
- row 88  merged into the existing row
get_row shows one in full.
```

### `update_row`

[writes] [idempotent]

Change some columns of one row.

Only the columns in data change; the rest stay as they are. Each changes by its merge policy, and the response names any column where that policy, not the value sent, decided what's stored. expected_rev is the rev get_row shows. If the row has changed since (its rev moved on), nothing is written and the response shows the row as it is now, with its new rev, so you can decide again. Changing a row starts no flow. Columns the app's state machine owns are refused (they change only by a transition), and so are credential columns.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_id` [required] | `int` | The row's ID ("row 88" is 88). |
| `data` [required] | `dict[str, Any]` | The columns to change, as column: value. |
| `expected_rev` [required] | `int` | The row's rev, from get_row. |

**Example** — “Add a note to claim 4471 in #intake that the adjuster called back.”

```text
→ update_row(project_id="c7d2…5b", table="claims", row_id=88, data={"Notes": "Adjuster called back 10/6."}, expected_rev=4)

Project: #intake (c7d2…5b) · table: claims
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

Delete rows from one of a project's tables, by ID.

Without confirm=true this is a dry run that deletes nothing: it lists the rows it would delete. Show the person the dry run, and confirm only once they agree. A deleted row can't be restored with these tools. Rows are deleted one at a time, and the response says which were deleted, which were already gone and which failed.

| Argument | Type | Notes |
|---|---|---|
| `project_id` [required] | `str` | The project's ID (not its name). |
| `table` [required] | `str` | The table's name, as list_tables shows it. |
| `row_ids` [required] | `list[int]` | The rows' IDs ("row 88" is 88). At most 50. |
| `confirm` | `bool` | true to delete. Show the user the dry run first. Default `False`. |

**Example** — “Delete the duplicate row 91 from #intake's claims.”

```text
→ delete_rows(project_id="c7d2…5b", table="claims", row_ids=[91])

Project: #intake (c7d2…5b) · table: claims
**Dry run.** Nothing was changed.

Delete 1 row from claims:
- row 91  claim_no: 44710  claimant: Lee  amount: 900  (updated 2026-09-29 14:05)
- Warning: the app's state machine runs on this table; a deleted row leaves the app's tracker and its open items.
- A deleted row can't be restored with these tools. Deleting starts no flow.

Call again with `confirm=true` to delete this row.

→ delete_rows(project_id="c7d2…5b", table="claims", row_ids=[91], confirm=true)

Project: #intake (c7d2…5b) · table: claims
Deleted 1 of 1 rows: row 91.
```

