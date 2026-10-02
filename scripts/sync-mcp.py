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
import render

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "content" / "reference" / "mcp.md"
DEFAULT_BACKEND = pathlib.Path.home() / "popcorn" / "backend"
TOOLS_DIR = ("services", "mcp", "tools")
EXAMPLES_DIR = ("services", "mcp", "examples")

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
    "details": "Channels",
    "messages": "Messages",
    "search_messages": "Messages",
    "app_bundle": "App bundle",
}
# Long enough that no word or shortened ID matches, only an opaque token.
_LONG_TOKEN = re.compile(r"[A-Za-z0-9+/=_-]{32,}")

# Designed, not built. See the module docstring before adding to this.
# The design rules are a numbered list, not bullets: on a lookup page a bullet
# that opens in bold is read as a glossary-style entry and indexed.
PROPOSED = """\
## Proposed tools

**This tool does not exist yet, and nothing depends on it arriving.** It is
listed so an author can see what is being considered; its arguments may change
before it ships. Today a bundle's files are edited and published with the
CLI's `app` commands.

### `publish_app_bundle`

Publishes a new version of the channel's bundle to its fork line. Without
`confirm=true`, a dry run of the real publish: the version it would mint, a
diff summary, every check the publish runs, warnings, and how many channels on
the line it reaches. Published is not installed: the channel installs it, and
the rest of the line follows.

Publishing is for workspace admins only, because a publish reaches every
channel on the line. It takes edits rather than whole files, so a one-line
change costs one line; the exact shape of an edit is not settled.

| Argument | Default | Notes |
|---|---|---|
| `channel_id` | | Channel ID; the channel that installs first |
| `base_version_id` | | The head the edits were made against |
| `changes` | | The edits, applied in order; shape not settled |
| `expected_sha256` | `{}` | Per path; refuses a publish against bytes that changed |
| `changelog` | | What changed |
| `confirm` | `false` | Perform the publish the dry run showed |
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
    """Every tool, in page order: by module as `GROUPS` orders them, then in
    the order its module defines them, which keeps a listing beside the reads
    it leads to. Two modules under one heading follow one another."""
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
            found.append({"name": node.name, "summary": summary, "group": GROUPS[path.stem],
                          "at": (list(GROUPS).index(path.stem), node.lineno),
                          "hints": hints(decorator), "args": args})
    return sorted(found, key=lambda t: t["at"])


def examples(root: pathlib.Path, names: set[str]) -> dict[str, dict]:
    """The worked examples by the tool each documents.

    Every call in an example must name a tool the server defines: a stale
    example would show a call nobody can make, so it stops the sync instead.
    """
    found = {}
    for path in sorted(root.joinpath(*EXAMPLES_DIR).glob("*.json")):
        example = json.loads(path.read_text())
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


def anchor(name: str) -> str:
    """The anchor the renderer gives a tool's heading, from the renderer itself:
    nothing checks a link's fragment, so a second copy of the rule could drift."""
    return render._slug(f"`{name}`", set())


def overview(found: list[dict]) -> list[str]:
    """Every tool on one screen: a small table per area, each row its access
    and its first sentence, linking to its entry. A table per area rather than
    an area column, which would take the width the sentences need."""
    out: list[str] = []
    group = None
    for t in found:
        if t["group"] != group:
            group = t["group"]
            out += ([""] if out else []) + [f"**{group}**", "", "| Tool | Access | What it does |", "|---|---|---|"]
        out.append(f"| [`{t['name']}`](#{anchor(t['name'])}) | {access(t['hints'])} "
                   f"| {cell(lead(t['summary'])[0])} |")
    return out + [""]


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
        "  The tools the hosted Popcorn MCP server exposes — people, channels,",
        "  messages and a channel's app bundle — with their arguments, generated",
        "  from the server's own definitions. They read a bundle, fork it and install",
        "  a version; editing and publishing it is the CLI's `app` commands, and a",
        "  publish tool is proposed, listed apart, and not built.",
        "concepts: [app-bundle, publish-and-apply, fork-line]",
        "applies_to: [cli, mcp, human]",
        "---",
        "",
        f"The hosted MCP server exposes {len(found)} tools. They cover people, channels,",
        "messages and a channel's app bundle: find people and channels, read and",
        "search a channel's messages, send messages and reactions, read a bundle's",
        "files, fork it onto the workspace's own line, bring a channel on a fork",
        "line to its line's head, or move it onto another line. They work on",
        "channels only; direct messages are out of reach.",
        "",
        *overview(found),
        "Every call runs as the person who connected the server, with that person's",
        "permissions, in the one workspace the connection is bound to; every",
        "response starts with that workspace's name. To use another workspace,",
        "reconnect. Read tools accept a channel's `#name` or its ID; tools that",
        "write into a channel take `channel_id`, the ID only. A listing returns one",
        "page and a `next_cursor` to pass back with the same arguments. A fork, and",
        "an install that moves a channel onto another line, are a dry run until",
        "called again with `confirm=true`; an install that brings a channel to its",
        "own line's head starts at once.",
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
