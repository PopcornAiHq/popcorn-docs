#!/usr/bin/env python3
"""Regenerate the CLI pages in `content/reference/` from the installed `popcorn` CLI.

The CLI reference is its help menu as pages, laid out like the Temporal and
Terraform CLI docs: `cli/index.md` is the CLI's landing page — installing it,
signing in, and what every command shares (global flags, agent mode, the
`--json` envelope, exit and error codes) — `cli/commands/index.md` indexes
every command A to Z, and each top-level command gets a page of its own,
`cli/commands/<command>.md`, with every subcommand under it: what it does, a
Usage line, and its arguments. A command with no subcommands is a single
entry, so those share `cli/commands/other.md`. All of them sit in the Reference
tab's CLI section. They are generated, never hand-written, because the CLI
already describes itself two ways and a third copy would only disagree with
them:

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

    python3 scripts/sync-cli.py            # read the installed CLI, write the pages
    python3 scripts/sync-cli.py --check    # exit 1 if any page is stale

The pages describe whichever CLI is installed, so upgrade first. The output is
deterministic — schema order, no timestamps — so a run with nothing changed
produces no diff. A `cli-*.md` page whose heading the menu no longer has is
deleted, so a removed command does not leave its old page behind.

The install and sign-in prose on the landing page is the one part written
here rather than read from the CLI; it follows the CLI repository's README.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "content" / "reference"
PAGE = REFERENCE / "cli" / "index.md"
# Where the CLI pages sit among the reference pages: after Activities and MCP,
# the landing page first, then the menu's headings in its order.
ORDER = 200
REPO = "https://github.com/PopcornAiHq/popcorn-cli.git"
# The command index, and the parent of every command's page: its URL is the
# folder the command pages sit in.
INDEX = "cli/commands"
# Where the commands with no subcommands go. Each is one entry, so a page each
# would be a page holding one Usage line, and several would be stubs. The
# CLI's own `commands` command is one of them, so it never claims INDEX's URL.
OTHER = f"{INDEX}/other"

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


def slug(command: str) -> str:
    """A top-level command's page id: `channel-config` → `cli/commands/channel-config`."""
    if f"{INDEX}/{command}" == OTHER:
        sys.exit(f"✖  a command named {command!r} would take the Other commands page's URL")
    return f"{INDEX}/{command}"


def file_of(page_id: str) -> pathlib.Path:
    """Where a page's source is written: its id as a path, or the `index.md`
    of the folder its children sit in."""
    if page_id in ("cli", INDEX):
        return REFERENCE / page_id / "index.md"
    return REFERENCE / f"{page_id}.md"


def bare(top: dict) -> bool:
    """A command with no subcommands, listed on OTHER."""
    return not top.get("subcommands")


def href_of(top: dict) -> str:
    """Where a command is described: its own page, or its entry on OTHER."""
    name = top["name"]
    return f"{OTHER}.md#{name}" if bare(top) else f"{slug(name)}.md"


def usage(name: str, args: list[dict]) -> str:
    """The command as typed: its positional arguments, its required flags, and
    `[flags]` when it takes optional ones."""
    parts = ["popcorn", name]
    for arg in args:
        if "flags" in arg:
            continue
        parts.append(f"<{arg['name']}>" if arg.get("required") else f"[<{arg['name']}>]")
    for arg in args:
        if "flags" in arg and arg.get("required"):
            value = "" if arg.get("type") == "bool" else f" <{arg.get('type') or 'value'}>"
            parts.append(arg["flags"][0] + value)
    if any("flags" in a and not a.get("required") for a in args):
        parts.append("[flags]")
    return " ".join(parts)


def header(*, id: str, title: str, order: int, version: str, summary: str,
           lede: str, concepts: list[str], lookup: bool, parent: str = "") -> list[str]:
    wrapped = lambda text: textwrap.wrap(text, 76, break_on_hyphens=False)
    return [
        "---",
        f"id: {id}",
        f"title: {title}",
        f"order: {order}",
        "group: CLI",
        *([f"parent: {parent}"] if parent else []),
        *(["layout: lookup"] if lookup else []),
        f"version: {version}",
        "summary: >",
        *(f"  {line}" for line in wrapped(summary)),
        "lede: >",
        *(f"  {line}" for line in wrapped(lede)),
        f"concepts: [{', '.join(concepts)}]",
        "---",
        "",
    ]


