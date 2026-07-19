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

## How APISIX handles a request

1. A client connects through DNS and the cloud load balancer.
2. APISIX accepts the connection on a gateway listener.
3. TLS and SNI configuration select the certificate where APISIX terminates TLS.
4. The router matches host, path, method, header, or other criteria.
5. Plugins run in request phases such as rewrite, access, proxy, response, and log.
6. APISIX selects an upstream target.
7. The request is proxied to a Kubernetes Service endpoint or other backend.
8. APISIX records logs, metrics, and tracing data.

This makes APISIX both a reverse proxy and a policy execution point.

## Main components

| Component | Role | Operational concern |
| --- | --- | --- |
| APISIX gateway | Data plane that receives requests and proxies to upstreams. | Scale, readiness, TLS, plugins, and resource limits. |
| APISIX Ingress Controller | Reconciles Kubernetes resources into APISIX configuration. | RBAC, version compatibility, and controller errors. |
| Gateway API resources | Standard Kubernetes API for gateways and routes. | Status conditions such as `Accepted` and `Programmed`. |
| APISIX CRDs | APISIX-specific extensions for gateway behavior. | Avoid mixing incompatible API generations. |
| Kubernetes Service and EndpointSlice | Backend discovery. | Service selectors, ready endpoints, and port names. |

## APISIX object model

| Object | What it does | Kubernetes-facing equivalent |
| --- | --- | --- |
| Route | Matches requests and attaches behavior. | `HTTPRoute`, `Ingress`, or APISIX route CRD. |
| Upstream | Defines backend targets and load-balancing behavior. | Service endpoints or explicitly defined nodes. |
| Service | Reusable APISIX policy and upstream abstraction. | Not the same as a Kubernetes `Service`. |
| Consumer | Represents a known caller. | Often created through APISIX consumer resources. |
| Plugin | Adds behavior such as auth, rate limit, rewrite, or telemetry. | Gateway policy or APISIX-specific configuration. |
| SSL object | Stores certificate/SNI behavior. | Kubernetes `Secret` and gateway TLS config. |

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

### Minimal HTTPRoute example

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: orders
  namespace: orders
spec:
  parentRefs:
    - name: public-api
      namespace: gateway-system
  hostnames:
    - api.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /orders
      backendRefs:
        - name: orders-service
          port: 8080
```

What it does: asks the gateway controller to route `api.example.com/orders` traffic to the `orders-service` backend.

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

### EKS Service exposure example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: apisix-gateway
  namespace: ingress-apisix
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: external
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      targetPort: 9080
    - name: https
      port: 443
      targetPort: 9443
  selector:
    app.kubernetes.io/name: apisix
```

What it does: exposes APISIX gateway Pods through an AWS Network Load Balancer using IP targets.

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
