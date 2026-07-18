# MongoDB on AWS

## Purpose

Use this page to choose how MongoDB-style workloads should run in or near AWS.

## Options

| Option | Use when | Watch for |
| --- | --- | --- |
| MongoDB Atlas on AWS | You want MongoDB-managed operations with AWS region placement. | Network peering, private endpoints, cost, and operational ownership. |
| Self-managed MongoDB on AWS | You need full control or have a specialized platform requirement. | Backup, upgrades, security, failover, and on-call burden. |
| Amazon DocumentDB | You need an AWS-managed document database compatible with selected MongoDB APIs. | Feature compatibility, query behavior, migration testing, and lock-in. |

## Decision checklist

- Verify application feature requirements against the target service.
- Test real queries, indexes, transactions, and aggregation behavior before migration.
- Define backup, restore, encryption, network access, and credential rotation.
- Keep application data modeling guidance in the database section, not only in AWS notes.

## Related links

- [MongoDB fundamentals](../../../databases/mongodb/fundamentals.md)
- [MongoDB data modeling](../../../databases/mongodb/data-modeling.md)
- [DocumentDB vs. MongoDB Atlas](documentdb-vs-mongodb-atlas.md)
- [MongoDB documentation](https://www.mongodb.com/docs/)
- [Amazon DocumentDB documentation](https://docs.aws.amazon.com/documentdb/)
- [Back to AWS databases](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
