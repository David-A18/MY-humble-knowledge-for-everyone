---
type: Explanation
title: JWT authentication and Istio authorization
description: Validate end-user tokens and combine them with workload identity.
tags:
- kubernetes
- istio
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: requestauthentication-api
  resource: https://istio.io/latest/docs/reference/config/security/request_authentication/
  title: RequestAuthentication API
- id: authorizationpolicy-api
  resource: https://istio.io/latest/docs/reference/config/security/authorization-policy/
  title: AuthorizationPolicy API
---

# JWT authentication and Istio authorization

## Purpose

Validate end-user tokens and combine them with workload identity.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Request identity differs from peer identity

mTLS identifies the calling workload. A JWT can identify an end user or external client. `RequestAuthentication` validates accepted token issuers, signatures, audiences, and lifetime using configured or discovered JWKS. Istio validates tokens; it does not act as your login service or issue application tokens.[^requestauthentication-api][^authorizationpolicy-api]

## Validation and mandatory authentication

```yaml
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata:
  name: api-jwt
  namespace: demo
spec:
  selector:
    matchLabels:
      app: web
  jwtRules:
    - issuer: https://issuer.example.test
      audiences: [demo]
      jwksUri: https://issuer.example.test/.well-known/jwks.json
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: demo
spec:
  selector:
    matchLabels:
      app: web
  action: ALLOW
  rules:
    - from:
        - source:
            requestPrincipals: ["*"]
      to:
        - operation:
            methods: [GET]
```

What it does: accepts tokens from a specified issuer/audience and permits GET only for authenticated request principals. The example issuer is intentionally non-resolving: substitute a real IdP or use the lab's inline JWKS.

A missing token can pass request authentication; the AuthorizationPolicy makes it mandatory. A malformed or invalid presented token normally yields 401; a request failing authorization normally yields 403. Proxies/gateways can transform responses, so diagnose the enforcing hop.

## Policy composition

ALLOW rules combine additively across matching ALLOW policies; one broad rule can weaken a narrow rule. Matching DENY rules override ALLOW. CUSTOM, DENY, ALLOW, and AUDIT have different semantics: AUDIT is not a blocking control. An empty ALLOW rule set denies covered requests, while a matching unrestricted rule permits them.

Use `source.principals` for workload identities and `requestPrincipals`/verified claims for JWT identity. Restrict methods, paths, and ports deliberately. Token forwarding is a separate decision; avoid exposing bearer tokens to unnecessary upstream services.

## Rotation and troubleshooting

Test issuer/audience mismatch, expiry, JWKS reachability, key rollover, missing tokens, and insufficient claims. Never trust an unverified claim copied into an ordinary HTTP header. Introduce new signing keys with overlap so cached validators can refresh.

## Related links

- [RequestAuthentication API](https://istio.io/latest/docs/reference/config/security/request_authentication/)
- [AuthorizationPolicy API](https://istio.io/latest/docs/reference/config/security/authorization-policy/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^requestauthentication-api]: [RequestAuthentication API](https://istio.io/latest/docs/reference/config/security/request_authentication/).
[^authorizationpolicy-api]: [AuthorizationPolicy API](https://istio.io/latest/docs/reference/config/security/authorization-policy/).
