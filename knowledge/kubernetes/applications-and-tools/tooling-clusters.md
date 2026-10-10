---
type: Explanation
title: When a tooling cluster helps
description: Choose where to run shared Kubernetes platform tools by following their users, permissions, and failure dependencies.
tags: [kubernetes, platform-engineering, tooling-clusters, beginner]
status: draft
maturity: draft
audience: Beginning platform and application teams
maintainer: unassigned
sources:
  - id: argo-clusters
    resource: https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-management/
    title: Argo CD - Cluster Management
  - id: argo-getting-started
    resource: https://argo-cd.readthedocs.io/en/stable/getting_started/
    title: Argo CD - Getting Started
  - id: argo-projects
    resource: https://argo-cd.readthedocs.io/en/stable/user-guide/projects/
    title: Argo CD - Projects
  - id: flux-remote
    resource: https://fluxcd.io/flux/components/kustomize/kustomizations/
    title: Flux - Kustomization and remote clusters
  - id: kubernetes-rbac
    resource: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
    title: Kubernetes - Using RBAC Authorization
  - id: kubernetes-network-policy
    resource: https://kubernetes.io/docs/concepts/services-networking/network-policies/
    title: Kubernetes - Network Policies
  - id: kubernetes-policy
    resource: https://kubernetes.io/docs/concepts/policy/
    title: Kubernetes - Policies
  - id: external-secrets
    resource: https://external-secrets.io/latest/introduction/overview/
    title: External Secrets Operator - Overview
---

# When a tooling cluster helps

## The idea in one minute

A **tooling cluster** is a normal Kubernetes cluster used mainly for
platform services that help other clusters: for example, a deployment
controller, a central dashboard, or a build service. The name describes
its *job*, not a special Kubernetes resource. A workload cluster runs
applications for their users. A team can put platform tools in each
workload cluster, share them from a separate cluster, or mix the two.

Think of a workshop shared by several buildings. One workshop can
serve them all, but it needs routes and keys to enter each building.
The analogy stops there: a GitOps controller does not carry user
requests between clusters; it makes API requests to change their
configuration. The choice is about **who operates a tool, what it can
reach, and what stops when it fails**.[^argo-clusters][^flux-remote]

## Start with one concrete service

Suppose an invented learning platform has two application clusters,
`courses` and `practice`. It wants one GitOps service to deploy both.
These are design options, not configurations tested in this repository.

| Placement | What the controller can do | What the team takes on |
| --- | --- | --- |
| One controller inside each application cluster | Reconcile its local cluster. | Operate and upgrade two installations; a local outage can affect that cluster's deployments. |
| One controller in a separate tooling cluster | Reach each target Kubernetes API if network access, authentication, and permission are configured. | Operate a third cluster; protect credentials and recover a service whose outage can delay deployments to both targets. |
| One controller in an existing application cluster | Potentially reach both targets with the same access setup. | Share capacity and failure fate with the host application cluster. |
| Local reconcilers with a shared interface, where supported | Keep each target's reconciliation local while sharing some visibility or source management. | Operate local controllers and the shared service; verify that the chosen product actually supports this layout. |
| External managed service for a specific function | Avoid hosting that function in a new cluster. | Check its permissions, availability, cost, and recovery contract instead. |

Argo CD supports external clusters, and Flux Kustomizations can target
remote clusters. The product name alone does not establish what a
controller can change. Its target credentials and the target cluster's
authorization determine that. For example, the usual `argocd cluster
add` path installs an admin-level target ClusterRole; an Argo CD
Project restriction does not narrow that Kubernetes credential.
[^argo-clusters][^argo-getting-started][^argo-projects][^flux-remote]

A third cluster is useful when the team has a real reason to operate
shared services separately: independent upgrades, capacity, ownership,
or access controls for several targets. It also creates another
cluster to maintain. For a small learning setup with one target,
local tooling may be easier to understand and recover.

