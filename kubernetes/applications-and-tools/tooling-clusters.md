# Tooling clusters

## Purpose

Use this page to decide when a dedicated Kubernetes tooling cluster is useful.

## What a tooling cluster is

A tooling cluster is a cluster role, not a Kubernetes resource type. It runs platform tools that manage, observe, secure, or deploy to workload clusters.

## Common workloads

| Tool category | Examples | Risk to manage |
| --- | --- | --- |
| GitOps | Argo CD, Flux | Excessive privileges into workload clusters. |
| Observability | Metrics, logs, traces, dashboards | Central outage hides workload signals. |
| Security | Policy, scanning, secret controllers | Credential blast radius. |
| Platform lifecycle | Crossplane, Cluster API, internal portals | Self-destruction and broad control-plane access. |

## Decision guide

- Use a dedicated tooling cluster when many workload clusters need shared platform services.
- Keep tools in workload clusters for simpler environments or early learning.
- Treat the tooling cluster as privileged infrastructure with strong access control and disaster recovery.

## Related links

- [kind custom clusters](kind-custom-clusters.md)
- [EKS tooling cluster architecture](../../cross-topic-guides/eks-tooling-cluster-architecture.md)
- [Kubernetes best practices](../best-practices/README.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
