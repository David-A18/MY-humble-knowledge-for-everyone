---
type: How-to Guide
title: eksctl commands for EKS access and workload permissions
description: Grant people cluster access with access entries or legacy aws-auth, and give pods AWS permissions with Pod Identity or IRSA, using eksctl.
tags: [kubernetes, eksctl-commands, eks, iam]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# eksctl commands for EKS access and workload permissions

These commands control who can reach an EKS cluster and which AWS permissions its pods receive. It is part of [eksctl commands for Amazon EKS](eksctl-commands.md).

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

## Related links

- [eksctl commands for Amazon EKS](eksctl-commands.md)
- [Back to index](index.md)
