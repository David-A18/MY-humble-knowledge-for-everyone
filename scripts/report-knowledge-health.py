#!/usr/bin/env python3
"""Report what the OKF bundle holds and how far each area can be trusted."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml

THIN_WORDS = 200
EXCLUDED = ("knowledge/templates/", "knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/")


def split_page(text: str) -> tuple[dict, str]:
    end = text.find("\n---\n", 4)
    return (yaml.safe_load(text[4:end]) or {}, text[end + 5:]) if text.startswith("---\n") and end != -1 else ({}, text)


def prose_words(body: str) -> int:
    return len(re.findall(r"\w+", re.sub(r"```.*?```", "", body, flags=re.S)))


def tier(metadata: dict) -> str:
    verified = metadata.get("verified")
    if not verified:
        return "unverified"
    entries = verified if isinstance(verified, list) else [verified]
    return "human-reviewed" if any(str(e.get("by", "")).startswith("human:") for e in entries) else "machine-confirmed"


def build(bundle: Path, today: date) -> dict:
    root = bundle.parent
    areas: dict[str, Counter] = defaultdict(Counter)
    tiers: Counter = Counter()
    status: Counter = Counter()
    thin, unsourced, stale, expiring = [], [], [], []
    for path in sorted(bundle.rglob("*.md")):
        name = path.relative_to(root).as_posix()
        if path.name in {"index.md", "log.md"} or name.startswith(EXCLUDED):
            continue
        metadata, body = split_page(path.read_text(encoding="utf-8"))
        parts = name.split("/")
        area = areas[parts[1] if len(parts) > 2 else "(root)"]
        words = prose_words(body)
        area["concepts"] += 1
        area["words"] += words
        area["sourced"] += bool(metadata.get("sources"))
        area["stable"] += metadata.get("status") == "stable"
        area["thin"] += words < THIN_WORDS
        status[metadata.get("status", "stable")] += 1
        tiers[tier(metadata)] += 1
        if words < THIN_WORDS:
            thin.append({"path": name, "words": words})
        if not metadata.get("sources"):
            unsourced.append({"path": name, "words": words})
        if metadata.get("stale_after"):
            deadline = str(metadata["stale_after"])[:10]
            (stale if date.fromisoformat(deadline) <= today else expiring).append({"path": name, "stale_after": deadline})
    empty = sorted(p.parent.name for p in bundle.glob("*/index.md") if p.parent.name != "assets"
                   and not any(c.name not in {"index.md", "log.md"} for c in p.parent.rglob("*.md")))
    concepts = sum(area["concepts"] for area in areas.values())
    return {
        "generated_on": today.isoformat(),
        "scope": "Real concepts only; templates and the synthetic OKF example bundle are excluded.",
        "concepts": concepts,
        "words": sum(area["words"] for area in areas.values()),
        "sourced": sum(area["sourced"] for area in areas.values()),
        "status": dict(status),
        "trust_tiers": dict(tiers),
        "empty_areas": empty,
        "areas": {name: dict(counts) for name, counts in sorted(areas.items(), key=lambda kv: -kv[1]["words"])},
        "thin_pages": sorted(thin, key=lambda page: page["words"]),
        "largest_unsourced": sorted(unsourced, key=lambda page: -page["words"])[:25],
        "unsourced_count": len(unsourced),
        "stale_now": stale,
        "next_to_expire": sorted(expiring, key=lambda page: page["stale_after"])[:10],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", default="knowledge", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.bundle.resolve(), date.today()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
