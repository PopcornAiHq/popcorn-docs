#!/usr/bin/env python3
"""Regenerate `content/reference/mcp.md` from the MCP server's tool definitions.

The page lists the tools the hosted Popcorn MCP server exposes, each with its
arguments, as the server itself declares them: the name and signature of each
function registered with `@mcp.tool`, its docstring, and its annotations. It
is generated, never hand-written, for the same reason as the activity
reference — the definitions are what the server serves, and a hand-kept list
is a second source that can only drift from them.

The server lives in the private backend, so this runs only where a backend
checkout exists, named by `$POPCORN_BACKEND` (default `$HOME/popcorn/backend`),
the same checkout `scripts/drift.py` reads. With none there it prints a notice
and exits 0. It reads the source with `ast` and imports nothing, so it needs
none of the backend's dependencies. Check the checkout is on current main
before running: the page describes whatever that checkout defines.

    python3 scripts/sync-mcp.py            # read the checkout, write the page
    python3 scripts/sync-mcp.py --check    # exit 1 if the page is stale
    python3 scripts/sync-mcp.py --platform-version V

After each prod deploy the backend's deploy pipeline runs the last form
against the deployed checkout with the deploy's version, then opens a pull
request here as the docs bot when the page changed. `--platform-version` sets
the page's `platform:` date; `platform_version.py` says when that line moves.

The page also carries a "Proposed tools" section, which is the one part of
the reference no source generates: tools that are designed but not built.
It is kept here, as `PROPOSED`, so the page still has one writer and is
never edited by hand, and it is deleted as the tools ship and start being
generated like the rest. Nothing in it may name a ticket, a pull request, a
private repository or a design document; describe the tool and stop.

Descriptions come from backend docstrings, which can carry internal
references a public page must not; the leak guard runs on the generated page
like any other, and the fix for a hit is the docstring, not this script.
"""

from __future__ import annotations

import argparse
import ast
import os
import pathlib
import re
import sys

import platform_version

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "content" / "reference" / "mcp.md"
DEFAULT_BACKEND = pathlib.Path.home() / "popcorn" / "backend"
TOOLS_DIR = ("services", "mcp", "tools")

_ARG = re.compile(r"^(?P<name>\w+):\s*(?P<text>.*)$")

# Designed, not built. See the module docstring before adding to this.
# The design rules are a numbered list, not bullets: on a lookup page a bullet
# that opens in bold is read as a glossary-style entry and indexed.
PROPOSED = """\
## Proposed tools

**None of these tools exist yet, and nothing depends on them arriving.** They
are a design for changing an app from an MCP host: check out a channel's
bundle, edit it, prove the edit with a publish dry run, fork if the channel is
still on the product version, publish to its fork line, and watch the
install. The dry run comes before the fork because the fork is the step that
cannot be undone. They are listed so an author can see
what is being considered; names and arguments may change before any ships.
Today an app is changed with the CLI's `app` commands.

Three rules run through the design:

1. **Every write is previewed by the server.** A call without `confirm=true`
  runs the real operation with the write removed and returns what would
  happen, with a `preview_id`. The confirming call passes that id back, and
  the server refuses a confirm whose id does not match a preview of the same
  arguments by the same caller. This proves a dry run happened; whether a
  person read it is up to the host.
2. **Writes take the channel's UUID**, never a `#name`: names are not unique,
  and a publish is the worst place to resolve one to the wrong channel.
3. **Publish takes edits, not whole files** — each edit replaces text that
  must be non-empty and occur exactly once in the file, edits apply in the
  order given, and the file is checked against its hash — so a one-line change
  costs one line.

### `app_status`

Read-only. What a channel runs: the app, its line, the bound version and the
line's head, the install state and why, and the other channels on the line.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID or `#name` |

### `app_checkout`

Read-only. Without `paths`, lists the bundle's files with sizes, hashes and
the `base_version_id` a publish must name. With `paths`, returns those files,
and never a truncated one: a file that does not fit in the response is listed
as not returned, to ask for again, and a file too large for any response comes
back in byte ranges with its hash.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID or `#name` |
| `ref` | `head` | `head` is a publish base; `bound` reads what runs and says when it is not a base |
| `paths` | | Files to return whole |
| `version_id` | | A past version, for reading; never a publish base. Wins over `ref`, and the response reports `ref` as `version` |

### `app_fork`

Moves a channel from the product version onto a fork line. One-way. Without
`confirm`, previews whether it would create a line, adopt an existing one, do
nothing because the channel is already on a fork, or refuse because more than
one line could be meant.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID |
| `line` | | The line to fork to or adopt |
| `confirm` | `false` | Perform the previewed fork |
| `preview_id` | | The id the preview returned; required with `confirm` |

### `app_publish`

Publishes a new version to the channel's line. Without `confirm`, a dry run of
the real publish: the version it would mint, a diff summary, every check the
publish runs, warnings, and how many channels on the line it reaches. Published
is not installed: the channel installs it, and the rest of the line follows.

Publishing is for workspace admins only, because a publish reaches every
channel on the line. The dry run also accepts the product version as a base,
so an edit can be proven before the channel forks; only the confirmed publish
needs the fork line.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID; the channel that installs first |
| `base_version_id` | | The head the edits were made against |
| `edits` | `[]` | `{path, old, new}`, applied in order; `old` must be non-empty and occur exactly once |
| `files` | `{}` | New files only |
| `deletes` | `[]` | Paths to remove |
| `expected_sha256` | `{}` | Per path; refuses a publish against bytes that changed |
| `changelog` | | What changed |
| `confirm` | `false` | Perform the previewed publish |
| `preview_id` | | The id the preview returned; required with `confirm` |

### `app_apply`

Installs the line's head on a channel. Catching up on the line the channel is
already on needs no confirmation; adopting a different line does.

| Argument | Default | Notes |
|---|---|---|
| `channel` | | Channel UUID |
| `confirm` | `false` | Perform an adoption |
| `preview_id` | | The id the adoption preview returned; required with `confirm` |
"""


