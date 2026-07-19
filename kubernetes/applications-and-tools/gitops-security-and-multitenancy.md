# GitOps security and multi-tenancy

## Purpose

Use this guide to keep GitOps controllers powerful enough to reconcile clusters without giving every team uncontrolled cluster-wide deployment authority.

## How GitOps changes security

GitOps turns repository write access into a path toward runtime change. The controller becomes the actor that applies those changes, so both Git permissions and Kubernetes permissions matter.

```text
developer pull request
  -> review and branch policy
  -> merge to protected branch
  -> GitOps controller detects desired state
  -> Kubernetes API applies changes using controller permissions
```

If the controller can create cluster-admin bindings, then a Git change may become a cluster-admin change.

## Threat model

| Asset | Risk | Control |
| --- | --- | --- |
| Git repository | Unauthorized manifest change. | Branch protection, reviews, signed commits where required. |
| Controller credentials | Cluster takeover if stolen. | Scope credentials and protect Secrets. |
| Target namespace | Team deploys outside its boundary. | RBAC, admission policy, and project scoping. |
| CRDs and cluster-scoped resources | Platform-wide impact. | Separate platform and tenant reconciliation units. |
| Secrets | Plaintext exposure in Git or logs. | SOPS, external secret operators, and least privilege. |
| Images and charts | Supply-chain compromise. | Pin versions, scan, verify signatures where required. |

## Ownership boundaries

| Boundary | Use when | Notes |
| --- | --- | --- |
| Namespace ownership | Teams own apps in separate namespaces. | Start here for most platform teams. |
| Cluster ownership | Different controllers manage different clusters. | Clear failure and permission boundary. |
| Workload-category ownership | Platform owns add-ons, teams own apps. | Requires clear path and resource conventions. |
| Migration ownership | Argo CD and Flux temporarily coexist. | Only one controller owns a resource at a time. |

> [!WARNING]
> Do not let Argo CD and Flux reconcile the same Kubernetes object. They can continuously overwrite each other and turn a simple deployment into a confusing control loop.

## Argo CD controls

Argo CD Projects can restrict trusted source repositories, target clusters, namespaces, resource kinds, and project roles. Use Projects as a first-class tenancy boundary rather than putting every application into the default project.

### Argo CD project boundary example

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: payments
  namespace: argocd
spec:
  sourceRepos:
    - https://github.com/example/payments-platform.git
  destinations:
    - namespace: payments
      server: https://kubernetes.default.svc
  clusterResourceWhitelist: []
```

What it does: limits applications in the project to one source repository and one namespace destination.

## Flux controls

Flux multi-tenancy usually combines:

- namespace-scoped Kustomizations,
- scoped service accounts,
- Kubernetes RBAC,
- source repository boundaries,
- `dependsOn` for platform ordering,
- admission controls for disallowed resources.

### Flux scoped reconciliation example

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: payments-apps
  namespace: flux-system
spec:
  serviceAccountName: payments-reconciler
  targetNamespace: payments
  path: ./teams/payments
```

What it does: asks Flux to reconcile a team's path using a scoped service account instead of the controller's default authority.

## Secret handling

| Pattern | Use when | Risk |
| --- | --- | --- |
| SOPS-encrypted Secret manifests | Git remains the delivery path. | Key management becomes critical. |
| External Secrets Operator | Secrets live in a dedicated secret manager. | Controller permissions must be scoped. |
| Plain Kubernetes Secret in Git | Local labs only. | Base64 is not encryption. |

## Review checklist

- Are cluster-scoped resources owned by the platform team?
- Can a tenant deploy to another tenant's namespace?
- Can a tenant create RBAC that grants broader permissions?
- Are Git credentials read-only where possible?
- Is manual production drift detected and reconciled intentionally?
- Are controller alerts routed to the owning team?
- Is there a documented break-glass procedure?

## Incident response checks

When an unexpected object appears in a cluster:

1. Identify whether it is managed by Argo CD, Flux, Helm, or manual apply.
2. Find the source repository, path, chart, or Kustomization that owns it.
3. Check commit history and pull request approvals.
4. Check the controller service account that applied it.
5. Revert in Git or suspend the owning reconciliation object.
6. Preserve controller logs for audit.

## Related links

- Official documentation: [Argo CD Projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/)
- Official documentation: [Argo CD repository security notes](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/)
- Official documentation: [Flux security documentation](https://fluxcd.io/flux/security/)
- [GitOps](gitops.md)
- [Argo CD vs. Flux](argo-cd-vs-flux.md)
- [Flux reconciliation and Helm releases](flux-reconciliation-and-helm.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
