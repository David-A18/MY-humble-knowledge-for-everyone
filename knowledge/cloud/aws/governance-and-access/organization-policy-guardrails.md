---
type: Explanation
title: AWS organization policy guardrails
description: Distinguish principal and resource guardrails, evaluate inherited SCPs,
  and plan a bounded rollout and recovery.
tags:
- aws
- governance
- human-access
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
- id: scp
  title: Service control policies
  resource: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html
- id: scp-evaluation
  title: SCP inheritance and evaluation
  resource: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html
- id: rcp
  title: Resource control policies
  resource: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html
---

# AWS organization policy guardrails

Service control policies (SCPs) bound applicable principal permissions in member accounts; resource control policies (RCPs) bound access to supported member-account resources. Neither grants permission. Both require an all-features organization and supported policy configuration.[^scp][^rcp] Keep the [IAM request-evaluation guide](../security/iam-policy-evaluation-and-least-privilege.md) as the detailed authorization model.

## Follow the inherited control path

For an applicable SCP-controlled operation, an allow must be available at every level from organization root through the direct OU path and account. An inherited explicit deny cannot be overridden by adding a child allow.[^scp-evaluation] Multiple policies at one level do not mean every policy must independently allow the operation.

`FullAWSAccess` supplies an SCP allow envelope; it does not make a role an administrator. Removing it without an appropriate allow replacement can block operations below that path. SCPs do not restrict management-account users/roles or service-linked roles.[^scp] A delegated-administrator member account is not exempt merely because it administers a service.

RCPs attach restrictions to supported resources and can constrain access by principals outside the organization. They do not cover every AWS service/action/resource uniformly; verify current support and exceptions.[^rcp] Do not substitute an SCP for a resource-side restriction when the caller is external.

## A narrowly described teaching policy

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyNewLongTermUserKeys",
    "Effect": "Deny",
    "Action": "iam:CreateAccessKey",
    "Resource": "*"
  }]
}
```

What it does: illustrates a deny for creating IAM access keys where this SCP applies. It does not remove existing keys, deny STS role credentials, or protect management-account principals. It assumes the intended allow envelope is retained elsewhere. This example was parsed locally as JSON, not attached to an organization or tested by AWS.

## Roll out and recover deliberately

Use a policy-test OU and one owned test account before increasing scope.[^scp] Capture the full inherited path and expected actor/action/resource/context matrix, including workload/service roles and emergency administrators. Prove intended operations still work and targeted operations fail for the right reason. Keep a separately controlled principal able to restore the relevant policy attachment; a role inside the affected account cannot simply override an inherited deny.

For a regression, preserve the request/error and policy revision, then use the approved rollback from the policy-owning level. Re-test both outcomes after propagation. OU moves, policy-type enablement and root-level attachments are operational changes, not harmless cleanup. This guide performs none of them.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^scp]: [Service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html).
[^scp-evaluation]: [SCP inheritance and evaluation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html).
[^rcp]: [Resource control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html).
