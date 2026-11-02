#!/usr/bin/env python3
"""Regenerate the Activity pages in `content/reference/` from the deployed catalog.

The reference is laid out like the CLI's: `activities.md` is the landing
page — what an Activity is, how a Flow Step calls one, the tiers and
statuses, the arguments every Activity takes, and how to list them. Under it,
three levels: the Activity Catalog (`activities-catalog.md`) indexes the
tiers, each published tier's page (`activities-<tier>.md`) indexes its
domains, and each domain has a page (`activities-<tier>-<domain>.md`) with
its activities. The sidebar nests them in that order. All of them sit in the
Reference tab's Activities section.

The activity reference is generated, never hand-written: the catalog derives
every activity's arguments from the model the activity accepts at runtime, so
a hand-kept copy is a second source that can only disagree with it. This
script reads the catalog from the DEPLOYED platform — prod, not backend main,
because the page describes what an author can call today, and main runs ahead
of what is released.

    python3 scripts/sync-activities.py               # fetch from prod, write the pages
    python3 scripts/sync-activities.py --check       # exit 1 if any page is stale
    python3 scripts/sync-activities.py --from DIR    # use saved <tier>.json files
    python3 scripts/sync-activities.py --from DIR --platform-version V

After each prod deploy the backend's deploy pipeline saves the catalog to a
directory and runs the last form with the deploy's version, then opens a pull
request here as the docs bot when a page changed. `--platform-version` sets
each page's `updated:` date; `platform_version.py` says when that line moves,
page by page. An `activities-*.md` page for a tier no longer published is
deleted.

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
import textwrap

import platform_version

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "content" / "reference"
PAGE = REFERENCE / "activities.md"
# Where the Activity pages sit among the reference pages: first, the landing
# page and then each tier.
ORDER = 100

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


def _placeholder(spec: dict) -> str:
    """A required argument's value in the Step example: its JSON type when it
    has a plain one, `...` otherwise — an enum or a nested type is in the table."""
    kind = spec.get("type")
    return f"<{kind}>" if isinstance(kind, str) and kind in ("string", "integer", "number", "boolean", "array", "object") else "..."


def step(a: dict) -> list[str]:
    """How a Flow Step calls the activity: its wire name and its required
    arguments, as `flow-grammar` writes a Step. Optional ones are in the table."""
    schema = a.get("args_schema") or {}
    props = schema.get("properties") or {}
    required = [n for n in props if n in set(schema.get("required") or []) and n not in BASE_ARGS]
    out = ["```yaml", "- id: <step>", f"  activity: {a['name']}"]
    if required:
        out.append("  args:")
        out += [f"    {n}: {_placeholder(props[n])}" for n in required]
    return out + ["```", ""]


def activity(a: dict) -> list[str]:
    # The status is kept out of the heading: the heading is the anchor, and a
    # link to an activity must not break the day it leaves beta.
    out = [f"### `{a['name']}`", ""]
    if a["status"] != "release":
        out += [f"*{a['status'].capitalize()}.*", ""]
    description = _prose(a.get("description"))
    out += [description or "No description in the catalog.", ""]
    out += step(a)
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


def header(*, id: str, title: str, order: int, summary: str, lede: str,
           concepts: list[str], lookup: bool, parent: str = "") -> list[str]:
    wrapped = lambda text: textwrap.wrap(text, 76, break_on_hyphens=False)
    return [
        "---",
        f"id: {id}",
        f"title: {title}",
        f"order: {order}",
        "group: Activities",
        *([f"parent: {parent}"] if parent else []),
        *(["layout: lookup"] if lookup else []),
        "summary: >",
        *(f"  {line}" for line in wrapped(summary)),
        "lede: >",
        *(f"  {line}" for line in wrapped(lede)),
        f"concepts: [{', '.join(concepts)}]",
        "---",
        "",
    ]


# Each tier page's title, summary and lede. No activity names and no domain
# words in the summaries: an activity is reached as this page's entry, which
# search matches by its wire name, and a domain word in a summary would make
# the tier page outrank the written page about that thing.
TIER_PAGES = {
    "foundation": (
        "Foundation activities",
        "The foundation tier: the platform operations every Flow is built from, "
        "each with the Step that calls it, its arguments and what it returns.",
        "The platform operations every Flow is built from, with their arguments and results.",
    ),
    "feature": (
        "Feature activities",
        "The feature tier: operations that build on the foundation tier for one "
        "product capability each, with the Step that calls each, its arguments "
        "and what it returns.",
        "Operations for one product capability each, with their arguments and results.",
    ),
}


def slug(tier: str) -> str:
    return f"activities-{tier}"


def domain(a: dict) -> str:
    return a["name"].rsplit(".", 1)[0]


def domain_slug(name: str) -> str:
    """A domain's page id: `foundation.store` → `activities-foundation-store`."""
    return "activities-" + name.replace(".", "-")


