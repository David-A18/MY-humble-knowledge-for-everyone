#!/usr/bin/env python3
"""Build a deterministic machine-readable catalog from OKF concept metadata."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

import yaml


def normalize(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in sorted(value.items())}
    return value


def split_frontmatter(markdown: str) -> dict:
    if not markdown.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = markdown.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter has no closing delimiter")
    data = yaml.safe_load(markdown[4:end])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def build_catalog(bundle: Path) -> dict:
    concepts = []
    for path in sorted(bundle.rglob("*.md")):
        if path.name in {"index.md", "log.md"}:
            continue
        metadata = split_frontmatter(path.read_text(encoding="utf-8"))
        sources = metadata.get("sources", [])
        concepts.append(
            {
                "path": path.as_posix(),
                "title": metadata["title"],
                "description": metadata["description"],
                "type": metadata["type"],
                "tags": metadata["tags"],
                "status": metadata["status"],
                "maturity": metadata["maturity"],
                "audience": metadata["audience"],
                "maintainer": metadata["maintainer"],
                "stale_after": metadata.get("stale_after"),
                "source_ids": [source["id"] for source in sources],
            }
        )
    return normalize(
        {
            "catalog_version": "1",
            "bundle_root": bundle.as_posix(),
            "concept_count": len(concepts),
            "concepts": concepts,
        }
    )


def render(catalog: dict) -> str:
    return json.dumps(catalog, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", default="knowledge", type=Path)
    parser.add_argument("--output", default="generated/knowledge-catalog.json", type=Path)
    parser.add_argument("--check", action="store_true", help="fail when the tracked catalog is stale")
    args = parser.parse_args()

    expected = render(build_catalog(args.bundle))
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != expected:
            print(f"{args.output}: catalog is missing or stale; run scripts/build-knowledge-catalog.py", file=sys.stderr)
            return 1
        print(f"Knowledge catalog is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
