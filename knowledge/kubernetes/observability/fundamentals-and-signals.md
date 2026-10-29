---
type: Explanation
title: Observability fundamentals and signals
description: Use evidence to explain system behavior and user impact.
tags:
- kubernetes
- observability
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: opentelemetry-signals
  resource: https://opentelemetry.io/docs/concepts/signals/
  title: OpenTelemetry signals
- id: prometheus-naming
  resource: https://prometheus.io/docs/practices/naming/
  title: Prometheus naming
- id: sre-monitoring
  resource: https://sre.google/sre-book/monitoring-distributed-systems/
  title: SRE monitoring
---

# Observability fundamentals and signals

## Purpose

Use evidence to explain system behavior and user impact.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## What o11y means

Observability is the ability to understand system behavior from outputs and telemetry. Monitoring checks known conditions; exploration correlates signals to investigate unfamiliar failures. More telemetry does not automatically produce better diagnosis.[^opentelemetry-signals][^prometheus-naming][^sre-monitoring]

| Signal | Good question | Common mistake |
| --- | --- | --- |
| Metrics | Is latency/error rate/saturation changing? | Unbounded labels such as user IDs. |
| Logs | What happened in this operation? | Recording secrets or unstructured noise. |
| Traces | Where did a request spend time? | Missing context propagation. |
| Profiles | Which code consumes CPU or memory? | Treating one short sample as universal. |
| Kubernetes events | Why did orchestration fail? | Treating short-lived events as durable history. |

## Start with user behavior

Define a service-level indicator, such as successful checkout requests divided by eligible requests. Choose an SLO over a stated window. The error budget is the allowed unreliability implied by that objective. Alert on user impact and meaningful budget consumption, not every transient restart.

Latency, traffic, errors, and saturation are useful starting signals. A healthy Deployment does not prove a dependency, DNS path, or user journey works.

## Correlate safely

Attach stable service, environment, cluster, namespace, and revision identifiers. Propagate trace context through supported libraries and queues. Keep customer identifiers and tokens out of labels and unrestricted payload capture.

```bash
kubectl get pods -A
kubectl get events -n demo --sort-by=.lastTimestamp
kubectl logs -n demo deployment/api --since=10m
```

What it does: gathers workload state, recent orchestration events, and application logs. These are first checks rather than a historical monitoring system.

## Operations

Set retention, access, sampling, redaction, and budget expectations before broad collection. Monitor the telemetry pipeline itself. Test that a known request can be found across signals, then simulate exporter failure and verify loss/backpressure evidence.

## Related links

- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)
- [Prometheus naming](https://prometheus.io/docs/practices/naming/)
- [SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^opentelemetry-signals]: [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/).
[^prometheus-naming]: [Prometheus naming](https://prometheus.io/docs/practices/naming/).
[^sre-monitoring]: [SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/).
