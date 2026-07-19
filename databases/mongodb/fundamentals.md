# MongoDB fundamentals

## Purpose

Use this page to understand MongoDB's core data model and when document databases are useful.

## What MongoDB does

MongoDB stores application data as BSON documents in collections. It is designed around document aggregates, flexible schema evolution, indexing, replication, sharding, and an aggregation pipeline for querying and transformation.

It is a good fit when application records are naturally read and written together as documents. It is less natural when strict relational constraints and complex joins are the main model.

## Core concepts

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Document | BSON object containing fields and nested structures. | It is the main unit MongoDB stores and returns. |
| Collection | Group of documents. | It is roughly analogous to a table, but schema can vary. |
| `_id` | Unique primary key for each document. | Every document needs a stable identity. |
| Aggregation pipeline | Ordered stages that transform and summarize data. | It supports analytics and complex query workflows. |
| Replica set | Group of MongoDB nodes with one primary and secondaries. | It provides high availability and failover. |
| Sharding | Horizontal partitioning across shards. | It supports growth beyond one replica set. |

## How it works

```text
application driver
  -> mongod or mongos
  -> collection
  -> BSON document
  -> indexes
  -> replica set or sharded cluster
```

For a replica set, writes go to the primary and replicate to secondaries. For a sharded cluster, routers send operations to the shard or shards that own matching shard-key ranges.

## Practical mental model

MongoDB works well when application data naturally forms aggregates, such as orders with line items or profiles with preferences. Flexible schema helps iteration, but production systems still need validation, indexes, migration habits, and clear ownership of document shape.

> [!IMPORTANT]
> Flexible schema does not mean no schema. It means the application and database can evolve schema with less coupling than a rigid table design.

## Document example

```json
{
  "_id": "ORD-7842",
  "customerId": "CUST-52",
  "status": "paid",
  "items": [
    { "sku": "BOOK-1", "quantity": 1, "price": 29.99 }
  ],
  "createdAt": "2026-07-18T09:30:00Z"
}
```

What it does: stores an order and its line items together when the application usually reads them together.

## Related links

- [MongoDB documentation](https://www.mongodb.com/docs/manual/)
- [MongoDB data modeling](data-modeling.md)
- [Schema validation and indexing](schema-validation-and-indexing.md)
- [Replication, sharding, and consistency](replication-sharding-and-consistency.md)
- [MongoDB operations](operations.md)
- [Relational vs. document databases](../relational-vs-document-databases.md)
- [Back to MongoDB index](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
