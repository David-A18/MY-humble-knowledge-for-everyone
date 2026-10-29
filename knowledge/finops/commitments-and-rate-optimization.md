---
type: Explanation
title: Commitments and rate optimization
description: Compare usage and rate changes without double-counting benefits, and
  make commitment exposure visible before a purchase.
tags:
- finops
- commitments
- rate-optimization
status: draft
maturity: draft
audience: Platform engineers and cloud cost owners
maintainer: unassigned
sources:
- id: finops-rate
  title: FinOps Foundation — Rate Optimization
  resource: https://www.finops.org/framework/capabilities/rate-optimization/
- id: aws-savings-plans
  title: AWS Savings Plans
  resource: https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html
- id: aws-plan-types
  title: Savings Plans types
  resource: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
---

# Commitments and rate optimization

Usage optimization changes what you consume; rate optimization changes what you pay for eligible consumption. They interact. A commitment can lower eligible rates while creating an ongoing obligation that survives a workload reduction or migration.[^finops-rate]

## Separate mechanisms

| Mechanism | Primary question |
| --- | --- |
| Rightsizing/scheduling | Can less capacity or runtime meet the workload requirement? |
| Negotiated/effective rate | Which price applies to the actual billable usage? |
| Usage or spend commitment | What ongoing obligation is accepted for an eligible discount? |
| Interruptible capacity | Can the workload handle interruption and replacement? |
| Architecture/product change | Does changing the workload deliver better business value? |

Do not equate an advertised maximum discount with your realized reduction. Product eligibility, term, scope, utilization, sharing, payment timing, and workload plans matter. AWS Savings Plans exchange an hourly commitment for eligible discounted usage over a term.[^aws-savings-plans] Current product types include Compute, Database, EC2 Instance, and SageMaker AI plans with different boundaries; verify the current service-specific rules rather than assuming one commitment covers every workload.[^aws-plan-types]

## Use consistent denominators

Commitment utilization asks how much of the committed benefit/spend was consumed, using the product's defined denominator. Coverage asks how much eligible usage was covered by commitments. They answer different questions: high coverage can coexist with poor utilization if the commitment is oversized. Do not compare tool percentages without checking their metric definitions.

Review remaining eligible demand after planned rightsizing, shutdowns, migrations, and existing commitments. Use representative hourly distributions and downside scenarios, not only a monthly average. Account for future flexibility and the cost of unused commitment. The decision belongs with accountable engineering, finance, and procurement owners.

## Avoid overlapping savings claims

For a synthetic one-period example, quantity falls from 100 to 80 and rate falls from 1.00 to 0.75. Cost changes from 100 to 60. The quantity effect at the original rate is 20; the rate effect on the remaining 80 units is another 20. The combined difference is 40, not 45 obtained by adding 20% and 25% as if independent.

This decomposition is an explainable modeling convention. A fixed real commitment obligation, credits, license charges, or transfer costs can change the cash outcome. Use the [local lab](examples/cost-analysis-lab/index.md) to verify the arithmetic, then reconcile actual contracts/billing before claiming realized results.

## Decision and operational boundaries

Record assumptions, alternatives, eligible demand, downside exposure, review owner, and expiry/reassessment dates. A provider recommendation is input to that decision. Do not automate purchases or change availability commitments solely to pass an optimization target.

This page purchases nothing and recommends no particular commitment amount. A future account-backed exercise must use current pricing/eligibility and its normal financial approval process. Remove only task-owned reports after retention; an acquired commitment is not disposable infrastructure that a cleanup script can destroy.

## Evidence and limits

Official sources reviewed on 2026-10-29. Examples use synthetic assumptions, not customer bills, current price quotations, or verified production savings. The local Decimal-based lab was executed with Python 3.13.17; AWS account queries, notifications, purchases, resource changes, and live optimization were not executed. These draft guides do not imply ownership approval or runtime evidence for an organization.

## Related routes

- [Rightsizing validation](rightsizing-and-savings-validation.md).
- [AWS optimizer and commitments](../cloud/aws/finops/compute-optimizer-and-commitments.md).
- [Back to this section](index.md)
- [Back to FinOps](index.md)

[^finops-rate]: [FinOps Foundation — Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/)
[^aws-savings-plans]: [AWS Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html)
[^aws-plan-types]: [Savings Plans types](https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html)
