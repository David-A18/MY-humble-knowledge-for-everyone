#!/usr/bin/env python3
"""Score the RAG lab against golden retrieval cases, using a disposable index."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import yaml


def load_rag(path: Path):
    spec = importlib.util.spec_from_file_location("rag", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank_of(hits: list[dict], expected: list[str]) -> int | None:
    """Return the 1-based concept rank of the first expected path."""
    concepts: list[str] = []
    for hit in hits:
        if hit["path"] not in concepts:
            concepts.append(hit["path"])
    for rank, path in enumerate(concepts, 1):
        if path in expected:
            return rank
    return None


def area(path: str) -> str:
    parts = path.split("/")
    return parts[1] if len(parts) > 2 else "(root)"


def score(rag, database: Path, cases: list[dict], k: int) -> dict:
    ranks: list[int | None] = []
    context: list[int] = []
    misses = []
    per_area: dict[str, list[int | None]] = defaultdict(list)
    for case in cases:
        result = rag.search(database, case["question"], k=k)
        rank = rank_of(result["hits"], case["expected_paths"])
        ranks.append(rank)
        context.append(result["context_characters"])
        per_area[area(case["expected_paths"][0])].append(rank)
        if rank is None or rank > 3:
            misses.append({"id": case["id"], "rank": rank, "question": case["question"],
                           "got": [hit["path"] for hit in result["hits"][:3]]})
    total = len(ranks) or 1
    within = lambda limit, values=ranks: sum(1 for r in values if r and r <= limit) / (len(values) or 1)
    return {
        "cases": len(ranks),
        "hit_at_1": round(within(1), 3),
        "hit_at_3": round(within(3), 3),
        "hit_at_5": round(within(5), 3),
        "mrr": round(sum(1 / r for r in ranks if r) / total, 3),
        "mean_context_characters": round(sum(context) / total),
        "per_area_hit_at_3": {name: round(within(3, values), 3) for name, values in sorted(per_area.items())},
        "misses": misses,
    }


def score_abstention(rag, database: Path, questions: list[str], k: int) -> dict:
    answered = [q for q in questions if rag.search(database, q, k=k)["sufficient"]]
    return {"cases": len(questions), "correctly_refused": len(questions) - len(answered), "wrongly_answered": answered}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument("--rag", default="knowledge/llm/rag/examples/rag.py", type=Path)
    parser.add_argument("--cases", default=[Path("tests/retrieval-cases.yaml")], nargs="+", type=Path)
    parser.add_argument("--unanswerable", type=Path, help="YAML list of questions the corpus cannot answer")
    parser.add_argument("--k", default=8, type=int)
    parser.add_argument("--min-hit-at-3", type=float, help="fail below this score on any case file")
    parser.add_argument("--min-refused", type=float, help="fail below this refused fraction")
    parser.add_argument("--show-misses", action="store_true")
    args = parser.parse_args()

    rag = load_rag(args.rag)
    failed = False
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "index.sqlite"
        summary = {"index": rag.ingest(args.root, database)}
        for path in args.cases:
            cases = yaml.safe_load(path.read_text(encoding="utf-8"))["cases"]
            report = score(rag, database, cases, args.k)
            if not args.show_misses:
                report.pop("misses")
            summary[path.name] = report
            if args.min_hit_at_3 is not None and report["hit_at_3"] < args.min_hit_at_3:
                print(f"{path}: hit@3 {report['hit_at_3']} is below {args.min_hit_at_3}", file=sys.stderr)
                failed = True
        if args.unanswerable:
            questions = yaml.safe_load(args.unanswerable.read_text(encoding="utf-8"))["questions"]
            report = score_abstention(rag, database, questions, args.k)
            summary[args.unanswerable.name] = report
            if args.min_refused is not None and report["correctly_refused"] / report["cases"] < args.min_refused:
                print(f"{args.unanswerable}: refused too few unanswerable questions", file=sys.stderr)
                failed = True
    print(json.dumps(summary, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
