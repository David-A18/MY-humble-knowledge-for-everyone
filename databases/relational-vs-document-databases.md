# Relational vs. document databases

## Purpose

Use this page to decide whether a relational database or document database is a better starting point for a workload.

## Decision guide

| Situation | Prefer | Reason |
| --- | --- | --- |
| Strong relational integrity and joins dominate | Relational database | Constraints and joins are first-class design tools. |
| Data is aggregate-shaped and read together | Document database | Documents can match application object boundaries. |
| Reporting requires many cross-entity queries | Relational or analytical model | Normalized data and SQL are often easier to query. |
| Schema evolves quickly but still has patterns | Document database with validation | Flexible documents support iteration with guardrails. |
| Transactions span many independent entities | Relational database | Multi-row consistency is often simpler to model. |

## Practical rule

Choose the data model that makes the most important reads and writes simple, explicit, and safe. Do not choose a database only because it is familiar, fashionable, or managed by the current cloud provider.

## Related links

- [MongoDB fundamentals](mongodb/fundamentals.md)
- [MongoDB data modeling](mongodb/data-modeling.md)
- [Back to databases index](README.md)
- [Back to root index](../README.md)
