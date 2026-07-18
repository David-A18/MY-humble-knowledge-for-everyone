# EKS workload identity

## Purpose

Use this guide to choose between IRSA and EKS Pod Identity for AWS permissions from Pods.

## Options

| Option | How it works | Use when |
| --- | --- | --- |
| IRSA | Kubernetes service account token is exchanged through IAM OIDC trust and STS web identity. | You need the established OIDC-based pattern or compatibility with existing tooling. |
| EKS Pod Identity | EKS-managed association provides IAM credentials to Pods without using an IAM OIDC provider. | You want the newer EKS-native workflow and it supports your requirements. |

## Design checklist

- Use one service account per permission boundary.
- Keep IAM trust and permissions policies narrow.
- Avoid sharing broad roles across unrelated workloads.
- Verify the Pod receives credentials from the intended role.
- Monitor role assumption and access-denied events.

## Related links

- [OIDC fundamentals](../security/identity-federation/oidc-fundamentals.md)
- [IAM OIDC provider and STS web identity](../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
- [Amazon EKS Pod Identity documentation](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
- [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
