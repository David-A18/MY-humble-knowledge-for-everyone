# Kubernetes

Practical Kubernetes notes for workloads, core objects, kubectl workflows, application tooling, troubleshooting, and operations.

## Security and operations learning paths

- [Istio security](applications-and-tools/istio/index.md) - Workload authentication and authorization.
- [Manifest validation](applications-and-tools/manifest-validation/index.md) - Differences, drift, and regressions.
- [kro](applications-and-tools/kro/index.md) - Kubernetes platform APIs.
- [Common platform tools](applications-and-tools/platform-tooling/index.md) - Tool selection and integrations.
- [IRSA S3 lab](../cross-topic-guides/irsa-s3-access-on-eks.md) - AWS workload permissions.
- [Kafka aggregation lab](../cross-topic-guides/kubernetes-data-aggregation.md) - Stateful event processing.

## Added learning guides

- [Kubernetes observability](observability/index.md) - Focused learning material and supporting examples.

## Index

| Section | Focus |
| --- | --- |
| [Fundamentals](fundamentals/index.md) | Cluster concepts, control plane basics, and workload lifecycle. |
| [Core objects](core-objects/index.md) | Pods, deployments, services, config, storage, and ingress concepts. |
| [Commands](commands/index.md) | `kubectl` workflows and diagnostic commands. |
| [Crossplane](crossplane/index.md) | Kubernetes-native infrastructure control planes, professional operating models, AWS workflows, managed resources, providers, compositions, GitOps, operations, labs, and troubleshooting. |
| [Applications and tools](applications-and-tools/index.md) | Helm, Kustomize, controllers, and platform tooling. |
| [Troubleshooting](troubleshooting/index.md) | Symptom-driven cluster and workload diagnostics. |
| [Best practices](best-practices/index.md) | Operational safety, resource design, and reliability habits. |
| [Tricks](tricks/index.md) | Helpful command patterns and productivity notes. |
| [Examples](examples/index.md) | Practical manifests and walkthroughs. |

## Fast paths for application tooling

| Topic | Start here | Follow-up |
| --- | --- | --- |
| APISIX | [Apache APISIX](applications-and-tools/apache-apisix.md) | [Architecture and deployment](applications-and-tools/apisix-architecture-and-deployment.md), [security and observability](applications-and-tools/apisix-security-traffic-and-observability.md), [APISIX on EKS](../cross-topic-guides/apisix-on-eks.md). |
| Flux | [Flux](applications-and-tools/flux.md) | [Flux reconciliation and Helm releases](applications-and-tools/flux-reconciliation-and-helm.md), [GitOps security and multi-tenancy](applications-and-tools/gitops-security-and-multitenancy.md), [GitOps on EKS](../cross-topic-guides/gitops-on-eks.md). |
| GitOps comparison | [Argo CD vs. Flux](applications-and-tools/argo-cd-vs-flux.md) | Choose between UI-centered application operations and composable controller-based reconciliation. |
| K9s | [K9s](applications-and-tools/k9s.md) | Navigate, inspect, filter, and operate Kubernetes resources from a terminal UI. |
| Velero | [Velero](../migrations/velero/index.md) | [Storage and volume backups](../migrations/velero/storage-and-volume-backups.md), [backup and restore workflows](../migrations/velero/backup-restore-workflows.md), [cluster migration and disaster recovery](../migrations/velero/cluster-migration-and-disaster-recovery.md). |

## Fast paths for Crossplane

| Topic | Start here | Follow-up |
| --- | --- | --- |
| XRDs, Compositions, and XR calls | [XRDs, Compositions, and XR calls](crossplane/xrd-composition-and-xr-calls.md) | [Component model](crossplane/component-model.md), [Compositions](crossplane/compositions.md), [Terraform vs Crossplane](crossplane/terraform-vs-crossplane.md), [AWS VPC platform API](crossplane/aws-vpc-platform-api.md). |

## Symptom-driven diagnostics

Start with [troubleshooting triage](troubleshooting/common-solutions.md), then follow [Service connectivity](troubleshooting/service-connectivity.md), [DNS](troubleshooting/dns-resolution.md), [scheduling](troubleshooting/pending-pods-and-scheduling.md), [storage](troubleshooting/persistent-volume-failures.md), [gateway/TLS](troubleshooting/gateway-route-and-tls.md), or [rollouts](troubleshooting/rollout-stalls.md).

## AWS and EKS workflows

| Guide | Focus |
| --- | --- |
| [Kubernetes on AWS](../cross-topic-guides/kubernetes-on-aws.md) | EKS operating model, identity, networking, storage, add-ons, and cost visibility. |
| [Deploying to EKS](../cross-topic-guides/deploying-to-eks.md) | EKS deployment workflow from kubeconfig through rollout validation. |
| [EKS operations](../cross-topic-guides/eks-operations.md) | AWS CLI and `kubectl` commands for day-to-day EKS operations. |
| [Velero AWS S3 and EBS installation](../migrations/velero/aws-s3-ebs-installation.md) | EKS backup and restore setup with S3 backup storage, EBS snapshots, and CSI snapshot support. |

## Official documentation

- [Kubernetes documentation](https://kubernetes.io/docs/)
- [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
- [Amazon EKS documentation](https://docs.aws.amazon.com/eks/)

[Back to root index](../../README.md)