def tier_page(tier: str, acts: list[dict], order: int) -> str:
    """A tier's index: one entry per domain, linking its page. The domain
    pages are its children in the sidebar, as it is the catalog's."""
    title, summary, lede = TIER_PAGES[tier]
    out = header(id=slug(tier), title=title, order=order, summary=summary, lede=lede,
                 concepts=["activities", "flow-grammar"], lookup=True, parent=CATALOG)
    out += [
        f"The {len(acts)} `{tier}` activities at `release` or `beta` status, a page for",
        "each domain. Each activity also takes the optional `integration_id` and",
        "`integration_name` arguments, which the",
        "[Activities](https://docs.popcorn.ai/activities.md) page explains with the",
        "rest of what every activity shares.",
        "",
    ]
    for name, in_domain in domains(acts).items():
        out.append(f"- **[`{name}`](https://docs.popcorn.ai/{domain_slug(name)}.md)** — "
                   f"{len(in_domain)} {'activity' if len(in_domain) == 1 else 'activities'}")
    return "\n".join(out).rstrip() + "\n"


def domains(acts: list[dict]) -> dict[str, list[dict]]:
    """The activities by domain, in catalog order."""
    out: dict[str, list[dict]] = {}
    for a in acts:
        out.setdefault(domain(a), []).append(a)
    return out


def domain_page(name: str, tier: str, acts: list[dict], order: int) -> str:
    """One domain's activities, each with the Step that calls it, its
    arguments and what it returns."""
    out = header(
        id=domain_slug(name),
        title=name,
        order=order,
        # The domain is in the title already; said again here it would count
        # twice for any question sharing its word ("email", "channel").
        summary="One domain's activities, each with the Step that calls it, its "
                "arguments and what it returns.",
        lede=f"The {name} activities, with how a Step calls each and its arguments.",
        concepts=["activities", "flow-grammar"],
        lookup=True,
        parent=slug(tier),
    )
    out += [
        f"The `{name}` activities at `release` or `beta` status; `beta` ones are",
        "marked. Each also takes the optional `integration_id` and",
        "`integration_name` arguments, which the",
        "[Activities](https://docs.popcorn.ai/activities.md) page explains.",
        "",
    ]
    for a in acts:
        out += activity(a)
    return "\n".join(out).rstrip() + "\n"


def landing(acts: list[dict]) -> str:
    counts = {t: sum(1 for a in acts if a["tier"] == t) for t in TIERS}
    out = header(
        id="activities",
        title="Activities",
        order=ORDER,
        summary="An Activity is a platform operation a Flow Step calls by its wire name, "
                "such as foundation.store.upsert_rows, with its arguments under `args:`. "
                "Every one also takes integration_id or integration_name, the connected "
                "account the step runs as. The Activity Catalog lists the foundation and "
                "feature tiers at release or beta status; `popcorn flow activities` lists "
                "alpha and deprecated ones too.",
        lede="What an Activity is, how a Flow Step calls one, and where each tier's are listed.",
        concepts=["flow-grammar", "app-bundle", "template-authoring"],
        lookup=False,
    )
    out += [
        "An Activity is a platform operation a Flow Step calls. A Step names one by",
        "its wire name in `activity:` and passes its arguments in `args:`:",
        "",
        "```yaml",
        "- id: fetch",
        "  activity: foundation.store.list_rows",
        "  args: { ... }",
        "```",
        "",
        "These pages are generated from the catalog the platform serves, which",
        "derives every argument list from the model the activity accepts at",
        "runtime — so where they and a hand-written example disagree, they are",
        "right. They are regenerated by `scripts/sync-activities.py` after each prod",
        "deploy and never edited by hand; a date beside a title is the day of the",
        "deploy that last changed that page.",
        "",
        "## Names, tiers and status",
        "",
        "A wire name is `<tier>.<domain>.<verb>`, sometimes with more segments",
        "before the verb. These pages list two tiers: `foundation`, the platform",
        "operations every Flow is built from, and `feature`, operations that build",
        "on them for one product capability each. `app` activities belong to",
        "individual shipped apps and `system` ones to the platform itself, so",
        "neither is listed here.",
        "",
        f"They list the {counts['foundation']} `foundation` and {counts['feature']} `feature`",
        "activities at `release` or `beta` status; `beta` ones are marked. `alpha`",
        "and `deprecated` ones are not what a new Flow should reach for, and are",
        "left out.",
        "",
        "## Arguments every activity takes",
        "",
        "Every activity also accepts two optional arguments not repeated on its",
        "entry: `integration_id`, the connected account to run the step against —",
        "normally `$channel.integrations.<name>.id` — and `integration_name`, a named",
        "channel integration to resolve instead. Omit both for steps that touch no",
        "user account.",
        "",
        "## Listing them",
        "",
        "The CLI lists the whole catalog, every tier and status included:",
        "",
        "```",
        "popcorn flow activities --summary",
        "popcorn flow activities --name <wire.name>",
        "popcorn --json flow activities",
        "```",
        "",
        "`--name` shows one activity with its full JSON schemas.",
        "",
        "## The Activity Catalog",
        "",
        f"The [Activity Catalog](https://docs.popcorn.ai/{CATALOG}.md) lists every activity a Flow",
        "can call, a page for each tier.",
    ]
    return "\n".join(out).rstrip() + "\n"


