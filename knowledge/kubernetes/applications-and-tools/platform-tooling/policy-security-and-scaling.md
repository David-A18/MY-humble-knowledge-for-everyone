---
type: Explanation
title: Policy, security, and scaling tools
description: Select controls by what they observe or change, and understand their
  failure boundaries.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: kyverno
  resource: https://kyverno.io/docs/
  title: Kyverno
- id: gatekeeper
  resource: https://open-policy-agent.github.io/gatekeeper/website/docs/
  title: Gatekeeper
- id: trivy
  resource: https://trivy.dev/latest/docs/
  title: Trivy
- id: falco
  resource: https://falco.org/docs/
  title: Falco
- id: keda
  resource: https://keda.sh/docs/
  title: KEDA
- id: karpenter
  resource: https://karpenter.sh/docs/
  title: Karpenter
- id: hubble
  resource: https://docs.cilium.io/en/stable/observability/hubble/
  title: Hubble
---

# Policy, security, and scaling tools

## Purpose

Select controls by what they observe or change, and understand their failure boundaries.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Security roles

| Tool | Role | Operational consideration |
| --- | --- | --- |
| Kyverno | Admission policy and background reporting | Webhook availability and controller privileges. |
| OPA Gatekeeper | Admission constraints and audit using OPA/Rego | Audit findings differ from enforced rejection. |
| Trivy | Image, dependency, and configuration scanning | Database freshness, scope, and exploit context. |
| Falco | Runtime system-event detection | Alerts need a response workflow. |
| Cilium / Hubble | Networking, policy, and flow visibility | Flow visibility is not complete application tracing. |

Start policies in audit/warn mode where supported, correct legitimate workloads, then enforce deliberately. Document exception owners, expiry, and webhook failure policies. Record scanner database revisions when reproducing results.

## Scaling roles

HPA adjusts workload replicas. Metrics Server provides short-lived resource metrics used by HPA and `kubectl top`; it is not historical monitoring. KEDA integrates event-source metrics into autoscaling. Karpenter provisions and consolidates nodes according to configured workload constraints.

```bash
kubectl get hpa -A
kubectl top pods -A
kubectl get events -A --field-selector type=Warning
```

What it does: checks replica decisions, resource metrics, and scheduling warnings. `kubectl top` requires a working metrics API.

## Design sequence

1. Set realistic requests and limits.
2. Define replica bounds, cooldowns, and disruption expectations.
3. Prove replicas can obtain nodes, identity, storage, and downstream capacity.
4. Test scale-up, scale-down, eviction, and recovery.
5. Alert on persistent saturation and failed scheduling.

HPA cannot supply nodes; more nodes cannot fix database saturation. Queue scaling needs decisions about concurrency and retries. Consolidation requires application readiness for disruption and appropriate disruption budgets.

Source references: [^kyverno][^gatekeeper][^trivy][^falco][^keda][^karpenter][^hubble]

## Related links

- [Kyverno](https://kyverno.io/docs/)
- [Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/)
- [Trivy](https://trivy.dev/latest/docs/)
- [Falco](https://falco.org/docs/)
- [KEDA](https://keda.sh/docs/)
- [Karpenter](https://karpenter.sh/docs/)
- [Hubble](https://docs.cilium.io/en/stable/observability/hubble/)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^kyverno]: [Kyverno](https://kyverno.io/docs/).
[^gatekeeper]: [Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/).
[^trivy]: [Trivy](https://trivy.dev/latest/docs/).
[^falco]: [Falco](https://falco.org/docs/).
[^keda]: [KEDA](https://keda.sh/docs/).
[^karpenter]: [Karpenter](https://karpenter.sh/docs/).
[^hubble]: [Hubble](https://docs.cilium.io/en/stable/observability/hubble/).