def backend() -> pathlib.Path | None:
    path = pathlib.Path(os.environ.get("POPCORN_BACKEND") or DEFAULT_BACKEND).expanduser()
    return path if path.joinpath(*TOOLS_DIR).is_dir() else None


def docstring(text: str) -> tuple[str, dict[str, str]]:
    """Split a Google-style docstring into its prose and its `Args:` entries.

    Prose after the `Args:` block, as in a closing "provide one or the other"
    note, is kept with the summary rather than dropped.
    """
    prose: list[str] = []
    args: dict[str, str] = {}
    current: str | None = None
    in_args = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "Args:":
            in_args = True
            continue
        if in_args and line.startswith("    ") and stripped:
            arg = _ARG.match(stripped)
            if arg and not line.startswith("        "):
                current = arg.group("name")
                args[current] = arg.group("text")
            elif current:
                args[current] += " " + stripped
            continue
        if in_args and not stripped:
            continue
        in_args = False
        prose.append(line)
    return " ".join(" ".join(prose).split()), args


def kind(annotation: ast.expr | None) -> tuple[str, bool]:
    """(type as a reader writes it, whether None is allowed)."""
    if annotation is None:
        return "", True
    text = ast.unparse(annotation)
    optional = "| None" in text or text.startswith("Optional[")
    text = text.replace(" | None", "")
    literal = re.fullmatch(r"Literal\[(.*)\]", text)
    if literal:
        values = [v.strip().strip("'\"") for v in literal.group(1).split(",")]
        text = "one of " + ", ".join(f"`{v}`" for v in values)
    else:
        text = f"`{text}`"
    return text, optional


def hints(decorator: ast.Call) -> dict[str, bool]:
    for kw in decorator.keywords:
        if kw.arg == "annotations" and isinstance(kw.value, ast.Call):
            return {
                k.arg: bool(k.value.value)
                for k in kw.value.keywords
                if k.arg and isinstance(k.value, ast.Constant)
            }
    return {}