Placement also differs **by function**. Admission decisions must be
enforced by each target's API server, even if a central service
distributes policy definitions. A secret-sync controller such as
External Secrets Operator ordinarily runs where it creates Kubernetes
Secrets and reads an external secret store. Telemetry agents can run
near workloads and send data to a shared backend. A dashboard or
long-term telemetry store is easier to centralize. Untrusted CI jobs
need a boundary from credentials that can deploy across clusters.
These are design patterns to evaluate, not a requirement to put every
tool in one place.[^kubernetes-policy][^external-secrets]

## Ask three questions before choosing

1. **Who depends on it?** Name the specific services and target
   clusters. A central GitOps controller serves deployment and drift
   repair; it need not sit on the path of an existing user's request.
   A central runtime dependency, such as a remote secret service, could
   affect those requests. Trace each service separately.
2. **What authority does it gain?** For each target, list the API
   endpoint, network path, authentication method, and allowed actions.
   Kubernetes RBAC can scope an identity's API permissions. A namespace
   or network boundary by itself does not grant or remove all of those
   permissions.[^kubernetes-rbac][^kubernetes-network-policy]
3. **What happens when it disappears?** Decide how the team will make
   an urgent change, see application health, and rebuild the shared
   service if the tooling cluster is unavailable. Existing Pods may
   continue if their own clusters and required dependencies remain
   healthy; this is a conditional design expectation, not an outage
   result.

There is no useful cluster-count threshold by itself. The decision
becomes stronger when the team can name a separate recovery owner,
independent monitoring need, target access plan, and acceptable extra
operating cost. If those are unclear, first improve the existing
cluster's isolation and recovery procedure, then revisit placement.

> [!NOTE]
> A separate cluster does not automatically provide strong isolation.
> A shared controller with broad target credentials can affect more
> applications than either local controller. Review the effective
> identity and the source that the controller trusts.

## Choose a first step

For the invented two-cluster example, start by drawing the current
source-to-controller-to-API path and the user-to-application path. If
independent operation is worth the extra cluster, design one bounded
management connection per target and a way to recover the controller.
If it is not, keep local controllers and revisit the choice when a
specific shared-service need appears. Neither choice requires moving
all observability, policy, secrets, and build jobs to the same place.

[Tooling cluster architecture](tooling-cluster-architecture.md) traces
the connections and outage paths in more detail. The
[EKS tooling cluster example](../../cross-topic-guides/eks-tooling-cluster-architecture.md)
applies the same reasoning to Amazon EKS.

## Check your understanding

1. Why does placing GitOps in another cluster add a target API connection?
2. Could existing application traffic continue while central GitOps is
   down? What dependency might change that answer?
3. What new operational responsibility comes with a third cluster?

## Deeper study

- [Argo CD cluster management](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-management/)
  and [Flux remote Kustomizations](https://fluxcd.io/flux/components/kustomize/kustomizations/)
  show two documented ways to manage external targets.
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
  and [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
  explain separate permission and network controls.
- [GitOps security and multi-tenancy](gitops-security-and-multitenancy.md)
  follows source writers, controller identity, and Kubernetes authority.

[Back to Kubernetes applications and tools](index.md)

[^argo-clusters]: [Argo CD - Cluster Management](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-management/).
[^argo-getting-started]: [Argo CD - Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/).
[^argo-projects]: [Argo CD - Projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/).
[^flux-remote]: [Flux - Kustomization and remote clusters](https://fluxcd.io/flux/components/kustomize/kustomizations/).
[^kubernetes-rbac]: [Kubernetes - Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/).
[^kubernetes-network-policy]: [Kubernetes - Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
[^kubernetes-policy]: [Kubernetes - Policies](https://kubernetes.io/docs/concepts/policy/).
[^external-secrets]: [External Secrets Operator - Overview](https://external-secrets.io/latest/introduction/overview/).
