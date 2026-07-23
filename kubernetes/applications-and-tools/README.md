# Kubernetes applications and tools

Status: Initial outline

Notes for tools commonly used to package, deploy, and operate Kubernetes workloads.

## Quick path: APISIX

| Need | Read |
| --- | --- |
| Understand what APISIX is and what it does. | [Apache APISIX](apache-apisix.md) |
| Understand APISIX components and request flow. | [APISIX architecture and deployment](apisix-architecture-and-deployment.md) |
| Configure auth, rate limits, traffic release, metrics, logs, and traces. | [APISIX security, traffic, and observability](apisix-security-traffic-and-observability.md) |
| Choose between Ingress, Gateway API, and APISIX CRDs. | [Gateway API and Ingress](gateway-api-and-ingress.md) |
| Run APISIX on Amazon EKS. | [APISIX on EKS](../../cross-topic-guides/apisix-on-eks.md) |
| Troubleshoot 404, 401, 403, 429, 503, TLS, and upstream failures. | [APISIX troubleshooting](../troubleshooting/apisix.md) |

## Quick path: Flux and GitOps

| Need | Read |
| --- | --- |
| Understand the GitOps operating model. | [GitOps](gitops.md) |
| Compare Argo CD and Flux. | [Argo CD vs. Flux](argo-cd-vs-flux.md) |
| Understand Flux controllers and repository structure. | [Flux](flux.md) |
| Follow source, Kustomization, and HelmRelease reconciliation. | [Flux reconciliation and Helm releases](flux-reconciliation-and-helm.md) |
| Scope controller permissions, tenancy, and secrets. | [GitOps security and multi-tenancy](gitops-security-and-multitenancy.md) |
| Operate GitOps on Amazon EKS. | [GitOps on EKS](../../cross-topic-guides/gitops-on-eks.md) |

## Quick path: Velero

| Need | Read |
| --- | --- |
| Understand Kubernetes backup, restore, and migration with Velero. | [Velero](../../migrations/velero/README.md) |
| Choose between S3, EBS snapshots, CSI snapshots, and File System Backup. | [Velero storage and volume backups](../../migrations/velero/storage-and-volume-backups.md) |
| Install Velero on EKS with S3 and EBS snapshot support. | [Velero AWS S3 and EBS installation](../../migrations/velero/aws-s3-ebs-installation.md) |

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
| [Velero](../../migrations/velero/README.md) | Back up, restore, migrate, and recover Kubernetes resources and persistent volumes. |

## Expected content

- Helm.
- Kustomize.
- External secrets operators.

[Back to Kubernetes index](../README.md) | [Back to root index](../../README.md)
