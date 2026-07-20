# Kubernetes

Practical Kubernetes notes for workloads, core objects, kubectl workflows, application tooling, troubleshooting, and operations.

## Index

| Section | Focus |
| --- | --- |
| [Fundamentals](fundamentals/README.md) | Cluster concepts, control plane basics, and workload lifecycle. |
| [Core objects](core-objects/README.md) | Pods, deployments, services, config, storage, and ingress concepts. |
| [Commands](commands/README.md) | `kubectl` workflows and diagnostic commands. |
| [Crossplane](crossplane/README.md) | Kubernetes-native infrastructure control planes, professional operating models, AWS workflows, managed resources, providers, compositions, GitOps, operations, labs, and troubleshooting. |
| [Applications and tools](applications-and-tools/README.md) | Helm, Kustomize, controllers, and platform tooling. |
| [Troubleshooting](troubleshooting/README.md) | Symptom-driven cluster and workload diagnostics. |
| [Best practices](best-practices/README.md) | Operational safety, resource design, and reliability habits. |
| [Tricks](tricks/README.md) | Helpful command patterns and productivity notes. |
| [Examples](examples/README.md) | Practical manifests and walkthroughs. |

## Fast paths for application tooling

| Topic | Start here | Follow-up |
| --- | --- | --- |
| APISIX | [Apache APISIX](applications-and-tools/apache-apisix.md) | [Architecture and deployment](applications-and-tools/apisix-architecture-and-deployment.md), [security and observability](applications-and-tools/apisix-security-traffic-and-observability.md), [APISIX on EKS](../cross-topic-guides/apisix-on-eks.md). |
| Flux | [Flux](applications-and-tools/flux.md) | [Flux reconciliation and Helm releases](applications-and-tools/flux-reconciliation-and-helm.md), [GitOps security and multi-tenancy](applications-and-tools/gitops-security-and-multitenancy.md), [GitOps on EKS](../cross-topic-guides/gitops-on-eks.md). |
| GitOps comparison | [Argo CD vs. Flux](applications-and-tools/argo-cd-vs-flux.md) | Choose between UI-centered application operations and composable controller-based reconciliation. |

## AWS and EKS workflows

| Guide | Focus |
| --- | --- |
| [Kubernetes on AWS](../cross-topic-guides/kubernetes-on-aws.md) | EKS operating model, identity, networking, storage, add-ons, and cost visibility. |
| [Deploying to EKS](../cross-topic-guides/deploying-to-eks.md) | EKS deployment workflow from kubeconfig through rollout validation. |
| [EKS operations](../cross-topic-guides/eks-operations.md) | AWS CLI and `kubectl` commands for day-to-day EKS operations. |

## Official documentation

- [Kubernetes documentation](https://kubernetes.io/docs/)
- [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
- [Amazon EKS documentation](https://docs.aws.amazon.com/eks/)

[Back to root index](../README.md)
