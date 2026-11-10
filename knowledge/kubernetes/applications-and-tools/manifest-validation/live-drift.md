---
type: Explanation
title: Detect desired-versus-live Kubernetes drift
description: Compare the prospective apply result with live state and interpret reconciliation
  ownership.
tags:
- kubernetes
- manifest-validation
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: kubectl-diff-contract
  resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/
  title: kubectl diff contract
- id: server-side-apply
  resource: https://kubernetes.io/docs/reference/using-api/server-side-apply/
  title: Server-side apply
- id: argo-cd-diff-customization
  resource: https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/
  title: Argo CD diff customization
- id: kubectl-134-source
  resource: https://raw.githubusercontent.com/kubernetes/kubectl/v0.34.1/pkg/cmd/diff/diff.go
  title: kubectl 1.34.1 external diff command implementation
---

# Detect desired-versus-live Kubernetes drift

Establish the intended revision, cluster, namespace and field owner before comparing live state. A live export contains server defaults, allocated fields, controller changes and status; a raw export-versus-Git patch does not automatically identify an operational problem.

## What the API comparison does

`kubectl diff` compares the current online configuration with the prospective applied configuration. Server-side mode exercises the API server's apply/dry-run path, including applicable admission and field ownership, without persisting the proposed object. It needs the relevant permissions; it is not an offline parser or a data-plane test.[^kubectl-diff-contract][^server-side-apply]

```bash
kubectl --context "$CONTEXT" --namespace "$NAMESPACE" diff --server-side --field-manager=release-manager -f desired.yaml
```

What it does: compares one explicitly selected environment using an intentional field-manager name. Replace the placeholders with the application's verified context, namespace, manager and rendered file. Use the same ownership model as the actual release process; do not invent a new manager merely to avoid a conflict.

## Handle all three outcomes

In a Bash CI step with error handling enabled:

```bash
result=0
kubectl --context "$CONTEXT" --namespace "$NAMESPACE" diff --server-side --field-manager=release-manager -f desired.yaml || result=$?
case "$result" in
  0) echo "No differences" ;;
  1) echo "Differences need review" ;;
  *) echo "Comparison failed with status $result" >&2; exit "$result" ;;
esac
```

What it does: handles the documented no-difference 0, difference 1 and error >1 contract without swallowing errors with `|| true`. This example reports an intentional difference; a release gate may deliberately reject status 1 after labeling it correctly. Inspect diagnostics when a result is unexpected.[^kubectl-diff-contract]

The lab checks actual baseline/reordered status 0 and changed-port status 1. It deliberately runs a failing external diff process to test the >1 branch; that is an external comparison failure, not an authentication test. `KUBECTL_EXTERNAL_DIFF` must itself follow kubectl's status convention. For dyff, include `between --set-exit-code`; a pretty-printer that always exits 0 would hide changes.[^kubectl-diff-contract]

## Use an executable wrapper for external commands

The pinned kubectl 1.34.1 splits `KUBECTL_EXTERNAL_DIFF` itself and restricts/reorders extra arguments; it does not evaluate shell quoting or a general command line. Passing `python /path/to/script.py` is not a portable way to invoke a custom comparator. Use an executable wrapper and set the variable to its single executable path, without spaces.[^kubectl-134-source]

```sh
#!/usr/bin/env sh
exec dyff between --omit-header --set-exit-code "$@"
```

What it does: an executable wrapper supplies dyff's command/flags itself, while preserving kubectl's two input-directory arguments. Save it in a task-owned path, make it executable, and assign that path to `KUBECTL_EXTERNAL_DIFF`. Check the pinned tools' behavior before adopting a different comparator. The lab uses its own executable wrapper returning 7 to exercise comparison-error handling; it does not execute this dyff wrapper integration.

## Interpret defaults and ownership

| Difference | Investigation |
| --- | --- |
| Status/resource version/managed fields in a raw export | These describe server state; compare the prospective object rather than blindly copying export metadata into Git. |
| Allocated Service address or admission-injected field | Identify the allocator/webhook and whether the desired file intentionally owns the field. |
| HPA-controlled replicas | Establish the autoscaler's ownership and the GitOps controller's documented narrow ignore behavior. |
| Apply conflict | Inspect field ownership and the release contract; do not automatically add `--force-conflicts`. |
| Image, selector, port, RBAC or storage difference | Review impact and run behavior/security checks; do not normalize away the evidence. |

A clean diff does not prove correct behavior: the lab deliberately makes live state equal to a broken Service file. Likewise, diffing only one file does not prove that every obsolete object will be pruned. Inventory/deletion policy and reconciliation ownership need their own review.

## Use the existing GitOps controller

Argo CD supports diff customizations; narrowly document the owner and field before ignoring it. Flux reconciliation/diff evidence must include the actual revision and reconciliation result. Manual incident changes can be reverted by the controller; follow its documented suspension/override process and reconcile the accepted fix into Git.[^argo-cd-diff-customization]

See [Argo CD versus Flux](../argo-cd-vs-flux.md), [GitOps](../gitops.md), and [Flux reconciliation](../flux-reconciliation-and-helm.md). This lab does not deploy either controller or claim to validate their behavior.

## Troubleshoot safely

Confirm the context, namespace, desired revision, credentials, API reachability and permissions. Then inspect admission messages and field ownership. Keep comparison errors separate from no-drift evidence. Never repair a comparison by applying an unreviewed object to a shared cluster.

Diff output can expose sensitive values, and dry-run requests can exercise admission services. Use synthetic files and least-privilege credentials for real CI. Source-only workflows need no cluster access.

Sources reviewed on 2026-11-10. The [lab](regression-lab-and-ci.md#validation-boundary) records hosted API/diff/request evidence separately from local source checks. Its runner owns a new kind cluster/private kubeconfig and checks that the diff did not persist `targetPort: 81`. Comparing alone needs no application cleanup; the lab verifies namespace and cluster removal after its deliberate mutations.

- [Back to series](index.md) | [Back to Kubernetes](../../index.md)

[^kubectl-diff-contract]: [kubectl diff behavior, statuses and external command contract](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/).
[^server-side-apply]: [Server-side apply ownership](https://kubernetes.io/docs/reference/using-api/server-side-apply/).
[^argo-cd-diff-customization]: [Argo CD diff customization](https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/).

[^kubectl-134-source]: [kubectl 1.34.1 external diff argument handling](https://raw.githubusercontent.com/kubernetes/kubectl/v0.34.1/pkg/cmd/diff/diff.go).
