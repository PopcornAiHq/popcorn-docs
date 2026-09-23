# Writing in this repository

## This repository is public

It is cloned, fetched raw over HTTPS, and read by agents we do not control.
Internal references must never land in it:

| Never write | Write instead |
|---|---|
| an issue-tracker id | the behaviour the ticket describes |
| a backend PR reference (`<private-repo>#<n>`) | what the change did |
| a private source path ending `.py` | the bare symbol — `fork_for_channel` |
| a repository that is not public | the behaviour, with no repository named |
| an internal document path | nothing — if it is not public, it is not citable |
| a real customer or channel name | `example-*`, or the shape without the value |

`scripts/check-public-repo.sh` fails the commit and the build on every row but
the last. It exists because the private sibling repo's house style actively
encourages these references — anyone moving between checkouts reintroduces
them while believing they are being consistent. The hook is there so nobody
has to remember.

**It is an allowlist, and that is the point.** The script is public too, so a
list of forbidden names would publish the names it protects. Instead it matches
a *shape* — anything repository-like, anything issue-key-like — and permits the
specific tokens that are already public. Adding a genuinely public repository
or an identifier standard such as `ISO-8601` means adding it to the allowlist
at the top of the script. A private name never goes in, which is why a private
name is caught without appearing anywhere.

## Cite symbols, never paths

A concept's `source:` field names bare symbols — the names a reader would
search the backend for, nothing about where they live. This is why a path is
both a leak and unnecessary. `scripts/drift.py sources` checks each name
still has a definition in a local backend checkout; CI cannot, since the
backend is private, so run it before any content PR. It checks existence, not
behaviour — see "Checking the pages against the backend" in `README.md`.

A symbol that moves file keeps its name; a path does not survive a refactor.
That is the same reason this rule holds in prose.

## Describe the present

Write what is true now. No `Last updated` fields — git knows. No forward
references to work that has not shipped; if planned work must be named, say
plainly that nothing depends on it arriving.

Measurements rot. "The catalog is large enough that filtering is the server's
job" survives; a byte count does not. When a figure genuinely carries the
argument, date it.

## Every page answers one question

If a concept needs two summaries, it is two concepts. If it needs none, it is
a paragraph in a guide.
