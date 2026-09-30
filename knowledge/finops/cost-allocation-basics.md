---
type: How-to Guide
title: Cost allocation basics
description: Build a simple cost-allocation policy that assigns direct costs, handles shared costs explicitly, and measures what remains unallocated.
tags: [finops, cost-allocation, tagging, governance]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: finops-allocation
    resource: https://framework.finops.org/framework/capabilities/allocation/
    title: FinOps Framework allocation capability
  - id: finops-cost-allocation-guide
    resource: https://www.finops.org/wg/cloud-cost-allocation/
    title: FinOps cloud cost allocation guide
stale_after: 2026-12-20
---

# Cost allocation basics

## Purpose

Use this guide to create a first cost-allocation policy that lets engineering,
product, and finance explain who owns cloud usage and what to do with shared
costs. It assumes access to a cost report and agreement on the teams or
products that will receive costs. The example is illustrative; no billing
system was changed for this page.

**Allocation** means assigning a cost to a responsible group. It may use
account or project ownership, tags, labels, a business mapping, or a shared
cost rule. A tag is one input, not the policy itself. The FinOps Framework
separates allocation, metadata, and shared-cost strategies for this
reason.[^finops-allocation]

Think of a bill for a shared building: a team can own its room directly, while
the lobby needs an agreed rule. The analogy stops at measurement. Cloud
providers expose different usage data, and a cost line may be impossible to
attribute to one resource.

## Define the allocation model

Start with a small set of mandatory ownership dimensions. Use names that match
systems people already recognize. Ask finance and product owners which
groupings they need before creating metadata keys.[^finops-allocation]

| Dimension | Example values | Decision it supports |
| --- | --- | --- |
| Owner | `payments`, `platform`, `data` | Who investigates cost and usage? |
| Application or service | `checkout-api`, `event-pipeline` | Which product or technical service consumed it? |
| Environment | `development`, `staging`, `production` | Which lifecycle boundary generated the cost? |
| Cost center or product | `cc-1042`, `subscriptions` | Which budget or business outcome receives the cost? |

Keep authoritative values in one owned registry. Do not create a tag key unless
a report, budget, policy, or decision will use it. Decide whether the first
report is **showback** (visibility) or **chargeback** (a financial transfer);
the second needs explicit agreement with finance.

## Make ownership metadata part of provisioning

1. Define required keys, allowed values, exceptions, and the person or team
   that approves exceptions.
2. Map accounts, projects, subscriptions, and resource tags to those values
   where the provider supplies that data. Record which charges cannot carry
   resource tags.
3. Put ownership metadata in provisioning templates and checks, with an
   exception route for legitimate shared or unsupported charges.
4. Produce a first report that separates directly assigned, shared, and
   still unallocated cost. Measure money, not just resource count.
5. Have owners correct newly unallocated costs while the context is fresh.

Expected result: a report can answer both "which team owns this cost?" and
"which costs still need a decision?" If the two answers disagree with an
account or resource inventory, inspect the mapping and report time period
before changing tags.

> [!IMPORTANT]
> Cost data and tag availability vary by provider and service. Validate
> reporting behavior in the target provider before treating a tag as an
> immediate allocation signal. For AWS, see the separate [cost allocation tags
> explanation](../cloud/aws/finops/cost-allocation-tags.md): a resource tag
> alone does not make it available in billing reports.

## Decide how shared costs work

Shared networking, observability, security, platform clusters, and support plans often cannot be assigned directly to one application. For each shared cost, document one of these choices:

- Keep it centrally funded and visible.
- Split it by a fixed percentage.
- Split it proportionally by direct spend or a usage metric.
- Assign it to a platform product with an agreed internal price model.

The important outcome is that a shared cost is visible and has a documented
rule, rather than silently appearing as unallocated spend. The FinOps
Framework explicitly allows a shared cost to remain centrally funded when
that is a deliberate business choice.[^finops-allocation]

## Illustrative first report

Suppose one month has 100 units of cloud cost. Account and tag mappings assign
60 directly to two product teams. A shared platform account costs 30 and
finance agrees to keep it centrally funded. The final 10 have no reliable
owner yet.

| Bucket | Amount | How to explain it |
| --- | ---: | --- |
| Directly assigned | 60 | The mapped account or resource metadata identifies an owner. |
| Shared, rule recorded | 30 | Platform owns the central budget; it is visible but not charged to either product. |
| Unallocated | 10 | No trustworthy mapping or shared-cost decision exists. |

The buckets add to 100. Direct allocation coverage is 60%, while the share
with an explicit ownership or shared-cost rule is 90%. Do not call the latter
"direct coverage" or count the shared 30 twice. These numbers are invented
to show the calculation, not measured cloud usage.

## Measure coverage

Track these measures at a consistent cadence:

| Measure | Calculation | Use |
| --- | --- | --- |
| Direct allocation coverage | Directly allocated cost / total cost | Shows how much spend maps directly to an owner. |
| Unallocated cost | Cost with no valid owner or hierarchy mapping | Prioritizes remediation by financial impact. |
| Metadata compliance by cost | Cost carrying valid required metadata / total cost | Prevents a low-cost resource count from hiding expensive gaps. |
| Shared-cost rule coverage | Shared cost with a documented allocation rule / total shared cost | Shows whether the remaining cost is understood. |

Choose a period, currency, and cost basis before comparing runs. Reconcile the
three buckets to the provider's total for the same basis. A higher coverage
percentage is useful only when the assignments are accurate; do not hide
uncertain costs in a catch-all owner to improve the number.

## Check your understanding

- Can you identify a direct owner and a shared-cost rule without relying on
  the same tag for every charge?
- If the report says 90% of cost has a decision, how much is directly
  assigned in the example?
- Who approves the rule for the shared platform account?

## Official documentation for deeper study

- [FinOps Framework: Allocation](https://framework.finops.org/framework/capabilities/allocation/) defines the allocation, metadata, and shared-cost strategies.
- [FinOps cloud cost allocation guide](https://www.finops.org/wg/cloud-cost-allocation/) discusses shared-cost choices and organizational practice.

## Related links

- [AWS cost allocation tags](../cloud/aws/finops/cost-allocation-tags.md)
- [FinOps Framework allocation capability](https://framework.finops.org/framework/capabilities/allocation/)
- [Back to FinOps](index.md)
- [Back to knowledge index](../index.md)

[^finops-allocation]: [FinOps Framework - Allocation](https://framework.finops.org/framework/capabilities/allocation/), source record `finops-allocation`.
