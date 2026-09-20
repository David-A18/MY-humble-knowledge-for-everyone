---
type: How-to Guide
title: kubectl basics
description: Inspect the current Kubernetes context, workloads, logs, events, and resource details safely before making changes.
tags: [kubernetes, kubectl, troubleshooting, beginner]
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
  - id: kubectl-reference
    resource: https://kubernetes.io/docs/reference/kubectl/
    title: kubectl command overview
  - id: kubectl-commands
    resource: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands
    title: kubectl command reference
stale_after: 2026-12-20
---

# kubectl basics

## Purpose

Inspect a Kubernetes cluster and its workloads safely before applying, deleting, or changing resources. These commands are read-only unless stated otherwise.

## Prerequisites

- `kubectl` is installed and can reach the intended cluster.
- You know the target namespace, or you have permission to list namespaces.
- You have confirmed whether the cluster is local, sandbox, staging, or production.

## Confirm the target first

```bash
kubectl config current-context
kubectl get namespaces
kubectl auth can-i get pods --all-namespaces
```

What it does: shows the active cluster context, lists namespaces, and checks whether the current identity can read Pods across namespaces.

Expected result: the context and namespace match the environment you intend to inspect. Stop before running mutating commands if they do not.

> [!WARNING]
> A valid `kubectl` command can still target the wrong cluster. Always inspect the context before applying, deleting, scaling, or restarting a workload.

## Inspect a workload

```bash
kubectl get pods -n <namespace> -o wide
kubectl get deployment <deployment-name> -n <namespace>
kubectl describe deployment <deployment-name> -n <namespace>
```

What it does: lists Pod readiness and placement, reads the Deployment's desired state, and shows conditions, events, and recent rollout information.

Expected result: healthy Pods show `Running` and their containers are ready. A Deployment reports available replicas when the rollout has succeeded.

## Read logs and events

```bash
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl logs <pod-name> -n <namespace> --previous --tail=100
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

What it does: reads current container logs, logs from the prior container instance after a restart, and the namespace event stream in chronological order.

Expected result: use logs for application errors and events for scheduling, image-pull, volume, probe, and controller messages.

If a Pod has more than one container, add `-c <container-name>` after the Pod name. Use `kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].name}'` to list container names.

## Inspect one Pod in detail

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get pod <pod-name> -n <namespace> -o yaml
```

What it does: `describe` summarizes state and related events; YAML shows the declared and observed resource details.

Use the output to distinguish a scheduling problem, image-pull failure, failed probe, permission issue, or application error before attempting a recovery.

## Next step

- For a repeatable symptom-based sequence, use [CrashLoopBackOff](../troubleshooting/crashloopbackoff.md) or [common Kubernetes solutions](../troubleshooting/common-solutions.md).
- For a safe local practice environment, use the [local deployment learning path](../../cross-topic-guides/local-deployment-learning-path.md).

## Related links

- [kubectl command overview](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes troubleshooting](../troubleshooting/index.md)
- [Kubernetes workflows](workflows.md)
- [Back to Kubernetes commands](index.md)
- [Back to Kubernetes index](../index.md)
- [Back to knowledge index](../../index.md)
