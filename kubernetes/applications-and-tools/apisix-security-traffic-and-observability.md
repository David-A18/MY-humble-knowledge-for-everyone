# APISIX security, traffic, and observability

## Purpose

Use this guide to place the right policy in Apache APISIX without turning the gateway into hidden business logic.

## How policy execution works

APISIX evaluates route matching and plugins around the request lifecycle.

```text
client request
  -> rewrite phase
  -> access phase
  -> upstream selection
  -> proxy request
  -> response header/body processing
  -> log phase
```

Authentication, authorization, and rate limiting usually happen before the request reaches the backend. Logging and metrics happen after APISIX has enough request and response context.

## Policy placement

| Policy | Good gateway responsibility | Keep in application code |
| --- | --- | --- |
| Authentication | API key, JWT, OIDC validation, mTLS. | User lifecycle and account recovery. |
| Authorization | Coarse consumer, tenant, route, or scope checks. | Domain ownership and transaction rules. |
| Rate limits | Per IP, consumer, credential, or tenant limits. | Business quotas that need transactional state. |
| Routing | Host, path, header, canary, and weighted routing. | Workflow decisions based on private domain data. |
| Observability | Request IDs, metrics, logs, traces. | Domain events and business audit records. |

## Policy components

| Component | What it controls |
| --- | --- |
| Route plugin | Behavior attached to one matched API path. |
| Service plugin | Behavior shared by several routes. |
| Consumer plugin | Policy applied after caller identity is known. |
| Global rule | Broad policy across gateway traffic. |
| Plugin config | Reusable plugin settings referenced by routes or consumers. |
| Secret or credential | API key, JWT secret, client certificate, or IdP settings. |

## Authentication and identity

APISIX can identify callers through plugins such as key authentication, JWT authentication, OpenID Connect, and mTLS.

| Pattern | Use when | Watch for |
| --- | --- | --- |
| API key | Machine clients need simple consumer identity. | Keys must be rotated and scoped. |
| JWT | A trusted issuer signs bearer tokens. | Validate issuer, audience, expiration, and algorithm. |
| OIDC | Interactive login or token validation against an identity provider is required. | Keep redirect and token flows distinct from API bearer validation. |
| mTLS | Client certificate identity is required. | Certificate lifecycle and revocation must be operational. |

> [!WARNING]
> Forwarded identity headers are trustworthy only when every path to the backend passes through the gateway and the backend rejects spoofed direct requests.

## Rate limiting

Choose the limiting key based on the abuse or fairness problem.

| Key | Good for | Risk |
| --- | --- | --- |
| Client IP | Basic edge protection. | Shared NATs and proxies can punish many users together. |
| Consumer | API product quotas. | Requires reliable authentication first. |
| Tenant | SaaS fairness. | Requires tenant identity in the gateway context. |
| Route | Protecting expensive endpoints. | Does not distinguish callers. |

### Rate-limit policy example

```yaml
plugins:
  limit-count:
    count: 1000
    time_window: 60
    key_type: var
    key: consumer_name
```

What it does: expresses a per-consumer request limit for a 60-second window. The exact Kubernetes wrapper depends on the APISIX Ingress Controller API version in use.

## Traffic release patterns

| Pattern | Use when | Validation |
| --- | --- | --- |
| Weighted canary | Gradually move traffic to a new backend. | Compare errors, latency, and saturation by backend version. |
| Header canary | Test with internal users or synthetic clients. | Confirm only intended clients match. |
| Cookie canary | Keep a user on one version during a session. | Check cookie TTL and rollback path. |
| Blue/green | Switch between complete environments. | Keep DNS, gateway, and backend rollback independent. |

## Observability

Minimum telemetry for production APISIX routes:

- request ID or correlation ID,
- matched route,
- consumer or tenant where available,
- upstream service,
- response status,
- request duration,
- upstream duration,
- rate-limit decisions,
- authentication and authorization failures,
- gateway and upstream error classes.

### Request ID propagation example

```text
Client -> APISIX adds or preserves X-Request-ID
APISIX -> backend receives X-Request-ID
Backend -> logs X-Request-ID with business context
APISIX -> access log includes same X-Request-ID
```

What it does: allows the platform team to connect gateway logs, application logs, and distributed traces during an incident.

### Check gateway and controller logs

```bash
kubectl logs -n ingress-apisix deployment/apisix-ingress-controller
kubectl logs -n ingress-apisix -l app.kubernetes.io/name=apisix
```

What it does: separates reconciliation errors from data-plane request handling.

## Failure symptoms

| Symptom | Likely layer | First check |
| --- | --- | --- |
| `404` from APISIX | Route matching. | Host header, path, route status, controller logs. |
| `401` | Authentication. | Token/key presence, issuer, audience, credential object. |
| `403` | Authorization or security policy. | IP restriction, consumer policy, mTLS, WAF layer. |
| `429` | Rate limiting. | Limiter key, window, route, and retry behavior. |
| `503` | Upstream health. | Service endpoints, readiness, health checks, NetworkPolicy. |

## Related links

- Official documentation: [APISIX plugins](https://apisix.apache.org/docs/apisix/terminology/plugin/)
- Official documentation: [APISIX OpenID Connect plugin](https://apisix.apache.org/docs/apisix/plugins/openid-connect/)
- Official documentation: [APISIX Prometheus plugin](https://apisix.apache.org/docs/apisix/plugins/prometheus/)
- [APISIX architecture and deployment](apisix-architecture-and-deployment.md)
- [APISIX troubleshooting](../troubleshooting/apisix.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
