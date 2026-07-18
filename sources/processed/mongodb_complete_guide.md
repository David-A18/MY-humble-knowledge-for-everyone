# MongoDB Complete Guide

> A practical, in-depth study guide to MongoDB and its differences from PostgreSQL, MySQL, and MariaDB.
>
> **Last reviewed:** 18 July 2026
> **Audience:** developers, cloud engineers, DevOps engineers, solution architects, and database beginners
> **Scope:** concepts, architecture, data modeling, queries, transactions, scaling, availability, security, operations, AWS options, examples, and database-selection guidance

---

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [Database concepts you should understand first](#2-database-concepts-you-should-understand-first)
3. [What MongoDB is](#3-what-mongodb-is)
4. [MongoDB terminology and architecture](#4-mongodb-terminology-and-architecture)
5. [BSON documents and data types](#5-bson-documents-and-data-types)
6. [Flexible schema and schema validation](#6-flexible-schema-and-schema-validation)
7. [Relational modeling versus document modeling](#7-relational-modeling-versus-document-modeling)
8. [Embedding versus referencing](#8-embedding-versus-referencing)
9. [MongoDB CRUD operations](#9-mongodb-crud-operations)
10. [MongoDB aggregation pipelines](#10-mongodb-aggregation-pipelines)
11. [MongoDB indexes and query performance](#11-mongodb-indexes-and-query-performance)
12. [Atomicity, ACID, transactions, and concurrency](#12-atomicity-acid-transactions-and-concurrency)
13. [Read concern, write concern, and read preference](#13-read-concern-write-concern-and-read-preference)
14. [Replication and high availability](#14-replication-and-high-availability)
15. [Horizontal scaling and sharding](#15-horizontal-scaling-and-sharding)
16. [Storage, memory, and the WiredTiger engine](#16-storage-memory-and-the-wiredtiger-engine)
17. [Change streams and event-driven applications](#17-change-streams-and-event-driven-applications)
18. [Security fundamentals](#18-security-fundamentals)
19. [Backup, recovery, and disaster recovery](#19-backup-recovery-and-disaster-recovery)
20. [MongoDB deployment options](#20-mongodb-deployment-options)
21. [MongoDB on AWS](#21-mongodb-on-aws)
22. [MongoDB Atlas versus Amazon DocumentDB](#22-mongodb-atlas-versus-amazon-documentdb)
23. [PostgreSQL explained](#23-postgresql-explained)
24. [MySQL explained](#24-mysql-explained)
25. [MariaDB explained](#25-mariadb-explained)
26. [MongoDB versus PostgreSQL](#26-mongodb-versus-postgresql)
27. [MongoDB versus MySQL](#27-mongodb-versus-mysql)
28. [MongoDB versus MariaDB](#28-mongodb-versus-mariadb)
29. [MySQL versus MariaDB](#29-mysql-versus-mariadb)
30. [Complete comparison matrix](#30-complete-comparison-matrix)
31. [One e-commerce domain modeled in MongoDB and SQL](#31-one-e-commerce-domain-modeled-in-mongodb-and-sql)
32. [When MongoDB is a strong choice](#32-when-mongodb-is-a-strong-choice)
33. [When a relational database is a stronger choice](#33-when-a-relational-database-is-a-stronger-choice)
34. [Common MongoDB mistakes and anti-patterns](#34-common-mongodb-mistakes-and-anti-patterns)
35. [Performance investigation workflow](#35-performance-investigation-workflow)
36. [Migration considerations](#36-migration-considerations)
37. [A practical local laboratory](#37-a-practical-local-laboratory)
38. [Learning path and checklist](#38-learning-path-and-checklist)
39. [Interview questions and model answers](#39-interview-questions-and-model-answers)
40. [Final decision framework](#40-final-decision-framework)
41. [Official references](#41-official-references)

---

# 1. Executive summary

MongoDB is a **document-oriented database**. It stores application records as BSON documents in collections. A document can contain scalar values, nested objects, and arrays, so one record can represent an entire application aggregate such as a customer profile, product catalog entry, or order.

PostgreSQL, MySQL, and MariaDB are primarily **relational database management systems**. They normally represent information in tables composed of rows and columns. Relationships between independent entities are expressed through primary keys, foreign keys, and joins.

The most important distinction is therefore not simply **SQL versus NoSQL**. It is:

> **Relational modeling versus document-oriented modeling.**

A relational model typically asks:

> Which independent entities exist, and how should they be normalized and related?

A document model typically asks:

> Which data belongs to the same business aggregate, has the same lifecycle, and is usually read or updated together?

MongoDB is particularly attractive when application data is naturally hierarchical, records have variable attributes, an aggregate can be retrieved as one document, and horizontal distribution is an important architectural requirement.

A relational database is usually preferable when relationships are central, database-enforced referential integrity is essential, transactions frequently span multiple business entities, and users need complex ad hoc SQL queries or reporting.

A practical default is:

- Start with **PostgreSQL** when requirements are uncertain and the system contains important relationships.
- Choose **MongoDB deliberately** when the application has a clear document/aggregate model.
- Choose **MySQL** when the organization, application, or vendor ecosystem is already standardized on MySQL.
- Choose **MariaDB** when the organization intentionally wants the MariaDB ecosystem and has validated compatibility requirements.

---

# 2. Database concepts you should understand first

Before comparing database products, it helps to separate several concepts that are often mixed together.

## 2.1 Database management system

A database management system, or DBMS, is software that stores, retrieves, protects, and manages data. It normally provides:

- A data model.
- A query and update interface.
- Concurrency control.
- Durability and recovery mechanisms.
- Authentication and authorization.
- Indexes and query optimization.
- Replication, backup, or clustering capabilities.

MongoDB, PostgreSQL, MySQL, and MariaDB are DBMS products.

## 2.2 Data model

The data model determines how information is represented.

Common models include:

- **Relational:** tables, rows, columns, keys, and joins.
- **Document:** documents containing fields, nested documents, and arrays.
- **Key-value:** opaque values addressed by a key.
- **Graph:** vertices and edges optimized for traversing relationships.
- **Wide-column:** sparse, distributed rows organized into column families.
- **Time series:** records optimized around timestamps, measurements, and retention.

MongoDB is document-oriented, although it also supports specialized capabilities such as time-series collections, geospatial indexes, text search integrations, and vector-search functionality in its wider platform.

## 2.3 Database engine versus managed service

A database engine is the actual database software. A managed database service operates an engine or a compatible implementation for you.

Examples:

- MongoDB Server is the database engine.
- MongoDB Atlas is MongoDB's managed cloud service.
- PostgreSQL is an engine; Amazon RDS for PostgreSQL is a managed AWS service for it.
- MySQL is an engine; Amazon RDS for MySQL and Amazon Aurora MySQL-Compatible Edition are managed AWS services.
- MariaDB is an engine; Amazon RDS for MariaDB is a managed service.
- Amazon DocumentDB is an AWS-managed document database with MongoDB API compatibility, but it is not the MongoDB server engine.

This distinction matters because API compatibility does not guarantee identical features, behavior, performance, operational tooling, or release cadence.

## 2.4 OLTP and OLAP

**Online transaction processing**, or OLTP, describes operational workloads such as:

- Creating orders.
- Updating account balances.
- Registering users.
- Reserving inventory.
- Recording application events.

OLTP systems normally require low-latency reads and writes, concurrency control, and reliable transactions.

**Online analytical processing**, or OLAP, describes analytical workloads such as:

- Large scans.
- Historical trend analysis.
- Complex aggregations.
- Business intelligence reports.
- Data warehouse queries.

MongoDB, PostgreSQL, MySQL, and MariaDB are commonly used for OLTP. They can perform analytical queries, but very large analytical workloads are often moved to dedicated analytical systems or data warehouses.

## 2.5 Scale up and scale out

**Vertical scaling**, or scaling up, means giving one server more CPU, memory, or storage.

**Horizontal scaling**, or scaling out, means distributing load and data across more servers.

Relational databases can scale horizontally, but the architecture may require read replicas, partitioning, middleware, a distributed SQL extension, or application-level sharding.

MongoDB includes a native sharded-cluster model in which collections can be partitioned across shards and requests can be routed through `mongos` processes.

---

# 3. What MongoDB is

MongoDB is a general-purpose document database. It stores records as BSON documents inside collections.

A simple document looks like this:

```javascript
{
  _id: ObjectId("66a812d2caa85186d723c917"),
  name: "Alice Smith",
  email: "alice@example.com",
  active: true,
  createdAt: ISODate("2026-07-18T08:30:00Z"),
  address: {
    street: "Gran Via 20",
    city: "Madrid",
    postalCode: "28013",
    country: "Spain"
  },
  skills: ["AWS", "Kubernetes", "Terraform"]
}
```

This document contains:

- A unique identifier.
- Strings.
- A Boolean.
- A date.
- An embedded address document.
- An array of skills.

The structure resembles an object used in JavaScript, Python, Java, Go, C#, or another programming language. This can reduce the amount of object-relational mapping required between application objects and normalized SQL tables.

## 3.1 What MongoDB is not

MongoDB is not:

- A replacement for every relational database.
- A database without a schema.
- A system without transactions.
- Automatically scalable without design work.
- Automatically faster than SQL.
- Identical to Amazon DocumentDB.
- A reason to ignore integrity, indexes, backups, or capacity planning.

MongoDB changes the modeling strategy, but it does not remove the need for database engineering.

## 3.2 Why MongoDB became popular

MongoDB is popular because it offers a combination of:

- A developer-friendly document model.
- Native nested documents and arrays.
- Flexible schemas.
- Rich queries and aggregation pipelines.
- Secondary indexes.
- Replica sets for high availability.
- Sharding for horizontal distribution.
- Multi-document transactions when needed.
- Drivers for common programming languages.
- Managed operation through MongoDB Atlas.

---

# 4. MongoDB terminology and architecture

The following mapping is useful when moving from relational databases to MongoDB.

| Relational concept | MongoDB concept | Important qualification |
|---|---|---|
| Database | Database | Similar organizational boundary |
| Table | Collection | A collection contains BSON documents |
| Row | Document | A document may include nested data and arrays |
| Column | Field | Documents in one collection can have different fields |
| Primary key | `_id` | Every document requires a unique `_id` value |
| Child table | Embedded array/document or another collection | The choice depends on access patterns and lifecycle |
| Foreign key | Stored reference value | MongoDB does not provide SQL-style foreign-key constraints between collections |
| Join | `$lookup`, embedding, or application logic | Embedding is often preferred for tightly coupled data |
| SQL aggregation | Aggregation pipeline | Pipelines process documents through stages |
| Schema migration | Validation/model evolution | Flexible documents still need controlled evolution |

## 4.1 Core server processes

A self-managed MongoDB environment commonly includes:

- **`mongod`:** the database server process that stores data and responds to operations.
- **`mongos`:** a query router used in a sharded cluster.
- **Config server replica set:** stores metadata for a sharded cluster.
- **MongoDB Shell (`mongosh`):** interactive command-line client.
- **Drivers:** application libraries that connect to MongoDB.
- **MongoDB Compass:** graphical client and exploration tool.

## 4.2 Basic standalone architecture

```text
Application
    |
MongoDB driver
    |
Standalone mongod
    |
Data files and journal
```

A standalone server is useful for learning or limited development scenarios. It is not the preferred architecture for a production system requiring high availability.

## 4.3 Replica-set architecture

```text
                    +----------------+
Application ------> | Primary mongod | <--- accepts writes
                    +----------------+
                       |          |
                       | oplog    | oplog
                       v          v
                +-----------+  +-----------+
                | Secondary |  | Secondary |
                +-----------+  +-----------+
```

A replica set is a group of `mongod` processes that maintain copies of the same data. The primary accepts writes. Secondary members replicate changes and can participate in elections.

## 4.4 Sharded-cluster architecture

```text
Applications
     |
MongoDB drivers
     |
+--------------------+
| mongos routers     |
+--------------------+
   |       |       |
   v       v       v
Shard A  Shard B  Shard C
(replica (replica (replica
 set)     set)     set)

Config server replica set
stores cluster metadata
```

Each production shard is normally a replica set. This combines horizontal data distribution with redundancy inside each shard.

---

# 5. BSON documents and data types

MongoDB stores records in **BSON**, a binary serialization format related to JSON. BSON supports types not represented cleanly by ordinary JSON, including dates, binary data, decimals, timestamps, regular expressions, and `ObjectId` values.

## 5.1 Common BSON types

Common types include:

- String.
- Boolean.
- 32-bit integer.
- 64-bit integer.
- Double.
- Decimal128.
- Date.
- Timestamp.
- ObjectId.
- Array.
- Embedded document.
- Binary data.
- Null.
- Regular expression.

## 5.2 Choosing numeric types carefully

Do not treat every numeric value as an interchangeable JavaScript number.

For example:

- Use integers for counters where appropriate.
- Use `Decimal128` for decimal values such as money when exact decimal representation is required.
- Avoid floating-point types for financial values unless rounding behavior is explicitly acceptable.

Example:

```javascript
{
  sku: "KEYBOARD-001",
  unitPrice: NumberDecimal("99.90"),
  stock: NumberInt(25)
}
```

## 5.3 The `_id` field

Every MongoDB document must contain an `_id` field. If the application does not provide one, the driver or server normally generates an `ObjectId`.

Properties of `_id`:

- It must be unique within the collection.
- MongoDB creates a unique index on `_id`.
- It can use a type other than `ObjectId`, provided values are unique and valid.
- It should be stable. Treat changing identity values as a design smell.

Natural business identifiers such as email addresses can change. A stable technical identifier is often safer, while a unique secondary index can enforce uniqueness of the business field.

```javascript
db.customers.createIndex(
  { email: 1 },
  { unique: true }
)
```

## 5.4 Document-size limit

A BSON document has a maximum size of **16 mebibytes**. This limit is one reason unbounded arrays are dangerous.

Do not create a document such as:

```javascript
{
  userId: "user-1",
  everyEventEverGenerated: [ /* grows forever */ ]
}
```

Instead, store high-volume events in their own collection or use a bounded bucketing strategy.

For files larger than the document limit, MongoDB offers GridFS. In many cloud architectures, however, the preferred pattern is to store the binary object in object storage such as Amazon S3 and store only metadata and the object key in the database.

---

# 6. Flexible schema and schema validation

MongoDB collections use a flexible schema by default. Documents in the same collection do not have to contain exactly the same fields.

Example:

```javascript
{
  _id: 1,
  type: "physical",
  name: "Mechanical Keyboard",
  weightKg: 0.9,
  layout: "ISO-ES"
}
```

```javascript
{
  _id: 2,
  type: "software",
  name: "Monitoring Platform",
  licenseType: "subscription",
  billingPeriod: "monthly"
}
```

This can be useful for a product catalog where product categories have different attributes.

## 6.1 Flexible schema does not mean no schema

Every production application has a schema, whether it is written down or not. The schema may live in:

- Application classes.
- API contracts.
- Validation libraries.
- Collection validators.
- Documentation.
- Migration scripts.
- Data-quality monitoring.

Without governance, schema flexibility can create:

- Misspelled fields such as `email`, `eMail`, and `emailAddress`.
- Mixed data types in one field.
- Documents that old application versions cannot understand.
- Indexes that work for only part of the collection.
- Difficult analytics and migrations.

## 6.2 JSON Schema validation

MongoDB can validate documents using `$jsonSchema` and query expressions.

```javascript
db.createCollection("customers", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email", "status", "createdAt"],
      properties: {
        name: {
          bsonType: "string",
          minLength: 1,
          description: "Customer name is required"
        },
        email: {
          bsonType: "string",
          description: "Email must be stored as a string"
        },
        status: {
          enum: ["active", "suspended", "closed"]
        },
        age: {
          bsonType: ["int", "null"],
          minimum: 18
        },
        createdAt: {
          bsonType: "date"
        }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})
```

A strong production approach is:

1. Define the document contract.
2. Validate it in the application.
3. Add database validation for critical invariants.
4. Version the schema when evolution is nontrivial.
5. Monitor validation failures.

## 6.3 Schema-versioning pattern

A document can include a schema version:

```javascript
{
  _id: ObjectId("..."),
  schemaVersion: 2,
  name: "Alice Smith",
  contact: {
    email: "alice@example.com",
    phone: "+34..."
  }
}
```

Application code can then:

- Read old and new versions during a transition.
- Migrate documents lazily when accessed.
- Run an offline backfill.
- Remove legacy handling after migration is complete.

Flexible schemas make gradual migrations possible, but the migration still needs a controlled plan.

---

# 7. Relational modeling versus document modeling

## 7.1 Relational normalization

Relational design commonly uses normalization to reduce duplication and update anomalies.

An e-commerce system might contain:

```text
customers
addresses
orders
order_items
products
categories
payments
shipments
```

Each entity exists in a table, and relationships are represented with keys.

Advantages include:

- Strong referential integrity.
- One authoritative representation of shared entities.
- Flexible joins between entities.
- Efficient updates to shared information.
- A mature declarative query model.

## 7.2 Document aggregates

Document modeling often groups data around an aggregate boundary.

An order document might contain:

```javascript
{
  _id: ObjectId("..."),
  orderNumber: "ORD-2026-0001",
  status: "paid",
  customer: {
    customerId: ObjectId("..."),
    nameAtPurchase: "Alice Smith",
    emailAtPurchase: "alice@example.com"
  },
  shippingAddress: {
    street: "Gran Via 20",
    city: "Madrid",
    postalCode: "28013",
    country: "Spain"
  },
  items: [
    {
      productId: ObjectId("..."),
      sku: "KEY-001",
      nameAtPurchase: "Mechanical Keyboard",
      quantity: 1,
      unitPrice: NumberDecimal("99.90")
    }
  ],
  total: NumberDecimal("99.90"),
  createdAt: ISODate("2026-07-18T08:30:00Z")
}
```

Notice that names and prices are snapshots. This duplication can be intentional: an old order should normally preserve what the customer purchased and the price paid, even if the product catalog changes later.

## 7.3 Denormalization is not automatically bad

In a relational database, unnecessary duplication is often considered a problem. In a document database, controlled denormalization can be a performance and consistency strategy.

The important questions are:

- Is the duplicated value historical or current?
- Which copy is authoritative?
- How often does it change?
- How many documents would need updating?
- Is eventual synchronization acceptable?
- Does duplication eliminate a high-volume join?

An order's product name at purchase is historical and should normally remain unchanged. A user's current legal name may need one authoritative source.

## 7.4 Model for access patterns

MongoDB data modeling should start with the operations the application must perform.

For each operation, document:

- Query filter.
- Sort order.
- Fields returned.
- Expected result count.
- Read frequency.
- Write frequency.
- Latency objective.
- Consistency requirement.
- Expected data growth.

Then design documents and indexes to support those operations.

This is different from beginning only with an entity-relationship diagram and assuming the database optimizer will efficiently assemble all required shapes later.

---

# 8. Embedding versus referencing

This is the central MongoDB modeling decision.

## 8.1 Embedding

Embedding stores related data inside a parent document.

```javascript
{
  _id: ObjectId("..."),
  name: "Alice Smith",
  addresses: [
    {
      type: "home",
      street: "Gran Via 20",
      city: "Madrid"
    },
    {
      type: "work",
      street: "Paseo de la Castellana 100",
      city: "Madrid"
    }
  ]
}
```

Embedding is usually appropriate when:

- The child data belongs exclusively to the parent.
- Parent and child share a lifecycle.
- The data is usually read together.
- The data is usually updated together.
- The number of child elements is bounded.
- Atomic modification of the aggregate is valuable.

Benefits:

- One read can retrieve the complete aggregate.
- One document update is atomic.
- Fewer joins or application round trips.
- The schema reflects the application's object shape.

Risks:

- Large documents.
- Repeated data.
- Unbounded array growth.
- Updating many duplicated copies.
- Writing a large document when only one small nested value changes, depending on the workload and storage behavior.

## 8.2 Referencing

Referencing stores a related document's identifier.

```javascript
// customers
{
  _id: ObjectId("64a..."),
  name: "Alice Smith"
}
```

```javascript
// orders
{
  _id: ObjectId("64b..."),
  customerId: ObjectId("64a..."),
  total: NumberDecimal("99.90")
}
```

Referencing is usually appropriate when:

- The related entity exists independently.
- Many documents share it.
- It changes frequently.
- The relationship is many-to-many.
- The number of related elements is unbounded.
- The related data is not normally required in the same operation.

Benefits:

- Less duplication.
- Independent lifecycles.
- Smaller documents.
- One authoritative source for shared information.

Costs:

- Multiple application queries or `$lookup`.
- Weaker cross-collection integrity than SQL foreign keys.
- More complex transaction boundaries.

## 8.3 `$lookup`

MongoDB supports join-like operations through the aggregation framework.

```javascript
db.orders.aggregate([
  {
    $match: { status: "paid" }
  },
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
    }
  },
  {
    $unwind: "$customer"
  }
])
```

`$lookup` is useful, but it should not become an excuse to reproduce a highly normalized SQL design mechanically inside MongoDB.

If nearly every operation requires several complex cross-collection joins, a relational database may be a more natural choice.

## 8.4 Cardinality decision guide

| Relationship | Typical MongoDB option | Reasoning |
|---|---|---|
| One-to-one, same lifecycle | Embed | Keeps aggregate together |
| One-to-few, bounded | Embed | Efficient single-document access |
| One-to-many, unbounded | Reference | Avoids unlimited document growth |
| Many-to-many | Reference/bridge collection | Avoids large duplicated arrays |
| Historical snapshot | Embed copied fields | Preserves state at the time of the event |
| Shared, frequently updated entity | Reference | Maintains one authoritative copy |

## 8.5 Useful document-modeling patterns

### Extended-reference pattern

Copy a small subset of frequently read fields from a referenced document.

```javascript
{
  orderNumber: "ORD-1",
  customer: {
    id: ObjectId("..."),
    displayName: "Alice Smith",
    tier: "gold"
  }
}
```

Keep the customer ID for identity, while copying fields needed for fast reads. Define whether copied fields are historical snapshots or synchronized current values.

### Subset pattern

Store the most frequently needed subset in the main document and place large or infrequently used data elsewhere.

Example: product summary in `products`; long audit history in `product_audit_events`.

### Bucket pattern

Group many small time-based records into bounded documents.

```javascript
{
  sensorId: "sensor-17",
  hour: ISODate("2026-07-18T08:00:00Z"),
  measurements: [
    { minute: 0, value: 21.3 },
    { minute: 1, value: 21.4 }
  ],
  count: 2
}
```

This can reduce per-document overhead and index volume, but bucket size and update contention must be considered.

### Computed pattern

Precompute expensive values that are read frequently and updated less often.

```javascript
{
  productId: ObjectId("..."),
  ratingSummary: {
    count: 1820,
    average: 4.63
  }
}
```

You must define how the computed value is updated and repaired.

---

# 9. MongoDB CRUD operations

CRUD means create, read, update, and delete.

## 9.1 Create

Insert one document:

```javascript
db.customers.insertOne({
  name: "Alice Smith",
  email: "alice@example.com",
  status: "active",
  createdAt: new Date()
})
```

Insert several documents:

```javascript
db.customers.insertMany([
  {
    name: "Alice Smith",
    country: "Spain",
    status: "active"
  },
  {
    name: "John Murphy",
    country: "Ireland",
    status: "active"
  }
])
```

## 9.2 Read

Find all active customers:

```javascript
db.customers.find({ status: "active" })
```

Find by a nested field:

```javascript
db.customers.find({ "address.city": "Madrid" })
```

Find values in an array:

```javascript
db.customers.find({ skills: "Kubernetes" })
```

Comparison operators:

```javascript
db.products.find({
  price: { $gte: 50, $lte: 200 },
  stock: { $gt: 0 }
})
```

Logical operators:

```javascript
db.customers.find({
  $or: [
    { country: "Spain" },
    { tier: "gold" }
  ]
})
```

Projection:

```javascript
db.customers.find(
  { status: "active" },
  { name: 1, email: 1, _id: 0 }
)
```

Sort and limit:

```javascript
db.orders
  .find({ customerId: ObjectId("...") })
  .sort({ createdAt: -1 })
  .limit(20)
```

## 9.3 Update

Update one document:

```javascript
db.customers.updateOne(
  { email: "alice@example.com" },
  {
    $set: {
      status: "suspended",
      updatedAt: new Date()
    },
    $inc: {
      statusChangeCount: 1
    }
  }
)
```

Add a value to an array without duplicates:

```javascript
db.customers.updateOne(
  { _id: ObjectId("...") },
  { $addToSet: { skills: "MongoDB" } }
)
```

Remove an array value:

```javascript
db.customers.updateOne(
  { _id: ObjectId("...") },
  { $pull: { skills: "LegacyTool" } }
)
```

Upsert:

```javascript
db.settings.updateOne(
  { application: "checkout", environment: "production" },
  {
    $set: {
      timeoutSeconds: 30,
      updatedAt: new Date()
    },
    $setOnInsert: {
      createdAt: new Date()
    }
  },
  { upsert: true }
)
```

An upsert updates a matching document or inserts one if no match exists.

## 9.4 Delete

```javascript
db.customers.deleteOne({
  _id: ObjectId("...")
})
```

```javascript
db.sessions.deleteMany({
  expiresAt: { $lt: new Date() }
})
```

For expiration workflows, a TTL index is often better than running a manual delete repeatedly.

```javascript
db.sessions.createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0 }
)
```

## 9.5 Bulk writes

Bulk operations reduce network round trips and can group mixed writes.

```javascript
db.inventory.bulkWrite([
  {
    updateOne: {
      filter: { sku: "KEY-001" },
      update: { $inc: { stock: -1 } }
    }
  },
  {
    insertOne: {
      document: {
        sku: "MOUSE-001",
        stock: 30
      }
    }
  }
])
```

Use ordered or unordered execution based on whether later operations should continue after an error.

---

# 10. MongoDB aggregation pipelines

Aggregation pipelines process documents through ordered stages.

```text
Documents
   |
$match
   |
$unwind
   |
$group
   |
$sort
   |
$project
   |
Result
```

## 10.1 Common stages

| Stage | Purpose |
|---|---|
| `$match` | Filter documents |
| `$project` | Select, rename, or calculate fields |
| `$set` / `$addFields` | Add or replace fields |
| `$unset` | Remove fields |
| `$group` | Group documents and calculate aggregates |
| `$sort` | Sort documents |
| `$limit` | Limit result count |
| `$skip` | Skip results, often for simple pagination |
| `$unwind` | Create one output document per array element |
| `$lookup` | Join another collection |
| `$facet` | Run multiple sub-pipelines over the same input |
| `$bucket` | Group values into ranges |
| `$count` | Count documents |
| `$merge` | Merge results into a collection |
| `$out` | Write pipeline results to a collection |

## 10.2 Revenue by country example

```javascript
db.orders.aggregate([
  {
    $match: {
      status: "paid",
      createdAt: {
        $gte: ISODate("2026-01-01T00:00:00Z")
      }
    }
  },
  {
    $group: {
      _id: "$shippingAddress.country",
      orderCount: { $sum: 1 },
      totalRevenue: { $sum: "$total" },
      averageOrderValue: { $avg: "$total" }
    }
  },
  {
    $sort: { totalRevenue: -1 }
  }
])
```

Equivalent SQL:

```sql
SELECT
    shipping_country,
    COUNT(*) AS order_count,
    SUM(total) AS total_revenue,
    AVG(total) AS average_order_value
FROM orders
WHERE status = 'paid'
  AND created_at >= TIMESTAMP '2026-01-01 00:00:00'
GROUP BY shipping_country
ORDER BY total_revenue DESC;
```

## 10.3 Unwinding arrays

Suppose each order embeds items. To find the top products:

```javascript
db.orders.aggregate([
  { $match: { status: "paid" } },
  { $unwind: "$items" },
  {
    $group: {
      _id: "$items.sku",
      productName: { $first: "$items.nameAtPurchase" },
      unitsSold: { $sum: "$items.quantity" },
      revenue: {
        $sum: {
          $multiply: ["$items.quantity", "$items.unitPrice"]
        }
      }
    }
  },
  { $sort: { revenue: -1 } },
  { $limit: 10 }
])
```

## 10.4 Pipeline design advice

- Filter early with `$match`.
- Project away large unnecessary fields when it reduces memory and network use.
- Ensure fields used by early filters and sorts have appropriate indexes.
- Be cautious with `$unwind` because one input document can produce many outputs.
- Be cautious with large `$lookup` operations.
- Use `explain()` and production-like data volumes.
- Do not assume a pipeline that works on 1,000 documents will behave the same on 1 billion.

---

# 11. MongoDB indexes and query performance

Indexes let MongoDB locate documents without scanning an entire collection. The `_id` index is created automatically.

Indexes improve reads but add cost to:

- Inserts.
- Updates to indexed fields.
- Deletes.
- Storage.
- Memory usage.
- Backup and maintenance.

## 11.1 Single-field index

```javascript
db.customers.createIndex({ email: 1 })
```

## 11.2 Unique index

```javascript
db.customers.createIndex(
  { email: 1 },
  { unique: true }
)
```

Be careful when adding a unique index to existing dirty data. Duplicate values must be resolved first.

## 11.3 Compound index

```javascript
db.orders.createIndex({
  customerId: 1,
  status: 1,
  createdAt: -1
})
```

This may support:

```javascript
db.orders.find({
  customerId: ObjectId("..."),
  status: "paid"
}).sort({ createdAt: -1 })
```

Field order matters. A compound index is not an unordered set of fields.

A useful heuristic is the **ESR rule**:

1. Equality fields.
2. Sort fields.
3. Range fields.

This is a heuristic rather than a substitute for testing. Selectivity, result volume, and alternative query shapes can change the best order.

## 11.4 Multikey index

When an indexed field is an array, MongoDB creates a multikey index.

```javascript
db.customers.createIndex({ skills: 1 })
```

This supports queries such as:

```javascript
db.customers.find({ skills: "Kubernetes" })
```

Arrays can create many index entries, so large arrays increase index size and write cost.

## 11.5 Partial index

A partial index includes only documents matching a filter.

```javascript
db.orders.createIndex(
  { customerId: 1, createdAt: -1 },
  {
    partialFilterExpression: {
      status: "open"
    }
  }
)
```

This can reduce index size when only a subset needs acceleration.

## 11.6 Sparse index

A sparse index includes documents that contain the indexed field. Partial indexes are generally more expressive and often preferable for new designs.

## 11.7 TTL index

TTL indexes automatically remove expired documents.

```javascript
db.sessions.createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0 }
)
```

TTL deletion is asynchronous. Do not design security behavior that assumes a document disappears at the exact expiration millisecond.

## 11.8 Text, geospatial, wildcard, hashed, and other indexes

MongoDB supports index types for different workloads, including:

- Text search in the database engine.
- Geospatial queries.
- Hashed shard keys.
- Wildcard indexing for variable field paths.
- Clustered collection options in supported scenarios.
- Search indexes and vector-search indexes through MongoDB Atlas capabilities.

Use specialized indexes only when the query requirement justifies them.

## 11.9 Covered queries

A covered query can be answered entirely from the index without fetching the full document, provided the filter and returned fields are contained in the index and other conditions are satisfied.

Example index:

```javascript
db.customers.createIndex({
  status: 1,
  country: 1,
  email: 1
})
```

Potential query:

```javascript
db.customers.find(
  { status: "active", country: "Spain" },
  { email: 1, _id: 0 }
)
```

## 11.10 Explain plans

Use `explain()` to inspect how MongoDB executes a query.

```javascript
db.orders.find({
  customerId: ObjectId("..."),
  status: "paid"
}).sort({
  createdAt: -1
}).explain("executionStats")
```

Important fields include:

- Winning plan.
- Collection scan versus index scan.
- Documents examined.
- Index keys examined.
- Documents returned.
- Execution time.
- Sort stage behavior.

A simple diagnostic ratio is:

```text
documents examined / documents returned
```

A very high ratio can indicate an inefficient filter, an inadequate index, low selectivity, or a query that inherently reads a large part of the dataset.

## 11.11 Index anti-patterns

Avoid:

- Indexing every field.
- Creating indexes without known queries.
- Keeping obsolete indexes forever.
- Ignoring field order in compound indexes.
- Using very large arrays without considering multikey growth.
- Assuming indexes eliminate all sorting costs.
- Testing only with tiny datasets.

---

# 12. Atomicity, ACID, transactions, and concurrency

## 12.1 ACID

ACID means:

- **Atomicity:** a transaction is applied completely or not at all.
- **Consistency:** a transaction moves data from one valid state to another according to defined rules.
- **Isolation:** concurrent transactions do not produce unacceptable interference.
- **Durability:** committed data survives failures according to the configured durability guarantees.

## 12.2 Single-document atomicity

A MongoDB write to one document is atomic. This is a major reason to embed values that must change together.

Example inventory update:

```javascript
db.products.updateOne(
  {
    _id: ObjectId("..."),
    stock: { $gte: 1 }
  },
  {
    $inc: { stock: -1 },
    $push: {
      stockMovements: {
        type: "sale",
        quantity: -1,
        at: new Date()
      }
    }
  }
)
```

The stock decrement and embedded movement insertion occur as one atomic document operation.

Including the current condition in the update filter is a form of optimistic concurrency control.

## 12.3 Multi-document transactions

MongoDB supports transactions across multiple documents and collections, and supports distributed transactions in replica sets and sharded clusters.

Conceptual JavaScript example:

```javascript
const session = db.getMongo().startSession()
const bank = session.getDatabase("bank")

try {
  session.startTransaction()

  bank.accounts.updateOne(
    { _id: "account-A", balance: { $gte: 100 } },
    { $inc: { balance: -100 } },
    { session }
  )

  bank.accounts.updateOne(
    { _id: "account-B" },
    { $inc: { balance: 100 } },
    { session }
  )

  session.commitTransaction()
} catch (error) {
  session.abortTransaction()
  throw error
} finally {
  session.endSession()
}
```

Real driver code should use the driver's transaction helper, retry guidance, timeouts, and error handling.

## 12.4 Transactions are not a substitute for document design

A schema that requires a distributed transaction for every ordinary request may be fighting the document model.

Prefer:

- One-document atomic operations for natural aggregates.
- Multi-document transactions where business rules genuinely cross aggregate boundaries.
- Short transactions.
- Predictable retry behavior.
- Careful testing under failover and concurrency.

Avoid:

- Long-running interactive transactions.
- Reading huge result sets inside a transaction.
- Treating MongoDB as normalized SQL with every relation in a separate collection.

## 12.5 Concurrency control

Concurrent writes can produce lost updates if the application reads a document, modifies it locally, and writes it back without verifying that it has not changed.

A version field can help:

```javascript
{
  _id: ObjectId("..."),
  version: 7,
  status: "open"
}
```

Update only if the version matches:

```javascript
db.orders.updateOne(
  { _id: ObjectId("..."), version: 7 },
  {
    $set: { status: "paid" },
    $inc: { version: 1 }
  }
)
```

If `matchedCount` is zero, another writer may have changed the document. The application can reload and retry according to business rules.

---

# 13. Read concern, write concern, and read preference

MongoDB exposes consistency, durability, and routing controls. They should be selected according to business requirements, not copied blindly.

## 13.1 Write concern

Write concern controls the level of acknowledgment requested for a write.

Conceptual example:

```javascript
{
  w: "majority",
  j: true,
  wtimeout: 5000
}
```

Questions write concern answers include:

- Must only the primary acknowledge the write?
- Must a majority acknowledge it?
- Must the write be journaled?
- How long should the client wait?

Stronger acknowledgment generally increases confidence in durability but can add latency or reduce availability during failures.

A write-concern timeout does not always mean the write was rolled back. The application must handle ambiguous outcomes using retryable operations, idempotency, and driver guidance.

## 13.2 Read concern

Read concern controls consistency and isolation properties of reads.

The correct level depends on whether the application can tolerate:

- Reading data that is not majority committed.
- Reading a snapshot for a transaction.
- Waiting for causal or majority guarantees.

## 13.3 Read preference

Read preference controls which replica-set members can serve reads.

Common conceptual modes include:

- Primary.
- Primary preferred.
- Secondary.
- Secondary preferred.
- Nearest.

Reading from secondaries can distribute read load or support regional reads, but it can expose replication lag. It is not automatically suitable for immediately reading a value after writing it.

## 13.4 Consistency is a system property

Do not describe MongoDB simply as “eventually consistent.” Its behavior depends on:

- Deployment topology.
- Read concern.
- Write concern.
- Read preference.
- Sessions and causal consistency.
- Transactions.
- Failure conditions.

Similarly, do not assume a SQL database is always strongly consistent in every distributed topology. Read replicas and asynchronous replication can also return stale data.

---

# 14. Replication and high availability

MongoDB production deployments normally use replica sets.

## 14.1 Replica-set members

A common three-member topology contains:

- One primary.
- Two secondaries.

MongoDB documentation recommends three data-bearing members for the minimum common production replica-set configuration. An arbiter can vote but does not hold data, so it does not provide data redundancy.

## 14.2 Oplog

The primary records data changes in the operation log, or oplog. Secondary members replicate and apply oplog entries.

The oplog is capped. Its size determines the time window available for secondaries, delayed members, backups, and change-stream resume scenarios to catch up before required history is overwritten.

## 14.3 Election and failover

When the primary becomes unavailable, eligible members can elect a new primary. During election and client reconnection, writes may be temporarily unavailable.

Applications should:

- Use an official driver.
- Use a replica-set-aware connection string.
- Configure sensible server-selection and operation timeouts.
- Retry supported transient errors.
- Make business operations idempotent where possible.
- Test failover instead of assuming it works.

## 14.4 Replication is not backup

Replication protects against server failure. It does not by itself protect against:

- Accidental deletion.
- Corrupt application writes.
- Malicious changes.
- Logical data corruption replicated to every member.
- A failed migration.
- An operator dropping a collection.

Backups and point-in-time recovery are separate controls.

## 14.5 Multi-region architecture

Replica sets can span regions, but topology design must account for:

- Voting majority.
- Network latency.
- Write latency.
- Region failure.
- Split-brain prevention.
- Data sovereignty.
- Cost.

Placing members equally across two regions can create quorum problems. Production designs normally place a voting majority in a preferred region or use a carefully designed three-region topology.

---

# 15. Horizontal scaling and sharding

Sharding distributes collection data across multiple shards.

## 15.1 Why shard

Sharding may be required when:

- The dataset no longer fits economically on one replica set.
- The working set exceeds available memory.
- Write throughput exceeds one replica set's capacity.
- Read throughput cannot be met by replicas alone.
- Regional data placement is required.

Do not shard only because sharding exists. It increases operational and modeling complexity.

## 15.2 Sharded-cluster components

A production sharded cluster includes:

- Shards, normally replica sets.
- `mongos` query routers.
- A config server replica set.
- A balancer and metadata management processes.

## 15.3 Shard key

The shard key determines data distribution and query routing.

A good shard key typically has:

- Sufficient cardinality.
- Good write distribution.
- Alignment with common query filters.
- No extreme hotspot.
- A distribution that remains healthy as data grows.

A bad shard key can produce:

- One hot shard.
- One hot chunk or range.
- Uneven storage.
- Scatter-gather queries.
- High migration activity.
- Poor scaling despite adding nodes.

## 15.4 Range-based sharding

Range sharding groups adjacent shard-key values.

Good for:

- Range queries that target specific ranges.
- Data-locality requirements.

Risk:

- Monotonically increasing keys such as timestamps can concentrate new writes in one range unless the compound key and distribution strategy avoid it.

## 15.5 Hashed sharding

Hashed sharding distributes hashed key values more uniformly.

Good for:

- Distributing writes across shards.
- High-cardinality equality keys.

Trade-off:

- Range locality on the original key is lost.

## 15.6 Targeted versus scatter-gather queries

A query containing an appropriate shard-key filter can be routed to the relevant shard or shards.

A query without it may need to be sent to every shard, after which results are merged.

```text
Targeted query:
Client -> mongos -> one shard

Scatter-gather query:
Client -> mongos -> all shards -> merge results
```

Scatter-gather is not always unacceptable, but high-volume latency-sensitive operations should normally be targetable.

## 15.7 Choosing a shard key: example

Suppose an application stores orders and common queries are:

1. Find one order by `orderId`.
2. List recent orders for a customer.
3. Insert orders at high volume.

Possible key:

```javascript
{ customerId: 1, orderId: 1 }
```

This can provide customer locality and targeted customer queries, but a very large customer can become a hotspot.

Possible hashed key:

```javascript
{ customerId: "hashed" }
```

This distributes customers, but queries involving ranges of customer IDs are not local in original order. The real answer depends on tenant sizes, access patterns, and growth.

## 15.8 Resharding

Modern MongoDB versions support resharding, but changing a shard key remains a significant production operation. Choose the original key carefully and validate it with realistic workload data.

---

# 16. Storage, memory, and the WiredTiger engine

MongoDB commonly uses the WiredTiger storage engine.

Important concepts include:

- Data and index compression.
- Journaling.
- Checkpoints.
- An internal cache.
- The operating-system file cache.
- Document and index working sets.

## 16.1 Working set

The working set is the data and index portion actively used by the workload.

When the working set fits in memory, reads can often avoid storage latency. When it does not, the system may experience more page faults and disk I/O.

Memory planning must include:

- Frequently accessed documents.
- Indexes.
- Aggregation working memory.
- Connections and application overhead.
- Operating-system requirements.

## 16.2 Compression

Compression reduces storage and I/O but consumes CPU. The right balance depends on workload and hardware.

## 16.3 Journaling and checkpoints

The journal records changes for recovery. Checkpoints create a consistent view of data files. Durability behavior also depends on write concern and deployment configuration.

## 16.4 Storage-performance symptoms

Possible signs of storage or memory pressure include:

- Growing query latency.
- High disk read latency.
- Cache eviction pressure.
- High page-fault activity.
- Large differences between documents examined and returned.
- Replication lag.
- Long checkpoints or stalls.

Do not solve every performance problem by adding CPU. Investigate schema, indexes, query shape, memory, storage, and concurrency together.

---

# 17. Change streams and event-driven applications

Change streams allow applications to subscribe to database changes without manually reading the oplog.

They can watch:

- A collection.
- A database.
- A deployment.

Conceptual example:

```javascript
const pipeline = [
  {
    $match: {
      operationType: { $in: ["insert", "update"] },
      "fullDocument.status": "paid"
    }
  }
]

const stream = db.orders.watch(pipeline, {
  fullDocument: "updateLookup"
})

while (stream.hasNext()) {
  const event = stream.next()
  printjson(event)
}
```

Use cases:

- Search-index synchronization.
- Cache invalidation.
- Notification workflows.
- Audit processing.
- Materialized views.
- Event-driven integration.

## 17.1 Important design points

- Store resume tokens when reliable resumption matters.
- Handle duplicate processing with idempotency.
- Understand oplog history and resume-window limitations.
- Size connection pools for open streams.
- Use a queue or stream platform when consumers need durable replay beyond the database change-history window.
- Do not treat the database as a complete replacement for Kafka in every event-driven architecture.

## 17.2 MongoDB change streams versus Kafka

Change streams report database changes. Kafka is a distributed event-streaming platform designed around durable logs, independent consumers, partitions, replay, retention, and decoupled event processing.

A common architecture is:

```text
Application writes MongoDB
          |
     Change stream / connector
          |
        Kafka
          |
 Multiple downstream consumers
```

Use change streams for reacting to MongoDB changes. Use Kafka or another streaming platform when the event log itself is a central integration product with independent retention and replay requirements.

---

# 18. Security fundamentals

Database security is a layered responsibility.

## 18.1 Authentication

Applications and administrators should authenticate using dedicated identities. Avoid shared administrative users.

Depending on deployment and platform, MongoDB supports mechanisms such as:

- Username and password authentication.
- X.509 certificates.
- LDAP integrations in applicable editions/services.
- Cloud-provider identity integrations in MongoDB Atlas, including AWS IAM-based application authentication in supported configurations.

## 18.2 Authorization and least privilege

Use role-based access control. Separate roles for:

- Application read/write access.
- Read-only analytics.
- Backup operations.
- Monitoring.
- Database administration.
- Security administration.

An application should not run as a cluster administrator.

## 18.3 Network isolation

Use:

- Private networks.
- Security groups/firewall rules.
- Private endpoints or peering where appropriate.
- Restricted source ranges.
- No unauthenticated public exposure.

## 18.4 Encryption

Protect data:

- In transit with TLS.
- At rest with storage encryption.
- In backups.
- In logs and exports.
- At the field level when highly sensitive values require stronger separation.

MongoDB and Atlas also provide capabilities for client-side field-level encryption or queryable encryption in supported configurations. These require careful schema, driver, key-management, and query planning.

## 18.5 Secrets management

Do not commit database passwords or connection strings into Git.

Use a secrets-management system such as:

- AWS Secrets Manager.
- HashiCorp Vault.
- Kubernetes Secrets combined with an external secret manager.
- A platform-native secrets store.

Rotate credentials and audit their use.

## 18.6 Auditing and monitoring

Monitor:

- Authentication failures.
- Privilege changes.
- New database users.
- Unusual query volume.
- Large exports.
- Schema or index changes.
- Backup failures.
- Public-network changes.

Security is not complete merely because encryption is enabled.

---

# 19. Backup, recovery, and disaster recovery

## 19.1 Recovery objectives

Define:

- **RPO — Recovery Point Objective:** the maximum acceptable data loss measured in time.
- **RTO — Recovery Time Objective:** the maximum acceptable restoration time.

Example:

```text
RPO: 5 minutes
RTO: 60 minutes
```

This means the organization accepts at most approximately five minutes of data loss and expects service restoration within one hour.

## 19.2 Backup types

Possible methods include:

- Logical exports.
- Filesystem or storage snapshots coordinated for consistency.
- Managed continuous backups.
- Point-in-time recovery.
- Cross-region copies.
- Offline archival exports.

Logical tools are useful for migrations and selected restores, but they may not be the best primary mechanism for very large, low-RPO production systems.

## 19.3 Restore testing

A backup is not proven until it has been restored.

Test:

1. Whether the backup is readable.
2. Whether keys and credentials are available.
3. Whether indexes and users are restored as expected.
4. Whether applications can connect.
5. How long restoration takes.
6. Whether point-in-time selection works.
7. Whether runbooks are understandable by someone other than the author.

## 19.4 Disaster-recovery scenarios

Plan for:

- Node failure.
- Availability Zone failure.
- Region failure.
- Accidental collection deletion.
- Bad application deployment.
- Credential compromise.
- Encryption-key loss.
- Ransomware or destructive operator action.

Replication, backup, and multi-region architecture solve different problems. A complete design may need all three.

---

# 20. MongoDB deployment options

## 20.1 Local development

Options include:

- A local MongoDB package.
- A Docker container.
- A development replica set.
- A free or low-cost Atlas deployment, subject to current service offerings.

Use a replica set locally when testing transactions, change streams, or failover behavior that a standalone server cannot represent.

## 20.2 Self-managed MongoDB

You operate:

- Hosts or Kubernetes resources.
- Patching and upgrades.
- Replica-set configuration.
- Sharded-cluster configuration.
- TLS and certificates.
- Monitoring.
- Backups.
- Scaling.
- Capacity planning.
- Incident response.

Self-management provides control but creates substantial operational responsibility.

## 20.3 MongoDB Atlas

MongoDB Atlas is MongoDB's managed multi-cloud database service for AWS, Azure, and Google Cloud.

Atlas can provide managed capabilities around:

- Deployment and upgrades.
- Backups.
- Monitoring and performance advice.
- Scaling.
- Networking.
- Security integrations.
- Search and vector-search features.
- Data federation and other platform services.

Managed does not mean responsibility-free. The customer still owns areas such as:

- Data model.
- Index design.
- Application security.
- User and network configuration.
- Cost control.
- Backup policy choices.
- Compliance configuration.

## 20.4 Kubernetes

MongoDB can run on Kubernetes, and MongoDB provides operator-based tooling for supported products. However, running a stateful distributed database on Kubernetes is not automatically simpler than using a managed service.

You must consider:

- Persistent-volume performance.
- Pod disruption budgets.
- Anti-affinity and topology spread.
- Node maintenance.
- Backup integration.
- Certificates.
- Stateful upgrades.
- Failure-domain placement.
- Operator lifecycle.

Kubernetes is a platform, not a substitute for database expertise.

---

# 21. MongoDB on AWS

There are several distinct ways to use document databases with AWS.

## 21.1 MongoDB Atlas on AWS

Atlas can deploy MongoDB infrastructure in AWS regions. Common integrations can include:

- AWS VPC connectivity.
- VPC peering or private endpoints, depending on configuration.
- AWS IAM authentication for supported Atlas application configurations.
- AWS KMS integrations for customer-managed keys in eligible tiers/configurations.
- AWS CloudFormation or Terraform-based provisioning options.
- Amazon S3 integrations in features such as data federation or backup/export workflows.

Always verify region, tier, and feature availability in the current Atlas documentation.

## 21.2 Self-managed MongoDB on EC2

You can run MongoDB on EC2 instances.

Responsibilities include:

- Choosing instance types.
- Designing EBS performance and durability.
- Placing members across Availability Zones.
- Managing operating systems.
- TLS and authentication.
- Backup and restore.
- Monitoring and alerting.
- Upgrade orchestration.
- Failure testing.

A conceptual three-AZ replica set:

```text
AZ-a: Primary EC2 + EBS
AZ-b: Secondary EC2 + EBS
AZ-c: Secondary EC2 + EBS
```

Use private subnets, tightly restricted security groups, TLS, and proper identity management.

## 21.3 MongoDB on EKS

MongoDB can be deployed to EKS, but this is an advanced stateful workload.

Questions to answer first:

- Why is EKS preferable to Atlas or EC2 for this database?
- Who owns operator upgrades?
- Which EBS classes and IOPS are required?
- How are replicas distributed across zones and nodes?
- How are backups taken independently of the cluster?
- How will node drains affect quorum?
- How are secrets and certificates rotated?
- How is a region failure handled?

Use StatefulSets and operators only as part of a deliberate supported architecture.

## 21.4 Amazon DocumentDB

Amazon DocumentDB is an AWS-managed document database with MongoDB API compatibility. It uses an AWS-designed storage architecture and documents functional differences from MongoDB.

This means:

- Many MongoDB drivers and API patterns can work.
- Compatibility is version- and feature-specific.
- Some operators, commands, index behaviors, or administrative functions differ.
- You must test the exact application, not assume complete equivalence.

---

# 22. MongoDB Atlas versus Amazon DocumentDB

| Area | MongoDB Atlas | Amazon DocumentDB |
|---|---|---|
| Engine | Managed MongoDB | AWS document database with MongoDB API compatibility |
| Provider | MongoDB | AWS |
| Cloud placement | AWS, Azure, and Google Cloud | AWS |
| Feature source | MongoDB server and Atlas platform | AWS implementation and compatibility roadmap |
| Compatibility | Native MongoDB | Selected MongoDB APIs and behavior, with documented differences |
| Search/vector capabilities | Atlas-specific services and indexes | AWS DocumentDB-specific capabilities and syntax support |
| Operations | Atlas console/API/CLI/providers | AWS console/API/CLI/CloudFormation ecosystem |
| IAM integration | Supported Atlas AWS IAM authentication options | Native AWS service integrations |
| Migration risk | Low when moving from compatible MongoDB versions/features | Requires compatibility assessment and functional testing |

## 22.1 Do not choose only from the word “compatible”

Run a compatibility assessment covering:

- Commands.
- Aggregation stages.
- Index types.
- Transactions.
- Change streams.
- Drivers.
- Authentication.
- Monitoring commands.
- Backup/restore tools.
- Query plans.
- Performance at realistic scale.

## 22.2 Practical selection

Choose Atlas when:

- Native MongoDB behavior is important.
- MongoDB-specific platform features are required.
- Portability across major clouds is valuable.
- The team wants the MongoDB vendor to operate MongoDB.

Consider DocumentDB when:

- AWS-native management and integration are priorities.
- The required API subset is supported.
- The workload passes compatibility and performance testing.
- The organization accepts implementation differences.

Neither option is universally superior. Architecture, compatibility, cost, operations, and feature requirements determine the answer.

---

# 23. PostgreSQL explained

PostgreSQL is an open-source object-relational database system that uses and extends SQL.

## 23.1 Core relational model

```sql
CREATE TABLE customers (
    customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('active', 'suspended', 'closed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

PostgreSQL can enforce:

- Primary keys.
- Foreign keys.
- Unique constraints.
- Check constraints.
- Not-null constraints.
- Exclusion constraints.
- Transactional integrity.

## 23.2 Foreign keys

```sql
CREATE TABLE orders (
    order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL
        REFERENCES customers(customer_id),
    status TEXT NOT NULL,
    total NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

The foreign key prevents an order from referencing a nonexistent customer, subject to transaction and constraint settings.

## 23.3 Joins

```sql
SELECT
    o.order_id,
    o.status,
    o.total,
    c.name,
    c.email
FROM orders AS o
JOIN customers AS c
  ON c.customer_id = o.customer_id
WHERE o.status = 'paid';
```

PostgreSQL supports sophisticated joins, subqueries, window functions, common table expressions, recursive queries, and rich SQL analytics.

## 23.4 MVCC

PostgreSQL uses multiversion concurrency control, or MVCC. Readers generally see a consistent snapshot while concurrent transactions create new row versions.

MVCC reduces reader-writer blocking, but old row versions must eventually be cleaned up. This is why vacuuming, autovacuum tuning, and transaction duration matter.

## 23.5 JSON and JSONB

PostgreSQL supports both `json` and `jsonb`.

```sql
CREATE TABLE products (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    attributes JSONB NOT NULL DEFAULT '{}'::jsonb
);
```

```sql
INSERT INTO products (sku, name, attributes)
VALUES (
    'KEY-001',
    'Mechanical Keyboard',
    '{"layout":"ISO-ES","switches":"brown","wireless":true}'::jsonb
);
```

Query:

```sql
SELECT *
FROM products
WHERE attributes @> '{"wireless": true}'::jsonb;
```

A GIN index can support suitable `jsonb` operators:

```sql
CREATE INDEX products_attributes_gin
ON products
USING GIN (attributes);
```

PostgreSQL is therefore not limited to rigid rows. It can combine strong relational structure with flexible document fields.

## 23.6 Index types

PostgreSQL supports several index types, including:

- B-tree.
- Hash.
- GiST.
- SP-GiST.
- GIN.
- BRIN.

This is a major strength for workloads involving JSONB, arrays, full-text search, ranges, geospatial extensions, and very large naturally ordered tables.

## 23.7 Extensibility

PostgreSQL is highly extensible through:

- Extensions.
- Custom types.
- Functions and procedures.
- Operators.
- Foreign data wrappers.
- Index access methods.

PostGIS is a well-known example for geospatial workloads.

## 23.8 Replication and high availability

PostgreSQL supports physical streaming replication and logical replication. Production high availability commonly combines PostgreSQL with orchestration, managed services, or cluster-management tooling.

The core engine is powerful, but a complete HA architecture must address:

- Failover coordination.
- Connection routing.
- Split-brain prevention.
- Backup and WAL archiving.
- Replica lag.
- Schema-change strategy.

## 23.9 When PostgreSQL is particularly strong

- Complex relationships.
- Financial and transactional systems.
- Rich SQL reporting.
- Mixed relational and JSON workloads.
- Geospatial systems.
- Data integrity.
- Systems requiring advanced index types or extensions.

---

# 24. MySQL explained

MySQL is a widely used relational database system. For transactional workloads, the normal storage engine is InnoDB.

## 24.1 InnoDB

InnoDB provides capabilities including:

- ACID transactions.
- Row-level locking.
- MVCC-style consistent reads.
- Foreign keys.
- Crash recovery.
- Redo and undo mechanisms.
- Clustered primary-key organization.

A simplified table:

```sql
CREATE TABLE customers (
    customer_id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(320) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id),
    UNIQUE KEY customers_email_uq (email)
) ENGINE = InnoDB;
```

## 24.2 Transactions

```sql
START TRANSACTION;

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 1
  AND balance >= 100;

UPDATE accounts
SET balance = balance + 100
WHERE account_id = 2;

COMMIT;
```

Applications must check affected-row counts and handle deadlocks or retries.

## 24.3 JSON

MySQL has a native JSON type and JSON functions.

```sql
CREATE TABLE products (
    product_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(100) NOT NULL UNIQUE,
    attributes JSON NOT NULL
);
```

```sql
SELECT *
FROM products
WHERE JSON_VALUE(attributes, '$.wireless') = TRUE;
```

Indexes over JSON expressions may use generated columns or expression/index capabilities supported by the target version.

## 24.4 Replication

Traditional MySQL replication uses the binary log. It is commonly asynchronous, although MySQL also provides semisynchronous options and Group Replication.

MySQL InnoDB Cluster combines Group Replication with management and routing components for high-availability architectures.

## 24.5 Partitioning

MySQL supports table partitioning for supported storage engines such as InnoDB. Partitioning divides one logical table into physical partitions. It is not the same as transparent multi-node sharding.

## 24.6 When MySQL is particularly strong

- Conventional web applications.
- Established LAMP-style ecosystems.
- Packaged software certified for MySQL.
- Teams with strong MySQL operational experience.
- Relational OLTP with straightforward query patterns.
- Organizations using MySQL-specific managed services or tooling.

---

# 25. MariaDB explained

MariaDB originated from the MySQL codebase and preserves substantial protocol and SQL compatibility, but it is an independent database product with its own roadmap.

## 25.1 Storage engines

MariaDB supports multiple storage engines. InnoDB is the normal transactional engine for general-purpose workloads and provides:

- ACID transactions.
- Row-level locking.
- Foreign keys.
- Crash recovery.

Other MariaDB engines and products serve different use cases. This flexibility is useful, but architecture should not mix engines without understanding their transactional and operational differences.

## 25.2 SQL and transactions

MariaDB uses familiar SQL and transaction constructs:

```sql
START TRANSACTION;

INSERT INTO orders(customer_id, status, total)
VALUES (10, 'pending', 99.90);

UPDATE inventory
SET stock = stock - 1
WHERE sku = 'KEY-001'
  AND stock > 0;

COMMIT;
```

## 25.3 JSON difference from MySQL

A significant difference is that MariaDB's `JSON` type is an alias for `LONGTEXT` with JSON-related validation/behavior, while MySQL stores JSON in a native binary format.

This difference affects:

- Storage representation.
- Some indexing approaches.
- Replication compatibility.
- Migration assumptions.

Do not assume a MySQL schema using JSON will behave identically in MariaDB.

## 25.4 Replication and Galera

MariaDB supports traditional replication and GTID-based workflows. MariaDB Galera Cluster provides a multi-primary synchronous or virtually synchronous clustering architecture for suitable workloads.

Galera is not magic horizontal scaling. It has constraints around:

- Write-set certification.
- Network latency.
- Conflicts.
- Large transactions.
- Schema operations.
- Quorum.

## 25.5 MySQL compatibility is not identity

MySQL and MariaDB have diverged in:

- Features.
- Optimizer behavior.
- JSON storage.
- Replication and GTID implementation.
- Authentication plugins.
- System tables.
- SQL behavior and defaults.
- Version numbering.

Validate drivers, ORMs, migrations, monitoring, backup tools, and vendor support before switching.

---

# 26. MongoDB versus PostgreSQL

This is often the most meaningful comparison because PostgreSQL can handle both relational data and JSONB.

## 26.1 Modeling philosophy

MongoDB:

```text
Aggregate -> document
```

PostgreSQL:

```text
Independent entities -> normalized tables -> joins
```

## 26.2 Integrity

PostgreSQL provides strong database-enforced relationships through foreign keys and constraints.

MongoDB provides:

- Document validation.
- Unique indexes.
- Atomic document operations.
- Transactions.

However, it does not provide SQL-style foreign-key constraints between collections. Cross-collection referential integrity is normally maintained by application logic, transactions, background reconciliation, or event-driven processes.

## 26.3 Query flexibility

PostgreSQL is often stronger for:

- Ad hoc joins.
- Complex reporting.
- Window functions.
- Recursive queries.
- Flexible queries that were not anticipated during schema design.

MongoDB is often strong when:

- The requested output matches a stored document aggregate.
- Nested arrays and documents are central.
- Pipelines can process the document shape directly.
- Access patterns are known and modeled deliberately.

## 26.4 JSON capability

PostgreSQL JSONB means the choice is not “documents or SQL.” A system can store:

- Stable core fields in typed relational columns.
- Variable attributes in JSONB.
- Relationships through foreign keys.
- JSON indexes through GIN or expression indexes.

Choose MongoDB when document orientation should be the primary model, not merely because some values are JSON.

## 26.5 Scaling

MongoDB offers a native sharded-cluster architecture.

PostgreSQL commonly scales through:

- Larger instances.
- Read replicas.
- Partitioning.
- Connection pooling.
- Caching.
- Application-level sharding.
- Distributed PostgreSQL extensions or services.

MongoDB's built-in sharding can be an advantage, but only with a suitable shard key and operational maturity.

## 26.6 Decision examples

Prefer PostgreSQL for:

- Accounting ledger.
- ERP.
- Complex SaaS billing.
- Inventory with many constraints.
- Systems with many independent entities and reports.

Prefer MongoDB for:

- Product catalog with highly variable category attributes.
- User profile/preferences document.
- Content documents with nested sections.
- Game state aggregates.
- Application configuration with controlled schema flexibility.

---

# 27. MongoDB versus MySQL

## 27.1 Data structure

MySQL normally uses normalized tables.

MongoDB uses documents with embedded structures.

A blog post in MongoDB:

```javascript
{
  _id: ObjectId("..."),
  title: "Learning Kubernetes",
  author: {
    authorId: ObjectId("..."),
    displayName: "Alice"
  },
  tags: ["kubernetes", "eks", "aws"],
  sections: [
    { heading: "Pods", body: "..." },
    { heading: "Deployments", body: "..." }
  ]
}
```

A normalized MySQL model might use:

```text
posts
post_sections
authors
tags
post_tags
```

MongoDB can simplify retrieving the whole article. MySQL can simplify queries and integrity when sections, authors, tags, and other entities have complex independent relationships.

## 27.2 Transactions

Both can provide transactions. The distinction is normal transaction scope:

- In MySQL/InnoDB, multi-row and multi-table transactions are central to the relational model.
- In MongoDB, one-document atomicity is central, with multi-document transactions available when needed.

## 27.3 JSON

MySQL's native JSON type is a column type inside a relational table. MongoDB's document is the fundamental storage unit.

## 27.4 Scaling and HA

MySQL provides replication, Group Replication, InnoDB Cluster, partitioning, and managed-service options. MongoDB provides replica sets and sharded clusters as native core concepts.

The operational comparison must include the exact topology or managed service, not only the engine names.

---

# 28. MongoDB versus MariaDB

The high-level comparison resembles MongoDB versus MySQL:

- MongoDB is document-oriented.
- MariaDB is relational.
- MongoDB emphasizes aggregates, embedding, and native sharding.
- MariaDB emphasizes SQL tables, foreign keys, joins, and transactional storage engines.

MariaDB may be preferable when:

- The application expects a MySQL-compatible relational interface.
- Existing tooling and staff knowledge center on MariaDB.
- SQL reporting and constraints are important.
- MariaDB-specific clustering or storage-engine capabilities are required.

MongoDB may be preferable when:

- Document-shaped aggregates dominate.
- Nested arrays and objects are first-class.
- Variable attributes are widespread.
- Native document sharding matches the scale strategy.

---

# 29. MySQL versus MariaDB

MySQL and MariaDB are much closer to one another than either is to MongoDB, but they are not interchangeable products.

| Area | MySQL | MariaDB |
|---|---|---|
| Origin | Oracle-maintained MySQL product | Fork originating from MySQL developers |
| Main model | Relational | Relational |
| Common transactional engine | InnoDB | InnoDB |
| JSON | Native binary JSON type | `JSON` alias based on `LONGTEXT` with MariaDB behavior |
| Replication | MySQL binlog/GTID ecosystem, Group Replication | MariaDB replication/GTID ecosystem, Galera options |
| Clustering | InnoDB Cluster/Group Replication and NDB options | Galera Cluster and MariaDB-specific products/options |
| Compatibility | Defines MySQL behavior | Significant compatibility, but growing differences |

Before migration, test:

- SQL modes.
- Authentication plugins.
- Character sets and collations.
- JSON columns.
- Stored procedures and functions.
- Replication.
- Backup/restore tools.
- ORMs and connectors.
- Vendor-certified support.

---

# 30. Complete comparison matrix

| Characteristic | MongoDB | PostgreSQL | MySQL | MariaDB |
|---|---|---|---|---|
| Primary model | Document | Object-relational | Relational | Relational |
| Main record | BSON document | Table row | Table row | Table row |
| Query interface | MongoDB Query Language and aggregation pipeline | SQL | SQL | SQL |
| Nested objects/arrays | Native, primary model | JSONB, arrays, composite types | JSON column | JSON-compatible text type/functions |
| Schema | Flexible with optional validation | Defined table schema, JSONB optional | Defined table schema, JSON optional | Defined table schema, JSON-compatible fields optional |
| Relationships | Embed or reference | Foreign keys and joins | Foreign keys and joins | Foreign keys and joins |
| Referential integrity | Application/transaction/reconciliation for cross-collection references | Strong database constraints | Strong with InnoDB constraints | Strong with InnoDB constraints |
| Single-record atomicity | Whole document | Row operations in transactions | Row operations in transactions | Row operations in transactions |
| Multi-record transactions | Supported | Core capability | Supported with transactional engines | Supported with transactional engines |
| Complex joins | `$lookup`, but not the primary modeling goal | Excellent | Strong | Strong |
| Ad hoc analytics | Aggregation framework | Excellent SQL analytics | Good SQL analytics | Good SQL analytics |
| Indexes | B-tree based and specialized types | Many access methods: B-tree, GIN, GiST, BRIN, etc. | B-tree-centric plus specialized capabilities | Engine-dependent, B-tree-centric for InnoDB |
| Native HA concept | Replica set | Replication plus HA orchestration/service | Replication, Group Replication/InnoDB Cluster | Replication, Galera options |
| Native horizontal data distribution | Sharded cluster | Usually extensions/services/application sharding | NDB or additional architecture; partitioning is not sharding | Additional clustering/sharding architecture; partitioning is not sharding |
| Best conceptual fit | Aggregate/document applications | Relationship-rich and mixed relational/JSON systems | Conventional relational applications | MariaDB-standardized relational environments |
| Main modeling risk | Bad embedding/reference boundaries and shard key | Over-normalization, poor queries, vacuum/index issues | Poor indexing, locking, replication design | Assuming perfect MySQL compatibility, engine/cluster complexity |

---

# 31. One e-commerce domain modeled in MongoDB and SQL

## 31.1 Requirements

The application must:

- Create customers.
- Manage products.
- Place orders.
- Preserve the purchased price and product name.
- List a customer's recent orders.
- Calculate revenue by country.
- Update inventory safely.

## 31.2 MongoDB design

### Products

```javascript
{
  _id: ObjectId("..."),
  sku: "KEY-001",
  name: "Mechanical Keyboard",
  category: "keyboards",
  attributes: {
    layout: "ISO-ES",
    switches: "brown",
    wireless: true
  },
  price: NumberDecimal("99.90"),
  stock: NumberInt(25),
  updatedAt: ISODate("...")
}
```

### Customers

```javascript
{
  _id: ObjectId("..."),
  name: "Alice Smith",
  email: "alice@example.com",
  addresses: [
    {
      addressId: "home",
      street: "Gran Via 20",
      city: "Madrid",
      country: "Spain"
    }
  ]
}
```

### Orders

```javascript
{
  _id: ObjectId("..."),
  orderNumber: "ORD-2026-0001",
  customerId: ObjectId("..."),
  customerSnapshot: {
    name: "Alice Smith",
    email: "alice@example.com"
  },
  shippingAddress: {
    street: "Gran Via 20",
    city: "Madrid",
    country: "Spain"
  },
  items: [
    {
      productId: ObjectId("..."),
      sku: "KEY-001",
      nameAtPurchase: "Mechanical Keyboard",
      quantity: 1,
      unitPrice: NumberDecimal("99.90")
    }
  ],
  status: "paid",
  total: NumberDecimal("99.90"),
  createdAt: ISODate("...")
}
```

Indexes:

```javascript
db.products.createIndex({ sku: 1 }, { unique: true })
db.customers.createIndex({ email: 1 }, { unique: true })
db.orders.createIndex({ orderNumber: 1 }, { unique: true })
db.orders.createIndex({ customerId: 1, createdAt: -1 })
db.orders.createIndex({ status: 1, createdAt: -1 })
```

### MongoDB strengths in this design

- One order read returns items and address.
- Historical snapshots are natural.
- Product attributes can vary by category.
- Customer order history has a direct compound index.

### MongoDB challenges

- Inventory and order creation may require a transaction or carefully designed reservation workflow.
- Cross-collection references are not protected by foreign keys.
- Product and customer copied fields need explicit snapshot/synchronization semantics.

## 31.3 PostgreSQL/MySQL/MariaDB relational design

```sql
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(12, 2) NOT NULL,
    stock INTEGER NOT NULL,
    CHECK (stock >= 0)
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    order_number VARCHAR(100) NOT NULL UNIQUE,
    customer_id BIGINT NOT NULL,
    customer_name_snapshot VARCHAR(200) NOT NULL,
    customer_email_snapshot VARCHAR(320) NOT NULL,
    shipping_country VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL,
    total DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    sku_snapshot VARCHAR(100) NOT NULL,
    product_name_snapshot VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id),
    CHECK (quantity > 0)
);
```

Recent orders query:

```sql
SELECT *
FROM orders
WHERE customer_id = 1001
ORDER BY created_at DESC
LIMIT 20;
```

Order detail:

```sql
SELECT
    o.order_number,
    o.status,
    o.total,
    oi.sku_snapshot,
    oi.product_name_snapshot,
    oi.quantity,
    oi.unit_price
FROM orders AS o
JOIN order_items AS oi
  ON oi.order_id = o.order_id
WHERE o.order_number = 'ORD-2026-0001';
```

### Relational strengths

- Foreign keys protect references.
- Inventory/order changes fit a multi-table transaction.
- SQL supports flexible reporting.
- Shared entities have clear authoritative rows.

### Relational challenges

- Retrieving aggregates needs joins.
- Product-category variation can create many nullable columns, subtype tables, or JSON fields.
- Object-relational mapping can be more involved.

## 31.4 The right answer may be hybrid

A business might use:

- PostgreSQL for orders, payments, inventory, and accounting.
- MongoDB for product catalog content and customer-facing configuration.
- Kafka for domain events.
- A search engine for full-text product search.
- A warehouse for analytics.

Polyglot persistence is valid when each database has clear ownership and the operational cost is justified. Do not add multiple databases merely because each one is interesting.

---

# 32. When MongoDB is a strong choice

MongoDB is often a strong choice when several of the following are true:

## 32.1 Natural document aggregates

The application already works with objects that should be persisted and retrieved together.

Examples:

- User profile.
- Product catalog item.
- Content page.
- Application configuration.
- Game state.
- Device configuration.

## 32.2 Variable attributes

Different records have different meaningful fields.

Example product categories:

```text
Laptop: CPU, RAM, screen, battery
Shoe: size, material, color
Book: author, ISBN, pages
Software: license, plan, billing period
```

MongoDB can store category-specific attributes naturally, although validation and indexing still require planning.

## 32.3 Read-together/write-together data

Embedding can eliminate repeated joins and make aggregate updates atomic.

## 32.4 High write distribution with a suitable shard key

MongoDB sharding can distribute data and load when the key and workload are designed for it.

## 32.5 Rapid but controlled schema evolution

New fields can be introduced gradually without immediately rebuilding an entire table, provided application compatibility and validation are managed.

## 32.6 Event or time-oriented records

MongoDB can work well for application events, audit-like records, IoT metadata, and time-series use cases, depending on retention, query patterns, throughput, and analytical requirements.

---

# 33. When a relational database is a stronger choice

A relational engine is commonly stronger when:

## 33.1 Relationships are the center of the model

Examples:

- Students, classes, teachers, and enrollments.
- Customers, contracts, invoices, payments, and tax rules.
- Employees, roles, departments, projects, and approvals.

## 33.2 Referential integrity is critical

The database must prevent orphan records and invalid relationships regardless of application bugs.

## 33.3 Transactions span many entities

A routine request must update several independent rows or tables atomically.

## 33.4 Ad hoc querying is important

Analysts and business users need to combine data in ways not known when the schema was designed.

## 33.5 SQL ecosystem matters

The system depends on:

- BI tools.
- Reporting tools.
- SQL skills.
- Existing ETL processes.
- Vendor-certified relational products.

## 33.6 Strong hybrid requirements

PostgreSQL is particularly compelling when the core is relational but some attributes need JSONB flexibility.

---

# 34. Common MongoDB mistakes and anti-patterns

## 34.1 Treating MongoDB as a relational database

Creating one collection for every tiny entity and joining everything with `$lookup` can produce complexity without gaining the benefits of document aggregates.

## 34.2 Treating MongoDB as an unstructured dump

Allowing arbitrary documents without validation, ownership, or versioning creates data-quality problems.

## 34.3 Unbounded arrays

Do not put unlimited comments, events, logs, or transactions into one document.

Use separate collections, pagination, bucketing, or bounded recent-history arrays.

## 34.4 Monotonically hot shard keys

A timestamp-only shard key can send all new writes to one range. Shard-key design must distribute both data and operations.

## 34.5 Too many indexes

Every index adds write, memory, and storage cost. Remove unused indexes after validating with monitoring and workload evidence.

## 34.6 No unique constraints

Application checks such as “find email, then insert if absent” are race-prone. Use unique indexes for values that must be unique.

## 34.7 Large multi-document transactions everywhere

This often indicates unsuitable aggregate boundaries or a workload better served by a relational model.

## 34.8 Reading from secondaries without understanding lag

Secondary reads can return stale data. Select read preference and consistency settings deliberately.

## 34.9 Assuming replication is backup

A destructive write is replicated. Maintain independent, tested backups.

## 34.10 Ignoring document growth

Documents that grow substantially can affect storage and write behavior. Model growth, array bounds, and expected size from the start.

## 34.11 Offset pagination at huge offsets

```javascript
db.events.find().sort({ createdAt: -1 }).skip(1000000).limit(20)
```

Large skips can be inefficient. Prefer seek/range pagination using a stable ordered key:

```javascript
db.events.find({
  createdAt: { $lt: lastSeenCreatedAt }
}).sort({ createdAt: -1 }).limit(20)
```

Use a tie-breaker such as `_id` when timestamps may be equal.

---

# 35. Performance investigation workflow

When a MongoDB workload is slow, use a structured process.

## Step 1: Define the symptom

- Which operation is slow?
- What percentile is affected: p50, p95, or p99?
- Is it read or write latency?
- Is the issue constant or periodic?
- Did data volume, deployment, or traffic change?

## Step 2: Capture the exact query shape

Record:

- Filter.
- Projection.
- Sort.
- Limit.
- Collation.
- Read preference/read concern.
- Aggregation stages.
- Transaction context.

## Step 3: Inspect the execution plan

Use `explain("executionStats")` and examine:

- `COLLSCAN` versus `IXSCAN`.
- Keys examined.
- Documents examined.
- Documents returned.
- Blocking sorts.
- Lookup stages.

## Step 4: Verify index suitability

Ask:

- Does the index support equality filters?
- Does it support the sort?
- Are range fields in an appropriate position?
- Is the query selective?
- Is the index too large for memory?

## Step 5: Inspect resource pressure

- CPU.
- Memory/cache.
- Disk latency and IOPS.
- Network.
- Connections.
- Queue depth.
- Replication lag.
- Lock or ticket pressure.

## Step 6: Inspect document design

- Are documents too large?
- Are arrays unbounded?
- Is `$lookup` replacing a better embedding decision?
- Is the application fetching fields it does not need?
- Is a high-frequency computed value recalculated every time?

## Step 7: Validate topology behavior

- Is traffic reaching the intended region?
- Are reads accidentally sent to lagging replicas?
- Is a shard hot?
- Are queries scatter-gather?
- Is the balancer moving data during peak load?

## Step 8: Test one change at a time

Benchmark with representative data and concurrency. A faster development query can become slower in production because of cache, cardinality, or write-amplification differences.

---

# 36. Migration considerations

## 36.1 Relational to MongoDB

Do not convert every table into a collection mechanically.

Instead:

1. Identify application aggregates.
2. Identify read/write access patterns.
3. Decide what to embed.
4. Decide what to reference.
5. Define validation.
6. Define indexes.
7. Define transaction boundaries.
8. Define migration and synchronization strategy.
9. Load-test the new model.

A relational join table might become an embedded array, a reference array, or remain a separate collection. The correct result depends on cardinality and access patterns.

## 36.2 MongoDB to PostgreSQL/MySQL/MariaDB

Identify:

- Document variants.
- Optional fields.
- Nested arrays.
- Duplicated snapshots.
- Invalid references.
- Mixed data types.
- Schema versions.

Then decide whether nested data becomes:

- Relational child tables.
- JSON/JSONB fields.
- Separate entities.
- Historical snapshot columns.

## 36.3 Online migration

A low-downtime migration may use:

1. Initial bulk copy.
2. Change capture or dual writes.
3. Continuous validation.
4. Read-shadowing.
5. Cutover.
6. Rollback window.
7. Decommission after confidence is established.

Dual writes are difficult because partial failures can diverge systems. Prefer a reliable change-data-capture or outbox design where possible.

## 36.4 Validation

Compare:

- Record counts.
- Aggregate totals.
- Checksums or hashes.
- Sampled business objects.
- Referential integrity.
- Query results.
- Performance.

Migration success is not merely “all rows were copied.”

---

# 37. A practical local laboratory

The following lab uses Docker Compose. Pin versions approved by your organization rather than relying on `latest` in a real project.

## 37.1 MongoDB replica-set lab

Create `compose.yaml`:

```yaml
services:
  mongo1:
    image: mongo:8.0
    command: ["mongod", "--replSet", "rs0", "--bind_ip_all"]
    ports:
      - "27017:27017"
    volumes:
      - mongo1-data:/data/db

  mongo2:
    image: mongo:8.0
    command: ["mongod", "--replSet", "rs0", "--bind_ip_all"]
    ports:
      - "27018:27017"
    volumes:
      - mongo2-data:/data/db

  mongo3:
    image: mongo:8.0
    command: ["mongod", "--replSet", "rs0", "--bind_ip_all"]
    ports:
      - "27019:27017"
    volumes:
      - mongo3-data:/data/db

volumes:
  mongo1-data:
  mongo2-data:
  mongo3-data:
```

Start:

```bash
docker compose up -d
```

Initialize the replica set:

```bash
docker exec -it $(docker ps -qf name=mongo1) mongosh --eval '
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})'
```

Connect from inside the network or adjust the replica-set hostnames for your client environment. For a reusable development setup, configure host resolution and authentication correctly rather than depending on container IDs.

## 37.2 Create data

```javascript
use shop

db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sku", "name", "price", "stock"],
      properties: {
        sku: { bsonType: "string" },
        name: { bsonType: "string" },
        price: { bsonType: "decimal" },
        stock: { bsonType: "int", minimum: 0 }
      }
    }
  }
})

db.products.createIndex({ sku: 1 }, { unique: true })

db.products.insertMany([
  {
    sku: "KEY-001",
    name: "Mechanical Keyboard",
    category: "keyboards",
    attributes: {
      layout: "ISO-ES",
      switches: "brown"
    },
    price: NumberDecimal("99.90"),
    stock: NumberInt(25)
  },
  {
    sku: "MOUSE-001",
    name: "Wireless Mouse",
    category: "mice",
    attributes: {
      dpi: 16000,
      wireless: true
    },
    price: NumberDecimal("49.90"),
    stock: NumberInt(40)
  }
])
```

## 37.3 Practice queries

```javascript
db.products.find({
  "attributes.wireless": true
})
```

```javascript
db.products.updateOne(
  { sku: "KEY-001", stock: { $gte: 1 } },
  { $inc: { stock: -1 } }
)
```

```javascript
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      products: { $sum: 1 },
      averagePrice: { $avg: "$price" }
    }
  }
])
```

## 37.4 Explain an indexed query

```javascript
db.products.createIndex({ category: 1, price: 1 })

db.products.find({
  category: "keyboards",
  price: { $lte: NumberDecimal("150.00") }
}).explain("executionStats")
```

## 37.5 Test failover

1. Run `rs.status()` and identify the primary.
2. Stop the primary container.
3. Observe election of a new primary.
4. Confirm the driver reconnects.
5. Restart the stopped member and observe it rejoin.

Do this only in the lab. Production failover tests require change control and defined safeguards.

## 37.6 Compare with PostgreSQL

Create a PostgreSQL container and model the same product catalog using relational columns plus JSONB. Compare:

- Query syntax.
- Index creation.
- Validation.
- Join requirements.
- Transaction behavior.
- Query plans.

This practical comparison is more valuable than memorizing marketing claims.

---

# 38. Learning path and checklist

## Phase 1: Fundamentals

- [ ] Explain database, collection, document, and field.
- [ ] Explain BSON versus JSON.
- [ ] Create, read, update, and delete documents.
- [ ] Query nested fields and arrays.
- [ ] Use projection, sorting, and limiting.
- [ ] Understand the `_id` index.

## Phase 2: Data modeling

- [ ] Explain embedding versus referencing.
- [ ] Identify one-to-one, one-to-few, one-to-many, and many-to-many relationships.
- [ ] Recognize unbounded-array risks.
- [ ] Design a document from application access patterns.
- [ ] Add schema validation.
- [ ] Plan schema versioning.

## Phase 3: Queries and indexes

- [ ] Build aggregation pipelines.
- [ ] Use `$match`, `$project`, `$group`, `$unwind`, and `$lookup`.
- [ ] Create single and compound indexes.
- [ ] Explain compound-index field order.
- [ ] Read `explain("executionStats")`.
- [ ] Identify unused or excessive indexes.

## Phase 4: Reliability

- [ ] Explain single-document atomicity.
- [ ] Execute a multi-document transaction.
- [ ] Explain read concern, write concern, and read preference.
- [ ] Explain replica sets and elections.
- [ ] Test driver behavior during failover.
- [ ] Explain why replication is not backup.

## Phase 5: Scale

- [ ] Explain sharded-cluster components.
- [ ] Explain range versus hashed sharding.
- [ ] Identify targeted and scatter-gather queries.
- [ ] Evaluate shard-key cardinality and hotspots.
- [ ] Explain why sharding adds operational complexity.

## Phase 6: Production operations

- [ ] Configure TLS and least-privilege users.
- [ ] Define RPO and RTO.
- [ ] Test backup restoration.
- [ ] Monitor latency, replication lag, cache, disk, and connections.
- [ ] Plan upgrades and rollbacks.
- [ ] Estimate storage and index growth.
- [ ] Establish cost alerts.

## Phase 7: Database selection

- [ ] Compare MongoDB with PostgreSQL JSONB.
- [ ] Compare MongoDB transactions with relational transactions.
- [ ] Explain MySQL and MariaDB divergence.
- [ ] Explain why Amazon DocumentDB is not identical to MongoDB.
- [ ] Select a database from requirements rather than popularity.

---

# 39. Interview questions and model answers

## What is MongoDB?

MongoDB is a document-oriented database that stores BSON documents in collections. It supports nested data, indexes, aggregation pipelines, replica sets, sharding, schema validation, and multi-document transactions.

## What is the difference between a MongoDB document and a SQL row?

A SQL row contains values for table columns and normally relates to other rows through keys. A MongoDB document can contain an entire nested aggregate with embedded objects and arrays, and documents in one collection can have different optional fields.

## Is MongoDB schemaless?

It is better described as schema-flexible. Production applications still have a schema, and MongoDB can enforce validation rules with JSON Schema and query expressions.

## Does MongoDB support ACID transactions?

Yes. A single-document write is atomic, and MongoDB supports multi-document distributed transactions on replica sets and sharded clusters. Good document design still tries to keep natural atomic aggregates in one document.

## What is a replica set?

A replica set is a group of MongoDB servers that maintain the same dataset. One member is primary and accepts writes; secondary members replicate changes and can elect a new primary after failure.

## What is sharding?

Sharding horizontally distributes collection data across shards. A shard key determines distribution and query routing. Poor shard-key selection can create hotspots and scatter-gather queries.

## Embedding or referencing?

Embed when related data has the same lifecycle, is bounded, and is normally read or updated together. Reference when entities are independent, shared, frequently updated, many-to-many, or unbounded.

## MongoDB or PostgreSQL?

Use PostgreSQL when relationships, constraints, complex SQL, and multi-entity transactions dominate. Use MongoDB when document aggregates, nested data, variable attributes, and native document sharding are central. PostgreSQL JSONB makes it a strong hybrid option.

## MongoDB or MySQL?

The same relational-versus-document decision applies. MySQL/InnoDB is a mature relational OLTP system; MongoDB is document-first. Existing ecosystem, data relationships, query patterns, and scaling requirements should drive the choice.

## Are MySQL and MariaDB the same?

No. MariaDB originated from MySQL and remains substantially compatible in many areas, but they have independent roadmaps and differences in JSON representation, replication, GTIDs, clustering, authentication, optimizer behavior, and tooling.

## Is Amazon DocumentDB MongoDB?

No. Amazon DocumentDB is an AWS-managed document database with MongoDB API compatibility. AWS publishes a compatibility matrix and functional differences, so applications must be tested against the exact required features.

---

# 40. Final decision framework

Use the following process before choosing a database.

## Question 1: What is the natural unit of consistency?

- One self-contained aggregate: MongoDB may fit well.
- Several independent entities: relational may fit better.

## Question 2: How important are relationships?

- Many central relationships and joins: PostgreSQL/MySQL/MariaDB.
- Mostly hierarchical ownership: MongoDB.

## Question 3: Must the database enforce references?

- Yes, strongly: relational foreign keys are a major advantage.
- Application-controlled references are acceptable: MongoDB remains possible.

## Question 4: How variable is the record shape?

- Highly variable by category/type: MongoDB or PostgreSQL JSONB.
- Stable tabular structure: relational.

## Question 5: What are the real query patterns?

- Retrieve complete aggregate by ID/key: MongoDB is strong.
- Join arbitrary entities and run flexible reports: PostgreSQL is strong.

## Question 6: What is the transaction boundary?

- Usually one aggregate: MongoDB.
- Routinely many tables/entities: relational.

## Question 7: What scale is required?

- One strong server plus replicas is enough: any engine may work.
- Native horizontal document distribution is required: MongoDB has an architectural advantage.
- Distributed SQL is required: evaluate distributed relational products/services explicitly.

## Question 8: What does the team know how to operate?

The technically ideal engine can become the operationally worst choice if nobody can secure, monitor, back up, restore, tune, and troubleshoot it.

## Question 9: What managed services and constraints apply?

Compare:

- Engine compatibility.
- Regions.
- Network architecture.
- Backup and PITR.
- Encryption and key management.
- Version support.
- Upgrade control.
- Cost at realistic scale.
- Vendor support.
- Lock-in.

## Professional default recommendation

When requirements are uncertain, PostgreSQL is commonly the safest general-purpose starting point because it combines relational integrity, advanced SQL, extensibility, and JSONB.

Choose MongoDB deliberately when the application can clearly state:

> This information belongs together, normally moves through the system together, and should be stored as a document aggregate.

Choose MySQL or MariaDB when relational modeling fits and the surrounding platform, vendor, team, or application ecosystem makes that engine the best operational choice.

The database should follow the domain and workload—not fashion.

---

# 41. Official references

The guide above is a synthesis and explanation, not a replacement for product documentation. Verify feature availability and version-specific behavior in the current official manuals.

## MongoDB

- [MongoDB Database Manual](https://www.mongodb.com/docs/manual/)
- [Documents](https://www.mongodb.com/docs/manual/core/document/)
- [BSON types](https://www.mongodb.com/docs/manual/reference/bson-types/)
- [Databases and collections](https://www.mongodb.com/docs/manual/core/databases-and-collections/)
- [Schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [JSON Schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/)
- [Embedding versus references](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)
- [Indexes](https://www.mongodb.com/docs/manual/indexes/)
- [Aggregation](https://www.mongodb.com/docs/manual/aggregation/)
- [Transactions](https://www.mongodb.com/docs/manual/core/transactions/)
- [Read concern](https://www.mongodb.com/docs/manual/reference/read-concern/)
- [Write concern](https://www.mongodb.com/docs/manual/reference/write-concern/)
- [Replica-set members](https://www.mongodb.com/docs/manual/core/replica-set-members/)
- [Replication data synchronization](https://www.mongodb.com/docs/manual/core/replica-set-sync/)
- [Sharding](https://www.mongodb.com/docs/manual/sharding/)
- [Shard keys](https://www.mongodb.com/docs/manual/core/sharding-shard-key/)
- [Change streams](https://www.mongodb.com/docs/manual/changeStreams/)
- [MongoDB limits and thresholds](https://www.mongodb.com/docs/manual/reference/limits/)
- [MongoDB Atlas](https://www.mongodb.com/docs/atlas/)
- [Atlas on AWS](https://www.mongodb.com/docs/atlas/reference/amazon-aws/)
- [Atlas infrastructure as code](https://www.mongodb.com/docs/atlas/infrastructure/)
- [Atlas database authentication](https://www.mongodb.com/docs/atlas/security/config-db-auth/)

## PostgreSQL

- [PostgreSQL documentation](https://www.postgresql.org/docs/)
- [About PostgreSQL](https://www.postgresql.org/about/)
- [Constraints and foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Concurrency control and MVCC](https://www.postgresql.org/docs/current/mvcc.html)
- [JSON types](https://www.postgresql.org/docs/current/datatype-json.html)
- [JSON functions and operators](https://www.postgresql.org/docs/current/functions-json.html)
- [Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [GIN indexes](https://www.postgresql.org/docs/current/gin.html)
- [Table partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)

## MySQL

- [MySQL documentation](https://dev.mysql.com/doc/)
- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/)
- [InnoDB storage engine](https://dev.mysql.com/doc/refman/8.4/en/innodb-storage-engine.html)
- [InnoDB and ACID](https://dev.mysql.com/doc/refman/8.4/en/mysql-acid.html)
- [JSON data type](https://dev.mysql.com/doc/refman/8.4/en/json.html)
- [Replication implementation](https://dev.mysql.com/doc/refman/8.4/en/replication-implementation.html)
- [Group Replication](https://dev.mysql.com/doc/refman/8.4/en/group-replication.html)
- [Partitioning](https://dev.mysql.com/doc/refman/8.4/en/partitioning.html)

## MariaDB

- [MariaDB Server documentation](https://mariadb.com/docs/server/)
- [InnoDB introduction](https://mariadb.com/docs/server/server-usage/storage-engines/innodb/innodb-storage-engine-introduction)
- [Storage engines](https://mariadb.com/docs/server/server-usage/storage-engines)
- [JSON data type](https://mariadb.com/docs/server/reference/data-types/string-data-types/json)
- [Replication compatibility between MariaDB and MySQL](https://mariadb.com/docs/release-notes/community-server/about/compatibility-and-differences/replication-compatibility-between-mariadb-and-mysql)

## AWS

- [What is Amazon DocumentDB?](https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html)
- [Amazon DocumentDB compatibility with MongoDB](https://docs.aws.amazon.com/documentdb/latest/devguide/compatibility.html)
- [Functional differences between Amazon DocumentDB and MongoDB](https://docs.aws.amazon.com/documentdb/latest/devguide/functional-differences.html)
- [Supported MongoDB APIs, operations, and data types in Amazon DocumentDB](https://docs.aws.amazon.com/documentdb/latest/devguide/mongo-apis.html)

---

## Closing note

A database comparison is useful only when connected to a real workload. Before adopting an engine, build a proof of concept with representative data, concurrency, indexes, transactions, failure tests, backups, and cost estimates. The best database is the one that meets the system's correctness, performance, resilience, security, operability, and cost requirements with the least unnecessary complexity.
