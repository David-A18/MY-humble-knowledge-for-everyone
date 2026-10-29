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
---

# Detect desired-versus-live Kubernetes drift

## Purpose

Compare the prospective apply result with live state and interpret reconciliation ownership.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Server-side comparison

```bash
kubectl diff --server-side -f desired.yaml
```

What it does: asks the API server to calculate the would-be applied configuration and compares it with current objects. It needs cluster access and permissions and may exercise dry-run admission. It does not prove data-plane success.

## Correct exit-code handling

```bash
set +e
kubectl diff -f desired.yaml
result=$?
set -e
case "$result" in
  0) echo "No differences" ;;
  1) echo "Differences need review" ;;
  *) echo "Comparison failed" >&2; exit "$result" ;;
esac
```

What it does: distinguishes no difference (0), differences (1), and errors (>1). Pipelines may deliberately fail on differences, but must label them correctly. Do not use `|| true`, which hides authentication and API failures.

## Controller-managed fields

Status, defaulted values, HPA-controlled replicas, webhook-injected containers, and allocated Service fields can differ legitimately. Configure narrow ignore rules only after identifying the owner. Ignoring a complete object or broad subtree can hide a real security or routing change.

Argo CD and Flux also compare and reconcile configuration. Use the existing controller's revision and reconciliation status as evidence. A manual emergency change can be reverted at the next reconciliation; record it in Git or use the documented temporary suspension procedure.

## Troubleshooting

First confirm context, namespace, desired revision, and permissions. Next inspect field ownership and admission mutation. Finally investigate unexpected pruning or resource renaming. A forbidden API request is a failed comparison, not evidence of no drift.

Source references: [^kubectl-diff-contract][^server-side-apply][^argo-cd-diff-customization]

## Related links

- [kubectl diff contract](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/)
- [Server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
- [Argo CD diff customization](https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/)
- [Flux reconciliation](../flux-reconciliation-and-helm.md)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^kubectl-diff-contract]: [kubectl diff contract](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/).
[^server-side-apply]: [Server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/).
[^argo-cd-diff-customization]: [Argo CD diff customization](https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/).
