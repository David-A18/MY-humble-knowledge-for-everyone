# Cloud

Provider-neutral and provider-specific cloud knowledge.

Status: Initial outline

## Providers

| Provider | Use it for |
| --- | --- |
| [AWS](aws/README.md) | AWS fundamentals, networking, compute, storage, security, governance, FinOps, architecture, troubleshooting, and certification notes. |
| [Azure](azure/README.md) | Azure services, identity, networking, operations, cost, governance, and architecture notes. |
| [Google Cloud](gcloud/README.md) | Google Cloud services, identity, networking, operations, cost, governance, and architecture notes. |

## Shared cloud areas

| Area | Use it for |
| --- | --- |
| [Edge and CDN](edge/README.md) | CDN, edge routing, cache behavior, origin protection, and multi-CDN guidance. |

## Edge and CDN quick paths

| Topic | Start here | Follow-up |
| --- | --- | --- |
| Akamai or "Acamai" | [Akamai vs. CloudFront](edge/akamai-vs-cloudfront.md) | Compare concepts, product fit, cache behavior, origin protection, and migration risks. |
| Amazon CloudFront | [CloudFront](aws/networking/cloudfront.md) | Design AWS-native CDN distributions, origins, cache behavior, and EKS edge paths. |
| CDN caching | [CDN caching and origin protection](edge/cdn-caching-and-origin-protection.md) | Design cache keys, TTLs, purges, and direct-origin controls. |
| Multi-CDN operations | [Multi-CDN operations](edge/multi-cdn-operations.md) | Keep DNS, cache, security, logs, purges, and rollback consistent across providers. |

## Provider-neutral topics

- Cloud operating models.
- Multi-cloud comparison notes.
- Shared architecture, governance, reliability, and cost-management patterns.

[Back to root index](../README.md)
