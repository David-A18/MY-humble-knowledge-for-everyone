---
type: Template
title: News brief template
description: Start a dated, sourced news brief that explains what happened, why it matters, and what readers should do.
tags: [templates, news]
status: draft
audience: News contributors
maintainer: unassigned
---

# News brief template

> [!IMPORTANT]
> Copy this file to `knowledge/news/YYYY/MM/<short-kebab-title>.md`, list it in
> that month's `index.md`, and replace the frontmatter. Read the
> [news editorial policy](../../governance/news-editorial-policy.md) first.

Use this frontmatter. The validator requires `published`, at least one source,
and `stale_after`, and rejects `status: stable` for news:

```yaml
---
type: News Brief
title: Short factual headline
description: One sentence that says what happened and who it affects.
tags: [news, ai]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
published: 2026-11-19
stale_after: 2027-03-19
sources:
  - id: primary-announcement
    resource: https://example.com/announcement
    title: Title of the official announcement
---
```

Rarely, a brief is news that readers should know about right away. Then add
`alert: critical`, and optionally `alert_until` (an ISO date between
`published` and `stale_after`; without it the alert lasts until
`stale_after`). The website shows these briefs as a notice. Read
[critical alerts](../../governance/news-editorial-policy.md#critical-alerts)
in the editorial policy first:

```yaml
alert: critical
alert_until: 2026-12-03
```

## What happened

Two or three plain sentences: the date, who acted, and what changed.[^primary-announcement]

## Why it matters

Explain the concrete effect on readers: their tools, costs, jobs, security, or
plans.

## What to do

Give one next step, link the concept page that covers it, or write "No action
needed".

## Related links

- [News](../news/index.md)

After copying, change these to the month's `index.md` and `../../index.md`.

[^primary-announcement]: [Title of the official announcement](https://example.com/announcement)

The footnote definitions above render as the brief's source list.
