---
type: Reference
title: Manifest comparison and regression concepts
description: Choose the check that answers the actual operational question.
tags:
- kubernetes
- manifest-validation
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: kubectl-diff
  resource: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/
  title: kubectl diff
- id: dyff
  resource: https://github.com/homeport/dyff
  title: dyff
- id: helm-diff
  resource: https://github.com/databus23/helm-diff
  title: Helm Diff
---

# Manifest comparison and regression concepts

## Purpose

Choose the check that answers the actual operational question.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Four different questions

| Question | Appropriate tools | Blind spot |
| --- | --- | --- |
| What changed in source? | `git diff` | Templates may render differently. |
| What changed in rendered objects? | `dyff`, Helm Diff, Helm/Kustomize rendering | No proof of runtime health. |
| Does live state differ from desired? | `kubectl diff`, Argo CD diff, Flux diff/reconciliation | Admission and controller defaults add noise. |
| Does behavior still work? | Helm tests, Chainsaw, HTTP/DNS probes | Covers only asserted scenarios. |

A regression is previously working behavior broken by a change. Drift is divergence between actual and intended state. A formatting change is neither automatically a regression nor operational drift.

## Layer the checks

Render -> schema validation -> policy checks -> semantic comparison -> cluster admission/diff -> behavioral checks. Stop at the earliest meaningful failure, but preserve later checks: schema-valid YAML can still route to the wrong port.

## Review rules

Compare the same chart versions, values, overlays, and API capabilities. Identify objects by API group/kind/namespace/name. Avoid sorting lists blindly: environment-variable order, init-container order, and policy-rule semantics may matter. Normalize only fields proven irrelevant to the question.

Generated timestamps, resource versions, status, and managed fields often create live-export noise. Keep selectors, resource limits, images, permissions, probes, and routing fields visible. Secret values need redaction, not an unrestricted diff artifact.

## Practical outcome

A useful pipeline reports whether it found an intentional difference, an invalid object, a policy violation, a cluster communication failure, or a failed behavior test. Avoid a single ambiguous green/red result that hides the cause.

Source references: [^kubectl-diff][^dyff][^helm-diff]

## Related links

- [kubectl diff](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/)
- [dyff](https://github.com/homeport/dyff)
- [Helm Diff](https://github.com/databus23/helm-diff)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^kubectl-diff]: [kubectl diff](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/).
[^dyff]: [dyff](https://github.com/homeport/dyff).
[^helm-diff]: [Helm Diff](https://github.com/databus23/helm-diff).
