#!/usr/bin/env python3
"""Regenerate the MCP pages in `content/reference/` from the server's tool definitions.

The pages list the tools the hosted Popcorn MCP server exposes, each with its
arguments, as the server itself declares them: the name and signature of each
function registered with `@mcp.tool`, its docstring, and its annotations.
They are two pages: `mcp/index.md` says what the server is, how to connect
to it, the conventions every tool shares and the tools still proposed, and
`mcp/tools/index.md` lists every tool A to Z, one line each, and each tool has
a page of its own under it (`mcp/tools/get-status.md`) with its signature,
arguments and example. All sit in the Reference tab's MCP section. They are generated, never hand-written, for the same reason as the activity
reference — the definitions are what the server serves, and a hand-kept list
is a second source that can only drift from them.

The server lives in the private backend, so this runs only where a backend
checkout exists, named by `$POPCORN_BACKEND` (default `$HOME/popcorn/backend`),
the same checkout `scripts/drift.py` reads. With none there it prints a notice
and exits 0. It reads the source with `ast` and imports nothing, so it needs
none of the backend's dependencies. Check the checkout is on current main
before running: the page describes whatever that checkout defines.

    python3 scripts/sync-mcp.py            # read the checkout, write the pages
    python3 scripts/sync-mcp.py --check    # exit 1 if any page is stale
    python3 scripts/sync-mcp.py --platform-version V

After each prod deploy the backend's deploy pipeline runs the last form
against the deployed checkout with the deploy's version, then opens a pull
request here as the docs bot when the page changed. `--platform-version` sets
the page's `updated:` date; `platform_version.py` says when that line moves.

The page also carries a "Proposed tools" section, which is the one part of
the reference no source generates: tools that are designed but not built.
It is kept here, as `PROPOSED`, so the page still has one writer and is
never edited by hand, and it is deleted as the tools ship and start being
generated like the rest, or as a design is dropped. Nothing in it may name a ticket, a pull request, a
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
import textwrap

import platform_version

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "content" / "reference"
PAGE = REFERENCE / "mcp" / "index.md"
# The tool index, and the parent of every tool's page: its URL is the folder
# the tool pages sit in.
TOOLS = "mcp/tools"
# Where the MCP pages sit among the reference pages: the landing page, then
# the tools.
ORDER = 300
DEFAULT_BACKEND = pathlib.Path.home() / "popcorn" / "backend"
TOOLS_DIR = ("services", "mcp", "tools")
EXAMPLES_DIR = ("services", "mcp", "examples")
INTERNAL_TOOLS = ("services", "mcp", "internal_tools.py")

_ARG = re.compile(r"^(?P<name>\w+):\s*(?P<text>.*)$")
# The end of a description's first sentence: a stop followed by a capital, so
# an "e.g." mid-sentence does not end it.
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")

# The concept page each tool module's tools are about, shown as Related on a
# tool's page: the idea behind the tool, for a reader who has its arguments
# and wants the why. The server files its tools one module per area, so the
# map is by module. None says the area has no concept page of its own; a
# module missing here stops the sync, so a new area is placed, not dropped.
CONCEPTS: dict[str, tuple[str, ...] | None] = {
    "context": None,
    "details": ("routines",),
    "new_project": ("set-up-a-routine",),
    "routine_change": ("steps",),
    "messages": None,
    "search_messages": None,
    "app_bundle": ("copying-a-template", "versions"),
    "flows": ("flow-grammar",),
    "setup": ("set-up-a-routine",),
    "settings": ("routine-settings",),
    "instructions": ("instructions",),
    "agent_store": ("tables",),
    "triggers": ("triggers",),
    "connections": ("connections",),
    "references": ("reference-documents",),
    "status": ("actions-and-status",),
    "actions": ("actions-and-status",),
    "history": ("history",),
    "docs": None,
}
# Long enough that no word or shortened ID matches, only an opaque token.
_LONG_TOKEN = re.compile(r"[A-Za-z0-9+/=_-]{32,}")

# Designed, not built: the product surface, named from the glossary.
# See the module docstring before adding to this. An entry is a
# "## Proposed tools" intro, then one "### `tool`" section per tool;
# proposed() drops a section once the server defines that name. Any numbered
# rules go in a numbered list, not bullets: on a lookup page a bullet that
# opens in bold is read as a glossary-style entry and indexed.
PROPOSED = """\
## Proposed tools

