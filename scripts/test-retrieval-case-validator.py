#!/usr/bin/env python3
"""Fixture tests for retrieval-case validation entry points."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

script = Path(__file__).with_name("validate-retrieval-cases.py")
with tempfile.TemporaryDirectory(prefix="retrieval-cases-") as temporary:
    root = Path(temporary)
    catalog = root / "catalog.json"
    cases = root / "cases.yaml"
    catalog.write_text(json.dumps({"concepts": [{"path": "knowledge/example.md", "source_ids": ["example-source"]}]}), encoding="utf-8")
    cases.write_text("""version: \"1\"\ncases:\n  - id: example\n    question: Example?\n    expected_paths: [knowledge/example.md]\n    required_source_ids: [example-source]\n""", encoding="utf-8")
    result = subprocess.run(["python3", str(script), "--catalog", str(catalog), "--cases", str(cases)], check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    cases.write_text(cases.read_text(encoding="utf-8").replace("example-source", "missing-source"), encoding="utf-8")
    result = subprocess.run(["python3", str(script), "--catalog", str(catalog), "--cases", str(cases)], check=False, capture_output=True, text=True)
    assert result.returncode == 1
print("Retrieval-case validator fixtures passed.")
