#!/usr/bin/env python3
"""Read-only MCP stdio server for the OKF knowledge bundle. Standard library only."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sqlite3
import sys
import tempfile
from contextlib import closing
from pathlib import Path

MAX_PAGE_CHARACTERS = 20000
MAX_ROUTES = 100
SERVER_INFO = {"name": "knowledge-base", "version": "1.0.0"}
TOOLS = [
    {
        "name": "search_knowledge",
        "description": "Search the knowledge base. Returns ranked, cited excerpts with OKF trust and "
        "freshness metadata. `sufficient: false` means the evidence is weak: say so instead of answering.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Question or keywords."},
                "k": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
            },
            "required": ["query"],
        },
    },
    {
        "name": "fetch_page",
        "description": "Read one concept returned by search_knowledge or list_routes, optionally one section.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Concept path, such as knowledge/git/index.md."},
                "section": {"type": "string", "description": "Optional heading anchor from a search citation."},
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_routes",
        "description": "List indexed concepts with titles and descriptions, optionally under a path prefix.",
        "inputSchema": {
            "type": "object",
            "properties": {"prefix": {"type": "string", "description": "Path prefix, such as knowledge/terraform/."}},
        },
    },
]


def load_rag(path: Path):
    spec = importlib.util.spec_from_file_location("rag", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KnowledgeServer:
    def __init__(self, root: Path, database: Path):
        self.root = root.resolve()
        self.database = database
        self.rag = load_rag(self.root / "knowledge/llm/rag/examples/rag.py")
        self.rag.ingest(self.root, database)

    def concepts(self) -> dict[str, dict]:
        with closing(sqlite3.connect(self.database)) as db:
            return {path: json.loads(data) for path, data in db.execute("SELECT path,data FROM concepts ORDER BY path")}

    def search_knowledge(self, query: str, k: int = 5) -> dict:
        return self.rag.search(self.database, query, k=k)

    def fetch_page(self, path: str, section: str | None = None) -> dict:
        # Only indexed concepts are reachable, so path tricks cannot leave the bundle.
        state = self.concepts().get(path)
        if state is None:
            raise ValueError(f"Not an indexed concept: {path}")
        text = (self.root / path).read_text(encoding="utf-8-sig")
        if section:
            parts = [part for part in self.rag.sections(text) if part[2] == section]
            if not parts:
                raise ValueError(f"No section {section} in {path}")
            text = parts[0][3].strip()
        return {"path": path, "section": section, "text": text[:MAX_PAGE_CHARACTERS],
                "truncated": len(text) > MAX_PAGE_CHARACTERS, "metadata": state}

    def list_routes(self, prefix: str = "knowledge/") -> dict:
        matches = [{"path": path, "title": state["title"], "description": state["description"],
                    "status": state["status"]}
                   for path, state in self.concepts().items() if path.startswith(prefix)]
        return {"total": len(matches), "routes": matches[:MAX_ROUTES], "truncated": len(matches) > MAX_ROUTES}

    def handle(self, message: dict) -> dict | None:
        method = message.get("method")
        if "id" not in message:
            return None
        reply = {"jsonrpc": "2.0", "id": message["id"]}
        params = message.get("params") or {}
        if method == "initialize":
            reply["result"] = {"protocolVersion": params.get("protocolVersion", "2025-06-18"),
                               "capabilities": {"tools": {}}, "serverInfo": SERVER_INFO}
        elif method == "ping":
            reply["result"] = {}
        elif method == "tools/list":
            reply["result"] = {"tools": TOOLS}
        elif method == "tools/call":
            reply["result"] = self.call(params.get("name"), params.get("arguments") or {})
        else:
            reply["error"] = {"code": -32601, "message": f"Method not found: {method}"}
        return reply

    def call(self, name: str, arguments: dict) -> dict:
        if name not in {tool["name"] for tool in TOOLS}:
            return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}
        try:
            result = getattr(self, name)(**arguments)
        except (TypeError, ValueError, OSError, sqlite3.Error) as error:
            return {"isError": True, "content": [{"type": "text", "text": re.sub(r"\s+", " ", str(error))}]}
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        server = KnowledgeServer(args.root, Path(directory) / "index.sqlite")
        for line in sys.stdin:
            if not line.strip():
                continue
            try:
                reply = server.handle(json.loads(line))
            except json.JSONDecodeError:
                reply = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
            if reply is not None:
                print(json.dumps(reply), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
