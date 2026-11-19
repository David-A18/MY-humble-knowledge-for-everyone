---
type: Decision Record
title: "ADR-0006: Publish dated news briefs inside the OKF bundle"
description: "Add a news section of short, sourced, dated briefs on AI, technology, and the economy that expire instead of becoming permanent guidance."
tags: [decision-records, okf, news, editorial-policy]
status: draft
audience: Knowledge-base maintainers and contributors
maintainer: unassigned
---

# ADR-0006: Publish dated news briefs inside the OKF bundle

## Decision state

Accepted on 2026-11-19.

## Context

Readers want to know what is changing in artificial intelligence, technology,
and the economy, and how it affects their work, without leaving the knowledge
base. Concept pages are written to stay valid for a long time. News is the
opposite: it is true on a date and goes stale quickly. Mixing the two would make
evergreen pages harder to trust and would leave old news looking current.

## Decision

1. News lives in `knowledge/news/YYYY/MM/` as concepts of the new controlled type
   `News Brief`.
2. Each brief summarizes one development in the contributor's own words, links
   to the original sources, and explains why it matters to readers.
3. A brief must declare `published` (an ISO date), at least one entry in
   `sources`, and `stale_after`. The validator enforces these fields, the folder
   matching the publication month, and a `status` of `draft` or `deprecated`
   (never `stable`).
4. When a development changes lasting guidance, the brief links to the concept
   page that is updated. The concept page, not the brief, carries the guidance.
5. Scope, sourcing, neutrality, and corrections follow the
   [news editorial policy](../../governance/news-editorial-policy.md).
6. Automation may collect candidate links into `sources/`, but a person writes,
   reviews, and merges every brief. Nothing is published automatically.

## Options considered

| Option | Benefit | Cost or risk |
| --- | --- | --- |
| Dated briefs in the bundle (chosen) | One validated, searchable corpus; expiry is explicit metadata. | Needs a new type and validator rules. |
| A separate news repository | Keeps the bundle evergreen. | Duplicates the review and safety pipeline; readers lose cross-links. |
| Automated feed aggregation | Little effort per item. | Copies external text, cannot judge relevance, and bypasses review and moderation. |

## Consequences

- News passes the same repository gate, link allowlist, and moderation scan as
  every other contribution. New outlets are added to the domain allowlist
  through review.
- Readers and AI tools can filter briefs by `type`, `published`, and
  `stale_after` in the generated catalog.
- The future reading site needs a news listing and feed; the
  [website plan](../../knowledge-base-upgrade/features/knowledge-website/README.md)
  tracks that work.

## Reconsider when

- The volume of briefs makes the bundle hard to navigate or validate.
- Readers ask for real-time updates that a reviewed, pull-request-based flow
  cannot provide.

## Related links

- [News](../news/index.md)
- [News brief template](../templates/news-brief-template.md)
- [Decision records](index.md)
