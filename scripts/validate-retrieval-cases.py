#!/usr/bin/env python3
"""Validate retrieval golden-set cases against the generated knowledge catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default="generated/knowledge-catalog.json", type=Path)
    parser.add_argument("--cases", default="tests/retrieval-cases.yaml", type=Path)
    args = parser.parse_args()

    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    cases = yaml.safe_load(args.cases.read_text(encoding="utf-8"))
    if not isinstance(cases, dict) or not isinstance(cases.get("cases"), list):
        print(f"{args.cases}: cases must contain a cases list")
        return 1

    by_path = {concept["path"]: concept for concept in catalog["concepts"]}
    errors = []
    seen_ids = set()
    for case in cases["cases"]:
        if not isinstance(case, dict) or not all(case.get(field) for field in ("id", "question", "expected_paths")):
            errors.append(f"invalid retrieval case: {case!r}")
            continue
        if case["id"] in seen_ids:
            errors.append(f"duplicate retrieval case id: {case['id']}")
        seen_ids.add(case["id"])
        expected = case["expected_paths"]
        if not isinstance(expected, list):
            errors.append(f"{case['id']}: expected_paths must be a list")
            continue
        concepts = []
        for path in expected:
            concept = by_path.get(path)
            if concept is None:
                errors.append(f"{case['id']}: expected path is not a catalog concept: {path}")
            else:
                concepts.append(concept)
        source_ids = {source_id for concept in concepts for source_id in concept.get("source_ids", [])}
        for source_id in case.get("required_source_ids", []):
            if source_id not in source_ids:
                errors.append(f"{case['id']}: required source id is absent from expected concepts: {source_id}")
    if errors:
        print("\n".join(errors))
        print(f"Retrieval-case validation failed with {len(errors)} error(s).")
        return 1
    print(f"Retrieval-case validation passed for {len(cases['cases'])} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
