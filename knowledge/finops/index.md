# FinOps

FinOps is the practice of making cloud spending visible and owned, so that
engineering, product, and finance can decide together what is worth paying
for. It starts with knowing who owns each cost, then adds reporting, budgets,
alerts, and optimization.

**New here?** Start with [cost allocation basics](cost-allocation-basics.md),
then try the [cost analysis lab](cost-analysis-lab.md), which uses made-up data
and needs no cloud account.

## Learning and operating routes

| Guide | Outcome |
| --- | --- |
| [Cost allocation basics](cost-allocation-basics.md) | Define ownership, shared-cost policy, reconciliation, and unknown-cost handling. |
| [Reporting and unit economics](reporting-and-unit-economics.md) | Choose consistent metrics, freshness, scope, and useful business denominators. |
| [Budgets, forecasts, and alerts](budgets-forecasts-and-alerts.md) | Separate approved funding, estimates, notification, and controlled actions. |
| [Anomaly response](anomaly-response.md) | Diagnose growth, usage/rate changes, delayed data, and unintended cost. |
| [Rightsizing and savings validation](rightsizing-and-savings-validation.md) | Validate capacity changes and distinguish modeled avoidance from realized results. |
| [Commitments and rate optimization](commitments-and-rate-optimization.md) | Understand obligations, utilization/coverage, and overlapping savings claims. |
| [Kubernetes allocation](kubernetes-cost-allocation.md) | Join cluster labels/metrics with real charges and owned shared/idle pools. |
| [Cost analysis lab](cost-analysis-lab.md) | Execute synthetic calculations and thirteen tests without account access. The runnable files live in [examples](../../examples/finops/README.md). |

## AWS implementation routes

- [AWS FinOps](../cloud/aws/finops/index.md) — tag activation/backfill, budgets/anomalies, cost data/exports, optimizer/commitments, and storage/network investigations.
- [AWS networking](../cloud/aws/networking/index.md) — trace the path behind transfer, NAT, and endpoint costs.

## Evidence and scope

Reviewed 2026-10-29. Framework concepts are credited to the FinOps Foundation; linked sources retain their own licensing and the framework's attribution requirements. Original examples are synthetic and do not quote current provider prices or customer outcomes. Account-backed notification delivery, real billing reconciliation, commitment decisions, and workload optimization remain follow-up evidence.

[Back to knowledge bundle](../index.md)
