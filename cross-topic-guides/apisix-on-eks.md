# APISIX on EKS

## Purpose

Use this guide to run Apache APISIX as a Kubernetes API gateway on Amazon EKS.

## Reference architecture

| Layer | Common choice | Notes |
| --- | --- | --- |
| Edge | CloudFront or external CDN | Optional, useful for global delivery and edge security. |
| AWS load balancer | Network Load Balancer | Often used to expose APISIX Gateway. |
| Gateway | Apache APISIX Gateway | Handles routing and plugins. |
| Controller | APISIX Ingress Controller | Reconciles Kubernetes routing resources into APISIX config. |
| Workloads | Kubernetes Services and Pods | Backends must be healthy and discoverable. |

## Production checklist

- Choose Gateway API, Ingress, or APISIX CRDs deliberately.
- Keep TLS and certificate ownership clear.
- Apply authentication, rate limiting, and observability through explicit plugins.
- Monitor controller reconciliation, APISIX gateway health, and backend endpoints.
- Use GitOps for gateway configuration when multiple teams change routes.

## Related links

- [Apache APISIX](../kubernetes/applications-and-tools/apache-apisix.md)
- [Gateway API and Ingress](../kubernetes/applications-and-tools/gateway-api-and-ingress.md)
- [APISIX troubleshooting](../kubernetes/troubleshooting/apisix.md)
- [Amazon EKS documentation](https://docs.aws.amazon.com/eks/)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
