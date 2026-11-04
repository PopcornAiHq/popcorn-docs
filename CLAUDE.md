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

If a page needs two summaries, it is two pages. If it needs none, it is a
paragraph in another page.

## Asides are callouts

A sentence the page reads fine without — where to look, a shortcut, what
an assistant shows along the way — goes in a callout, not in the prose:

```
> [!TIP]
> Most assistants show the tool calls they make: look for `get_workspace`.
```

The kinds are GitHub's five, each with its own colour and icon, from
information to risk:

| Kind | For |
|---|---|
| `[!NOTE]` | a limit or behaviour worth knowing even when skimming |
| `[!TIP]` | a shortcut, or where to look |
| `[!IMPORTANT]` | what a reader needs to reach their goal and could miss |
| `[!WARNING]` | what goes wrong if it's ignored, such as a Publish reaching every Routine |
| `[!CAUTION]` | what can't be undone, such as a Copy or deleted rows |

Pick the mildest kind that is true: a Caution on something harmless teaches
readers to skip the ones that aren't. Text after the marker is the label
instead of the kind's name (`> [!NOTE] One Workspace at a time`); keep it
to a few words.

The MCP tools behind a step go in a Tip labelled "MCP tool call", right
under the step's prompt, so the prose can say what the assistant does
instead of naming them:

```
> [!TIP] MCP tool call
> Your assistant calls `list_connections`, then `make_connection`.
```

A plain `>` quote stays what it is everywhere else:
something a person says to their assistant. Anything a reader must do is a
step, never a callout.

## Tabs are for one choice, made once

When the same step differs by what the reader uses, such as their
assistant, give each a tab instead of a list of alternatives:

````
=== "Claude Code"

    ```bash
    claude mcp add …
    ```

=== "ChatGPT"

    See OpenAI's help.
````

A tab's content is indented four spaces. Sets with the same labels switch
together, and the site remembers the choice on the next page, so label the
same choice the same way everywhere. Without its script the page, like the
Markdown an agent reads, shows every tab under its label. Keep anything that
applies to every choice outside the tabs.

## A code block names its file

A block that is the whole or part of a file gets its file name as a title:

````
```yaml title="manifest.yaml"
````

A command or a fragment that isn't one file has no title.

## Glossary terms are capitalized

Every term `content/glossary/glossary.md` defines is capitalized wherever it
means that concept — everyday words included: a Workspace, an Item, a Run, a
Flow, a Merge Policy, the Head of a Copy. A capital tells the reader the word
is the product's, with a glossary entry behind it, and not the English word.
The model is Temporal's docs, which capitalize Schedule, Task and Event for
the same reason.

- **Ordinary English stays lowercase.** "Run the command", "the server's
  state", "a dry run", "ask for an outcome". Decide by meaning, never by
  search-and-replace.
- **Verbs stay lowercase.** Copy, publish, install, apply and check out are
  capitalized as nouns of the concept — a Copy, the Publish, an Install —
  and not as the action: "publish the Bundle".
- **Code is written as code spells it**: `manifest.yaml`, `popcorn app
  publish`, `call_flow`, `version:`.
- **Exceptions, each lowercase for a reason:** *active* and *deactivated*
  are adjectives; *rev* and `call_flow` are identifiers; channel
  parameters, channel agent and channel integration are the API's names,
  written as it spells them; *customizing a Routine* is a phrase, not a
  noun; *Popcorn's version* is the shared series, not a Version; the
  glossary's "Another name for" entries are headed by the names being
  mapped, not the product's word.

The glossary's entries are alphabetical, under a heading for their first
letter, like a printed one: a new entry goes in its place, not at the end of
a topic. Each is a `###` heading naming the term, its definition as plain
paragraphs, and a closing "Learn more:" line linking the page about it.

`scripts/check-vocabulary.py --strict` flags the terms that have no ordinary
sense — multi-word ones such as merge policy, and words such as workspace
and manifest — when written lowercase in prose. The rest are left to review.

## A term's first use links to its concept page

The first time a page's body uses a glossary term, the term links to its
concept page — the page about that term, such as Steps for a Step or Actions
and Status for an Action. A term with no concept page of its own stays plain
text; it does not link to its glossary entry, which only restates the
definition the reader is about to meet in context.

Titles, headings, frontmatter, a page's opening summary paragraph, code and
link text are exempt, and a page never links to itself. Later uses may link
again where it helps, but need not.
