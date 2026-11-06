---
id: mcp/tools
title: Tools
order: 301
group: MCP
layout: lookup
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Every tool the hosted server offers, A to Z, each with whether it reads or
  writes and what it does, linking its own page.
lede: >
  Every tool on the server, A to Z, each linking its own page.
concepts: [mcp]
---

Every tool the hosted server offers, A to Z. Each tool's page has its call,
its arguments and, for many, a worked example. Every call runs as you, in
the one Workspace your assistant is connected to; the [MCP server
overview](https://docs.popcorn.ai/mcp.md) says how to choose it.

A [read-only] tool takes a Routine as `routine`, by its `#name` or its ID. A
tool that [writes] takes the ID only, as `routine_id`.

A tool marked [dry run] previews, then acts when called again with
`confirm=true`:

```text
→ delete_rows(…, row_ids=[91])                dry run: lists the rows
→ delete_rows(…, row_ids=[91], confirm=true)  deletes them
```

For some, your assistant confirms straight away when you asked for that
change yourself, such as an Action on Items you named; others, such as
deleting rows, always preview first. Each tool's page says which.

A listing returns one page and a `next_cursor`: pass it back with the same
arguments for the next page.

The other badges are the hints the server declares to your assistant's app,
which may use them to decide what to ask before a call: [read-only], or
[writes] with [destructive] or [idempotent]. On a tool's page, an argument
marked [required] must be passed, and any other may be left out.

A worked example is a request a person might make, each call an assistant
makes for it, marked `→`, and what the tool returns. The response is the
server's real output for sample data, the Workspace Acme, produced by its
tests. It leaves out the Workspace line, shortens IDs as `8c1f…e2`, and
keeps the first rows of a long listing.

The list below and each tool's page are generated from the server's own
definitions after each prod deploy, and never edited by hand.

<!-- generated: tools -->
## A

- **[`add_reference`](https://docs.popcorn.ai/mcp/tools/add-reference.md)** — [writes] [destructive] [dry run] Add one of a Routine's References, or replace the one it has, as Replace on the Reference's card in Popcorn does.

## C

- **[`change_routine`](https://docs.popcorn.ai/mcp/tools/change-routine.md)** — [writes] [destructive] [dry run] Change a Routine's Steps by describing the change in words, previewed before anything is installed, or put back an earlier version of its Steps.
- **[`complete_setup_step`](https://docs.popcorn.ai/mcp/tools/complete-setup-step.md)** — [writes] [destructive] [dry run] Complete one step of a Routine's setup that asks for a value, as its card on the Today tab in Popcorn does: a setting its work needs (a reply-by date, a waiting period) or a booking page's link. get_setup lists the steps and what each asks for.
- **[`copy_routine_template`](https://docs.popcorn.ai/mcp/tools/copy-routine-template.md)** — [writes] [destructive] [dry run] Give a Routine its own named copy of the Routine Template it runs.
- **[`create_reference_upload`](https://docs.popcorn.ai/mcp/tools/create-reference-upload.md)** — [writes] Get a URL to upload one file for one of a Routine's References, for add_reference to take.
- **[`create_routine`](https://docs.popcorn.ai/mcp/tools/create-routine.md)** — [writes] Create a Routine in this workspace, optionally from a Routine Template.
- **[`create_routine_file_upload`](https://docs.popcorn.ai/mcp/tools/create-routine-file-upload.md)** — [writes] Get a URL to upload one file you made, for create_routine_version to take.
- **[`create_routine_version`](https://docs.popcorn.ai/mcp/tools/create-routine-version.md)** — [writes] [destructive] [dry run] Save changes as the next version of the Routine's own copy of its Routine Template.
- **[`create_rows`](https://docs.popcorn.ai/mcp/tools/create-rows.md)** — [writes] [dry run] Add rows to one of a Routine's tables.

## D

- **[`delete_rows`](https://docs.popcorn.ai/mcp/tools/delete-rows.md)** — [writes] [destructive] [idempotent] [dry run] Delete rows from one of a Routine's tables, by ID.
- **[`duplicate_routine`](https://docs.popcorn.ai/mcp/tools/duplicate-routine.md)** — [writes] [dry run] Create a new Routine in this workspace that copies an existing one's setup: its Routine Template, on the same line, its Routine Settings and agent notes, its own Steps, its guidelines, and the References it has added.

## G

- **[`get_instructions`](https://docs.popcorn.ai/mcp/tools/get-instructions.md)** — [read-only] A Routine's Instructions in one read: the guidance its agents work from, Routine-wide and for each Step, each with where it came from (the template's, or changed for this Routine) and what changes it.
- **[`get_memory`](https://docs.popcorn.ai/mcp/tools/get-memory.md)** — [read-only] One memory whole: its text, its category and name, when it was saved and last changed, and its metadata.
- **[`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md)** — [read-only] Show one Routine: its details, your membership, and its Routine Template, with the version it's on, the latest version, where its updates come from (Popcorn, or this workspace's own copy of the template), whether the latest install landed, and its Connections: each account or webhook the template needs, and whether it's connected.
- **[`get_routine_change`](https://docs.popcorn.ai/mcp/tools/get-routine-change.md)** — [read-only] Where a change to a Routine's Steps stands: still drafting, the proposal as Steps before and after, refused and why, or installed.
- **[`get_routine_setting`](https://docs.popcorn.ai/mcp/tools/get-routine-setting.md)** — [read-only] One of a Routine's settings in full: the whole value (a prompt or email template's whole text), the template default, what it accepts, its description, its options with the warning each one carries, and who may change it.
- **[`get_row`](https://docs.popcorn.ai/mcp/tools/get-row.md)** — [read-only] One row in full: every column, its rev (update_row needs it as expected_rev), when it was created and last changed, and its state if the Routine's state machine runs on the table.
- **[`get_run`](https://docs.popcorn.ai/mcp/tools/get-run.md)** — [read-only] One of a Routine's runs, by its reference: how it is going or how it ended, what started it, its inputs and outputs, the error it failed with, and its newest steps.
- **[`get_setup`](https://docs.popcorn.ai/mcp/tools/get-setup.md)** — [read-only] Show a Routine's setup checklist, the steps on its Today tab in Popcorn, in order: each done or not, which are required, and what each one left still needs (a Connection, a document, a booking page, a value).
- **[`get_status`](https://docs.popcorn.ai/mcp/tools/get-status.md)** — [read-only] Where a Routine's items stand: how many are at each Status, and what is waiting for a person, with why and the Actions that settle it (take_action takes one on the item's row).
- **[`get_table`](https://docs.popcorn.ai/mcp/tools/get-table.md)** — [read-only] A table's columns, in order: each one's name, type, label and merge policy, the table's merge key, and its state machine if the Routine runs one on it.
- **[`get_user`](https://docs.popcorn.ai/mcp/tools/get-user.md)** — [read-only] Look up a person by handle: yourself, a member of this workspace, or someone from another workspace you share a Routine or DM with.
- **[`get_workspace`](https://docs.popcorn.ai/mcp/tools/get-workspace.md)** — [read-only] The Popcorn workspace this connection is bound to.

## I

- **[`install_routine`](https://docs.popcorn.ai/mcp/tools/install-routine.md)** — [writes] [destructive] [dry run] Install the newest version of a Routine's copy of its template, or move it onto a copy the workspace already has.

## L

- **[`list_actions`](https://docs.popcorn.ai/mcp/tools/list-actions.md)** — [read-only] List the Actions a person can take on one of a Routine's items now, given where it stands: the buttons Popcorn shows on it, each with the Status it moves the item to. take_action takes one.
- **[`list_connections`](https://docs.popcorn.ai/mcp/tools/list-connections.md)** — [read-only] List the Connections a Routine needs: the accounts and other services its template works through.
- **[`list_history`](https://docs.popcorn.ai/mcp/tools/list-history.md)** — [read-only] What happened to one item: each change with who or what made it and why, the runs that changed it and how they ended, and its email turns.
- **[`list_memories`](https://docs.popcorn.ai/mcp/tools/list-memories.md)** — [read-only] List memories, newest first: what people told a Routine's agent (preferences, decisions, feedback) and what its template keeps there (categories named "<feature>:<name>", such as autochat:day).
- **[`list_messages`](https://docs.popcorn.ai/mcp/tools/list-messages.md)** — [read-only] A Routine's messages, newest first, or one thread's replies.
- **[`list_references`](https://docs.popcorn.ai/mcp/tools/list-references.md)** — [read-only] The documents a Routine works from (its References), each with what it is used for, when it was added and by whom, and the ones it is still waiting for.
- **[`list_routine_files`](https://docs.popcorn.ai/mcp/tools/list-routine-files.md)** — [read-only] List the files of the Routine Template version a Routine runs, with sizes and sha256.
- **[`list_routine_settings`](https://docs.popcorn.ai/mcp/tools/list-routine-settings.md)** — [read-only] List the settings of a Routine's Routine Template, set or not.
- **[`list_routine_templates`](https://docs.popcorn.ai/mcp/tools/list-routine-templates.md)** — [read-only] List the Routine Templates a new Routine in this workspace can start from.
- **[`list_routines`](https://docs.popcorn.ai/mcp/tools/list-routines.md)** — [read-only] List the Routines you can see in this workspace: the ones you're in (including Routines shared in from another workspace) and the ones you can view without joining (marked [not joined]).
- **[`list_rows`](https://docs.popcorn.ai/mcp/tools/list-rows.md)** — [read-only] List a table's rows, newest first unless sort says otherwise.
- **[`list_runs`](https://docs.popcorn.ai/mcp/tools/list-runs.md)** — [read-only] The Routine's runs, newest first: the work each did or is doing, how it ended, when, what started it, and its reference.
- **[`list_tables`](https://docs.popcorn.ai/mcp/tools/list-tables.md)** — [read-only] List the tables in a Routine, with each one's row count.
- **[`list_triggers`](https://docs.popcorn.ai/mcp/tools/list-triggers.md)** — [read-only] List how work arrives in a Routine: each schedule with its cadence, each webhook another system posts to, each message or document that starts work.
- **[`list_workspace_members`](https://docs.popcorn.ai/mcp/tools/list-workspace-members.md)** — [read-only] List the members of this workspace, alphabetically by name.

## M

- **[`make_connection`](https://docs.popcorn.ai/mcp/tools/make-connection.md)** — [writes] [destructive] [dry run] Make one of a Routine's Connections: connect an account you have signed in to, or make the webhook another system posts to.

## R

- **[`react`](https://docs.popcorn.ai/mcp/tools/react.md)** — [writes] [idempotent] Add an emoji reaction to a Routine message, or take yours off with remove=true.
- **[`read_doc`](https://docs.popcorn.ai/mcp/tools/read-doc.md)** — [read-only] Read one page of the Popcorn docs by its id (search_docs gives it), or one section of it.
- **[`read_history_entry`](https://docs.popcorn.ai/mcp/tools/read-history-entry.md)** — [read-only] One change from an item's History, in full: every field it changed, before and after, who or what made it and why, and, when Popcorn's work made it, what that run did, in order, and how it ended.
- **[`read_message`](https://docs.popcorn.ai/mcp/tools/read-message.md)** — [read-only] One message in a Routine, in full: its whole text, a line per attachment or other part, the reply count and thread_id, and its reactions (marking yours).
- **[`read_reference`](https://docs.popcorn.ai/mcp/tools/read-reference.md)** — [read-only] One of a Routine's References: its text, or a download link for a file that isn't text, such as a PDF.
- **[`read_routine_file`](https://docs.popcorn.ai/mcp/tools/read-routine-file.md)** — [read-only] Read one file of the Routine Template version a Routine runs, exactly as stored.
- **[`run_trigger`](https://docs.popcorn.ai/mcp/tools/run-trigger.md)** — [writes] [destructive] [dry run] Run one of a Routine's schedules now, with the inputs it runs with on schedule.

## S

- **[`search_docs`](https://docs.popcorn.ai/mcp/tools/search-docs.md)** — [read-only] Search the Popcorn docs (docs.popcorn.ai) and get the best pages' titles, ids and summaries.
- **[`search_messages`](https://docs.popcorn.ai/mcp/tools/search-messages.md)** — [read-only] Search message text across the Routines you can see, ranked by relevance (or newest first with sort="recent").
- **[`send_message`](https://docs.popcorn.ai/mcp/tools/send-message.md)** — [writes] Post a message in a Routine, visible to its members.
- **[`stop_run`](https://docs.popcorn.ai/mcp/tools/stop-run.md)** — [writes] [destructive] [idempotent] Stop one of a Routine's runs that's still going.

## T

- **[`take_action`](https://docs.popcorn.ai/mcp/tools/take-action.md)** — [writes] [destructive] [dry run] Take one Action on one or more of a Routine's items, as a person pressing its button in Popcorn would.

## U

- **[`update_routine_setting`](https://docs.popcorn.ai/mcp/tools/update-routine-setting.md)** — [writes] [destructive] [dry run] Change one of a Routine's settings, on this Routine only.
- **[`update_row`](https://docs.popcorn.ai/mcp/tools/update-row.md)** — [writes] [idempotent] Change some columns of one row.
<!-- /generated -->
