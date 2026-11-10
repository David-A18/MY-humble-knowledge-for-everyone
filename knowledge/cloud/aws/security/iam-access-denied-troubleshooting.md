---
type: Troubleshooting Guide
title: Diagnose AWS AccessDenied
description: Locate the failing credential, trust, service permission, resource, organization,
  endpoint, or key boundary without granting broad access.
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
- id: caller
  title: STS GetCallerIdentity
  resource: https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html
- id: simulator
  title: IAM policy simulator and limitations
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html
- id: kms-policy
  title: KMS key policies
  resource: https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html
---

# Diagnose AWS AccessDenied

Begin with the failing operation and exact error, not a guess about which policy is missing. Record time, account/Region, expected and actual caller, action, resource ARN, request ID, and whether failure happened at credential acquisition or the later service request. Redact tokens, values, and unrelated customer data.

## Follow the failure stage

| Observation | Inspect next |
| --- | --- |
| Missing/expired credentials | Provider selection, token/cache expiry, refresh, clocks and endpoint reachability. |
| STS web-identity failure | Issuer/signature/audience/subject, IAM OIDC provider, role trust, role/session constraints. |
| Caller is unexpected | Explicit/static/profile credentials, SDK provider chain, Pod identity and node metadata. |
| Expected caller, S3 denied | Correct operation/ARN/prefix, identity and bucket/access-point policy, organization and endpoint restrictions. |
| SSE-KMS object denied | S3 decision plus actual key state, key policy, grants, IAM and context. |
| Simulation allowed, live denied | Missing context, unmodeled policy/service path, principal form, resource state and propagation. |
| Non-authorization error | DNS, timeout, object existence or service health; do not count it as the expected deny. |

The caller ARN is evidence of identity, not authorization. `GetCallerIdentity` succeeds without an ordinary permission grant and cannot be used as a negative permission test.[^caller] Test the intended service operation instead.

## Inspect the relevant policy set

Role trust and role permissions answer different questions. Check attached managed policies and their active versions, inline policies, permissions boundary, session policy, resource policy, organization limits, and endpoint restrictions. An applicable explicit deny overrides an allow.[^evaluation]

Same-account resource policy behavior depends on whether the principal is a user, role, or role session. Cross-account access adds evaluation on both sides. Do not flatten these rules into a simplistic 'every policy must allow' diagnostic.[^principal-evaluation] KMS has its own key-policy authorization path.[^kms-policy]

## Use validation and simulation as supporting evidence

For candidate policies, use [Access Analyzer and simulation](examples/policy-contract-lab/policy-contract-lab.md). Supply required context and interpret missing-context results. A simulator does not execute the requested API and cannot reproduce all live controls; verify allowed and forbidden operations in the actual disposable environment.[^simulator]

Change only the demonstrated missing grant or incorrect constraint, with a rollback and owner. Recheck the caller and both sides of the access matrix after propagation. An unexpected allowed write or role assumption is a security regression; do not treat it as a lab success.

## Evidence to retain

Record the original failure, policy revision, modeled outcome, live expected result and observed result, and cleanup. Keep credential values out of the report. For workload-specific details use [IRSA troubleshooting](irsa-troubleshooting.md), [Pod Identity operations](eks-pod-identity-operations.md), and [KMS boundaries](kms-encryption-and-access.md).

## Evidence and limits

Official sources reviewed on 2026-11-10. This draft records source review and local fixture checks where stated. AWS account calls, live EKS credentials, key/secret changes, detection delivery, and incident containment were not executed. CLI examples require a supported AWS CLI v2 and authorized account access; no CLI runtime version was tested in this batch.

[Back to AWS security](index.md) | [Back to AWS](../index.md)

[^evaluation]: [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
[^principal-evaluation]: [IAM enforcement and principal-specific evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic_policy-eval-denyallow.html)
[^caller]: [STS GetCallerIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html)
[^simulator]: [IAM policy simulator and limitations](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html)
[^kms-policy]: [KMS key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)
