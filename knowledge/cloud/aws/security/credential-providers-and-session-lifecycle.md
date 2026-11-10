---
type: Explanation
title: AWS credential providers and session lifecycle
description: Identify which credentials an application actually uses and distinguish
  projected tokens, temporary sessions, refresh, and revocation.
tags:
- aws
- security
- credential
status: draft
maturity: draft
audience: Cloud and platform engineers
maintainer: unassigned
sources:
- id: providers
  title: SDK credential providers
  resource: https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html
- id: caller
  title: STS GetCallerIdentity
  resource: https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html
- id: irsa-sdk
  title: IRSA SDK integration
  resource: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html
- id: web-identity
  title: STS AssumeRoleWithWebIdentity
  resource: https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html
- id: revoke
  title: IAM role session revocation
  resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html
---

# AWS credential providers and session lifecycle

An application can have correct IAM configuration and still use the wrong identity. AWS SDKs search supported credential providers; a source earlier in the selected SDK's chain can mask a new workload identity configuration. Explicit credentials in application code can bypass the default chain. Provider support and precedence vary by SDK/tool and version.[^providers]

## Distinguish the lifetimes

| Artifact | Meaning |
| --- | --- |
| Kubernetes projected token | Signed workload assertion with its own audience and expiry. |
| AWS temporary credentials | Access-key ID, secret key, and session token with a separate expiration. |
| Application credential cache | Provider-managed in-memory or tool cache, refreshed according to the provider. |
| IAM policy/trust change | Change to future assumption or effective permission; propagation and existing sessions matter. |

For IRSA, the SDK exchanges the projected token for STS credentials and supported providers refresh them.[^irsa-sdk] A manually copied STS response is not automatically a refreshing provider. Web-identity session duration is bounded by the API and role configuration; token lifetime and session duration are different controls.[^web-identity]

## Establish the caller safely

```bash
aws sts get-caller-identity --profile <profile> --region <region> --no-cli-pager
kubectl exec -n <namespace> <pod> -- aws sts get-caller-identity --no-cli-pager
```

What it does: records the operator and workload's account/ARN without printing secrets. The workload command requires AWS CLI inside that container. Operator identity does not prove workload identity; compare the returned role/account with an explicit expected value.

`GetCallerIdentity` identifies credentials; it does not establish S3, KMS, or Kubernetes permission. AWS documents that this operation needs no permission, even with an explicit deny on that action.[^caller] Prove resource authorization with a separate allowed/denied matrix.

Inspect credential-provider names/configuration and whether expected variables or token mounts exist, without dumping environment values, credential files, or JWTs. Check mounted shared profiles, static environment keys, explicit SDK configuration, IRSA versus container providers, and node metadata exposure. The [IRSA guide](irsa-fundamentals.md) and [Pod Identity operations](eks-pod-identity-operations.md) describe their distinct paths.

## Diagnose expiry and revocation

An expired session can indicate stale copied credentials, missing refresh support, inaccessible token/agent/STS endpoints, or clock errors. Fix the intended refresh path instead of adding permanent keys. An annotation change normally needs newly admitted Pods to receive new injected configuration.

Removing trust blocks future assumptions after propagation; it is not a universal kill switch for existing credentials. IAM's role-session revocation procedure applies a time-based deny to older sessions and affects all matching users of that role. Pair session restrictions with containment of the compromised source and verify both old-session denial and authorized recovery.[^revoke]

## Evidence and limits

Official sources reviewed on 2026-11-10. This draft records source review and local fixture checks where stated. AWS account calls, live EKS credentials, key/secret changes, detection delivery, and incident containment were not executed. CLI examples require a supported AWS CLI v2 and authorized account access; no CLI runtime version was tested in this batch.

[Back to AWS security](index.md) | [Back to AWS](../index.md)

[^providers]: [SDK credential providers](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html)
[^caller]: [STS GetCallerIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html)
[^irsa-sdk]: [IRSA SDK integration](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html)
[^web-identity]: [STS AssumeRoleWithWebIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)
[^revoke]: [IAM role session revocation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html)
