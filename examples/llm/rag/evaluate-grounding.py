"""Measure paraphrase retrieval and citation support on a small fixed RAG corpus."""

import argparse
import json
from pathlib import Path
import re
import tempfile

import rag


SOURCES = {
    "current": "The current Juniper deployment approval window is 30 minutes.",
    "legacy": "The legacy Juniper deployment approval window was 60 minutes.",
    "unrelated": "The Cedar deployment approval window is 15 minutes.",
}
CASES = [
    ("direct", "What is the current Juniper deployment approval window?", ("current",), True),
    ("paraphrase", "For a Juniper deployment, what is the current approval window?", ("current",), True),
    ("low-overlap", "How many minutes can approval wait for a Juniper deployment today?", ("current",), False),
    ("conflict", "Juniper: what is the approval window for current and legacy deployment?", ("current", "legacy"), True),
    ("conflict-paraphrase", "Compare the current and legacy Juniper deployment approval windows.", ("current", "legacy"), False),
]
CLAIMS = {"30": "current", "60": "legacy", "15": "unrelated"}
PERIOD = {
    "current": re.compile(r"\b(?:current|today|now|present)\b", re.I),
    "legacy": re.compile(r"\b(?:legacy|previous|past|old)\b", re.I),
}
DURATION = re.compile(r"\b(\d+)\s*(?:minutes?|mins?)\b", re.I)
CITATION = re.compile(r"\[(\d+)\]")


def make_corpus(root):
    docs = root / "knowledge" / "devops"
    docs.mkdir(parents=True)
    for name, source in SOURCES.items():
        (docs / f"{name}.md").write_text(
            f"# {name.title()} approval window\n\n{source}\n", encoding="utf-8"
        )


def score_answer(answer, hits, expected):
    """Match seeded values to their own citations within the same clause."""
    supported = set()
    problems = []
    for clause in re.split(r"[\n;.!?]+", answer):
        references = {int(value) for value in CITATION.findall(clause)}
        cited = {hits[index - 1]["path"] for index in references if 1 <= index <= len(hits)}
        if any(index < 1 or index > len(hits) for index in references):
            problems.append("citation outside evidence")
        values = set(DURATION.findall(CITATION.sub("", clause)))
        if len(values) > 1:
            problems.append("state each duration and supporting citation in its own clause")
        for value in sorted(values):
            name = CLAIMS.get(value)
            if name is None:
                problems.append(f"unknown duration {value}")
            elif name not in expected:
                problems.append(f"unexpected value from {name}")
            elif not PERIOD[name].search(clause) or any(
                pattern.search(clause) for other, pattern in PERIOD.items() if other != name
            ):
                problems.append(f"{name} claim lacks an unambiguous time period")
            elif f"knowledge/devops/{name}.md" not in cited:
                problems.append(f"{name} claim lacks its supporting citation")
            else:
                supported.add(name)
    problems.extend(f"missing supported {name} claim" for name in expected if name not in supported)
    return {"passed": not problems, "problems": problems}


def fixture_answers(hits, expected):
    indices = {Path(hit["path"]).stem: i for i, hit in enumerate(hits, 1)}
    correct = "\n".join(f"{SOURCES[name][:-1]} [{indices[name]}]." for name in expected)
    wrong = next(i for name, i in indices.items() if name != expected[0])
    misattributed = correct.replace(f"[{indices[expected[0]]}]", f"[{wrong}]", 1)
    uncited = CITATION.sub("", correct)
    invented = "The current approval window is 45 minutes [" + str(indices[expected[0]]) + "]."
    reversed_period = correct.replace("current", "legacy", 1)
    return correct, misattributed, uncited, invented, reversed_period


def evaluate(root, model, timeout):
    make_corpus(root)
    db = root / "index.sqlite"
    index = rag.ingest(root, db)
    results = []
    for case, question, expected, expected_sufficient in CASES:
        result = rag.search(db, question, k=8)
        paths = {hit["path"] for hit in result["hits"]}
        needed = {f"knowledge/devops/{name}.md" for name in expected}
        row = {
            "case": case, "retrieved": needed <= paths,
            "coverage": result["best_coverage"], "sufficient": result["sufficient"],
            "expected_sufficient": expected_sufficient,
        }
        if row["retrieved"]:
            row["scorer_controls"] = [
                score_answer(candidate, result["hits"], expected)["passed"]
                for candidate in fixture_answers(result["hits"], expected)
            ]
        if model:
            try:
                generated = rag.ask(db, question, model=model, timeout=timeout)
                if result["sufficient"]:
                    row["model"] = score_answer(generated["answer"], generated["hits"], expected)
                else:
                    row["model"] = {"expected_refusal": generated["answer"] == "NO_EVIDENCE"}
            except (OSError, ValueError) as exc:
                row["model"] = {"passed": False, "problems": [str(exc)]}
        results.append(row)
    return {"index": index, "model": model, "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", help="optional installed Ollama model")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="rag-grounding-") as directory:
        report = evaluate(Path(directory), args.model, args.timeout)
    print(json.dumps(report, indent=2))
    passed = all(
        row["retrieved"] and row["sufficient"] == row["expected_sufficient"]
        and row["scorer_controls"] == [True, False, False, False, False]
        and (not args.model or row["model"].get("passed", row["model"].get("expected_refusal", False)))
        for row in report["cases"]
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
