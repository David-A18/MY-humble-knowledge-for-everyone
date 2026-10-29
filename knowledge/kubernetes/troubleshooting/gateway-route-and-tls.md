---
type: Troubleshooting Guide
title: Gateway route and TLS failures
description: Trace an external request through Gateway API acceptance, backend references,
  listener TLS, and application routing.
tags:
- kubernetes
- troubleshooting
- gateway-api
- tls
- ingress
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: gateway-status
  title: Gateway API troubleshooting and status
  resource: https://gateway-api.sigs.k8s.io/docs/concepts/troubleshooting/
- id: gateway-api
  title: Gateway API reference
  resource: https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/
---

# Gateway route and TLS failures

Use this guide when an external request fails but the backend may be healthy. The path is DNS → external address → listener/TLS → route match → Service → endpoint. First use [Service connectivity](service-connectivity.md) to establish whether the backend path works.

## Check reconciliation status first

This sequence assumes Gateway API CRDs and a compatible controller are installed. For legacy Ingress, inspect the IngressClass, Ingress events, and that controller's version-specific diagnostics instead. Missing resource types indicate an API/installation mismatch, not necessarily a dead controller.

```bash
kubectl get gatewayclass
kubectl get gateway <gateway> -n <gateway-namespace> -o yaml
kubectl get httproute <route> -n <route-namespace> -o yaml
```

What it does: identifies the owning controller, listener/address configuration, and Route parent status. Compare each condition's `observedGeneration` with that resource's `metadata.generation` before trusting it. A Route's status is per parent; inspect the parent actually serving this request.[^gateway-status]

| Condition / observation | Investigation |
| --- | --- |
| No status | Is the object in the controller's scope, and does its parent reference exist? |
| `Accepted=False` | Reason/message, listener protocol, hostname intersection, route kinds, and attachment permissions. |
| `ResolvedRefs=False` | Missing backend or Secret, wrong port/kind, or prohibited cross-namespace reference. |
| Gateway/listener not `Programmed` | Controller reconciliation and data-plane configuration delivery. |
| Conditions current and positive; request still fails | Actual address reachability, SNI/Host/path, certificate validation, and backend behavior. |

`Programmed=True` describes configuration progress; it is not an end-to-end health test. Cross-namespace Route attachment is governed by the listener's `allowedRoutes`; cross-namespace object references such as a backend or certificate can require a `ReferenceGrant` in the target namespace. These are separate permission checks.[^gateway-api]

## Test the intended hostname and certificate

Run the following from an authorized client with `curl`. Replace the example hostname and IP with your own. Use a read-only health path.

```bash
curl --connect-timeout 5 --max-time 10 --resolve app.example.com:443:192.0.2.10 https://app.example.com/health
```

What it does: sends the request to a chosen address while preserving the URL hostname for TLS SNI, certificate verification, and HTTP Host. Expect the correct certificate chain and application response. A certificate failure happens before HTTP routing; a 404/503 can originate from the gateway or application, so correlate with logs. Do not use `-k` as proof that TLS is healthy.

If the forced-address test succeeds but the normal URL fails, compare DNS answers and reachable addresses. If TLS fails, inspect listener protocol, `certificateRefs`, Secret namespace/type, certificate names, chain, and validity dates using approved tooling without printing the private key. For cert-manager-managed certificates, inspect Certificate/CertificateRequest/issuer conditions rather than replacing a Secret manually.

## Recovery and verification

Correct one route, reference, listener, or certificate problem through its owner. Recheck fresh conditions, a permitted path, a deliberately unmatched path, and the normal DNS URL from the actual client network. Keep necessary authentication in place. These inspection commands create no resources; remove any temporary test routes or diagnostic clients you independently added.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Gateway API and Ingress](../applications-and-tools/gateway-api-and-ingress.md).
- [APISIX-specific diagnostics](apisix.md).
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^gateway-status]: [Gateway API troubleshooting and status](https://gateway-api.sigs.k8s.io/docs/concepts/troubleshooting/)
[^gateway-api]: [Gateway API reference](https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/)