# The tier pages' parent: the catalog `popcorn flow activities` lists, which
# the sidebar opens to show them while the reader is in it.
CATALOG = "activities-catalog"


def catalog_page(acts: list[dict]) -> str:
    """The catalog's index: one row per tier, linking its page and naming its
    domains. The tier pages are its children in the sidebar."""
    out = header(
        id=CATALOG,
        title="Activity Catalog",
        order=ORDER + 1,
        summary="The Activity Catalog: every activity a Flow can call at release or beta "
                "status, on a page for each tier.",
        lede="Every activity a Flow can call, a page for each tier.",
        concepts=["activities", "flow-grammar"],
        lookup=True,
    )
    out += [
        f"The {len(acts)} activities a Flow can call at `release` or `beta` status, a page",
        "for each tier. `popcorn flow activities` lists the same catalog from the",
        "platform you are signed in to.",
        "",
    ]
    # One entry per tier, so the page is a list like the pages under it. The
    # tier's page lists its domains; repeating them here would make this page
    # a second index of the same thing.
    for tier in TIERS:
        count = sum(1 for a in acts if a["tier"] == tier)
        if count:
            title, _, lede = TIER_PAGES[tier]
            out.append(f"- **[{title}](https://docs.popcorn.ai/{slug(tier)}.md)** — "
                       f"{lede.rstrip('.')} ({count} activities).")
    return "\n".join(out).rstrip() + "\n"


def pages(acts: list[dict]) -> dict[pathlib.Path, str]:
    """Every Activity page, freshly generated without an `updated:` line, by path."""
    out = {PAGE: landing(acts), REFERENCE / f"{CATALOG}.md": catalog_page(acts)}
    order = ORDER + 2
    for tier in TIERS:
        tier_acts = [a for a in acts if a["tier"] == tier]
        if not tier_acts:
            continue
        out[REFERENCE / f"{slug(tier)}.md"] = tier_page(tier, tier_acts, order)
        order += 1
    # The domain pages follow every tier page, so each tier's index comes
    # before the pages under it in reading order.
    for tier in TIERS:
        for name, in_domain in domains([a for a in acts if a["tier"] == tier]).items():
            out[REFERENCE / f"{domain_slug(name)}.md"] = domain_page(name, tier, in_domain, order)
            order += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env", default="prod", help="CLI environment to read (default: prod)")
    ap.add_argument("--from", dest="source", type=pathlib.Path,
                    help="read <tier>.json files from this directory instead of the CLI")
    ap.add_argument("--check", action="store_true", help="exit 1 if any page differs, write nothing")
    platform_version.add_argument(ap)
    args = ap.parse_args()

    wanted = {}
    for path, text in pages(load(args.source, args.env)).items():
        current = path.read_text() if path.exists() else ""
        wanted[path] = platform_version.stamp(text, current, args.platform)
    stale = [p for p in REFERENCE.glob("activities-*.md") if p not in wanted]
    changed = [p for p, text in wanted.items() if not p.exists() or p.read_text() != text]
    if args.check:
        for p in changed + stale:
            print(f"✖  {p.relative_to(ROOT)} is stale — run scripts/sync-activities.py", file=sys.stderr)
        if changed or stale:
            return 1
        print(f"✔  the {len(wanted)} Activity pages match the catalog")
        return 0
    if not changed and not stale:
        print(f"✔  the {len(wanted)} Activity pages already match the catalog — nothing to write")
        return 0
    for p in changed:
        p.write_text(wanted[p])
    for p in stale:
        p.unlink()
    n = sum(text.count("\n### ") for text in wanted.values())
    print(f"✔  wrote {len(changed)} and removed {len(stale)} of the Activity pages ({n} activities). "
          "Review the diff, then run the leak guard before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
