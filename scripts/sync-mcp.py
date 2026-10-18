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
the page's `deployed:` date; `platform_version.py` says when that line moves.

The page also carries a "Proposed tools" section, which is the one part of
the reference no source generates: tools that are designed but not built.
It is kept here, as `PROPOSED`, so the page still has one writer and is
never edited by hand, and it is deleted as the tools ship and start being
generated like the rest. Nothing in it may name a ticket, a pull request, a
private repository or a design document; describe the tool and stop.

Some tools carry a worked example: a request a person might make, the calls
an assistant makes for it, and what each returns. The backend writes these as
`services/mcp/examples/<tool>.json` by running the real tools against fixed
sample data in its own tests, which fail when a tool's output stops matching
its file; this script only reads them, and trims what it shows — the
workspace line and long cursors — without changing the files. An example
naming a tool the server does not define stops the sync, since a rename must
carry its example along.

Descriptions come from backend docstrings, which can carry internal
references a public page must not; the leak guard runs on the generated page
like any other, and the fix for a hit is the docstring, not this script.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import re
import sys

import platform_version

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "content" / "reference" / "mcp.md"
DEFAULT_BACKEND = pathlib.Path.home() / "popcorn" / "backend"
TOOLS_DIR = ("services", "mcp", "tools")
EXAMPLES_DIR = ("services", "mcp", "examples")
INTERNAL_TOOLS = ("services", "mcp", "internal_tools.py")

_ARG = re.compile(r"^(?P<name>\w+):\s*(?P<text>.*)$")
# The end of a description's first sentence: a stop followed by a capital, so
# an "e.g." mid-sentence does not end it.
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")

# The page's sections, in reading order, by the tool module each one covers.
# The server already files its tools by area, one module per area, so the
# grouping is the server's; this only names it. A module missing here stops
# the sync, so a new area gets a heading rather than going unlisted.
GROUPS = {
    "context": "Workspace and people",
    "details": "Routines",
    "new_project": "Routines",
    "messages": "Messages",
    "search_messages": "Messages",
    "app_bundle": "Apps",
    "flows": "Flows",
    "settings": "Routine settings",
    "agent_store": "Tables",
    "triggers": "Triggers",
    "status": "Status",
    "actions": "Actions",
}
# Long enough that no word or shortened ID matches, only an opaque token.
_LONG_TOKEN = re.compile(r"[A-Za-z0-9+/=_-]{32,}")

# Designed, not built: the product surface, named from the product glossary.
# See the module docstring before adding to this. An entry is a
# "## Proposed tools" intro, then one "### `tool`" section per tool;
# proposed() drops a section once the server defines that name. Any numbered
# rules go in a numbered list, not bullets: on a lookup page a bullet that
# opens in bold is read as a glossary-style entry and indexed.
PROPOSED = """\
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

### `list_routines`

Read-only. The Routines the caller can see in this workspace, each with its
template, its Status counts and whether it is missing a Connection.

| Argument | Default | Notes |
|---|---|---|
| `template` | | Only Routines made from this Routine Template |
| `query` | | Matches a Routine's name |
| `cursor` | | From the previous page |

### `get_routine`

Read-only. One Routine: its template, whether it still receives the
template's improvements, its Triggers, its Connections and which are missing,
and a count of items per Status.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `wait_seconds` | `0` | Wait up to this long for a Routine that is still being set up |

### `list_routine_templates`

Read-only. The Routine Templates this workspace can start a Routine from,
each with what it is for and the Connections it needs.

| Argument | Default | Notes |
|---|---|---|
| `query` | | Matches a template's name or description |

### `create_routine`

Starts a new Routine from a Routine Template. Without `confirm`, says what
the Routine will be set up with and which Connections a person will need to
make.

| Argument | Default | Notes |
|---|---|---|
| `name` | | The new Routine's name |
| `template` | | The Routine Template to start from |
| `confirm` | `false` | Create the previewed Routine |

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

### `list_triggers`

Read-only. How work arrives in a Routine: each schedule with its cadence,
each address another system posts to (never the address itself, which is a
credential), each message or document that starts work, and a booking link.
A Trigger that is paused says so.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |

### `run_trigger`

Runs a scheduled Trigger now, with the inputs it runs with on schedule, and
leaves its schedule unchanged. Without `confirm`, says what the run will do.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | Routine ID |
| `trigger` | | A scheduled Trigger, as `list_triggers` names it |
| `confirm` | `false` | Start the run |

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

### `list_routine_settings`

Read-only. A Routine's settings: each one's value, what it does, whether it
was changed for this Routine, and who may change it. Secrets are never shown.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |

### `get_routine_setting`

Read-only. One setting in full, including long text values.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `setting` | | As `list_routine_settings` names it |

### `update_routine_setting`

Changes one setting on one Routine, or sets it back to the template's value.
The change reaches only that Routine and survives the template's
improvements.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | Routine ID |
| `setting` | | As `list_routine_settings` names it |
| `value` | | The new value |
| `reset` | `false` | Return to the template's value |
| `confirm` | `false` | Apply the previewed change |

### `get_status`

Read-only. Where a Routine's items stand: a count per Status, the items
waiting on a person, and the stages an item moves through. One item's Status
is on its Row.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `table` | | The Table to count; the Routine's main one by default |

### `list_actions`

Read-only. The Actions a person can take on one item now, given where it
stands, with what each will do.

| Argument | Default | Notes |
|---|---|---|
| `routine` | | Routine ID or `#name` |
| `table` | | The item's Table |
| `row_id` | | The item |

### `take_action`

Takes an Action on one or more items, as a person pressing its button would.
Refused for an item where the Action does not apply. Without `confirm`, says
what will happen to each item.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | Routine ID |
| `table` | | The items' Table |
| `row_ids` | | The items |
| `action` | | As `list_actions` names it |
| `confirm` | `false` | Take the previewed Action |

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
"""


