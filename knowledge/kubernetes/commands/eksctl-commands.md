---
type: "How-to Guide"
title: "eksctl commands for Amazon EKS"
description: "Collect eksctl commands that are specific to Amazon EKS operations and different from normal kubectl work."
tags: [kubernetes, eksctl-commands]
status: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# eksctl commands for Amazon EKS

## Purpose

Collect `eksctl` commands that are specific to Amazon EKS operations and different from normal `kubectl` work.

`kubectl` manages Kubernetes API objects such as Pods, Deployments, Services, and ConfigMaps. `eksctl` manages AWS-side EKS resources such as clusters, node groups, Fargate profiles, EKS add-ons, IAM access, Pod Identity, VPC endpoint access, CloudWatch control plane logging, and CloudFormation-backed infrastructure.

## When to use eksctl instead of kubectl

| Need | Use | Why |
| --- | --- | --- |
| Inspect or change Kubernetes resources | `kubectl` | Talks to the Kubernetes API server. |
| Create or delete an EKS cluster | `eksctl` | Provisions AWS resources and EKS control plane configuration. |
| Manage EKS node groups | `eksctl` | Uses EKS, EC2 Auto Scaling, and CloudFormation behavior. |
| Manage EKS add-ons | `eksctl` | Talks to EKS add-on APIs and can manage related IAM. |
| Grant IAM principals cluster access | `eksctl` | Manages EKS access entries or legacy `aws-auth` mappings. |
| Grant pods AWS permissions | `eksctl` | Creates Pod Identity associations or IRSA resources. |
| Change EKS endpoint or control plane logging | `eksctl` | Updates AWS-side cluster configuration. |

> [!IMPORTANT]
> `eksctl` can create, update, and delete AWS infrastructure. Always confirm AWS account, Region, cluster name, and config file before running mutating commands.

## Daily discovery

| Task | Command | When to use it |
| --- | --- | --- |
| Show `eksctl` version | `eksctl version` | Confirm the local tool version. |
| Show command help | `eksctl help` | Discover available command groups. |
| Show subcommand help | `eksctl <command> --help` | Check flags before a risky operation. |
| Confirm AWS identity | `aws sts get-caller-identity` | Verify the AWS account and role used by `eksctl`. |
| List clusters | `eksctl get cluster --region <region>` | Find EKS clusters visible to the current AWS identity. |
| Write kubeconfig | `eksctl utils write-kubeconfig --cluster <cluster> --region <region>` | Configure `kubectl` access through `eksctl`. |
| Show CloudFormation stacks | `eksctl utils describe-stacks --cluster <cluster> --region <region>` | Inspect stacks managed by `eksctl`. |

### Confirm identity and list clusters

```bash
aws sts get-caller-identity
eksctl get cluster --region eu-west-1
```

What it does: confirms the AWS caller and lists EKS clusters in the selected Region.

### Write kubeconfig with eksctl

```bash
eksctl utils write-kubeconfig --cluster production-platform --region eu-west-1
kubectl config current-context
```

What it does: writes kubeconfig for the EKS cluster, then checks the active Kubernetes context.

> [!TIP]
> `aws eks update-kubeconfig` and `eksctl utils write-kubeconfig` both prepare kubeconfig. Use whichever is standard in your team, then verify the active context before running `kubectl`.

## Cluster lifecycle

| Task | Command | When to use it |
| --- | --- | --- |
| Create default cluster | `eksctl create cluster --name <cluster> --region <region>` | Quick test or learning cluster. |
| Create from config | `eksctl create cluster -f cluster.yaml` | Reproducible cluster creation. |
| Dry-run config | `eksctl create cluster -f cluster.yaml --dry-run` | Inspect generated config before creation. |
| Get cluster details | `eksctl get cluster --name <cluster> --region <region>` | Confirm cluster presence and metadata. |
| Upgrade control plane plan | `eksctl upgrade cluster --name <cluster> --region <region>` | Preview next supported Kubernetes minor upgrade. |
| Upgrade control plane | `eksctl upgrade cluster --name <cluster> --region <region> --approve` | Apply a planned control plane upgrade. |
| Delete from config | `eksctl delete cluster -f cluster.yaml --wait` | Tear down a config-managed cluster. |
| Delete by name | `eksctl delete cluster --name <cluster> --region <region> --wait` | Tear down a named cluster. |

