---
type: Explanation
title: cert-manager
description: Automate certificate issuance and renewal while understanding trust and
  private-key handling.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: certificate-resource
  resource: https://cert-manager.io/docs/usage/certificate/
  title: Certificate resource
- id: issuers
  resource: https://cert-manager.io/docs/concepts/issuer/
  title: Issuers
- id: acme-troubleshooting
  resource: https://cert-manager.io/docs/troubleshooting/acme/
  title: ACME troubleshooting
---

# cert-manager

## Purpose

Automate certificate issuance and renewal while understanding trust and private-key handling.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Components and lifecycle

A `Certificate` describes DNS names, issuer, and target Secret. cert-manager creates a `CertificateRequest`; an `Issuer` or `ClusterIssuer` fulfills it. ACME also uses Orders and Challenges. The certificate and key are written to a Secret and renewal is reconciled before expiry.[^certificate-resource][^issuers][^acme-troubleshooting]

An Issuer is namespaced; a ClusterIssuer is cluster-scoped. Issuance does not automatically distribute CA trust or prove that a gateway reloaded the Secret. Istio has its own workload-certificate lifecycle.

## Disposable self-signed lab

Prerequisites: an installed, pinned cert-manager release serving `cert-manager.io/v1`, its webhook ready, and an empty `cert-lab` namespace.

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: local-selfsigned
  namespace: cert-lab
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: demo
  namespace: cert-lab
spec:
  secretName: demo-tls
  dnsNames: [demo.test]
  issuerRef:
    name: local-selfsigned
    kind: Issuer
```

What it does: requests a lab certificate without external DNS or ACME. It is not publicly trusted or a production CA design.

```bash
kubectl wait certificate/demo -n cert-lab --for=condition=Ready --timeout=120s
kubectl get certificate,certificaterequest -n cert-lab
kubectl get secret demo-tls -n cert-lab -o jsonpath='{.type}{"\n"}'
```

What it does: checks issuance without dumping keys. Expect `Ready=True` and type `kubernetes.io/tls`.

## Production and troubleshooting

Use ACME staging before production. HTTP-01 requires a reachable challenge route; DNS-01 needs narrow DNS permissions and propagation. Private CAs require trust distribution and protected keys. Alert on expiry and renewal failures; test consumer reload.

For stalled issuance follow Certificate -> CertificateRequest -> Order -> Challenge and inspect conditions/events. A ready Certificate with browser errors requires checking DNS names, chain, trust, ingress routing, and the certificate actually served.

> [!WARNING]
> Clean up only the disposable `cert-lab` namespace. Keep shared ClusterIssuers, CA Secrets, and CRDs intact.

## Related links

- [Certificate resource](https://cert-manager.io/docs/usage/certificate/)
- [Issuers](https://cert-manager.io/docs/concepts/issuer/)
- [ACME troubleshooting](https://cert-manager.io/docs/troubleshooting/acme/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^certificate-resource]: [Certificate resource](https://cert-manager.io/docs/usage/certificate/).
[^issuers]: [Issuers](https://cert-manager.io/docs/concepts/issuer/).
[^acme-troubleshooting]: [ACME troubleshooting](https://cert-manager.io/docs/troubleshooting/acme/).
