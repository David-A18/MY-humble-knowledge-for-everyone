"""Mutation tests for bounded fixture regression checks, not IAM decisions."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("contracts", HERE / "check-contracts.py")
contracts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contracts)


class Contracts(unittest.TestCase):
    def setUp(self):
        self.trust = contracts.read_policy(HERE / "irsa-trust.json")
        self.permission = contracts.read_policy(HERE / "read-policy.json")

    def test_fixture_baseline(self):
        contracts.check_trust(self.trust)
        contracts.check_permission(self.permission)

    def test_permission_action_expansion(self):
        for action in ("s3:*", ["s3:GetObject", "s3:PutObject"], "s3:DeleteObject"):
            with self.subTest(action=action):
                self.permission["Statement"][0]["Action"] = action
                with self.assertRaises(ValueError):
                    contracts.check_permission(self.permission)

    def test_permission_scope_broadening(self):
        for resource in ("*", "arn:aws:s3:::example-lab-bucket/*", "arn:aws:s3:::example-lab-bucket/public-lab*", "arn:aws:s3:::another-bucket/public-lab/*"):
            with self.subTest(resource=resource):
                self.permission["Statement"][0]["Resource"] = resource
                with self.assertRaises(ValueError):
                    contracts.check_permission(self.permission)

    def test_extra_statement_or_unknown_field(self):
        for mutate in (lambda p: p["Statement"].append(copy.deepcopy(p["Statement"][0])),
                       lambda p: p["Statement"][0].update(NotAction="s3:DeleteObject"),
                       lambda p: p.update(Unexpected=True)):
            policy = copy.deepcopy(self.permission)
            mutate(policy)
            with self.assertRaises(ValueError):
                contracts.check_permission(policy)

    def test_wrong_version_and_statement_shape(self):
        for policy in ({**self.permission, "Version": "2008-10-17"},
                       {**self.permission, "Statement": self.permission["Statement"][0]},
                       {**self.permission, "Statement": []}, {"Version": "2012-10-17", "Statement": [None]}):
            with self.subTest(policy=policy), self.assertRaises(ValueError):
                contracts.check_permission(policy)

    def test_wrong_principal_and_action(self):
        for field, value in (("Principal", "*"), ("Principal", {"Federated": "arn:aws:iam::999999999999:oidc-provider/other"}), ("Action", "sts:AssumeRole"), ("Effect", "Deny")):
            policy = copy.deepcopy(self.trust)
            policy["Statement"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                contracts.check_trust(policy)

    def test_subject_and_audience_expansion(self):
        for claim, value in (("sub", "system:serviceaccount:irsa-lab:*"), ("sub", "system:serviceaccount:other:s3-reader"), ("aud", "pods.eks.amazonaws.com")):
            policy = copy.deepcopy(self.trust)
            policy["Statement"][0]["Condition"]["StringEquals"][f"{contracts.ISSUER}:{claim}"] = value
            with self.subTest(claim=claim, value=value), self.assertRaises(ValueError):
                contracts.check_trust(policy)

    def test_missing_claim_or_changed_operator(self):
        for field in ("aud", "sub"):
            policy = copy.deepcopy(self.trust)
            del policy["Statement"][0]["Condition"]["StringEquals"][f"{contracts.ISSUER}:{field}"]
            with self.assertRaises(ValueError):
                contracts.check_trust(policy)
        policy = copy.deepcopy(self.trust)
        policy["Statement"][0]["Condition"]["StringLike"] = policy["Statement"][0]["Condition"].pop("StringEquals")
        with self.assertRaises(ValueError):
            contracts.check_trust(policy)

    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):
            json.loads('{"Effect":"Allow","Effect":"Deny"}', object_pairs_hook=contracts.unique_keys)

    def test_reordered_fields_and_cli(self):
        policy = json.loads(json.dumps(self.permission, sort_keys=True))
        contracts.check_permission(policy)
        before = (HERE / "read-policy.json").read_bytes()
        result = subprocess.run([sys.executable, str(HERE / "check-contracts.py")], capture_output=True, text=True, check=True)
        self.assertIn("No IAM authorization", result.stdout)
        self.assertEqual(before, (HERE / "read-policy.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
