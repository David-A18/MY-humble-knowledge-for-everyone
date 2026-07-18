# Argo CD vs. Flux

## Purpose

Use this page to compare Argo CD and Flux for Kubernetes GitOps delivery.

## Comparison

| Area | Argo CD | Flux |
| --- | --- | --- |
| Operating model | Application-centric with strong UI and sync workflows. | Controller-centric with composable source, Kustomize, Helm, notification, and image automation controllers. |
| User experience | Strong visual operations and manual sync patterns. | Git-native automation and toolkit-style composition. |
| Multi-cluster | Common for centralized visibility and app management. | Common for distributed reconciliation with Git-driven automation. |
| Best fit | Teams that value a UI and application inventory. | Teams that value controller composition and automation-first workflows. |

## Coexistence

Argo CD and Flux can coexist, but they should not own the same resources. Split ownership by cluster, namespace, application, or platform concern.

## Related links

- [GitOps](gitops.md)
- [Flux](flux.md)
- [Argo CD documentation](https://argo-cd.readthedocs.io/)
- [Flux documentation](https://fluxcd.io/flux/)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