def command_page(top: dict, commands: list[tuple[str, dict]], order: int, version: str) -> str:
    """One top-level command and every subcommand under it, as the Temporal
    docs give `temporal workflow` a page."""
    name = top["name"]
    out = header(
        id=slug(name),
        title=name,
        order=order,
        version=version,
        # No "popcorn" and no list of subcommands: the subcommands are this
        # page's entries, which search matches by name, and a word on every
        # CLI page would count as one most pages share.
        summary=f"The {name} command and its subcommands, each with its Usage line "
                "and arguments.",
        lede=f"Every {name} subcommand, with how to run it and its arguments.",
        concepts=["cli"],
        lookup=True,
        parent=INDEX,
    )
    out += [
        f"`popcorn {name}` in `popcorn` {version}. Global flags go before the command, as",
        "in `popcorn --json app status`; the",
        "[CLI overview](https://docs.popcorn.ai/cli.md) page lists them, with the",
        "`--json` envelope and the exit codes every command shares.",
        "",
    ]
    for full, cmd in commands:
        args = cmd.get("arguments") or []
        out += [f"### `{full}`", ""]
        if cmd.get("description"):
            out += [cell(cmd["description"]), ""]
        out += ["```", usage(full, args), "```", ""]
        out += table(args)
    return "\n".join(out).rstrip() + "\n"


def landing(schema: dict, tops: list[tuple[dict, list[tuple[str, dict]]]], version: str) -> str:
    count = sum(len(cmds) for _, cmds in tops)
    out = header(
        id="cli",
        # Not "Popcorn CLI": search weighs a title word heavily, and "popcorn"
        # is in most questions, so the landing page would answer all of them.
        title="CLI overview",
        order=ORDER,
        version=version,
        summary="The `popcorn` CLI works with Popcorn from a terminal or a script. It "
                "installs from its GitHub repository, not PyPI, and `popcorn auth login` "
                "signs in. This page has what every command shares: global flags, agent "
                "mode, the `--json` envelope, exit codes and error codes. Each command "
                "group has its own page.",
        lede="Install the popcorn CLI, sign in, and learn the flags and output every command shares.",
        concepts=["template-authoring", "versions", "copying-a-template"],
        lookup=False,
    )
    out += [
        f"The `popcorn` CLI works with Popcorn from a terminal or a script: building and",
        "publishing Routine Templates, reading and posting messages, running Flows and",
        "reading their Runs. The CLI and the API call a Routine a *channel* and a",
        "Routine Template an *app*, and its commands keep those names.",
        "",
        f"These pages describe `popcorn` {version} and are generated from the CLI's own",
        "`popcorn --help` and `popcorn commands`. When they and the CLI you have",
        "disagree, the CLI is right: run `popcorn <command> --help`.",
        "",
        "## Install",
        "",
        "The CLI installs from its GitHub repository; it is not on PyPI.",
        "",
        "```",
        "# With uv (recommended)",
        f"uv tool install git+{REPO}",
        "",
        "# With pipx",
        f"pipx install git+{REPO}",
        "",
        "# With pip",
        f"pip install git+{REPO}",
        "```",
        "",
        "`popcorn --version` shows the version installed, and `popcorn upgrade`",
        "upgrades it to the latest. `popcorn doctor` checks the local setup: sign-in,",
        "whether the API is reachable, the environment and the config.",
        "",
        "## Sign in",
        "",
        "```",
        "popcorn auth login",
        "popcorn whoami",
        "```",
        "",
        "`popcorn auth login` signs in through the browser, then asks which Workspace",
        "to use; `--workspace <name>` chooses it instead. `popcorn whoami` shows who",
        "you are signed in as and in which Workspace, and `popcorn workspace switch`",
        "moves to another. A profile holds one sign-in: `-e <name>` uses a profile",
        "for one command, and `popcorn env <name>` switches to it. The",
        f"[auth](https://docs.popcorn.ai/{slug('auth')}.md) and [workspace](https://docs.popcorn.ai/{slug('workspace')}.md) have the rest.",
        "",
        "## Basics",
        "",
        "Each command is run as `popcorn <command>`, and the global flags go before",
        "the command, as in `popcorn --json app status`.",
        "",
        "### Global flags",
        "",
    ]
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
    out += [
        "",
        "## Command reference",
        "",
        f"[Commands](https://docs.popcorn.ai/{INDEX}.md) lists every command, A to Z, with a",
        f"page for each and its subcommands: {count} in all.",
    ]
    return "\n".join(out).rstrip() + "\n"


