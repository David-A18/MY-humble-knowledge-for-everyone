# MongoDB replication, sharding, and consistency

## Purpose

Use this guide to decide when MongoDB needs replica sets, sharding, read preferences, write concern, and restore testing.

## Replica set model

A replica set keeps copies of the same data across `mongod` members.

```text
primary
  -> secondary
  -> secondary
```

The primary accepts writes. Secondaries replicate from the primary and can become primary during an election.

## Replication decisions

| Decision | Why it matters |
| --- | --- |
| Member count and placement | Affects fault tolerance and election behavior. |
| Write concern | Controls acknowledgement durability for writes. |
| Read concern | Controls the isolation and freshness expectation for reads. |
| Read preference | Controls whether reads go to primary or secondary members. |
| Backup method | Replication is not a backup. |
| Restore test | Proves the backup can meet RPO and RTO. |

> [!WARNING]
> Replication protects availability for some failures, but it also replicates accidental deletes, bad writes, and application corruption. Keep separate backups and test restores.

## Sharding model

Use sharding when one replica set cannot handle data size, write volume, or working-set requirements.

```text
application
  -> mongos router
  -> shard A
  -> shard B
  -> shard C
```

The shard key determines how documents are distributed and how targeted queries reach the right shard.

## Shard-key checklist

- High enough cardinality.
- Even write distribution.
- Supports common query filters.
- Avoids one tenant, status, or timestamp becoming a hot range.
- Stable enough that resharding is rare.
- Compatible with uniqueness requirements.

## Query routing

| Query type | Behavior |
| --- | --- |
| Includes shard key or prefix. | Can target fewer shards. |
| Does not include shard key. | May scatter across shards. |
| Uses a hot shard-key value. | Can overload one shard. |
| Sorts without supporting index. | Can become expensive across shards. |

## Consistency reminders

| Concept | Practical meaning |
| --- | --- |
| Write concern | How many members acknowledge a write. |
| Read concern | Which committed state a read can observe. |
| Read preference | Which member type receives reads. |
| Transactions | Useful, but not a substitute for good document modeling. |
| Change streams | Useful for event-driven reactions, but consumers still need idempotency. |

## Operations checks

| Symptom | First check |
| --- | --- |
| Failover caused write errors | Driver retry behavior and write concern. |
| Secondary reads are stale | Replication lag and read preference. |
| One shard is hot | Shard-key distribution and query pattern. |
| Backups are large or slow | Backup method, retention, and restore targets. |
| Change stream missed processing | Resume tokens, retention window, and consumer durability. |

## Related links

- Official documentation: [MongoDB replication](https://www.mongodb.com/docs/manual/replication/)
- Official documentation: [MongoDB sharding](https://www.mongodb.com/docs/manual/sharding/)
- Official documentation: [MongoDB read concern](https://www.mongodb.com/docs/manual/reference/read-concern/)
- [MongoDB operations](operations.md)
- [MongoDB data modeling](data-modeling.md)
- [MongoDB on AWS](../../cloud/aws/databases/mongodb-on-aws.md)
- [Back to MongoDB](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
