---
type: Troubleshooting Guide
title: APISIX troubleshooting
description: Locate APISIX failures between Kubernetes reconciliation, gateway configuration,
  request matching, and backend delivery.
tags:
- kubernetes
- troubleshooting
- apisix
- gateway
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: apisix-config
  title: APISIX configuration troubleshooting
  resource: https://apisix.apache.org/docs/ingress-controller/reference/apisix-ingress-controller/configuration-troubleshoot/
- id: apisix-ready
  title: APISIX Status API
  resource: https://apisix.apache.org/docs/apisix/status-api/
---

# APISIX troubleshooting

Use this guide after identifying Apache APISIX as the gateway serving a failing request. Establish the controller release and deployment mode before applying version-specific advice: APISIX Ingress Controller, APISIX gateway, and their configuration provider are separate components. Do not assume every installation uses etcd or the same administrative API.

## Identify the failing layer

You need read/log permissions in the gateway and application namespaces. Replace names from your installation; the examples deliberately do not assume chart-generated Deployment names.

```bash
kubectl get deployments,pods,services -n <apisix-namespace> -o wide
kubectl get deployment <controller> -n <apisix-namespace> -o jsonpath='{.spec.template.spec.containers[*].image}{"\n"}'
kubectl logs deployment/<controller> -n <apisix-namespace> -c <controller-container> --since=10m --tail=100
kubectl logs <gateway-pod> -n <apisix-namespace> -c <gateway-container> --since=10m --tail=100
```

What it does: captures topology, controller image version, reconciliation errors, and gateway request/upstream errors near the failure time. Avoid publishing complete logs or configuration dumps; plugin configuration and administrative credentials may be sensitive.

| Observation | Next evidence |
| --- | --- |
| Route missing / stale | Actual routing API in use, controller ownership, resource events/status, and reconciliation logs. |
| 404 from gateway | Host/path/method/listener matching and whether the configuration reached the data plane. |
| 502/503 / timeout | [Service endpoints and ports](service-connectivity.md), upstream health, policies, and gateway logs. |
| Plugin behavior missing | Attachment scope, route identity, supported plugin/configuration, and translated configuration. |
| TLS handshake failure | [Gateway/listener/certificate diagnostics](gateway-route-and-tls.md) before HTTP routing. |

For Gateway API resources, inspect current per-parent status first. For APISIX custom resources, use the CRD schema installed with your release. A command failing because a CRD is absent does not prove APISIX itself is unhealthy.

## Compare intended and delivered configuration

The current controller documentation describes translation into ADC configuration and a debug interface for inspecting it. Use that procedure only if supported by your controller release, through a private, access-controlled administrative path. Compare one affected route/backend rather than exporting all configuration.[^apisix-config]

If listener-port matching is explicitly enabled, compare the Gateway listener port with the gateway's actual accepted port after Service translation. A Service mapping 443 to 9443 can matter to that feature. Do not copy newer release flags into an older controller without confirming its configuration schema.[^apisix-config]

APISIX's Status API distinguishes a responding worker from all workers having loaded configuration. In releases supporting it, `/status/ready` checks the latter; a generic `/status` success alone does not establish that every worker is ready.[^apisix-ready] Reach administrative endpoints only through the installation's approved private diagnostics path.

## Recover and verify

Fix the evidenced owner/resource mismatch, backend, or plugin setting in the source of truth. Preserve the failing version and request correlation data. Do not delete etcd, expose the Admin API publicly, or disable authentication to make a route respond.

Re-test the original hostname/path, an unmatched path, and required authentication outcomes. Verify the intended backend receives the request and fresh controller errors stop. End any temporary administrative forwarding session and remove temporary diagnostics; retain private evidence for the incident record.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [APISIX architecture](../applications-and-tools/apisix-architecture-and-deployment.md).
- [APISIX security and observability](../applications-and-tools/apisix-security-traffic-and-observability.md).
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^apisix-config]: [APISIX configuration troubleshooting](https://apisix.apache.org/docs/ingress-controller/reference/apisix-ingress-controller/configuration-troubleshoot/)
[^apisix-ready]: [APISIX Status API](https://apisix.apache.org/docs/apisix/status-api/)
