#!/usr/bin/env python3
"""Upload `build/` to the docs bucket, declaring the charset on every text file.

The reason this exists rather than a bare `aws s3 sync`: the CLI guesses a
content type from the extension and guesses it without a charset. A response
of `text/markdown` with no charset is decoded as windows-1252 by browsers, so
every em dash in a published page arrived as `â€"`. The HTML pages escaped it
only because they carry `<meta charset="utf-8">` in the document, which the
`.md` and `.txt` files have no way to do — and those are the ones an agent
fetches.

So the mapping is declared here, once, and the publish is not a command
someone retypes from memory.

Every file is uploaded on every run rather than diffed. `aws s3 sync` compares
size and mtime, and `emit.py` rebuilds `build/` from empty, so every file is
always "new" and sync re-uploads the whole corpus anyway — the comparison buys
nothing and hides which content type each object got. The corpus is small
enough that unconditional upload is the simpler thing that is also the honest
thing.

Orphans are removed one key at a time, not with `rm --recursive`. A prefix
delete against a live bucket is the operation that cannot be taken back, and
the only keys that should ever disappear are the ones this build stopped
producing.

The publish ends with an invalidation, and that is not belt-and-braces. A
change to a header alone leaves the body byte-identical, so the ETag does not
move; when the TTL lapses CloudFront revalidates, S3 answers 304 Not Modified,
and the cached response is served again with its stale headers. Waiting cannot
fix a metadata-only change — this is exactly how the missing charset survived
its first correction. A deleted orphan has the same shape: gone from the
bucket, still served until something says otherwise.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

# JSON is UTF-8 by specification and takes no charset parameter.
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".json": "application/json",
}


def aws(*args: str) -> str:
    """Run an aws command, failing loudly. Credentials come from the caller."""
    done = subprocess.run(
        ["aws", *args, "--no-cli-pager"],
        capture_output=True,
        text=True,
    )
    if done.returncode != 0:
        sys.exit(f"✖  aws {' '.join(args[:3])}…: {done.stderr.strip()}")
    return done.stdout


def local_files() -> dict[str, pathlib.Path]:
    if not BUILD.is_dir():
        sys.exit("✖  build/ missing — run scripts/emit.py first")
    return {
        str(p.relative_to(BUILD)): p
        for p in sorted(BUILD.rglob("*"))
        if p.is_file()
    }


def remote_keys(bucket: str) -> set[str]:
    out = aws(
        "s3api", "list-objects-v2", "--bucket", bucket,
        "--query", "Contents[].Key", "--output", "text",
    )
    return {k for k in out.split() if k}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bucket", default="popcorn-prod-docs")
    ap.add_argument("--distribution", default="E2KXXLZNE4W83R")
    ap.add_argument(
        "--no-invalidate",
        action="store_true",
        help="skip the CloudFront invalidation (headers and deletions will lag)",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = local_files()
    unknown = sorted({p.suffix for p in files.values()} - set(CONTENT_TYPES))
    if unknown:
        sys.exit(
            f"✖  no content type declared for: {', '.join(unknown)}. "
            "Add it to CONTENT_TYPES rather than letting the CLI guess."
        )

    for key, path in files.items():
        ctype = CONTENT_TYPES[path.suffix]
        if args.dry_run:
            print(f"   would upload {key}  ({ctype})")
            continue
        aws(
            "s3", "cp", str(path), f"s3://{args.bucket}/{key}",
            "--content-type", ctype,
        )

    orphans = sorted(remote_keys(args.bucket) - set(files))
    for key in orphans:
        if args.dry_run:
            print(f"   would delete {key}")
            continue
        aws("s3api", "delete-object", "--bucket", args.bucket, "--key", key)

    invalidated = False
    if not args.no_invalidate:
        if args.dry_run:
            print(f"   would invalidate /* on {args.distribution}")
        else:
            aws(
                "cloudfront", "create-invalidation",
                "--distribution-id", args.distribution,
                "--paths", "/*",
            )
            invalidated = True

    verb = "would publish" if args.dry_run else "published"
    tail = f", {len(orphans)} orphan(s) removed" if orphans else ""
    tail += ", invalidated /*" if invalidated else ""
    print(f"✔  {verb} {len(files)} files to s3://{args.bucket}/{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
