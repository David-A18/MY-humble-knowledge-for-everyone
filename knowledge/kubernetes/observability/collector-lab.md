---
type: Tutorial
title: OpenTelemetry Collector delivery and failure lab
description: Send a synthetic span through a pinned gateway and observe failure.
tags:
- kubernetes
- observability
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: collector-configuration
  resource: https://opentelemetry.io/docs/collector/configuration/
  title: Collector configuration
- id: resiliency
  resource: https://opentelemetry.io/docs/collector/resiliency/
  title: Resiliency
- id: otlp
  resource: https://opentelemetry.io/docs/specs/otlp/
  title: OTLP
---

# OpenTelemetry Collector delivery and failure lab

## Purpose

Send a synthetic span through a pinned gateway and observe failure.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prerequisites

Use a disposable Kubernetes cluster, kubectl, and Python 3.13. The fixture pins `otel/opentelemetry-collector-contrib:0.139.0`, a historical lab baseline rather than the newest-release recommendation. Runtime execution is recorded in the validation report.[^collector-configuration][^resiliency][^otlp]

## Deploy

```bash
kubectl create namespace telemetry-lab
kubectl apply -n telemetry-lab -f examples/collector.yaml
kubectl rollout status deployment/collector -n telemetry-lab --timeout=120s
kubectl port-forward -n telemetry-lab service/collector 4318:4318
```

What it does: starts an OTLP/HTTP gateway with memory limiting, batching, and debug export. Run from this series directory; port-forwarding remains in the foreground.

```bash
python examples/send-span.py
kubectl logs -n telemetry-lab deployment/collector --since=2m
```

What it does: sends `kb-lab-request` to `/v1/traces` and checks output. Expect HTTP success and the named span after the batch interval. Use only synthetic values because debug export prints data.

## Failure checks

Stop forwarding and rerun the sender: it must exit nonzero with a connection error. Restart and confirm recovery. For a Collector outage, scale its dedicated Deployment to zero, observe failure, restore one replica, wait for readiness, and retry.

For backend failure, replace debug export in a temporary configuration with a supported OTLP exporter pointed at a controlled unavailable backend. Configure bounded queue/retry behavior and inspect failures and drops. Receiver HTTP success can precede export failure and does not prove durable delivery.

## Security and cleanup

The receiver binds to the Pod network so its Service can reach it. Add access restrictions and TLS/authentication before production. It is a diagnostic fixture without durable storage.

> [!WARNING]
> Stop forwarding, verify context, then delete only `telemetry-lab`. Its queued/in-memory data is disposable.

## Related links

- [Collector configuration](https://opentelemetry.io/docs/collector/configuration/)
- [Resiliency](https://opentelemetry.io/docs/collector/resiliency/)
- [OTLP](https://opentelemetry.io/docs/specs/otlp/)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^collector-configuration]: [Collector configuration](https://opentelemetry.io/docs/collector/configuration/).
[^resiliency]: [Resiliency](https://opentelemetry.io/docs/collector/resiliency/).
[^otlp]: [OTLP](https://opentelemetry.io/docs/specs/otlp/).
