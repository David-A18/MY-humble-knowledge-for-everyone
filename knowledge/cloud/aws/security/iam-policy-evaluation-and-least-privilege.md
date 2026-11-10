---
type: Explanation
title: IAM policy evaluation and least privilege
description: Separate role trust, permission grants, restrictive controls, and service-specific
  access before designing a least-privilege change.
tags:
- aws
- security
- iam
status: draft
maturity: draft
audience: Cloud and platform engineers
maintainer: unassigned
sources:
- id: evaluation
  title: IAM policy evaluation
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
- id: principal-evaluation
  title: IAM enforcement and principal-specific evaluation
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic_policy-eval-denyallow.html
- id: pass-role
  title: IAM PassRole
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html
- id: analyzer
  title: IAM Access Analyzer policy validation
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html
---

# IAM policy evaluation and least privilege

An IAM policy describes permissions in a request context: principal, action, resource, and conditions. Authentication establishes the caller; authorization determines whether that caller may perform this operation. A role's trust policy controls role assumption, while its permission policies control subsequent service calls.

## Map the applicable policies

| Control | Question it answers |
| --- | --- |
| Role trust | Which identity/service can obtain a session, under which conditions? |
| Identity policy | Which operations/resources does this user or role grant? |
| Resource policy | Which principals does this resource grant or deny? |
| Permissions boundary | What is the maximum identity-policy permission envelope? |
| Session policy | What additional restriction applies to this issued session? |
| SCP / RCP | What organization limits apply to the principal / resource in supported scope? |
| Endpoint / KMS policy | What additional network endpoint or cryptographic access rule applies? |

An applicable explicit deny overrides an allow. Missing an allow is an implicit deny. Boundaries, session policies, and organization controls do not independently grant access.[^evaluation] Avoid reducing all evaluation to one universal intersection: same-account resource grants behave differently for a user ARN, role ARN, or role-session ARN. Cross-account requests also need the relevant trust/grants on each side.[^principal-evaluation]

## Design one bounded permission

Start from an operation the application actually needs. For a known S3 object prefix, `s3:GetObject` targets object ARNs such as `arn:aws:s3:::example-lab-bucket/public-lab/*`; listing is a different bucket-level permission. Do not add listing or writes merely to make a diagnostic command convenient. See [IRSA policy examples](irsa-trust-and-permissions.md).

Write the expected access matrix before editing a policy: intended principal/action/resource succeeds; another subject, another prefix, and write/delete operations fail. Include required encryption/service conditions and a clear owner. Use [local policy contracts](examples/policy-contract-lab/index.md) to catch accidental fixture broadening, then AWS validation/simulation and live disposable-resource tests for the actual decision.

`iam:PassRole` allows an operator to delegate an approved role to a service; it does not mean the operator can assume that role directly. Scope which roles and services can be passed. A broad ability to pass a powerful role can bypass the intended operator boundary.[^pass-role]

## Review a change

Review additions as well as deletions: principals, actions, resources, conditions, policy attachments, and the exact principal form in resource policies. Access Analyzer syntax/best-practice findings help identify issues, but a clean finding list does not prove the policy matches your intended access matrix.[^analyzer]

Retain a previous policy version and an independent recovery principal before a risky access change. Removing a role trust grant does not retract previously issued credentials. Link the change to [session response](security-incident-response.md) and [AccessDenied diagnosis](iam-access-denied-troubleshooting.md).

## Evidence and limits

Official sources reviewed on 2026-11-10. This draft records source review and local fixture checks where stated. AWS account calls, live EKS credentials, key/secret changes, detection delivery, and incident containment were not executed. CLI examples require a supported AWS CLI v2 and authorized account access; no CLI runtime version was tested in this batch.

[Back to AWS security](index.md) | [Back to AWS](../index.md)

[^evaluation]: [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
[^principal-evaluation]: [IAM enforcement and principal-specific evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic_policy-eval-denyallow.html)
[^pass-role]: [IAM PassRole](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html)
[^analyzer]: [IAM Access Analyzer policy validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)
