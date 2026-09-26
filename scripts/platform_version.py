"""The `platform:` date a generated reference page carries, and when it changes.

`sync-activities.py` and `sync-mcp.py` describe the deployed platform, and
the backend's deploy pipeline runs them after every prod deploy with that
deploy's version:

    --platform-version vYYYYMMDD-HHMMSS-<7 hex>

Only the date is recorded, as `platform: YYYY-MM-DD` in the frontmatter. The
deploy version ends in a commit hash from a private repository, which this
public one must not carry; the date is what tells a reader how fresh the page
is, and that is all the page needs to say.

The date moves only when the rest of the page does. Every deploy runs the
generators, and most deploys change neither the catalog nor the tools; if the
date moved anyway, every deploy would produce a diff and a pull request that
said nothing. So the page is generated without the line, compared with the
current page with its line removed, and:

* unchanged: the current page is kept exactly, date or no date
* changed, with a version: the new date is written
* changed, without one: the line is left out, since a hand run does not know
  which deploy it read

`--check` compares the same way, so it reports a page stale only when
something other than the date would change.
"""

from __future__ import annotations

import argparse
import datetime
import re

_VERSION = re.compile(r"^v(?P<date>\d{8})-\d{6}-[0-9a-f]{7}$")
_LINE = re.compile(r"^platform: .*\n", re.M)
_FRONT = re.compile(r"^---\n.*?\n---\n", re.S)


def deploy_date(value: str) -> str:
    """The `YYYY-MM-DD` of a deploy version, or an argparse error naming the format."""
    found = _VERSION.match(value)
    try:
        if not found:
            raise ValueError
        day = datetime.datetime.strptime(found.group("date"), "%Y%m%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{value!r} is not a deploy version — expected vYYYYMMDD-HHMMSS-<7 hex>, "
            "such as v20260925-120000-abc1234"
        ) from None
    return day.isoformat()


def add_argument(ap: argparse.ArgumentParser) -> None:
    ap.add_argument("--platform-version", dest="platform", type=deploy_date, metavar="VERSION",
                    help="the deploy version the page was read from (vYYYYMMDD-HHMMSS-<sha>); "
                         "only its date is written, and only when the page otherwise changes")


def _without(text: str) -> str:
    """The page with its `platform:` line removed from the frontmatter only."""
    front = _FRONT.match(text)
    if not front:
        return text
    return _LINE.sub("", front.group(0), count=1) + text[front.end():]


def stamp(generated: str, current: str, date: str | None) -> str:
    """What to write, given the freshly generated page (which has no line).

    The line goes before `summary:`, beside the other short scalars.
    """
    if generated == _without(current):
        return current
    if date is None:
        return generated
    return generated.replace("\nsummary:", f"\nplatform: {date}\nsummary:", 1)