def tools(root: pathlib.Path) -> list[dict]:
    found = []
    for path in sorted(root.joinpath(*TOOLS_DIR).glob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            decorator = next(
                (d for d in node.decorator_list
                 if isinstance(d, ast.Call) and ast.unparse(d.func) == "mcp.tool"),
                None,
            )
            if decorator is None:
                continue
            summary, described = docstring(ast.get_docstring(node) or "")
            params = node.args.args
            defaults = [None] * (len(params) - len(node.args.defaults)) + node.args.defaults
            args = []
            for param, default in zip(params, defaults):
                type_text, optional = kind(param.annotation)
                args.append({
                    "name": param.arg,
                    "type": type_text,
                    "required": default is None and not optional,
                    "default": None if default is None or ast.unparse(default) == "None"
                    else ast.unparse(default).strip("'\""),
                    "text": described.get(param.arg, ""),
                })
            found.append({"name": node.name, "summary": summary,
                          "hints": hints(decorator), "args": args})
    return sorted(found, key=lambda t: t["name"])


def access(h: dict[str, bool]) -> str:
    if h.get("readOnlyHint"):
        return "Read-only."
    words = ["Writes"]
    if h.get("destructiveHint"):
        words.append("destructive")
    if h.get("idempotentHint"):
        words.append("idempotent")
    return ", ".join(words) + "."


def cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def page(found: list[dict]) -> str:
    out = [
        "---",
        "id: mcp",
        "title: MCP",
        "order: 3",
        "layout: lookup",
        "summary: >",
        "  The tools the hosted Popcorn MCP server exposes — identity, channel",
        "  details, search, message history, posting and reactions — with their",
        "  arguments, generated from the server's own definitions. None changes an",
        "  app: that is the CLI's `app` commands. Tools for checking out, forking,",
        "  publishing and applying an app are proposed, listed apart, and not built.",
        "concepts: [app-bundle, publish-and-apply, fork-line]",
        "applies_to: [cli, mcp, human]",
        "---",
        "",
        f"The hosted MCP server exposes {len(found)} tools. They cover the conversation",
        "surface: who you are, a channel's details, search, message history,",
        "posting and reactions. Reads accept a channel's `#name` or its ID. Every",
        "call runs as the person who connected the server, in the workspace",
        "`whoami` last selected, with that person's permissions.",
        "",
        "This page is generated from the server's tool definitions by",
        "`scripts/sync-mcp.py` after each prod deploy and never edited by hand; a",
        "date beside the title is the day of the deploy that last changed it. The",
        "access line under each tool is the hint the server declares to the host; a",
        "host may use it to decide what to ask before calling.",
        "",
        "## Tools",
        "",
    ]
    for tool in found:
        out += [f"### `{tool['name']}`", "", f"{access(tool['hints'])} {cell(tool['summary'])}", ""]
        if tool["args"]:
            out += ["| Argument | Type | Required | Notes |", "|---|---|---|---|"]
            for a in tool["args"]:
                note = cell(a["text"])
                # A docstring often states its own default; say it once.
                if a["default"] is not None and "default" not in note.lower():
                    note = f"{note} Default `{a['default']}`.".strip()
                out.append(f"| `{a['name']}` | {a['type']} | {'yes' if a['required'] else ''} | {note} |")
            out.append("")
    return "\n".join(out) + "\n" + PROPOSED


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if the page differs, write nothing")
    platform_version.add_argument(ap)
    args = ap.parse_args()

    root = backend()
    if root is None:
        print("ℹ  no backend checkout found. The MCP server's source is in the private "
              "backend, so this runs only beside a checkout; set POPCORN_BACKEND to point at one.")
        return 0
    found = tools(root)
    if not found:
        sys.exit("✖  no @mcp.tool definitions found — has the server moved in the checkout?")

    current = PAGE.read_text() if PAGE.exists() else ""
    text = platform_version.stamp(page(found), current, args.platform)
    if args.check:
        if text != current:
            print(f"✖  {PAGE.relative_to(ROOT)} is stale — run scripts/sync-mcp.py", file=sys.stderr)
            return 1
        print(f"✔  {PAGE.relative_to(ROOT)} matches the server's tool definitions")
        return 0
    if text == current:
        print(f"✔  {PAGE.relative_to(ROOT)} already matches — nothing to write")
        return 0
    PAGE.write_text(text)
    print(f"✔  wrote {PAGE.relative_to(ROOT)}: {len(found)} tools. "
          "Review the diff, then run the leak guard before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
