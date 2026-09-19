#!/usr/bin/env python3
"""Compare .github/labels.yml with labels in a GitHub repository."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only when dependency is missing
    raise SystemExit(
        "PyYAML is required. Install it with `python -m pip install PyYAML`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
LABELS_FILE = ROOT / ".github" / "labels.yml"


def load_declared_labels(path: Path) -> dict[str, dict[str, str]]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, list):
        raise SystemExit(f"{path.relative_to(ROOT)} must be a list")

    labels: dict[str, dict[str, str]] = {}
    for item in data:
        if not isinstance(item, dict):
            raise SystemExit(f"{path.relative_to(ROOT)} contains a non-mapping label")
        name = item.get("name")
        color = item.get("color")
        description = item.get("description")
        if not all(isinstance(value, str) and value for value in [name, color, description]):
            raise SystemExit(f"{path.relative_to(ROOT)} labels need name, color, and description")
        labels[name] = {"color": color.lower(), "description": description}
    return labels


def fetch_github_labels(repo: str) -> dict[str, dict[str, str]]:
    command = [
        "gh",
        "label",
        "list",
        "--repo",
        repo,
        "--limit",
        "1000",
        "--json",
        "name,color,description",
    ]
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("GitHub CLI `gh` is required for live label checks.") from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.stderr.strip() or "gh label list failed") from exc

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Could not parse gh output as JSON: {exc}") from exc

    labels: dict[str, dict[str, str]] = {}
    for item in data:
        labels[item["name"]] = {
            "color": item.get("color", "").lower(),
            "description": item.get("description") or "",
        }
    return labels


def compare_labels(
    declared: dict[str, dict[str, str]],
    actual: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    for name, expected in sorted(declared.items()):
        if name not in actual:
            errors.append(f"missing GitHub label: {name}")
            continue

        found = actual[name]
        if found["color"] != expected["color"]:
            errors.append(
                f"label {name!r} color mismatch: expected {expected['color']}, found {found['color']}"
            )
        if found["description"] != expected["description"]:
            errors.append(
                f"label {name!r} description mismatch: expected {expected['description']!r}, found {found['description']!r}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub repository, for example owner/name")
    args = parser.parse_args()

    declared = load_declared_labels(LABELS_FILE)
    actual = fetch_github_labels(args.repo)
    errors = compare_labels(declared, actual)
    if errors:
        print("GitHub label check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"GitHub label check passed for {len(declared)} declared labels in {args.repo}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
