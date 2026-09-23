#!/usr/bin/env python3
"""Fetch the published site and check it is actually usable.

The offline checks cannot see this. `check-links.py` proves the build is
self-consistent, and it would have passed happily while the live site returned
403 for all ten concepts, because a build knows nothing about what reached the
bucket or what headers the CDN puts on it. Both of the ways this site has been
broken so far were invisible until something fetched a real URL:

    every link in llms.txt 404'd      the pages were published at another path
    every em dash arrived mojibake'd  no charset on the content type

So this asks what those failures answer to:

    does the bare domain serve something      the root object, and the rewrite
                                              that used to eat it
    does every advertised URL resolve         the index matching what exists
    does every text response name utf-8       the header a .md cannot carry
                                              for itself
    is each one served as its own type        a .md delivered as
                                              application/octet-stream is a
                                              download prompt, not a page

It runs after a publish, against the real domain, and is the only check here
that needs the network. That makes it the only one that can fail for reasons
unrelated to the commit — a CDN hiccup, DNS — so it runs as its own step after
the upload rather than gating it. A failure here means the site is wrong now,
not that the build was.
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request

DEFAULT_SITE = "https://docs.popcorn.ai"
TIMEOUT = 20

# A text response without a charset is decoded as windows-1252 by browsers.
# JSON is exempt: it is UTF-8 by specification and takes no charset parameter.
NEEDS_CHARSET = ("text/",)

# What each extension must actually arrive as. This mirrors the mapping in
# publish.py deliberately, from the other side: that file decides what to send
# and this one reads back what a stranger receives. A guess by the uploader
# that nobody sends is how .md pages became downloads.
EXPECTED_TYPE = {
    ".html": "text/html",
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".json": "application/json",
}


def fetch(url: str) -> tuple[int, str, bytes]:
    # No hyphens in the agent string: the leak guard matches anything
    # repository-shaped, and a public repo should not teach people to add
    # exceptions to it for cosmetics.
    req = urllib.request.Request(url, headers={"User-Agent": "popcorn docs check"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), b""
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, f"unreachable: {e}", b""


def check(url: str, failures: list[str]) -> bytes:
    status, ctype, body = fetch(url)
    if status != 200:
        failures.append(f"{url} → {status or ctype}")
        return b""

    suffix = "." + url.rsplit(".", 1)[-1] if "." in url.rsplit("/", 1)[-1] else ""
    expected = EXPECTED_TYPE.get(suffix)
    if expected and not ctype.lower().startswith(expected):
        failures.append(f"{url} → served as {ctype!r}, expected {expected}")
    elif ctype.startswith(NEEDS_CHARSET) and "charset=utf-8" not in ctype.lower():
        failures.append(f"{url} → {ctype!r} declares no utf-8 charset")
    return body


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", default=DEFAULT_SITE)
    args = ap.parse_args()
    site = args.site.rstrip("/")

    failures: list[str] = []

    # The bare domain. Someone handed the domain types exactly this.
    check(site + "/", failures)

    index = check(site + "/llms.txt", failures)
    if not index:
        print(f"✖  {site}/llms.txt did not serve — nothing else can be checked",
              file=sys.stderr)
        for f in failures:
            print(f"✖  {f}", file=sys.stderr)
        return 1

    urls = [
        line.strip()
        for line in index.decode("utf-8").splitlines()
        if line.strip().startswith(("http://", "https://"))
    ]
    if not urls:
        print("✖  the published llms.txt advertises no URLs", file=sys.stderr)
        return 1

    for url in urls:
        check(url, failures)
        # Each concept has an HTML twin a person follows from the index.
        if url.endswith(".md"):
            check(url[: -len(".md")] + ".html", failures)

    for f in failures:
        print(f"✖  {f}", file=sys.stderr)
    if failures:
        print(f"\n✖  {len(failures)} problem(s) with the published site",
              file=sys.stderr)
        return 1

    print(f"✔  {site} serves its root, {len(urls)} advertised URLs and their "
          f"HTML twins, all as utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
