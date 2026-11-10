---
type: How-to Guide
title: Operate permission sets and account assignments
description: Design, provision, verify, change and retire human account assignments
  without confusing templates with effective access.
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
- id: custom-policy
  title: Permission-set policy types
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetcustom.html
- id: role-refs
  title: Permission-set roles in resource policies
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html
- id: delegation
  title: Identity Center delegated administration
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html
- id: assignments-cli
  title: AWS CLI account assignment listing
  resource: https://docs.aws.amazon.com/cli/latest/reference/sso-admin/list-account-assignments.html
- id: provisioned-cli
  title: AWS CLI provisioned permission-set listing
  resource: https://docs.aws.amazon.com/cli/latest/reference/sso-admin/list-permission-sets-provisioned-to-account.html
---

# Operate permission sets and account assignments

A permission set is a policy template. Assigning it to a user/group for an account provisions an Identity Center-controlled role there. The organization instance needs multi-account permissions enabled for this workflow.[^sets] Start from the person's task and target account, not a convenient administrator policy.

## Specify the assignment contract

Record immutable principal ID/type, account ID, permission-set ARN, owner, business purpose, approved scope, review expiry, intended session duration and allowed/denied test operations. Group-based access can simplify routine member-account administration, but group-membership administration then becomes an access-grant boundary.

AWS recommends dedicated management-account permission sets and direct-user assignments there, with strict controls over management-account administration; delegated administrators cannot modify permission sets provisioned in that account.[^delegation] Do not apply a routine group pattern there without reviewing those implications.

## Provision and inspect the actual result

Custom permission sets can combine supported policies and a boundary. Customer-managed policy references require the named/path-matched policies to exist in each target account; those same names need not imply identical policy content.[^custom-policy] Deploy the intended content/version and dependencies before assignment.

The following read-only checks require an existing instance/account, the relevant listing permissions and an approved profile. Replace placeholders with actual IDs/ARNs and the Identity Center Region; the display name of a permission set is not its ARN.

```bash
aws sso-admin list-account-assignments --instance-arn <instance-arn> --account-id <account-id> --permission-set-arn <permission-set-arn> --region <identity-center-region> --profile <audit-profile> --no-cli-pager
aws sso-admin list-permission-sets-provisioned-to-account --instance-arn <instance-arn> --account-id <account-id> --region <identity-center-region> --profile <audit-profile> --no-cli-pager
```

What it does: reads assignments and provisioned permission-set references for an existing account.[^assignments-cli][^provisioned-cli] Preserve pagination and scope; listing is not a login or authorization test. An asynchronous change needs its corresponding request status and deployed-policy result, not just an accepted request ID.

For a scoped change, compare template and deployed roles/policies, perform required reprovisioning, and verify allowed and forbidden operations as the intended user. Do not edit generated roles manually as a substitute for updating their owning permission set. Preserve a prior policy/assignment revision and independent recovery access.

## Retire references carefully

Removing all assignments for a permission set in an account deletes its corresponding generated role. A later assignment creates a new unique role suffix/ARN; references in resource policies or other access configuration can become stale.[^role-refs] Inventory KMS/EKS and other role references before removing the final assignment. Do not preserve an unnecessary grant just to avoid a dependency you have not reviewed; use a deliberately designed recovery/reference strategy.

Assignment removal prevents that assignment's future role acquisition after propagation; it does not establish that already-issued IAM credentials stopped working. Complete [offboarding/session response](access-review-and-offboarding.md) separately. Remove only task-owned test assignments and retain the audit trail; deleting a shared permission set is not routine lab cleanup.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^sets]: [Permission sets and multi-account access](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html).
[^custom-policy]: [Permission-set policy types](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetcustom.html).
[^role-refs]: [Permission-set roles in resource policies](https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html).
[^delegation]: [Identity Center delegated administration](https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html).
[^assignments-cli]: [AWS CLI account assignment listing](https://docs.aws.amazon.com/cli/latest/reference/sso-admin/list-account-assignments.html).
[^provisioned-cli]: [AWS CLI provisioned permission-set listing](https://docs.aws.amazon.com/cli/latest/reference/sso-admin/list-permission-sets-provisioned-to-account.html).
