---
type: Tutorial
title: Reconcile a synthetic human-access inventory
description: Join direct and group permission-set assignments to dated review records while preserving overlapping paths and collection uncertainty.
tags: [aws, governance, access-review, synthetic-data, lab]
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
  - id: sets
    title: Permission sets and multi-account access
    resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html
  - id: sessions
    title: Identity Center session types and termination
    resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html
  - id: account-access
    title: IAM account access manager
    resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/account-access-manager.html
---

# Reconcile a synthetic human-access inventory

This local exercise asks which people have potential permission-set assignment paths to which accounts, and whether a current review record covers each person/account/permission-set tuple. It teaches an inventory join, not effective AWS authorization. No credentials, network requests, account changes, or notification messages are involved.

## Understand the normalized input

The [snapshot](snapshot.json) is a teaching schema, not an AWS API response, SCIM export or production adapter. All identities, accounts and reviewer labels are synthetic. Permission sets can be assigned directly to users or through groups; the exercise keeps those paths visible.[^sets]

| Input | Meaning in this exercise |
| --- | --- |
| Users/groups/memberships | Stable-ID join; a disabled user is retained for investigation. |
| Accounts | Twelve-digit synthetic IDs, owner, and normalized `active`/`retiring` lifecycle. |
| Permission sets | Stable teaching ID and a display name; no IAM policy evaluation. |
| Assignments | Account, principal type/ID, permission-set ID and normalized provisioning observation. |
| Reviews | Synthetic reviewer label, review time and expiry for one user/account/set tuple. |
| Scope and snapshot time | Declared permission-set-only scope, complete-input assertion and collection age. |

The `complete: true` input is an assumption supplied by the exercise. The program cannot verify cloud collection permissions, pagination or actual completeness. Account access manager maps users/groups to existing IAM roles separately and is deliberately outside this schema.[^account-access] Other roles, keys, resource policies, organization controls and issued sessions are also outside the calculation.

## Run the frozen exercise

Use Python 3.10+ with its standard library. Authoring execution used Python 3.13.17. Run from the repository root:

```bash
python knowledge/cloud/aws/governance-and-access/examples/access-review-lab/reconcile.py
python knowledge/cloud/aws/governance-and-access/examples/access-review-lab/test-reconcile.py
```

What it does: reads the fixture, prints JSON, and runs fourteen regression tests. The default review time is explicitly frozen at `2026-11-10T09:00:00Z` for repeatability; it is not the machine's current time. The calculator writes no report file and leaves the fixture unchanged. Tests may create ignored Python bytecode.

## Explain the expected result

| Observation | Expected report |
| --- | --- |
| Source assignments | Four rows: group readers, Alice direct, Bob direct, and an empty group. |
| Potential user/account/set tuples | Three rows after expanding group membership and retaining assignment-path provenance. |
| Alice | One tuple with two paths (`a-direct`, `a-group`) and one current synthetic review record. |
| Departed user | Still appears through the group; `disabled_user_with_assignment` and `no_current_review`. |
| Bob | Expired review, missing account owner, retiring account; the pending assignment also produces a provisioning finding. |
| Empty assigned group | A visible finding, even though it expands to no user tuple. |
| Total findings | Seven. These are fixture review findings, not proof of seven exploitable AWS permissions. |

Deleting Alice's direct assignment from a scratch copy still leaves the group path. Deleting an expired review does not remove the assignment. A current review record represents only this teaching approval model; it does not grant AWS access. Pending/failed/unknown provisioning is retained as uncertainty rather than treated as zero exposure.

## Exercise time and failure boundaries

```bash
python knowledge/cloud/aws/governance-and-access/examples/access-review-lab/reconcile.py --as-of 2026-11-11T09:00:00Z --max-age-hours 24
python knowledge/cloud/aws/governance-and-access/examples/access-review-lab/reconcile.py --fail-on-findings
```

What it does: first demonstrates a stale-snapshot warning under a locally chosen 24-hour freshness rule; then makes fixture findings cause exit 2. The freshness threshold is a teaching policy, not an AWS propagation or review guarantee. Default reporting returns 0 even when findings exist; invalid input returns 1; `--fail-on-findings` returns 2 for findings or warnings. The second command is intentionally nonzero.

Reviews are current when `reviewed_at <= as_of < expires_at`. A review expiring exactly at the query time is expired. A future-dated review is not current. Explicit time zones are required and normalized to UTC; snapshots later than the review time are rejected.

Tests reject duplicate IDs/memberships/semantic assignments, duplicate JSON keys, unknown references, incomplete or wrong scope, invalid normalized types/states and invalid time intervals. They verify overlapping direct/group paths, removal of only one path, disabled-user visibility, pending provisioning, expiry renewal, stale snapshots, output claims, exit codes and unchanged fixture bytes.

## Interpret the evidence correctly

The report explicitly says it did not evaluate effective IAM permissions, existing sessions, other access models or cloud collection completeness. A report with no findings would still not prove no live access. Identity Center portal and IAM role sessions have different lifetimes, and assignment reconciliation does not revoke either.[^sessions]

For an actual review, design a separate redacted adapter with authenticated/paginated collection, timestamps and scope evidence, consistent stable IDs, all relevant access models, current approvals and service authorization/session tests. Do not feed real personal/permission data into a public teaching fixture or commit exports. The [operational review guide](../../access-review-and-offboarding.md) defines the handoff.

## Validation and cleanup

Official sources reviewed on 2026-11-10. The report and fourteen regression tests were executed locally with Python 3.13.17; no AWS CLI/account walkthrough was executed. The [AWS security example workflow](../../../../../../.github/workflows/aws-security-examples.yml) runs the same tests/report in Linux CI; inspect the exact published revision for its hosted result.

Remove only task-owned scratch copies or redirected reports after retaining needed evidence. No account object, grant or session exists for this lab to delete or revoke.

[Back to this lab](index.md) | [Back to examples](../index.md) | [Back to governance and access](../../index.md)

[^sets]: [Permission sets and multi-account access](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html).
[^sessions]: [Identity Center session types and termination](https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html).
[^account-access]: [IAM account access manager](https://docs.aws.amazon.com/IAM/latest/UserGuide/account-access-manager.html).
