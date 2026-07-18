# Apache APISIX

## Purpose

Use this page to understand Apache APISIX as an API gateway for Kubernetes and EKS environments.

## Mental model

Apache APISIX is a gateway data plane and policy engine. In Kubernetes, the APISIX Ingress Controller watches Kubernetes resources such as Gateway API resources or APISIX custom resources and configures APISIX Gateway.

| Area | What it does |
| --- | --- |
| Route | Matches requests and sends them to upstream services. |
| Upstream | Defines backend targets and load balancing. |
| Plugin | Adds policy such as auth, rate limiting, traffic shaping, or observability. |
| Consumer | Represents a caller identity for API-key or credential-based plugins. |
| Ingress Controller | Reconciles Kubernetes desired state into APISIX configuration. |

## When APISIX fits

- You need Kubernetes ingress plus API gateway policies.
- Teams need route-level plugins for authentication, rate limiting, transformations, or traffic releases.
- You want Gateway API or APISIX CRDs to manage traffic through Kubernetes-native workflows.

## Related links

- [Gateway API and Ingress](gateway-api-and-ingress.md)
- [APISIX on EKS](../../cross-topic-guides/apisix-on-eks.md)
- [APISIX troubleshooting](../troubleshooting/apisix.md)
- [Apache APISIX Ingress Controller documentation](https://apisix.apache.org/docs/ingress-controller/)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
