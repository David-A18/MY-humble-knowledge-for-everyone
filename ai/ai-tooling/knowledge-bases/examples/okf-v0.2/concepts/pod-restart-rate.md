---
type: Attested Computation
title: Pod restart rate
description: Example sanctioned computation for counting Kubernetes container restarts over a time window.
tags: [kubernetes, prometheus, attestation]
status: draft
runtime: prometheus
parameters:
  - { name: namespace, type: string, required: true }
  - { name: app, type: string, required: true }
  - { name: window, type: string, required: true }
computation: pod-restart-rate-promql
executor:
  resource: references/executors/run-prometheus-query.md
  receipt: [query, datasource, parameters, started_at, result_hash]
attester:
  resource: references/attesters/prometheus-receipt-shape.py
generated: { by: process:example-renderer, at: 2026-08-08T10:10:00Z }
verified:
  - { by: process:example-ci, at: 2026-08-08T10:40:00Z }
stale_after: 2026-10-08
usage_window: 2026-08
sources:
  - id: kube-state-metrics
    resource: references/sources/kube-state-metrics.md
    title: kube-state-metrics project
    author: process:kubernetes-project
    usage_count: 5
    last_modified: 2026-08-01
---

# Computation

```promql
sum by (pod) (
  increase(kube_pod_container_status_restarts_total{
    namespace="$namespace",
    container!="",
    pod=~"$app.*"
  }[$window])
)
```

What it does: counts container restart increases for Pods whose names match an application prefix in one namespace and time window.

The metric comes from kube-state-metrics-style Kubernetes state metrics.[^kube-state-metrics]

## Attestation model

The executor runs the query and returns a receipt containing the query, datasource, parameters, start time, and result hash. The attester is deterministic code that checks the receipt shape and confirms the query matches the sanctioned computation.

An LLM may explain the result, but it must not act as the attester.

[^kube-state-metrics]: kube-state-metrics project.

## Related links

- [Retrieval budget](retrieval-budget.md)
- [Prometheus executor](../references/executors/run-prometheus-query.md)
- [Receipt-shape attester](../references/attesters/prometheus-receipt-shape.md)
- [kube-state-metrics source reference](../references/sources/kube-state-metrics.md)
- [Back to bundle index](../index.md)
