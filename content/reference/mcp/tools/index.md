---
id: mcp/tools
title: Tools
order: 301
group: MCP
layout: lookup
generated: scripts/sync-mcp.py
updated: 2026-11-09
summary: >
  Every tool the hosted server offers and what it does, with what its badges
  mean and which tools preview a change before making it.
lede: >
  Every tool on the server, and how your assistant calls them.
concepts: [mcp]
---

Each tool's page, generated from the server's own definitions, has its call
and arguments. Many also have a worked example.

A tool's badges say how it behaves. The first four are hints the server
declares to your assistant, helping it decide what to ask before a call:

| Badge | Means |
|---|---|
| [read-only] | Safe to call any time. Takes a Routine's `#name` or ID, as `routine` |
| [writes] | May ask you first. Takes a Routine's ID only, as `routine_id` |
| [destructive] | Can remove or overwrite what's there |
| [idempotent] | Calling it again with the same arguments changes nothing more |
| [dry run] | Previews first, and acts when called again with `confirm=true` |
| [required] | Marks an argument that must be passed |

> [!NOTE] Straight to it
> Some [dry run] tools act straight away when you've asked for the change
> yourself, such as an Action on Items you named. Others, such as
> [deleting rows](https://docs.popcorn.ai/mcp/tools/delete-rows.md), always
> preview first. Each tool's page says which.

<!-- generated: tools -->
## A

- **[`add_reference`](https://docs.popcorn.ai/mcp/tools/add-reference.md)** — [writes] [destructive] [dry run] Add one of a Routine's References, or replace the one it has, as Replace on the Reference's card in Popcorn does.

## C

- **[`change_routine`](https://docs.popcorn.ai/mcp/tools/change-routine.md)** — [writes] [destructive] [dry run] Change a Routine's Steps by describing the change in words, previewed before anything is installed, or put back an earlier version of its Steps.
- **[`complete_setup_step`](https://docs.popcorn.ai/mcp/tools/complete-setup-step.md)** — [writes] [destructive] [dry run] Complete one step of a Routine's setup that asks for a value, as its card on the Today tab in Popcorn does.
- **[`copy_routine_template`](https://docs.popcorn.ai/mcp/tools/copy-routine-template.md)** — [writes] [destructive] [dry run] Give a Routine its own named copy of the Routine Template it runs.
- **[`create_reference_upload`](https://docs.popcorn.ai/mcp/tools/create-reference-upload.md)** — [writes] Get a URL to upload one file for one of a Routine's References.
- **[`create_routine`](https://docs.popcorn.ai/mcp/tools/create-routine.md)** — [writes] Create a Routine in this workspace, optionally from a Routine Template.
- **[`create_routine_file_upload`](https://docs.popcorn.ai/mcp/tools/create-routine-file-upload.md)** — [writes] Get a URL to upload one file you made, for the next version of a Routine's template.
- **[`create_routine_version`](https://docs.popcorn.ai/mcp/tools/create-routine-version.md)** — [writes] [destructive] [dry run] Save changes as the next version of the Routine's own copy of its Routine Template.
- **[`create_rows`](https://docs.popcorn.ai/mcp/tools/create-rows.md)** — [writes] [dry run] Add rows to one of a Routine's tables.

## D

- **[`delete_rows`](https://docs.popcorn.ai/mcp/tools/delete-rows.md)** — [writes] [destructive] [idempotent] [dry run] Delete rows from one of a Routine's tables, by ID.
- **[`duplicate_routine`](https://docs.popcorn.ai/mcp/tools/duplicate-routine.md)** — [writes] [dry run] Create a new Routine in this workspace that copies an existing one's setup.

## G

- **[`get_instructions`](https://docs.popcorn.ai/mcp/tools/get-instructions.md)** — [read-only] Show a Routine's Instructions, the guidance its agents work from, Routine-wide and for each Step.
- **[`get_memory`](https://docs.popcorn.ai/mcp/tools/get-memory.md)** — [read-only] One memory in full: its text, its category and name, when it was saved and last changed, and its metadata.
- **[`get_routine`](https://docs.popcorn.ai/mcp/tools/get-routine.md)** — [read-only] Show one Routine: its details, your membership, its Routine Template and the version it's on, and its Connections.
- **[`get_routine_change`](https://docs.popcorn.ai/mcp/tools/get-routine-change.md)** — [read-only] Show where a change to a Routine's Steps stands: still drafting, the proposal as Steps before and after, refused, failed or installed.
- **[`get_routine_setting`](https://docs.popcorn.ai/mcp/tools/get-routine-setting.md)** — [read-only] Show one of a Routine's settings in full: its whole value, the template default, what it accepts and who may change it.
- **[`get_row`](https://docs.popcorn.ai/mcp/tools/get-row.md)** — [read-only] Show one row in full: every column, its rev, when it was created and last changed, and its state if the table has a state machine.
- **[`get_run`](https://docs.popcorn.ai/mcp/tools/get-run.md)** — [read-only] One of a Routine's runs, by its reference: how it is going or how it ended, what started it, and its inputs and outputs.
- **[`get_setup`](https://docs.popcorn.ai/mcp/tools/get-setup.md)** — [read-only] Show a Routine's setup checklist, the steps on its Today tab in Popcorn, in order, each with whether it's done and what it still needs.
- **[`get_status`](https://docs.popcorn.ai/mcp/tools/get-status.md)** — [read-only] Where a Routine stands: what its template reports, how many items are at each Status, and what is waiting for a person.
- **[`get_table`](https://docs.popcorn.ai/mcp/tools/get-table.md)** — [read-only] Show a table's columns in order, with each one's type and merge policy, the table's merge key, and its state machine if it has one.
- **[`get_user`](https://docs.popcorn.ai/mcp/tools/get-user.md)** — [read-only] Look up a person by handle: yourself, a member of this workspace, or someone from another workspace you share a Routine or direct message with.
- **[`get_workspace`](https://docs.popcorn.ai/mcp/tools/get-workspace.md)** — [read-only] Show the Popcorn workspace this connection is bound to, and your role in it.

## I

- **[`install_routine`](https://docs.popcorn.ai/mcp/tools/install-routine.md)** — [writes] [destructive] [dry run] Install the newest version of a Routine's copy of its template, or move it onto a copy the workspace already has.

## L

- **[`list_actions`](https://docs.popcorn.ai/mcp/tools/list-actions.md)** — [read-only] List the Actions a person can take on one of a Routine's items now: the buttons Popcorn shows on it, each with the Status it moves the item to.
- **[`list_connections`](https://docs.popcorn.ai/mcp/tools/list-connections.md)** — [read-only] List the Connections a Routine needs: the accounts and other services its template works through.
- **[`list_history`](https://docs.popcorn.ai/mcp/tools/list-history.md)** — [read-only] What happened to one item: each change with who or what made it and why, the runs that changed it and how they ended, and its email turns.
- **[`list_memories`](https://docs.popcorn.ai/mcp/tools/list-memories.md)** — [read-only] List the memories kept for a Routine, the workspace or you, most recently changed first: what people told an agent and what templates keep.
- **[`list_messages`](https://docs.popcorn.ai/mcp/tools/list-messages.md)** — [read-only] A Routine's top-level messages, newest first, or one thread's replies.
- **[`list_references`](https://docs.popcorn.ai/mcp/tools/list-references.md)** — [read-only] List the documents a Routine works from (its References): what each is for, when it was added and by whom, and which are still waiting.
- **[`list_routine_files`](https://docs.popcorn.ai/mcp/tools/list-routine-files.md)** — [read-only] List the files of a version of a Routine's template, with each file's size and sha256.
- **[`list_routine_settings`](https://docs.popcorn.ai/mcp/tools/list-routine-settings.md)** — [read-only] List a Routine's settings, set or not: what its template lets this Routine change on its own.
- **[`list_routine_templates`](https://docs.popcorn.ai/mcp/tools/list-routine-templates.md)** — [read-only] List the Routine Templates a new Routine in this workspace can start from.
- **[`list_routines`](https://docs.popcorn.ai/mcp/tools/list-routines.md)** — [read-only] List the Routines you can see in this workspace: the ones you're in, and the ones you can view without joining.
- **[`list_rows`](https://docs.popcorn.ai/mcp/tools/list-rows.md)** — [read-only] List a table's rows, newest first unless sort says otherwise.
- **[`list_runs`](https://docs.popcorn.ai/mcp/tools/list-runs.md)** — [read-only] The Routine's runs, newest first: the work each did or is doing, how it ended, when, what started it, and its reference.
- **[`list_tables`](https://docs.popcorn.ai/mcp/tools/list-tables.md)** — [read-only] List the tables in a Routine, with each one's row count.
- **[`list_triggers`](https://docs.popcorn.ai/mcp/tools/list-triggers.md)** — [read-only] List how work arrives in a Routine: its schedules, the webhooks other systems post to, and the messages and References that start work.
- **[`list_workspace_members`](https://docs.popcorn.ai/mcp/tools/list-workspace-members.md)** — [read-only] List the members of this workspace, alphabetically by name.

## M

- **[`make_connection`](https://docs.popcorn.ai/mcp/tools/make-connection.md)** — [writes] [destructive] [dry run] Make one of a Routine's Connections: connect an account you have signed in to, or make the webhook another system posts to.

## R

- **[`react`](https://docs.popcorn.ai/mcp/tools/react.md)** — [writes] [idempotent] Add an emoji reaction to a Routine message, or take yours off.
- **[`read_doc`](https://docs.popcorn.ai/mcp/tools/read-doc.md)** — [read-only] Read one page of the Popcorn docs by its id, or one section of it.
- **[`read_history_entry`](https://docs.popcorn.ai/mcp/tools/read-history-entry.md)** — [read-only] One change from an item's History, in full: every field it changed, before and after, and who or what made it and why.
- **[`read_message`](https://docs.popcorn.ai/mcp/tools/read-message.md)** — [read-only] One message in a Routine, in full: its whole text, a line per attachment or other part, its reply count and its reactions.
- **[`read_reference`](https://docs.popcorn.ai/mcp/tools/read-reference.md)** — [read-only] Read one of a Routine's References: its text, or a download link for a file that isn't text, such as a PDF.
- **[`read_routine_file`](https://docs.popcorn.ai/mcp/tools/read-routine-file.md)** — [read-only] Read one file of a version of a Routine's template, exactly as stored.
- **[`run_trigger`](https://docs.popcorn.ai/mcp/tools/run-trigger.md)** — [writes] [destructive] [dry run] Run one of a Routine's schedules now, with the inputs it runs with on schedule.

## S

- **[`search_docs`](https://docs.popcorn.ai/mcp/tools/search-docs.md)** — [read-only] Search the Popcorn docs and get the best pages' titles, ids and summaries.
- **[`search_messages`](https://docs.popcorn.ai/mcp/tools/search-messages.md)** — [read-only] Search message text across the Routines you can see, ranked by relevance or newest first.
- **[`send_message`](https://docs.popcorn.ai/mcp/tools/send-message.md)** — [writes] Post a message in a Routine, visible to its members.
- **[`stop_run`](https://docs.popcorn.ai/mcp/tools/stop-run.md)** — [writes] [destructive] [idempotent] Stop one of a Routine's runs that's still going.

## T

- **[`take_action`](https://docs.popcorn.ai/mcp/tools/take-action.md)** — [writes] [destructive] [dry run] Take one Action on one or more of a Routine's items, as a person pressing its button in Popcorn would.

## U

- **[`update_routine_setting`](https://docs.popcorn.ai/mcp/tools/update-routine-setting.md)** — [writes] [destructive] [dry run] Change one of a Routine's settings, on this Routine only.
- **[`update_row`](https://docs.popcorn.ai/mcp/tools/update-row.md)** — [writes] [idempotent] Change some columns of one row.
<!-- /generated -->
