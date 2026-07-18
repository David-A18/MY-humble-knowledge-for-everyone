# Gateway API and Ingress

## Purpose

Use this page to choose between Kubernetes Ingress, Gateway API, and gateway-specific custom resources.

## Comparison

| Option | Use it when | Watch for |
| --- | --- | --- |
| Ingress | You need simple HTTP routing. | Provider-specific annotations often become hard to port. |
| Gateway API | You need role-oriented, extensible L4/L7 routing. | Requires a compatible controller. |
| Gateway-specific CRDs | You need vendor features beyond standard APIs. | Stronger coupling to one controller. |

## Gateway API roles

- Platform teams usually own `GatewayClass` and shared `Gateway` infrastructure.
- Application teams usually own `HTTPRoute` or other route resources.
- Security teams may own policy attachment, TLS, and allowed route boundaries.

## Related links

- [Apache APISIX](apache-apisix.md)
- [Kubernetes Gateway API documentation](https://kubernetes.io/docs/concepts/services-networking/gateway/)
- [Gateway API project documentation](https://gateway-api.sigs.k8s.io/)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
