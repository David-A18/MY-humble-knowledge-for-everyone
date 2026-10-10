---
type: "Explanation"
title: "MongoDB data modeling"
description: "Choose what to embed in a MongoDB document and what to store separately by following one support-ticket access pattern."
tags: [databases, mongodb, data-modeling]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: mongodb-workload
    resource: https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/identify-workload/
    title: MongoDB manual - Identify Application Workload
  - id: mongodb-relationships
    resource: https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/map-relationships/
    title: MongoDB manual - Map Schema Relationships
  - id: mongodb-embedding
    resource: https://www.mongodb.com/docs/manual/data-modeling/embedding/
    title: MongoDB manual - Embedded Data
  - id: mongodb-referencing
    resource: https://www.mongodb.com/docs/manual/data-modeling/referencing/
    title: MongoDB manual - Reference Data
  - id: mongodb-unbounded-arrays
    resource: https://www.mongodb.com/docs/manual/data-modeling/design-antipatterns/unbounded-arrays/
    title: MongoDB manual - Avoid Unbounded Arrays
---

# MongoDB data modeling

## The question this page answers

When two pieces of information are related, should they live **inside one
MongoDB document** or in **separate documents linked by an identifier**? This
page teaches that choice with one support-ticket example. If documents and
collections are new to you, start with [MongoDB fundamentals](fundamentals.md).

## Start with the way people use the data

A document's shape should serve the application's common reads and writes.
MongoDB's schema-design process starts by listing those operations, then
mapping the relationships between the data they use.[^mongodb-workload][^mongodb-relationships]
For a ticket system, ask:

| Action | What it needs | What changes |
| --- | --- | --- |
| Open a ticket | Subject, status, and the requester's displayed name. | Status changes during the ticket's life. |
| Read the conversation | Ticket plus recent comments. | Comments are added over time. |
| Edit a user's profile | The current name and contact details. | The same user may have many tickets. |
| Moderate one comment | That comment and its moderation state. | It can change independently of the ticket. |

These are **invented requirements**, not observed traffic. In a real design,
measure which actions are frequent, their response times, and how many
comments a ticket can accumulate before committing to a shape.

## Two ways to connect related data

**Embed** a small, bounded piece of information inside the document that
usually needs it. One read can return both pieces, and one write to that
document is atomic. But repeated copies must be maintained if they are meant
to stay current, and a MongoDB document must stay below 16
mebibytes.[^mongodb-embedding]

**Reference** related information by storing its identifier and keeping the
full record elsewhere. This lets it grow or change independently. The
application then needs another read, or a join-like `$lookup`, when it needs
both pieces together.[^mongodb-referencing]

Think of embedding as putting a short contact card inside a ticket folder and
referencing as writing the person's file number on the folder. The analogy
helps with *where information lives*. It does not describe MongoDB's read
cost, update behavior, size limit, or security rules; decide those from the
actual workload.

```mermaid
flowchart LR
  t["Ticket: subject, status,<br/>requester snapshot"]
  u["User: current profile"]
  c["Comment: text,<br/>moderation state"]
  t -- "requester.userId" --> u
  c -- "ticketId" --> t
```

Text alternative: the ticket contains a small requester snapshot and points
to the separately managed user by `requester.userId`. Each separately stored
comment points back to its ticket by `ticketId`. The two arrows are stored
identifiers, not automatic database relationships.

## Work through one ticket

Suppose the ticket detail screen shows the requester's name immediately, but
comments can grow for months and moderators edit them one at a time. A possible
model is:

```json
{
  "_id": "TCK-1043",
  "subject": "Cannot reset password",
  "status": "open",
  "requester": { "userId": "USR-88", "nameAtCreation": "Dana Reyes" }
}
```

```json
{
  "_id": "CMT-701",
  "ticketId": "TCK-1043",
  "authorId": "USR-88",
  "text": "The reset email never arrives.",
  "moderationState": "visible"
}
```

These are illustrative JSON documents, not output from a database. The first
read gets the ticket and its **historical name snapshot**. A separate query
gets comments for `TCK-1043`; the application decides how many to show at
once. To display the user's **current** name, it reads the user record by
`requester.userId` instead. The name snapshot is deliberately allowed to
differ from the live profile; if the product requires every old ticket to show
the current name, this snapshot alone does not meet that requirement.

Why keep comments separate here? An array that grows every time someone
comments has no clear bound. It can increase document size and strain
queries and indexes, even before the 16 mebibyte document limit is reached.
MongoDB recommends bounding such arrays, for example with a small embedded
subset and separate referenced records.[^mongodb-unbounded-arrays] A ticket
system with a proven small, fixed comment limit could instead embed all its
comments and simplify the ticket read.[^mongodb-embedding]

## Make the decision explicit

| Ask | Embedding tends to fit when… | Referencing tends to fit when… |
| --- | --- | --- |
| Are these read together? | Most important reads need both. | They are usually read separately. |
| Will the related data grow? | Its size is small and bounded. | It may grow without a practical bound. |
| Who changes it? | The same operation changes it with its parent. | It is edited or managed on its own. |
| Is it copied elsewhere? | A snapshot or rarely changing copy has a clear meaning. | A frequently changing value needs one current source. |

These are prompts, not automatic rules. Embedding can reduce reads, while
referencing can reduce duplicate updates and document growth. MongoDB calls
out independent querying and frequently changed duplicate data as reasons to
consider references.[^mongodb-referencing]

For this example, the next design questions are whether a query on
`comments.ticketId` has a suitable index and whether ticket fields need
validation. [Schema validation and indexing](schema-validation-and-indexing.md)
covers those choices. Test the model with representative reads and writes
before treating it as a production design.

## Check your understanding

1. Why is the requester's name copied into the example ticket, and what does
   `requester.userId` add?
2. If a ticket can receive thousands of comments, what changes in the
   embedding decision?
3. If the page must always show the user's current name, which record must
   it read?

## Continue learning

- [MongoDB fundamentals](fundamentals.md) explains the basic document model.
- [Schema validation and indexing](schema-validation-and-indexing.md) covers
  the next choices after document shape.
- [MongoDB's workload-design guide](https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/identify-workload/)
  shows how to list actual application operations.
- [Back to MongoDB index](index.md)

[^mongodb-workload]: [MongoDB manual: Identify Application Workload](https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/identify-workload/).
[^mongodb-relationships]: [MongoDB manual: Map Schema Relationships](https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/map-relationships/).
[^mongodb-embedding]: [MongoDB manual: Embedded Data](https://www.mongodb.com/docs/manual/data-modeling/embedding/).
[^mongodb-referencing]: [MongoDB manual: Reference Data](https://www.mongodb.com/docs/manual/data-modeling/referencing/).
[^mongodb-unbounded-arrays]: [MongoDB manual: Avoid Unbounded Arrays](https://www.mongodb.com/docs/manual/data-modeling/design-antipatterns/unbounded-arrays/).
