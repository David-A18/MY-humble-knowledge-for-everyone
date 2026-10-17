---
type: "Attester Reference"
title: "Prometheus receipt shape"
description: "Explains why a synthetic receipt-shape check cannot attest a real Prometheus execution."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
resource: prometheus-receipt-shape.py
---

# Prometheus receipt shape

The [Python example](prometheus-receipt-shape.py) checks whether a synthetic
receipt resembles the expected query record. It is **not** a production
attester. It deliberately returns `ok: false` even for a plausible receipt,
because shape alone cannot prove that the query ran.

The attester checks:

- Required receipt keys and the exact three parameters exist.
- Namespace, Pod prefix, and window fit narrow input patterns.
- The query matches the illustrative computation after those values are bound.
- The timestamp has a time-zone offset and the hash has a SHA-256-shaped value.

It cannot authenticate the datasource, recompute a hash from an actual
Prometheus result, or know who created the receipt. A caller could fabricate
every field, so the `ok` attestation verdict remains false. A real system
would need a trusted executor and result evidence that the attester can
independently check.

## Related links

- [Pod restarts in a time window](../../concepts/pod-restart-rate.md)
- [Prometheus executor](../executors/run-prometheus-query.md)
- [Back to attester references](index.md)
