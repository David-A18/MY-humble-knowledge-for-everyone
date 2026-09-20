---
type: Explanation
title: Kubernetes fundamentals
description: Learn the cluster, Namespace, Pod, Deployment, Service, label, and reconciliation concepts used in the local learning path.
tags: [kubernetes, fundamentals, beginner]
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
  - id: kubernetes-concepts
    resource: https://kubernetes.io/docs/concepts/
    title: Kubernetes Concepts
  - id: kubernetes-workloads
    resource: https://kubernetes.io/docs/concepts/workloads/
    title: Kubernetes workloads
stale_after: 2026-12-19
---

# Kubernetes fundamentals

## Purpose

Learn the Kubernetes mental model needed to complete the local deployment learning path and to understand the operational guides in this knowledge base.

## Core ideas

| Concept | What it means | Why it matters |
| --- | --- | --- |
| Cluster | A set of machines or local containers running the Kubernetes control plane and worker components. | It is the boundary where workloads are scheduled and operated. |
| Namespace | A named scope for resources. | It keeps the first exercise isolated and makes cleanup safer. |
| Pod | One or more containers scheduled together. | It is the smallest workload unit you usually inspect during failures. |
| Deployment | Desired state for replicated Pods and rolling updates. | It creates and replaces Pods for you through ReplicaSets. |
| Service | Stable network endpoint for a set of Pods. | Pods change names and IPs; Services give clients a stable target. |
| Label | Key-value metadata attached to resources. | Services and commands use labels to select the right objects. |
| Reconciliation | The control loop that compares desired state with actual state. | Kubernetes keeps trying to make actual resources match the manifests. |

## First local exercise

Start with [Start here](../../start-here.md), then complete the [local deployment learning path](../../cross-topic-guides/local-deployment-learning-path.md). That path creates a local cluster, deploys a small app, breaks it with a bad image tag, diagnoses the failure, rolls back, and cleans up.

## Related links

- [Kubernetes concepts](https://kubernetes.io/docs/concepts/)
- [Local deployment learning path](../../cross-topic-guides/local-deployment-learning-path.md)
- [Kubernetes commands](../commands/index.md)
- [Back to Kubernetes fundamentals](index.md)
- [Back to Kubernetes index](../index.md)
- [Back to knowledge index](../../index.md)
