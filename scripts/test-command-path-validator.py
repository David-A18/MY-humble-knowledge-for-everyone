#!/usr/bin/env python3
"""Fixture tests for the fenced command-path validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path

module_path = Path(__file__).with_name("validate-command-paths.py")
spec = importlib.util.spec_from_file_location("validate_command_paths", module_path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

assert module.outdated_paths("```bash\ncp terraform/example.tf /tmp/\n```")
assert not module.outdated_paths("```bash\ncp knowledge/terraform/example.tf /tmp/\n```")
assert not module.outdated_paths("```text\n  assets/\n```")
assert not module.outdated_paths("Outside a fence terraform/example.tf is documentation prose.")
print("Command-path validator fixtures passed.")
