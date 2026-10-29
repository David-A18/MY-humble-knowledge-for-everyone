---
type: How-to Guide
title: Cost allocation basics
description: Establish a practical cloud cost-allocation policy using ownership metadata, hierarchy, shared-cost rules, and measurable coverage.
tags: [finops, cost-allocation, tagging, governance]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: finops-allocation
    resource: https://www.finops.org/framework/capabilities/allocation/
    title: FinOps Framework allocation capability
  - id: finops-cost-allocation-guide
    resource: https://www.finops.org/wg/cloud-cost-allocation/
    title: FinOps cloud cost allocation guide
stale_after: 2026-12-20
---

# Cost allocation basics

## Purpose

Create a cost-allocation policy that lets engineering, product, and finance understand who owns cloud usage and which costs need an explicit shared-cost rule.

## Define the allocation model

Start with a small set of mandatory ownership dimensions. Use names that match systems people already recognize.

| Dimension | Example values | Decision it supports |
| --- | --- | --- |
| Owner | `payments`, `platform`, `data` | Who investigates cost and usage? |
| Application or service | `checkout-api`, `event-pipeline` | Which product or technical service consumed it? |
| Environment | `development`, `staging`, `production` | Which lifecycle boundary generated the cost? |
| Cost center or product | `cc-1042`, `subscriptions` | Which budget or business outcome receives the cost? |

Keep authoritative values in one owned registry. Do not create a tag key unless a report, budget, policy, or decision will use it.

## Make ownership metadata part of provisioning

1. Define required keys, allowed values, exceptions, and the exception owner.
2. Apply the same vocabulary to accounts, projects, subscriptions, resource groups, and resource tags where each provider supports them.
3. Enforce required metadata in infrastructure templates, policy checks, or provisioning workflows.
4. Report unallocated spend by cost, not only by resource count.
5. Send exceptions to the accountable owner while the resource is still new.

> [!IMPORTANT]
> Cost data and tag availability vary by provider and service. Validate reporting behavior in the target provider before treating a tag as an immediate allocation signal.

## Decide how shared costs work

Shared networking, observability, security, platform clusters, and support plans often cannot be assigned directly to one application. For each shared cost, document one of these choices:

- Keep it centrally funded and visible.
- Split it by a fixed percentage.
- Split it proportionally by direct spend or a usage metric.
- Assign it to a platform product with an agreed internal price model.

The important outcome is that a shared cost is visible and has a documented rule, rather than silently appearing as unallocated spend.

## Measure coverage

Track these measures at a consistent cadence:

| Measure | Calculation | Use |
| --- | --- | --- |
| Direct allocation coverage | Directly allocated cost / total cost | Shows how much spend has a clear owner. |
| Unallocated cost | Cost with no valid owner or hierarchy mapping | Prioritizes remediation by financial impact. |
| Metadata compliance by cost | Cost carrying valid required metadata / total cost | Prevents a low-cost resource count from hiding expensive gaps. |
| Shared-cost rule coverage | Shared cost with a documented allocation rule / total shared cost | Shows whether the remaining cost is understood. |

## Reconcile totals, credits, and unknown owners

Define a report contract before allocating: currency, period/time zone, cost basis, included accounts/charge classes, and data freshness. A cash invoice and an amortized management view need not have the same timing. Choose the intended basis and keep it consistent through allocation.[^finops-allocation]

Preserve direct costs, shared pools, credits/refunds, and an explicit unallocated remainder. Do not silently spread unknown ownership over known teams to make coverage appear complete. Define the rounding rule and reconcile the final allocated total to the same source total.

For example, the [synthetic calculation lab](examples/cost-analysis-lab/index.md) totals 675.01 including a -20.00 credit. Payments/data direct costs are 330.00/200.00, unknown cost is 25.00, and a 120.01 shared pool is allocated 3:1. Final payments/data/unknown totals are 420.01/230.00/25.00, still 675.01. These are teaching amounts and a chosen allocation policy, not customer billing.

For coverage percentages, define the eligible charge base and how credits are treated. A zero or negative net denominator can make a percentage meaningless; report absolute exceptions and credit treatment rather than forcing a reassuring ratio. Allocation changes who sees a cost, not necessarily the provider total.

## Evidence and next steps

FinOps Foundation allocation sources were reviewed on 2026-10-29; the original governance choices remain draft/unassigned. The local Decimal example and its thirteen tests execute synthetic calculations only. Organization-specific ownership, billing reconciliation, showback/chargeback agreement, and real savings evidence remain follow-ups.

## Related links

- [AWS cost allocation tags](../cloud/aws/finops/cost-allocation-tags.md)
- [FinOps Framework allocation capability](https://www.finops.org/framework/capabilities/allocation/)
- [Back to FinOps](index.md)
- [Back to knowledge index](../index.md)

[^finops-allocation]: [FinOps Foundation allocation capability](https://www.finops.org/framework/capabilities/allocation/).
