# Popcorn docs

Source for **docs.popcorn.ai** — the concepts an agent or a person needs to
author, publish and operate a Popcorn app bundle.

This repository is **public**. See `CLAUDE.md` before writing anything.

## Layout

```
content/
├── concepts/     one addressable idea per file — the unit the MCP serves
├── guides/       task-shaped walkthroughs
└── reference/    GENERATED — do not edit by hand
```

## The summary is the product

Every concept's frontmatter carries a `summary` under 400 characters. That
field is what an agent gets back in one call; the body is what the website and
a CLI checkout get. Writing the summary well is the work — a generator cannot
do it, and a body without one is not finished.
