# The docs MCP server

Three read-only tools over `build/chunks.json`, which `scripts/emit.py`
produces from `content/`.

```bash
python3 scripts/emit.py                    # build the corpus
pip install -r server/requirements.txt
python3 server/docs_mcp.py                 # stdio
```

`retrieval.py` holds every answer and imports no SDK, so it can be exercised
without a transport:

```python
import pathlib, retrieval
pages = retrieval.load(pathlib.Path("build/chunks.json"))
print(retrieval.search(pages, "my scalar keeps resetting"))
```

Run `scripts/emit.py` after any content change — the server reads the built
corpus, not `content/`, so an un-emitted edit is invisible to it.
