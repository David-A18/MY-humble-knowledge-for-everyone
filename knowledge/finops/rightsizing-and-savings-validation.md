---
type: How-to Guide
title: Rightsizing and savings validation
description: Choose a workload-aware capacity change and distinguish recommendation
  estimates, normalized cost avoidance, and realized financial results.
tags:
- finops
- rightsizing
- optimization
status: draft
maturity: draft
audience: Platform engineers and cloud cost owners
maintainer: unassigned
sources:
- id: finops-usage
  title: FinOps Foundation — Usage Optimization
  resource: https://www.finops.org/framework/capabilities/usage-optimization/
- id: finops-rate
  title: FinOps Foundation — Rate Optimization
  resource: https://www.finops.org/framework/capabilities/rate-optimization/
- id: aws-optimizer-preferences
  title: Compute Optimizer rightsizing preferences
  resource: https://docs.aws.amazon.com/compute-optimizer/latest/ug/rightsizing-preferences.html
---

# Rightsizing and savings validation

Rightsizing changes capacity or configuration to meet measured demand with appropriate reliability headroom. It is one form of usage optimization, alongside removing unused work, scheduling, elasticity, and architectural changes.[^finops-usage] A low average CPU value alone is insufficient evidence to downsize.

## 1. Record a defensible baseline

Define workload owner, representative periods, demand units, latency/error/SLO limits, peak/burst behavior, CPU, memory, I/O, network, storage, concurrency, and recovery/failover needs. Note incomplete telemetry and upcoming changes. For AWS recommendations, missing memory metrics and chosen headroom/percentile preferences affect what the tool can justify.[^aws-optimizer-preferences]

Write a hypothesis such as: reduce one capacity tier while preserving the defined peak load and failover requirement, then compare cost per successful transaction. Specify success/failure thresholds, rollout scope, and rollback before changing production.

## 2. Model the full effect

Include compute, storage, licensing, network, observability, migration effort, and commitments. A smaller instance can still leave a fixed commitment bill unchanged or shift demand to another bottleneck. Do not add a rightsizing recommendation and a commitment recommendation as if they both apply independently to the original spend.[^finops-rate]

| Evidence level | Honest statement |
| --- | --- |
| Recommendation | A tool estimates an opportunity under its assumptions. |
| Modeled scenario | Defined rates/quantities imply a possible difference. |
| Controlled workload test | The chosen configuration met the tested behavior. |
| Normalized comparison | Cost per comparable output improved under stated conditions. |
| Realized financial outcome | Reconciled billing and commitments show the actual attributable effect. |

## 3. Change in a controlled scope

Use the workload's normal change process: a staging/load test or small production slice where appropriate, explicit ownership, health observations, and a reversible configuration. Monitor tail latency, throttling, OOMs, retries, queues, and recovery behavior, not only utilization. Roll back on the agreed failure signal even if the nominal hourly rate is lower.

## 4. Compare comparable demand

The synthetic lab contrasts 600 cost for 10,000 successful units with 660 for 15,000 units. The bill-like total rises by 60, but unit cost falls from 0.060 to 0.044. Applying the old unit cost to the new demand yields a 900 baseline and 240 modeled cost avoidance. That is a counterfactual calculation, not proof that a real invoice fell by 240.

Record changes to demand mix, quality, time window, cost basis, and allocation. A cheaper cost per request caused by counting failed retries as successful units is not an improvement. Validate the denominator and include new costs before accepting the result.

## Close and clean up

Retain the before/after configuration, representative workload evidence, rate/cost basis, owner, and decision. Delete only disposable test resources after verifying the production recovery path and retaining required data. This guide makes no resource change; the local lab reads synthetic inputs and requires no cloud cleanup.

## Evidence and limits

Official sources reviewed on 2026-10-29. Examples use synthetic assumptions, not customer bills, current price quotations, or verified production savings. The local Decimal-based lab was executed with Python 3.13.17; AWS account queries, notifications, purchases, resource changes, and live optimization were not executed. These draft guides do not imply ownership approval or runtime evidence for an organization.

## Related routes

- [Rate optimization and commitments](commitments-and-rate-optimization.md).
- [AWS recommendation workflow](../cloud/aws/finops/compute-optimizer-and-commitments.md).
- [Back to this section](index.md)
- [Back to FinOps](index.md)

[^finops-usage]: [FinOps Foundation — Usage Optimization](https://www.finops.org/framework/capabilities/usage-optimization/)
[^finops-rate]: [FinOps Foundation — Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/)
[^aws-optimizer-preferences]: [Compute Optimizer rightsizing preferences](https://docs.aws.amazon.com/compute-optimizer/latest/ug/rightsizing-preferences.html)
