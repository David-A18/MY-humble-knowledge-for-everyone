---
type: Attester Reference
title: Prometheus receipt shape
description: Deterministic receipt-shape attester for the Pod restart rate example.
resource: prometheus-receipt-shape.py
tags: [python, attester, attested-computation]
status: draft
generated: { by: process:example-renderer, at: 2026-08-08T11:09:00Z }
verified:
  - { by: human:kb-reviewer, at: 2026-08-08T11:19:00Z }
stale_after: 2026-10-08
---

# Prometheus receipt shape

This reference points to [prometheus-receipt-shape.py](prometheus-receipt-shape.py), a small deterministic example attester.

The attester checks:

- Required receipt keys exist.
- `parameters` is an object.
- `result_hash` starts with `sha256:`.
- The query contains the expected restart metric name.

It does not prove the metric source is correct, authenticate the datasource, or authorize access. Production attesters need stronger checks.

## Related links

- [Pod restart rate](../../concepts/pod-restart-rate.md)
- [Prometheus executor](../executors/run-prometheus-query.md)
- [Back to attester references](README.md)
