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

## Access entries and legacy aws-auth

| Task | Command | When to use it |
| --- | --- | --- |
| Update auth mode | `eksctl utils update-authentication-mode --cluster <cluster> --authentication-mode API_AND_CONFIG_MAP` | Prepare a cluster to use EKS access entries. |
| Create access entry | `eksctl create accessentry -f access.yaml` | Grant an IAM principal Kubernetes access through EKS APIs. |
| List access entries | `eksctl get accessentry --cluster <cluster>` | Review IAM principals with EKS access entries. |
| Get one access entry | `eksctl get accessentry --cluster <cluster> --principal-arn <arn>` | Inspect one IAM principal. |
| Delete access entry | `eksctl delete accessentry --cluster <cluster> --principal-arn <arn>` | Remove an IAM principal's EKS access entry. |
| Migrate from aws-auth | `eksctl utils migrate-to-access-entry --cluster <cluster> --target-authentication-mode API_AND_CONFIG_MAP` | Move legacy identity mappings to access entries. |
| Get legacy mappings | `eksctl get iamidentitymapping --cluster <cluster> --region <region>` | Inspect `aws-auth` ConfigMap mappings. |
| Create legacy mapping | `eksctl create iamidentitymapping --cluster <cluster> --region <region> --arn <arn> --group <group> --username <name>` | Add an `aws-auth` mapping when access entries are not used. |
| Delete legacy mapping | `eksctl delete iamidentitymapping --cluster <cluster> --region <region> --arn <arn>` | Remove an `aws-auth` mapping. |

### List access entries

```bash
eksctl get accessentry --cluster production-platform
```

What it does: lists EKS access entries associated with the cluster.

### Migrate legacy aws-auth mappings

```bash
eksctl utils migrate-to-access-entry --cluster production-platform --target-authentication-mode API_AND_CONFIG_MAP
```

What it does: plans or performs migration from `aws-auth` identity mappings to EKS access entries, depending on command behavior and flags.

> [!WARNING]
> Cluster access changes can lock out users or automation. Keep a tested admin break-glass path before changing authentication mode, access entries, or `aws-auth`.

## Workload AWS permissions

| Task | Command | When to use it |
| --- | --- | --- |
| Install Pod Identity agent | `eksctl create addon --cluster <cluster> --name eks-pod-identity-agent` | Enable EKS Pod Identity support on worker nodes. |
| Create Pod Identity association | `eksctl create podidentityassociation --cluster <cluster> --namespace <namespace> --service-account-name <name> --permission-policy-arns <arns>` | Grant a service account AWS permissions with EKS Pod Identity. |
| List Pod Identity associations | `eksctl get podidentityassociation --cluster <cluster>` | Review workload AWS identity mappings. |
| Get one association | `eksctl get podidentityassociation --cluster <cluster> --namespace <namespace> --service-account-name <name>` | Inspect one service account mapping. |
| Update association role | `eksctl update podidentityassociation --cluster <cluster> --namespace <namespace> --service-account-name <name> --role-arn <arn>` | Point a service account at a different IAM role. |
| Delete association | `eksctl delete podidentityassociation --cluster <cluster> --namespace <namespace> --service-account-name <name>` | Remove pod access to an IAM role. |
| Migrate IRSA to Pod Identity | `eksctl utils migrate-to-pod-identity --cluster <cluster> --approve` | Convert supported IRSA and add-on roles to Pod Identity. |
| Associate OIDC provider | `eksctl utils associate-iam-oidc-provider --cluster <cluster>` | Prepare cluster for IRSA. |
| Create IRSA service account | `eksctl create iamserviceaccount --cluster <cluster> --namespace <namespace> --name <name> --attach-policy-arn <arn>` | Create IAM role plus Kubernetes ServiceAccount annotation. |
| Update IRSA service account | `eksctl update iamserviceaccount -f cluster.yaml` | Reconcile IAM service account permissions from config. |
| Delete IRSA service account | `eksctl delete iamserviceaccount --cluster <cluster> --namespace <namespace> --name <name>` | Delete an `eksctl` IAM service account pair. |

### Create Pod Identity association

```bash
eksctl create podidentityassociation \
  --cluster production-platform \
  --namespace app \
  --service-account-name s3-reader \
  --permission-policy-arns arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

What it does: creates or configures a Pod Identity association so pods using the `app/s3-reader` service account can access AWS APIs allowed by the policy.

> [!IMPORTANT]
> Only grant the AWS permissions the workload needs. Avoid broad managed policies for application service accounts unless the risk is understood and accepted.

### Create an IRSA service account

```bash
eksctl utils associate-iam-oidc-provider --cluster production-platform
eksctl create iamserviceaccount \
  --cluster production-platform \
  --namespace app \
  --name s3-reader \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

