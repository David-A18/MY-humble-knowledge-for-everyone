# Kubernetes fundamentals

Status: Draft
Audience: Beginning platform engineer
Page type: Explanation
Maintainer: Unassigned
Last substantive review: 2026-09-18
Applicable versions: Kubernetes v1.37.0 client used for attempted local validation; concepts apply to stable Namespace, Pod, Deployment, Service, label, and reconciliation behavior
Validation evidence: Source reviewed and statically checked; local exercise execution is tracked in the linked learning path and currently blocked by unavailable Docker daemon
Known limitations: This page introduces concepts and does not replace the full Kubernetes documentation
Next review: After the first completed local learning-path run

Core Kubernetes concepts and operational mental models.

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

[Back to Kubernetes index](../README.md) | [Back to root index](../../README.md)
