# Kafka delivery guarantees and failure handling

## Purpose

Use this guide to choose producer, consumer, retry, and dead-letter patterns that match the real business risk of duplicate, lost, or delayed records.

## Delivery guarantee choices

| Guarantee | Meaning | Common fit |
| --- | --- | --- |
| At-most-once | A record might be lost, but is not intentionally retried after processing starts. | Low-value telemetry where loss is acceptable. |
| At-least-once | A record is retried until processed, but duplicates can happen. | Most business event consumers with idempotency. |
| Exactly-once within Kafka | Kafka read-process-write can be transactional. | Stream processing that writes back to Kafka. |

> [!IMPORTANT]
> Exactly-once Kafka processing does not make an external payment provider, email service, database, or HTTP API exactly-once. Define the transactional boundary before relying on the label.

## Producer safety settings

| Setting | Typical production direction | Why |
| --- | --- | --- |
| `acks` | `all` for important records. | Waits for stronger broker acknowledgement. |
| `enable.idempotence` | `true` where supported. | Reduces duplicates from producer retries. |
| `retries` | Enabled with bounded delivery timeout. | Handles transient broker or network failures. |
| `compression.type` | Test `zstd`, `lz4`, or another supported codec. | Reduces network and storage pressure. |
| Key selection | Stable business key. | Preserves ordering within that key. |

### Baseline producer properties

```properties
acks=all
enable.idempotence=true
compression.type=zstd
delivery.timeout.ms=120000
request.timeout.ms=30000
linger.ms=5
```

What it does: starts with safer acknowledgement and retry behavior, then leaves throughput and latency tuning to load tests.

## Consumer failure patterns

| Failure | Symptom | Safer response |
| --- | --- | --- |
| Poison record | Same record fails repeatedly. | Route to a dead-letter topic after bounded retries. |
| Slow dependency | Lag grows and retries amplify traffic. | Add backoff, circuit breaking, and dependency protection. |
| Crash after side effect | Duplicate business action on restart. | Use idempotency keys or an inbox table. |
| Bad schema | Deserialization failures. | Validate compatibility before rollout and isolate bad records. |
| Partition hot spot | One partition stays behind. | Revisit key choice and topic partition strategy. |

## Retry topology

Avoid infinite tight retry loops in the main consumer. A common pattern is:

```text
orders.v1
  -> payment-consumer
  -> payment-retry-5m
  -> payment-retry-1h
  -> payment-dlq
```

What it does: gives transient failures time to recover while preserving a final place for records that need human or automated repair.

## Transactional outbox

Use a transactional outbox when a service must update its database and publish an event based on that update.

```text
Application transaction
  -> write order row
  -> write outbox row

Publisher or CDC connector
  -> reads outbox row
  -> publishes Kafka event
```

What it does: avoids the unsafe sequence where the database commit succeeds but the Kafka publish fails, or the Kafka publish succeeds but the database commit rolls back.

## Idempotency checklist

- Include an event ID or operation ID.
- Store processed IDs or enforce unique constraints.
- Use conditional writes where available.
- Make external API calls with provider-supported idempotency keys.
- Keep retry handlers from changing the business meaning of an event.
- Document whether replay is allowed for every topic.

## Related links

- Official documentation: [Kafka producer configuration](https://kafka.apache.org/documentation/#producerconfigs)
- Official documentation: [Kafka design and guarantees](https://kafka.apache.org/documentation/#design)
- [Topic and event design](topic-and-event-design.md)
- [Consumer groups, lag, and replay](consumer-groups-lag-and-replay.md)
- [Kafka operations](operations.md)
- [Back to Kafka](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
