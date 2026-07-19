# MongoDB schema validation and indexing

## Purpose

Use this guide to combine MongoDB's flexible document model with enough schema discipline and indexing to keep applications correct and queries predictable.

## How it works

MongoDB stores BSON documents in collections. The server does not require every document in a collection to have the same shape, but it can enforce validation rules and indexes.

```text
application write
  -> driver sends BSON document
  -> collection validator checks accepted shape
  -> indexes update for indexed fields
  -> write concern determines acknowledgement
```

Validation protects basic structure. Indexes make query access paths efficient. They solve different problems and should be designed together.

## Components

| Component | What it does |
| --- | --- |
| Collection | Stores related documents. |
| BSON document | Record with typed fields and nested structures. |
| Validator | Enforces database-side rules for accepted documents. |
| Index | Data structure that speeds reads and can enforce uniqueness. |
| Query planner | Chooses how MongoDB executes a query. |
| Explain plan | Shows whether a query used an index and how much work it did. |
| Schema version | Field that helps applications migrate document shapes safely. |

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

### Create a collection with validation

```javascript
db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["orderId", "customerId", "status", "createdAt"],
      properties: {
        orderId: { bsonType: "string" },
        customerId: { bsonType: "string" },
        status: { enum: ["created", "paid", "cancelled"] },
        createdAt: { bsonType: "date" }
      }
    }
  }
})
```

What it does: rejects documents that miss required fields or use an unsupported order status.

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

### Create compound and unique indexes

```javascript
db.orders.createIndex(
  { tenantId: 1, orderId: 1 },
  { unique: true }
)

db.orders.createIndex(
  { customerId: 1, createdAt: -1 }
)
```

What it does: the first index enforces tenant-scoped order uniqueness; the second supports listing a customer's recent orders.

### Create a TTL index

```javascript
db.sessions.createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0 }
)
```

What it does: expires session documents after the timestamp stored in `expiresAt`.

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

## Review checklist

- Does every collection have documented access patterns?
- Are required fields enforced by application and database validation where appropriate?
- Are indexes tied to real queries?
- Are unique constraints enforced where identity requires them?
- Are large arrays and unbounded embedded documents avoided?
- Are explain plans reviewed for high-traffic queries?
- Are indexes monitored for size and write overhead?

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
