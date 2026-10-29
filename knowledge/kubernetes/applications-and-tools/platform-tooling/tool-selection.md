---
type: Reference
title: Choose Kubernetes platform tools
description: Build a small, supportable platform around operational requirements.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: cncf-landscape
  resource: https://landscape.cncf.io/
  title: CNCF landscape
- id: kubernetes-controllers
  resource: https://kubernetes.io/docs/concepts/architecture/controller/
  title: Kubernetes controllers
---

# Choose Kubernetes platform tools

## Purpose

Build a small, supportable platform around operational requirements.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Start with the operating contract

For each component, name its owner, API permissions, data access, upgrade method, failure behavior, and recovery path. Separate cluster-wide infrastructure owned by platform engineers from namespace configuration owned by application teams.[^cncf-landscape][^kubernetes-controllers]

| Need | Common choices | Main decision |
| --- | --- | --- |
| Packaging and overlays | Helm, Kustomize | Parameterized packages or patches over ordinary YAML. |
| Continuous deployment | Argo CD, Flux | Application UI or composable reconciliation controllers. |
| Secrets and certificates | ESO, CSI Driver, Vault, cert-manager | Where values live and how workloads receive changes. |
| Metrics and dashboards | Prometheus, Grafana, Metrics Server | Monitoring versus resource metrics for autoscaling. |
| Logs and traces | Fluent Bit, Vector, OpenTelemetry; Loki, Tempo, Jaeger | Collectors versus storage/query backends. |
| Networking | Cilium/Hubble, gateways, Istio | Connectivity, flow visibility, API routing, or mesh identity. |
| Policy and security | Kyverno, Gatekeeper, Trivy, Falco | Admission, vulnerability discovery, or runtime detection. |
| Scaling | HPA, KEDA, Karpenter | Scale replicas from metrics/events or supply nodes. |
| Operations and recovery | K9s, Velero, CSI snapshots | Inspection, resource backup, and volume recovery. |

## Selection sequence

1. Describe a requirement: for example, credentials cannot be stored in Git.
2. Check native Kubernetes capabilities before adding an operator.
3. Compare permissions, availability, portability, cost, and team experience.
4. Install one pinned release in a disposable cluster; record resource usage and failure behavior.
5. Prove upgrade, rollback, alerting, and ownership before production adoption.

## Inspect the installed platform

```bash
kubectl get deployments,daemonsets -A
kubectl get crds
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations
kubectl get apiservices
```

What it does: inventories controllers, extension APIs, admission hooks, and aggregated API services. Expect CRDs only for tools that expose custom resources; Helm and Kustomize do not require their own controllers.

## Common mistakes

Two controllers reconciling the same fields can continuously undo each other's changes. A failed admission webhook can block deployments when its failure policy is fail-closed. Monitoring a controller Pod alone misses stalled reconciliation; also monitor queue failures, object conditions, and stale outputs.

## Related links

- [CNCF landscape](https://landscape.cncf.io/)
- [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/)
- [Argo CD vs Flux](../argo-cd-vs-flux.md)
- [K9s](../k9s.md)
- [Velero](../../../migrations/velero/index.md)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^cncf-landscape]: [CNCF landscape](https://landscape.cncf.io/).
[^kubernetes-controllers]: [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/).
