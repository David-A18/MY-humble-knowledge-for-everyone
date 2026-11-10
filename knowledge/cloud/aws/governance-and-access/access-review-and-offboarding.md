---
type: How-to Guide
title: Review human access and complete offboarding
description: Reconcile direct and group assignments with current approvals and contain
  future and already-issued access separately.
tags:
- aws
- governance
- human-access
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
- id: sets
  title: Permission sets and multi-account access
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html
- id: account-access
  title: IAM account access manager
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/account-access-manager.html
- id: revoke-users
  title: Revoke Identity Center user access
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/revoke-user-permissions.html
- id: sessions
  title: Identity Center session types and termination
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html
---

# Review human access and complete offboarding

An access review asks which person can obtain which account role, why the assignment exists, who approved it, when that approval expires, and whether the assignment still fits the person's work. It must cover direct assignments and group-derived paths; a single portal screenshot is not a complete inventory.

## Build a scoped inventory

Collect users and enabled state from the authoritative source/directory, groups and memberships, accounts and owners, permission sets/deployed status, assignments, review records and collection times. Inventory account access manager role assignments too if used; they are a separate mapping from permission sets.[^sets][^account-access] Track pagination, collection permissions, missing scopes and inconsistent snapshots.

The [synthetic inventory lab](examples/access-review-lab/index.md) demonstrates stable-ID joins, direct/group expansion, duplicate-path handling, expired/missing reviews, disabled users, empty groups, unknown ownership and provisioning uncertainty. Its report is potential assignment exposure under declared inputs, not an effective IAM permission or session-revocation result.

## Review and remediate

| Finding | Decision/evidence |
| --- | --- |
| Missing or expired approval | Named owner renews justified scope or removes the path; no silent auto-renewal. |
| Disabled user still assigned | Investigate membership/assignment/session state; directory status alone is insufficient. |
| Direct and group path overlap | Review all paths; deleting one must not be mistaken for removing the entitlement. |
| Permission-set update pending/failed | Inspect actual request/provisioned policy state before inferring access. |
| Account lacks an owner | Assign responsibility before certifying access/lifecycle. |
| Incomplete or stale snapshot | Recollect/qualify the scope; an empty report cannot prove absent access. |

Retain the before/after assignment path and an approved decision. Data collection and reconciliation are reversible read-only work; changing grants and stopping sessions need an owned operational procedure and impact assessment.

## Contain departure or compromise at each layer

Map identity source, directory provisioning, direct/group permission-set and account access manager assignments, portal/application sessions, issued IAM role credentials, and any separate keys or federated paths. AWS's revocation procedure distinguishes removing assignments, stopping active sessions and disabling sign-in; disabling a user alone can leave active-session access paths.[^revoke-users]

Issued IAM role sessions have their own lifetime. Portal/session termination is not immediate proof that every service credential is unusable.[^sessions] Prepare the documented session-denial/revocation mechanism before needing it, verify resource-operation denial with affected credentials, and keep restrictions for the applicable lifetime. Follow the current console ordering/prerequisites rather than inventing a universal one-button disable procedure.

## Verify completion and retain evidence

Prove both that the person cannot obtain new effective access through any inventoried path and that targeted issued credentials cannot perform prohibited operations. Verify ordinary colleagues/recovery roles retain intended access. `GetCallerIdentity` is not a negative permission test. Record scope not assessed, propagation/caching observations, evidence locations, owner and retention.

Cleanup removes only task-created exports or temporary review artifacts under the retention policy; actual access-removal and account-retirement changes belong to the approved workflow. Link [credential incident response](../security/security-incident-response.md) for compromised sessions and [governance diagnosis](governance-access-troubleshooting.md) for failed removals.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^sets]: [Permission sets and multi-account access](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html).
[^account-access]: [IAM account access manager](https://docs.aws.amazon.com/IAM/latest/UserGuide/account-access-manager.html).
[^revoke-users]: [Revoke Identity Center user access](https://docs.aws.amazon.com/singlesignon/latest/userguide/revoke-user-permissions.html).
[^sessions]: [Identity Center session types and termination](https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html).
