#!/usr/bin/env python3
"""Exercise live-label comparison without credentials or a network request."""

from __future__ import annotations

import importlib.util
from io import BytesIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error

spec = importlib.util.spec_from_file_location(
    "label_validator", Path(__file__).with_name("check-github-labels.py")
)
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class GitHubLabelContracts(unittest.TestCase):
    def test_missing_cli_uses_paginated_public_rest(self):
        first = [
            {"name": f"label-{i}", "color": "ABCDEF", "description": None}
            for i in range(100)
        ]
        second = [{"name": "last", "color": "123456", "description": "Final label"}]
        responses = [BytesIO(json.dumps(page).encode()) for page in (first, second)]
        with patch.object(validator.subprocess, "run", side_effect=FileNotFoundError):
            with patch.object(validator.urllib.request, "urlopen", side_effect=responses) as call:
                with patch.dict(validator.os.environ, {}, clear=True):
                    actual = validator.fetch_github_labels("owner/repository")
        self.assertEqual(len(actual), 101)
        self.assertEqual(actual["label-0"], {"color": "abcdef", "description": ""})
        self.assertIn("page=2", call.call_args_list[1].args[0].full_url)

    def test_rest_failure_is_not_a_clean_result(self):
        with patch.object(
            validator.urllib.request, "urlopen", side_effect=urllib.error.URLError("unavailable")
        ):
            with self.assertRaisesRegex(SystemExit, "REST check failed"):
                validator.fetch_github_labels_rest("owner/repository")

    def test_missing_and_changed_labels_are_reported(self):
        expected = {"missing": {"color": "000000", "description": "Required"},
                    "changed": {"color": "ffffff", "description": "Expected"}}
        actual = {"changed": {"color": "000000", "description": "Old"}}
        errors = validator.compare_labels(expected, actual)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("missing GitHub label" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
