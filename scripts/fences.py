"""Generated regions inside a hand-written page.

An index or landing page in `content/reference/` is mostly prose a person
writes — what the list is, how to read it — around data a sync script
derives: the tools A to Z, the CLI's global flags, the tiers of the activity
catalog. The prose lives in the page, where it is edited and previewed like
any other Markdown, and the script owns only what sits between a pair of
markers:

    <!-- generated: tools -->
    …written by the script…
    <!-- /generated -->

The script reads the page, replaces each region it knows by name, and leaves
every other byte alone. A region it does not know, or one it knows and the
page lacks, stops the sync rather than dropping content: a renamed region
must be renamed in both places. Such a page still carries `generated:`,
naming the script, since part of it is that script's.

The markers never reach a reader: `emit.py` removes them before rendering,
so neither the site nor a page's Markdown twin shows them.
"""

from __future__ import annotations

import re

_REGION = re.compile(
    r"^<!-- generated: (?P<name>[a-z][a-z0-9-]*) -->\n(?P<body>.*?)^<!-- /generated -->$",
    re.M | re.S,
)
_MARKER = re.compile(r"^<!-- (?:generated: [a-z][a-z0-9-]*|/generated) -->\n?", re.M)


def names(page: str) -> list[str]:
    """The regions a page has, in order."""
    return [m.group("name") for m in _REGION.finditer(page)]


def fill(page: str, regions: dict[str, str], where: str) -> str:
    """The page with each region's body replaced by `regions[name]`.

    `where` names the page in an error. The page must have exactly the
    regions given, each once.
    """
    found = names(page)
    if sorted(found) != sorted(regions) or len(set(found)) != len(found):
        raise SystemExit(
            f"✖  {where} has generated regions {found}, and the script writes "
            f"{sorted(regions)} — rename or add the markers so they match"
        )

    def body(m: re.Match) -> str:
        text = regions[m.group("name")].strip("\n")
        return f"<!-- generated: {m.group('name')} -->\n{text}\n<!-- /generated -->"

    return _REGION.sub(body, page)


def strip(text: str) -> str:
    """The text without its markers, the regions' content kept."""
    return _MARKER.sub("", text)


def outside(text: str) -> str:
    """The text with every region, markers and content, removed: what a
    person wrote."""
    return _REGION.sub("", text)


def unbalanced(text: str) -> bool:
    """Whether a marker is left over once every well-formed region is out."""
    return bool(_MARKER.search(outside(text)))