What it does: ensures the cluster has an IAM OIDC provider, then creates an IAM role and service account annotation for IRSA.

> [!WARNING]
> `eksctl delete iamserviceaccount` can delete Kubernetes ServiceAccounts, including ones not originally created by `eksctl`. Review ownership before deleting.

## Fargate profiles

| Task | Command | When to use it |
| --- | --- | --- |
| Create cluster with Fargate | `eksctl create cluster --fargate` | Create a cluster with default Fargate support. |
| Create Fargate profile | `eksctl create fargateprofile --cluster <cluster> --namespace <namespace>` | Schedule matching pods onto Fargate. |
| Create profiles from config | `eksctl create fargateprofile -f cluster.yaml` | Manage more complex selectors. |
| List profiles | `eksctl get fargateprofile --cluster <cluster>` | Inspect Fargate selectors and execution roles. |
| Show profiles as YAML | `eksctl get fargateprofile --cluster <cluster> -o yaml` | Review detailed profile configuration. |
| Delete profile | `eksctl delete fargateprofile --cluster <cluster> --name <profile> --wait` | Remove a Fargate scheduling profile. |

### Create a Fargate profile

```bash
eksctl create fargateprofile --cluster production-platform --namespace batch --name fp-batch
```

What it does: creates a Fargate profile that schedules matching pods in the `batch` namespace onto Fargate.

> [!IMPORTANT]
> Fargate profiles are immutable. To change selectors, create a replacement profile and delete the old one after workloads are safe.

## EKS Auto Mode and Karpenter setup

| Task | Command | When to use it |
| --- | --- | --- |
| Create Auto Mode cluster | `eksctl create cluster -f auto-mode-cluster.yaml` | Create a cluster with `autoModeConfig.enabled: true`. |
| Enable Auto Mode | `eksctl update auto-mode-config -f cluster.yaml` | Turn on Auto Mode for an existing cluster. |
| Disable Auto Mode | `eksctl update auto-mode-config -f cluster.yaml` | Turn Auto Mode off with `autoModeConfig.enabled: false`. |
| Create Karpenter-ready cluster | `eksctl create cluster -f karpenter-cluster.yaml` | Install Karpenter prerequisites from cluster config. |

### Enable Auto Mode from config

```bash
eksctl update auto-mode-config -f cluster.yaml
```

What it does: updates EKS Auto Mode settings from the cluster config file.

> [!WARNING]
> Auto Mode changes AWS-managed compute, storage, networking, and load balancing behavior for the cluster. Review subnet placement and workload assumptions before enabling it.

## Networking, endpoint access, and logging

| Task | Command | When to use it |
| --- | --- | --- |
| Update endpoint access | `eksctl utils update-cluster-vpc-config --cluster <cluster> --private-access=true --public-access=false` | Change public/private Kubernetes API endpoint access. |
| Update endpoint config from file | `eksctl utils update-cluster-vpc-config -f cluster.yaml --approve` | Apply endpoint and CIDR settings from config. |
| Set public access CIDRs | `eksctl utils update-cluster-vpc-config --cluster <cluster> --public-access-cidrs <cidrs>` | Restrict public API endpoint sources. |
| Enable all control plane logs | `eksctl utils update-cluster-logging --cluster <cluster> --enable-types all --approve` | Send EKS control plane logs to CloudWatch Logs. |
| Enable one log type | `eksctl utils update-cluster-logging --cluster <cluster> --enable-types audit --approve` | Turn on a specific control plane log stream. |
| Disable all logs | `eksctl utils update-cluster-logging --cluster <cluster> --disable-types all --approve` | Stop control plane log ingestion. |

### Restrict public API endpoint access

```bash
eksctl utils update-cluster-vpc-config \
  --cluster production-platform \
  --public-access=true \
  --private-access=true \
  --public-access-cidrs 203.0.113.10/32
```

What it does: keeps public and private endpoint access enabled while restricting public endpoint access to the listed CIDR.

> [!WARNING]
> Endpoint changes can break `kubectl`, `eksctl`, nodes joining the cluster, and automation. Confirm private access paths and allowed CIDRs before applying.

### Enable audit logs

```bash
eksctl utils update-cluster-logging \
  --cluster production-platform \
  --enable-types audit \
  --approve
```

What it does: enables EKS control plane audit logs in CloudWatch Logs.

> [!WARNING]
> Control plane logging can create CloudWatch ingestion and storage costs. Enable the log types you need and set retention where appropriate.

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
- [Back to Kubernetes commands](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
