---
type: Troubleshooting Guide
title: AWS troubleshooting first checks
description: Start any AWS investigation by confirming the account, Region, and identity, finding recent changes in CloudTrail, and reading access-denied errors correctly.
tags: [aws, troubleshooting, iam, cloudtrail]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: get-caller-identity
    resource: https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html
    title: aws sts get-caller-identity
  - id: cloudtrail-events
    resource: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html
    title: Working with CloudTrail event history
  - id: iam-access-denied
    resource: https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html
    title: Troubleshoot access denied error messages
---

# AWS troubleshooting first checks

Most AWS problems are solved faster by checking a few basic facts first than by
guessing. Are you looking at the right account and Region? What changed
recently? What does the exact error message say? These checks take minutes and
often find the cause straight away.

## 1. Confirm where you are looking

```bash
aws sts get-caller-identity
aws configure get region
```

What it does: shows the account and identity your credentials use, and the
default Region of your CLI profile.[^get-caller-identity] A resource that
"does not exist" is very often in another account or Region.

## 2. Find what changed

Most incidents follow a change. CloudTrail records API calls in your account,
and its event history lets you search the last 90 days of management
events.[^cloudtrail-events]

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=<resource-name> \
  --max-results 20
```

What it does: lists recent API calls that touched the named resource, with who
made them and when. Replace `<resource-name>` with the resource's name or ID.

## 3. Read access-denied errors carefully

An `AccessDenied` error usually names the identity, the action, and the
resource. Check, in order:[^iam-access-denied]

1. **Identity:** is it the role you expected? (step 1)
2. **Identity policy:** does it allow this exact action on this resource?
3. **Resource policy:** does the bucket, key, or queue policy allow it?
4. **Guardrails:** does an organization policy (SCP), permissions boundary, or
   session policy deny it? An explicit deny always wins.

See [IAM policy evaluation](../security/iam-policy-evaluation-and-least-privilege.md)
for how AWS combines these.

## 4. Capture the evidence

Write down the exact error message, the time, the Region, the request ID if
shown, and what you already checked. It saves time when you ask for help or
open a support case.

## Common problems and where to go

| Symptom | Start here |
| --- | --- |
| Cannot connect to an instance, endpoint, or service | [AWS network connectivity troubleshooting](../networking/network-connectivity-troubleshooting.md) |
| Access denied or unexpected permission | [IAM policy evaluation](../security/iam-policy-evaluation-and-least-privilege.md) |
| Pods on EKS cannot reach AWS services | [IRSA troubleshooting](../security/irsa-troubleshooting.md) |
| Unexpected cost increase | [Cost anomaly response](../../../finops/anomaly-response.md) |

## Related links

- [AWS fundamentals](../fundamentals/aws-fundamentals.md)
- [Back to AWS troubleshooting](index.md)

[^get-caller-identity]: [aws sts get-caller-identity](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html)
[^cloudtrail-events]: [Working with CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)
[^iam-access-denied]: [Troubleshoot access denied error messages](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html)
