# Flux reconciliation and Helm releases

## Purpose

Use this guide to understand Flux as a source-to-artifact-to-reconciler pipeline and to decide when to use `Kustomization` or `HelmRelease`.

## Flux pipeline model

```text
GitRepository or HelmRepository
  -> source-controller artifact
  -> kustomize-controller or helm-controller
  -> Kubernetes API
  -> workload rollout
```

Flux separates source acquisition from workload reconciliation. That makes dependencies, intervals, retries, and ownership visible in Kubernetes resources.

## Main controllers

| Controller | Primary resources | Role |
| --- | --- | --- |
| source-controller | `GitRepository`, `HelmRepository`, `Bucket`, `OCIRepository`. | Fetches and packages source artifacts. |
| kustomize-controller | `Kustomization`. | Applies manifests and Kustomize overlays. |
| helm-controller | `HelmRelease`. | Installs and reconciles Helm releases. |
| notification-controller | `Provider`, `Alert`, `Receiver`. | Sends alerts and receives webhooks. |
| image automation controllers | `ImageRepository`, `ImagePolicy`, `ImageUpdateAutomation`. | Detects image tags and commits updates. |

## Reconciliation flow

1. A commit changes the desired state.
2. `source-controller` detects the new revision or receives a webhook.
3. Flux creates a source artifact.
4. `kustomize-controller` or `helm-controller` reconciles dependent resources.
5. Kubernetes performs the rollout.
6. Flux reports readiness and health conditions.
7. If live state drifts, Flux reconciles it back when pruning and correction are enabled.

### Force reconciliation

```bash
flux reconcile source git platform-config
flux reconcile kustomization apps-prod --with-source
```

What it does: asks Flux to fetch source and reconcile the dependent Kustomization immediately instead of waiting for the interval.

## Kustomization or HelmRelease

| Need | Prefer | Reason |
| --- | --- | --- |
| Plain YAML or Kustomize overlays | `Kustomization` | Direct manifest reconciliation. |
| Third-party chart installation | `HelmRelease` | Declarative Helm lifecycle and remediation. |
| App manifests plus patches | `Kustomization` | Clear Git-owned Kubernetes objects. |
| Chart with values from Secrets or ConfigMaps | `HelmRelease` | Helm-native values management. |
| Ordered infrastructure then apps | Either with `dependsOn` | Make dependencies explicit. |

## Helm release guardrails

- Pin chart versions intentionally.
- Keep production values in Git or approved secret tooling.
- Use remediation settings for failed installs and upgrades.
- Monitor HelmRelease conditions, not only Pod status.
- Avoid manual `helm upgrade` against Flux-owned releases.

## Troubleshooting

| Symptom | First check | Likely cause |
| --- | --- | --- |
| Source not updating | `GitRepository` conditions. | Auth, branch, tag, network, or webhook issue. |
| Kustomization stuck | `flux describe kustomization`. | Invalid YAML, dry-run failure, missing dependency. |
| HelmRelease fails | HelmRelease conditions and controller logs. | Chart render error, values error, hook failure. |
| Drift keeps reverting | Ownership labels and Flux scope. | Manual change to Flux-owned resource. |
| App waits forever | Health checks and dependencies. | `dependsOn` or readiness condition cannot pass. |

## Related links

- Official documentation: [Flux source-controller](https://fluxcd.io/flux/components/source/)
- Official documentation: [Flux kustomize-controller](https://fluxcd.io/flux/components/kustomize/)
- Official documentation: [Flux Helm releases](https://fluxcd.io/flux/guides/helmreleases/)
- [Flux](flux.md)
- [GitOps](gitops.md)
- [GitOps on EKS](../../cross-topic-guides/gitops-on-eks.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
