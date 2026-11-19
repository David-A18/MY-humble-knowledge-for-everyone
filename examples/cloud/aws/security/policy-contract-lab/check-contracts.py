"""Check this lab's fixture contract; never simulates IAM or contacts AWS."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ISSUER = "oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE"
PROVIDER = f"arn:aws:iam::123456789012:oidc-provider/{ISSUER}"
SUBJECT = "system:serviceaccount:irsa-lab:s3-reader"
OBJECTS = "arn:aws:s3:::example-lab-bucket/public-lab/*"


def unique_keys(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_policy(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def one_statement(policy: dict) -> dict:
    if not isinstance(policy, dict) or set(policy) != {"Version", "Statement"}:
        raise ValueError("Fixture requires only Version and Statement")
    if policy["Version"] != "2012-10-17":
        raise ValueError("Unexpected policy version")
    statements = policy["Statement"]
    if not isinstance(statements, list) or len(statements) != 1 or not isinstance(statements[0], dict):
        raise ValueError("Fixture requires exactly one statement in a list")
    return statements[0]


def check_trust(policy: dict) -> None:
    statement = one_statement(policy)
    if set(statement) != {"Effect", "Principal", "Action", "Condition"}:
        raise ValueError("Unexpected trust fields")
    if statement["Effect"] != "Allow" or statement["Action"] != "sts:AssumeRoleWithWebIdentity":
        raise ValueError("Unexpected trust effect/action")
    if statement["Principal"] != {"Federated": PROVIDER}:
        raise ValueError("Trust must name the exact synthetic OIDC provider")
    expected = {"StringEquals": {f"{ISSUER}:aud": "sts.amazonaws.com", f"{ISSUER}:sub": SUBJECT}}
    if statement["Condition"] != expected:
        raise ValueError("Trust must retain exact audience and subject conditions")


def check_permission(policy: dict) -> None:
    statement = one_statement(policy)
    if set(statement) != {"Effect", "Action", "Resource"}:
        raise ValueError("Unexpected permission fields")
    if statement != {"Effect": "Allow", "Action": "s3:GetObject", "Resource": OBJECTS}:
        raise ValueError("Permission must remain one synthetic-prefix GetObject grant")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    check_trust(read_policy(args.directory / "irsa-trust.json"))
    check_permission(read_policy(args.directory / "read-policy.json"))
    print("Both fixture contracts pass. No IAM authorization or AWS runtime was tested.")


if __name__ == "__main__":
    main()
