---
type: How-to Guide
title: eksctl commands for Fargate, Auto Mode, and networking
description: Configure Fargate profiles, EKS Auto Mode and Karpenter, endpoint access, and control plane logging with eksctl.
tags: [kubernetes, eksctl-commands, eks, networking]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# eksctl commands for Fargate, Auto Mode, and networking

These commands choose where EKS pods run and how the cluster endpoint and logs are configured. It is part of [eksctl commands for Amazon EKS](eksctl-commands.md).

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

## Related links

- [eksctl commands for Amazon EKS](eksctl-commands.md)
- [Back to index](index.md)
