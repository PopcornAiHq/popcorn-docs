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
    <section>/<id>.md  the plain-Markdown twin of each page, at the path
                     its llms.txt entry advertises
    <section>/<id>.html  the same page for a person with a browser
    index.html       the landing page, every concept with its summary

`llms.txt` is the file most likely to be fetched by something we do not
control, so it carries summaries and not bodies. A reader that wants
everything asks for `llms-full.txt` and knows what it is paying for.

Pages are written under their section, mirroring the URL in the index, so
that the link an agent follows is the file that was emitted. They were once
flattened into a single `md/` directory while the index advertised
`<section>/<id>`, and every link in the index 404ed. `check-links.py` is
what now holds the two together.

The `.md` suffix is load-bearing: it is what makes S3 serve the page as
text/markdown without the upload having to name a content type per object.

The HTML twin sits beside the Markdown one rather than replacing it, and
`llms.txt` keeps pointing at the `.md`. An agent asking for a page should get
prose, not a document it has to strip tags out of first; a person following
the same path in a browser gets the `.html`. Neither has to content-negotiate
and neither URL moves when the other changes.
"""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import sys

import render

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


# The order sections appear on the landing page. A guide is where a person
# starts; the concepts are what it and every agent answer points into.
SECTION_ORDER = {"guides": ("Start here", "guides"), "concepts": ("Concepts", "concepts")}


def landing(pages: list[dict]) -> str:
    """The one page a person lands on: every page, grouped by section."""
    groups: dict[str, list[str]] = {}
    for page in pages:
        href = f"/{page['section']}/{page['id']}.html"
        groups.setdefault(page["section"], []).append(
            f'<li><a href="{href}">{render.inline(page["title"])}</a>'
            f"<p>{render.inline(page['summary'])}</p></li>"
        )
    ordered = sorted(groups, key=lambda s: (s not in SECTION_ORDER, list(SECTION_ORDER).index(s) if s in SECTION_ORDER else 0, s))
    sections = []
    for section in ordered:
        heading, anchor = SECTION_ORDER.get(section, (section.title(), section))
        sections.append(
            f'<h2 class="section-title" id="{anchor}">{heading}</h2>\n'
            '<ul class="index">' + "".join(groups[section]) + "</ul>"
        )
    return render.document(
        "Popcorn docs",
        "<h1>Popcorn docs</h1>\n"
        '<p class="summary">How app bundles work — the concepts an author or an '
        "agent needs in order to change what a channel tracks.</p>\n"
        + "\n".join(sections)
        + "\n<footer>For agents: the index is <a href=\"/llms.txt\">/llms.txt</a>, "
        "every body at <a href=\"/llms-full.txt\">/llms-full.txt</a>, "
        "and one record per concept at <a href=\"/chunks.json\">/chunks.json</a>."
        "</footer>",
        description="How Popcorn app bundles work: tables, flows, schedules and "
        "webhooks, and what happens when you publish.",
    )


def related(page: dict, by_id: dict[str, dict]) -> str:
    """"See also" from the page's `concepts:` — only ids that exist.

    An id naming no page is dropped rather than linked, so a typo costs a
    missing link, not a 404 on the published site.
    """
    links = [
        f'<li><a href="/{by_id[i]["section"]}/{i}.html">{render.inline(by_id[i]["title"])}</a></li>'
        for i in page.get("concepts", [])
        if i in by_id and i != page["id"]
    ]
    if not links:
        return ""
    return '<section class="related"><h2>Related</h2><ul>' + "".join(links) + "</ul></section>\n"


def main() -> int:
    pages = [
        parse(p)
        for p in sorted(CONTENT.rglob("*.md"))
        if not p.name.startswith("_")
    ]
    if not pages:
        print("✖  no content", file=sys.stderr)
        return 1

    # Rebuild from empty. Without this a page that was renamed or deleted in
    # `content/` keeps its old file here, and the publish is a sync rather than
    # a replacement, so the stale copy stays reachable on the site long after
    # nothing links to it.
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    (BUILD / "chunks.json").write_text(
        json.dumps({"site": SITE, "pages": pages}, indent=2) + "\n"
    )

    index = ["# Popcorn docs", ""]
    full = ["# Popcorn docs — full text", ""]
    by_id = {page["id"]: page for page in pages}
    for page in pages:
        path = f"{page['section']}/{page['id']}.md"
        index += [f"## {page['title']}", f"{SITE}/{path}", "", page["summary"], ""]
        full += [f"# {page['title']}", "", page["summary"], "", page["body"], ""]
        page_file = BUILD / path
        page_file.parent.mkdir(parents=True, exist_ok=True)
        page_file.write_text(
            f"# {page['title']}\n\n{page['summary']}\n\n{page['body']}\n"
        )
        rendered = render.body(page["body"])
        page_file.with_suffix(".html").write_text(
            render.document(
                f"{page['title']} — Popcorn docs",
                f"<h1>{render.inline(page['title'])}</h1>\n"
                f'<p class="summary">{render.inline(page["summary"])}</p>\n'
                f"{render.toc(rendered)}{rendered}\n"
                f"{related(page, by_id)}"
                "<footer>This page as Markdown: "
                f'<a href="/{path}">/{path}</a></footer>',
                description=page["summary"],
            )
        )

    (BUILD / "llms.txt").write_text("\n".join(index))
    (BUILD / "llms-full.txt").write_text("\n".join(full))
    (BUILD / "index.html").write_text(landing(pages))

    size = (BUILD / "llms.txt").stat().st_size
    sections = ", ".join(sorted({f"{p['section']}/" for p in pages}))
    print(f"✔  {len(pages)} pages → chunks.json, llms.txt ({size:,}B), "
          f"llms-full.txt, index.html, {sections}(.md + .html)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
