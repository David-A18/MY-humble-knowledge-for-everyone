# Kafka consumer groups, lag, and replay

## Purpose

Use this guide to reason about Kafka consumer progress, scaling, lag, and safe replay.

## Consumer group model

A consumer group is one logical application made of one or more consumer instances.

```text
Topic: orders.v1 with 6 partitions

consumer group: payment-service
  pod-a -> partitions 0, 3
  pod-b -> partitions 1, 4
  pod-c -> partitions 2, 5
```

Within one group, a partition is assigned to one active consumer at a time. Different groups read the same topic independently.

## Scaling rule

| Situation | Result |
| --- | --- |
| Consumers fewer than partitions | Some consumers process multiple partitions. |
| Consumers equal partitions | Each consumer may process one partition. |
| Consumers more than partitions | Extra consumers are idle for that topic. |
| Hot partition exists | Adding consumers may not reduce lag enough. |

> [!IMPORTANT]
> For a single topic in one consumer group, useful parallelism is bounded by partition count. Scaling a Kubernetes Deployment past that count does not create more partition workers.

## Offset commits

Offsets are progress markers for a group and partition.

| Commit style | Use when | Risk |
| --- | --- | --- |
| Auto commit | Low-risk learning or simple consumers. | Can commit before processing is durable. |
| Manual commit after processing | Side effects must finish first. | A crash after side effect but before commit can duplicate work. |
| Transactional processing | Kafka read-process-write boundary is transactional. | External systems are not automatically included. |

### Describe group lag

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server "$BOOTSTRAP_SERVERS" \
  --command-config client.properties \
  --describe \
  --group payment-service-v1
```

What it does: shows committed offsets, log-end offsets, and lag by partition for the target consumer group.

## Lag diagnosis

| Symptom | Check | Likely cause |
| --- | --- | --- |
| Lag grows on every partition | Consumer throughput and downstream dependencies. | Consumers are slower than producers. |
| Lag grows on one partition | Key distribution and partition traffic. | Hot key or hot tenant. |
| Lag remains after scaling pods | Partition count and assignment. | More pods than useful partitions or repeated rebalances. |
| Consumers rebalance repeatedly | Poll loop, probes, and deployment churn. | Pods restart or exceed poll interval. |
| Lag falls then rises during releases | Deployment strategy. | Rolling updates repeatedly revoke assignments. |

## Replay workflow

Replay means intentionally reading older retained records again. It is useful for rebuilding projections, repairing failed consumers, or validating a new consumer version.

1. Confirm the records are still retained.
2. Decide whether to reuse a group or create a new replay group.
3. Confirm downstream operations are idempotent.
4. Stop active consumers if resetting an existing group.
5. Run a dry run.
6. Execute the reset.
7. Monitor lag, errors, and downstream side effects.

### Dry-run offset reset

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server "$BOOTSTRAP_SERVERS" \
  --command-config client.properties \
  --group payment-service-replay \
  --topic orders.v1 \
  --reset-offsets \
  --to-earliest \
  --dry-run
```

What it does: previews the offset change without applying it.

### Execute offset reset

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server "$BOOTSTRAP_SERVERS" \
  --command-config client.properties \
  --group payment-service-replay \
  --topic orders.v1 \
  --reset-offsets \
  --to-earliest \
  --execute
```

What it does: moves the selected group offsets so records can be consumed again from the chosen point.

> [!WARNING]
> Never reset offsets for a production group casually. Reprocessing can repeat payments, emails, inventory reservations, or other side effects unless consumers are idempotent.

## Related links

- Official documentation: [Apache Kafka consumer groups and offsets](https://kafka.apache.org/documentation/)
- Official documentation: [Kafka basic operations](https://kafka.apache.org/42/operations/basic-kafka-operations/)
- [Kafka fundamentals](fundamentals.md)
- [Kafka operations](operations.md)
- [Delivery guarantees and failure handling](delivery-guarantees-and-failure-handling.md)
- [Back to Kafka](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
