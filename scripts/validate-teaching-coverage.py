#!/usr/bin/env python3
"""Check teaching-wave accounting against the generated concept catalog.

This validates coverage bookkeeping, not the editorial quality of a page.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re


WAVE = re.compile(r"^### Wave \d+ \(", re.MULTILINE)
CONCEPT_LINK = re.compile(r"^\| \[[^]]+\]\((knowledge/[^)]+\.md)\) \|", re.MULTILINE)
SUMMARY_ROW = re.compile(r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", re.MULTILINE)
AREAS = {
    "ai": "AI, including the embedded OKF example",
    "cloud": "Cloud",
    "cross-topic-guides": "Cross-topic guides",
    "databases": "Databases",
    "decision-records": "Decision records",
    "devops": "DevOps",
    "finops": "FinOps",
    "git": "Git",
    "kubernetes": "Kubernetes",
    "migrations": "Migrations",
    "programming-languages": "Programming languages",
    "security": "Security",
    "solutions-architect": "Solutions architect",
    "templates": "Templates",
    "terraform": "Terraform",
}
ROOT_AREA = "Bundle root (Start here, glossary)"


def area_for(path: str) -> str:
    parts = Path(path).parts
    if len(parts) == 2 and parts[0] == "knowledge":
        return ROOT_AREA
    if len(parts) < 3 or parts[0] != "knowledge":
        raise ValueError(f"not a knowledge concept path: {path}")
    try:
        return AREAS[parts[1]]
    except KeyError as error:
        raise ValueError(f"unclassified knowledge area: {path}") from error


def authored_paths(plan: str) -> list[str]:
    start = plan.index("### Wave 1 (")
    end = plan.index("### Not yet reviewed against the teaching standard", start)
    section = plan[start:end]
    if not WAVE.search(section):
        raise ValueError("no teaching waves found")
    authored = []
    for line in section.splitlines():
        match = CONCEPT_LINK.match(line)
        if match and "Route order only" not in line:
            authored.append(match.group(1))
    return authored


def summary_rows(plan: str) -> dict[str, tuple[int, int, int]]:
    start = plan.index("### Not yet reviewed against the teaching standard")
    end = plan.index("### Candidates for the next wave", start)
    section = plan[start:end]
    rows = {}
    for name, total, authored, remaining in SUMMARY_ROW.findall(section):
        name = name.strip().replace("**", "")
        if name in {"Area", "Total"} or name.startswith("---"):
            if name == "Total":
                rows[name] = (int(total.strip().replace("**", "")),
                              int(authored.strip().replace("**", "")),
                              int(remaining.strip().replace("**", "")))
            continue
        # The first wave records a route edit without counting it as authored.
        authored_number = authored.strip().split(" ", 1)[0]
        rows[name] = (int(total.strip()), int(authored_number), int(remaining.strip()))
    return rows


def validate(catalog: dict, plan: str) -> list[str]:
    errors = []
    concepts = catalog.get("concepts")
    if not isinstance(concepts, list):
        return ["catalog has no concepts list"]
    catalog_paths = [item.get("path") for item in concepts if isinstance(item, dict)]
    if len(catalog_paths) != catalog.get("concept_count"):
        errors.append("catalog concept_count does not match its concepts list")
    if len(set(catalog_paths)) != len(catalog_paths):
        errors.append("catalog contains duplicate concept paths")
    known = set(catalog_paths)

    try:
        authored = authored_paths(plan)
        rows = summary_rows(plan)
    except (ValueError, IndexError) as error:
        return errors + [f"plan format: {error}"]
    duplicates = [path for path, count in Counter(authored).items() if count > 1]
    errors.extend(f"concept appears in multiple teaching waves: {path}" for path in duplicates)
    errors.extend(f"authored path absent from catalog: {path}" for path in authored if path not in known)

    try:
        by_area = Counter(area_for(path) for path in catalog_paths)
        authored_by_area = Counter(area_for(path) for path in set(authored) & known)
    except ValueError as error:
        return errors + [str(error)]
    expected_areas = set(by_area)
    if set(rows) != expected_areas | {"Total"}:
        errors.append(f"summary areas mismatch: expected {sorted(expected_areas)}, got {sorted(rows)}")
    for area in expected_areas & set(rows):
        actual = (by_area[area], authored_by_area[area], by_area[area] - authored_by_area[area])
        if rows[area] != actual:
            errors.append(f"{area}: summary {rows[area]} does not match catalog and waves {actual}")
    total = (len(catalog_paths), len(set(authored) & known), len(known - set(authored)))
    if rows.get("Total") != total:
        errors.append(f"Total: summary {rows.get('Total')} does not match catalog and waves {total}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("generated/knowledge-catalog.json"))
    parser.add_argument("--plan", type=Path, default=Path("knowledge-content-quality-expansion-plan.md"))
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    plan = args.plan.read_text(encoding="utf-8")
    errors = validate(catalog, plan)
    if errors:
        print("\n".join(errors))
        print(f"Teaching-coverage validation failed with {len(errors)} error(s).")
        return 1
    print(f"Teaching-coverage accounting passed: {len(authored_paths(plan))} of {catalog['concept_count']} concepts authored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
