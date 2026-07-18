# Kafka fundamentals

## Purpose

Use this page to understand the core Kafka mental model before designing producers, consumers, or AWS streaming architectures.

## Core concepts

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Record | One event with a key, value, timestamp, and metadata. | It is the unit producers write and consumers read. |
| Topic | Named append-only log split into partitions. | It organizes related events and retention policy. |
| Partition | Ordered shard of a topic. | It controls ordering, parallelism, and broker distribution. |
| Broker | Kafka server that stores partitions and serves clients. | More brokers can increase capacity and resilience. |
| Producer | Client that writes records to topics. | Key choice controls which partition receives a record. |
| Consumer group | Consumers sharing work for a topic. | Each partition is consumed by one group member at a time. |
| Offset | Position of a record in a partition. | Consumers commit offsets to track progress. |

## Message flow

1. A producer serializes an event and sends it to a topic.
2. Kafka chooses a partition, often from the record key.
3. The partition leader appends the record to the log.
4. Followers replicate the record.
5. Consumers fetch records and commit offsets after processing.

## Design reminders

- Ordering is guaranteed inside one partition, not across all partitions in a topic.
- More partitions can increase parallelism, but they add operational overhead.
- Consumer lag means consumers are behind the latest produced offset.
- Retention allows replay, but it is not a substitute for a permanent database.

## Related links

- [Apache Kafka documentation](https://kafka.apache.org/documentation/)
- [Topic and event design](topic-and-event-design.md)
- [Kafka operations](operations.md)
- [Back to Kafka index](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
