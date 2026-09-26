#!/usr/bin/env python3
"""Reject fenced code examples that reference pre-OKF root knowledge paths."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TOP_LEVEL_AREAS = (
    "ai",
    "ai-agents",
    "assets",
    "cloud",
    "cross-topic-guides",
    "databases",
    "decision-records",
    "devops",
    "finops",
    "git",
    "kubernetes",
    "llm",
    "migrations",
    "ml",
    "mlops",
    "programming-languages",
    "security",
    "solutions-architect",
    "templates",
    "terraform",
)
PATH = re.compile(r"(?<![A-Za-z0-9_.:/-])(" + "|".join(map(re.escape, TOP_LEVEL_AREAS)) + r")/")


def outdated_paths(markdown: str) -> list[tuple[int, str]]:
    errors: list[tuple[int, str]] = []
    in_fence = False
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and PATH.search(line) and not re.match(r"^\s+[A-Za-z0-9_.-]+/$", line):
            errors.append((line_number, line.strip()))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", nargs="?", default="knowledge", type=Path)
    args = parser.parse_args()

    errors = []
    for path in sorted(args.bundle.rglob("*.md")):
        for line_number, line in outdated_paths(path.read_text(encoding="utf-8")):
            errors.append(f"{path}:{line_number}: pre-OKF path in fenced code: {line}")
    if errors:
        print("\n".join(errors))
        print(f"Command-path validation failed with {len(errors)} error(s).")
        return 1
    print(f"Command-path validation passed for {args.bundle}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
