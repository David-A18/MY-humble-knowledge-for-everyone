---
type: Tutorial
title: Synthetic FinOps calculation lab
description: Run deterministic cost reconciliation, shared allocation, demand normalization,
  and non-overlapping savings calculations without an account.
tags:
- finops
- lab
- decimal
- synthetic-data
status: draft
maturity: draft
audience: Platform engineers and cloud cost owners
maintainer: unassigned
sources:
- id: finops-allocation
  title: FinOps Foundation — Allocation
  resource: https://www.finops.org/framework/capabilities/allocation/
- id: finops-units
  title: FinOps Foundation — Unit Economics
  resource: https://www.finops.org/framework/capabilities/unit-economics/
- id: finops-rate
  title: FinOps Foundation — Rate Optimization
  resource: https://www.finops.org/framework/capabilities/rate-optimization/
---

# Synthetic FinOps calculation lab

This local-only lab turns the reporting rules into executable calculations. It reads a small synthetic CSV and prints JSON; it never reads credentials, queries a provider, sends notifications, purchases commitments, or changes infrastructure. Every currency amount is a teaching input, not an AWS quote or customer bill.

## Prerequisites and files

Use Python 3.10+ with only its standard library. Authoring execution used Python 3.13.17. The [CSV](synthetic-ledger.csv) is a deliberately normalized USD ledger for one month with cent precision and a `synthetic-amortized` label. It is not CUR, FOCUS, or a full accounting ingestion schema.

The [calculator](cost-analysis.py) uses Decimal rather than binary floats. The [tests](test-cost-analysis.py) cover reconciliation and misleading-result edge cases. A real export adapter must preserve higher-precision source values and explicitly handle charge classes, currencies, periods, replacements, and cost bases.

## Run from the repository root

```bash
python knowledge/finops/examples/cost-analysis-lab/cost-analysis.py
python knowledge/finops/examples/cost-analysis-lab/test-cost-analysis.py
```

What it does: prints a deterministic report and runs thirteen tests. JSON decimal values are strings to preserve exact arithmetic. The calculator writes no output file and leaves the fixture unchanged; Python may create an ignored bytecode cache during tests.

The [FinOps example workflow](../../../../.github/workflows/finops-examples.yml) runs the same tests/report on Python 3.13 in Linux CI. Inspect the exact published commit for its hosted result; local authoring execution and hosted validation are separate evidence.

## Explain the expected results

| Example | Expected evidence |
| --- | --- |
| Source total | Six synthetic rows total 675.01 after a -20.00 payments credit. |
| Direct costs | Payments 330.00, data 200.00, unknown owner 25.00. |
| Shared pool | 120.01 allocated by explicit weights payments:data = 3:1. |
| Final allocation | Payments 420.01, data 230.00, unallocated 25.00; total still 675.01. |
| Uneven cents | Largest-remainder allocation with alphabetical tie-break reconciles exactly. |
| Demand comparison | 600/10,000 versus 660/15,000 gives unit costs .060/.044 and 240 modeled avoidance at later demand, despite total cost rising 60. |
| Quantity/rate | 100 × 1.00 versus 80 × .75 gives a combined difference of 40, not the naïve sum of percentage reductions. |
| Straight-line run rate | 960 over 12 of 30 days extrapolates to 2,400, subject to the stated assumptions. |

The shared-cost rule is an illustrative organizational policy.[^finops-allocation] Unit comparisons require comparable useful outputs.[^finops-units] Quantity and rate effects must not count the same original spend twice.[^finops-rate] The demand comparison, quantity/rate example, and small ledger are separate teaching scenarios, not one consolidated business case.

## Failure cases and limits

Tests reject duplicate IDs, mixed periods/currencies, non-finite values, unsupported scope, fractional-cent ledger amounts, empty ledgers, invalid weights, and invalid forecast periods. Zero business units produce an undefined unit cost instead of a misleading zero. Shared credits preserve their sign and total.

The toy anomaly example compares a fixed baseline with absolute and relative thresholds. It has no learned seasonality and is not an implementation of AWS Cost Anomaly Detection. A zero baseline is labeled cold-start and uses the defined absolute-threshold path; it cannot support a percentage-growth claim.

The results prove arithmetic under synthetic assumptions. They do not establish budget delivery, financial approval, safe rightsizing, billing reconciliation, a causal savings attribution, or production anomaly quality. Use the surrounding guides to design that evidence separately.

## Cleanup

The program creates no account resources or reports to destroy. If you redirect JSON to a local file, remove only that task-owned output after retaining the exercise evidence. Do not feed customer billing data into a public example or commit generated real-cost reports.

## Evidence and limits

Official sources reviewed on 2026-10-29. Examples use synthetic assumptions, not customer bills, current price quotations, or verified production savings. The local Decimal-based lab was executed with Python 3.13.17; AWS account queries, notifications, purchases, resource changes, and live optimization were not executed. These draft guides do not imply ownership approval or runtime evidence for an organization.

## Related routes

- [Reporting contracts](../../reporting-and-unit-economics.md).
- [Rightsizing evidence](../../rightsizing-and-savings-validation.md).
- [Back to this section](index.md)
- [Back to FinOps](../../index.md)

[^finops-allocation]: [FinOps Foundation — Allocation](https://www.finops.org/framework/capabilities/allocation/)
[^finops-units]: [FinOps Foundation — Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/)
[^finops-rate]: [FinOps Foundation — Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/)
