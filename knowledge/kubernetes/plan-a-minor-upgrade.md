---
type: How-to Guide
title: Plan a Kubernetes minor upgrade
description: Build a staging checklist for a Kubernetes minor upgrade and decide when production rollout can proceed.
tags: [kubernetes, upgrades, platform-engineering]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: version-skew
    resource: https://kubernetes.io/releases/version-skew-policy/
    title: Kubernetes version skew policy
  - id: api-migration
    resource: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
    title: Kubernetes deprecated API migration guide
  - id: api-deprecation
    resource: https://kubernetes.io/docs/reference/deprecation-policy/
    title: Kubernetes API deprecation policy
---

# Plan a Kubernetes minor upgrade

Make a checklist for the target version, then run it against a staging cluster
before touching production. For example, if a deployment uses an old API
version, update the source manifest or chart and confirm the new version works
before the upgrade removes the old API.

## Record what runs today

- Record the control plane version, each node pool's kubelet and container
  runtime versions, and the `kubectl` version used by CI.
- Inventory add-ons and webhooks, including DNS, networking, storage, ingress
  and admission. Record the versions supported by their maintainers for the
  target Kubernetes minor.
- Check the distribution's upgrade sequence alongside the upstream component
  version skew rules, which describe how far versions may differ during
  an upgrade.[^version-skew]

### Collect a staging baseline

Set `STAGING_CONTEXT` to the kubeconfig context for the intended staging
cluster. Use credentials that can read the server version and list nodes.

```bash
kubectl --context "$STAGING_CONTEXT" version -o yaml
kubectl --context "$STAGING_CONTEXT" get nodes -o custom-columns='NAME:.metadata.name,KUBELET:.status.nodeInfo.kubeletVersion,RUNTIME:.status.nodeInfo.containerRuntimeVersion'
```

What it does: records the client and server versions and lists the kubelet and
container runtime version of each visible node. Compare all node pools because
a partial rollout can leave pools at different versions. Run the client version
check from your deployment job as well if it uses a different kubectl binary.

## Check what the target version changes

Read the release notes for each minor version on your upgrade path. Compare the
deprecated API migration guide against rendered Helm charts, GitOps manifests
and API clients. A cluster may still return a resource through a supported API
even when a chart or client continues to send requests to an older version.
Check both the desired configuration and the clients that run in
practice.[^api-migration]

### Check what clients actually request

Where API server metrics are available, check which deprecated resources have
been requested and read the `removed_release` label. This example uses 1.32
to match the compatibility exercise below. Use the release you are assessing
and scope the query to the intended cluster.[^api-deprecation]

```promql
apiserver_requested_deprecated_apis{removed_release="1.32"} == 1
```

What it does: shows matching deprecated API endpoints observed by the
instrumented API server processes. This gauge does not count requests or
identify the caller. Use available audit events to identify the requesting
identity, and check the owner of the controller, job, or deployment pipeline.
A quiet result is inconclusive when metrics are unavailable, API servers have
restarted, or scheduled workloads have yet to run. Review rendered manifests
and exercise those workloads before treating the inventory as complete.

## Decide whether to proceed

Run the same checks before and after upgrading staging. Use representative
workloads and the versions you plan to use in production.

| Check | Evidence to record |
| --- | --- |
| Nodes and scheduling | The upgraded nodes become Ready and a representative workload starts on them. |
| Network and DNS | An application resolves a Service name and reaches the expected backend. |
| Storage | A test workload can mount its volume and read a known test record. |
| Admission and delivery | The normal deployment pipeline creates or updates a workload and required policies still apply. |

If a required check fails, pause before upgrading production. Capture the
first failing operation, compare it with the baseline and rerun after fixing
the dependency. Before production rollout, identify the recovery path supported
by your distribution and record who can pause the rollout. For example, a
provider may let you replace a node pool while offering a different recovery
path for the control plane.

## Rehearse a removed API

Run the [disposable compatibility exercise](../../examples/kubernetes/minor-upgrade-rehearsal/README.md) against Kubernetes 1.31 and 1.32. The example uses FlowSchema, an API server request-classification resource. A legacy client using `v1beta3` works on the baseline and receives NotFound on the target. Switching the request to `v1` restores it. Use the same pattern to test any API clients identified in your inventory.[^api-migration]

## Related links

- [Manifest validation and regressions](applications-and-tools/manifest-validation/index.md)
- [Kubernetes backup and recovery with Velero](../migrations/velero/index.md)
- [Kubernetes index](index.md)
- [Knowledge home](../index.md)

[^version-skew]: [Kubernetes version skew policy](https://kubernetes.io/releases/version-skew-policy/)
[^api-migration]: [Kubernetes deprecated API migration guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)
[^api-deprecation]: [Kubernetes API deprecation policy](https://kubernetes.io/docs/reference/deprecation-policy/)
