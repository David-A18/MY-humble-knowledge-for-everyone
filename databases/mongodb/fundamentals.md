# MongoDB fundamentals

## Purpose

Use this page to understand MongoDB's core data model and when document databases are useful.

## Core concepts

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Document | BSON object containing fields and nested structures. | It is the main unit MongoDB stores and returns. |
| Collection | Group of documents. | It is roughly analogous to a table, but schema can vary. |
| `_id` | Unique primary key for each document. | Every document needs a stable identity. |
| Aggregation pipeline | Ordered stages that transform and summarize data. | It supports analytics and complex query workflows. |
| Replica set | Group of MongoDB nodes with one primary and secondaries. | It provides high availability and failover. |
| Sharding | Horizontal partitioning across shards. | It supports growth beyond one replica set. |

## Practical mental model

MongoDB works well when application data naturally forms aggregates, such as orders with line items or profiles with preferences. Flexible schema helps iteration, but production systems still need validation, indexes, migration habits, and clear ownership of document shape.

> [!IMPORTANT]
> Flexible schema does not mean no schema. It means the application and database can evolve schema with less coupling than a rigid table design.

## Related links

- [MongoDB documentation](https://www.mongodb.com/docs/manual/)
- [MongoDB data modeling](data-modeling.md)
- [MongoDB operations](operations.md)
- [Relational vs. document databases](../relational-vs-document-databases.md)
- [Back to MongoDB index](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
