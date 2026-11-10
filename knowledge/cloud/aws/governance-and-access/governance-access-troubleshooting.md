---
type: Troubleshooting Guide
title: Diagnose AWS human-access and governance failures
description: Locate directory, assignment, provisioning, credential, policy-path or
  recovery failures before changing grants.
tags:
- aws
- governance
- human-access
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
- id: instances
  title: Identity Center organization/account instances
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html
- id: custom-policy
  title: Permission-set policy types
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetcustom.html
- id: role-refs
  title: Permission-set roles in resource policies
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html
- id: scp-evaluation
  title: SCP inheritance and evaluation
  resource: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html
- id: sessions
  title: Identity Center session types and termination
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html
---

# Diagnose AWS human-access and governance failures

Begin with the expected person, account, role/access model, operation and Region. Record the actual caller, time, error/request ID, directory/assignment/provisioning revision and last known working state. Keep tokens, credentials and personal directory exports out of public reports.

## Route the symptom

| Symptom | Inspect before changing access |
| --- | --- |
| Portal login works but no AWS account access | Correct organization instance/access model, user/group synchronization, exact assignment and account scope. |
| Application access exists but multi-account options do not | Account-instance versus organization-instance capabilities and permission-set multi-account configuration.[^instances] |
| Permission-set provisioning fails | Named/path-matched customer-managed policies, boundary dependencies, request status and target account.[^custom-policy] |
| CLI returns a different role/account | Profile/SSO model, prior/static credentials, provider precedence and actual session. |
| Assignment looks right but service call fails | Identity/resource policies, inherited SCP/RCP, session/boundary/context, endpoint and KMS paths. |
| A child allow does not restore access | An inherited SCP deny or missing allow envelope on another path level.[^scp-evaluation] |
| KMS/EKS access broke after reassigning a permission set | Old generated-role ARN/reference and independent recovery path.[^role-refs] |
| Disabled user still performs operations | Existing portal/application/role sessions and alternate/direct/group grants.[^sessions] |

Use [Identity Center concepts](identity-center-and-human-federation.md) to identify the access model, [CLI sessions](cli-sso-and-role-sessions.md) for provider selection, and [AccessDenied diagnosis](../security/iam-access-denied-troubleshooting.md) for the actual request. Do not create an IAM user key or grant administrator access merely to bypass an unexplained failure.

## Inspect scope and asynchronous state

An inventory API's empty response can mean wrong instance/Region, insufficient scope, stale collection or missing pagination. A provisioning request being accepted is not completion. Compare immutable IDs, deployed policy versions and account ownership; display names can be changed or reused. A group grant can survive removal of a direct grant to the same person.

Collect read-only evidence first. For each proposed correction, name the missing or incorrect boundary, minimum change, expected positive/negative outcomes and recovery owner. After propagation, establish the caller again and repeat the actual service tests. Keep the original error and resulting revision for the review record.

## Recovery boundaries

Management-account, delegated-administration, organization-policy and root/IdP recovery paths have different authority and dependencies. See [emergency access](root-and-emergency-access.md). A person inside a denied member-account path cannot override its inherited control just by assuming a more privileged local role. Do not remove root-level policies or delete generated roles to experiment without a bounded recovery plan.

No access or policy is changed by this diagnostic guide. Remove task-owned exported reports only after retaining required evidence; keep the actual fix, rollback and unassessed scopes explicit.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^instances]: [Identity Center organization/account instances](https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html).
[^custom-policy]: [Permission-set policy types](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetcustom.html).
[^role-refs]: [Permission-set roles in resource policies](https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html).
[^scp-evaluation]: [SCP inheritance and evaluation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html).
[^sessions]: [Identity Center session types and termination](https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html).
