# Flux

## Purpose

Use this page to understand Flux as a GitOps toolkit for Kubernetes.

## Flux building blocks

| Controller | Responsibility |
| --- | --- |
| source-controller | Fetches Git, Helm, bucket, or OCI sources and turns them into artifacts. |
| kustomize-controller | Applies Kustomize-based desired state. |
| helm-controller | Reconciles Helm releases. |
| notification-controller | Sends reconciliation events and receives webhooks. |
| image automation controllers | Detect and write image updates back to Git. |

## Repository design habits

- Separate infrastructure, platform, and application concerns.
- Keep environment overlays explicit.
- Use dependency ordering when one reconciled object depends on another.
- Protect Git write permissions for image automation.

## Related links

- [GitOps](gitops.md)
- [Argo CD vs. Flux](argo-cd-vs-flux.md)
- [Flux documentation](https://fluxcd.io/flux/)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
