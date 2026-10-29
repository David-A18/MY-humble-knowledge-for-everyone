---
type: How-to Guide
title: AWS storage and network cost investigations
description: Investigate retention, unused capacity, lifecycle, and traffic-path costs
  while preserving data and operational requirements.
tags:
- finops
- aws
- storage
- networking
status: draft
maturity: draft
audience: Platform engineers and cloud cost owners
maintainer: unassigned
sources:
- id: aws-s3-lifecycle
  title: S3 object lifecycle
  resource: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
- id: aws-s3-rules
  title: S3 lifecycle configuration elements
  resource: https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html
- id: finops-usage
  title: FinOps Foundation — Usage Optimization
  resource: https://www.finops.org/framework/capabilities/usage-optimization/
---

# AWS storage and network cost investigations

Compute rightsizing is only one cost driver. Storage retention, request/transition patterns, snapshots, telemetry, data transfer, and NAT/endpoints can dominate a workload. Investigate the actual charge dimensions and operating requirements before changing or deleting resources.[^finops-usage]

## Storage: price the lifecycle, not only stored bytes

For each candidate, record owner, data class, recovery/retention obligations, access frequency, object size/count, versioning, current/noncurrent versions, request/retrieval costs, and minimum duration constraints. A lower storage-class byte rate can be outweighed by retrieval, transition, or early-deletion charges.

S3 Lifecycle rules can transition or expire both existing and new matching objects. A newly enabled expiration rule can therefore affect data already old enough to match. Bucket policies do not generally block lifecycle actions merely by denying user actions.[^aws-s3-lifecycle] Review the exact rule/filter and data recovery implications before enabling it.

Versioned buckets need separate consideration of current versions, delete markers, and noncurrent-version actions. Expiring the current object is not a guarantee that all historical versions cease incurring charges.[^aws-s3-rules] Preserve retention/legal-hold and tested restore requirements; an apparently old object is not automatically disposable.

## Inspect, do not delete

Use a permitted profile and the real bucket/resource Region. These examples are read-only and were checked offline; they were not run against an account.

```bash
aws s3api get-bucket-lifecycle-configuration --bucket <bucket> --profile <profile> --region <region> --no-cli-pager
aws ec2 describe-volumes --filters Name=status,Values=available --profile <profile> --region <region> --no-cli-pager
```

What it does: reads lifecycle rules and lists unattached EBS volumes. `NoSuchLifecycleConfiguration` can simply mean none is configured. An available volume is a review candidate, not evidence it is safe to delete; check owner, recovery use, snapshots/retention, and expected future attachment.

## Network: explain the path and bytes

Group the charge by service, usage type, Region/AZ, and owning workload. Trace source/destination and whether the path includes cross-AZ/Region transfer, public egress, NAT processing, interface endpoints, load balancing, or repeated internal traffic. Use the [AWS network path guides](../networking/index.md) to identify the actual design.

Compare alternative paths with current regional pricing and the complete traffic distribution. A gateway endpoint can avoid a relevant NAT path for supported services, while interface endpoints introduce their own per-AZ/time/data model. One option is not universally cheaper. Correlate bill dimensions with flow/application metrics; do not claim a traffic reduction from a route diagram alone.

## Verify the outcome and preserve ownership

Test a retention/storage/path change on an approved scope, verify retrieval/recovery and application SLOs, then measure the relevant later billing period under the same metric. Check whether charges moved to retrieval, another AZ, or another service. Retain the before/after evidence and updated policy owner.

This guide deletes no data or network resource. A sandbox cleanup must name only task-owned objects, respect retention, and confirm that no production consumer depends on the volume, endpoint, or gateway. Cost pressure is not authorization to remove shared infrastructure.

## Evidence and limits

Official sources reviewed on 2026-10-29. Examples use synthetic assumptions, not customer bills, current price quotations, or verified production savings. The local Decimal-based lab was executed with Python 3.13.17; AWS account queries, notifications, purchases, resource changes, and live optimization were not executed. These draft guides do not imply ownership approval or runtime evidence for an organization.

## Related routes

- [Rightsizing and verification](../../../finops/rightsizing-and-savings-validation.md).
- [Cost Explorer investigations](cost-explorer-and-data-exports.md).
- [Back to this section](index.md)
- [Back to FinOps](../../../finops/index.md)

[^aws-s3-lifecycle]: [S3 object lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
[^aws-s3-rules]: [S3 lifecycle configuration elements](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html)
[^finops-usage]: [FinOps Foundation — Usage Optimization](https://www.finops.org/framework/capabilities/usage-optimization/)
