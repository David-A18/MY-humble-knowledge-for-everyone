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
LABELS_FILE = ROOT / ".github" / "labels.yml"
ALLOWED_TYPES = {"checkboxes", "dropdown", "input", "markdown", "textarea"}
REQUIRED_TOP_LEVEL = {"name", "description", "title", "labels", "body"}
REQUIRED_LABEL_FIELDS = {"name", "color", "description"}


def fail(path: Path, message: str) -> str:
    return f"{path.relative_to(ROOT)}: {message}"


def validate_label_manifest(path: Path) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    if not path.exists():
        return set(), [fail(path, "label manifest is missing")]

    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        return set(), [fail(path, f"invalid YAML: {exc}")]

    if not isinstance(data, list) or not data:
        return set(), [fail(path, "label manifest must be a non-empty list")]

    labels: set[str] = set()
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(fail(path, f"label item {index} must be a mapping"))
            continue

        missing = sorted(REQUIRED_LABEL_FIELDS - set(item))
        if missing:
            errors.append(fail(path, f"label item {index} missing fields: {', '.join(missing)}"))

        name = item.get("name")
        if not isinstance(name, str) or not name:
            errors.append(fail(path, f"label item {index} must have a non-empty name"))
        elif name in labels:
            errors.append(fail(path, f"duplicate label {name!r}"))
        else:
            labels.add(name)

        color = item.get("color")
        if not isinstance(color, str) or len(color) != 6 or any(char not in "0123456789abcdefABCDEF" for char in color):
            errors.append(fail(path, f"label item {index} color must be a six-character hex string without #"))

        description = item.get("description")
        if not isinstance(description, str) or not description:
            errors.append(fail(path, f"label item {index} must have a non-empty description"))

    return labels, errors


def validate_template(path: Path, declared_labels: set[str]) -> list[str]:
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
        else:
            unknown_labels = sorted(set(labels) - declared_labels)
            if unknown_labels:
                errors.append(fail(path, f"labels are not declared in .github/labels.yml: {', '.join(unknown_labels)}"))

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

    declared_labels, errors = validate_label_manifest(LABELS_FILE)
    for path in paths:
        errors.extend(validate_template(path, declared_labels))

    if errors:
        print("Issue template validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Issue template validation passed for {len(paths)} files and {len(declared_labels)} declared labels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
