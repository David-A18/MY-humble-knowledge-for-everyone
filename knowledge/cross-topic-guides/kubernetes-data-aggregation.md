---
type: Explanation
title: Kafka data aggregation on Kubernetes
description: Calculate minute-level order totals while handling duplicates, late events,
  and restarts.
tags:
- cross-topic-guides
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: kafka-docker-guide
  resource: https://kafka.apache.org/40/getting-started/docker/
  title: Kafka Docker guide
- id: kafka-delivery-semantics
  resource: https://kafka.apache.org/40/design/design/
  title: Kafka delivery semantics
- id: kafka-python-consumer
  resource: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
  title: kafka-python consumer
---

# Kafka data aggregation on Kubernetes

## Purpose

Calculate minute-level order totals while handling duplicates, late events, and restarts.

Sources reviewed: 2026-10-29. See the [validation record](../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Contract and limits

The [example](examples/data-aggregation/index.md) uses one Kafka partition and one consumer with a SQLite database on a PVC. Each JSON event has a globally unique `id`, integer Unix-seconds `ts`, non-empty `region`, and integer `amount_cents`. It groups by region and 60-second tumbling window.[^kafka-docker-guide][^kafka-delivery-semantics][^kafka-python-consumer]

The watermark is maximum observed event time minus 30 seconds. A new event for a window whose end is at or behind the watermark is recorded as late rather than changing totals. Accepted event IDs and count/sum updates commit in one SQLite transaction. Consumer offsets commit afterward, so replay after a crash is deduplicated. This makes the local aggregate idempotent for matching event IDs, not every possible downstream effect exactly once.

The teaching engine retains deduplication IDs and totals indefinitely and advances its watermark only on input. Production use needs bounded retention, idle-input handling, and validation of implausible future timestamps; a bad future timestamp could close earlier windows. Signed amounts permit adjustments/refunds and require an application-specific business contract.

## Offline first

Use Python 3.13; the state engine uses only the standard library. Run from the repository root:

```bash
python knowledge/cross-topic-guides/examples/data-aggregation/aggregate.py --db /tmp/aggregate.sqlite < knowledge/cross-topic-guides/examples/data-aggregation/events.jsonl
python knowledge/cross-topic-guides/examples/data-aggregation/test_aggregate.py
```

What it does: processes synthetic records, shows accepted/duplicate/late outcomes, and tests restart/replay behavior. Reusing the database deliberately retains prior state. Use a fresh dedicated file for a clean run.

## Kubernetes/Kafka lab

Use a disposable kind cluster with a default StorageClass, Docker, kubectl, and the pinned Kafka **4.0.0** image. The consumer image pins Python **3.13** and kafka-python **2.2.15**. Run from the example directory.

```bash
docker build -t kb-aggregator:lab .
kind load docker-image kb-aggregator:lab
kubectl create namespace aggregation-lab
kubectl apply -n aggregation-lab -f kafka.yaml
kubectl rollout status deployment/kafka -n aggregation-lab --timeout=180s
kubectl exec -n aggregation-lab deployment/kafka -- /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1
kubectl apply -n aggregation-lab -f consumer.yaml
kubectl exec -i -n aggregation-lab deployment/kafka -- /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders < events.jsonl
kubectl logs -n aggregation-lab deployment/aggregator
```

What it does: creates an ephemeral single-broker teaching cluster and a persistent aggregate consumer. Expect the fixture's duplicate to leave totals unchanged and its closed-window event to be recorded late. Kafka storage here is deliberately ephemeral and unreplicated; the example is unsuitable for production.

## Failure and recovery

Delete only the aggregator Pod and let the Deployment recreate it. Its PVC must preserve state. Replay the same events and verify totals do not grow. Stop Kafka temporarily, observe consumer errors/reconnect behavior, and restore it. A crash after SQLite commit but before Kafka offset commit must not double-count a replay.

Invalid JSON or a conflicting reuse of an event ID stops the consumer before offset commit. Diagnose and quarantine through a reviewed dead-letter procedure; the sample does not silently discard poison records. Late, well-formed events are persisted separately. Stateful scaling, durable Kafka, retention, and migration require further design.

## Cleanup

> [!WARNING]
> Verify context before deleting `aggregation-lab`. This deletes its PVC and aggregate history. Preserve a state snapshot first if you need to inspect results later.

```bash
kubectl delete namespace aggregation-lab
```

What it does: removes only this disposable workload and its local broker/state.

## Related links

- [Kafka Docker guide](https://kafka.apache.org/40/getting-started/docker/)
- [Kafka delivery semantics](https://kafka.apache.org/40/design/design/)
- [kafka-python consumer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)
- [Databases](../databases/index.md)
- [Kafka](../databases/kafka/index.md)
- [Kubernetes](../kubernetes/index.md)
- [Back to parent index](index.md)
- [Back to root index](../../README.md)

[^kafka-docker-guide]: [Kafka Docker guide](https://kafka.apache.org/40/getting-started/docker/).
[^kafka-delivery-semantics]: [Kafka delivery semantics](https://kafka.apache.org/40/design/design/).
[^kafka-python-consumer]: [kafka-python consumer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html).
