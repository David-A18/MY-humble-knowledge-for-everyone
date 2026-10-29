---
type: Explanation
title: Istio workload identity and mutual TLS
description: Follow how a Kubernetes service account becomes a mesh identity.
tags:
- kubernetes
- istio
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: peerauthentication
  resource: https://istio.io/latest/docs/reference/config/security/peer_authentication/
  title: PeerAuthentication
- id: identity-and-certificates
  resource: https://istio.io/latest/docs/concepts/security/#identity-and-certificate-management
  title: Identity and certificates
---

# Istio workload identity and mutual TLS

## Purpose

Follow how a Kubernetes service account becomes a mesh identity.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Certificate flow

A workload uses its Kubernetes service-account identity to authenticate to Istio's certificate authority integration. The agent obtains and rotates short-lived certificates, and proxies use them for mutual TLS. A typical SPIFFE-style identity is `spiffe://cluster.local/ns/demo/sa/api`; the trust domain is configurable.[^peerauthentication][^identity-and-certificates]

Both peers prove identity during mTLS. Authorization can match the authenticated source principal. Pods using the same service account share that identity boundary; namespace or Pod names alone are not distinct credentials.

## Require mTLS

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: demo
spec:
  mtls:
    mode: STRICT
```

What it does: requires inbound mesh mTLS for covered workloads in `demo`. Unenrolled plaintext clients can fail even if an application port still looks healthy.

`PERMISSIVE` allows both plaintext and mTLS in sidecar migration scenarios. `STRICT` requires mTLS. Auto mTLS helps clients select transport, but does not independently authorize business operations. Workload port overrides refer to workload ports rather than Service ports.

## Inspect before enforcement

```bash
istioctl proxy-status
istioctl proxy-config secret deploy/web -n demo
kubectl get serviceaccount,pod -n demo
```

What it does: checks configuration synchronization, delivered certificate metadata, and workload identities. Keep private-key material out of diagnostic bundles.

## Trust and failure handling

Certificate expiry, clock skew, incorrect trust bundles, missed injection, and blocked control-plane connectivity can cause handshake failures. Check both ends of the path. Trust-domain changes and multi-cluster trust require migration planning; they are not merely string replacements in policies.

Roll out encryption after inventorying non-mesh clients, probes, gateways, and external access. Test actual requests, then verify telemetry shows authenticated traffic. Retain a namespace-scoped rollback plan.

## Related links

- [PeerAuthentication](https://istio.io/latest/docs/reference/config/security/peer_authentication/)
- [Identity and certificates](https://istio.io/latest/docs/concepts/security/#identity-and-certificate-management)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^peerauthentication]: [PeerAuthentication](https://istio.io/latest/docs/reference/config/security/peer_authentication/).
[^identity-and-certificates]: [Identity and certificates](https://istio.io/latest/docs/concepts/security/#identity-and-certificate-management).
