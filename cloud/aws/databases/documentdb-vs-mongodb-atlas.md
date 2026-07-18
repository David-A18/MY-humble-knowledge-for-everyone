# DocumentDB vs. MongoDB Atlas

## Purpose

Use this page to compare Amazon DocumentDB and MongoDB Atlas for MongoDB-oriented workloads on AWS.

## Comparison

| Area | Amazon DocumentDB | MongoDB Atlas |
| --- | --- | --- |
| Provider | AWS managed service. | MongoDB managed service running on cloud infrastructure. |
| Compatibility | MongoDB-compatible API with service-specific limits and differences. | Native MongoDB service with MongoDB-managed feature support. |
| Operations | Integrated with AWS networking, IAM-adjacent controls, CloudWatch, and AWS billing. | MongoDB operational tooling, backups, upgrades, and cross-cloud options. |
| Migration risk | Requires compatibility testing for features, drivers, indexes, and queries. | Requires network, cost, and organization integration decisions. |

## Decision rule

Choose after testing the actual workload. Compatibility claims are not a substitute for running representative queries, transactions, aggregations, indexes, and failover scenarios.

## Related links

- [MongoDB on AWS](mongodb-on-aws.md)
- [MongoDB operations](../../../databases/mongodb/operations.md)
- [Amazon DocumentDB documentation](https://docs.aws.amazon.com/documentdb/)
- [MongoDB Atlas documentation](https://www.mongodb.com/docs/atlas/)
- [Back to AWS databases](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
