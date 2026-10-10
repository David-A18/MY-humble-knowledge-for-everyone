# Kafka

Apache Kafka knowledge for event streaming architecture, topic design, operations, and cloud deployment.

## Articles

| Article | Purpose |
| --- | --- |
| [Kafka fundamentals](fundamentals.md) | Follow one event from producer to partition and independent consumer groups before designing a topic. |
| [Topic and event design](topic-and-event-design.md) | Choose business-fact boundaries, keys, and schemas while distinguishing partition append order, retention, and replay. |
| [Consumer groups, lag, and replay](consumer-groups-lag-and-replay.md) | See how groups divide partitions, what lag measures, and why replay can repeat side effects. |
| [Delivery guarantees and failure handling](delivery-guarantees-and-failure-handling.md) | Follow one event across the external side effect and offset commit, then choose a repeat-safe business action. |
| [Kafka operations](operations.md) | Locate a likely fault along the producer, broker, consumer, and application path using distinct signals. |
| [Kafka on AWS](../../cloud/aws/databases/amazon-msk.md) | Use Amazon MSK and connect AWS workloads to Kafka. |

[Back to databases index](../index.md) | [Back to knowledge index](../../index.md)
