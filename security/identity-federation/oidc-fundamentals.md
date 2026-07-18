# OIDC fundamentals

## Purpose

Use this page to understand OpenID Connect before applying it to AWS, EKS, or GitHub Actions.

## Concepts

| Concept | Meaning |
| --- | --- |
| OpenID Provider | Identity provider that issues signed tokens. |
| Relying Party | Application or service that trusts the provider. |
| Issuer | Stable URL identifying the token issuer. |
| JWKS | Public keys used to verify token signatures. |
| ID token | Token carrying authentication claims about a subject. |
| Access token | Token used to access an API. |
| Claims | Token fields such as `iss`, `sub`, `aud`, and `exp`. |

## Validation checklist

- Verify the token signature with the issuer keys.
- Confirm `iss` is the expected issuer.
- Confirm `aud` matches the intended recipient.
- Confirm `exp` and `nbf` are valid for the current time.
- Authorize actions separately from authentication.

## Related links

- [IAM OIDC provider and STS web identity](../../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
- [EKS workload identity](../../cross-topic-guides/eks-workload-identity.md)
- [OpenID Connect specification](https://openid.net/developers/specs/)
- [Back to identity federation](README.md)
- [Back to security index](../README.md)
- [Back to root index](../../README.md)
