---
type: How-to Guide
title: AWS Compute Optimizer and commitment decisions
description: Evaluate AWS recommendations against workload telemetry, operating risk,
  existing commitments, and verified financial outcomes.
tags:
- finops
- aws
- rightsizing
- savings-plans
status: draft
maturity: draft
audience: Platform engineers and cloud cost owners
maintainer: unassigned
sources:
- id: aws-optimizer
  title: Compute Optimizer EC2 recommendations
  resource: https://docs.aws.amazon.com/compute-optimizer/latest/ug/view-ec2-recommendations.html
- id: aws-optimizer-metrics
  title: Compute Optimizer metrics
  resource: https://docs.aws.amazon.com/compute-optimizer/latest/ug/metrics.html
- id: aws-optimizer-preferences
  title: Compute Optimizer rightsizing preferences
  resource: https://docs.aws.amazon.com/compute-optimizer/latest/ug/rightsizing-preferences.html
- id: aws-plan-types
  title: Savings Plans types
  resource: https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html
---

# AWS Compute Optimizer and commitment decisions

Compute Optimizer recommendations help identify configuration options; they are not instructions to resize production automatically or proof that the next invoice will fall. Separate the engineering performance decision from the financial commitment decision.

## Establish recommendation context

Record resource/Region, recommendation timestamp, observation window, included metrics, finding/reasons, projected utilization, migration/platform constraints, and performance risk. Compute Optimizer uses accumulated metrics and can use a longer paid history option; verify the actual configuration rather than assuming a generic graph represents your peak workload.[^aws-optimizer][^aws-optimizer-metrics]

Memory-sensitive decisions need appropriate memory telemetry. Current EC2 preferences support CloudWatch-agent or configured external memory metrics and adjustable headroom/percentile assumptions.[^aws-optimizer-preferences] Missing memory data does not justify inferring safe memory downsizing from low CPU alone.

## Inspect an existing recommendation

This read-only command requires account access, permissions, an enrolled/supported resource, and representative metrics. Replace the ARN, profile, and resource Region. It was checked offline only.

```bash
aws compute-optimizer get-ec2-instance-recommendations --instance-arns <instance-arn> --profile <profile> --region <region> --no-cli-pager
```

What it does: retrieves the selected instance's recommendation/options and supporting metrics/risk fields. It does not opt in an account, enable a paid feature, change an instance, or purchase a commitment. Missing findings can mean insufficient history, unsupported scope, or access problems; investigate those conditions before making a decision.

## Validate the workload change

Use the [rightsizing process](../../../finops/rightsizing-and-savings-validation.md): define peak/SLO/failover requirements, perform a scoped test or rollout, retain rollback, and compare useful output plus all changed cost components. Check architecture/AMI compatibility, memory, I/O, network, licensing, and interruption behavior, not only the headline compute rate.

Inspect existing commitments before claiming benefit. A smaller resource can reduce eligible usage while leaving a prior hourly obligation intact. An overlapping commitment recommendation can count the same original spend twice if modeled independently.

## Make the commitment choice separately

Current Savings Plans types include Compute, Database, EC2 Instance, and SageMaker AI, with different eligibility/flexibility.[^aws-plan-types] Confirm the current product, term, payment timing, regional/family/service constraints, sharing policy, remaining demand, and downside scenario. Do not assume Database Savings Plans and database reservations are the same instrument, or that every usage charge is covered.

Assign the financial decision to the organization's approved engineering/finance/procurement owners. This guide makes no purchase recommendation, resource change, or actual savings claim. The synthetic quantity/rate lab demonstrates accounting logic; an account-backed result needs real contract, utilization/coverage, workload, and billing evidence.

Remove only task-owned test reports and temporary workload resources after their normal recovery/retention steps. Commitments and real production capacity are not disposable cleanup artifacts.

## Evidence and limits

Official sources reviewed on 2026-10-29. Examples use synthetic assumptions, not customer bills, current price quotations, or verified production savings. The local Decimal-based lab was executed with Python 3.13.17; AWS account queries, notifications, purchases, resource changes, and live optimization were not executed. These draft guides do not imply ownership approval or runtime evidence for an organization.

## Related routes

- [Commitment modeling](../../../finops/commitments-and-rate-optimization.md).
- [AWS spending alerts](budgets-and-cost-anomaly-detection.md).
- [Back to this section](index.md)
- [Back to FinOps](../../../finops/index.md)

[^aws-optimizer]: [Compute Optimizer EC2 recommendations](https://docs.aws.amazon.com/compute-optimizer/latest/ug/view-ec2-recommendations.html)
[^aws-optimizer-metrics]: [Compute Optimizer metrics](https://docs.aws.amazon.com/compute-optimizer/latest/ug/metrics.html)
[^aws-optimizer-preferences]: [Compute Optimizer rightsizing preferences](https://docs.aws.amazon.com/compute-optimizer/latest/ug/rightsizing-preferences.html)
[^aws-plan-types]: [Savings Plans types](https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html)
