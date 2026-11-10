---
type: Explanation
title: CloudTrail evidence and security detection
description: Distinguish API audit coverage, threat findings, posture findings, and
  tested response delivery.
tags:
- aws
- security
- cloudtrail
status: draft
maturity: draft
audience: Cloud and platform engineers
maintainer: unassigned
sources:
- id: trail-history
  title: CloudTrail event history
  resource: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html
- id: trail-data
  title: CloudTrail data-event configuration
  resource: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
- id: guardduty
  title: GuardDuty findings and sample findings
  resource: https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html
- id: securityhub
  title: Security Hub CSPM
  resource: https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html
---

# CloudTrail evidence and security detection

Security evidence starts with a concrete event question: who called which API, against which resource, from which context, and with what outcome? An audit event, a threat finding, and a posture finding provide different evidence. None alone proves that every relevant action was recorded or that a responder received an alert.

## Choose the evidence source

| Source | Useful question | Limit to check |
| --- | --- | --- |
| CloudTrail management events | Who changed a role, policy, trail, or resource configuration? | Correct account/Region, retention, event type, and delivery. |
| Configured CloudTrail data events | Who performed selected object/data-plane operations? | Resource/event selectors and cost; not part of ordinary Event history. |
| GuardDuty | What activity looks suspicious for enabled protections? | Finding scope, underlying evidence, duplicates, and detection coverage. |
| Security Hub CSPM | Which configured posture controls/findings need attention? | Enabled standards, accounts/Regions, aggregation, and suppression. |
| Application/Kubernetes audit records | What happened beyond AWS API boundaries? | Actual logging policy, identity join, and retention/privacy. |

Event history exposes the last 90 days of management events in a single account/Region; it is separate from configured trails/event stores. It does not include S3 object data events.[^trail-history] Trails do not log data events by default; explicitly choose the required selectors and evaluate volume/cost.[^trail-data]

## Inspect a recent management operation

```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRoleWithWebIdentity --start-time <utc-start> --end-time <utc-end> --profile <profile> --region <region> --no-cli-pager
```

What it does: searches Event history by one lookup attribute and time range. Choose the Region/account relevant to the recorded STS path and inspect pagination. An empty result can be a scope, time, delivery, or coverage problem; it does not prove no role was assumed. Restrict access to exported records, which can include identifiers and request details.

Join principal/session identity, event time, request ID, target and error with the workload's own timeline. Use actual data-event configuration to investigate an S3 read; `lookup-events` cannot substitute for it. Preserve raw evidence in controlled storage before producing redacted teaching examples.

## Test detection and response independently

GuardDuty findings represent potential security issues; generated sample findings carry fictitious data and test downstream handling, not real threat coverage.[^guardduty] Security Hub CSPM produces posture-control findings and aggregates supported findings; a posture score is not proof that a particular incident was detected.[^securityhub]

For a bounded exercise, record the sample or controlled event, routing rule, notification destination, responder acknowledgement, and elapsed times. Require idempotent handling of repeated events and a visible delivery-failure path. Test investigation and containment separately from notification. Creating a sample finding or reading a dashboard is not a completed response drill.

This guide sends no notification and enables no service. Future test cleanup removes task-owned rules/test records under the retention policy; it must not erase incident evidence, disable shared trails, or suppress real findings to make a dashboard green. Continue with [incident response](security-incident-response.md).

## Evidence and limits

Official sources reviewed on 2026-11-10. This draft records source review and local fixture checks where stated. AWS account calls, live EKS credentials, key/secret changes, detection delivery, and incident containment were not executed. CLI examples require a supported AWS CLI v2 and authorized account access; no CLI runtime version was tested in this batch.

[Back to AWS security](index.md) | [Back to AWS](../index.md)

[^trail-history]: [CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)
[^trail-data]: [CloudTrail data-event configuration](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)
[^guardduty]: [GuardDuty findings and sample findings](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html)
[^securityhub]: [Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
