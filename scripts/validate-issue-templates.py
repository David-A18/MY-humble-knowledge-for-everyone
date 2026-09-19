#!/usr/bin/env python3
"""Validate GitHub issue form YAML files for repository conventions."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only when dependency is missing
    raise SystemExit(
        "PyYAML is required. Install it with `python -m pip install PyYAML`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
ALLOWED_TYPES = {"checkboxes", "dropdown", "input", "markdown", "textarea"}
REQUIRED_TOP_LEVEL = {"name", "description", "title", "labels", "body"}


def fail(path: Path, message: str) -> str:
    return f"{path.relative_to(ROOT)}: {message}"


def validate_template(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        return [fail(path, f"invalid YAML: {exc}")]

    if not isinstance(data, dict):
        return [fail(path, "template must be a YAML mapping")]

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append(fail(path, f"missing top-level fields: {', '.join(missing)}"))

    for key in ["name", "description", "title"]:
        if key in data and not isinstance(data[key], str):
            errors.append(fail(path, f"{key} must be a string"))

    labels = data.get("labels")
    if labels is not None:
        if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
            errors.append(fail(path, "labels must be a list of strings"))

    body = data.get("body")
    if not isinstance(body, list) or not body:
        errors.append(fail(path, "body must be a non-empty list"))
        return errors

    seen_ids: set[str] = set()
    for index, item in enumerate(body, start=1):
        if not isinstance(item, dict):
            errors.append(fail(path, f"body item {index} must be a mapping"))
            continue

        item_type = item.get("type")
        if item_type not in ALLOWED_TYPES:
            errors.append(
                fail(
                    path,
                    f"body item {index} has unsupported type {item_type!r}; expected one of {sorted(ALLOWED_TYPES)}",
                )
            )
            continue

        attributes = item.get("attributes")
        if not isinstance(attributes, dict):
            errors.append(fail(path, f"body item {index} must have attributes mapping"))
            continue

        item_id = item.get("id")
        if item_type != "markdown":
            if not isinstance(item_id, str) or not item_id:
                errors.append(fail(path, f"body item {index} must have a non-empty id"))
            elif item_id in seen_ids:
                errors.append(fail(path, f"duplicate body id {item_id!r}"))
            else:
                seen_ids.add(item_id)

            if not isinstance(attributes.get("label"), str) or not attributes.get("label"):
                errors.append(fail(path, f"body item {index} must have an attributes.label string"))

        if item_type == "markdown" and not isinstance(attributes.get("value"), str):
            errors.append(fail(path, f"markdown body item {index} must have attributes.value"))

        if item_type == "dropdown":
            options = attributes.get("options")
            if not isinstance(options, list) or not options or not all(isinstance(option, str) for option in options):
                errors.append(fail(path, f"dropdown body item {index} must have string options"))

        validations = item.get("validations")
        if validations is not None:
            if not isinstance(validations, dict):
                errors.append(fail(path, f"body item {index} validations must be a mapping"))
            elif "required" in validations and not isinstance(validations["required"], bool):
                errors.append(fail(path, f"body item {index} validations.required must be boolean"))

    return errors


def main() -> int:
    paths = sorted(TEMPLATE_DIR.glob("*.yml")) + sorted(TEMPLATE_DIR.glob("*.yaml"))
    if not paths:
        print("No issue templates found.")
        return 0

    errors: list[str] = []
    for path in paths:
        errors.extend(validate_template(path))

    if errors:
        print("Issue template validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Issue template validation passed for {len(paths)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
