---
type: "Executor Reference"
title: "Run Prometheus query"
description: "This is a synthetic executor contract. It is not a production credential, endpoint, or runnable integration."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Run Prometheus query

This is a synthetic executor contract. It is not a production credential,
endpoint, or runnable integration. The receipt below is **invented** and
does not prove that Prometheus returned a value.

## Inputs

| Parameter | Type | Rule |
| --- | --- | --- |
| `namespace` | string | Kubernetes namespace name. |
| `app` | string | Safe Pod-name prefix ending in a hyphen, such as `checkout-`; reject regex operators and quotes. |
| `window` | string | Positive Prometheus duration such as `5m`, `30m`, or `1h`. |

## Receipt

An actual executor would need to record the **executed** query, its trusted
datasource, time, and result evidence. This JSON only illustrates the fields:

```json
{
  "query": "sum by (pod) (increase(kube_pod_container_status_restarts_total{namespace=\"payments\",pod=~\"checkout-.*\"}[30m]))",
  "datasource": "synthetic-prometheus",
  "parameters": {
    "namespace": "payments",
    "app": "checkout-",
    "window": "30m"
  },
  "started_at": "2026-08-08T11:20:00Z",
  "result_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
}
```

The zero hash is a placeholder, not a digest of a result. The sample checker
can recognize this JSON's shape but still refuses a successful execution
attestation. For a real verdict, the consumer would need a trusted executor,
authenticated datasource, and a digest recomputed from the returned result.

## Related links

- [Pod restarts in a time window](../../concepts/pod-restart-rate.md)
- [Attester reference](../attesters/prometheus-receipt-shape.md)
- [Back to executor references](index.md)
