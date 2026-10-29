---
type: Explanation
title: Helm and Kustomize
description: Choose and inspect how Kubernetes configuration becomes deployable manifests.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: helm-template
  resource: https://helm.sh/docs/helm/helm_template/
  title: Helm template
- id: kustomize
  resource: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
  title: Kustomize
---

# Helm and Kustomize

## Purpose

Choose and inspect how Kubernetes configuration becomes deployable manifests.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## How they work

Helm renders chart templates with values and manages releases when used through its CLI. Kustomize transforms Kubernetes resources using overlays, patches, generators, and image changes. Argo CD and Flux can consume these formats and continuously reconcile a cluster.[^helm-template][^kustomize]

| Situation | Prefer | Reason |
| --- | --- | --- |
| Install a vendor-supported controller | Its Helm chart | The vendor maintains component wiring and defaults. |
| Small application with environment differences | Kustomize | Ordinary YAML plus explicit patches. |
| Reusable configurable package | Helm | Values expose an installation interface. |
| GitOps deployment | Either, through the chosen reconciler | Keep a single owner for applied fields. |

## Review before applying

```bash
helm template demo ./chart --values values-dev.yaml > rendered.yaml
kubectl kustomize overlays/dev > overlay-rendered.yaml
kubectl diff -f rendered.yaml
```

What it does: renders locally and compares prospective configuration with the cluster. `helm template` does not reproduce every upgrade-time API interaction. `kubectl diff` requires cluster access and returns 1 when differences exist.

Pin chart versions and image digests. Commit non-secret values, dependency locks, and overlays. Render each supported environment in CI; test changed selectors, ports, probes, and security contexts.

## Troubleshooting

| Symptom | Check | Next step |
| --- | --- | --- |
| Wrong environment | Values order and overlay target | Render the exact CI inputs. |
| Unintended replacement | Immutable fields and names | Plan migration before applying. |
| Secret appears in output | Values and templates | Redact artifacts and change secret delivery. |

> [!WARNING]
> Rendered manifests may contain plaintext credentials. Keep them out of public logs and Git. Do not uninstall shared CRDs as application cleanup.

## Related links

- [Helm template](https://helm.sh/docs/helm/helm_template/)
- [Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [Manifest validation](../manifest-validation/index.md)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^helm-template]: [Helm template](https://helm.sh/docs/helm/helm_template/).
[^kustomize]: [Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/).
