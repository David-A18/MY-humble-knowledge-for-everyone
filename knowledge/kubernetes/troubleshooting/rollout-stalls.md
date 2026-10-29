---
type: Troubleshooting Guide
title: Deployment rollout stalls
description: Find why a new Deployment revision cannot become available and choose
  a safe fix or compatible rollback.
tags:
- kubernetes
- troubleshooting
- deployments
- rollout
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: deployments
  title: Deployments
  resource: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- id: deployment-api
  title: Deployment API
  resource: https://kubernetes.io/docs/reference/kubernetes-api/apps/deployment-v1/
---

# Deployment rollout stalls

Use this guide when a Deployment update waits indefinitely or reports `ProgressDeadlineExceeded`. Inspect the new ReplicaSet and its Pods instead of treating rollout status as the root cause. This guide covers Deployments; StatefulSets and progressive-delivery controllers have different update behavior.

## Capture revision and progress

Confirm context and namespace. Commands below are read-only, including the bounded status wait.

```bash
kubectl rollout status deployment/<deployment> -n <namespace> --timeout=30s
kubectl describe deployment <deployment> -n <namespace>
kubectl rollout history deployment/<deployment> -n <namespace>
kubectl get rs,pods -n <namespace> -l '<deployment-selector>' -o wide
```

What it does: checks observed rollout progress, controller conditions, retained revisions, and old versus new replicas. A client timeout means the local wait ended; it is different from the controller's progress deadline. The Deployment reports `ProgressDeadlineExceeded` but does not automatically roll back.[^deployments]

| Evidence in the new ReplicaSet/Pods | Route |
| --- | --- |
| `FailedCreate`; no new Pods | Admission, quota, LimitRange, policy, or permissions. |
| Unscheduled Pods | [Scheduling](pending-pods-and-scheduling.md), including surge capacity. |
| Images cannot start | [Image pulls](image-pull-failures.md). |
| Restarts / failed initialization | [CrashLoopBackOff](crashloopbackoff.md). |
| Running but not Ready | Readiness configuration, dependencies, application health, and readiness gates. |
| Ready but not yet available | `minReadySeconds`, readiness stability, and desired replica counts. |

Read the Deployment's actual strategy. `maxSurge` can require temporary extra capacity; `maxUnavailable` constrains availability during an update. Quota can reject the extra Pod before scheduling begins. A paused Deployment requires a deliberate resume decision. Do not simply increase the progress deadline to hide persistent failures.

## Choose a correction or rollback

Prefer fixing an understood configuration error in the source of truth. For GitOps, coordinate recovery with its reconciler; otherwise it may restore the failed revision immediately.

> [!WARNING]
> Rollback changes live application behavior. Confirm the target image still exists, its configuration is compatible, and database migrations or external side effects permit downgrade. Deployment history does not restore data or automatically version external ConfigMaps and Secrets.

After selecting a retained revision from history and obtaining the incident's normal change authorization:

```bash
kubectl rollout undo deployment/<deployment> -n <namespace> --to-revision=<known-good-revision>
kubectl rollout status deployment/<deployment> -n <namespace> --timeout=120s
```

What it does: restores the selected retained Pod template and waits for the resulting rollout. History retention is controlled by `revisionHistoryLimit`; an old revision may no longer be available.[^deployment-api] If rollback also stalls, diagnose its replacement Pods rather than issuing repeated undo commands.

## Verify application recovery

Confirm desired updated/available replicas, the actual image identity, readiness, and a representative read-only user request. Test the intended Service and gateway paths, and compare error rate and latency. `Available=True` alone does not prove the intended revision serves every request or that user behavior is correct.

Retain the redacted failure evidence and commit the durable correction to the authoritative source. Remove temporary debugging resources; do not delete old ReplicaSets manually just to make status look tidy.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Manifest differences and regression checks](../applications-and-tools/manifest-validation/index.md).
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^deployments]: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
[^deployment-api]: [Deployment API](https://kubernetes.io/docs/reference/kubernetes-api/apps/deployment-v1/)