def commands_page(tops: list[tuple[dict, list[tuple[str, dict]]]], version: str) -> str:
    """The command reference's index: every top-level command A to Z, linking
    its page. Those pages are its children in the sidebar."""
    count = sum(len(cmds) for _, cmds in tops)
    out = header(
        id=INDEX,
        title="Commands",
        order=ORDER + 1,
        version=version,
        summary="The CLI's command reference: every command, A to Z, each on a page with "
                "its subcommands.",
        lede="Every command in the popcorn CLI, A to Z, each on its own page.",
        concepts=["cli"],
        lookup=True,
    )
    out += [
        f"Every command `popcorn` {version} lists in its help menu, A to Z: {count} with",
        "their subcommands. Each page shows the Usage line and arguments;",
        "`popcorn <command> --help` describes the one you have installed.",
        "",
    ]
    # One entry per command, so the page is a list like the pages under it:
    # its rail indexes the commands, and search reads it as a list.
    for top, _ in tops:
        out.append(f"- **[`{top['name']}`](https://docs.popcorn.ai/{href_of(top)})** — "
                   f"{cell(top.get('description') or '')}")
    return "\n".join(out).rstrip() + "\n"


def other_page(tops: list[dict], order: int, version: str) -> str:
    """The commands that have no subcommands, one entry each."""
    out = header(
        id=OTHER,
        title="Other commands",
        order=order,
        version=version,
        summary="The CLI's commands that have no subcommands, each with what it does, "
                "its Usage line and its arguments.",
        lede="The commands that have no subcommands, with how to run each and its arguments.",
        concepts=["cli"],
        lookup=True,
        parent=INDEX,
    )
    out += [
        f"The commands in `popcorn` {version} that have no subcommands.",
        "Global flags still go before them, as in `popcorn --json whoami`; the",
        "[CLI overview](https://docs.popcorn.ai/cli.md) page lists them.",
        "",
    ]
    for top in tops:
        out += [f"### `{top['name']}`", ""]
        if top.get("description"):
            out += [cell(top["description"]), ""]
        args = top.get("arguments") or []
        out += ["```", usage(top["name"], args), "```", ""]
        out += table(args)
    return "\n".join(out).rstrip() + "\n"


def pages(schema: dict, help_text: str) -> dict[pathlib.Path, str]:
    """Every CLI page, by the path it is written to. A command is listed when
    the help menu lists it, as before; the menu's headings no longer group
    the pages, which run A to Z."""
    version = schema["version"]
    by_name = {c["name"]: c for c in schema["commands"]}
    listed = sorted({c for _, cmds in menu(help_text) for c in cmds if c in by_name})
    tops = [(by_name[c], leaves(by_name[c])) for c in listed]
    out = {
        PAGE: landing(schema, tops, version),
        file_of(INDEX): commands_page(tops, version),
    }
    own = [(top, cmds) for top, cmds in tops if not bare(top)]
    for n, (top, cmds) in enumerate(own, 2):
        out[file_of(slug(top['name']))] = command_page(top, cmds, ORDER + n, version)
    others = [top for top, _ in tops if bare(top)]
    if others:
        out[file_of(OTHER)] = other_page(others, ORDER + len(own) + 2, version)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if any page differs, write nothing")
    args = ap.parse_args()

    wanted = pages(json.loads(run("commands")), run("--help"))
    stale = [p for p in (REFERENCE / "cli").rglob("*.md") if p not in wanted]
    changed = [p for p, text in wanted.items() if not p.exists() or p.read_text() != text]
    if args.check:
        for p in changed + stale:
            print(f"✖  {p.relative_to(ROOT)} is stale — run scripts/sync-cli.py", file=sys.stderr)
        if changed or stale:
            return 1
        print(f"✔  the {len(wanted)} CLI pages match the installed CLI")
        return 0
    if not changed and not stale:
        print(f"✔  the {len(wanted)} CLI pages already match the installed CLI — nothing to write")
        return 0
    for p in changed:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(wanted[p])
    for p in stale:
        p.unlink()
    commands = sum(text.count("\n### `") for text in wanted.values())
    print(f"✔  wrote {len(changed)} and removed {len(stale)} of the CLI pages ({commands} commands). "
          "Review the diff, then run the leak guard before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
