# ADR-0003: Keep repository navigation before adding a searchable site

Status: Accepted

## Context

The knowledge base is currently published as a Git repository with Markdown indexes, focused articles, local validation scripts, and an explicit maintenance review queue. The improvement plan asks whether a searchable static reading site would be worthwhile after reader-task testing produces findability evidence.

As of 2026-09-19, that reader evidence does not exist yet. The repository does have stronger navigation than the review baseline: a root index with coverage labels, fast topic paths, a beginner start route, local-link validation, source traceability, priority guide review blocks, and a maintenance queue for reader testing.

A static site could improve search, mobile reading, and browsing comfort. It would also add generator configuration, publishing workflows, accessibility checks, archive handling, link compatibility rules, and another surface that must stay synchronized with the Markdown source.

## Decision

Keep the Markdown repository navigation as the canonical publishing surface for now. Do not build or deploy a static searchable site until KB-14 reader testing shows a concrete findability or readability problem that repository navigation cannot reasonably solve.

Revisit this decision after KB-14 records actual reader outcomes. If a site is reconsidered, prototype it against the same reader tasks before choosing a generator, hosting model, or public deployment workflow.

## Options considered

| Option | Pros | Cons |
| --- | --- | --- |
| Keep repository navigation for now | Uses the existing single source of truth, avoids extra publishing maintenance, preserves current relative links, and lets reader testing determine the real problem. | Readers do not get site-level search, mobile-focused layout, or web navigation enhancements yet. |
| Build a small static site now | Could improve search, browsing, and sharing if the current repository interface is limiting readers. | Premature without KB-14 evidence; adds generator, deployment, accessibility, archive, and link-compatibility work before a measured need exists. |
| Build a prototype only | Could reveal static-site costs and layout issues before a full commitment. | Still consumes maintenance time before reader testing shows whether the repository navigation is the blocker. |

## Consequences

- The repository remains the canonical knowledge-base interface.
- Future content work should continue improving indexes, article review blocks, local validation, and reader-test tasks before introducing another publishing layer.
- KB-14 reader testing becomes the trigger for reopening this decision.
- If repeated reader tasks fail because of search, mobile readability, or navigation limits, the next ADR or revision should evaluate a bounded static-site prototype with those same tasks.
- Public deployment remains out of scope until a separate implementation task selects and validates a publishing approach.

## Related links

- [Knowledge-base improvement plan](../knowledge-base-improvement-plan.md)
- [Maintenance review queue](../maintenance-review-queue.md)
- [Knowledge-base review](../knowledge-base-review.md)
- [Decision records](README.md)
- [Back to root index](../README.md)
