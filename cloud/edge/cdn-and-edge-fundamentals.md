# CDN and edge fundamentals

## Purpose

Use this page to understand the basic CDN and edge-computing vocabulary used by CloudFront, Akamai, and multi-CDN designs.

## Key concepts

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Edge location | Provider location close to users. | Reduces latency and absorbs traffic away from the origin. |
| Cache hit | Edge already has a valid response. | Improves performance and reduces origin load. |
| Cache miss | Edge must fetch from the origin. | Adds latency and origin cost. |
| Origin | Backend source such as S3, ALB, API, or custom server. | Must be protected from direct and excessive traffic. |
| Edge compute | Code that runs near the viewer or request path. | Useful for redirects, header changes, lightweight auth, or personalization. |

## Design checklist

- Identify which responses are cacheable and for how long.
- Keep cache keys deliberate; extra headers, cookies, or query strings reduce hit ratio.
- Protect origins with private access, allow lists, signed requests, or service-native controls.
- Monitor cache hit ratio, origin latency, errors, and edge security events.
- Plan DNS, TLS, and rollback before CDN migrations.

## Related links

- [Akamai vs. CloudFront](akamai-vs-cloudfront.md)
- [CloudFront](../aws/networking/cloudfront.md)
- [Amazon CloudFront documentation](https://docs.aws.amazon.com/cloudfront/)
- [Back to edge and CDN index](README.md)
- [Back to cloud index](../README.md)
- [Back to root index](../../README.md)
