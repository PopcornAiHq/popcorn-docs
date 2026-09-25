#!/usr/bin/env python3
"""Regenerate `content/reference/activities.md` from the deployed activity catalog.

The activity reference is generated, never hand-written: the catalog derives
every activity's arguments from the model the activity accepts at runtime, so
a hand-kept copy is a second source that can only disagree with it. This
script reads the catalog from the DEPLOYED platform — prod, not backend main,
because the page describes what an author can call today, and main runs ahead
of what is released.

    python3 scripts/sync-activities.py               # fetch from prod, write the page
    python3 scripts/sync-activities.py --check       # exit 1 if the page is stale
    python3 scripts/sync-activities.py --from DIR    # use saved <tier>.json files

It shells out to the `popcorn` CLI rather than calling the API itself, so it
runs on the credentials the author already has and needs no token of its own.
`-e prod` is passed explicitly: the CLI's current environment is whatever was
last switched to, and a reference generated from dev would describe activities
that are not deployed.

Only `foundation` and `feature` activities at `release` or `beta` are
published. `app` activities belong to individual shipped apps, `system` ones
to the platform itself, and `alpha` and `deprecated` are not what a new flow
should reach for; `popcorn flow activities` lists everything.

The output is deterministic — sorted, no timestamps — so a run with nothing
changed produces no diff, and a run with something changed produces exactly
that change for review. Descriptions come from backend docstrings, which can
carry internal references a public page must not; the leak guard runs on the
generated page like any other, and the fix for a hit is the docstring, not
this script.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "content" / "reference" / "activities.md"

TIERS = ("foundation", "feature")
STATUSES = ("release", "beta")

# Every activity input inherits these two from the shared base model, with the
# same description each time. Explained once at the top instead of repeated in
# every table.
BASE_ARGS = ("integration_id", "integration_name")


def fetch(tier: str, env: str) -> list[dict]:
    cmd = ["popcorn", "-e", env, "--json", "flow", "activities", "--tier", tier]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("✖  the `popcorn` CLI is not installed — it is how this reads the catalog")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"✖  {' '.join(cmd)} failed:\n{exc.stderr.strip()}")
    return _activities(json.loads(out))


def _activities(doc: dict) -> list[dict]:
    """The CLI wraps the API response in `{ok, data}`; saved files may be either."""
    return (doc.get("data") or doc).get("activities", [])


def load(source: pathlib.Path | None, env: str) -> list[dict]:
    acts = []
    for tier in TIERS:
        if source:
            path = source / f"{tier}.json"
            if not path.exists():
                sys.exit(f"✖  {path} missing — --from expects one <tier>.json per tier")
            acts += _activities(json.loads(path.read_text()))
        else:
            acts += fetch(tier, env)
    public = [a for a in acts if a.get("tier") in TIERS and a.get("status") in STATUSES]
    if not public:
        sys.exit("✖  the catalog returned no public activities — refusing to write an empty page")
    # Foundation first: it is what every flow is built from, and the feature
    # tier builds on it.
    return sorted(public, key=lambda a: (TIERS.index(a["tier"]), a["name"]))


# --- rendering -------------------------------------------------------------

def _prose(text: str) -> str:
    """A docstring as Markdown: reST ``code`` becomes `code`, nothing else moves."""
    return re.sub(r"``([^`]+)``", r"`\1`", text or "").strip()


def _cell(text: str) -> str:
    """One table cell: a single line, and no `|` — the table syntax owns it."""
    return " ".join(_prose(text).split()).replace("|", "/")


def _type(schema: dict) -> str:
    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[-1]
    if "anyOf" in schema:
        kinds = [_type(s) for s in schema["anyOf"]]
        optional = "null" in kinds
        kinds = [k for k in kinds if k != "null"]
        joined = " or ".join(dict.fromkeys(kinds)) or "null"
        return f"{joined}, optional" if optional else joined
    if "enum" in schema:
        return " / ".join(f"`{v}`" for v in schema["enum"])
    kind = schema.get("type", "any")
    if kind == "array":
        return f"list of {_type(schema.get('items', {}))}"
    if kind == "object" and "additionalProperties" in schema and isinstance(schema["additionalProperties"], dict):
        return f"map of {_type(schema['additionalProperties'])}"
    return kind


def _fields(schema: dict, *, args: bool) -> list[str]:
    props = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    rows = []
    for name, spec in props.items():
        if args and name in BASE_ARGS:
            continue
        note = _cell(spec.get("description", ""))
        if args and "default" in spec and spec["default"] is not None:
            default = json.dumps(spec["default"])
            note = f"{note} Default `{default}`.".strip()
        need = "yes" if name in required else "no"
        if args:
            rows.append(f"| `{name}` | {_cell(_type(spec))} | {need} | {note} |")
        else:
            rows.append(f"| `{name}` | {_cell(_type(spec))} | {note} |")
    if not rows:
        return []
    head = (["| Argument | Type | Required | Notes |", "|---|---|---|---|"] if args
            else ["| Field | Type | Notes |", "|---|---|---|"])
    return head + rows


def _types(schemas: list[dict]) -> list[str]:
    """Named sub-types (`$defs`) the arguments or result refer to, one table each."""
    defs: dict[str, dict] = {}
    for schema in schemas:
        defs.update(schema.get("$defs") or {})
    out = []
    for name in sorted(defs):
        spec = defs[name]
        table = _fields(spec, args=False)
        if not table and "enum" in spec:
            out += [f"`{name}` is one of {_type(spec)}.", ""]
            continue
        if table:
            out += [f"`{name}`:", ""] + table + [""]
    return out


def activity(a: dict) -> list[str]:
    # The status is kept out of the heading: the heading is the anchor, and a
    # link to an activity must not break the day it leaves beta.
    out = [f"### `{a['name']}`", ""]
    if a["status"] != "release":
        out += [f"*{a['status'].capitalize()}.*", ""]
    description = _prose(a.get("description"))
    out += [description or "No description in the catalog.", ""]
    args = _fields(a.get("args_schema") or {}, args=True)
    out += (["**Arguments**", ""] + args + [""]) if args else ["Takes no arguments of its own.", ""]
    result = _fields(a.get("result_schema") or {}, args=False)
    if result:
        out += ["**Returns**", ""]
        if a.get("result_description"):
            out += [_prose(a["result_description"]), ""]
        out += result + [""]
    out += _types([a.get("args_schema") or {}, a.get("result_schema") or {}])
    return out


def page(acts: list[dict]) -> str:
    counts = {t: sum(1 for a in acts if a["tier"] == t) for t in TIERS}
    head = [
        "---",
        "id: activities",
        "title: Activities",
        "order: 1",
        "layout: lookup",
        "summary: >",
        "  Every foundation and feature activity a flow step can call at release or",
        "  beta status, with its arguments and what it returns — generated from the",
        "  deployed catalog. Look an activity up here by its wire name, such as",
        "  foundation.store.upsert_rows; `popcorn flow activities` lists alpha and",
        "  deprecated ones too.",
        "concepts: [app-bundle, template-authoring]",
        "applies_to: [cli, mcp, human]",
        "---",
        "",
        "A flow step names one of these by its wire name in `activity:` and passes",
        "its arguments in `args:`. This page is generated from the catalog the",
        "platform serves, which derives every argument list from the model the",
        "activity accepts at runtime — so where this page and a hand-written example",
        "disagree, this page is right. It is regenerated by `scripts/sync-activities.py`",
        "and never edited by hand.",
        "",
        f"It lists the {counts['foundation']} `foundation` and {counts['feature']} `feature`",
        "activities at `release` or `beta` status. `beta` ones are marked. For",
        "`alpha`, `deprecated`, and app-specific activities, and for the full JSON",
        "schemas, ask the CLI: `popcorn flow activities --name <wire.name>`.",
        "",
        "Every activity also accepts two optional arguments not repeated below:",
        "`integration_id`, the connected account to run the step against — normally",
        "`$channel.integrations.<name>.id` — and `integration_name`, a named channel",
        "integration to resolve instead. Omit both for steps that touch no user",
        "account.",
        "",
    ]
    body = []
    category = None
    for a in acts:
        group = a["name"].rsplit(".", 1)[0]
        if group != category:
            category = group
            body += [f"## {group}", ""]
        body += activity(a)
    return "\n".join(head + body).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env", default="prod", help="CLI environment to read (default: prod)")
    ap.add_argument("--from", dest="source", type=pathlib.Path,
                    help="read <tier>.json files from this directory instead of the CLI")
    ap.add_argument("--check", action="store_true", help="exit 1 if the page differs, write nothing")
    args = ap.parse_args()

    text = page(load(args.source, args.env))
    current = PAGE.read_text() if PAGE.exists() else ""
    if args.check:
        if text != current:
            print(f"✖  {PAGE.relative_to(ROOT)} is stale — run scripts/sync-activities.py", file=sys.stderr)
            return 1
        print(f"✔  {PAGE.relative_to(ROOT)} matches the catalog")
        return 0
    if text == current:
        print(f"✔  {PAGE.relative_to(ROOT)} already matches the catalog — nothing to write")
        return 0
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(text)
    n = text.count("\n### ")
    print(f"✔  wrote {PAGE.relative_to(ROOT)}: {n} activities. Review the diff, then run the leak guard before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
