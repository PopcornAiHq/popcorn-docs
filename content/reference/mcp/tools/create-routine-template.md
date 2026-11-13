---
id: mcp/tools/create-routine-template
title: create_routine_template
order: 311
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-13
summary: >
  Create a new Routine Template, owned by this workspace, from files you
  write, with its first Version.
concepts: [copying-a-template, versions]
used_with: [mcp/tools/copy-routine-template, mcp/tools/create-routine-version, mcp/tools/read-doc, mcp/tools/create-routine]
---

[writes] [dry run]

```
create_routine_template(name, changes=None, changelog=None, confirm=False, plan_id=None, diff="full")
```

Workspace-only: no other workspace sees it, and it never appears in Popcorn's catalog or takes Popcorn's updates. Workspace admins only. To change an existing template instead, use [`copy_routine_template`](https://docs.popcorn.ai/mcp/tools/copy-routine-template.md) and [`create_routine_version`](https://docs.popcorn.ai/mcp/tools/create-routine-version.md).

Its key is "ws_" + name (name "intake" → "`ws_intake`"), and manifest.yaml's `app_type:` must be that key. [`read_doc`](https://docs.popcorn.ai/mcp/tools/read-doc.md) `template-authoring` covers the files.

Without `confirm=true` it's a dry run that changes nothing: each file's diff, every check it would fail (`create_routine_version`'s checks), and, when all pass, a `plan_id` lasting 30 minutes. Confirm with name, `confirm=true` and that `plan_id`.

Next: create_routine(name=…, template="ws_<name>") creates a Routine on it; `create_routine_version` on that Routine publishes its next Versions, as for a copy.

Changes: `create_routine_version`'s format over an empty template, so each change creates a file:

```text
{"path": "manifest.yaml", "create": "<whole file>"}
```

`from_url` works as there; `from_upload` doesn't (an upload belongs to a Routine), so send the content or add the file in a later Version.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `name` [required] | `str` | Lowercase letters, digits, "-" and "_", starting with a letter or digit, at most 64 characters; not one of this workspace's templates already. |
| `changes` | `list[Change]` | The files, one create or `from_url` change each. |
| `changelog` | `str` | What the template is for (at most 2,000 characters). |
| `confirm` | `bool` | true to create it. With a person there, show them the dry run first. Default `False`. |
| `plan_id` | `str` | The dry run's `plan_id`, with `confirm=true`, in place of changes and changelog. |
| `diff` | `DiffLevel` | The dry run's diffs: "full" (default), "summary" or "none". |

**Example** — “Make us a new template for tracking vendor certificates, then start a Routine on it.”

```text
→ create_routine_template(name="vendor-certs", changes=[{"path": "manifest.yaml", "create": "app_type: ws_vendor-certs\nversion: 0.1.0\ndisplay_name: Vendor certificates\ndescription: Tracks each vendor's insurance certificate and when it expires.\n"}], changelog="Track vendor insurance certificates and their expiry.")

**Dry run.** Nothing was changed.

New Routine Template: ws_vendor-certs, version 0.1.0, in Acme. It is this workspace's own: other workspaces can't see it, and it has no Popcorn template to take updates from.
Files:
- manifest.yaml: created
  ```diff
  --- /dev/null
  +++ b/manifest.yaml
  @@ -0,0 +1,4 @@
  +app_type: ws_vendor-certs
  +version: 0.1.0
  +display_name: Vendor certificates
  +description: Tracks each vendor's insurance certificate and when it expires.
  ```
Reach: no Routine runs it until one is created on it.
plan_id: pL4nN3wT3mpl4t3xQ2a7bc (lasts 30 minutes)

Call again with `confirm=true` to create Routine Template ws_vendor-certs: pass name and plan_id="pL4nN3wT3mpl4t3xQ2a7bc" in place of changes and changelog.

→ create_routine_template(name="vendor-certs", confirm=true, plan_id="pL4nN3wT3mpl4t3xQ2a7bc")

Created Routine Template ws_vendor-certs, version 0.1.0 (version 77). It is this workspace's own: other workspaces can't see it, and it takes no updates from Popcorn.
No Routine runs it yet. Create one on it with create_routine(name=…, template="ws_vendor-certs"); get_routine shows when it is installed. Then change it with create_routine_version on that Routine, with base_version 77.
Files now (use these sha256s as expected_sha256 in the next version):
- manifest.yaml  sha256: d28e8c5b…
```
