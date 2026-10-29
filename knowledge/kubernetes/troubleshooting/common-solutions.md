---
type: Troubleshooting Guide
title: Kubernetes common solutions
description: Choose the correct Kubernetes troubleshooting route from observed symptoms
  and collect a minimal safe evidence set.
tags:
- kubernetes
- troubleshooting
- triage
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: debug-pods
  title: Debug Pods
  resource: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
---

# Kubernetes common solutions

Use this as the entry point when a workload is unhealthy and the failing layer is unclear. Start with scope and evidence, then follow one focused guide. Repeated restarts or broad policy changes can erase the useful symptom without fixing its cause.

## Establish the scope

You need permission to inspect the intended namespace. Confirm whether the environment is local, staging, or production. Inspect one affected workload before listing or exporting an entire cluster.

```bash
kubectl config current-context
kubectl get pods -n <namespace> -o wide
kubectl get deploy,rs,sts,ds,job -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

What it does: confirms the target, workload/controller state, node placement, and recent namespace events. `describe` and events narrow the next diagnostic; events are temporary observations and not a durable audit trail.[^debug-pods]

Record when the failure began, the last relevant change, affected namespaces/nodes, image/revision, and whether all replicas or only some fail. Keep outputs private and redact sensitive arguments, environment values, and request data.

## Select a guide from evidence

| Symptom | First useful distinction | Focused guide |
| --- | --- | --- |
| Pod repeatedly exits | Which container and termination/probe reason? | [CrashLoopBackOff](crashloopbackoff.md) |
| Pod Pending / no new Pod | Unassigned, assigned but blocked, or rejected creation? | [Scheduling](pending-pods-and-scheduling.md) |
| ImagePullBackOff | Exact registry error before startup | [Image pulls](image-pull-failures.md) |
| Service cannot be reached | DNS, endpoint availability, application port, or network path? | [Service connectivity](service-connectivity.md) |
| Name lookup fails | Namespace/search suffix, resolver response, or upstream? | [DNS resolution](dns-resolution.md) |
| PVC Pending / failed mount | Binding, topology, attachment, mount, or permissions? | [Persistent volumes](persistent-volume-failures.md) |
| External route or certificate fails | Listener, route acceptance, reference, TLS, or backend? | [Gateway route and TLS](gateway-route-and-tls.md) |
| Deployment stalls | New ReplicaSet's admission, scheduling, or readiness? | [Rollout stalls](rollout-stalls.md) |
| APISIX-specific behavior | Controller, delivered gateway config, or backend? | [APISIX](apisix.md) |
| Local kind failure | Host runtime, selected context, cache, or node? | [kind](kind.md) |

## Separate API permissions from workload failure

```bash
kubectl auth can-i get pods -n <namespace>
kubectl auth can-i get pods --subresource=log -n <namespace>
kubectl auth can-i update deployments.apps -n <namespace>
```

What it does: asks whether the current Kubernetes identity may perform each operation. A denied log request is an inspection-permission issue, not evidence that the application produced no logs. Request the narrow permission needed rather than broad administrative access.

For EKS, use the [EKS deployment workflow](../../cross-topic-guides/deploying-to-eks.md) to distinguish AWS authentication, EKS access configuration, and Kubernetes authorization. A Pod's AWS identity is a separate concern; start with the [workload-identity comparison](../../cross-topic-guides/eks-workload-identity.md).

## Close the diagnosis

Capture a small redacted before/after record and fix the authoritative workload or platform configuration. Verify both recovery and the intended permission boundary. A green Pod phase, empty diff, or successful port-forward alone does not prove the user request succeeds. Remove temporary test resources, retain incident evidence privately, and add a regression check for the diagnosed failure where practical.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [kubectl basics](../commands/kubectl-basics.md).
- [Manifest validation and behavioral regression](../applications-and-tools/manifest-validation/index.md).
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^debug-pods]: [Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
