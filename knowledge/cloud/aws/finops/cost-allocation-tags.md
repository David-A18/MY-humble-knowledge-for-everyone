---
type: "Explanation"
title: "Cost allocation tags"
description: "Understand how an AWS resource tag becomes a billing dimension, what activation and backfill can recover, and why some costs need another rule."
tags: [cloud, aws, finops]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: aws-cost-allocation-tags
    resource: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html
    title: AWS Billing - Organizing and tracking costs using cost allocation tags
  - id: aws-activate-tags
    resource: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html
    title: AWS Billing - Activating user-defined cost allocation tags
  - id: aws-tag-backfill
    resource: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-allocation-backfill.html
    title: AWS Billing - Backfill cost allocation tags
  - id: finops-allocation
    resource: https://framework.finops.org/framework/capabilities/allocation/
    title: FinOps Framework - Allocation
---

# Cost allocation tags

## Purpose

Use this page to understand why a tag visible on an AWS resource may be absent
from Cost Explorer, and how to make tagging useful for ownership reporting.
It explains the path from a resource label to a billing dimension; it does
not change an AWS account.

## The simple model

An AWS **tag** is a key and value attached to a resource, such as
`application=checkout`. A **cost allocation tag** is a tag key that has also
been activated for AWS billing reports. AWS can then group eligible usage
costs by values of that key.[^aws-cost-allocation-tags][^aws-activate-tags]

```text
resource has tag key and value
  -> eligible billing usage records carry the value
  -> management or standalone account activates the key
  -> refreshed cost report can group by that key
```

The arrows describe a data path, not an instant operation. AWS says a new
user-defined tag key can take up to 24 hours to appear for activation and up
to another 24 hours to activate. Report refresh adds its own delay. A resource
tag is therefore not proof that today's cost view already contains
it.[^aws-activate-tags][^aws-tag-backfill]

## Choose keys that answer questions

| Example key | Reader question it helps answer | Important limit |
| --- | --- | --- |
| `owner` | Who investigates this cost? | Decide whether a team or an individual is the stable owner. |
| `application` | Which product or service generated it? | One resource may serve several applications. |
| `environment` | Is this development, staging, or production cost? | Shared infrastructure may serve several environments. |
| `cost-center` | Which finance grouping receives it? | Confirm allowed values with finance before tagging. |

These are example keys, not AWS-required keys. Keep the approved keys and
values in one owned list and apply them consistently where a service supports
resource tagging. Do not place sensitive data in tags.[^aws-cost-allocation-tags]
The broader [cost allocation policy](../../../finops/cost-allocation-basics.md)
decides how to assign costs that tags cannot describe.[^finops-allocation]

## Example: a tag exists but Cost Explorer has no value

This scenario is illustrative; it is not an observed AWS bill. A team tags an
EC2 instance `application=checkout` on Monday. On Tuesday it filters Cost
Explorer by `application` and sees nothing.

There are several distinct questions to check:

1. Does the instance actually have the expected key and value? Spelling and
   capitalization matter.
2. Is the `application` key listed and active under **Billing and Cost
   Management → Cost allocation tags**? In a standard AWS Organization, the
   management account manages those activations; a standalone account can
   manage its own. AWS documents a separate bill-source path for billing
   transfer.[^aws-cost-allocation-tags][^aws-activate-tags]
3. Has the appearance, activation, and report refresh time passed? The AWS
   documentation gives the first two steps up to 24 hours each.[^aws-activate-tags]
4. Does the selected report period contain usage from a resource that carried
   that tag at the time? A newly added tag does not create historical resource
   values that were never present.[^aws-tag-backfill]

Expected result after activation and refresh: eligible instance cost for the
tagged period can appear under `application=checkout`. If the report still
does not match the resource inventory, inspect the specific service's tagging
and billing support, the time range, and untagged charges before changing
the allocation policy.

## What backfill can and cannot do

AWS lets management account users request cost allocation tag **backfill**
for up to twelve months. Backfill applies the current activation status to
earlier billing periods. It can expose a tag value for a past month **only if
that value was actually assigned to the resource in that month**. It cannot
invent a value for usage before the resource was tagged.[^aws-tag-backfill]

Backfill also refreshes Cost Explorer and cost data exports asynchronously, so
review the result after the documented refresh. Before requesting it, confirm
the historical tag coverage and intended reporting period with the billing
owner; the request changes historical cost views.[^aws-tag-backfill]

## Where tags stop helping

Not every charge is tied to a taggable resource, and a shared resource can
benefit several teams. Tags alone therefore cannot allocate the whole bill.
Use an account or project mapping where appropriate, and record a deliberate
rule for shared or otherwise unassigned costs. The FinOps Framework treats
allocation, metadata, and shared-cost strategies as related but distinct
decisions.[^finops-allocation]

## Check your understanding

- What is the difference between adding `application=checkout` to an
  instance and activating `application` for billing?
- If a tag was added in June, can backfill produce that tag value for March
  when the resource had no such tag?
- Which costs in your environment need an account mapping or shared-cost rule
  instead of a resource tag?

## Official documentation for deeper study

- [AWS cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html) defines tag types, activation, and billing use.
- [Activating user-defined tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html) gives the console path and timing.
- [Backfill cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-allocation-backfill.html) states the historical limit and refresh behavior.
- [FinOps Framework: Allocation](https://framework.finops.org/framework/capabilities/allocation/) places tags inside a broader allocation strategy.

## Related links

- [Cost allocation basics](../../../finops/cost-allocation-basics.md)
- [Back to AWS FinOps](index.md)
- [Back to AWS index](../index.md)
- [Back to knowledge index](../../../index.md)

[^aws-cost-allocation-tags]: [AWS Billing - Cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html), source record `aws-cost-allocation-tags`.
[^aws-activate-tags]: [AWS Billing - Activating user-defined cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html), source record `aws-activate-tags`.
[^aws-tag-backfill]: [AWS Billing - Backfill cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-allocation-backfill.html), source record `aws-tag-backfill`.
[^finops-allocation]: [FinOps Framework - Allocation](https://framework.finops.org/framework/capabilities/allocation/), source record `finops-allocation`.
