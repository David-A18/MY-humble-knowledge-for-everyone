# EKS tooling cluster architecture

## Purpose

Use this guide to design a dedicated EKS tooling cluster that supports workload clusters.

## Reference pattern

| Layer | Responsibility |
| --- | --- |
| Tooling cluster | Runs GitOps, observability, platform APIs, policy, and automation tools. |
| Workload clusters | Run product applications. |
| Git repositories | Store desired state and platform configuration. |
| AWS accounts | Separate platform, workload, and shared-services permissions. |
| Identity layer | Controls human and workload access to clusters and AWS APIs. |

## Design rules

- Treat the tooling cluster as highly privileged.
- Avoid granting one controller broad write access to every cluster unless the risk is accepted.
- Keep disaster recovery for platform tools separate from workload cluster recovery.
- Define which tools continue working if the tooling cluster is unavailable.
- Use separate namespaces, roles, and credentials for different platform functions.

## Related links

- [Tooling clusters](../kubernetes/applications-and-tools/tooling-clusters.md)
- [kind custom clusters](../kubernetes/applications-and-tools/kind-custom-clusters.md)
- [GitOps on EKS](gitops-on-eks.md)
- [EKS operations](eks-operations.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
