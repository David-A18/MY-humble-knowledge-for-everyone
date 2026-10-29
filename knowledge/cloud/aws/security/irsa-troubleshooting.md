---
type: Troubleshooting Guide
title: IRSA troubleshooting and operational security
description: Find credential-source, trust, and AWS authorization failures without
  exposing tokens.
tags:
- cloud
- security
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: irsa-benefits-and-caveats
  resource: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
  title: IRSA benefits and caveats
- id: eks-pod-identity
  resource: https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
  title: EKS Pod Identity
- id: aws-sdk-support
  resource: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html
  title: AWS SDK support
---

# IRSA troubleshooting and operational security

## Purpose

Find credential-source, trust, and AWS authorization failures without exposing tokens.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## First checks

```bash
aws eks describe-cluster --name "$CLUSTER" --region "$AWS_REGION" --query cluster.identity.oidc.issuer --output text
kubectl get pod reader -n irsa-lab -o jsonpath='{.spec.serviceAccountName}{"\n"}'
kubectl get serviceaccount s3-reader -n irsa-lab -o yaml
kubectl exec -n irsa-lab reader -- aws sts get-caller-identity
```

What it does: checks issuer, actual Pod identity, annotation, and effective AWS caller. These commands assume an existing lab and configured operator access.

| Symptom | Check | Likely fix |
| --- | --- | --- |
| Node role returned | Static credentials, provider precedence, injection, SDK | Correct the credential source; restrict metadata. |
| InvalidIdentityToken | Issuer, audience, key discovery, expiry | Repair OIDC/token integration. |
| STS AccessDenied | Trust principal, exact subject, audience | Narrowly correct the trust relationship. |
| S3 AccessDenied after STS success | Object ARN, prefix, KMS, bucket policy, SCP | Fix only the missing authorization. |
| DNS/connection timeout | Egress, DNS, STS/service endpoint paths | Restore network access. |
| Annotation changed but old Pods fail | Admission-time injection | Recreate the workload through an intentional rollout. |

## Troubleshoot safely

Avoid printing projected JWTs, session credentials, or Secret contents into logs. Inspect Pod specs and credential-provider names rather than credential values. Confirm clocks and SDK support. An annotated service account on the wrong Pod proves nothing.

Private-cluster DNS and endpoint behavior depends on network configuration. Test OIDC discovery from the administrative environment and STS connectivity from the workload; they are different paths. Use current AWS instructions for private endpoints and resolver setup.

## Production checklist

- Exact audience and service-account trust, scoped resource permissions.
- Compatible SDK and no accidental static credentials.
- Restricted metadata access and reviewed privileged/hostNetwork workloads.
- CloudTrail visibility and tested denied actions.
- Documented IAM ownership, rotation/revocation response, and cross-account access.

Use Pod Identity where its supported capabilities and operating model fit; retain IRSA when federation or compatibility requirements justify it. Compare against current AWS constraints rather than assuming both mechanisms support identical node types or cross-account flows.

Source references: [^irsa-benefits-and-caveats][^eks-pod-identity][^aws-sdk-support]

## Related links

- [IRSA benefits and caveats](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
- [AWS SDK support](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^irsa-benefits-and-caveats]: [IRSA benefits and caveats](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).
[^eks-pod-identity]: [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).
[^aws-sdk-support]: [AWS SDK support](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html).
