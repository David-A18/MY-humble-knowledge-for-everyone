# OIDC token validation

## Purpose

Use this guide to validate OIDC and JWT tokens safely before trusting identity claims in an application, gateway, or federation flow.

## Validation sequence

| Step | Check | Why |
| --- | --- | --- |
| Parse safely | Decode without trusting claims yet. | The payload is not proof by itself. |
| Restrict algorithms | Allow only expected signing algorithms. | Prevent algorithm-confusion attacks. |
| Fetch signing keys | Use issuer JWKS. | Confirms which public keys are trusted. |
| Verify signature | Match token `kid` to a valid key. | Proves the issuer signed the token. |
| Validate issuer | Check `iss` exactly. | Prevents accepting tokens from another issuer. |
| Validate audience | Check `aud` and `azp` where applicable. | Ensures the token is intended for this client/API. |
| Validate time | Check `exp`, `nbf`, and clock skew. | Rejects expired or not-yet-valid tokens. |
| Validate nonce | For interactive login. | Prevents replay into the login flow. |
| Validate token type | ID token versus access token. | Prevents using a token for the wrong purpose. |
| Validate app claims | Required groups, tenant, or subject rules. | Applies local authorization policy. |

> [!WARNING]
> Do not authorize a request only because a JWT decodes successfully. A decoded payload is untrusted until signature, issuer, audience, time, and intended-use checks pass.

## JWKS and key rotation

The issuer publishes public signing keys through a JWKS endpoint, usually discovered from:

```text
https://issuer.example.com/.well-known/openid-configuration
```

Applications should:

- cache keys for a bounded time,
- refetch when a token references an unknown `kid`,
- keep issuer matching strict,
- handle key rotation without disabling validation,
- fail closed when validation cannot be completed.

## ID token or access token

| Token | Intended use | Common mistake |
| --- | --- | --- |
| ID token | Proves authentication to a relying party. | Sending it to APIs as a bearer authorization token. |
| Access token | Authorizes access to an API or resource server. | Treating provider-specific claims as universal. |
| Refresh token | Gets new tokens from the token endpoint. | Exposing it to browsers, logs, or frontend code. |

## AWS federation note

AWS STS `AssumeRoleWithWebIdentity` exchanges a trusted web identity token for AWS temporary credentials. The resulting AWS access key, secret access key, and session token are not OIDC tokens; they are AWS credentials with IAM permissions controlled by the role.

## Related links

- Official documentation: [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- Official documentation: [AWS IAM OIDC providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [OIDC fundamentals](oidc-fundamentals.md)
- [AWS IAM OIDC provider and STS web identity](../../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
- [Back to identity federation](README.md)
- [Back to security index](../README.md)
- [Back to root index](../../README.md)
