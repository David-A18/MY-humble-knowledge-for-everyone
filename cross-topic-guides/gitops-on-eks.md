# GitOps on EKS

## Purpose

Use this guide to operate EKS workloads with GitOps controllers such as Argo CD or Flux.

## Operating model

1. Application or platform state is committed to Git.
2. Argo CD or Flux detects the change.
3. The controller reconciles manifests, Helm releases, or Kustomize overlays.
4. Kubernetes rolls out the workloads.
5. Operators monitor sync, drift, rollout status, and application health.

## EKS-specific checklist

- Keep cluster access for GitOps controllers least-privileged.
- Decide whether controllers run in each workload cluster or in a tooling cluster.
- Use IRSA or EKS Pod Identity for AWS API access when the controller needs it.
- Store secrets through a secure secret-management workflow.
- Avoid manual changes to GitOps-owned resources.

## Navigation path

1. Start with [GitOps](../kubernetes/applications-and-tools/gitops.md) for the operating model.
2. Read [Argo CD vs. Flux](../kubernetes/applications-and-tools/argo-cd-vs-flux.md) if you are choosing a controller.
3. Use [Flux](../kubernetes/applications-and-tools/flux.md) and [Flux reconciliation and Helm releases](../kubernetes/applications-and-tools/flux-reconciliation-and-helm.md) for Flux-specific controller, source, Kustomization, and HelmRelease behavior.
4. Use [GitOps security and multi-tenancy](../kubernetes/applications-and-tools/gitops-security-and-multitenancy.md) for RBAC, secrets, controller scope, and team ownership.

## Related links

- [GitOps](../kubernetes/applications-and-tools/gitops.md)
- [Argo CD vs. Flux](../kubernetes/applications-and-tools/argo-cd-vs-flux.md)
- [Flux](../kubernetes/applications-and-tools/flux.md)
- [Flux reconciliation and Helm releases](../kubernetes/applications-and-tools/flux-reconciliation-and-helm.md)
- [GitOps security and multi-tenancy](../kubernetes/applications-and-tools/gitops-security-and-multitenancy.md)
- [EKS workload identity](eks-workload-identity.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
