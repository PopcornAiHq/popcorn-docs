---
id: mcp/tools/create-routine-version
title: create_routine_version
order: 309
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-06
summary: >
  Save changes as the next version of the Routine's own copy of its Routine
  Template.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/list-routine-settings, mcp/tools/copy-routine-template, mcp/tools/read-doc, mcp/tools/list-routine-files, mcp/tools/read-routine-file, mcp/tools/create-routine-file-upload]
---

[writes] [destructive] [dry run]

```
create_routine_version(routine_id, base_version=None, changes=None, changelog=None, confirm=False, plan_id=None, diff="full")
```

A new version reaches every Routine on that copy: this Routine installs it now (unless its template updates are locked or another install is running), and every other Routine on the copy updates at its daily check. Workspace admins only. To change how one Routine behaves, check [`list_routine_settings`](https://docs.popcorn.ai/mcp/tools/list-routine-settings.md) first, and make a version only for what settings can't express. Without `confirm=true` it's a dry run that changes nothing: the version it would create, each file's diff, every check it would fail, warnings and the reach, and, when every check passes on a copy, a `plan_id` that lasts 30 minutes. To create it, call again with `routine_id`, `confirm=true` and that `plan_id` alone: the changes needn't be sent again, and every check runs again. A Routine on Popcorn's template can dry-run changes, but needs its own copy ([`copy_routine_template`](https://docs.popcorn.ai/mcp/tools/copy-routine-template.md)) before they can be made.

Before writing a change, [`read_doc`](https://docs.popcorn.ai/mcp/tools/read-doc.md) with `template-authoring`; `manifest-keys` and `flow-grammar` cover what a manifest and a Flow may hold.

Each change is one file. A change to a file that exists carries the sha256 it was read at: copy it exactly from [`list_routine_files`](https://docs.popcorn.ai/mcp/tools/list-routine-files.md) or [`read_routine_file`](https://docs.popcorn.ai/mcp/tools/read-routine-file.md).

```text
{"path": "manifest.yaml", "expected_sha256": "…", "ops": […]}
{"path": "flows/new.yaml", "create": "<whole file>"}
{"path": "flows/old.yaml", "delete": true, "expected_sha256": "…"}
{"path": "flows/a.yaml", "rename": "flows/b.yaml", "expected_sha256": "…"}
{"path": "code/x/lib.js", "from_url": "https://unpkg.com/…", "sha256": "…"}
{"path": "code/x/app.js", "from_upload": "<upload_id>"}
```

Ops apply in order. To rewrite a whole file, delete it and create it again. Bump `version:` in manifest.yaml in every new version.

Every op is a text op. The anchor is the file's exact text and must match once: `{"op": "replace", "old_string": "days: 3", "new_string": "days: 5"}`. Also `insert_before` and `insert_after` (anchor, text), prepend and append (text), and `replace_range` (from, to, `new_string`), which replaces from `from` up to `to`: `to` is not replaced and stays in the file, so never end `new_string` with it.

`from_url` has Popcorn fetch a public UTF-8 text file, so you needn't send its content: unpkg.com, cdn.jsdelivr.net, registry.npmjs.org, raw.githubusercontent.com or a github.com release download; at most 10 files and 4 MiB per version. Pin a version in the URL. To replace an existing file, add its `expected_sha256`. The dry run shows each file's sha256, and the confirm takes exactly that content: a confirm by `plan_id` holds it, and a confirm that resends the changes must give each `from_url` change that sha256. Content that changed since the dry run is refused.

`from_upload` takes a file you uploaded with [`create_routine_file_upload`](https://docs.popcorn.ai/mcp/tools/create-routine-file-upload.md), for this Routine and path. Its size and sha256 were fixed when you created it, so it needs no sha256 here. It counts toward the same 10 files and 4 MiB as `from_url`, and goes into one version only.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). This Routine installs the new version at once. |
| `base_version` | `int \| str` | The version the files were read from, as `list_routine_files`' header shows it: the copy's newest version. Its number ("0.16.0") or its version id. Just after `copy_routine_template`, the Popcorn version the copy was made from works too. |
| `changes` | `list[Change]` | The changes, one per file, applied in order. |
| `changelog` | `str` | What changed and why, in a sentence or two (at most 2,000 characters). |
| `confirm` | `bool` | true to create the version. With a person there, show them the dry run first. Default `False`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true`, in place of `base_version`, changes and changelog. |
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
Reach: #intake would install it now. 2 other Routines on this copy will update at their daily check. The Routines on this copy that you can see: list_routines(template="claimcoordinator", copy="acme-intake").
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
