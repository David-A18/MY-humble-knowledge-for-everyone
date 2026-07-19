# Multi-CDN operations

## Purpose

Use this guide to operate more than one CDN provider without creating inconsistent cache, security, DNS, logging, or rollback behavior.

## When to use it

Use a multi-CDN design when provider resilience, regional performance, contract requirements, or migration risk justify the extra operational burden.

## Design model

```text
Users
  -> DNS or traffic steering
  -> CDN provider A or CDN provider B
  -> protected origin layer
  -> application
```

The CDNs should usually run in parallel, not in an accidental chain.

> [!WARNING]
> Avoid `User -> CDN A -> CDN B -> origin` unless there is a deliberate and tested reason. Chaining can duplicate caches, confuse client IP handling, add latency, and make purge behavior ambiguous.

## Shared behavior contract

Create a provider-neutral behavior contract before configuring either CDN.

| Area | Contract question |
| --- | --- |
| Hostnames | Which public names route to each CDN? |
| TLS | Where are certificates issued, stored, renewed, and tested? |
| Origins | Which origin hostnames are allowed, and how is direct access blocked? |
| Cache keys | Which headers, cookies, and query parameters affect the response? |
| TTLs | Which paths are long-cache, short-cache, or no-cache? |
| Security | Which WAF, bot, rate, and geoblocking rules must match? |
| Logs | Which fields are required for incident response and analytics? |
| Purge | How is one asset removed across every provider? |
| Rollback | How do DNS, CDN config, and origin changes roll back independently? |

### Example behavior contract

```yaml
path: /assets/*
cache:
  ttl_seconds: 86400
  query_parameters: ignore
security:
  waf_policy: baseline
headers:
  add:
    X-Content-Type-Options: nosniff
origin:
  name: origin-shop.example.com
  timeout_seconds: 10
```

What it does: describes the intended behavior once, then each CDN implementation maps it to that provider's controls.

## DNS and traffic steering

| Pattern | Use when | Watch for |
| --- | --- | --- |
| Weighted DNS | You need simple traffic split or migration. | DNS caching slows exact cutovers. |
| Latency routing | User geography and network path matter. | Validate with real-user monitoring. |
| Health-check failover | A provider or origin path can fail. | Health checks must test useful application behavior. |
| Manual CNAME switch | You need a controlled migration step. | Prepare rollback before lowering confidence. |

## Operational checklist

- Keep a single owner for cache-key policy.
- Test every high-risk path on every provider before production traffic.
- Use versioned asset filenames where possible.
- Keep purge tooling provider-aware and auditable.
- Normalize request IDs, client IP headers, and trace headers.
- Send CDN logs to a common analysis location.
- Document provider-specific limits and activation delays.
- Test origin failover, CDN failover, and DNS rollback separately.

## Common mistakes

| Mistake | Result | Safer approach |
| --- | --- | --- |
| Comparing only point-of-presence counts. | Misleading performance decision. | Test with target users and real workload paths. |
| Using different cache keys per provider. | Different users see different behavior. | Maintain a shared behavior contract. |
| Purging one CDN only. | Stale content persists in the other path. | Use a multi-provider purge runbook. |
| Logging different fields. | Incidents cannot be correlated. | Define required log fields before go-live. |
| Letting origins remain public. | CDN controls are bypassable. | Restrict origins and monitor direct access. |

## Related links

- Official documentation: [Akamai Fast Purge](https://techdocs.akamai.com/purge-cache/reference/api)
- Official documentation: [CloudFront invalidations](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)
- [CDN caching and origin protection](cdn-caching-and-origin-protection.md)
- [Akamai vs. CloudFront](akamai-vs-cloudfront.md)
- [CDN in front of EKS](../../cross-topic-guides/cdn-in-front-of-eks.md)
- [Back to edge and CDN](README.md)
- [Back to cloud index](../README.md)
- [Back to root index](../../README.md)
