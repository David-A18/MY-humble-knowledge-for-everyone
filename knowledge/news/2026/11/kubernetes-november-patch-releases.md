---
type: News Brief
title: Kubernetes publishes November patches for 1.35 through 1.37
description: Upstream Kubernetes released three patch versions on 25 November 2026.
tags: [news, kubernetes, platform-engineering]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
published: 2026-11-26
stale_after: 2027-02-26
sources:
  - id: patch-137
    resource: https://github.com/kubernetes/kubernetes/releases/tag/v1.37.3
    title: Kubernetes 1.37.3 release
  - id: patch-136
    resource: https://github.com/kubernetes/kubernetes/releases/tag/v1.36.7
    title: Kubernetes 1.36.7 release
  - id: patch-135
    resource: https://github.com/kubernetes/kubernetes/releases/tag/v1.35.11
    title: Kubernetes 1.35.11 release
---

# Kubernetes publishes November patches for 1.35 through 1.37

## What happened

The Kubernetes project published 1.37.3, 1.36.7, and 1.35.11 on 25 November
2026. Each release is a patch for its own minor version and links to that
version's detailed changelog.[^patch-137][^patch-136][^patch-135]

## Why it matters

Operators can review the patch for their current minor series while preparing
for a future minor upgrade. Managed Kubernetes operators should check the
provider's own release notes for the platform version and rollout timing.

## What to do

Record the server and node versions, then read the changelog for the matching
minor series. If your distribution offers the patch, test it in staging and
check node readiness, representative workloads, and any components affected
by the release before rolling it out.

## Related links

- [Plan a Kubernetes minor upgrade](../../../kubernetes/plan-a-minor-upgrade.md)
- [November 2026](index.md)
- [News](../../index.md)
- [Knowledge home](../../../index.md)

[^patch-137]: [Kubernetes 1.37.3 release](https://github.com/kubernetes/kubernetes/releases/tag/v1.37.3)
[^patch-136]: [Kubernetes 1.36.7 release](https://github.com/kubernetes/kubernetes/releases/tag/v1.36.7)
[^patch-135]: [Kubernetes 1.35.11 release](https://github.com/kubernetes/kubernetes/releases/tag/v1.35.11)
