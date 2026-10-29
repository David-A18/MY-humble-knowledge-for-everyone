---
type: How-to Guide
title: Budgets, forecasts, and alerts
description: Set an owned spending plan, model expected demand, and define budget
  responses without treating alerts as a hard spending cap.
tags:
- finops
- budgeting
- forecasting
status: draft
maturity: draft
audience: Platform engineers and cloud cost owners
maintainer: unassigned
sources:
- id: finops-budgeting
  title: FinOps Foundation — Budgeting
  resource: https://www.finops.org/framework/capabilities/budgeting/
- id: finops-forecasting
  title: FinOps Foundation — Forecasting
  resource: https://www.finops.org/framework/capabilities/forecasting/
- id: aws-budget-practices
  title: AWS Budgets best practices
  resource: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html
---

# Budgets, forecasts, and alerts

A budget is an approved spending boundary and accountability agreement; a forecast is an estimate of likely future cost. An alert asks someone to act when an agreed condition is met. Treat these as separate decisions instead of raising a budget whenever a forecast rises.[^finops-budgeting][^finops-forecasting]

## 1. Define scope before choosing thresholds

Record the accountable owner, period/time zone, currency, cost basis, included accounts/services, shared-cost rules, credits/tax treatment, business demand, and planned changes. Compare like with like: an amortized operating forecast can differ from the cash timing of an upfront purchase.

| Item | Required decision |
| --- | --- |
| Budget | Approved amount, approver, validity period, and exception process. |
| Forecast | Baseline, demand/rate assumptions, known changes, uncertainty, and refresh cadence. |
| Alert | Condition, recipient/backup owner, routing, expected response time, and escalation. |
| Action | Investigation, approved remediation, or controlled automation with impact and recovery. |

Use actual and forecast-based thresholds where they answer different questions. A low absolute amount changing by a large percentage may not warrant the same response as a modest percentage of a large workload. Thresholds must reflect the service's business and operational impact, not copied universal percentages.

## 2. Build an explainable forecast

Start with demand × effective unit cost, then account for fixed/shared costs, commitments, planned migrations, seasonality, and billing lag. Show a range or scenarios when uncertain. Do not label a simple straight-line extrapolation a reliable statistical forecast.

The [local lab](examples/cost-analysis-lab/index.md) uses a deliberately simple example: 960 synthetic USD accrued over 12 complete days in a 30-day period gives a 2,400 run-rate estimate. If data is delayed or a deployment doubles demand tomorrow, that arithmetic is not a prediction of the final bill.

## 3. Test the response path

Before enabling enforcement, verify that the intended owner can receive and interpret a test notification through an authorized process, knows which data to inspect, and can reach the service owner. This guide sends no notifications.

Budget alerts do not inherently stop spending. Provider billing data is delayed, and separately configured actions have permissions and operational limitations. For example, stopping one EC2 instance in an Auto Scaling group can cause replacement rather than lasting savings.[^aws-budget-practices] An automatic deny/stop action therefore needs a separately reviewed impact and recovery design.

## 4. Close the loop

At each review, explain budget-to-forecast and budget-to-actual variance using demand, rate, scope, timing, and allocation changes. Keep the original approved budget visible when documenting exceptions. Track response effectiveness and false alerts rather than only counting configured thresholds.

Remove only test-owned alert/subscription resources when an exercise ends, after confirming a real owner still receives needed production notifications. Provider-specific setup and notification delivery remain live acceptance work; the calculation lab requires no account cleanup.

## Evidence and limits

Official sources reviewed on 2026-10-29. Examples use synthetic assumptions, not customer bills, current price quotations, or verified production savings. The local Decimal-based lab was executed with Python 3.13.17; AWS account queries, notifications, purchases, resource changes, and live optimization were not executed. These draft guides do not imply ownership approval or runtime evidence for an organization.

## Related routes

- [Anomaly response](anomaly-response.md).
- [AWS budgets and anomaly detection](../cloud/aws/finops/budgets-and-cost-anomaly-detection.md).
- [Back to this section](index.md)
- [Back to FinOps](index.md)

[^finops-budgeting]: [FinOps Foundation — Budgeting](https://www.finops.org/framework/capabilities/budgeting/)
[^finops-forecasting]: [FinOps Foundation — Forecasting](https://www.finops.org/framework/capabilities/forecasting/)
[^aws-budget-practices]: [AWS Budgets best practices](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
