# Kubernetes applications and tools

Status: Initial outline

Notes for tools commonly used to package, deploy, and operate Kubernetes workloads.

## Articles

| Article | Purpose |
| --- | --- |
| [Apache APISIX](apache-apisix.md) | Understand APISIX as a Kubernetes API gateway. |
| [APISIX architecture and deployment](apisix-architecture-and-deployment.md) | Understand APISIX data-plane, controller, Gateway API, and EKS exposure patterns. |
| [APISIX security, traffic, and observability](apisix-security-traffic-and-observability.md) | Place authentication, rate limits, release policy, and telemetry in APISIX safely. |
| [Gateway API and Ingress](gateway-api-and-ingress.md) | Choose between Ingress, Gateway API, and gateway-specific CRDs. |
| [GitOps](gitops.md) | Understand Kubernetes GitOps reconciliation. |
| [Argo CD vs. Flux](argo-cd-vs-flux.md) | Compare two common GitOps controllers. |
| [Flux](flux.md) | Understand Flux controllers and repository design. |
| [Flux reconciliation and Helm releases](flux-reconciliation-and-helm.md) | Follow Flux source, Kustomization, and HelmRelease reconciliation. |
| [GitOps security and multi-tenancy](gitops-security-and-multitenancy.md) | Scope GitOps controller permissions, secrets, and ownership boundaries. |
| [Tooling clusters](tooling-clusters.md) | Decide when to use a dedicated platform tooling cluster. |
| [Tooling cluster architecture](tooling-cluster-architecture.md) | Design tooling cluster patterns, failure behavior, security, and EKS account boundaries. |
| [kind custom clusters](kind-custom-clusters.md) | Create local Kubernetes clusters for labs and CI. |
| [kind images and local registries](kind-images-and-local-registries.md) | Load host-built images into kind or use a local registry. |

## Expected content

- Helm.
- Kustomize.
- External secrets operators.

[Back to Kubernetes index](../README.md) | [Back to root index](../../README.md)
