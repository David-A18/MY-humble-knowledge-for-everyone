---
type: Reference
title: Instrumentation and observability tool selection
description: Choose collection and storage according to the operational question.
tags:
- kubernetes
- observability
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: instrumentation
  resource: https://opentelemetry.io/docs/concepts/instrumentation/
  title: Instrumentation
- id: prometheus-overview
  resource: https://prometheus.io/docs/introduction/overview/
  title: Prometheus overview
- id: grafana
  resource: https://grafana.com/docs/
  title: Grafana
- id: hubble
  resource: https://docs.cilium.io/en/stable/observability/hubble/
  title: Hubble
---

# Instrumentation and observability tool selection

## Purpose

Choose collection and storage according to the operational question.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Component roles

| Component | Role | Does not automatically provide |
| --- | --- | --- |
| Prometheus | Metrics storage, queries, and rules | Application logs and complete traces. |
| Grafana | Dashboards and data-source exploration | Universal collection/storage. |
| OpenTelemetry | APIs, SDKs, conventions, protocol, Collector | A required permanent backend. |
| Fluent Bit / Vector | Collection, transformation, routing | Complete long-term querying. |
| Loki / Tempo / Jaeger | Log or trace storage/query capabilities | Instrumentation of all application code. |
| Pixie | eBPF-assisted Kubernetes telemetry/debugging | Universal protocols or unlimited retention. |
| Cilium / Hubble | Networking, policy, flow visibility | Full business-request context. |
| Falco | Runtime security detection | Application performance diagnosis alone. |

## Instrumentation choices

Manual SDK instrumentation adds business context and trace propagation. Automatic language instrumentation reduces code changes but depends on runtime/library compatibility. eBPF observes selected kernel/user-space boundaries and supported protocols; it cannot infer every business operation or create perfect cross-service context.

A useful combination is application OpenTelemetry for business traces, metrics, structured logs, and network/eBPF diagnostics. Select measured coverage rather than assuming a single product captures everything.

## Selection criteria

Check runtimes, kernels, node types, privileges, residency, retention, export integration, and team support. Estimate cardinality and ingestion cost. Reproduce a slow request and failed dependency before choosing dashboards.

## Validation

Inspect attributes, timestamps, trace relationships, and dropped-data counters. Determine whether the dashboard shows fresh data. A healthy collector process can still reject every export because of authentication or a wrong protocol endpoint.

Source references: [^instrumentation][^prometheus-overview][^grafana][^hubble]

## Related links

- [Instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/)
- [Prometheus overview](https://prometheus.io/docs/introduction/overview/)
- [Grafana](https://grafana.com/docs/)
- [Hubble](https://docs.cilium.io/en/stable/observability/hubble/)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^instrumentation]: [Instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/).
[^prometheus-overview]: [Prometheus overview](https://prometheus.io/docs/introduction/overview/).
[^grafana]: [Grafana](https://grafana.com/docs/).
[^hubble]: [Hubble](https://docs.cilium.io/en/stable/observability/hubble/).
