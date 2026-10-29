---
type: How-to Guide
title: AWS Cost Explorer and Data Exports
description: Choose a cost basis, query the intended billing scope, and build a reproducible
  export pipeline without treating delayed data as final invoices.
tags:
- finops
- aws
- reporting
- billing
status: draft
maturity: draft
audience: Platform engineers and cloud cost owners
maintainer: unassigned
sources:
- id: aws-cost-explorer
  title: AWS Cost Explorer
  resource: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html
- id: aws-cost-query
  title: AWS CLI get-cost-and-usage
  resource: https://docs.aws.amazon.com/cli/latest/reference/ce/get-cost-and-usage.html
- id: aws-cost-options
  title: Cost Explorer cost options
  resource: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-advanced.html
- id: aws-data-exports
  title: AWS Data Exports
  resource: https://docs.aws.amazon.com/cur/latest/userguide/what-is-data-exports.html
---

# AWS Cost Explorer and Data Exports

Use Cost Explorer for interactive investigation and scoped API queries; use Data Exports when a durable, controlled dataset is needed for repeatable analysis. Start with the report's decision and cost basis, not a tool screenshot.

## Choose the metric and data boundary

Document billing account/view, start/end semantics, currency, cost metric, included charge types, grouping/filter definitions, and the data refresh timestamp. Unblended, amortized, and net views have different treatment of timing/discounts; compare the same basis across periods.[^aws-cost-options]

Cost Explorer data refreshes periodically and can arrive late. Programmatic API requests can incur charges, including pagination; a read-only query is not necessarily free.[^aws-cost-explorer] Review current pricing and access scope before running a broad automated scan. No billable account query was executed here.

## Inspect one bounded period

This is an illustrative read-only account query, not part of the offline lab. Use an authorized named profile and confirm who can see the returned billing scope.

```bash
aws ce get-cost-and-usage --time-period Start=2026-09-01,End=2026-10-01 --granularity DAILY --metrics AmortizedCost --group-by Type=DIMENSION,Key=SERVICE --profile <profile> --region us-east-1 --no-cli-pager
```

What it does: requests daily amortized cost grouped by service for a September interval whose end is exclusive.[^aws-cost-query] The CLI Region chooses the service endpoint; it is not a filter limiting costs to workloads in that Region. Inspect `Estimated`, returned units, groups, and pagination before treating the result as a complete period. A query definition is reproducible meaning, not proof the underlying data never changes.

## Choose and protect an export

AWS recommends CUR 2.0 in Data Exports for detailed cost/usage data; it also offers FOCUS-formatted tables and other export types. Select the actual schema/version, columns, and rows rather than assuming legacy CUR fields and APIs are identical.[^aws-data-exports]

For a production pipeline, define destination ownership, access/encryption, data freshness, update/replacement behavior, partition/query strategy, duplicate handling, and retention. Export storage, query engines, dashboards, and repeated API calls can add cost. Remove unnecessary identifying columns without destroying the ability to reconcile legitimate ownership.

## Reconcile and verify

Compare source totals to the intended billing view and charge basis, then reconcile allocation outputs. Investigate missing accounts, filters, unused commitments, credits/tax/support, late updates, and duplicate partitions before attributing a discrepancy to the cloud bill. Do not sum current and replaced versions of the same export blindly.

The local teaching CSV is deliberately not CUR or FOCUS data. It is a small, cent-normalized ledger with one currency/period; adapt real provider data through a separately tested ingestion layer that preserves its precision and semantics.

No export, bucket, dashboard, or query job was created for this guide. In a future sandbox, remove only task-owned exports/query outputs and storage after retaining required billing evidence; do not purge shared cost records as cleanup.

## Evidence and limits

Official sources reviewed on 2026-10-29. Examples use synthetic assumptions, not customer bills, current price quotations, or verified production savings. The local Decimal-based lab was executed with Python 3.13.17; AWS account queries, notifications, purchases, resource changes, and live optimization were not executed. These draft guides do not imply ownership approval or runtime evidence for an organization.

## Related routes

- [Reporting contract](../../../finops/reporting-and-unit-economics.md).
- [Tag activation and backfill](cost-allocation-tags.md).
- [Back to this section](index.md)
- [Back to FinOps](../../../finops/index.md)

[^aws-cost-explorer]: [AWS Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)
[^aws-cost-query]: [AWS CLI get-cost-and-usage](https://docs.aws.amazon.com/cli/latest/reference/ce/get-cost-and-usage.html)
[^aws-cost-options]: [Cost Explorer cost options](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-advanced.html)
[^aws-data-exports]: [AWS Data Exports](https://docs.aws.amazon.com/cur/latest/userguide/what-is-data-exports.html)
