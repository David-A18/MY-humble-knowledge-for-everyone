# GitOps

## Purpose

Use this page to understand GitOps as an operating model for Kubernetes delivery.

## Mental model

Git stores desired state. A controller continuously compares desired state with cluster state and reconciles drift.

| Concept | Meaning |
| --- | --- |
| Desired state | Manifests, Helm releases, or Kustomize overlays in Git. |
| Reconciliation | Controller loop that applies the desired state. |
| Drift | Difference between Git and the live cluster. |
| Pruning | Removing live resources that are no longer desired. |
| Self-healing | Reverting manual cluster changes back to Git. |

## Operating rules

- Treat Git as the source of truth for GitOps-managed resources.
- Keep secrets and environment overlays deliberate.
- Avoid manual cluster edits unless the runbook explains how to reconcile them back to Git.
- Monitor controller health, sync status, and failed reconciliations.

## Related links

- [Argo CD vs. Flux](argo-cd-vs-flux.md)
- [Flux](flux.md)
- [GitOps on EKS](../../cross-topic-guides/gitops-on-eks.md)
- [Argo CD documentation](https://argo-cd.readthedocs.io/)
- [Flux documentation](https://fluxcd.io/flux/)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
