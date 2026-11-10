"""Reconcile a synthetic assignment snapshot; never contacts AWS or evaluates IAM."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys

TABLES = ("users", "groups", "memberships", "accounts", "permission_sets", "assignments", "reviews")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value):
    require(isinstance(value, str), "Timestamp must be a string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Invalid timestamp") from error
    require(parsed.tzinfo is not None and parsed.utcoffset() is not None, "Timestamp needs an explicit timezone")
    return parsed.astimezone(timezone.utc)


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def records(rows, fields, table):
    require(isinstance(rows, list), table + " must be a list")
    result = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == fields, "Unexpected fields in " + table)
        require(all(isinstance(row[field], str) for field in fields - {"enabled"}), "Expected normalized string fields in " + table)
        identifier = row["id"]
        require(isinstance(identifier, str) and bool(identifier.strip()), "Missing stable ID in " + table)
        require(identifier not in result, "Duplicate ID in " + table)
        result[identifier] = row
    return result


def reconcile(data, as_of, max_age_hours=24):
    require(isinstance(data, dict) and set(data) == {"schema_version", "scope", "complete", "snapshot_at", *TABLES}, "Unexpected snapshot fields")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "Unsupported teaching schema")
    require(data["scope"] == "synthetic-permission-set-assignments-only", "Unsupported inventory scope")
    require(data["complete"] is True, "Incomplete input cannot support this scoped reconciliation")
    as_of = timestamp(as_of)
    collected = timestamp(data["snapshot_at"])
    require(collected <= as_of, "Snapshot is later than the review time")
    require(type(max_age_hours) is int and 0 < max_age_hours <= 8760, "Invalid review freshness threshold")
    users = records(data["users"], {"id", "enabled"}, "users")
    groups = records(data["groups"], {"id"}, "groups")
    accounts = records(data["accounts"], {"id", "owner", "lifecycle"}, "accounts")
    sets = records(data["permission_sets"], {"id", "name"}, "permission_sets")
    assignments = records(data["assignments"], {"id", "account_id", "principal_type", "principal_id", "permission_set_id", "provisioning"}, "assignments")
    reviews = records(data["reviews"], {"id", "user_id", "account_id", "permission_set_id", "reviewer", "reviewed_at", "expires_at"}, "reviews")
    for user in users.values():
        require(type(user["enabled"]) is bool, "User enabled must be boolean")
    for account in accounts.values():
        require(re.fullmatch(r"[0-9]{12}", account["id"]) is not None, "Teaching account ID must have twelve digits")
        require(isinstance(account["owner"], str), "Owner must be a string")
        require(account["lifecycle"] in ("active", "retiring"), "Unsupported normalized account lifecycle")
    for permission_set in sets.values():
        require(isinstance(permission_set["name"], str) and permission_set["name"].strip(), "Missing permission-set display name")
    require(isinstance(data["memberships"], list), "Memberships must be a list")
    members = {group: set() for group in groups}
    for membership in data["memberships"]:
        require(isinstance(membership, dict) and set(membership) == {"group_id", "user_id"}, "Invalid membership fields")
        group, user = membership["group_id"], membership["user_id"]
        require(isinstance(group, str) and isinstance(user, str), "Membership IDs must be strings")
        require(group in groups and user in users, "Unknown membership reference")
        require(user not in members[group], "Duplicate membership")
        members[group].add(user)
    review_index = {}
    for review in reviews.values():
        key = (review["user_id"], review["account_id"], review["permission_set_id"])
        require(key[0] in users and key[1] in accounts and key[2] in sets, "Unknown review reference")
        require(isinstance(review["reviewer"], str) and review["reviewer"].strip(), "Missing synthetic reviewer label")
        start, expiry = timestamp(review["reviewed_at"]), timestamp(review["expires_at"])
        require(start < expiry, "Review expiry must follow review time")
        review_index.setdefault(key, []).append((review["id"], start, expiry))
    findings = []
    entitlements = {}
    seen_assignments = set()
    for assignment in assignments.values():
        require(assignment["account_id"] in accounts and assignment["permission_set_id"] in sets, "Unknown account or permission set")
        kind, principal = assignment["principal_type"], assignment["principal_id"]
        require(kind in ("USER", "GROUP"), "Unsupported principal type")
        require(principal in (users if kind == "USER" else groups), "Unknown assignment principal")
        semantic = (assignment["account_id"], kind, principal, assignment["permission_set_id"])
        require(semantic not in seen_assignments, "Duplicate semantic assignment")
        seen_assignments.add(semantic)
        require(assignment["provisioning"] in ("SUCCEEDED", "IN_PROGRESS", "FAILED", "UNKNOWN"), "Unsupported normalized provisioning state")
        people = {principal} if kind == "USER" else members[principal]
        if not people:
            findings.append({"code": "assigned_group_has_no_members", "assignment_id": assignment["id"]})
        if assignment["provisioning"] != "SUCCEEDED":
            findings.append({"code": "provisioning_not_confirmed", "assignment_id": assignment["id"], "observed": assignment["provisioning"]})
        for user in sorted(people):
            key = (user, assignment["account_id"], assignment["permission_set_id"])
            entitlements.setdefault(key, []).append(assignment["id"])
    rows = []
    for key, paths in sorted(entitlements.items()):
        user, account, permission_set = key
        history = review_index.get(key, [])
        current = sorted(id_ for id_, start, expiry in history if start <= as_of < expiry)
        codes = []
        if not users[user]["enabled"]:
            codes.append("disabled_user_with_assignment")
        if not current:
            codes.append("expired_review" if history and all(expiry <= as_of for _, _, expiry in history) else "no_current_review")
        if not accounts[account]["owner"].strip():
            codes.append("account_owner_missing")
        if accounts[account]["lifecycle"] != "active":
            codes.append("account_retiring")
        row = {"user_id": user, "account_id": account, "permission_set_id": permission_set,
               "assignment_paths": sorted(paths), "current_review_records": current, "findings": codes}
        rows.append(row)
        findings.extend({"code": code, "user_id": user, "account_id": account, "permission_set_id": permission_set} for code in codes)
    stale = as_of - collected > timedelta(hours=max_age_hours)
    return {"scope": data["scope"], "as_of": as_of.isoformat(), "snapshot_at": collected.isoformat(),
            "freshness_threshold_hours": max_age_hours, "warnings": ["stale_snapshot"] if stale else [],
            "claims": {"synthetic_only": True, "effective_iam_permissions_evaluated": False,
                       "existing_sessions_evaluated": False, "other_access_models_included": False,
                       "cloud_collection_completeness_verified": False},
            "potential_assignment_rows": rows, "findings": findings,
            "summary": {"source_assignments": len(assignments), "unique_user_account_set_rows": len(rows), "finding_count": len(findings)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=Path(__file__).with_name("snapshot.json"))
    parser.add_argument("--as-of", default="2026-11-10T09:00:00Z", help="Explicit review time; default belongs to the frozen teaching fixture")
    parser.add_argument("--max-age-hours", type=int, default=24)
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.snapshot.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
        report = reconcile(data, args.as_of, args.max_age_hours)
    except (ValueError, OSError) as error:
        print("Invalid teaching snapshot: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 2 if args.fail_on_findings and (report["findings"] or report["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
