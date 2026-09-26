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
    resource: https://framework.finops.org/framework/capabilities/allocation/
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

## Related links

- [AWS cost allocation tags](../cloud/aws/finops/cost-allocation-tags.md)
- [FinOps Framework allocation capability](https://framework.finops.org/framework/capabilities/allocation/)
- [Back to FinOps](index.md)
- [Back to knowledge index](../index.md)
