#!/usr/bin/env python3
"""Fixture tests for the GitHub issue-template validator."""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-issue-templates.py"

spec = importlib.util.spec_from_file_location("issue_template_validator", VALIDATOR_PATH)
if spec is None or spec.loader is None:  # pragma: no cover - defensive import guard
    raise SystemExit(f"Cannot load validator from {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def write(path: Path, contents: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents)
    return path


def assert_contains(errors: list[str], expected: str) -> None:
    joined = "\n".join(errors)
    if expected not in joined:
        raise AssertionError(f"expected {expected!r} in errors:\n{joined}")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix=".issue-template-validator-", dir=ROOT))
    try:
        valid_labels = write(
            tmp / "labels.yml",
            """
- name: documentation
  color: "0075ca"
  description: Documentation work
- name: validation
  color: "5319e7"
  description: Validation work
""".strip()
            + "\n",
        )
        labels, errors = validator.validate_label_manifest(valid_labels)
        assert labels == {"documentation", "validation"}
        assert errors == []

        bad_labels = write(
            tmp / "bad-labels.yml",
            """
- name: documentation
  color: "0075ca"
  description: Documentation work
- name: documentation
  color: "not-a-color"
  description: Duplicate with bad color
""".strip()
            + "\n",
        )
        _, errors = validator.validate_label_manifest(bad_labels)
        assert_contains(errors, "duplicate label 'documentation'")
        assert_contains(errors, "color must be a six-character hex string without #")

        valid_template = write(
            tmp / "valid-template.yml",
            """
name: Valid
labels:
  - documentation
description: Valid template
title: "docs: "
body:
  - type: input
    id: page
    attributes:
      label: Page
    validations:
      required: true
""".strip()
            + "\n",
        )
        assert validator.validate_template(valid_template, labels) == []

        undeclared_label_template = write(
            tmp / "undeclared-label-template.yml",
            """
name: Undeclared label
description: Should fail
title: "docs: "
labels:
  - missing-label
body:
  - type: input
    id: page
    attributes:
      label: Page
""".strip()
            + "\n",
        )
        errors = validator.validate_template(undeclared_label_template, labels)
        assert_contains(errors, "labels are not declared in .github/labels.yml: missing-label")

        duplicate_id_template = write(
            tmp / "duplicate-id-template.yml",
            """
name: Duplicate id
description: Should fail
title: "docs: "
labels:
  - documentation
body:
  - type: input
    id: page
    attributes:
      label: Page
  - type: textarea
    id: page
    attributes:
      label: More detail
""".strip()
            + "\n",
        )
        errors = validator.validate_template(duplicate_id_template, labels)
        assert_contains(errors, "duplicate body id 'page'")
    finally:
        shutil.rmtree(tmp)

    print("Issue template validator fixtures passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
