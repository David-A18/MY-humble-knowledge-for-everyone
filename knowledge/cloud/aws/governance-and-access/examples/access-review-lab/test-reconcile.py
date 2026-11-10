"""Exercise inventory join, review-time and coverage failure cases."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("reconciler", HERE / "reconcile.py")
reconciler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reconciler)
AS_OF = "2026-11-10T09:00:00Z"


class InventoryReview(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((HERE / "snapshot.json").read_text(encoding="utf-8"))

    def report(self, time=AS_OF):
        return reconciler.reconcile(self.data, time)

    def row(self, report, user):
        return next(row for row in report["potential_assignment_rows"] if row["user_id"] == user)

    def test_teaching_baseline(self):
        report = self.report()
        self.assertEqual(report["summary"], {"source_assignments": 4, "unique_user_account_set_rows": 3, "finding_count": 7})
        self.assertEqual(self.row(report, "user-alice")["current_review_records"], ["r-alice"])
        self.assertEqual(report["warnings"], [])

    def test_direct_and_group_paths_deduplicate_person_row(self):
        alice = self.row(self.report(), "user-alice")
        self.assertEqual(alice["assignment_paths"], ["a-direct", "a-group"])
        self.assertEqual(alice["findings"], [])

    def test_deleting_one_path_leaves_the_other(self):
        self.data["assignments"] = [a for a in self.data["assignments"] if a["id"] != "a-direct"]
        self.assertEqual(self.row(self.report(), "user-alice")["assignment_paths"], ["a-group"])

    def test_disabled_user_is_not_silently_dropped(self):
        row = self.row(self.report(), "user-departed")
        self.assertEqual(row["findings"], ["disabled_user_with_assignment", "no_current_review"])

    def test_expiry_boundary_and_newer_review(self):
        self.data["reviews"][0]["expires_at"] = AS_OF
        self.assertIn("expired_review", self.row(self.report(), "user-alice")["findings"])
        current = copy.deepcopy(self.data["reviews"][0])
        current.update(id="r-renewed", reviewed_at=AS_OF, expires_at="2026-12-01T00:00:00Z")
        self.data["reviews"].append(current)
        row = self.row(self.report(), "user-alice")
        self.assertEqual(row["current_review_records"], ["r-renewed"])
        self.assertNotIn("expired_review", row["findings"])

    def test_future_review_does_not_authorize_current_review(self):
        self.data["reviews"][0]["reviewed_at"] = "2026-11-11T00:00:00Z"
        row = self.row(self.report(), "user-alice")
        self.assertEqual(row["current_review_records"], [])
        self.assertIn("no_current_review", row["findings"])

    def test_empty_group_and_pending_provisioning_remain_visible(self):
        report = self.report()
        codes = {finding["code"] for finding in report["findings"]}
        self.assertIn("assigned_group_has_no_members", codes)
        self.assertIn("provisioning_not_confirmed", codes)
        self.assertEqual(self.row(report, "user-bob")["assignment_paths"], ["a-bob"])

    def test_duplicate_records_memberships_and_semantic_assignments(self):
        mutations = [lambda d: d["users"].append(copy.deepcopy(d["users"][0])),
                     lambda d: d["memberships"].append(copy.deepcopy(d["memberships"][0])),
                     lambda d: d["assignments"].append({**d["assignments"][0], "id": "different-source-id"})]
        for mutate in mutations:
            data = copy.deepcopy(self.data)
            mutate(data)
            with self.assertRaises(ValueError):
                reconciler.reconcile(data, AS_OF)

    def test_unknown_references_are_rejected(self):
        mutations = [lambda d: d["memberships"][0].update(user_id="missing"),
                     lambda d: d["assignments"][0].update(account_id="999999999999"),
                     lambda d: d["assignments"][0].update(principal_id="missing-group"),
                     lambda d: d["reviews"][0].update(permission_set_id="missing-set")]
        for mutate in mutations:
            data = copy.deepcopy(self.data)
            mutate(data)
            with self.assertRaises(ValueError):
                reconciler.reconcile(data, AS_OF)

    def test_incomplete_and_wrong_scope_are_rejected(self):
        for field, value in (("complete", False), ("complete", "true"), ("scope", "all-effective-permissions"), ("schema_version", True)):
            data = copy.deepcopy(self.data)
            data[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                reconciler.reconcile(data, AS_OF)

    def test_stale_and_future_snapshot_boundaries(self):
        self.assertIn("stale_snapshot", self.report("2026-11-11T09:00:00Z")["warnings"])
        self.assertEqual(self.report("2026-11-11T08:00:00Z")["warnings"], [])
        with self.assertRaises(ValueError):
            self.report("2026-11-10T07:59:59Z")

    def test_normalized_types_timezone_and_review_intervals(self):
        mutations = [lambda d: d["users"][0].update(enabled="false"),
                     lambda d: d["assignments"][0].update(principal_id=[]),
                     lambda d: d["assignments"][0].update(provisioning="MAYBE"),
                     lambda d: d["reviews"][0].update(expires_at="2026-10-01T00:00:00Z"),
                     lambda d: d.update(snapshot_at="2026-11-10T08:00:00")]
        for mutate in mutations:
            data = copy.deepcopy(self.data)
            mutate(data)
            with self.assertRaises(ValueError):
                reconciler.reconcile(data, AS_OF)
        self.assertEqual(reconciler.timestamp("2026-11-10T10:00:00+01:00"), reconciler.timestamp(AS_OF))

    def test_duplicate_json_and_no_permission_claim(self):
        with self.assertRaises(ValueError):
            json.loads('{"complete":true,"complete":false}', object_pairs_hook=reconciler.unique_keys)
        claims = self.report()["claims"]
        self.assertTrue(claims["synthetic_only"])
        self.assertTrue(all(value is False for key, value in claims.items() if key != "synthetic_only"))

    def test_cli_finding_exit_code_and_fixture_unchanged(self):
        before = (HERE / "snapshot.json").read_bytes()
        result = subprocess.run([sys.executable, str(HERE / "reconcile.py"), "--fail-on-findings"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["finding_count"], 7)
        self.assertEqual(before, (HERE / "snapshot.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
