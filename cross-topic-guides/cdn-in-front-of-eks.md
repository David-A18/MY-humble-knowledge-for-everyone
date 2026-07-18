# CDN in front of EKS

## Purpose

Use this guide to place a CDN such as CloudFront or Akamai in front of workloads running on Amazon EKS.

## Request path

1. User resolves the public hostname through DNS.
2. The CDN terminates TLS and evaluates cache, security, and routing rules.
3. Cacheable responses are served at the edge.
4. Dynamic requests go to the origin, often an AWS load balancer in front of Kubernetes ingress.
5. Kubernetes routes the request to the application Service and Pods.

## Design checklist

- Decide which paths are cacheable and which must always reach the origin.
- Keep origin access controlled so clients cannot bypass the CDN.
- Align CDN TLS names, ingress host rules, and application redirects.
- Monitor CDN errors, origin latency, ingress errors, and application errors together.
- Test rollback by lowering DNS TTLs and keeping the previous origin path available during migration.

## Related links

- [CDN and edge fundamentals](../cloud/edge/cdn-and-edge-fundamentals.md)
- [CloudFront](../cloud/aws/networking/cloudfront.md)
- [Kubernetes on AWS](kubernetes-on-aws.md)
- [Deploying to EKS](deploying-to-eks.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
