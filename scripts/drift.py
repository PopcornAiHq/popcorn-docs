#!/usr/bin/env python3
"""Check the concept pages against a local checkout of the backend.

Each page's backend symbols — the names that implement what it describes —
are listed in a mapping kept in the private backend repository, keyed by page
id. They are private names, so no page here carries them; `check-content.py`
refuses a `source:` field. The backend's own CI fails when a listed symbol
loses its definition. That is not the same as the page still being right: a
citation nobody re-reads decays at the rate the code moves.

Three subcommands, one script, because all three start from the same two
steps — read a page's list from the mapping, then find where each symbol is
defined — and three scripts would carry three copies of the lookup that could
disagree about what "defined" means:

    python3 scripts/drift.py sources          # every cited symbol exists
    python3 scripts/drift.py changes          # backend commits since each page
    python3 scripts/drift.py packet <id> ...  > /elsewhere/packet.md
    python3 scripts/drift.py packet --all     > /elsewhere/packets.md

`sources` is a hard check: it exits 1 on a symbol with no definition, or on a
mapping entry for a page id that does not exist here — a renamed or deleted
page whose entry did not follow it. It says nothing about behaviour — a symbol can exist and do the opposite of what the
page says. `changes` narrows that down to the pages worth re-reading: the
backend commits, since the page last changed, to the files that define what it
cites. It is a review list, not a verdict, so it always exits 0 — and it is
only as wide as the mapping. A change to code no page cites, such as a new
endpoint beside a cited function, reaches `changes` only if it shares a file
with something cited, and the pages it contradicts may not be the pages
flagged. `packet`
assembles what a model needs to do the re-reading: the page, every cited
definition in full, and the instructions to list what the code contradicts.

**These run locally only.** The backend repository is private, so CI cannot
check it out; the checkout is read from `$POPCORN_BACKEND`, defaulting to
`$HOME/popcorn/backend`. With no checkout there, every subcommand prints a
notice and exits 0, so wiring one into a CI job cannot turn it red. Every
subcommand prints private symbol names, `changes` and `packet` print private
source paths, and `packet` reproduces private source — redirect the output
outside this repository, never into `build/`, which is published whole.

The mapping is found by content, not by path: it is the one tracked `.toml`
in the backend with a `[docs_sources]` table, whose keys are page ids and
whose values are lists of symbols. That keeps a private path out of this
public script.

A definition is a `def` or `class` at any depth (methods count), or an
assignment or annotated name in a module or class body — the forms a reader
searching for the name would accept as "where it lives". Assignments inside a
function are locals, not definitions. Test files are skipped: a fake with the
real name must not stand in for a symbol production code removed. The lookup
parses Python with `ast`, which gives the exact extent of a definition,
decorators included; a file this interpreter's grammar cannot parse falls back
to matching the line and taking the indented block beneath it. The backend's
CI check applies the same rules; change the two together.
"""

from __future__ import annotations

import argparse
import ast
import os
import pathlib
import re
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DEFAULT_BACKEND = pathlib.Path.home() / "popcorn" / "backend"

# Commits shown per file in `changes`. A file that churns daily would otherwise
# bury every other page; the count of the rest still says it moved.
COMMITS_SHOWN = 5

# Where a symbol may be defined. Tests are excluded for the reason in the
# module docstring: a test's stand-in is not the implementation.
# `glob` magic lets `**/` match zero directories, so a repo-root conftest.py
# is excluded too.
PATHSPEC = [
    "*.py",
    ":(exclude,glob)**/tests/**",
    ":(exclude,glob)**/test_*.py",
    ":(exclude,glob)**/conftest.py",
    ":(exclude,glob)integration_tests/**",
]

# The mapping's table, which is also how it is found — see the docstring.
TABLE = "docs_sources"

sys.path.insert(0, str(ROOT / "scripts"))
from emit import parse  # noqa: E402 — the frontmatter reader the build uses


# ── the backend ─────────────────────────────────────────────────────────────


def backend() -> pathlib.Path | None:
    path = pathlib.Path(os.environ.get("POPCORN_BACKEND") or DEFAULT_BACKEND).expanduser()
    if (path / ".git").exists() and git(path, "rev-parse", "--git-dir", check=False) is not None:
        return path
    print(
        f"–  skipped: no backend checkout at {path}. These checks read the "
        "private backend and run locally only; set POPCORN_BACKEND to point at one.",
        file=sys.stderr,
    )
    return None


