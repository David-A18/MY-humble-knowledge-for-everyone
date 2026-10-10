# Identity federation

Identity federation knowledge for OIDC, token trust, external identity providers, and cloud access.

## Articles

| Article | Purpose |
| --- | --- |
| [OIDC fundamentals](oidc-fundamentals.md) | Follow a browser authorization-code sign-in, then compare it with GitHub-to-AWS workload federation. |
| [OIDC token validation](oidc-token-validation.md) | See why decoding proves nothing and how a receiver checks the signature, issuer, token type, audience, expiry, and sign-in binding before applying its own permissions. |
| [EKS human identity and Kubernetes RBAC](eks-human-identity-and-rbac.md) | See how a person's IAM identity reaches the Kubernetes API, and how an access entry grants permissions through EKS access policies, RBAC groups, or both. |
| [AWS IAM OIDC provider and STS web identity](../../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md) | Understand AWS trust for external OIDC tokens. |
| [EKS workload identity](../../cross-topic-guides/eks-workload-identity.md) | Understand how Pods get temporary AWS credentials, and choose IRSA or EKS Pod Identity from a workload's conditions. |
| [AWS GitHub Actions OIDC federation](../../git/github-actions/aws-oidc-federation.md) | Federate GitHub Actions to AWS without long-lived credentials. |

[Back to security index](../index.md) | [Back to knowledge index](../../index.md)
