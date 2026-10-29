# Identity federation

Identity federation knowledge for OIDC, token trust, external identity providers, and cloud access.

## AWS workload implementation

Continue with [IRSA trust](../../cloud/aws/security/irsa-trust-and-permissions.md) and the [EKS S3 lab](../../cross-topic-guides/irsa-s3-access-on-eks.md).

## Articles

| Article | Purpose |
| --- | --- |
| [OIDC fundamentals](oidc-fundamentals.md) | Understand OpenID Connect actors, tokens, claims, discovery, and validation. |
| [OIDC token validation](oidc-token-validation.md) | Validate JWT signatures, issuer, audience, time claims, JWKS keys, and token purpose. |
| [EKS human identity and Kubernetes RBAC](eks-human-identity-and-rbac.md) | Separate human EKS authentication from workload identity and bind access with RBAC. |
| [AWS IAM OIDC provider and STS web identity](../../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md) | Understand AWS trust for external OIDC tokens. |
| [EKS workload identity](../../cross-topic-guides/eks-workload-identity.md) | Choose between IRSA and EKS Pod Identity. |
| [AWS GitHub Actions OIDC federation](../../git/github-actions/aws-oidc-federation.md) | Federate GitHub Actions to AWS without long-lived credentials. |

[Back to security index](../index.md) | [Back to root index](../../../README.md)
