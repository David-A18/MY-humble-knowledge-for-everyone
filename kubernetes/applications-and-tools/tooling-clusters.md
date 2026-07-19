# Tooling clusters

## Purpose

Use this page to decide when a dedicated Kubernetes tooling cluster is useful.

## What it does

A tooling cluster centralizes platform tools that support other clusters. It can run deployment controllers, observability systems, security tooling, secret synchronization, CI runners, developer portals, and cluster lifecycle automation.

The value is operational separation: platform tools can have their own lifecycle, permissions, monitoring, and capacity instead of competing directly with application workloads.

## What a tooling cluster is

A tooling cluster is a cluster role, not a Kubernetes resource type. It runs platform tools that manage, observe, secure, or deploy to workload clusters.

## How it works

```text
tooling cluster
  -> reads Git and registries
  -> talks to workload-cluster APIs
  -> collects telemetry
  -> applies policy or deployment changes
```

The tooling cluster is privileged because it may hold credentials to many other environments.

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

## Components to plan

- Cluster access credentials for every managed workload cluster.
- Namespace and RBAC boundaries for platform teams and tenants.
- Backup and restore for stateful platform tools.
- Network paths from tooling to workload cluster APIs.
- Observability for the tooling cluster itself.
- Break-glass process if GitOps or identity tooling fails.

## Related links

- [Tooling cluster architecture](tooling-cluster-architecture.md)
- [kind custom clusters](kind-custom-clusters.md)
- [EKS tooling cluster architecture](../../cross-topic-guides/eks-tooling-cluster-architecture.md)
- [Kubernetes best practices](../best-practices/README.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
