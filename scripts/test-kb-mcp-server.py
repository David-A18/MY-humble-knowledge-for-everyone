#!/usr/bin/env python3
"""Drive the knowledge MCP server over stdio against the real bundle."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

script = Path(__file__).with_name("kb-mcp-server.py")


def exchange(messages: list[dict]) -> list[dict]:
    lines = "\n".join(json.dumps(message) for message in messages) + "\n"
    run = subprocess.run([sys.executable, str(script)], input=lines, capture_output=True, text=True, check=True)
    return [json.loads(line) for line in run.stdout.splitlines()]


def call(call_id: int, name: str, **arguments) -> dict:
    return {"jsonrpc": "2.0", "id": call_id, "method": "tools/call", "params": {"name": name, "arguments": arguments}}


def text(reply: dict) -> dict:
    return json.loads(reply["result"]["content"][0]["text"])


def main() -> int:
    replies = exchange([
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        call(3, "search_knowledge", query="How do I discard an unstaged edit?"),
        call(4, "fetch_page", path="knowledge/git/troubleshooting/undo-and-recovery.md"),
        call(5, "fetch_page", path="knowledge/git/troubleshooting/undo-and-recovery.md", section="missing-section"),
        call(6, "fetch_page", path="../../etc/passwd"),
        call(7, "fetch_page", path="README.md"),
        call(8, "list_routes", prefix="knowledge/terraform/"),
        call(9, "search_knowledge", query="How do I bake sourdough bread at home?"),
        call(10, "edit_page", path="knowledge/glossary.md"),
        {"jsonrpc": "2.0", "id": 11, "method": "resources/write"},
    ])
    by_id = {reply["id"]: reply for reply in replies}
    failures = []

    def check(condition: bool, label: str) -> None:
        if not condition:
            failures.append(label)

    check(len(replies) == 11, "notifications must not be answered")
    check(by_id[1]["result"]["protocolVersion"] == "2025-06-18", "initialize echoes the protocol version")
    names = [tool["name"] for tool in by_id[2]["result"]["tools"]]
    check(names == ["search_knowledge", "fetch_page", "list_routes"], "only read-only tools are listed")
    found = text(by_id[3])
    check(found["sufficient"] and found["hits"], "search returns sufficient evidence")
    check(all({"citation", "trust_tier", "stale", "status", "source_ids"} <= hit.keys() for hit in found["hits"]),
          "hits carry OKF trust metadata")
    page = text(by_id[4])
    check("reflog" in page["text"] and page["metadata"]["status"] == "stable", "fetch returns the page and metadata")
    for reply_id, label in [(5, "missing section"), (6, "path traversal"), (7, "non-bundle file")]:
        check(by_id[reply_id]["result"].get("isError") is True, f"{label} is refused")
    routes = text(by_id[8])
    check(routes["total"] > 0 and all(r["path"].startswith("knowledge/terraform/") for r in routes["routes"]),
          "routes respect the prefix")
    check(text(by_id[9])["sufficient"] is False, "unanswerable search is flagged")
    check(by_id[10]["result"].get("isError") is True, "write tools do not exist")
    check(by_id[11]["error"]["code"] == -32601, "unknown methods are rejected")

    if failures:
        print("\n".join(failures))
        return 1
    print("Knowledge MCP server tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
