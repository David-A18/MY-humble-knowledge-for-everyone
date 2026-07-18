# Akamai vs. CloudFront

## Purpose

Use this page to choose between Akamai, Amazon CloudFront, or a multi-CDN approach.

## Comparison

| Area | Akamai | CloudFront |
| --- | --- | --- |
| Platform fit | Broad edge platform with many enterprise traffic, security, and delivery products. | AWS-native CDN integrated with AWS origins, IAM, WAF, logs, and infrastructure automation. |
| Best fit | Large enterprise edge programs, complex global delivery, non-AWS estates, advanced vendor-managed edge features. | AWS-centered workloads, S3 and ALB origins, IaC-driven delivery, and teams already operating AWS. |
| Operations | Uses Akamai property, contract, group, product, and edge-hostname concepts. | Uses distributions, origins, cache behaviors, policies, functions, and AWS service integrations. |
| Migration focus | DNS, TLS, property rules, origin behavior, and staged traffic migration. | Distribution behavior, origin protection, cache policy, WAF, logs, and rollback plan. |

## Decision guide

- Choose CloudFront when the workload is mostly AWS-native and the team wants infrastructure-as-code integration with AWS controls.
- Choose Akamai when enterprise edge features, global delivery requirements, or non-AWS estates are the stronger driver.
- Consider multi-CDN only when availability, latency, geography, contract, or business requirements justify the added operational complexity.

## Common mistakes

- Comparing only CDN price and ignoring security, operations, logs, and migration effort.
- Migrating DNS without a tested rollback path.
- Caching personalized or auth-sensitive responses without a deliberate cache key.
- Leaving origins directly reachable when the CDN should be the controlled entry point.

## Related links

- [CDN and edge fundamentals](cdn-and-edge-fundamentals.md)
- [CloudFront](../aws/networking/cloudfront.md)
- [CDN in front of EKS](../../cross-topic-guides/cdn-in-front-of-eks.md)
- [Amazon CloudFront documentation](https://docs.aws.amazon.com/cloudfront/)
- [Akamai documentation](https://techdocs.akamai.com/)
- [Back to edge and CDN index](README.md)
- [Back to cloud index](../README.md)
- [Back to root index](../../README.md)
