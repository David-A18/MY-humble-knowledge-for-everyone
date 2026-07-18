# MongoDB operations

## Purpose

Use this page to operate MongoDB with attention to query performance, replication, sharding, backup, and recovery.

## Operational checks

| Area | Check | Why it matters |
| --- | --- | --- |
| Indexes | Query plans and index usage. | Missing or unused indexes create slow reads and high CPU. |
| Replication | Replica lag and primary health. | Lag affects failover and read freshness. |
| Sharding | Chunk distribution and shard key quality. | Poor distribution creates hot shards. |
| Backup | Recovery point and restore tests. | Backups only matter when restores work. |
| Security | Authentication, authorization, TLS, and audit needs. | Databases often hold sensitive business data. |

## Performance investigation sequence

1. Identify the slow operation and collection.
2. Check the filter, sort, projection, and index coverage.
3. Review document size and result cardinality.
4. Check whether writes, locks, or replication lag are contributing.
5. Confirm whether the workload belongs in MongoDB or in an analytical system.

## Related links

- [MongoDB fundamentals](fundamentals.md)
- [MongoDB data modeling](data-modeling.md)
- [MongoDB operations documentation](https://www.mongodb.com/docs/manual/administration/)
- [Back to MongoDB index](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