def git(repo: pathlib.Path, *args: str, check: bool = True) -> str | None:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    # `git grep` exits 1 for "no match", which is an answer, not a failure.
    if not check or (args and args[0] == "grep" and result.returncode == 1):
        return None
    sys.exit(f"✖  git {' '.join(args[:2])} failed in {repo}: {result.stderr.strip()}")


def mapping(repo: pathlib.Path) -> dict[str, list[str]]:
    """Page id → the backend symbols behind it, from the backend's mapping."""
    pattern = rf"^\[{TABLE}\][[:space:]]*$"
    listed = (git(repo, "grep", "-lE", "-e", pattern, "--", "*.toml") or "").split()
    if len(listed) != 1:
        sys.exit(
            f"✖  expected one tracked .toml with a [{TABLE}] table in the backend "
            f"checkout at {repo}, found {len(listed)}. Is the checkout up to date?"
        )
    try:
        table = tomllib.loads((repo / listed[0]).read_text())[TABLE]
    except (tomllib.TOMLDecodeError, KeyError) as exc:
        sys.exit(f"✖  the backend's [{TABLE}] mapping does not parse: {exc}")
    return {page: list(symbols) for page, symbols in table.items()}


class Definition:
    def __init__(self, path: str, start: int, end: int, lines: list[str]):
        self.path, self.start, self.end = path, start, end
        self.text = "\n".join(lines[start - 1 : end])


def _ast_definitions(symbol: str, tree: ast.AST) -> list[tuple[int, int]]:
    """(first line, last line) of every definition of `symbol` in `tree`."""
    found: list[tuple[int, int]] = []

    def visit(node: ast.AST, in_function: bool) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if child.name == symbol:
                    first = min([d.lineno for d in child.decorator_list] + [child.lineno])
                    found.append((first, child.end_lineno))
                visit(child, in_function or not isinstance(child, ast.ClassDef))
                continue
            if not in_function and isinstance(child, (ast.Assign, ast.AnnAssign)):
                targets = child.targets if isinstance(child, ast.Assign) else [child.target]
                names = [n.id for t in targets for n in ast.walk(t) if isinstance(n, ast.Name)]
                if symbol in names:
                    found.append((child.lineno, child.end_lineno))
            if isinstance(child, ast.stmt):
                visit(child, in_function)

    visit(tree, False)
    return found


def _line_definitions(symbol: str, lines: list[str]) -> list[tuple[int, int]]:
    """The fallback for a file `ast` cannot parse: match the line, then take
    every following line indented deeper than it (blank lines included)."""
    head = re.compile(
        rf"^(?P<indent>\s*)(?:(?:async\s+)?def\s+{symbol}\b|class\s+{symbol}\b|{symbol}\s*[:=])"
    )
    found = []
    for i, line in enumerate(lines):
        match = head.match(line)
        if not match:
            continue
        indent, end = len(match.group("indent")), i
        for j in range(i + 1, len(lines)):
            if lines[j].strip() and len(lines[j]) - len(lines[j].lstrip()) <= indent:
                break
            if lines[j].strip():
                end = j
        found.append((_decorated_from(lines, i, indent) + 1, end + 1))
    return found


def _decorated_from(lines: list[str], i: int, indent: int) -> int:
    """The first line of the decorators above line `i`, or `i` itself.

    The AST path counts decorators as part of a definition, and the `mcp:`
    check depends on it. This fallback is the common path, not a rare one: the
    backend is written for a newer Python than this repo runs, so many of its
    files do not parse here. Walk up through lines that are a decorator, a
    decorator's continuation (indented deeper) or its closing bracket, and keep
    the block only if its top line is a decorator.
    """
    top = i
    for k in range(i - 1, -1, -1):
        text = lines[k]
        if not text.strip():
            break
        depth = len(text) - len(text.lstrip())
        stripped = text.strip()
        if depth == indent and stripped.startswith("@"):
            top = k
        elif depth > indent or (depth == indent and stripped[:1] in ")]}"):
            continue
        else:
            break
    return top


