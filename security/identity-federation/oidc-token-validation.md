# OIDC token validation

## Purpose

Use this guide to validate OIDC and JWT tokens safely before trusting identity claims in an application, gateway, or federation flow.

## Components

| Component | What it does |
| --- | --- |
| Issuer | Identity provider that signs tokens. |
| Discovery document | Metadata document that publishes endpoints and signing-key location. |
| JWKS | Public key set used to verify token signatures. |
| ID token | Token that tells a relying party about user authentication. |
| Access token | Token intended for an API or resource server. |
| Claims | Token fields such as `iss`, `sub`, `aud`, and `exp`. |
| Client ID | Identifier for the application or relying party. |
| Nonce | Login-flow value used to prevent replay. |

## How validation works

```text
token arrives
  -> decode header to find algorithm and key ID
  -> load issuer metadata and JWKS
  -> verify signature
  -> validate issuer, audience, time, and token purpose
  -> map trusted claims to application identity
```

Only after this sequence should an application use claims for identity or authorization decisions.

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

### Discovery example

```bash
curl -s https://issuer.example.com/.well-known/openid-configuration
```

What it does: retrieves issuer metadata such as the JWKS URI, authorization endpoint, token endpoint, and supported algorithms.

## ID token or access token

| Token | Intended use | Common mistake |
| --- | --- | --- |
| ID token | Proves authentication to a relying party. | Sending it to APIs as a bearer authorization token. |
| Access token | Authorizes access to an API or resource server. | Treating provider-specific claims as universal. |
| Refresh token | Gets new tokens from the token endpoint. | Exposing it to browsers, logs, or frontend code. |

## Pseudocode example

```text
metadata = fetch(issuer + "/.well-known/openid-configuration")
keys = fetch(metadata.jwks_uri)
claims = verify_signature(token, keys, allowed_algorithms)
require claims.iss == expected_issuer
require expected_audience in claims.aud
require now < claims.exp
require claims.nbf is absent or now >= claims.nbf
```

What it does: shows the minimum trust checks before the application treats token claims as authenticated identity.

## AWS federation note

AWS STS `AssumeRoleWithWebIdentity` exchanges a trusted web identity token for AWS temporary credentials. The resulting AWS access key, secret access key, and session token are not OIDC tokens; they are AWS credentials with IAM permissions controlled by the role.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Signature verification fails after key rotation. | JWKS cache did not refresh for a new `kid`. |
| Token validates in one app but not another. | Audience or authorized-party claim differs. |
| Expired token is accepted. | Application skipped time validation or has clock skew. |
| API accepts an ID token as bearer token. | Token purpose was not validated. |
| AWS role assumption fails. | IAM provider, trust policy, audience, or subject condition mismatch. |

## Related links

- Official documentation: [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- Official documentation: [AWS IAM OIDC providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [OIDC fundamentals](oidc-fundamentals.md)
- [AWS IAM OIDC provider and STS web identity](../../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
- [Back to identity federation](README.md)
- [Back to security index](../README.md)
- [Back to root index](../../README.md)
