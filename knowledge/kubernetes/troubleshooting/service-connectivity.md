---
type: Troubleshooting Guide
title: Service connectivity failures
description: Isolate Service routing failures across selectors, EndpointSlices, application
  ports, and network enforcement.
tags:
- kubernetes
- troubleshooting
- services
- networking
- endpoint-slices
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: debug-service
  title: Debug Services
  resource: https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/
- id: endpoint-slices
  title: EndpointSlices
  resource: https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/
- id: network-policies
  title: Network Policies
  resource: https://kubernetes.io/docs/concepts/services-networking/network-policies/
---

# Service connectivity failures

Use this guide when an in-cluster client cannot reach a Service. If the name does not resolve, start with [DNS resolution](dns-resolution.md). The path to inspect is client → Service address/port → selected endpoint → listening application. Keep the same client identity, namespace, and destination while comparing tests.

## Inspect the declared path

Use a permitted client Pod with `curl` or equivalent already installed. Replace the selector below with the Service's actual selector. Do not install debugging software into a production container just to follow the example.

```bash
kubectl get service <service> -n <namespace> -o yaml
kubectl get pods -n <namespace> -l '<service-selector>' -o wide --show-labels
kubectl get endpointslices.discovery.k8s.io -n <namespace> -l kubernetes.io/service-name=<service> -o yaml
```

What it does: compares the Service's selector, `port`, `targetPort`, and protocol with selected Pods and the published endpoint ports. A named `targetPort` must resolve to the intended named container port. A declared `containerPort` does not start a listener.[^debug-service]

Inspect every matching EndpointSlice; a Service can have several, including separate address families. Check endpoint addresses, target references, `ready`, `serving`, and `terminating`. Ordinarily non-ready endpoints do not receive regular traffic, but `publishNotReadyAddresses` changes readiness publication. Selectorless Services require a separately managed endpoint path.[^endpoint-slices]

## Compare the same request at two layers

These commands send application requests. Use a safe read-only health path with no side effects and the correct protocol; `8080` and `/health` are illustrative.

```bash
kubectl exec <client-pod> -n <client-namespace> -c <client-container> -- curl --max-time 5 http://<service>.<namespace>:<service-port>/health
kubectl exec <client-pod> -n <client-namespace> -c <client-container> -- curl --max-time 5 http://<pod-ip>:8080/health
```

What it does: compares the Service path with a direct endpoint request from the same source. Expected success is the application's documented health response. Preserve any required Host header or TLS server name; virtual hosting and authorization can make the two URLs behave differently.

| Observation | Narrow the investigation |
| --- | --- |
| No selected Pods | Selector, namespace, controller replica count. |
| Pods exist but endpoints are unavailable | Readiness, termination, readiness gates, and named-port resolution. |
| Endpoint IP refuses connection | Application listener, bind address, port, or crash. |
| Endpoint and Service both time out | Source egress, destination ingress, CNI routing, node health. |
| Endpoint works but Service IP fails | Service ports/protocol, traffic policies, kube-proxy or the CNI's Service implementation. |

A NetworkPolicy-enforcing implementation must allow both applicable source egress and destination ingress. Policies in Kubernetes have effect only when supported by the network implementation. Compare permitted and denied identities; do not remove all policies to diagnose one connection.[^network-policies]

## Recovery and verification

Correct the smallest evidenced problem in the owning configuration. Re-test from the original client and across the affected node boundary. A successful `kubectl port-forward` is useful for application inspection but does not validate normal Service routing or NetworkPolicy behavior. Remove any temporary diagnostic resources you created; these inspection commands create none.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Gateway route and TLS failures](gateway-route-and-tls.md) — inspect the external entry path.
- [Manifest regression lab](../applications-and-tools/manifest-validation/regression-lab-and-ci.md) — reproduce a wrong target port locally.
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^debug-service]: [Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
[^endpoint-slices]: [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
[^network-policies]: [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
