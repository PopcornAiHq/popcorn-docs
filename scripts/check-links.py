#!/usr/bin/env python3
"""Nothing the corpus points at is missing, in either direction.

The index and the pages are written by the same loop in `emit.py`, which
makes them look impossible to disagree — but they disagreed for as long as
the index built its URL from `<section>/<id>` while the pages were flattened
into one `md/` directory. Nothing caught it: the frontmatter contract reads
`content/`, the retrieval check ranks concepts by id, and neither knows what
path the site serves. It surfaced only when a real agent followed a real link
and got a 403.

Three relationships, because there are now two audiences reading the same
corpus by different paths:

    llms.txt  → a file      an agent follows this; a miss is a dead link
    a .md page → llms.txt   a page no index names is undiscoverable
    an href   → a file      a person follows this; same failure, HTML side

The orphan rule applies only to the Markdown pages. An `.html` twin is
reached from `index.html`, never from `llms.txt`, so requiring an entry for
it would be requiring the wrong thing.

It runs offline against `build/`, not against the live site. A network check
would also catch a publish that never uploaded, but it cannot run before the
first deploy and it fails for reasons that have nothing to do with the commit
under test. The mismatch this guards is decided at build time.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SITE = "https://docs.popcorn.ai"

# The corpus-level files, reached directly rather than as a page.
INDEX_FILES = {"llms.txt", "llms-full.txt", "chunks.json", "index.html", "robots.txt", "sitemap.xml", "search.json"}

_HREF = re.compile(r'href="([^"]+)"')
_LOC = re.compile(r"<loc>([^<]+)</loc>")


def advertised() -> list[str]:
    """Site-relative paths named in llms.txt, in the order they appear."""
    index = BUILD / "llms.txt"
    if not index.exists():
        raise SystemExit("✖  build/llms.txt missing — run scripts/emit.py first")

    return [
        line.strip()[len(SITE) :].lstrip("/")
        for line in index.read_text().splitlines()
        if line.strip().startswith(SITE)
    ]


def emitted() -> set[str]:
    """Every build-relative file path."""
    return {str(p.relative_to(BUILD)) for p in BUILD.rglob("*") if p.is_file()}


def hrefs() -> list[tuple[str, str]]:
    """(source page, target path) for every link in every emitted HTML page."""
    out = []
    for page in sorted(BUILD.rglob("*.html")):
        src = str(page.relative_to(BUILD))
        for href in _HREF.findall(page.read_text()):
            if href.startswith(("http://", "https://", "#", "mailto:", "data:")):
                continue
            # A fragment names a place in the page, not a file; the file is
            # what has to exist.
            href = href.split("#", 1)[0]
            # "/" is the site root, which the distribution serves as index.html.
            target = "index.html" if href == "/" else href.lstrip("/")
            out.append((src, target))
    return out


def main() -> int:
    urls = advertised()
    if not urls:
        print("✖  llms.txt advertises no URLs at all", file=sys.stderr)
        return 1

    files = emitted()
    pages = {f for f in files if f.endswith(".md") and f not in INDEX_FILES}

    dead = [u for u in urls if u not in files]
    orphans = sorted(pages - set(urls))
    broken = [(src, t) for src, t in hrefs() if t not in files]
    # The sitemap is what a search engine indexes, so a dead entry there is a
    # dead search result.
    sitemap = BUILD / "sitemap.xml"
    for loc in _LOC.findall(sitemap.read_text()) if sitemap.exists() else []:
        target = loc[len(SITE):].lstrip("/") or "index.html"
        if target not in files:
            broken.append(("sitemap.xml", target))

    for path in dead:
        print(f"✖  {SITE}/{path} is advertised but was not emitted", file=sys.stderr)
    for path in orphans:
        print(f"✖  build/{path} was emitted but nothing links to it", file=sys.stderr)
    for src, target in broken:
        print(f"✖  {src} links to /{target}, which was not emitted", file=sys.stderr)

    if dead or orphans or broken:
        return 1

    print(
        f"✔  {len(urls)} advertised URLs and {len(hrefs())} page links "
        f"all resolve to an emitted file"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
