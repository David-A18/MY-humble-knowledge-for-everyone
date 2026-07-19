# GitOps

## Purpose

Use this page to understand GitOps as an operating model for Kubernetes delivery.

## What it does

GitOps makes Git the desired-state record for Kubernetes resources and uses a controller to reconcile the live cluster toward that state.

Traditional CI/CD often pushes changes directly into a cluster. GitOps usually lets CI build and publish artifacts, then a controller pulls desired state from Git and applies it.

## Mental model

Git stores desired state. A controller continuously compares desired state with cluster state and reconciles drift.

| Concept | Meaning |
| --- | --- |
| Desired state | Manifests, Helm releases, or Kustomize overlays in Git. |
| Reconciliation | Controller loop that applies the desired state. |
| Drift | Difference between Git and the live cluster. |
| Pruning | Removing live resources that are no longer desired. |
| Self-healing | Reverting manual cluster changes back to Git. |

## How it works

```text
developer change
  -> pull request
  -> merge to protected branch
  -> GitOps controller notices revision
  -> manifests or Helm release are applied
  -> controller reports health and drift
```

Git becomes the audit trail for intended runtime changes. The controller becomes the runtime actor, so its permissions and alerts matter.

## Main components

| Component | Role |
| --- | --- |
| Source repository | Stores desired state. |
| Environment path or overlay | Separates dev, staging, and production intent. |
| Controller | Watches source and reconciles the cluster. |
| Health checks | Tell whether resources became ready. |
| Pruning | Removes resources no longer defined in Git. |
| Notification path | Alerts owners when reconciliation fails. |

## Operating rules

- Treat Git as the source of truth for GitOps-managed resources.
- Keep secrets and environment overlays deliberate.
- Avoid manual cluster edits unless the runbook explains how to reconcile them back to Git.
- Monitor controller health, sync status, and failed reconciliations.

## Example repository shape

```text
clusters/
  prod/
    infrastructure/
    apps/
  staging/
    infrastructure/
    apps/
```

What it does: separates environment-specific desired state while keeping infrastructure and applications independently reconcilable.

## Related links

- [Argo CD vs. Flux](argo-cd-vs-flux.md)
- [Flux](flux.md)
- [Flux reconciliation and Helm releases](flux-reconciliation-and-helm.md)
- [GitOps security and multi-tenancy](gitops-security-and-multitenancy.md)
- [GitOps on EKS](../../cross-topic-guides/gitops-on-eks.md)
- [Argo CD documentation](https://argo-cd.readthedocs.io/)
- [Flux documentation](https://fluxcd.io/flux/)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
