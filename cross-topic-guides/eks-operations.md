# EKS operations

## Purpose

Collect practical Amazon EKS operations that combine AWS CLI checks with `kubectl` workflows.

## Identity and kubeconfig

| Task | Command | When to use it |
| --- | --- | --- |
| Confirm AWS identity | `aws sts get-caller-identity` | Before connecting to or changing an EKS cluster. |
| List EKS clusters | `aws eks list-clusters --region <region>` | Find available clusters in a Region. |
| Update kubeconfig | `aws eks update-kubeconfig --region <region> --name <cluster>` | Connect `kubectl` to an EKS cluster. |
| Check Kubernetes context | `kubectl config current-context` | Confirm the active target cluster. |
| Check permission | `kubectl auth can-i <verb> <resource> -n <namespace>` | Validate Kubernetes authorization. |

### Connect to an EKS cluster

```bash
aws sts get-caller-identity
aws eks update-kubeconfig --region eu-west-1 --name production-platform
kubectl config current-context
kubectl get namespaces
```

What it does: confirms the AWS caller, writes or updates kubeconfig for the EKS cluster, confirms context, and checks API access.

> [!IMPORTANT]
> `update-kubeconfig` changes local kubeconfig state. Confirm the AWS profile and Region before running it when you manage multiple accounts.

## Access entries

| Task | Command | When to use it |
| --- | --- | --- |
| List access entries | `aws eks list-access-entries --cluster-name <cluster>` | Review IAM principals mapped to the cluster. |
| Describe an access entry | `aws eks describe-access-entry --cluster-name <cluster> --principal-arn <arn>` | Inspect one IAM principal mapping. |
| List associated policies | `aws eks list-associated-access-policies --cluster-name <cluster> --principal-arn <arn>` | Review EKS access policies for a principal. |

### Review cluster access entries

```bash
aws eks list-access-entries --cluster-name production-platform --region eu-west-1
```

What it does: lists IAM principals that have EKS access entries on the cluster.

> [!WARNING]
> Access entries affect who can authenticate to the Kubernetes API. Review least privilege and audit requirements before adding broad admin access.

## Workload AWS permissions

| Option | Use it for | Notes |
| --- | --- | --- |
| EKS Pod Identity | EKS-native workload access to AWS services | Preferred for many EKS-only workloads when supported. |
| IAM roles for service accounts | Fine-grained IAM using Kubernetes service accounts | Useful and still supported, including patterns built around OIDC. |
| Node IAM role | Node-level permissions | Avoid using this for application-specific AWS access. |

### Check service account annotations

```bash
kubectl get serviceaccount web -n app -o yaml
```

What it does: shows whether the workload service account is configured for AWS permissions, such as IRSA annotations or Pod Identity-related ownership.

> [!IMPORTANT]
> Grant each workload only the AWS actions it needs. Avoid sharing broad IAM roles across unrelated applications.

## Add-ons and cluster components

| Task | Command | When to use it |
| --- | --- | --- |
| List EKS add-ons | `aws eks list-addons --cluster-name <cluster> --region <region>` | See managed add-ons on a cluster. |
| Describe add-on | `aws eks describe-addon --cluster-name <cluster> --addon-name <addon> --region <region>` | Check version, health, and configuration. |
| Check system pods | `kubectl get pods -n kube-system` | Inspect CoreDNS, CNI, proxy, and controllers. |

### Check add-ons and system pods

```bash
aws eks list-addons --cluster-name production-platform --region eu-west-1
kubectl get pods -n kube-system -o wide
```

What it does: lists EKS-managed add-ons and checks whether cluster system pods are running.

## Nodes and capacity

| Task | Command | When to use it |
| --- | --- | --- |
| List node groups | `aws eks list-nodegroups --cluster-name <cluster> --region <region>` | Find managed node groups. |
| Describe node group | `aws eks describe-nodegroup --cluster-name <cluster> --nodegroup-name <name> --region <region>` | Inspect scaling and health. |
| List Kubernetes nodes | `kubectl get nodes -o wide` | Check node readiness and versions. |
| Check node pressure | `kubectl describe node <node>` | Investigate scheduling and resource issues. |

### Inspect capacity

```bash
aws eks list-nodegroups --cluster-name production-platform --region eu-west-1
kubectl get nodes -o wide
kubectl top nodes
```

What it does: lists EKS managed node groups, shows Kubernetes nodes, and checks live node resource usage when metrics are available.

## Basic EKS diagnostics

```bash
aws sts get-caller-identity
kubectl config current-context
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A --field-selector=status.phase!=Running
kubectl get events -A --sort-by=.lastTimestamp
```

What it does: confirms identity and context, checks cluster reachability, lists nodes, finds non-running pods, and reviews recent cluster events.

## eksctl command reference

Use `eksctl` when the operation changes AWS/EKS infrastructure rather than normal Kubernetes objects.

| Need | Reference |
| --- | --- |
| Cluster and node group lifecycle | [eksctl commands for Amazon EKS](../kubernetes/commands/eksctl-commands.md) |
| Kubernetes object inspection and rollout workflows | [Kubernetes command workflows](../kubernetes/commands/workflows.md) |

## Official documentation

- [Amazon EKS kubeconfig](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
- [Amazon EKS access entries](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)
- [Amazon EKS workload IAM access](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html)
- [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
- [Amazon EKS add-ons](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html)
- [Amazon EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html)
- [eksctl user guide](https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html)

## Related links

- [Kubernetes on AWS](kubernetes-on-aws.md)
- [Deploying to EKS](deploying-to-eks.md)
- [eksctl commands for Amazon EKS](../kubernetes/commands/eksctl-commands.md)
- [Kubernetes commands](../kubernetes/commands/README.md)
- [AWS index](../cloud/aws/README.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
