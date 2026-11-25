---
type: News Brief
title: Amazon EKS 1.31 reaches the end of extended support
description: AWS lists 26 November 2026 as the end of extended support for Kubernetes 1.31 on EKS.
tags: [news, aws, eks, kubernetes]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
published: 2026-11-25
stale_after: 2027-02-25
sources:
  - id: eks-lifecycle
    resource: https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html
    title: Amazon EKS Kubernetes version lifecycle
---

# Amazon EKS 1.31 reaches the end of extended support

## What happened

AWS lists 26 November 2026 as the end of extended support for Kubernetes
1.31 on Amazon EKS. That date applies to the EKS lifecycle.[^eks-lifecycle]

## Why it matters

AWS can automatically upgrade the control plane after extended support
ends. Operators of remaining 1.31 clusters should check node groups and
add-ons separately because those components have their own upgrade
steps.[^eks-lifecycle]

## What to do

Check the control plane version in each account and Region you operate. For
clusters still on 1.31, review upgrade insights, confirm add-on compatibility,
and schedule the remaining node and workload checks with the owning team.

## Related links

- [Plan a Kubernetes minor upgrade](../../../kubernetes/plan-a-minor-upgrade.md)
- [November 2026](index.md)
- [News](../../index.md)
- [Knowledge home](../../../index.md)

[^eks-lifecycle]: [Amazon EKS Kubernetes version lifecycle](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html)
