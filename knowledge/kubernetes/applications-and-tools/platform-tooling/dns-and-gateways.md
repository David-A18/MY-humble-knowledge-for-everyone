---
type: Explanation
title: DNS, gateways, and service meshes
description: Place naming, edge routing, and service-to-service controls in the correct
  layer.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: gateway-api
  resource: https://gateway-api.sigs.k8s.io/
  title: Gateway API
- id: externaldns
  resource: https://kubernetes-sigs.github.io/external-dns/
  title: ExternalDNS
- id: service-dns
  resource: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
  title: Service DNS
---

# DNS, gateways, and service meshes

## Purpose

Place naming, edge routing, and service-to-service controls in the correct layer.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Layer map

CoreDNS resolves cluster names such as `service.namespace.svc.cluster.local`. ExternalDNS reconciles supported resources into external DNS providers. Ingress/Gateway API describes incoming routes; an implementing controller forwards traffic. Istio adds mesh traffic controls and workload identity.[^gateway-api][^externaldns][^service-dns]

Gateway CRDs alone do not forward traffic. ExternalDNS does not terminate TLS. Public DNS does not make a private load balancer reachable.

| Need | Starting point |
| --- | --- |
| Resolve internal Service | CoreDNS and Service/EndpointSlice health |
| Maintain provider DNS records | ExternalDNS with zone-scoped permissions |
| Route incoming HTTP | Gateway API/Ingress and implementing controller |
| Authenticate API consumers | Gateway policy and identity-provider integration |
| Authorize workload traffic | Istio identities and mesh policy |

## Diagnostics

```bash
kubectl get service,endpointslice -n demo
kubectl get gateway,httproute -A
kubectl get ingress -A
kubectl get deployment -n kube-system coredns
```

What it does: checks endpoints, routes, and DNS. Gateway commands require the CRDs. Inspect route acceptance and reference conditions before changing DNS.

Trace DNS -> load balancer -> listener -> route -> Service -> ready endpoint -> application. Check certificates at the actual TLS terminator. Accept forwarded identity headers only from trusted proxies.

## Ownership and cleanup

ExternalDNS needs record ownership to prevent clusters deleting each other's records. Restrict provider permissions and domain filters. Use a test subdomain; understand deletion policy and TTL before removing resources.

## Related links

- [Gateway API](https://gateway-api.sigs.k8s.io/)
- [ExternalDNS](https://kubernetes-sigs.github.io/external-dns/)
- [Service DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Gateway API and Ingress](../gateway-api-and-ingress.md)
- [APISIX](../apache-apisix.md)
- [Istio](../istio/index.md)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^gateway-api]: [Gateway API](https://gateway-api.sigs.k8s.io/).
[^externaldns]: [ExternalDNS](https://kubernetes-sigs.github.io/external-dns/).
[^service-dns]: [Service DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).
