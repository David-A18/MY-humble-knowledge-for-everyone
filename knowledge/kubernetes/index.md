# Kubernetes

Practical Kubernetes notes for workloads, core objects, kubectl workflows, application tooling, troubleshooting, and operations.

Start with [Kubernetes fundamentals](fundamentals/kubernetes-fundamentals.md)
if clusters, Pods, Deployments, or Services are new to you. Next, see
[how a Service selects Pods](core-objects/how-a-service-selects-pods.md).
For hands-on practice, follow [Start here](../start-here.md#end-to-end-local-practice-route):
it includes the Git basics needed to inspect and restore exercise files before
the [local deployment learning path](../cross-topic-guides/local-deployment-learning-path.md).

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
| kind local clusters | [How kind custom clusters fit together](applications-and-tools/kind-custom-clusters.md) | [How images reach a kind Pod](applications-and-tools/kind-images-and-local-registries.md), then [diagnose a local image pull](troubleshooting/kind.md) if a Pod cannot start. |
| APISIX | [What Apache APISIX does for an API](applications-and-tools/apache-apisix.md) | [How the gateway and controller fit together](applications-and-tools/apisix-architecture-and-deployment.md), [APISIX request policies](applications-and-tools/apisix-security-traffic-and-observability.md), [APISIX on EKS](../cross-topic-guides/apisix-on-eks.md). |
| Flux | [Flux](applications-and-tools/flux.md) | [How Flux applies a HelmRelease from Git](applications-and-tools/flux-reconciliation-and-helm.md), [GitOps security and multi-tenancy](applications-and-tools/gitops-security-and-multitenancy.md), [GitOps on EKS](../cross-topic-guides/gitops-on-eks.md). |
| GitOps comparison | [Argo CD vs. Flux](applications-and-tools/argo-cd-vs-flux.md) | Start from [GitOps](applications-and-tools/gitops.md), then compare documented defaults, interfaces, and ownership boundaries. |
| K9s | [Inspect a failing Pod with K9s](applications-and-tools/k9s.md) | Use a terminal UI to read Pod evidence and choose a troubleshooting path. |
| Velero | [Velero](../migrations/velero/index.md) | [Storage and volume backups](../migrations/velero/storage-and-volume-backups.md), [backup and restore workflows](../migrations/velero/backup-restore-workflows.md), [cluster migration and disaster recovery](../migrations/velero/cluster-migration-and-disaster-recovery.md). |

## Fast paths for Crossplane

| Topic | Start here | Follow-up |
| --- | --- | --- |
| First Crossplane request | [How Crossplane's components turn a request into a resource](crossplane/component-model.md) | [How to request a Crossplane platform API](crossplane/xrd-composition-and-xr-calls.md), [Compositions](crossplane/compositions.md), [When to use Terraform or Crossplane](crossplane/terraform-vs-crossplane.md), [How one Crossplane request becomes an AWS network](crossplane/aws-vpc-platform-api.md). |

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

[Back to knowledge index](../index.md)