### Dry-run cluster config

```bash
eksctl create cluster -f cluster.yaml --dry-run
```

What it does: validates and expands cluster settings without creating AWS resources.

### Create a cluster from config

```bash
eksctl create cluster -f cluster.yaml
```

What it does: creates the EKS cluster and related AWS resources described by `cluster.yaml`.

> [!WARNING]
> Cluster creation creates billable AWS resources such as the EKS control plane, EC2 capacity, load balancer-related infrastructure, CloudFormation stacks, and networking resources.

### Delete a cluster

```bash
eksctl delete cluster -f cluster.yaml --wait
```

What it does: deletes the cluster and waits for the CloudFormation-backed teardown to complete.

> [!WARNING]
> Cluster deletion removes infrastructure and can interrupt every workload on the cluster. Use `--wait` so deletion failures are surfaced, and check external dependencies such as load balancers, PVCs, and PodDisruptionBudgets.

## Node groups

| Task | Command | When to use it |
| --- | --- | --- |
| Create node group | `eksctl create nodegroup --cluster <cluster> --name <nodegroup>` | Add EC2 capacity to a cluster. |
| Create from config | `eksctl create nodegroup --config-file cluster.yaml` | Create declared node groups. |
| List node groups | `eksctl get nodegroup --cluster <cluster> --region <region>` | Inspect worker capacity groups. |
| Get node group as YAML | `eksctl get nodegroup --cluster <cluster> --name <nodegroup> --output yaml` | Review detailed node group state. |
| Scale node group | `eksctl scale nodegroup --cluster <cluster> --name <nodegroup> --nodes <count> --wait` | Change desired EC2 node count. |
| Drain node group | `eksctl drain nodegroup --cluster <cluster> --name <nodegroup>` | Evict pods from all nodes in a node group. |
| Undo drain | `eksctl drain nodegroup --cluster <cluster> --name <nodegroup> --undo` | Uncordon a drained node group. |
| Delete node group | `eksctl delete nodegroup --cluster <cluster> --name <nodegroup>` | Remove EC2 worker capacity. |
| Upgrade node group | `eksctl upgrade nodegroup --cluster <cluster> --name <nodegroup>` | Upgrade supported node group components. |
| Check node group health | `eksctl utils nodegroup-health --cluster <cluster> --name <nodegroup>` | Diagnose EKS node group health issues. |
| Set node labels | `eksctl set labels --cluster <cluster> --nodegroup <nodegroup> --labels <key=value>` | Apply labels at the managed node group level. |
| Remove node labels | `eksctl unset labels --cluster <cluster> --nodegroup <nodegroup> --labels <key>` | Remove labels at the managed node group level. |

### Scale a node group

```bash
eksctl scale nodegroup --cluster production-platform --name workers-a --nodes 5 --wait
```

What it does: changes desired capacity for the node group and waits for the scaling operation.

> [!IMPORTANT]
> Scaling down with `eksctl scale nodegroup` changes AWS capacity and does not replace a careful workload drain plan. Check workload disruption risk before reducing nodes.

### Drain a node group

```bash
eksctl drain nodegroup --cluster production-platform --name workers-a
```

What it does: cordons and evicts pods from nodes in the selected node group.

> [!WARNING]
> Draining can disrupt workloads. Check PodDisruptionBudgets, replica counts, and maintenance windows first.

### Delete a node group

```bash
eksctl delete nodegroup --cluster production-platform --name workers-a
```

What it does: drains eligible pods and removes the selected node group.

> [!WARNING]
> Node group deletion removes compute capacity. Confirm replacement capacity exists before deleting production node groups.

## EKS add-ons

| Task | Command | When to use it |
| --- | --- | --- |
| Create add-on | `eksctl create addon --cluster <cluster> --name <addon>` | Install an EKS-managed add-on. |
| Create add-ons from config | `eksctl create addon -f cluster.yaml` | Apply add-on declarations. |
| List add-ons | `eksctl get addon --cluster <cluster>` | See enabled add-ons and versions. |
| Discover add-on versions | `eksctl utils describe-addon-versions --cluster <cluster>` | Find compatible add-on versions. |
| Discover by Kubernetes version | `eksctl utils describe-addon-versions --kubernetes-version <version>` | Plan add-ons before cluster creation. |
| Show add-on config schema | `eksctl utils describe-addon-configuration --name <addon> --version <version>` | Inspect configurable fields. |
| Update add-on | `eksctl update addon --cluster <cluster> --name <addon> --version <version>` | Upgrade or reconfigure an add-on. |
| Update from config | `eksctl update addon -f cluster.yaml` | Reconcile declared add-on config. |
| Delete add-on | `eksctl delete addon --cluster <cluster> --name <addon>` | Remove an EKS-managed add-on. |

