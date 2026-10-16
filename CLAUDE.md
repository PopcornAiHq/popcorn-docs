# Writing in this repository

## This repository is public

It is cloned, fetched raw over HTTPS, and read by agents we do not control.
Internal references must never land in it:

| Never write | Write instead |
|---|---|
| an issue-tracker id, in a tracked file | the behaviour the ticket describes |
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

**Ticket ids may go in commit messages and pull requests.** A Linear id is
allowed in a commit message, a PR title or description, and a branch name —
that is what Linear's GitHub integration reads to link and close the issue,
and a bare id discloses nothing the change itself does not. Every other row
above still applies there. To close the issue when the PR merges, put a
closing magic word and the id in the **PR description** — `Fixes KEW-NNNN`
(`closes`, `resolves`, `completes`, `implements` work too); `Part of KEW-NNNN`
or `Refs KEW-NNNN` links without closing. The script scans tracked files only,
so it neither blocks nor checks messages — the judgement is yours.

**It is an allowlist, and that is the point.** The script is public too, so a
list of forbidden names would publish the names it protects. Instead it matches
a *shape* — anything repository-like, anything issue-key-like — and permits the
specific tokens that are already public. Adding a genuinely public repository
or an identifier standard such as `ISO-8601` means adding it to the allowlist
at the top of the script. A private name never goes in, which is why a private
name is caught without appearing anywhere.

## Cite symbols, never paths

When prose has to name backend code, it names the bare symbol a reader would
search for, nothing about where it lives. A path is both a leak and
unnecessary: a symbol that moves file keeps its name, and a path does not
survive a refactor.

Pages do not list the symbols behind them. That list lives in a mapping kept
in the private backend repository, keyed by page `id`, and the backend's CI
fails when a listed symbol loses its definition. A `source:` field in a page
fails `check-content.py`. A new or rewritten page that describes specific
backend behaviour gets its entry in that mapping through a backend PR, and
`scripts/drift.py` reads it from a local backend checkout — see "Checking the
pages against the backend" in `README.md`.

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
