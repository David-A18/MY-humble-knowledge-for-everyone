---
type: Explanation
title: Delegate IAM administration within a reviewed boundary
description: Design who may create, alter, pass and assume roles without allowing
  self-escalation through the delegation workflow.
tags:
- aws
- governance
- human-access
status: draft
maturity: draft
audience: Cloud administrators and platform engineers
maintainer: unassigned
sources:
- id: boundary
  title: IAM permissions boundaries
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
- id: pass-role
  title: IAM PassRole
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html
- id: delegation
  title: Identity Center delegated administration
  resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html
---

# Delegate IAM administration within a reviewed boundary

Delegation is more than giving a team `iam:CreateRole`. Define which role paths, trust relationships, policies, boundaries, tags, services and accounts the team may manage, and which security controls remain independently owned. Distinguish service-level delegated administration from permission to alter arbitrary IAM roles.

## Review the entire privilege path

| Capability | Review question |
| --- | --- |
| Create a role | Must the approved boundary and intended role path be supplied? |
| Edit policies/versions | Can the caller change the boundary policy itself or replace its active version? |
| Remove boundary | Can a delegated role/user shed the restriction after creation? |
| Change trust | Can an otherwise limited creator make a powerful role assumable by itself? |
| PassRole | Can a service execute as a role more powerful than the operator? |
| AssumeRole / session context | Which source principal, conditions and target role actually get used? |
| Tag changes | Can the operator change an authorization tag and cross its intended ABAC boundary? |

A permissions boundary sets the maximum identity-policy permissions for an IAM user or role; it grants nothing by itself.[^boundary] Protect both attachment and policy content/version control. Review resource-policy principal forms too: a boundary is not a universal substitute for understanding every resource grant.

`iam:PassRole` delegates a specified role to a service; it is separate from assuming the role. Scope approved role resources and supported passed-to-service conditions, and verify the service's own trust/execution behavior. AWS warns that controlling PassRole solely with a role resource-tag condition is unreliable.[^pass-role]

## Separate management and service administrators

Identity Center delegated administrators perform supported member-account tasks, while management-account access has additional restrictions. In particular, a permission set provisioned in the management account has management-account ownership constraints.[^delegation] An organization's administrator for one integrated service is not automatically an administrator of every account or service.

## Test a delegation contract

Prepare an approved sandbox role path and harmless service action. Prove an intended role can be created/passed and that omitting/changing the required boundary, editing protected policy versions, passing an out-of-scope role, and changing protected trust/tag controls are rejected. Observe the caller and actual service result rather than treating a policy simulator as the complete environment.

Use [AccessDenied diagnosis](../security/iam-access-denied-troubleshooting.md) and [policy review practice](../security/examples/policy-contract-lab/index.md) for supporting checks. Keep the prior policies and recovery principal outside the delegated change boundary. Cleanup removes only task-owned sandbox roles and artifacts after their service dependencies are stopped; this guide creates no such resources.

## Evidence and limits

Official sources reviewed on 2026-11-10. These drafts describe current AWS behavior and an applied review process. No AWS account/API call, login, policy attachment, organization change, root session, account creation/closure, or user-session revocation was executed during authoring. CLI examples are source-reviewed AWS CLI v2 instructions; no AWS CLI runtime version was tested. The separate synthetic inventory lab validates local reconciliation only.

[Back to governance and access](index.md) | [Back to AWS](../index.md)

[^boundary]: [IAM permissions boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html).
[^pass-role]: [IAM PassRole](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html).
[^delegation]: [Identity Center delegated administration](https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html).