# A citation written `mcp:<name>` means the hosted MCP server's tool of that
# name: a function registered with an `@<server>.tool` decorator. The product
# pages describe tools by name, and several tool names are also ordinary
# functions elsewhere in the backend, so a bare name would go on resolving
# after the tool was renamed. The backend's own check also confines tools to
# the server's directory; this one goes by the decorator alone, so the public
# repo names no backend path.
MCP_PREFIX = "mcp:"
_TOOL_DECORATOR = re.compile(r"^\s*@\w+\.tool\b", re.M)


def locate(repo: pathlib.Path, symbol: str, cache: dict) -> list[Definition]:
    """Every definition of `symbol` in the backend's tracked, non-test Python.

    `git grep -w` narrows the tree to the files that mention the name at all;
    only those are parsed, which is what keeps a full `sources` run quick.
    """
    if symbol in cache:
        return cache[symbol]
    if symbol.startswith(MCP_PREFIX):
        found = [
            d for d in locate(repo, symbol[len(MCP_PREFIX):], cache)
            if _TOOL_DECORATOR.search(d.text)
        ]
        cache[symbol] = found
        return found
    listed = git(repo, "grep", "-lwI", "-e", symbol, "--", *PATHSPEC) or ""
    found = []
    for rel in listed.split():
        text = (repo / rel).read_text(errors="replace")
        lines = text.splitlines()
        try:
            spans = _ast_definitions(symbol, ast.parse(text))
        except SyntaxError:
            spans = _line_definitions(symbol, lines)
        found += [Definition(rel, a, b, lines) for a, b in spans]
    cache[symbol] = found
    return found


# ── the pages ───────────────────────────────────────────────────────────────


def pages(cited: dict[str, list[str]]) -> list[tuple[pathlib.Path, dict, list[str]]]:
    """Every page, its frontmatter, and the symbols the mapping lists for it."""
    files = sorted(p for p in CONTENT.rglob("*.md") if not p.name.startswith("_"))
    out = []
    for p in files:
        meta = parse(p)
        out.append((p, meta, cited.get(meta["id"], [])))
    return out


def page_date(path: pathlib.Path) -> str | None:
    """When the page last changed in this repository — the moment it was last
    true to someone's reading of the backend, at best."""
    out = git(ROOT, "log", "-1", "--format=%cI", "--", str(path.relative_to(ROOT)))
    return out.strip() or None


# ── subcommands ─────────────────────────────────────────────────────────────


def cmd_sources(repo: pathlib.Path, _args) -> int:
    cited = mapping(repo)
    found = pages(cited)
    cache: dict = {}
    missing: list[tuple[str, str]] = []
    checked = 0
    for path, _meta, symbols in found:
        for symbol in symbols:
            checked += 1
            if not locate(repo, symbol, cache):
                missing.append((str(path.relative_to(ROOT)), symbol))
    orphans = sorted(set(cited) - {meta["id"] for _, meta, _ in found})

    if orphans:
        print(f"\n✖  the backend's mapping lists {len(orphans)} page id(s) with no page here:")
        for page in orphans:
            print(f"     {page}")
        print("\n   A page was renamed or deleted; move or drop its entry in the mapping.\n")
    if missing:
        print(f"\n✖  {len(missing)} cited symbol(s) have no definition in the backend:")
        for page, symbol in missing:
            print(f"     {page} → {symbol}")
        print(
            "\n   Search the backend for what the page means and cite that name in the "
            "mapping\n   (in the backend repo), or drop it — see \"Checking the pages "
            "against the backend\"\n   in README.md.\n"
        )
    if orphans or missing:
        return 1
    print(f"✔  {checked} cited symbols all have a definition in the backend")
    return 0


