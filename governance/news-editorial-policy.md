# News editorial policy

The [news section](../knowledge/news/index.md) publishes short, dated briefs about
developments that affect the people who use this knowledge base. This policy
sets what we cover, how we source it, and how we correct it. The format
decision is recorded in
[ADR-0006](../knowledge/decision-records/adr-0006-news-briefs.md).

## Scope

Cover a development when it changes what readers can do, must do, or should
plan for. Three areas are in scope:

| Area | Examples of what qualifies |
| --- | --- |
| Artificial intelligence | New model capabilities or availability, AI regulation, safety incidents, open-source releases, and changes to AI tools that engineers use. |
| Technology | Major releases, end-of-life dates, security vulnerabilities with wide impact, cloud and platform changes, and standards. |
| Economy | Technology jobs and skills demand, interest-rate or inflation decisions that change infrastructure budgets, cloud pricing, trade rules affecting hardware, and major industry funding shifts. |

Out of scope: rumors, unconfirmed leaks, stock tips, product promotion,
celebrity news, and partisan political commentary.

## Cadence

Publish a weekly roundup with a small number of briefs that pass the scope test.
Covering fewer items well is better than covering everything. A significant
event, such as a critical vulnerability, can get its own brief between
roundups.

## Writing a brief

Use the [news brief template](../knowledge/templates/news-brief-template.md):

1. **What happened**: two or three plain sentences with the date and who acted.
2. **Why it matters**: the concrete effect on readers.
3. **What to do**: a next step, or "no action needed".
4. **Sources**: the primary source first (the official announcement, filing,
   regulator, or project page), then one reputable report if useful.

## Sourcing and licensing

- Prefer primary sources: official announcements, release notes, regulators,
  central banks, standards bodies, and statistics offices.
- Use reputable news organizations only to add context, and say when a claim
  comes from one outlet.
- Summarize in your own words. Do not copy articles, headlines verbatim beyond
  a short quote, images, or video. Link to them instead.
- New source domains must be added to the
  [domain allowlist](policy/allowed-link-domains.txt) in the same pull request,
  so a maintainer reviews them.

## Neutrality

Report what happened and its effects without taking political sides. For
economic or policy news, give the facts and the official reasoning, and
attribute forecasts to whoever made them.

## Freshness and corrections

- Set `stale_after` to when the brief stops being useful, usually three to
  six months after `published`.
- Fix a factual error in a new commit, and add a dated **Correction** note to the
  brief that says what changed.
- When a later event overturns a brief, mark it `deprecated` and link to the
  newer brief.

## Critical alerts

A brief can carry `alert: critical` when readers should know about it right
away, not at the next weekly roundup. The website shows these briefs as a
notice that pops up on every page until the alert ends. Use it rarely, for
example:

- a security vulnerability with wide impact that needs patching now;
- a change at a major technology company or AI lab that changes the tools,
  models, or plans readers depend on;
- a release or regulation that takes effect within days.

Rules:

- Only `critical` is allowed. The validator rejects any other value.
- The alert ends at `alert_until` if set, otherwise at `stale_after`. Keep it
  short: days or a few weeks, not months.
- The same sourcing rules apply. Never mark a rumor or an unconfirmed report
  critical.
- When the event is over or overturned, remove the alert in a new commit.

## Review

Every brief goes through the [repository gate](../.github/workflows/repository-gate.yml),
the [content policy](content-policy.md), and a maintainer review before it
merges.
