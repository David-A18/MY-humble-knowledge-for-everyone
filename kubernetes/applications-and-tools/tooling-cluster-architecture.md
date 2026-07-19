# Tooling cluster architecture

## Purpose

Use this guide to design a Kubernetes tooling cluster that hosts platform tools without accidentally creating a fragile, over-privileged control point.

## What a tooling cluster is

A tooling cluster is a cluster role, not a Kubernetes resource kind. It hosts shared platform tools such as GitOps controllers, observability systems, security scanners, CI runners, secret operators, and developer portals.

## Common patterns

| Pattern | Use when | Trade-off |
| --- | --- | --- |
| Tools and apps in one cluster | Small teams or early labs. | Simple but noisy and harder to isolate. |
| Dedicated tooling cluster | Platform tools need independent lifecycle. | More clusters to operate. |
| Hub-and-spoke management | One cluster manages many workload clusters. | Credentials and blast radius must be tightly controlled. |
| Decentralized GitOps | Each workload cluster reconciles itself. | Local failure isolation, but more controller instances. |
| Specialized platform clusters | Security, build, and observability have separate needs. | Strong isolation with higher cost and complexity. |

## What usually runs there

- Argo CD or Flux.
- Observability collectors, dashboards, and alerting.
- Policy and compliance controllers.
- External secret operators or secret sync tooling.
- CI/CD runners and build systems.
- Developer portals and platform APIs.
- Cluster lifecycle tools.

## Failure behavior

| If the tooling cluster fails | Usually continues | May stop or degrade |
| --- | --- | --- |
| Existing workload Pods | Running workloads keep running. | New deployments and reconciliations. |
| Existing cloud resources | Already-created resources remain. | Drift correction and automation. |
| Existing metrics pipelines | Local agents may buffer briefly. | Dashboards, alerts, and central storage. |
| Access workflows | Existing sessions may remain. | Break-glass or approval automation. |

## Security checklist

- Treat the tooling cluster as privileged infrastructure.
- Separate build permissions from deployment permissions.
- Scope workload-cluster credentials per cluster and purpose.
- Use namespace and network isolation for tenants.
- Protect Git, registry, and cloud credentials.
- Keep audit logs for reconciliations and administrative actions.
- Test restore order before a real incident.

## EKS account model

```text
platform-tools account
  -> tooling EKS cluster
  -> GitOps and observability

workload account A
  -> workload EKS cluster

workload account B
  -> workload EKS cluster
```

What it does: separates the platform tooling plane from workload accounts while still allowing controlled cross-account access.

## Related links

- [Tooling clusters](tooling-clusters.md)
- [EKS tooling cluster architecture](../../cross-topic-guides/eks-tooling-cluster-architecture.md)
- [GitOps security and multi-tenancy](gitops-security-and-multitenancy.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
