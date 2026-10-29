# AWS FinOps

Use these AWS implementation routes alongside the [provider-neutral FinOps model](../../../finops/index.md). Confirm billing scope, cost basis, data freshness, resource ownership, and the intended decision before making changes.

## Routes

| Guide | Outcome |
| --- | --- |
| [Cost allocation tags](cost-allocation-tags.md) | Separate resource tagging, billing activation, historical backfill, and report verification. |
| [Budgets and anomaly detection](budgets-and-cost-anomaly-detection.md) | Inspect delayed spending signals, notification ownership, and action boundaries. |
| [Cost Explorer and Data Exports](cost-explorer-and-data-exports.md) | Query a defined period/metric and design controlled, reconciled cost datasets. |
| [Compute Optimizer and commitments](compute-optimizer-and-commitments.md) | Validate recommendation risk and keep capacity and financial decisions separate. |
| [Storage and network costs](storage-and-network-costs.md) | Investigate retention, lifecycle, unused capacity, and transfer paths safely. |

## Practice and evidence

The [local synthetic lab](../../../finops/examples/cost-analysis-lab/index.md) exercises allocation and comparison math without AWS access. Sources were reviewed on 2026-10-29. CLI snippets were checked offline with AWS CLI 2.38.5; no billable query, notification, purchase, tag/backfill change, or production optimization was executed. Pricing, service eligibility, and account/view permissions require current verification for a real run.

## Follow-up acceptance

Record actual billing permissions/scope, a known-tag visibility/backfill check where appropriate, authorized notification delivery, real source-total reconciliation, and a controlled workload/financial result. Commitment purchase and production deletion are separately owned decisions, not tutorial cleanup.

[Back to AWS](../index.md) | [Back to FinOps](../../../finops/index.md)
