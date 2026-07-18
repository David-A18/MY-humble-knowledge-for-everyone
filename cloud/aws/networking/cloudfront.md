# CloudFront

## Purpose

Use this page to design Amazon CloudFront distributions for AWS applications, APIs, static sites, and EKS ingress paths.

## Core objects

| Object | Meaning | Design note |
| --- | --- | --- |
| Distribution | CloudFront configuration that receives viewer requests. | Owns origins, cache behaviors, TLS, logging, and security settings. |
| Origin | Backend source such as S3, ALB, API Gateway, or custom HTTP server. | Protect direct origin access when possible. |
| Cache behavior | Path-based routing and cache rules. | Use separate behaviors for static, API, and auth-sensitive paths. |
| Cache policy | Controls cache key and TTL inputs. | Keep headers, cookies, and query strings narrow. |
| Origin request policy | Controls what CloudFront forwards to the origin. | Forward only what the origin needs. |

## Design checklist

- Use S3 origin access control for private S3 origins.
- Put AWS WAF in front of internet-facing distributions when application-layer filtering is needed.
- Separate cacheable static paths from dynamic API paths.
- Enable access logs or real-time logs when operations require request-level visibility.
- Plan invalidations carefully; broad invalidations can hide weak versioning practices.

## Related links

- [CDN and edge fundamentals](../../edge/cdn-and-edge-fundamentals.md)
- [Akamai vs. CloudFront](../../edge/akamai-vs-cloudfront.md)
- [CDN in front of EKS](../../../cross-topic-guides/cdn-in-front-of-eks.md)
- [Amazon CloudFront documentation](https://docs.aws.amazon.com/cloudfront/)
- [Back to AWS networking](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