def proposed(defined: set[str]) -> str:
    """`PROPOSED` without the tools the server already defines.

    A tool's entry stays in `PROPOSED` until someone deletes it, but the
    server can ship the tool first; the page then lists it once, as
    generated. With no proposed tool left, the section goes.
    """
    intro, _, rest = PROPOSED.partition("\n### ")
    sections = ["### " + part for part in rest.split("\n### ")] if rest else []
    kept = [s for s in sections if re.match(r"### `(\w+)`", s).group(1) not in defined]
    if not kept:
        return ""
    return intro + "\n" + "\n".join(kept)


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


def hidden(root: pathlib.Path) -> set[str]:
    """The tools the server keeps from a person's assistant: the keys of
    `EXTERNAL_EXCLUDED_TOOLS` in the server's dispatch module. They stay
    defined for the server's own use, so the page leaves them out by name.
    None when the checkout predates the set."""
    path = root.joinpath(*INTERNAL_TOOLS)
    if not path.exists():
        return set()
    for node in ast.walk(ast.parse(path.read_text())):
        target = getattr(node, "target", None) or next(iter(getattr(node, "targets", [])), None)
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(target, ast.Name) \
                and target.id == "EXTERNAL_EXCLUDED_TOOLS" and isinstance(node.value, ast.Dict):
            return {k.value for k in node.value.keys if isinstance(k, ast.Constant)}
    return set()


def tools(root: pathlib.Path) -> list[dict]:
    """Every tool a person's assistant gets, in page order: by module as
    `GROUPS` orders them, then in the order its module defines them, which
    keeps a listing beside the reads it leads to. Two modules under one
    heading follow one another. A module whose tools are all hidden gets no
    section."""
    skip = hidden(root)
    found = []
    for path in sorted(root.joinpath(*TOOLS_DIR).glob("*.py")):
        source = path.read_text()
        if "@mcp.tool" in source and path.stem not in GROUPS:
            sys.exit(f"✖  tool module {path.stem!r} has no section in GROUPS — name its area")
        for node in ast.walk(ast.parse(source)):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            decorator = next(
                (d for d in node.decorator_list
                 if isinstance(d, ast.Call) and ast.unparse(d.func) == "mcp.tool"),
                None,
            )
            if decorator is None or node.name in skip:
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
            found.append({"name": node.name, "summary": summary, "group": GROUPS[path.stem],
                          "at": (list(GROUPS).index(path.stem), node.lineno),
                          "hints": hints(decorator), "args": args})
    return sorted(found, key=lambda t: t["at"])


def examples(root: pathlib.Path, names: set[str]) -> dict[str, dict]:
    """The worked examples by the tool each documents.

    A hidden tool's example is skipped with its tool. Every call in the rest
    must name a tool on the page: a stale example would show a call nobody
    can make, so it stops the sync instead.
    """
    skip = hidden(root)
    found = {}
    for path in sorted(root.joinpath(*EXAMPLES_DIR).glob("*.json")):
        example = json.loads(path.read_text())
        if example["tool"] in skip:
            continue
        unknown = {c["tool"] for c in example["calls"]} - names
        if example["tool"] not in names or unknown:
            sys.exit(f"✖  example {path.name} calls a tool the server doesn't define: "
                     f"{sorted(unknown | ({example['tool']} - names))}")
        found[example["tool"]] = example
    return found


def call(tool: str, arguments: dict) -> str:
    """A call as the server's own responses write one: `name(arg="value")`."""
    args = ", ".join(f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in arguments.items())
    return f"{tool}({args})"


def shown_response(response: str) -> str:
    """A response as the page shows it: without the workspace line every
    response opens with, which the page's introduction states once, and with
    any long opaque token, such as a cursor, cut to its first characters. The
    point of an example is the response's shape, which neither carries."""
    lines = response.splitlines()
    if lines and lines[0].startswith("Workspace: "):
        lines = lines[1:]
    return "\n".join(_LONG_TOKEN.sub(lambda m: m.group()[:8] + "…", line) for line in lines)


