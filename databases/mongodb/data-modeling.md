# MongoDB data modeling

## Purpose

Use this page to choose MongoDB document shapes that match application access patterns.

## Modeling decisions

| Situation | Prefer | Reason |
| --- | --- | --- |
| Data is usually read together | Embed related data. | One read can fetch the aggregate. |
| Related data grows without a clear bound | Reference another document. | Avoids oversized documents and write contention. |
| Many owners update the same nested data | Reference or split ownership. | Reduces conflicts and accidental coupling. |
| Queries need consistent fields | Schema validation. | Keeps flexible documents from becoming unknowable. |
| Analytics spans many entities | Aggregation or analytical store. | Application documents are not always the best reporting model. |

## Access-pattern first workflow

1. List the screens, APIs, and jobs that read the data.
2. List update frequency and ownership for each part of the data.
3. Embed bounded one-to-one or one-to-few data that is read together.
4. Reference unbounded, independently updated, or independently secured data.
5. Add indexes for the most important query filters and sort patterns.

## Common mistakes

- Embedding unbounded arrays that grow forever.
- Referencing everything because it feels relational.
- Adding indexes without checking whether they match real query shapes.
- Treating schema validation as unnecessary because MongoDB is flexible.

## Related links

- [MongoDB fundamentals](fundamentals.md)
- [MongoDB operations](operations.md)
- [MongoDB data modeling documentation](https://www.mongodb.com/docs/manual/data-modeling/)
- [Back to MongoDB index](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
