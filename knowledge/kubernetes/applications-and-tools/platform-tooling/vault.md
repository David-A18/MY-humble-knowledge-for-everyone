---
type: Explanation
title: Vault on Kubernetes
description: Understand authentication, policies, leases, and the responsibility of
  operating a secrets platform.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: kubernetes-auth
  resource: https://developer.hashicorp.com/vault/docs/auth/kubernetes
  title: Kubernetes auth
- id: kubernetes-integrations
  resource: https://developer.hashicorp.com/vault/docs/platform/k8s
  title: Kubernetes integrations
- id: vault-policies
  resource: https://developer.hashicorp.com/vault/docs/concepts/policies
  title: Vault policies
---

# Vault on Kubernetes

## Purpose

Understand authentication, policies, leases, and the responsibility of operating a secrets platform.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## What Vault does

Vault authenticates clients, evaluates policies, and serves values through secrets engines. KV stores versioned values; dynamic engines can issue database or cloud credentials with leases. PKI and encryption-as-a-service are additional capabilities.[^kubernetes-auth][^kubernetes-integrations][^vault-policies]

| Component | Responsibility |
| --- | --- |
| Auth method | Maps a Kubernetes identity, JWT, or other login to a Vault token. |
| Role and policy | Limits identities, paths, and operations. |
| Secrets engine | Stores or generates values. |
| Agent / CSI / operator | Delivers values and may manage renewal. |
| Application | Consumes changes and handles credential expiry. |

## Kubernetes authentication

A workload presents a service-account token to Vault's Kubernetes auth method. Vault validates identity using its configured Kubernetes integration and selects a role bound to service accounts and namespaces. Token audience, issuer, TokenReview access, and expiry must match the configuration.

## Least-privilege example

```hcl
path "kv/data/demo/database" {
  capabilities = ["read"]
}
```

What it does: permits reading one KV v2 data path, without listing or modifying other applications' values. KV v1 uses a different path layout.

## Operations and recovery

Choose managed or self-hosted operation, persistent storage, HA, unseal/recovery, audit sinks, and ownership. Test storage snapshots and recovery. Development mode is disposable and unsuitable for production.

Dynamic credentials reduce long-lived exposure, but renewal failure can break running applications. Alert before lease expiry and test connection-pool recycling. Never place a root token in a Pod or GitOps manifest.

## Troubleshooting

Failed login suggests identity configuration. A successful login followed by permission denied suggests policy or path selection. Check TTL, renewal permissions, and clock synchronization for expiry issues. Inspect audit metadata without recording plaintext secret values.

## Related links

- [Kubernetes auth](https://developer.hashicorp.com/vault/docs/auth/kubernetes)
- [Kubernetes integrations](https://developer.hashicorp.com/vault/docs/platform/k8s)
- [Vault policies](https://developer.hashicorp.com/vault/docs/concepts/policies)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^kubernetes-auth]: [Kubernetes auth](https://developer.hashicorp.com/vault/docs/auth/kubernetes).
[^kubernetes-integrations]: [Kubernetes integrations](https://developer.hashicorp.com/vault/docs/platform/k8s).
[^vault-policies]: [Vault policies](https://developer.hashicorp.com/vault/docs/concepts/policies).
