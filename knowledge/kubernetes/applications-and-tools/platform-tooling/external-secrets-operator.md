---
type: Explanation
title: External Secrets Operator
description: Synchronize an external secret into a Kubernetes Secret with explicit
  ownership and refresh behavior.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: eso-overview
  resource: https://external-secrets.io/latest/
  title: ESO overview
- id: externalsecret-api
  resource: https://external-secrets.io/latest/api/externalsecret/
  title: ExternalSecret API
- id: aws-provider
  resource: https://external-secrets.io/latest/provider/aws-secrets-manager/
  title: AWS provider
---

# External Secrets Operator

## Purpose

Synchronize an external secret into a Kubernetes Secret with explicit ownership and refresh behavior.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Components and flow

External Secrets Operator (ESO) reconciles `ExternalSecret` objects. A namespaced `SecretStore` or cluster-scoped `ClusterSecretStore` configures the provider and authentication. ESO reads the external value and writes the target Secret; the application consumes it normally.[^eso-overview][^externalsecret-api][^aws-provider]

Use this when workloads already expect Kubernetes Secrets. Values also reside in the Kubernetes API store. Choose CSI mounting or direct retrieval when that is prohibited.

## AWS example

Prerequisites: a pinned ESO installation serving `external-secrets.io/v1`; a ready `aws-secrets` SecretStore in `demo`; and a provider identity allowed to read only the required Secrets Manager ARN. Configure provider authentication using the installed version's documentation.

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: app-credentials
  namespace: demo
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: app-credentials
    creationPolicy: Owner
  data:
    - secretKey: password
      remoteRef:
        key: demo/database
        property: password
```

What it does: copies a property from an external JSON secret into a Kubernetes Secret. This is configuration for an existing provider installation.

```bash
kubectl get externalsecret app-credentials -n demo
kubectl describe externalsecret app-credentials -n demo
kubectl get secretstore aws-secrets -n demo
```

What it does: checks readiness and reconciliation. Expect `Ready=True`. Investigate IAM, KMS access, region, key/property names, and connectivity before changing refresh frequency.

## Rotation, failure, and cleanup

A refresh does not restart containers using environment variables. Existing values may remain during a store outage while new values cannot arrive. Alert on stale reconciliation. Test deletion policies: deleting an owning ExternalSecret can delete its target Secret.

> [!WARNING]
> Cluster-scoped stores require explicit tenant controls. Avoid wildcard provider permissions and do not print synchronized data during diagnosis.

## Related links

- [ESO overview](https://external-secrets.io/latest/)
- [ExternalSecret API](https://external-secrets.io/latest/api/externalsecret/)
- [AWS provider](https://external-secrets.io/latest/provider/aws-secrets-manager/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^eso-overview]: [ESO overview](https://external-secrets.io/latest/).
[^externalsecret-api]: [ExternalSecret API](https://external-secrets.io/latest/api/externalsecret/).
[^aws-provider]: [AWS provider](https://external-secrets.io/latest/provider/aws-secrets-manager/).
