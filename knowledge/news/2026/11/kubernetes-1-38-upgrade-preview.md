---
type: News Brief
title: Kubernetes 1.38 preview flags node and kubectl changes
description: The release team outlines runtime and client changes operators can test before the planned December release.
tags: [news, kubernetes, platform-engineering]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
published: 2026-11-25
stale_after: 2027-02-25
sources:
  - id: announcement
    resource: https://kubernetes.io/blog/2026/11/23/kubernetes-v1-38-sneak-peek/
    title: Kubernetes 1.38 release preview
---

# Kubernetes 1.38 preview flags node and kubectl changes

## What happened

On 23 November 2026, the Kubernetes release team shared a preview of v1.38,
with a target release date of 16 December. The preview describes changes that
may still shift before release.[^announcement]

## Why it matters

The preview says kubelet will expect the container runtime to report the
cgroup driver by default. The driver controls how Linux groups and limits
process resources. An older runtime that cannot answer that request can
prevent a node from joining. The release also plans to remove two environment
variables that let operators opt out of trying WebSockets first for commands
such as `kubectl exec` and `kubectl port-forward`.[^announcement]

## What to do

Record the runtime version on each node pool and check automation for
`KUBECTL_REMOTE_COMMAND_WEBSOCKETS` and `KUBECTL_PORT_FORWARD_WEBSOCKETS`.
When your distribution makes the release available, confirm the final release
notes and test node registration and remote commands through your usual
network path in staging.

## Related links

- [Plan a Kubernetes minor upgrade](../../../kubernetes/plan-a-minor-upgrade.md)
- [November 2026](index.md)
- [News](../../index.md)
- [Knowledge home](../../../index.md)

[^announcement]: [Kubernetes 1.38 release preview](https://kubernetes.io/blog/2026/11/23/kubernetes-v1-38-sneak-peek/)
