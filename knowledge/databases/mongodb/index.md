# MongoDB

MongoDB knowledge for document modeling, indexing, replication, sharding, operations, and cloud deployment choices.

Start with [Relational vs. document databases](../relational-vs-document-databases.md)
for the basic order example, then use [MongoDB fundamentals](fundamentals.md)
to follow one support ticket through the document, query, and deployment model.

## Articles

| Article | Purpose |
| --- | --- |
| [MongoDB fundamentals](fundamentals.md) | Understand documents, collections, `_id`, embedding and references, validation, indexes, replica sets, and sharding. |
| [MongoDB data modeling](data-modeling.md) | Decide what to embed or reference by following the reads, updates, and growth of one support ticket. |
| [Schema validation and indexing](schema-validation-and-indexing.md) | Distinguish the document-shape rule from the index that supports a ticket query. |
| [Replication, sharding, and consistency](replication-sharding-and-consistency.md) | Tell apart replicated copies, sharded data, and read and write concern choices. |
| [MongoDB operations](operations.md) | Trace a reader symptom through application, query, member, shard, and recovery evidence before changing MongoDB. |

## Related choice guide

- [MongoDB on AWS](../../cloud/aws/databases/mongodb-on-aws.md) compares Atlas,
  self-managed MongoDB, and AWS integration choices after the fundamentals.

[Back to databases index](../index.md) | [Back to knowledge index](../../index.md)
