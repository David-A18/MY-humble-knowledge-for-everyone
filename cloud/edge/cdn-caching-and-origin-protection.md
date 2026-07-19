# CDN caching and origin protection

## Purpose

Use this guide to design CDN cache behavior without exposing private data, overwhelming the origin, or leaving a bypass path around the edge layer.

## When to use it

Use this page when a public application, API, or static asset path sits behind Akamai, Amazon CloudFront, or another CDN and the team must decide cache keys, TTLs, purge behavior, and direct-origin controls.

## Key ideas

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Cache key | The request attributes that identify a cached response. | A broad key can leak or mix responses; a narrow key fragments cache. |
| TTL | How long an object can remain fresh at the edge. | Longer TTLs improve offload but increase stale-content risk. |
| Origin offload | Traffic served by edge cache instead of the origin. | Higher offload reduces load on ALB, EKS, databases, and storage. |
| Origin bypass | A path where clients can reach the origin directly. | Bypass can skip WAF, bot controls, rate limits, and cache protection. |
| Origin shield or tiered cache | An intermediate cache layer in front of the origin. | Reduces duplicate origin requests during global cache misses. |

## Cache-key decisions

Start by classifying each path.

| Path type | Typical cache behavior | Cache-key inputs |
| --- | --- | --- |
| Versioned static assets | Long TTL. Prefer immutable filenames. | Host, path, compression variant. |
| Public catalog or search response | Short or moderate TTL if freshness allows. | Path and only business-relevant query parameters. |
| Authenticated user data | Usually bypass cache. | Avoid caching unless isolation is proven. |
| Login, checkout, payment, admin | Bypass cache. | Do not include session-specific responses in shared cache. |
| API health or metadata | Short TTL or bypass depending on purpose. | Keep cache key minimal and intentional. |

### Query-parameter example

```text
/api/greeting?language=en&utm_source=campaign-a
/api/greeting?language=en&utm_source=campaign-b
```

What it does: both requests can share the same cached response when only `language` changes the response body and `utm_source` is used only for analytics.

> [!WARNING]
> Do not include every query parameter, cookie, or header in the cache key by default. That usually destroys hit ratio and can hide cache behavior problems until production traffic arrives.

## Origin protection patterns

| Origin type | Protection pattern | Notes |
| --- | --- | --- |
| Private S3 | CloudFront Origin Access Control. | Keep the bucket private and allow signed CloudFront origin requests. |
| Private ALB, NLB, or EC2 | CloudFront VPC origin where supported. | Use supported origin types and security groups rather than a public listener. |
| Public ALB | Restrict source paths where possible. | Use WAF, secret headers, strict Host checks, and monitoring for bypass attempts. |
| Akamai to AWS origin | Dedicated origin hostname plus source controls. | Avoid using the public CDN hostname as the origin hostname. |
| Multi-CDN origin | Provider-specific allowlists or private connectivity. | Keep behavior specifications consistent across CDNs. |

### Avoid CDN-to-origin loops

```text
Public hostname: shop.example.com
Origin hostname: origin-shop.example.com
```

What it does: keeps the CDN viewer hostname separate from the origin hostname so origin requests do not resolve back to the CDN and create a loop.

> [!IMPORTANT]
> Treat direct-origin access as a production incident risk. If the origin is reachable without the CDN, attackers and accidental clients can bypass edge WAF, rate limiting, bot controls, TLS policy, and cache offload.

## TTL and purge guidance

| Situation | Prefer | Reason |
| --- | --- | --- |
| Static files with build hashes | Long TTL and versioned filenames. | Rollback and cache safety are simpler than global purges. |
| Emergency bad object | Targeted invalidation or purge. | Removes unsafe content quickly. |
| Frequently changing HTML | Short TTL plus validation headers. | Balances freshness and offload. |
| Personalized response | Bypass or private cache controls. | Shared cache can expose user-specific data. |
| Large global release | Staged rollout and monitoring. | Prevents cache stampede against the origin. |

## Troubleshooting

| Symptom | First check | Likely cause |
| --- | --- | --- |
| Wrong user sees data | Cache policy and response headers. | Authenticated content was cached in a shared cache. |
| Origin traffic spikes after deployment | TTL, invalidations, and cache-key changes. | Many edge locations missed at once. |
| 502 from CloudFront custom origin | Origin TLS certificate and origin domain name. | Certificate name does not match the configured origin name. |
| Cache hit ratio is low | Query strings, cookies, and headers in key. | Cache key is too specific. |
| CDN appears bypassed | Origin access logs and Host headers. | Clients can reach the origin directly. |

## Related links

- Official documentation: [CloudFront Origin Access Control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
- Official documentation: [CloudFront VPC origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html)
- Official documentation: [Akamai Property Manager caching](https://techdocs.akamai.com/property-mgr/docs/know-caching)
- [CDN and edge fundamentals](cdn-and-edge-fundamentals.md)
- [Akamai vs. CloudFront](akamai-vs-cloudfront.md)
- [CloudFront](../aws/networking/cloudfront.md)
- [Back to edge and CDN](README.md)
- [Back to cloud index](../README.md)
- [Back to root index](../../README.md)
