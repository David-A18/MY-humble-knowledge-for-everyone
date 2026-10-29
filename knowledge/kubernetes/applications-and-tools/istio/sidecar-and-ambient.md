---
type: Explanation
title: Sidecar and ambient security enforcement
description: Locate the enforcing proxy before writing authentication and authorization
  policy.
tags:
- kubernetes
- istio
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: ambient-security
  resource: https://istio.io/latest/docs/ambient/usage/l4-policy/
  title: Ambient security
- id: waypoint-configuration
  resource: https://istio.io/latest/docs/ambient/usage/waypoint/
  title: Waypoint configuration
- id: peerauthentication-reference
  resource: https://istio.io/latest/docs/reference/config/security/peer_authentication/
  title: PeerAuthentication reference
---

# Sidecar and ambient security enforcement

## Purpose

Locate the enforcing proxy before writing authentication and authorization policy.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Two deployment models

In sidecar mode, an Envoy proxy runs alongside each participating workload. In ambient mode, node-level ztunnel provides secure L4 transport and workload identity; optional waypoint proxies provide L7 processing for enrolled traffic.[^ambient-security][^waypoint-configuration][^peerauthentication-reference]

| Requirement | Sidecar | Ambient |
| --- | --- | --- |
| Workload mTLS | Workload proxy | ztunnel with HBONE transport |
| L4 identity/port policy | Workload proxy | ztunnel policy |
| HTTP/JWT/other L7 policy | Workload proxy or gateway | Appropriate waypoint/gateway |
| Application Pod restart for initial enrollment | Injection generally needs recreated Pods | Enrollment has different lifecycle behavior |

Do not copy a sidecar selector-based JWT policy into an ambient namespace and assume ztunnel validates HTTP JWTs. Use the documented waypoint attachment model, such as supported `targetRefs`, for L7 policy. Verify Service and waypoint enrollment and the actual traffic path.

## Policy scope

Policies can be mesh-, namespace-, or workload-scoped depending on location and attachment. Version-skew matters when older control planes do not understand newer attachment fields. During mixed-revision upgrades, follow Istio's revision guidance before applying new policies.

Ambient transport is intrinsically mTLS between participating proxies; `PeerAuthentication` DISABLE is unsupported there. STRICT can help reject bypass traffic. Plaintext arriving through an unintended path still requires explicit testing.

## Migration checks

Inventory gateway traffic, Pod-IP access, Service traffic, external dependencies, health probes, and mixed-mode callers. Verify positive and negative tests for every path before expanding enrollment. Inspect ztunnel/waypoint status and policy acceptance rather than only application Pod readiness.

Choose sidecar mode for the supplied introductory lab so each workload's security boundary is visible. Treat ambient migration as a separate production change with its own rollback and telemetry.

## Related links

- [Ambient security](https://istio.io/latest/docs/ambient/usage/l4-policy/)
- [Waypoint configuration](https://istio.io/latest/docs/ambient/usage/waypoint/)
- [PeerAuthentication reference](https://istio.io/latest/docs/reference/config/security/peer_authentication/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^ambient-security]: [Ambient security](https://istio.io/latest/docs/ambient/usage/l4-policy/).
[^waypoint-configuration]: [Waypoint configuration](https://istio.io/latest/docs/ambient/usage/waypoint/).
[^peerauthentication-reference]: [PeerAuthentication reference](https://istio.io/latest/docs/reference/config/security/peer_authentication/).