### Discover add-on versions

```bash
eksctl utils describe-addon-versions --cluster production-platform
```

What it does: discovers compatible EKS add-ons and versions for the cluster Kubernetes version.

### Update an add-on

```bash
eksctl update addon --cluster production-platform --name vpc-cni --version latest
```

What it does: updates the VPC CNI EKS add-on to the resolved latest compatible version.

> [!WARNING]
> Add-on changes can affect networking, DNS, proxying, storage, and observability. Test version and configuration changes outside production first.

### Delete an add-on

```bash
eksctl delete addon --cluster production-platform --name aws-ebs-csi-driver
```

What it does: removes the selected EKS add-on and IAM roles associated with it when they are managed by `eksctl`.

> [!WARNING]
> Deleting storage, networking, or DNS add-ons can break workloads. Confirm impact before removing add-ons.

## Upgrade workflow

Use `eksctl` for the AWS/EKS side of the upgrade and `kubectl` for workload validation.

```bash
eksctl upgrade cluster --name production-platform --region eu-west-1
eksctl upgrade cluster --name production-platform --region eu-west-1 --approve
eksctl get nodegroup --cluster production-platform --region eu-west-1
eksctl update addon --cluster production-platform --name vpc-cni --version latest
kubectl get nodes
kubectl get pods -A --field-selector=status.phase!=Running
```

What it does: previews and applies the control plane upgrade, reviews node groups, updates an add-on, and validates cluster health with `kubectl`.

> [!IMPORTANT]
> EKS control plane upgrades are one minor version at a time. Review AWS upgrade guidance and test add-on, node group, and workload compatibility before production upgrades.

## Related pages

Access, workload permissions, and compute and network options have their own pages:

- [eksctl commands for EKS access and workload permissions](eksctl-access-and-permissions.md) - Grant people cluster access with access entries or legacy aws-auth, and give pods AWS permissions with Pod Identity or IRSA, using eksctl.
- [eksctl commands for Fargate, Auto Mode, and networking](eksctl-compute-and-network-options.md) - Configure Fargate profiles, EKS Auto Mode and Karpenter, endpoint access, and control plane logging with eksctl.

## Official documentation

- [What is eksctl?](https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html)
- [Creating and managing clusters](https://docs.aws.amazon.com/eks/latest/eksctl/creating-and-managing-clusters.html)
- [Work with node groups](https://docs.aws.amazon.com/eks/latest/eksctl/general-nodegroups.html)
- [Add-ons](https://docs.aws.amazon.com/eks/latest/eksctl/addons.html)
- [EKS access entries](https://docs.aws.amazon.com/eks/latest/eksctl/access-entries.html)
- [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/eksctl/iamserviceaccounts.html)
- [EKS Pod Identity associations](https://docs.aws.amazon.com/eks/latest/eksctl/pod-identity-associations.html)
- [EKS Fargate support](https://docs.aws.amazon.com/eks/latest/eksctl/fargate.html)
- [EKS Auto Mode](https://docs.aws.amazon.com/eks/latest/eksctl/auto-mode.html)
- [Cluster access](https://docs.aws.amazon.com/eks/latest/eksctl/vpc-cluster-access.html)
- [CloudWatch logging](https://docs.aws.amazon.com/eks/latest/eksctl/cloudwatch-cluster-logging.html)
- [Cluster upgrades](https://docs.aws.amazon.com/eks/latest/eksctl/cluster-upgrade.html)
- [Non eksctl-created clusters](https://docs.aws.amazon.com/eks/latest/eksctl/unowned-clusters.html)

## Related links

- [Daily Kubernetes usage commands](daily-usage.md)
- [Kubernetes command workflows](workflows.md)
- [EKS operations](../../cross-topic-guides/eks-operations.md)
- [Back to Kubernetes commands](index.md)
- [Back to Kubernetes index](../index.md)
- [Back to root index](../../../README.md)
