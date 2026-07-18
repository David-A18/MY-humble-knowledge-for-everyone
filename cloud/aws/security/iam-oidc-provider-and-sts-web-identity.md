# IAM OIDC provider and STS web identity

## Purpose

Use this page to understand how AWS trusts an external OpenID Connect provider and exchanges a valid token for temporary IAM credentials.

## Components

| Component | Role |
| --- | --- |
| OIDC provider | Issues signed tokens with issuer, audience, subject, and expiry claims. |
| IAM OIDC provider | AWS IAM object that represents the trusted issuer. |
| Trust policy | Defines which token claims may assume a role. |
| Permissions policy | Defines what the assumed role can do after trust succeeds. |
| STS `AssumeRoleWithWebIdentity` | Exchanges the web identity token for temporary AWS credentials. |

## Security rules

- Keep `aud` and `sub` trust conditions narrow.
- Separate trust policy decisions from permissions policy decisions.
- Prefer short-lived credentials over long-lived access keys.
- Log and review role assumptions.
- Do not treat an OIDC token as AWS authorization by itself; it must match IAM trust and permissions.

## Related links

- [OIDC fundamentals](../../../security/identity-federation/oidc-fundamentals.md)
- [EKS workload identity](../../../cross-topic-guides/eks-workload-identity.md)
- [AWS GitHub Actions OIDC federation](../../../git/github-actions/aws-oidc-federation.md)
- [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [Back to AWS security](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
