#!/usr/bin/env python3
"""Regenerate `content/reference/cli.md` from the installed `popcorn` CLI.

The CLI reference is its help menu on a page: every command the menu lists,
under the menu's own headings, with each command's arguments. It is
generated, never hand-written, because the CLI already describes itself two
ways and a third copy would only disagree with them:

    popcorn --help     the grouping — the menu's headings, in its order
    popcorn commands   everything else — every command, subcommand and
                       argument as JSON, plus the --json envelope, exit codes
                       and error codes

The headings come from the help text rather than the schema because the
schema's `category` is coarser than the menu: it files `app`, `template` and
`flow` together, where the menu gives each its own heading. A command the
schema has and the menu does not list is left out, as the menu leaves it out;
one the menu lists and the schema lacks is skipped, since there is nothing to
say about it.

    python3 scripts/sync-cli.py            # read the installed CLI, write the page
    python3 scripts/sync-cli.py --check    # exit 1 if the page is stale

The page describes whichever CLI is installed, so upgrade first. The output is
deterministic — schema order, no timestamps — so a run with nothing changed
produces no diff.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "content" / "reference" / "cli.md"

_HEADING = re.compile(r"^(?P<name>[A-Z][^:]*):$")
_ENTRY = re.compile(r"^  (?P<cmd>[a-z][\w-]*)\s{2,}")


def run(*args: str) -> str:
    try:
        # `--help` exits 0; nothing here should fail, so a failure is real.
        return subprocess.run(["popcorn", *args], capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("✖  the `popcorn` CLI is not installed — this page is generated from it")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"✖  popcorn {' '.join(args)} failed:\n{exc.stderr}")


def menu(help_text: str) -> list[tuple[str, list[str]]]:
    """The help menu's command groups: (heading, top-level commands), in order.

    Only headings followed by indented commands count, so argparse's own
    "options:" block, whose entries start with a dash, is not mistaken for one.
    """
    groups: list[tuple[str, list[str]]] = []
    for line in help_text.splitlines():
        heading = _HEADING.match(line)
        if heading:
            groups.append((heading.group("name"), []))
            continue
        entry = _ENTRY.match(line)
        if entry and groups:
            groups[-1][1].append(entry.group("cmd"))
    return [(name, cmds) for name, cmds in groups if cmds]


def cell(text: str) -> str:
    """Table-safe: a pipe would end the cell, a newline the row."""
    return " ".join(str(text).split()).replace("|", "\\|")


def spelling(arg: dict) -> str:
    """How an argument is written on the command line."""
    if "flags" not in arg:
        return f"`<{arg['name']}>`"
    value = "" if arg.get("type") == "bool" else f" <{arg.get('type') or 'value'}>"
    return ", ".join(f"`{flag}{value}`" for flag in arg["flags"])


def notes(arg: dict) -> str:
    parts = [cell(arg.get("help") or "")]
    if arg.get("choices"):
        parts.append("One of " + ", ".join(f"`{c}`" for c in arg["choices"]) + ".")
    default = arg.get("default")
    if default not in (None, False, "", []):
        parts.append(f"Default `{default}`.")
    return " ".join(p for p in parts if p)


def table(args: list[dict]) -> list[str]:
    if not args:
        return []
    rows = ["| Argument | Required | Notes |", "|---|---|---|"]
    rows += [f"| {spelling(a)} | {'yes' if a.get('required') else ''} | {notes(a)} |" for a in args]
    return rows + [""]


def leaves(cmd: dict, prefix: str = "") -> list[tuple[str, dict]]:
    """Every runnable command under `cmd`, by its full name.

    A command with subcommands is a namespace, not something to run, so only
    its leaves get an entry.
    """
    name = f"{prefix} {cmd['name']}".strip()
    subs = cmd.get("subcommands") or []
    if not subs:
        return [(name, cmd)]
    return [leaf for sub in subs for leaf in leaves(sub, name)]


def page(schema: dict, help_text: str) -> str:
    version = schema["version"]
    by_name = {c["name"]: c for c in schema["commands"]}
    count = sum(len(leaves(by_name[c])) for _, cmds in menu(help_text) for c in cmds if c in by_name)
    out = [
        "---",
        "id: cli",
        "title: CLI",
        "order: 2",
        "layout: lookup",
        f"version: {version}",
        "summary: >",
        "  Every `popcorn` command, grouped the way `popcorn --help` groups them, with",
        "  its arguments — generated from the CLI's own schema. Global flags, agent",
        "  mode, the `--json` envelope, exit codes and error codes follow the",
        "  commands. The CLI installs from its GitHub repository, not PyPI; this page",
        "  describes one release, and `popcorn <command> --help` describes yours.",
        "concepts: [template-authoring, publish-and-apply, fork-line]",
        "applies_to: [cli, mcp, human]",
        "---",
        "",
        f"The {count} commands `popcorn` {version} lists in its help menu, under the",
        "menu's own headings. Each is run as `popcorn <command>`; the global flags",
        "at the end go before the command, as in `popcorn --json app status`.",
        "",
        "This page is generated from `popcorn --help` and `popcorn commands` by",
        "`scripts/sync-cli.py` and never edited by hand. When it and the CLI you",
        "have disagree, the CLI is right: run `popcorn <command> --help`.",
        "",
    ]

    for heading, cmds in menu(help_text):
        out += [f"## {heading}", ""]
        for top in cmds:
            if top not in by_name:
                continue
            for name, cmd in leaves(by_name[top]):
                out += [f"### `{name}`", ""]
                if cmd.get("description"):
                    out += [cell(cmd["description"]), ""]
                out += table(cmd.get("arguments") or [])

    out += ["## Global options", "", "### Global flags", ""]
    out += table(schema.get("global_flags") or [])
    agent = schema.get("agent_mode") or {}
    if agent:
        out += ["### Agent mode", "", f"`{agent['env_var']}=1`. {cell(agent['description'])}", ""]

    envelope = schema.get("envelope") or {}
    out += ["### The --json envelope", ""]
    out += [f"- {cell(n)}" for n in envelope.get("notes", [])]
    out += [
        "",
        "```json",
        json.dumps(envelope.get("success"), ensure_ascii=False),
        json.dumps(envelope.get("error"), ensure_ascii=False),
        "```",
        "",
    ]
    for key in ("streaming", "pagination"):
        if envelope.get(key, {}).get("description"):
            out += [f"**{key.title()}.** {cell(envelope[key]['description'])}", ""]

    out += ["### Exit codes", "", "| Code | Meaning |", "|---|---|"]
    out += [f"| `{code}` | {name} |" for name, code in schema.get("exit_codes", {}).items()]
    out += ["", "### Error codes", "", "| `error_code` | Meaning |", "|---|---|"]
    out += [f"| `{e['code']}` | {cell(e['description'])} |" for e in schema.get("error_codes", [])]
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if the page differs, write nothing")
    args = ap.parse_args()

    text = page(json.loads(run("commands")), run("--help"))
    current = PAGE.read_text() if PAGE.exists() else ""
    if args.check:
        if text != current:
            print(f"✖  {PAGE.relative_to(ROOT)} is stale — run scripts/sync-cli.py", file=sys.stderr)
            return 1
        print(f"✔  {PAGE.relative_to(ROOT)} matches the installed CLI")
        return 0
    if text == current:
        print(f"✔  {PAGE.relative_to(ROOT)} already matches the installed CLI — nothing to write")
        return 0
    PAGE.write_text(text)
    print(f"✔  wrote {PAGE.relative_to(ROOT)}: {text.count(chr(10) + '### `')} commands. "
          "Review the diff, then run the leak guard before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
