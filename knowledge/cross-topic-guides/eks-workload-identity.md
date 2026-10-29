---
type: "Explanation"
title: "EKS workload identity"
description: "Use this guide to choose between IRSA and EKS Pod Identity for AWS permissions from Pods."
tags: [cross-topic-guides, eks-workload-identity]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: aws-irsa
    resource: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
    title: IAM roles for service accounts
  - id: aws-pod-identity
    resource: https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
    title: EKS Pod Identity
  - id: aws-pod-identity-association
    resource: https://docs.aws.amazon.com/eks/latest/userguide/pod-id-association.html
    title: Assign an IAM role to a Kubernetes service account
---

# EKS workload identity

## Purpose

Choose IRSA or EKS Pod Identity, then verify the actual AWS credential path.

Sources reviewed: 2026-10-29. See the [validation record](../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Choose by integration requirements

| Question | IRSA | EKS Pod Identity |
| --- | --- | --- |
| Trust model | IAM OIDC federation and STS web identity | EKS associations and EKS service integration |
| Workload configuration | Service-account annotation and projected token integration | Association and supported credential-delivery integration |
| SDK path | Web-identity credential provider | Supported container credential provider |
| Cluster identity administration | IAM OIDC provider/trust per issuer | EKS-managed associations and supported infrastructure |
| Compatibility | Check SDK, node/runtime, issuer, and federation needs | Check current EKS agent/compute, SDK, and feature support |

For new EKS workloads, evaluate Pod Identity's supported operating model alongside existing platform standards. Retain IRSA where established OIDC federation, compatibility, or controls justify it. Current cross-account and target-role capabilities must be checked against AWS documentation; do not assume the two mechanisms have identical constraints.

## Identity boundaries

Kubernetes RBAC permits Kubernetes API operations. IAM permits AWS operations. Human EKS access is another identity path. Use one workload service account per meaningful permission boundary and verify both role trust and resource permissions.[^aws-irsa]

## Deployment constraints checked on 2026-10-29

EKS Pod Identity is documented for Linux EC2 worker nodes. It is not available for Fargate Pods, Windows EC2 Pods, EKS Anywhere, or self-managed Kubernetes on EC2. Standard clusters require the supported Pod Identity Agent; EKS Auto Mode provides the integration without the separate agent-installation step.[^aws-pod-identity]

Pod Identity associations are managed through the EKS API rather than a service-account annotation. A `kubectl get serviceaccount` inspection alone cannot establish that the association exists. Association changes are eventually consistent, so configure them before a critical workload path and verify the resulting AWS caller.[^aws-pod-identity-association]

```bash
aws eks list-pod-identity-associations --cluster-name "$CLUSTER" --namespace demo --service-account app
```

What it does: lists the EKS-side associations for the specified workload identity. The operator needs permission to query EKS. This read-only check complements the application's `sts get-caller-identity` result; it does not test resource permissions.

## IRSA study path

1. Read [IRSA fundamentals](../cloud/aws/security/irsa-fundamentals.md).
2. Understand [trust and permissions](../cloud/aws/security/irsa-trust-and-permissions.md).
3. Run the [S3 access lab](irsa-s3-access-on-eks.md).
4. Diagnose with [IRSA troubleshooting](../cloud/aws/security/irsa-troubleshooting.md).

## Verify before adoption

```bash
kubectl get serviceaccount app -n demo -o yaml
kubectl exec -n demo deployment/app -- aws sts get-caller-identity
```

What it does: compares configured workload identity with the caller actually used by an AWS-capable application container. An AWS CLI installation is required for this diagnostic; applications can expose the same identity through controlled SDK diagnostics.

Prove an allowed operation succeeds and a forbidden operation fails. Check static credentials and node metadata do not mask a broken configuration. Review privileged/hostNetwork workloads, token handling, CloudTrail visibility, and least privilege.

## Migration and recovery

Inventory controller and application SDK support, node types, role trust, account boundaries, and current sessions. Test one workload first, verify its caller and permissions, then expand. Avoid configuring multiple competing credential sources and guessing which wins. Retain a reviewed rollback path and record the desired identity in versioned configuration.

## Related links

- [AWS IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
- [AWS workload identities](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html)
- [OIDC fundamentals](../security/identity-federation/oidc-fundamentals.md)
- [AWS OIDC and STS](../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
- [Cloud](../cloud/index.md)
- [AWS](../cloud/aws/index.md)
- [Kubernetes](../kubernetes/index.md)
- [Back to parent index](index.md)
- [Back to root index](../../README.md)

[^aws-irsa]: [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).
[^aws-pod-identity]: [EKS Pod Identity limits and considerations](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).
[^aws-pod-identity-association]: [Pod Identity association configuration](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-association.html).
