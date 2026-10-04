# Kubernetes applications and tools

Status: Initial outline

Notes for tools commonly used to package, deploy, and operate Kubernetes workloads.

## Quick path: kind

| Need | Read |
| --- | --- |
| Understand node layout, context, and host port mappings. | [How kind custom clusters fit together](kind-custom-clusters.md) |
| Choose how a locally built image reaches a kind Pod. | [How images reach a kind Pod](kind-images-and-local-registries.md) |
| Diagnose a Pod that cannot pull a local image. | [Diagnose a local image pull in kind](../troubleshooting/kind.md) |

## Quick path: APISIX

| Need | Read |
| --- | --- |
| Follow one request through a gateway route, plugin, and upstream. | [What Apache APISIX does for an API](apache-apisix.md) |
| Separate gateway traffic, controller translation, and APISIX configuration storage. | [How the APISIX gateway and controller fit together](apisix-architecture-and-deployment.md) |
| Understand what configured auth, limits, traffic splits, and telemetry decide for one request. | [How APISIX policies shape one request](apisix-security-traffic-and-observability.md) |
| Follow an external request to a Service and choose between Ingress, Gateway API, and implementation-specific routes. | [Gateway API and Ingress](gateway-api-and-ingress.md) |
| Run APISIX on Amazon EKS. | [APISIX on EKS](../../cross-topic-guides/apisix-on-eks.md) |
| Find where a 404 arises along an APISIX request path. | [Trace an APISIX 404](../troubleshooting/apisix.md) |

## Quick path: Flux and GitOps

| Need | Read |
| --- | --- |
| Understand GitOps as a pulled, continuously reconciled operating model and what a green sync does not prove. | [GitOps](gitops.md) |
| Compare Argo CD and Flux on documented differences and defaults, or split ownership between them. | [Argo CD vs. Flux](argo-cd-vs-flux.md) |
| Understand the Flux chain from source to artifact to reconciler, and what `Ready` proves. | [Flux](flux.md) |
| Follow a HelmRelease declaration from Git to an installed chart. | [How Flux applies a HelmRelease from Git](flux-reconciliation-and-helm.md) |
| Follow Git writers, GitOps policy, apply identity, and Kubernetes permissions before trusting a tenant boundary. | [GitOps security and multi-tenancy](gitops-security-and-multitenancy.md) |
| Operate GitOps on Amazon EKS. | [GitOps on EKS](../../cross-topic-guides/gitops-on-eks.md) |

## Quick path: Helm

| Need | Read |
| --- | --- |
| Understand charts, releases, values, rendering, upgrades, and rollbacks. | [How Helm turns a chart into a release](helm.md) |
| Understand Helm's role in a Crossplane installation. | [Helm and Crossplane's controller boundary](helm.md#crossplane-is-a-second-controller-layer), then the [official Crossplane install procedure](https://docs.crossplane.io/latest/get-started/install/). |
| Publish or consume Helm OCI charts in Amazon ECR. | [Amazon ECR](../../cloud/aws/compute/amazon-ecr.md#helm-charts-in-ecr-through-oci) |

## Quick path: Velero

| Need | Read |
| --- | --- |
| Understand Kubernetes backup, restore, and migration with Velero. | [Velero](../../migrations/velero/index.md) |
| Choose between S3, EBS snapshots, CSI snapshots, and File System Backup. | [Velero storage and volume backups](../../migrations/velero/storage-and-volume-backups.md) |
| Install Velero on EKS with S3 and EBS snapshot support. | [Velero AWS S3 and EBS installation](../../migrations/velero/aws-s3-ebs-installation.md) |

## Quick path: K9s

| Need | Read |
| --- | --- |
| Understand what K9s reads from Kubernetes. | [Inspect a failing Pod with K9s](k9s.md#what-you-will-do) |
| Start in a known context and namespace. | [Confirm the target](k9s.md#1-confirm-the-target) |
| Read a Pod's status, events, and logs. | [Select a Pod](k9s.md#2-open-the-pod-view-and-select-one-pod) and [read its evidence](k9s.md#3-read-the-evidence-for-the-selected-pod). |
| Choose a next investigation without a blind repair. | [Follow the first failed boundary](k9s.md#4-follow-the-first-failed-boundary). |

## Articles

| Article | Purpose |
| --- | --- |
| [What Apache APISIX does for an API](apache-apisix.md) | Understand routes, plugins, upstreams, and the separate Kubernetes configuration path. |
| [How the APISIX gateway and controller fit together](apisix-architecture-and-deployment.md) | Understand the two paths, Gateway API objects, deployment modes, and status limits. |
| [How APISIX policies shape one request](apisix-security-traffic-and-observability.md) | Follow one request through optional auth, limit, release, and telemetry policies. |
| [Gateway API and Ingress](gateway-api-and-ingress.md) | Understand the request path, controller requirement, Gateway API ownership, and route choice. |
| [GitOps](gitops.md) | Understand the four GitOps principles, what CI publishes versus what a controller pulls, and the limits of a green sync. |
| [Argo CD vs. Flux](argo-cd-vs-flux.md) | Compare application model, components, interfaces, sync defaults, and multi-cluster boundaries from each project's documentation. |
| [Flux](flux.md) | Understand which Flux controller fetches, which reconciles, and which capabilities are optional. |
| [How Flux applies a HelmRelease from Git](flux-reconciliation-and-helm.md) | Understand the two controller handoffs and what their status reports prove. |
| [GitOps security and multi-tenancy](gitops-security-and-multitenancy.md) | Understand Argo CD projects, Flux apply identities, workload access, and secret handling. |
| [How Helm turns a chart into a release](helm.md) | Understand chart inputs, release revisions, preview limits, and the Crossplane controller boundary. |
| [When a tooling cluster helps](tooling-clusters.md) | Choose between local, shared, and hybrid tooling by tracing responsibility, authority, and failure dependencies. |
| [How a tooling cluster connects to workload clusters](tooling-cluster-architecture.md) | Trace source, target API, telemetry, user, and recovery paths for a shared controller. |
| [How kind custom clusters fit together](kind-custom-clusters.md) | Explain node roles, context, node images, and the full host-port-to-Pod path. |
| [How images reach a kind Pod](kind-images-and-local-registries.md) | Choose between loading an image into kind nodes and pulling from a configured registry. |
| [Inspect a failing Pod with K9s](k9s.md) | Select a target and read one Pod's status, events, and logs before choosing a troubleshooting route. |
| [Velero](../../migrations/velero/index.md) | Back up, restore, migrate, and recover Kubernetes resources and persistent volumes. |

## Expected content

- Kustomize.
- External secrets operators.

[Back to Kubernetes index](../index.md) | [Back to root index](../../../README.md)
