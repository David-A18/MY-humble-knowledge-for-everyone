#!/usr/bin/env python3
"""Exercise the coverage check against the real tracker and catalog."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("validate-teaching-coverage.py")
SPEC = importlib.util.spec_from_file_location("teaching_coverage", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CATALOG = json.loads(Path("generated/knowledge-catalog.json").read_text(encoding="utf-8"))
PLAN = Path("knowledge-content-quality-expansion-plan.md").read_text(encoding="utf-8")


class TeachingCoverageTests(unittest.TestCase):
    def test_current_accounting(self) -> None:
        self.assertEqual(MODULE.validate(CATALOG, PLAN), [])

    def test_duplicate_wave_entry_is_rejected(self) -> None:
        changed = PLAN.replace(
            "| [Bootstrapping a system](knowledge/programming-languages/bootstrapping-a-system.md)",
            "| [Git fundamentals](knowledge/git/git-fundamentals.md)",
            1,
        )
        self.assertNotEqual(changed, PLAN)
        self.assertTrue(any("multiple teaching waves" in error for error in MODULE.validate(CATALOG, changed)))

    def test_incorrect_summary_is_rejected(self) -> None:
        changed = PLAN.replace(
            "| **Total** | **165** | **24** | **141** |",
            "| **Total** | **165** | **25** | **140** |",
            1,
        )
        self.assertNotEqual(changed, PLAN)
        self.assertTrue(any("Total: summary" in error for error in MODULE.validate(CATALOG, changed)))

    def test_missing_catalog_path_is_rejected(self) -> None:
        changed = PLAN.replace(
            "knowledge/programming-languages/bootstrapping-a-system.md",
            "knowledge/programming-languages/nonexistent.md",
            1,
        )
        self.assertNotEqual(changed, PLAN)
        self.assertTrue(any("absent from catalog" in error for error in MODULE.validate(CATALOG, changed)))


if __name__ == "__main__":
    unittest.main()
