---
type: Executor Reference
title: Run Prometheus query
description: Synthetic executor contract for running the Pod restart rate PromQL query and returning a receipt.
tags: [prometheus, executor, attested-computation]
status: draft
generated: { by: process:example-renderer, at: 2026-08-08T11:07:00Z }
verified:
  - { by: human:kb-reviewer, at: 2026-08-08T11:17:00Z }
stale_after: 2026-10-08
---

# Run Prometheus query

This is a synthetic executor contract. It is not a production credential, endpoint, or runnable integration.

## Inputs

| Parameter | Type | Rule |
| --- | --- | --- |
| `namespace` | string | Kubernetes namespace name. |
| `app` | string | Application name prefix used in the Pod selector. |
| `window` | string | Prometheus duration such as `5m`, `30m`, or `1h`. |

## Receipt

The executor returns:

```json
{
  "query": "sum by (pod) (...)",
  "datasource": "synthetic-prometheus",
  "parameters": {
    "namespace": "payments",
    "app": "checkout",
    "window": "30m"
  },
  "started_at": "2026-08-08T11:20:00Z",
  "result_hash": "sha256:example"
}
```

What it does: records runtime evidence without storing private metrics or credentials in the bundle.

## Related links

- [Pod restart rate](../../concepts/pod-restart-rate.md)
- [Attester reference](../attesters/prometheus-receipt-shape.md)
- [Back to executor references](README.md)
