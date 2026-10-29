---
type: Troubleshooting Guide
title: Pending Pods and scheduling failures
description: Determine whether a Pod is unscheduled, blocked after assignment, or
  absent because admission rejected its creation.
tags:
- kubernetes
- troubleshooting
- scheduling
- resources
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: pod-lifecycle
  title: Pod Lifecycle
  resource: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- id: debug-pods
  title: Debug Pods
  resource: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
- id: assign-pods
  title: Assigning Pods to Nodes
  resource: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
- id: storage-classes
  title: Storage Classes
  resource: https://kubernetes.io/docs/concepts/storage/storage-classes/
---

# Pending Pods and scheduling failures

`Pending` is broader than a scheduler failure: a Pod may be waiting for node assignment or for containers to be prepared after assignment. First determine whether a Pod exists and whether it has a node. Scheduling fixes cannot solve a bad image or a failed volume mount.[^pod-lifecycle]

## Classify the wait

Confirm context and namespace. The examples inspect an existing workload; use its actual controller type.

```bash
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl describe deployment <deployment> -n <namespace>
kubectl get resourcequota,limitrange -n <namespace>
```

What it does: checks node assignment, `PodScheduled`, scheduler/kubelet events, controller creation errors, and namespace admission constraints. If a Deployment has no Pod, inspect its ReplicaSet events too. Quota or admission rejection can prevent creation altogether; there may be no Pending Pod to inspect.

| Evidence | Correct next route |
| --- | --- |
| No node; `FailedScheduling` | Read the complete event message and evaluate eligible nodes. |
| Node assigned; `FailedMount` or `FailedAttachVolume` | [Persistent-volume failures](persistent-volume-failures.md). |
| Node assigned; `ErrImagePull` | [Image pull failures](image-pull-failures.md). |
| Init container waiting or failing | Its state/logs and initialization dependencies. |
| No Pod; controller reports `FailedCreate` | Admission policy, quota, LimitRange, or controller permissions. |

## Explain why no eligible node exists

```bash
kubectl get nodes -o wide --show-labels
kubectl describe node <candidate-node>
kubectl get pod <pod> -n <namespace> -o yaml
```

What it does: compares node readiness, allocatable resources, existing requests, taints, and Pod placement requirements. `Insufficient cpu` or memory concerns scheduling requests and allocatable capacity; low instantaneous usage is not proof that another requested workload fits.[^debug-pods]

Hard node selectors and required affinity exclude nodes. Tolerations permit a tainted node to be considered but do not guarantee placement; preferred affinity is a preference rather than a hard requirement.[^assign-pods] For example, a Pod requiring a GPU node pool will not fit a new general-purpose node merely because that node has free memory.

When PVCs use `WaitForFirstConsumer`, binding depends on a schedulable consuming Pod and compatible storage topology. Setting `spec.nodeName` bypasses the scheduler and can leave that claim waiting; express placement through supported scheduling constraints instead.[^storage-classes]

## Recover and verify

Choose capacity, requests, or placement changes from the event evidence and workload requirements. Do not lower requests below measured needs simply to clear the queue. Do not add broad tolerations for control-plane or unhealthy nodes. Autoscaling helps only when it can create an eligible node within quotas and pool limits.

After a reviewed change in the owning source, expect node assignment and `PodScheduled=True`, then successful initialization and readiness. A scheduled Pod is only an intermediate result. These read-only checks require no cleanup; revert temporary placement experiments in the source of truth.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Rollout stalls](rollout-stalls.md) — diagnose admission and surge capacity during an update.
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^pod-lifecycle]: [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
[^debug-pods]: [Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
[^assign-pods]: [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
[^storage-classes]: [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
