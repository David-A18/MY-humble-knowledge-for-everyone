---
type: Explanation
title: AWS fundamentals
description: Understand AWS Regions and Availability Zones, accounts, the shared responsibility model, and service quotas before building anything.
tags: [aws, fundamentals, beginner]
status: draft
audience: Beginning cloud engineers
maintainer: unassigned
sources:
  - id: global-infrastructure
    resource: https://aws.amazon.com/about-aws/global-infrastructure/
    title: AWS global infrastructure
  - id: shared-responsibility
    resource: https://aws.amazon.com/compliance/shared-responsibility-model/
    title: AWS shared responsibility model
  - id: service-quotas
    resource: https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html
    title: What is Service Quotas?
  - id: get-caller-identity
    resource: https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html
    title: aws sts get-caller-identity
---

# AWS fundamentals

Amazon Web Services (AWS) rents computing resources, such as servers, storage,
and databases, that you create through an API and pay for as you use them. Four
ideas shape almost every AWS design: **where** resources run (Regions and
Availability Zones), **who owns** them (accounts), **who secures what** (the
shared responsibility model), and **how much** you can create (quotas).

## Regions and Availability Zones

- A **Region** is a geographic area, such as `eu-west-1` (Ireland). Most
  resources live in one Region, and data stays there unless you copy it.
- An **Availability Zone (AZ)** is one or more separate data centers inside a
  Region, with independent power and networking.[^global-infrastructure]

Running copies of an application in at least two AZs means one data-center
failure does not take it down. Choose a Region close to your users and allowed
by your data-protection rules.

## Accounts

An AWS account is the container for resources, permissions, and the bill.
Organizations use separate accounts for production, development, and security
tools, so a mistake or breach in one does not spread to the others. See
[AWS governance and human access](../governance-and-access/index.md) for how
to organize accounts.

Before any change, check which account and identity your tools are using:

```bash
aws sts get-caller-identity
```

What it does: prints the account ID and the user or role your credentials
belong to, without changing anything.[^get-caller-identity] Wrong-account
changes are one of the most common and costly mistakes.

## Shared responsibility

AWS secures the cloud itself: buildings, hardware, and the software that runs
its services. You secure what you put in the cloud: your data, who can access
it, your network rules, and the configuration of each service.[^shared-responsibility]
For example, AWS keeps an S3 storage service running, but you decide whether a
bucket is public.

## Quotas

Every account has limits, called quotas, such as how many virtual servers or IP
addresses you can create in a Region. Many can be raised on request through
Service Quotas.[^service-quotas] Check quotas before a launch or a load test,
because hitting one causes errors that look like outages.

## Where to go next

- [AWS networking](../networking/index.md) - VPCs, subnets, and routing.
- [AWS security](../security/index.md) - IAM and least privilege.
- [AWS FinOps](../finops/index.md) - budgets and cost alerts before you build.
- [Terraform on AWS](../../../cross-topic-guides/terraform-on-aws.md) - create resources from code.
- [Back to AWS fundamentals](index.md)

[^global-infrastructure]: [AWS global infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)
[^shared-responsibility]: [AWS shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/)
[^service-quotas]: [What is Service Quotas?](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)
[^get-caller-identity]: [aws sts get-caller-identity](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html)