def worked(example: dict) -> list[str]:
    """The example under a tool's arguments: the request on one line, then one
    block holding each call, marked `→`, and the response it returns, a blank
    line apart so the call stands out from the output. The response is a block
    because its line breaks are part of the payload."""
    out = [f"**Example** — “{' '.join(example['prompt'].split())}”", "", "```text"]
    for i, c in enumerate(example["calls"]):
        out += ([""] if i else []) + [f"→ {call(c['tool'], c['arguments'])}", "", shown_response(c["response"])]
    return out + ["```", ""]


def access(h: dict[str, bool]) -> str:
    """The tool's access hints as badges, which the renderer colours."""
    if h.get("readOnlyHint"):
        return "[read-only]"
    words = ["writes"]
    if h.get("destructiveHint"):
        words.append("destructive")
    if h.get("idempotentHint"):
        words.append("idempotent")
    return " ".join(f"[{w}]" for w in words)


def lead(summary: str) -> tuple[str, str]:
    """A description split into its first sentence and the rest."""
    parts = _SENTENCE_END.split(" ".join(summary.split()), maxsplit=1)
    return parts[0], parts[1] if len(parts) > 1 else ""


def cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def page(found: list[dict], shown: dict[str, dict]) -> str:
    out = [
        "---",
        "id: mcp",
        "title: MCP",
        "order: 3",
        "layout: lookup",
        "summary: >",
        "  The tools the hosted Popcorn MCP server gives a person's assistant —",
        "  people, Routines, their Triggers, Actions, settings and tables, and a",
        "  Routine's app — with their arguments, generated from the server's own",
        "  definitions.",
        "concepts: [app-bundle, publish-and-apply, fork-line]",
        "layer: product",
        "---",
        "",
        f"The hosted MCP server gives a person's assistant {len(found)} tools. With them it",
        "can find people and Routines, list the Routine Templates a new Routine can",
        "be made from, create a Routine (optionally from a template), see whether a",
        "Routine's Connections are made, see what starts its work and run a",
        "schedule now, list and take the Actions on its items, read and change its",
        "settings, read its tables and rows and add, change or delete rows, and read",
        "the files of the app a Routine runs, fork it onto the workspace's own line,",
        "publish changes to a fork line, and bring a Routine on a fork line to its",
        "line's head or move it onto another line. They work on Routines only; a",
        "Routine's messages and runs are read in Popcorn.",
        "",
        "A Routine is what the CLI and the API call a channel, and its Routine",
        "Template's code is what they call an app (an app bundle); the `#name` and",
        "the IDs are the same.",
        "",
        "Every call runs as the person who connected the server, with that person's",
        "permissions, in the one workspace the connection is bound to; every",
        "response starts with that workspace's name. To use another workspace,",
        "reconnect. Read tools accept a Routine's `#name` or its ID as `routine`;",
        "tools that write into a Routine take `routine_id`, the ID only. A listing",
        "returns one page and a `next_cursor` to pass back with the same arguments.",
        "A fork, a publish, an install that moves a Routine onto another line,",
        "creating a Routine from a template, running a Trigger, taking an Action,",
        "changing a setting and deleting rows are a dry run until called again with",
        "`confirm=true`. An",
        "install that brings a Routine to its own line's head starts at once, and",
        "so does creating a Routine with no template.",
        "",
        "This page is generated from the server's tool definitions by",
        "`scripts/sync-mcp.py` after each prod deploy and never edited by hand; a",
        "date beside the title is the day of the deploy that last changed it. The",
        "badges under each tool are the access hints the server declares to the",
        "host — `[read-only]`, or `[writes]` with `[destructive]` or `[idempotent]`",
        "— and a host may use them to decide what to ask before calling. An argument",
        "marked `[required]` must be passed; every other one may be left out.",
        "",
        "Under some tools is an example: a request a person might make, then each",
        "call an assistant makes for it, marked `→`, followed by what the tool",
        "returns. The response is the server's real output for sample data — the",
        "workspace Acme — produced by running the tool in the server's tests, so it",
        "changes when the tool's output does. Examples leave out the workspace line",
        "every response opens with. IDs are shortened, as `8c1f…e2`, a cursor keeps",
        "its first characters, and a long listing keeps its first rows.",
        "",
    ]
    group = None
    for tool in found:
        if tool["group"] != group:
            group = tool["group"]
            out += [f"## {group}", ""]
        first, rest = lead(tool["summary"])
        out += [f"### `{tool['name']}`", "", access(tool["hints"]), "", cell(first), ""]
        if rest:
            out += [cell(rest), ""]
        if tool["args"]:
            out += ["| Argument | Type | Notes |", "|---|---|---|"]
            for a in tool["args"]:
                note = cell(a["text"])
                # A docstring often states its own default; say it once.
                if a["default"] is not None and "default" not in note.lower():
                    note = f"{note} Default `{a['default']}`.".strip()
                name = f"`{a['name']}`" + (" [required]" if a["required"] else "")
                out.append(f"| {name} | {a['type']} | {note} |")
            out.append("")
        if tool["name"] in shown:
            out += worked(shown[tool["name"]])
    return "\n".join(out) + "\n" + proposed({t["name"] for t in found})


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
    shown = examples(root, {t["name"] for t in found})
    text = platform_version.stamp(page(found, shown), current, args.platform)
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
