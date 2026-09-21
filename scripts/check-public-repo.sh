#!/bin/sh
# Pre-commit hook and CI check: this repository is PUBLIC.
#
# Here because the sibling repository this documents is private, and its own
# conventions encourage citing tickets, pull requests and source paths. Anyone
# moving between the two checkouts reintroduces them while believing they are
# following house style. This fails instead of remembering.
#
# **This file is public too, which shapes the design.** A denylist of private
# names would publish the names it exists to protect. So the two checks that
# would need one are allowlists instead: they match a SHAPE, then permit the
# specific tokens that are already public. A private name is refused without
# ever being written down here.
#
# Scans the INDEX (`git grep --cached`), which is both what a commit is about
# to contain and, in a CI checkout, the whole tracked tree — so the hook and
# the CI job are one command with one scope. Scanning the index rather than the
# staged paths is deliberate: a hook that sees a single file cannot tell you
# the tree already contains a violation.
#
# Usage: scripts/check-public-repo.sh   (no arguments, in either context)

set -eu

# Skip this file: it necessarily contains the shapes it searches for.
self=':(exclude)scripts/check-public-repo.sh'

# Public names this repository may write. Mostly repositories, plus this
# project's own MCP server identifier, which shares their shape — the check
# matches a shape rather than a list, so anything named `popcorn-something`
# lands here whether or not it is a repository. Anything not listed is refused.
ALLOWED_REPO='^(PopcornAiHq/)?(docs|popcorn-docs|popcorn-cli|popcorn-claude-code)$'

# Prefixes of public identifier standards, which share their shape with an
# issue key. Without this, a page about datetime columns fails on "ISO-8601".
ALLOWED_KEY='^(ISO|RFC|UTF|ASCII|SHA|MD|AES|RSA|HTTP|HTML|XML|JSON|YAML|TOML|SQL|AWS|API|URL|URI|MCP|CLI|DSL|PDF|CSV|TSV|SDK|OAUTH|JWT|S3|EC2|IAM|KMS|TTL|UUID|ULID|SEP|PEP|CVE|UTC)-'

found=0

# report <label> <regex> [allowlist]
# Without an allowlist, any match is a violation. With one, a match is a
# violation unless the matched token itself is permitted.
report() {
    label=$1
    regex=$2
    allow=${3:-}

    set +e
    hits=$(git grep --cached -nIoE -e "$regex" -- "$self")
    status=$?
    set -e

    case "$status" in
        0) ;;
        1) return 0 ;;  # no match — the success case
        *)
            echo "✖  git grep failed (exit $status) scanning for $label" >&2
            exit "$status"
            ;;
    esac

    if [ -n "$allow" ]; then
        # "file:line:token" — drop the rows whose token is already public.
        # The shapes anchor on a preceding non-word character so they do not
        # fire mid-identifier, and `-o` returns it, so strip it before the
        # comparison or every token fails an anchored allowlist.
        hits=$(printf '%s\n' "$hits" | awk -F: -v ok="$allow" '
            { tok = $NF; sub(/^[^A-Za-z0-9]+/, "", tok); if (tok !~ ok) print }')
    fi

    [ -n "$hits" ] || return 0

    found=1
    echo ""
    echo "✖  $label in a public repo:"
    printf '%s\n' "$hits" | sed 's/^/     /'
}

# Deliberately narrow — a pattern that cries wolf gets switched off, which is
# worse than one that misses. The source-path shape requires a ".py" tail and a
# preceding non-path character, so prose naming a bare symbol is untouched.
report 'private source path' \
    '(^|[^/[:alnum:]_.-])(lib|services|ops)/[a-z_]+/[a-z_/]*\.py'
report 'internal document path' \
    '(specs|plans|runbooks|notes)/[0-9]{4}-[0-9]{2}-[0-9]{2}'
report 'machine-local path' \
    '(/Users/|/home/[a-z]|~/[a-z]+/)'
report 'non-public repository reference' \
    '(PopcornAiHq/[A-Za-z0-9_.-]+|(^|[^A-Za-z0-9-])popcorn-[a-z0-9-]+)' \
    "$ALLOWED_REPO"
report 'issue-tracker id' \
    '(^|[^A-Za-z0-9-])[A-Z]{2,6}-[0-9]{2,6}' \
    "$ALLOWED_KEY"

if [ "$found" -eq 1 ]; then
    cat <<'MSG'

   This repository is public. Cite the behaviour ("the server refuses X") and
   the bare symbol ("fork_for_channel"), never the ticket, private repository
   or source file that proves it.

   A public repository or identifier standard that is genuinely missing belongs
   in this script's allowlist. A private one does not belong anywhere.

   See CLAUDE.md — "This repository is public".
MSG
    exit 1
fi
