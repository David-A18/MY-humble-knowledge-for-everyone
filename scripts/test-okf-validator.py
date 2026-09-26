#!/usr/bin/env python3
"""Fixture tests for the repository OKF v0.2 profile validator."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate-okf.py")
SPEC = importlib.util.spec_from_file_location("validate_okf", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


VALID_CONCEPT = """---
type: Reference
title: Example
description: A valid example concept.
tags: [example]
status: draft
maturity: draft
audience: Readers
maintainer: unassigned
---

# Example
"""


with tempfile.TemporaryDirectory(prefix="okf-validator-") as temporary:
    root = Path(temporary)
    write(root, "index.md", "---\nokf_version: \"0.2\"\n---\n\n# Root\n\n- [Example](example.md)\n")
    write(root, "log.md", "# Log\n\n## 2026-09-20\n\n- **Creation**: Example.\n")
    write(root, "example.md", VALID_CONCEPT)
    assert MODULE.validate_bundle(root) == []

    write(root, "example.md", "# Missing frontmatter\n")
    assert any("missing YAML frontmatter" in error for error in MODULE.validate_bundle(root))

    write(root, "example.md", VALID_CONCEPT)
    write(root, "nested/index.md", "---\ntype: Reference\n---\n")
    assert any("nested index files" in error for error in MODULE.validate_bundle(root))

    write(root, "nested/index.md", "# Nested\n")
    write(root, "log.md", "# Log\n\n## 2026-01-01\n\n- Old.\n\n## 2026-09-20\n\n- New.\n")
    assert any("newest first" in error for error in MODULE.validate_bundle(root))

print("OKF validator fixtures passed.")
