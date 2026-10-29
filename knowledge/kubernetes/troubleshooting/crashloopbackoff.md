---
type: Troubleshooting Guide
title: CrashLoopBackOff
description: Find the failing container, distinguish application exits from probe
  and memory failures, and verify a targeted recovery.
tags:
- kubernetes
- troubleshooting
- containers
- probes
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: pod-lifecycle
  title: Pod Lifecycle
  resource: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- id: probes
  title: Liveness, Readiness, and Startup Probes
  resource: https://kubernetes.io/docs/concepts/workloads/pods/probes/
---

# CrashLoopBackOff

Use this guide when a container repeatedly starts and exits. `CrashLoopBackOff` is a displayed waiting reason: restart attempts are delayed after repeated failures. It is not a Pod phase or a diagnosis of the application. A Pod can contain a healthy proxy and a failing application or init container.[^pod-lifecycle]

## Capture the failure before restarting anything

Confirm the cluster with `kubectl config current-context`. You need permission to inspect Pods, events, and container logs in the selected namespace. Logs may be absent after garbage collection or if the container never started.

```bash
kubectl get pod <pod> -n <namespace> -o wide
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> -c <container> --tail=100 --timestamps
kubectl logs <pod> -n <namespace> -c <container> --previous --tail=100 --timestamps
```

What it does: identifies the affected container and compares its current attempt with the preceding terminated instance. In `describe`, inspect both regular and init containers, `Last State`, termination reason, exit code, restart count, and events. `--previous` addresses one previous instance of that named container, not the Pod's entire history.

## Decide which evidence explains the restart

| Evidence | Next check | Recovery direction |
| --- | --- | --- |
| Application stack trace, missing file, bad argument | Image command/args and referenced ConfigMap or Secret keys | Correct the owning workload configuration or image. |
| Process exits successfully but restarts | Whether this is a batch program under an always-restarting controller | Use the intended Job/controller or keep the service process running. |
| `OOMKilled` | Memory limit, memory trend, node events, and workload demand | Fix leaks or size resources using measured headroom. Exit 137 alone does not prove OOM. |
| `Unhealthy` followed by kubelet killing the container | Which probe failed, its target, timeout, and failure budget | Correct the probe or startup allowance after measuring startup. |
| Init container fails | Its own previous logs and dependency/configuration | Resolve initialization before diagnosing the application. |

Readiness failures make the Pod unavailable for ordinary Service traffic; they do not themselves restart its container. Failed liveness or startup probes can cause a restart under the applicable restart policy. A configured startup probe gates liveness and readiness until it succeeds.[^probes]

For example, a healthy application needing 90 seconds to initialize can repeatedly die if its liveness check kills it first. Measure startup, then choose an appropriate startup-probe budget. Increasing every timeout can conceal a deadlock; a permanently unavailable dependency should not automatically make every replica restart together.

## Recover and verify

Capture the failing image, workload revision, and redacted error first. Update the Deployment/StatefulSet or its GitOps source, rather than editing an ephemeral Pod. If considering rollback, use the [rollout guide](rollout-stalls.md) to check revision and data compatibility before changing state.

Verify that the replacement container stays running across several probe intervals, restart count stops increasing, readiness succeeds, and a representative request works. A new Pod's restart count begins at zero, so inspect its uptime and behavior too. If restarts continue, compare the new termination evidence rather than repeatedly deleting Pods.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Image pull failures](image-pull-failures.md) — use when the process never starts.
- [Service connectivity](service-connectivity.md) — use when it runs but cannot serve traffic.
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^pod-lifecycle]: [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
[^probes]: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)
