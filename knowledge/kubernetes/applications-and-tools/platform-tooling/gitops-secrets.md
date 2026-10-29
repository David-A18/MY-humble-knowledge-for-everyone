---
type: Explanation
title: SOPS and Sealed Secrets
description: Keep encrypted values in Git while retaining a recoverable decryption
  boundary.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: sops
  resource: https://getsops.io/docs/
  title: SOPS
- id: sealed-secrets
  resource: https://github.com/bitnami-labs/sealed-secrets
  title: Sealed Secrets
- id: flux-sops
  resource: https://fluxcd.io/flux/guides/mozilla-sops/
  title: Flux SOPS
---

# SOPS and Sealed Secrets

## Purpose

Keep encrypted values in Git while retaining a recoverable decryption boundary.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Different trust models

SOPS encrypts selected values in supported file formats. Authorized tooling decrypts with KMS, age, or another configured key mechanism. Sealed Secrets encrypts a Kubernetes Secret for a controller that recreates it inside a cluster.[^sops][^sealed-secrets][^flux-sops]

| Question | SOPS | Sealed Secrets |
| --- | --- | --- |
| Who decrypts? | Authorized human, CI, or GitOps integration | Target cluster controller |
| Access boundary | Keys, IAM, and decryptor permissions | Sealing scope and controller private key |
| Recovery | Keys or KMS access | Controller key backup |
| Common fit | Flux SOPS integration | Applying SealedSecret resources |

## SOPS workflow

```bash
sops --encrypt --age "$AGE_RECIPIENT" secret.plain.yaml > secret.enc.yaml
sops --decrypt secret.enc.yaml | kubectl apply -f -
```

What it does: encrypts an existing synthetic sample and decrypts directly to kubectl. Set `AGE_RECIPIENT` to a public recipient; retain its private key securely. Configure `.sops.yaml` creation rules for repeatability.

## Sealing workflow

```bash
kubeseal --format yaml < secret.plain.json > secret.sealed.yaml
kubectl apply -f secret.sealed.yaml
```

What it does: uses the controller's public key to seal an existing sample Secret. Default strict scope binds it to its name and namespace; moving it requires resealing.

## Key lifecycle

Historical ciphertext plus an old key can reveal historical credentials. Rotate exposed credentials independently of encryption keys. Sealed Secrets key renewal does not rotate upstream passwords. Test key recovery and cross-cluster migration in a disposable environment.

> [!WARNING]
> Keep plaintext inputs out of Git, avoid shell tracing and CI artifact uploads, and protect decryption roles. Deleting the only usable key makes encrypted content unrecoverable.

## Related links

- [SOPS](https://getsops.io/docs/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- [Flux SOPS](https://fluxcd.io/flux/guides/mozilla-sops/)
- [GitOps security](../gitops-security-and-multitenancy.md)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^sops]: [SOPS](https://getsops.io/docs/).
[^sealed-secrets]: [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets).
[^flux-sops]: [Flux SOPS](https://fluxcd.io/flux/guides/mozilla-sops/).
