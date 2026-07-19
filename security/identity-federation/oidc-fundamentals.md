# OIDC fundamentals

## Purpose

Use this page to understand OpenID Connect before applying it to AWS, EKS, or GitHub Actions.

## What OIDC does

OpenID Connect adds an identity layer on top of OAuth 2.0. It lets an application or service trust signed tokens from an identity provider instead of handling passwords or long-lived shared credentials directly.

OIDC can support interactive user login, workload federation, and CI/CD federation, but each use case has different token claims, audiences, and trust policies.

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

## How it works

```text
subject authenticates with identity provider
  -> provider issues signed token
  -> relying party validates signature and claims
  -> application maps trusted claims to local authorization
```

OIDC authenticates identity. Authorization still happens in the relying application, AWS IAM role, Kubernetes RBAC rule, or API gateway policy.

## Token anatomy

```text
header.payload.signature
```

What it does: separates metadata, claims, and cryptographic proof. The payload can be decoded by anyone; the signature is what makes the claims trustworthy after validation.

## Validation checklist

- Verify the token signature with the issuer keys.
- Confirm `iss` is the expected issuer.
- Confirm `aud` matches the intended recipient.
- Confirm `exp` and `nbf` are valid for the current time.
- Authorize actions separately from authentication.

## Related links

- [OIDC token validation](oidc-token-validation.md)
- [EKS human identity and Kubernetes RBAC](eks-human-identity-and-rbac.md)
- [IAM OIDC provider and STS web identity](../../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
- [EKS workload identity](../../cross-topic-guides/eks-workload-identity.md)
- [OpenID Connect specification](https://openid.net/developers/specs/)
- [Back to identity federation](README.md)
- [Back to security index](../README.md)
- [Back to root index](../../README.md)
