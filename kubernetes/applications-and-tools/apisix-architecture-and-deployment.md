# APISIX architecture and deployment

## Purpose

Use this guide to understand how Apache APISIX, the APISIX Ingress Controller, Gateway API, and Kubernetes Services fit together before choosing a deployment mode.

## Mental model

```text
Client traffic
  -> cloud load balancer
  -> APISIX gateway data plane
  -> plugins and route matching
  -> Kubernetes Service and Pod endpoints

Configuration traffic
  -> Git or kubectl
  -> Kubernetes API
  -> APISIX Ingress Controller
  -> APISIX gateway configuration
```

The ingress controller is normally not in the user request path. It watches Kubernetes resources and programs the gateway.

## Main components

| Component | Role | Operational concern |
| --- | --- | --- |
| APISIX gateway | Data plane that receives requests and proxies to upstreams. | Scale, readiness, TLS, plugins, and resource limits. |
| APISIX Ingress Controller | Reconciles Kubernetes resources into APISIX configuration. | RBAC, version compatibility, and controller errors. |
| Gateway API resources | Standard Kubernetes API for gateways and routes. | Status conditions such as `Accepted` and `Programmed`. |
| APISIX CRDs | APISIX-specific extensions for gateway behavior. | Avoid mixing incompatible API generations. |
| Kubernetes Service and EndpointSlice | Backend discovery. | Service selectors, ready endpoints, and port names. |

## Deployment modes

| Mode | Good fit | Notes |
| --- | --- | --- |
| Traditional | Teams already operating APISIX Admin API and etcd. | Protect the Admin API and operate etcd carefully. |
| Decoupled control and data plane | Larger or security-sensitive environments. | Separates management from public traffic. |
| Standalone file-driven | Generated declarative configuration. | Requires a safe file distribution process. |
| API-driven standalone | Kubernetes controller integrations. | Review maturity and version compatibility before production. |

> [!IMPORTANT]
> Choose the mode based on recovery, isolation, configuration durability, and support needs. Fewer components can still be harder to operate if configuration cannot be restored reliably after a restart.

## Gateway API object flow

```text
GatewayClass
  -> Gateway
  -> HTTPRoute
  -> Service
  -> EndpointSlice
  -> Pods
```

### Inspect route status

```bash
kubectl describe gatewayclass apisix
kubectl describe gateway public-api -n gateway-system
kubectl describe httproute orders -n orders
```

What it does: shows whether the controller accepted and programmed the gateway and route resources.

## EKS exposure pattern

A common Amazon EKS path is:

```text
Route 53
  -> AWS Network Load Balancer
  -> APISIX gateway Service
  -> APISIX Pods
  -> application Service
  -> application Pods
```

Use an NLB when APISIX should own Layer 7 gateway behavior while AWS provides a resilient Layer 4 entry point.

## Troubleshooting order

1. DNS record.
2. AWS load balancer listener and target health.
3. APISIX gateway Service and Pods.
4. APISIX Ingress Controller logs.
5. Gateway API or APISIX CRD status.
6. Backend Service and EndpointSlice.
7. Direct in-cluster request to the backend.
8. Direct request to APISIX with the expected Host header.

### Test the gateway directly

```bash
kubectl port-forward -n ingress-apisix svc/apisix-gateway 9080:80
curl -i -H 'Host: api.example.com' http://127.0.0.1:9080/orders
```

What it does: separates APISIX route behavior from DNS and cloud load balancer behavior.

## Related links

- Official documentation: [APISIX deployment modes](https://apisix.apache.org/docs/apisix/deployment-modes/)
- Official documentation: [APISIX Ingress Controller deployment architecture](https://apisix.apache.org/docs/ingress-controller/concepts/deployment-architecture/)
- Official documentation: [APISIX Gateway API support](https://apisix.apache.org/docs/ingress-controller/concepts/gateway-api/)
- [Apache APISIX](apache-apisix.md)
- [Gateway API and Ingress](gateway-api-and-ingress.md)
- [APISIX on EKS](../../cross-topic-guides/apisix-on-eks.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
