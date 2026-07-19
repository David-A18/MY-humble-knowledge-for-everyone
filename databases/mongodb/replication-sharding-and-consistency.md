# MongoDB replication, sharding, and consistency

## Purpose

Use this guide to decide when MongoDB needs replica sets, sharding, read preferences, write concern, and restore testing.

## How it works

MongoDB separates availability and scale concerns:

```text
Replica set
  -> multiple copies of the same data for failover

Sharded cluster
  -> multiple shards that each own part of the data
```

Most production MongoDB deployments start with a replica set. Sharding is added when one replica set no longer satisfies storage, working set, or throughput requirements.

## Replica set model

A replica set keeps copies of the same data across `mongod` members.

```text
primary
  -> secondary
  -> secondary
```

The primary accepts writes. Secondaries replicate from the primary and can become primary during an election.

## Replica set components

| Component | What it does |
| --- | --- |
| Primary | Accepts writes and records changes. |
| Secondary | Replicates changes and can serve reads when configured. |
| Oplog | Ordered operation log used for replication. |
| Election | Process that chooses a new primary after failure. |
| Write concern | Controls how many acknowledgements a write requires. |
| Read preference | Controls which member type receives reads. |
| Read concern | Controls what consistency level a read expects. |

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

## Sharded cluster components

| Component | What it does |
| --- | --- |
| Shard | Holds a subset of the data, usually as a replica set. |
| `mongos` router | Routes client operations to the correct shard or shards. |
| Config servers | Store cluster metadata. |
| Shard key | Field or fields used to partition data. |
| Chunk | Range of shard-key values managed by the balancer. |
| Balancer | Moves chunks to keep shards balanced. |

## Shard-key checklist

- High enough cardinality.
- Even write distribution.
- Supports common query filters.
- Avoids one tenant, status, or timestamp becoming a hot range.
- Stable enough that resharding is rare.
- Compatible with uniqueness requirements.

### Good and risky shard-key examples

```text
better: { tenantId: 1, orderId: 1 }
risky:  { status: 1 }
risky:  { createdAt: 1 } for high-volume inserts
```

What it does: a tenant/order key can support targeted lookups, while low-cardinality status values or monotonically increasing timestamps can concentrate traffic.

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

### Check replica set status

```javascript
rs.status()
```

What it does: shows member state, health, optime, and election information for a replica set.

### Inspect sharding distribution

```javascript
sh.status()
```

What it does: summarizes shards, databases, sharded collections, and chunk distribution.

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
