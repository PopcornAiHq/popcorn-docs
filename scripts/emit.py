#!/usr/bin/env python3
"""One pass over `content/`, every machine-readable output.

Deliberately one script rather than one per artifact. Sites that grew a second
transform for their LLM exports ended up with the two disagreeing, and the
fix was always to collapse them back into a single walk of the source. So
`chunks.json`, `llms.txt`, `llms-full.txt` and the per-page Markdown all come
out of the same read here, and a fifth output belongs in this file too.

Outputs, under `build/`:

    chunks.json      one record per concept — what the MCP server serves
    llms.txt         the index: id, title, summary. The whole corpus, cheaply.
    llms-full.txt    every body concatenated, for a reader that wants it all
    md/<id>.md       the plain-Markdown twin of each page

`llms.txt` is the file most likely to be fetched by something we do not
control, so it carries summaries and not bodies. A reader that wants
everything asks for `llms-full.txt` and knows what it is paying for.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
BUILD = ROOT / "build"
SITE = "https://docs.popcorn.ai"

_DOC = re.compile(r"^---\n(?P<fm>.*?)\n---\n(?P<body>.*)$", re.S)
_SCALAR = re.compile(r"^(?P<key>[a-z_]+):\s*(?P<val>.*)$")


def parse(path: pathlib.Path) -> dict:
    """Frontmatter and body. A deliberately small YAML subset.

    Only the shapes `content/_frontmatter.md` documents: plain scalars, folded
    blocks (`key: >`), and flow sequences (`key: [a, b]`). Anything else is a
    file that does not follow the contract, and the contract checker is what
    should say so — not a silent reinterpretation here.
    """
    doc = _DOC.match(path.read_text())
    if not doc:
        raise SystemExit(f"✖  {path.relative_to(ROOT)}: no frontmatter")

    meta: dict = {}
    key: str | None = None
    folded: list[str] = []

    for line in doc.group("fm").splitlines():
        if key and (line.startswith("  ") or line.startswith("\t")):
            folded.append(line.strip())
            continue
        if key:
            meta[key] = " ".join(folded).strip()
            key, folded = None, []

        found = _SCALAR.match(line)
        if not found:
            continue
        name, value = found.group("key"), found.group("val").strip()
        if value == ">":
            key = name
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[name] = [v.strip() for v in inner.split(",") if v.strip()]
        else:
            meta[name] = value

    if key:
        meta[key] = " ".join(folded).strip()

    meta["body"] = doc.group("body").strip()
    meta["section"] = path.parent.name
    return meta


def main() -> int:
    pages = [
        parse(p)
        for p in sorted(CONTENT.rglob("*.md"))
        if not p.name.startswith("_")
    ]
    if not pages:
        print("✖  no content", file=sys.stderr)
        return 1

    md = BUILD / "md"
    md.mkdir(parents=True, exist_ok=True)

    (BUILD / "chunks.json").write_text(
        json.dumps({"site": SITE, "pages": pages}, indent=2) + "\n"
    )

    index = ["# Popcorn docs", ""]
    full = ["# Popcorn docs — full text", ""]
    for page in pages:
        url = f"{SITE}/{page['section']}/{page['id']}"
        index += [f"## {page['title']}", f"{url}", "", page["summary"], ""]
        full += [f"# {page['title']}", "", page["summary"], "", page["body"], ""]
        (md / f"{page['id']}.md").write_text(
            f"# {page['title']}\n\n{page['summary']}\n\n{page['body']}\n"
        )

    (BUILD / "llms.txt").write_text("\n".join(index))
    (BUILD / "llms-full.txt").write_text("\n".join(full))

    size = (BUILD / "llms.txt").stat().st_size
    print(f"✔  {len(pages)} pages → chunks.json, llms.txt ({size:,}B), "
          f"llms-full.txt, md/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
