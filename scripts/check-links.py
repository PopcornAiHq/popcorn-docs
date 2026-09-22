#!/usr/bin/env python3
"""Every URL the index advertises resolves to a file that was emitted.

The index and the pages are written by the same loop in `emit.py`, which
makes them look impossible to disagree — but they disagreed for as long as
the index built its URL from `<section>/<id>` while the pages were flattened
into one `md/` directory. Nothing caught it: the frontmatter contract reads
`content/`, the retrieval check ranks concepts by id, and neither knows what
path the site serves. It surfaced only when a real agent followed a real link
and got a 403.

So this check reads the emitted `llms.txt` exactly as a stranger would, takes
the URLs at face value, and asks the filesystem whether each one was built.

It runs offline against `build/`, not against the live site. A network check
would also catch a publish that never uploaded, but it cannot run before the
first deploy and it fails for reasons that have nothing to do with the commit
under test. The mismatch this guards is decided at build time.

Both directions matter. A URL with no file is a dead link. A file with no URL
is a page nothing can discover, which is the same defect seen from the other
end.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SITE = "https://docs.popcorn.ai"

# The files that are the index rather than a page reached from it.
INDEX_FILES = {"llms.txt", "llms-full.txt", "chunks.json"}


def advertised() -> list[str]:
    """Site-relative paths named in llms.txt, in the order they appear."""
    index = BUILD / "llms.txt"
    if not index.exists():
        raise SystemExit("✖  build/llms.txt missing — run scripts/emit.py first")

    out = []
    for line in index.read_text().splitlines():
        line = line.strip()
        if line.startswith(SITE):
            out.append(line[len(SITE) :].lstrip("/"))
    return out


def emitted() -> set[str]:
    """Build-relative paths of every page file, excluding the index files."""
    return {
        str(p.relative_to(BUILD))
        for p in BUILD.rglob("*")
        if p.is_file() and p.name not in INDEX_FILES
    }


def main() -> int:
    urls = advertised()
    if not urls:
        print("✖  llms.txt advertises no URLs at all", file=sys.stderr)
        return 1

    files = emitted()
    dead = [u for u in urls if u not in files]
    orphans = sorted(files - set(urls))

    for path in dead:
        print(f"✖  {SITE}/{path} is advertised but was not emitted", file=sys.stderr)
    for path in orphans:
        print(f"✖  build/{path} was emitted but nothing links to it", file=sys.stderr)

    if dead or orphans:
        return 1

    print(f"✔  all {len(urls)} advertised URLs resolve to an emitted page")
    return 0


if __name__ == "__main__":
    sys.exit(main())
