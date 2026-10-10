---
type: How-to Guide
title: Record evidence from a Crossplane S3 sandbox lab
description: Capture the actual identity, versions, managed-resource conditions, AWS result, and cleanup outcome of one authorized S3 lab run.
tags: [kubernetes, crossplane, aws, s3, validation]
status: draft
maturity: draft
audience: Maintainers validating the Crossplane S3 tutorial
maintainer: unassigned
sources:
  - id: crossplane-managed
    resource: https://docs.crossplane.io/latest/managed-resources/managed-resources/
    title: Crossplane - Managed Resources
  - id: aws-head-bucket
    resource: https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadBucket.html
    title: AWS - HeadBucket
---

# Record evidence from a Crossplane S3 sandbox lab

## Purpose and expected result

Use this record *during* an authorized run of
[Create and remove one S3 bucket with Crossplane](local-aws-s3-lab.md).
A successful record shows the same sandbox identity was used for
the provider Secret and AWS CLI, the managed resource became
`Synced=True` and `Ready=True`, AWS returned the expected
bucket and tag, and deletion was confirmed before the local
cluster was removed. A filled-in form alone proves none of
these events occurred.[^crossplane-managed][^aws-head-bucket]

Copy the sections below to a private implementation record.
Never include access keys, secret keys, session tokens, full
credential files, or unredacted private account details in
this knowledge bundle. Use `not run`, `failed`, or
`inconclusive` where appropriate; leave no blank that could
be mistaken for a pass.

## Run identity

| Field | Actual value |
| --- | --- |
| Run date and executor | Not run |
| Repository commit of lab instructions | Not run |
| AWS sandbox account and provider role, suitably redacted | Not run |
| Region | Not run |
| Temporary credential expiry, if known | Not run |
| Cleanup owner | Not run |

The AWS CLI identity check must use the **same credential file**
that becomes the provider Secret. A default laptop profile is
not sufficient evidence of the provider's account. Record only
the account and role comparison, not the credential values.
[^crossplane-managed]

## Versions and prerequisites

| Item | Actual version or result |
| --- | --- |
| Docker daemon and `kind` | Not run |
| Kubernetes context and server version | Not run |
| Helm version and Crossplane chart | Not run |
| Crossplane core image/version | Not run |
| AWS S3 provider package and revision | Not run |
| AWS family provider package and revision, if installed | Not run |
| Namespaced Bucket CRD group/version | Not run |
| AWS CLI version | Not run |

If an installed API or package differs from the lab, record
the difference and the source used to validate the change.
Do not silently treat a different provider as the tested one.

## Evidence by handoff

Record a short result and a timestamp for each checkpoint.
A screenshot or redacted log excerpt may be linked in a
private record. Do not paste full Secret or Pod environment
output here.

| Checkpoint | Pass criterion | Actual result and time |
| --- | --- | --- |
| Same-file AWS identity | The credential file used for the Secret returns the intended sandbox account and role. | Not run |
| Crossplane installation | Helm reports success; Crossplane Pods are ready in the expected `kind` context. | Not run |
| Provider installation | S3 provider and any required family provider are healthy; namespaced Bucket CRD exists. | Not run |
| Bucket candidate precheck | `HeadBucket` returned `404` using valid sandbox credentials before apply. A `403` or timeout is inconclusive. | Not run |
| Kubernetes request | Server dry run and apply accepted the exact manifest used for this run. | Not run |
| Provider reconciliation | The Bucket managed resource showed `Synced=True`, `Ready=True`, and the intended external name. | Not run |
| AWS observation | `HeadBucket` succeeded with the same identity and `get-bucket-tagging` showed the requested `Purpose` tag. | Not run |
| Kubernetes deletion | Bucket managed resource disappeared after a normal delete; no finalizer was removed manually. | Not run |
| AWS deletion | `HeadBucket` returned `404` with still-valid sandbox credentials after deletion. A `403` or expired token is inconclusive. | Not run |
| Local cleanup | ProviderConfig, Secret, local credential file, and `kind` cluster were removed after the AWS result was checked. | Not run |

AWS documents `HeadBucket` as returning a generic HTTP
status when a bucket is absent or the caller cannot access
it. Record the **actual status code and identity context**;
a generic command failure is not a deletion result.
[^aws-head-bucket]

This lab does not create a `BucketPublicAccessBlock`
managed resource or test drift correction. New S3 buckets
may already show public-access blocks. Do not record
those defaults as evidence that Crossplane installed
a separate public-access resource.

## When a checkpoint fails

| Field | Actual observation |
| --- | --- |
| First failing checkpoint and time | Not run |
| Kubernetes condition Reason and Message, redacted | Not run |
| Provider package/revision health | Not run |
| AWS error code and operation, redacted | Not run |
| External resource still present? | Not run |
| Temporary credentials still valid? | Not run |
| Follow-up owner and next check | Not run |

If deletion remains unresolved, keep the provider and
control plane available for reconciliation. A missing
Kubernetes object, an expired token, or a removed cluster
does not prove the AWS bucket is gone.[^crossplane-managed]

## Outcome and publication

Choose exactly one after reviewing the recorded evidence:

- **Passed:** every relevant checkpoint above has an observed
  result meeting its pass criterion.
- **Partial:** the bucket was created or observed, but one or
  more checks or cleanup steps remain incomplete.
- **Failed:** a required checkpoint contradicted its criterion.
- **Not run:** no authorized execution occurred.

Current outcome: **Not run**.

After a real run, update the
[lab](local-aws-s3-lab.md) only with the behavior actually
observed, then add the evidence to the
[improvement plan](../../../knowledge-base-improvement-plan.md)
and [maintenance review queue](../../../maintenance-review-queue.md)
where it affects their status. Keep this reusable template
free of invented run results.

## Related links

- [Create and remove one S3 bucket with Crossplane](local-aws-s3-lab.md)
- [How an AWS resource request moves through Crossplane](aws-resource-workflow.md)
- [Find the first failing Crossplane handoff](troubleshooting.md)
- [Back to Crossplane index](index.md)

[^crossplane-managed]: Crossplane, [Managed Resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/).
[^aws-head-bucket]: AWS, [HeadBucket](https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadBucket.html).