def cmd_changes(repo: pathlib.Path, _args) -> int:
    cache: dict = {}
    flagged = 0
    found = pages(mapping(repo))
    for path, _meta, symbols in found:
        since = page_date(path)
        if not symbols or not since:
            continue
        # File → the cited symbols it defines, so a file defining two of them
        # lists its commits once.
        files: dict[str, list[str]] = {}
        for symbol in symbols:
            for d in locate(repo, symbol, cache):
                files.setdefault(d.path, [])
                if symbol not in files[d.path]:
                    files[d.path].append(symbol)

        report = []
        for rel, defined in sorted(files.items()):
            log = git(repo, "log", "--no-merges", f"--since={since}",
                      "--date=short", "--format=%h %ad %s", "--", rel) or ""
            commits = log.splitlines()
            if not commits:
                continue
            report.append(f"   {', '.join(defined)} → {rel}")
            report += [f"       {c}" for c in commits[:COMMITS_SHOWN]]
            if len(commits) > COMMITS_SHOWN:
                report.append(f"       … and {len(commits) - COMMITS_SHOWN} more")
        if report:
            flagged += 1
            print(f"\n●  {path.relative_to(ROOT)}  (page last changed {since[:10]})")
            print("\n".join(report))

    total = sum(1 for _, _, symbols in found if symbols)
    print(f"\n✔  {flagged} of {total} pages with mapped symbols cite backend files "
          "changed after the page itself last did — re-read those; `packet` helps")
    return 0


PACKET_BRIEF = """\
You are fact-checking one page of public documentation against the backend
source that implements it. The page is below, followed by the full definition
of every symbol it cites. Treat the code as the truth.

1. List every claim in the page that the code contradicts. For each: quote the
   claim exactly, cite the code (file and the lines or names that show it), and
   say in one sentence what is actually true.
2. List important behaviour the page omits — something a reader acting on the
   page would get wrong without it. Omissions of internal detail that would not
   change what a reader does are not worth listing.
3. List any claim you could not check because the code it depends on is not
   included here, so a person knows where to look next.

Do not rewrite the page. If nothing is contradicted, say so plainly.
"""


def packet(repo: pathlib.Path, path: pathlib.Path, meta: dict, symbols: list[str],
           head: str, cache: dict) -> str:
    out = [
        f"# Fact-check packet — `{meta['id']}`",
        "",
        f"Backend HEAD: `{head}`",
        "",
        "## Instructions",
        "",
        PACKET_BRIEF,
        f"## The page — {path.relative_to(ROOT)}",
        "",
        "`````markdown",
        path.read_text().rstrip("\n"),
        "`````",
        "",
        "## Cited source",
        "",
    ]
    if not symbols:
        out += ["The page cites no symbols, so there is no code to check it against.", ""]
    for symbol in symbols:
        found = locate(repo, symbol, cache)
        if not found:
            out += [f"### `{symbol}` — NO DEFINITION FOUND", "",
                    "The page cites a name the backend does not define. Say so in your answer.", ""]
            print(f"   ✖ {meta['id']}: {symbol} has no definition", file=sys.stderr)
        for d in found:
            out += [f"### `{symbol}` — {d.path}:{d.start}-{d.end} @ {head[:12]}", "",
                    "```python", d.text, "```", ""]
    return "\n".join(out)


def cmd_packet(repo: pathlib.Path, args) -> int:
    by_id = {meta["id"]: (path, meta, symbols) for path, meta, symbols in pages(mapping(repo))}
    if args.all:
        wanted = list(by_id)
    elif args.ids:
        unknown = [i for i in args.ids if i not in by_id]
        if unknown:
            sys.exit(f"✖  no such page: {', '.join(unknown)}")
        wanted = args.ids
    else:
        sys.exit("✖  name one or more page ids, or pass --all")

    head = (git(repo, "rev-parse", "HEAD") or "").strip()
    cache: dict = {}
    packets = [packet(repo, *by_id[i], head, cache) for i in wanted]
    print("\n\n---\n\n".join(packets))
    print(f"✔  {len(packets)} packet(s) against backend {head[:12]}", file=sys.stderr)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("sources", help="every cited symbol has a definition (exit 1 if not)")
    sub.add_parser("changes", help="backend commits since each page last changed")
    p = sub.add_parser("packet", help="a fact-check packet per page, to stdout")
    p.add_argument("ids", nargs="*", help="page ids")
    p.add_argument("--all", action="store_true", help="every page")
    args = ap.parse_args()

    repo = backend()
    if repo is None:
        return 0
    return {"sources": cmd_sources, "changes": cmd_changes, "packet": cmd_packet}[args.command](repo, args)


if __name__ == "__main__":
    sys.exit(main())
