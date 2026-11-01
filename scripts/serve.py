#!/usr/bin/env python3
"""Serve `build/` locally at the addresses the published site uses.

A page's HTML is written to `build/<id>.html` but published as `/<id>`
(`publish.key_for`), and every link in the site points at `/<id>`. A plain
`python3 -m http.server` would answer those links with 404, so this serves
`/<id>` from `<id>.html` and refuses `/<id>.html`, which the published site
does not have either. A missing path gets `404.html` with a 404 status, and
Markdown is served as text, both as the distribution does.

    python3 scripts/serve.py          # http://localhost:8000
    python3 scripts/serve.py 8001
"""

from __future__ import annotations

import functools
import http.server
import pathlib
import sys

from publish import NAMED_HTML

BUILD = pathlib.Path(__file__).resolve().parent.parent / "build"


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = http.server.SimpleHTTPRequestHandler.extensions_map | {
        ".md": "text/markdown; charset=utf-8",
    }

    def translate_path(self, path: str) -> str:
        local = pathlib.Path(super().translate_path(path))
        if local.suffix == ".html" and local.name not in NAMED_HTML:
            return str(BUILD / "missing")
        if not local.exists() and local.with_name(local.name + ".html").is_file():
            return str(local.with_name(local.name + ".html"))
        return str(local)

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        page = BUILD / "404.html"
        if code != 404 or not page.is_file():
            return super().send_error(code, message, explain)
        body = page.read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)


def main() -> int:
    if not BUILD.is_dir():
        sys.exit("✖  build/ missing — run scripts/emit.py first")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(Handler, directory=str(BUILD))
    with http.server.ThreadingHTTPServer(("", port), handler) as server:
        print(f"serving build/ at http://localhost:{port}")
        server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