**None of these tools exist yet, and nothing depends on them arriving.** They
are a design for the tools a person's assistant uses to run Routines, named
in the [glossary](https://docs.popcorn.ai/glossary.md)'s
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

### `duplicate_routine`

Makes a new Routine that starts as a copy of an existing one: its template,
Routine Settings, Instructions and References, but none of its items or
History. Connections are not copied, because they sign in as a person.

| Argument | Default | Notes |
|---|---|---|
| `routine_id` | | The Routine to copy |
| `name` | | The new Routine's name |
| `confirm` | `false` | Create the previewed copy |

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
    """Every tool a person's assistant gets, by name."""
    skip = hidden(root)
    found = []
    for path in sorted(root.joinpath(*TOOLS_DIR).glob("*.py")):
        source = path.read_text()
        if "@mcp.tool" in source and path.stem not in CONCEPTS:
            sys.exit(f"✖  tool module {path.stem!r} has no entry in CONCEPTS — name the page its tools are about, or None")
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
            found.append({"name": node.name, "summary": summary, "module": path.stem,
                          "hints": hints(decorator), "args": args})
    return sorted(found, key=lambda t: t["name"])


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


# Tools that take `confirm` only for Popcorn's own channel agent: an
# assistant's call acts at once, so their pages don't promise it a dry run.
CONFIRM_FOR_CHANNEL_AGENT_ONLY = {"create_routine"}


def access(tool: dict) -> str:
    """The tool's access hints as badges, which the renderer colours, and
    `[dry run]` on a tool that takes `confirm`: it only previews until called
    again with `confirm=true`, the convention an assistant most often misses."""
    h = tool["hints"]
    if h.get("readOnlyHint"):
        words = ["read-only"]
    else:
        words = ["writes"]
        if h.get("destructiveHint"):
            words.append("destructive")
        if h.get("idempotentHint"):
            words.append("idempotent")
    if tool["name"] not in CONFIRM_FOR_CHANNEL_AGENT_ONLY and any(
        a["name"] == "confirm" for a in tool["args"]
    ):
        words.append("dry run")
    return " ".join(f"[{w}]" for w in words)


def tool_id(name: str) -> str:
    """A tool's page id: `get_status` → `mcp/tools/get-status`. Dashes, like
    every other address on the site; the page's title keeps the tool's name."""
    return f"{TOOLS}/" + name.replace("_", "-")


def lead(summary: str) -> tuple[str, str]:
    """A description split into its first sentence and the rest."""
    parts = _SENTENCE_END.split(" ".join(summary.split()), maxsplit=1)
    return parts[0], parts[1] if len(parts) > 1 else ""


def cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def signature(tool: dict) -> str:
    """The call as an assistant writes it: required arguments by name, the rest
    with their defaults."""
    parts = []
    for a in tool["args"]:
        if a["required"]:
            parts.append(a["name"])
        else:
            default = a["default"]
            # The parsed default has lost its quotes, so a number or a boolean
            # is written bare and anything else as the string it was.
            if default is None:
                default = "None"
            elif not re.fullmatch(r"-?\d+(\.\d+)?|True|False", default):
                default = json.dumps(default)
            parts.append(f"{a['name']}={default}")
    return f"{tool['name']}({', '.join(parts)})"


def header(*, id: str, title: str, order: int, summary: str, lede: str,
           concepts: list[str], lookup: bool, parent: str = "",
           used_with: list[str] = ()) -> list[str]:
    wrapped = lambda text: textwrap.wrap(text, 76, break_on_hyphens=False)
    return [
        "---",
        f"id: {id}",
        f"title: {title}",
        f"order: {order}",
        "group: MCP",
        *([f"parent: {parent}"] if parent else []),
        *(["layout: lookup"] if lookup else []),
        "summary: >",
        *(f"  {line}" for line in wrapped(summary)),
        *(["lede: >", *(f"  {line}" for line in wrapped(lede))] if lede else []),
        f"concepts: [{', '.join(concepts)}]",
        *([f"used_with: [{', '.join(used_with)}]"] if used_with else []),
        "---",
        "",
    ]


def named_tools(tool: dict, names: set[str]) -> list[str]:
    """The other tools a tool's description and argument notes name, in the
    order they first appear: the workflow it belongs to, as the server
    describes it ("list_actions shows what can be done… take_action does
    it"). Read from the server's own text, so it follows each deploy."""
    text = " ".join([tool["summary"], *(a["text"] for a in tool["args"])])
    found = re.findall(r"(?<![\w.])([a-z]+(?:_[a-z]+)+)(?![\w(])|(?<![\w.])([a-z]+(?:_[a-z]+)+)\(", text)
    seen = []
    for a, b in found:
        n = a or b
        if n in names and n != tool["name"] and n not in seen:
            seen.append(n)
    return seen


def tool_page(tool: dict, shown: dict[str, dict], order: int, names: set[str]) -> str:
    """One tool: its badges, what it does, the call, its arguments and, where
    the server has one, a worked example. The summary is the tool's own first
    sentence, which is what an assistant searching for it should read."""
    first, rest = lead(tool["summary"])
    summary = cell(first)
    if len(summary) > 380:
        summary = summary[:377].rsplit(" ", 1)[0] + "…"
    out = header(
        id=tool_id(tool["name"]),
        title=tool["name"],
        order=order,
        summary=summary,
        lede="",
        concepts=list(CONCEPTS[tool["module"]] or ()),
        lookup=False,
        parent=TOOLS,
        used_with=[tool_id(n) for n in named_tools(tool, names)],
    )
    # The first sentence is the summary, which the page shows under its
    # title; the call comes next, as a usage line does, then the rest.
    out += [access(tool), "", "```", signature(tool), "```", ""]
    if rest:
        out += [cell(rest), ""]
    if tool["args"]:
        out += ["## Arguments", "", "| Argument | Type | Notes |", "|---|---|---|"]
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
    out += [
        "The [MCP server overview](https://docs.popcorn.ai/mcp.md) has what every tool",
        "shares: the Workspace a call runs in, dry runs and `confirm=true`,",
        "`routine` and `routine_id`, and paging with `next_cursor`.",
    ]
    return "\n".join(out).rstrip() + "\n"


def tools_page(found: list[dict], order: int) -> str:
    """Every tool A to Z under a heading for its first letter, one line each:
    its badges and what it does, linking its page. The tool pages are this
    page's children in the sidebar."""
    out = header(
        id=TOOLS,
        title="Tools",
        order=order,
        summary="Every tool the hosted server offers, A to Z, each with whether it reads "
                "or writes and what it does, linking its own page.",
        lede="Every tool on the server, A to Z, each linking its own page.",
        concepts=["mcp"],
        lookup=True,
    )
    reads = sum(1 for t in found if t["hints"].get("readOnlyHint"))
    out += [
        f"The {len(found)} tools the hosted server offers, A to Z: {reads} only read, and the",
        f"other {len(found) - reads} write. A tool marked [dry run] only previews until it is",
        "called again with `confirm=true`. Each tool's page has its call, its arguments",
        "and, for many, a worked example.",
        "",
    ]
    letter = None
    for tool in sorted(found, key=lambda t: t["name"]):
        if tool["name"][0].upper() != letter:
            letter = tool["name"][0].upper()
            out += ["", f"## {letter}", ""]
        first, _ = lead(tool["summary"])
        out.append(f"- **[`{tool['name']}`](https://docs.popcorn.ai/{tool_id(tool['name'])}.md)** — "
                   f"{access(tool)} {cell(first)}")
    return "\n".join(out).rstrip() + "\n"


def landing(found: list[dict]) -> str:
    out = header(
        id="mcp",
        # Not "Popcorn MCP server": search weighs a title word heavily, and
        # "popcorn" is in most questions. Setting the server up is its own
        # page, which this one links; "overview" pairs it with the CLI's.
        title="MCP server overview",
        order=ORDER,
        summary="The hosted Popcorn MCP server, at https://mcp.popcorn.ai/mcp, gives a "
                "person's assistant tools for their Routines. This page says what they "
                "cover and what every tool shares: the Workspace a call runs in, dry "
                "runs and `confirm=true`, `routine` and `routine_id`, and paging. Adding "
                "the server to an assistant has its own page, and the tools are listed "
                "A to Z on theirs.",
        lede="What Popcorn's MCP server gives your assistant, and what every tool shares.",
        concepts=["add-the-mcp-server", "app-bundle", "versions", "copying-a-template"],
        lookup=False,
    )
    out += [
        f"The hosted MCP server gives a person's assistant {len(found)} tools. With them it",
        "can find people and Routines, list the Routine Templates a new Routine can",
        "be made from, create a Routine (optionally from a template), see whether a",
        "Routine's Connections are made and make one from an account already",
        "signed in to or as a webhook, see what starts its work and run a",
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
        "## Get started",
        "",
        "The server's address is `https://mcp.popcorn.ai/mcp`. [Add the MCP",
        "server](https://docs.popcorn.ai/add-the-mcp-server.md) has the steps for",
        "Claude, Claude Code and other assistants, signing in and choosing a",
        "Workspace, and checking the connection.",
        "",
        "## What every tool shares",
        "",
        "Every call runs as the person who connected the server, with that person's",
        "permissions, in the one workspace the connection is bound to; every",
        "response starts with that workspace's name. To use another workspace,",
        "reconnect. Read tools accept a Routine's `#name` or its ID as `routine`;",
        "tools that write into a Routine take `routine_id`, the ID only. A listing",
        "returns one page and a `next_cursor` to pass back with the same arguments.",
        "A fork, a publish, an install that moves a Routine onto another line,",
        "creating a Routine from a template, running a Trigger, taking an Action,",
        "making a Connection, changing a setting and deleting rows are a dry run",
        "until called again with",
        "`confirm=true`. An",
        "install that brings a Routine to its own line's head starts at once, and",
        "so does creating a Routine with no template.",
        "",
        "These pages are generated from the server's tool definitions by",
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
        "## Tool reference",
        "",
        f"[Tools](https://docs.popcorn.ai/{TOOLS}.md) lists all {len(found)} tools A to Z, each linking a",
        "page of its own with its call, arguments and access hints.",
    ]
    out.append("")
    return "\n".join(out) + "\n" + proposed({t["name"] for t in found})


def pages(found: list[dict], shown: dict[str, dict]) -> dict[pathlib.Path, str]:
    """Every MCP page, by the path it is written to, without `updated:`."""
    names = {t["name"] for t in found}
    out = {PAGE: landing(found), REFERENCE / TOOLS / "index.md": tools_page(found, ORDER + 1)}
    for n, tool in enumerate(sorted(found, key=lambda t: t["name"]), 2):
        out[REFERENCE / f"{tool_id(tool['name'])}.md"] = tool_page(tool, shown, ORDER + n, names)
    return out


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

    shown = examples(root, {t["name"] for t in found})
    wanted = {
        path: platform_version.stamp(text, path.read_text() if path.exists() else "", args.platform)
        for path, text in pages(found, shown).items()
    }
    stale = [p for p in (REFERENCE / "mcp").rglob("*.md") if p not in wanted]
    changed = [p for p, text in wanted.items() if not p.exists() or p.read_text() != text]
    if args.check:
        for p in changed + stale:
            print(f"✖  {p.relative_to(ROOT)} is stale — run scripts/sync-mcp.py", file=sys.stderr)
        if changed or stale:
            return 1
        print(f"✔  the {len(wanted)} MCP pages match the server's tool definitions")
        return 0
    if not changed and not stale:
        print(f"✔  the {len(wanted)} MCP pages already match — nothing to write")
        return 0
    for p in changed:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(wanted[p])
    for p in stale:
        p.unlink()
    print(f"✔  wrote {len(changed)} and removed {len(stale)} of the MCP pages ({len(found)} tools). "
          "Review the diff, then run the leak guard before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
