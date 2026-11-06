#!/usr/bin/env python3
"""Regenerate the MCP pages in `content/reference/` from the server's tool definitions.

The pages list the tools the hosted Popcorn MCP server exposes, each with its
arguments, as the server itself declares them: the name and signature of each
function registered with `@mcp.tool`, its docstring, and its annotations.
Each tool has a page of its own (`mcp/tools/get-status.md`) with its
signature, arguments and example, and the Tools page (`mcp/tools/index.md`)
lists every tool A to Z, one line each. They are generated, never
hand-written, for the same reason as the activity reference — the
definitions are what the server serves, and a hand-kept list is a second
source that can only drift from them. The Tools page's prose and frontmatter
are hand-written, though: this script fills only its `tools` region
(`fences.py`).

The MCP overview above them, `mcp/index.md`, is hand-written: what the
server offers, how to connect, and what every tool shares, none of which a
tool definition says. It carries no `generated:` line, so this script leaves
it alone.

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

import fences
import platform_version

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "content" / "reference"
# Written into every page this script generates; it is also how the script
# knows which pages under its folder are its own to rewrite or remove.
GENERATED_BY = "scripts/sync-mcp.py"
# The tool index, and the parent of every tool's page: its URL is the folder
# the tool pages sit in.
TOOLS = "mcp/tools"
# Where the MCP pages sit among the reference pages. The overview
# (`mcp/index.md`) is `ORDER` and the Tools page `ORDER + 1`, both hand-written
# with their own `order:`; each tool's page follows from `ORDER + 2`.
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
    "memories": None,
    "docs": None,
}
# Long enough that no word or shortened ID matches, only an opaque token.
_LONG_TOKEN = re.compile(r"[A-Za-z0-9+/=_-]{32,}")

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
        f"generated: {GENERATED_BY}",
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


def tool_list(found: list[dict]) -> str:
    """The Tools page's `tools` region: every tool A to Z under a heading for
    its first letter, one line each — its badges and what it does, linking its
    page. The page around it, and its frontmatter, are hand-written; the tool
    pages are its children in the sidebar."""
    out = []
    letter = None
    for tool in sorted(found, key=lambda t: t["name"]):
        if tool["name"][0].upper() != letter:
            letter = tool["name"][0].upper()
            out += ["", f"## {letter}", ""]
        first, _ = lead(tool["summary"])
        out.append(f"- **[`{tool['name']}`](https://docs.popcorn.ai/{tool_id(tool['name'])}.md)** — "
                   f"{access(tool)} {cell(first)}")
    return "\n".join(out).strip("\n")


def pages(found: list[dict], shown: dict[str, dict]) -> dict[pathlib.Path, str]:
    """Every MCP page, by the path it is written to, without `updated:`."""
    names = {t["name"] for t in found}
    index = REFERENCE / TOOLS / "index.md"
    if not index.exists():
        sys.exit(f"✖  {index.relative_to(ROOT)} is missing — it is hand-written, with a `tools` region")
    page = fences.fill(index.read_text(), {"tools": tool_list(found)}, str(index.relative_to(ROOT)))
    out = {index: platform_version.without(page)}
    for n, tool in enumerate(sorted(found, key=lambda t: t["name"]), 2):
        out[REFERENCE / f"{tool_id(tool['name'])}.md"] = tool_page(tool, shown, ORDER + n, names)
    return out


def ours(path: pathlib.Path) -> bool:
    """A page this script generated, by its `generated:` line. A hand-written
    page beside the generated ones is never this script's to remove."""
    return re.search(rf"^generated: {re.escape(GENERATED_BY)}$", path.read_text(), re.M) is not None


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
    stale = [p for p in (REFERENCE / "mcp").rglob("*.md") if p not in wanted and ours(p) and not fences.names(p.read_text())]
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
