# Kafka operations

## Purpose

Use this page to operate Kafka by watching the signals that usually explain reliability, performance, and consumer health.

## Operational signals

| Signal | What to check | Why it matters |
| --- | --- | --- |
| Consumer lag | Lag by group, topic, and partition. | Shows whether consumers are keeping up. |
| Under-replicated partitions | Partition replication health. | Indicates broker or network problems. |
| Offline partitions | Partitions without available leaders. | Clients cannot read or write those partitions. |
| Request latency | Produce, fetch, and metadata latency. | Reveals broker, storage, or network pressure. |
| Disk usage | Broker log volume and retention. | Full disks can stop brokers. |

## Common troubleshooting sequence

1. Identify the affected topic and consumer group.
2. Check whether lag is isolated to one partition or spread across many.
3. Review consumer errors, retries, and downstream dependency latency.
4. Check broker health, partition leadership, and replication status.
5. Confirm recent deployment, schema, partition-count, or retention changes.

## Recovery habits

- Scale consumers only when there are enough partitions to use them.
- Avoid resetting offsets until you understand the replay impact.
- Keep dead-letter handling explicit for events that cannot be processed safely.
- Monitor broker storage before retention changes or traffic spikes.

## Related links

- [Kafka fundamentals](fundamentals.md)
- [Topic and event design](topic-and-event-design.md)
- [Amazon MSK](../../cloud/aws/databases/amazon-msk.md)
- [Apache Kafka documentation](https://kafka.apache.org/documentation/)
- [Back to Kafka index](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
