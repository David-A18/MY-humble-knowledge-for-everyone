# MongoDB schema validation and indexing

## Purpose

Use this guide to combine MongoDB's flexible document model with enough schema discipline and indexing to keep applications correct and queries predictable.

## Flexible schema does not mean no schema

MongoDB collections can accept documents with different shapes, but production applications still need a documented contract.

| Tool | Use it for |
| --- | --- |
| Application validation | Fast feedback before a write reaches the database. |
| JSON Schema validation | Database-side guardrails for required fields and types. |
| Unique indexes | Enforce identity or uniqueness rules. |
| Partial indexes | Index only documents matching a filter. |
| TTL indexes | Expire documents based on a date field. |
| Schema version field | Support gradual document evolution. |

## Validation strategy

| Situation | Suggested approach |
| --- | --- |
| New collection | Start with required identity, ownership, and lifecycle fields. |
| Existing messy collection | Add validation in warning mode or validate in application first. |
| Multi-version documents | Add `schemaVersion` and migration logic. |
| Compliance-sensitive data | Validate required classification and retention fields. |
| Expiring records | Pair TTL index expectations with date-field validation. |

### Example schema version field

```json
{
  "_id": "ORD-7842",
  "schemaVersion": 2,
  "customerId": "CUST-52",
  "status": "paid",
  "createdAt": "2026-07-18T09:30:00Z"
}
```

What it does: lets readers and migration code understand which document contract the record follows.

## Index design

Design indexes from access patterns, not from every field name.

| Query pattern | Candidate index |
| --- | --- |
| Find one tenant's order by ID | `{ tenantId: 1, orderId: 1 }` unique if order IDs are tenant-scoped. |
| List recent orders for a customer | `{ customerId: 1, createdAt: -1 }` |
| Expire login sessions | TTL index on `expiresAt`. |
| Query array values | Multikey index on the array field. |
| Filter active records only | Partial index with active-status filter. |

> [!IMPORTANT]
> Indexes improve reads but add write cost. High-write collections need fewer, more intentional indexes.

## Explain-plan checks

Use explain plans when a query is slow, expensive, or new.

```javascript
db.orders.find({
  customerId: "CUST-52",
  createdAt: { $gte: ISODate("2026-07-01T00:00:00Z") }
}).sort({ createdAt: -1 }).explain("executionStats")
```

What it does: shows whether MongoDB can use an index and how many documents are examined.

## Common mistakes

| Mistake | Consequence |
| --- | --- |
| Treating every flexible document shape as acceptable. | Application code fills with special cases. |
| Creating indexes for every field. | Writes slow down and memory pressure rises. |
| Ignoring compound index order. | Sorts or filters cannot use the index effectively. |
| Relying on unique indexes without migration planning. | Existing duplicates can block rollout. |
| Using TTL without validating the date field. | Records may not expire as expected. |

## Related links

- Official documentation: [MongoDB schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- Official documentation: [MongoDB indexes](https://www.mongodb.com/docs/manual/indexes/)
- Official documentation: [MongoDB TTL indexes](https://www.mongodb.com/docs/manual/core/index-ttl/)
- [MongoDB fundamentals](fundamentals.md)
- [MongoDB data modeling](data-modeling.md)
- [MongoDB operations](operations.md)
- [Back to MongoDB](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
