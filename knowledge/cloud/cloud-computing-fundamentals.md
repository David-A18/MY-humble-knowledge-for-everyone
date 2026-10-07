---
type: Explanation
title: Cloud computing fundamentals
description: Understand what cloud computing provides, what you still control, and why scaling, reliability, and metered cost need deliberate choices.
tags: [cloud, fundamentals, beginner, shared-responsibility]
status: draft
maturity: draft
audience: Curious learners and beginning engineers
maintainer: unassigned
sources:
  - id: nist-cloud-definition
    resource: https://csrc.nist.gov/pubs/sp/800/145/final
    title: NIST SP 800-145 - The NIST Definition of Cloud Computing
  - id: azure-shared-responsibility
    resource: https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility
    title: Microsoft Learn - Shared responsibility in the cloud
  - id: azure-reliability-responsibility
    resource: https://learn.microsoft.com/en-us/azure/reliability/concept-shared-responsibility
    title: Microsoft Learn - Shared responsibility for reliability
  - id: azure-regions-zones
    resource: https://learn.microsoft.com/en-us/azure/well-architected/design-guides/regions-availability-zones
    title: Microsoft Learn - Regions and availability zones
  - id: aws-autoscaling-groups
    resource: https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html
    title: Amazon EC2 Auto Scaling - Auto Scaling groups
  - id: aws-ec2-on-demand
    resource: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html
    title: Amazon EC2 - Purchasing On-Demand Instances
---

# Cloud computing fundamentals

## Purpose

Read this before choosing a public cloud provider or service. You should leave
able to explain what cloud computing supplies, which decisions remain yours, and why
"automatic scaling," "high availability," and "pay for what you use" need
closer questions.

This is a public cloud starting model, not a setup guide. NIST also describes
private and community clouds, where an organization can operate its own cloud
infrastructure.[^nist-cloud-definition] The example below is invented;
no cloud account, bill, or failure test was used to validate it.

## What cloud computing is

Cloud computing lets you request computing resources over a network without
installing each physical machine yourself. Resources can include servers,
storage, databases, and applications. In a public cloud, a provider operates
the shared infrastructure. NIST's five defining characteristics mean you can
request resources yourself, reach them over a network, draw from a shared
pool, change capacity relatively quickly, and measure use. They do not mean
every change is instant or automatic.[^nist-cloud-definition]

Think of **the cloud** as a way to obtain and operate resources, not a
different place where the usual questions about access, data, reliability,
and cost disappear.

## Why the model matters

Cloud services let a team start without buying hardware or guessing all its
future capacity in advance. The trade-off is that the team still has to make
the right service and configuration choices. Mistaking a provider feature
for a protection already in place can expose data, leave a single point of
failure, or produce a bill nobody expected.

## The mental model: who does what

The provider runs physical facilities and offers services. You decide what
to put in those services, who can reach it, and which protective features to
use. The exact split depends on the service. A **virtual machine** is a
software-defined computer whose operating system you manage. An application
**runtime** is the environment that runs your code; a managed runtime removes
some operating-system work. A ready-made software service removes more
application work. Your **workload** is the application and data you put on
the platform. Your data, identities, and configuration still need your
attention.[^azure-shared-responsibility]

| If you choose... | The provider generally operates... | You still decide... |
| --- | --- | --- |
| Infrastructure as a service (IaaS), such as a virtual machine | Facilities, physical network and hosts, and the software that makes virtual machines possible | Operating system, application, data, access, and configuration |
| Platform as a service (PaaS), such as a managed app runtime | IaaS layers plus operating system and runtime | Application behavior, data, access, and configuration |
| Software as a service (SaaS), such as a hosted application | PaaS layers plus the application service | Your data, users, permissions, and available settings |

These are broad service models, not a contract for every product. Read the
particular provider's responsibility guide before relying on its defaults.

## An analogy: renting a workshop

Imagine renting a workshop instead of building one. The owner maintains the
building and utilities. You choose the equipment, decide who has keys, and
protect the work stored inside. As with a rented workshop, an idle resource
can still cost money, and the owner does not automatically make a second copy
of your work.

The analogy helps separate the provider's infrastructure from your workload.
It breaks down in two useful ways:

- You do not normally add a workshop room through an API. Cloud capacity can
  be requested through software, sometimes by rules the service already
  offers and sometimes by rules you must configure.
- A workshop has a fixed floor plan and lease. Cloud resources can share
  physical hosts with other customers and be metered in different units.
  This shared-customer detail describes public cloud, not every deployment
  model.

## Four useful words with limits

- **Elasticity** means capacity can grow or shrink. Scaling behavior and
  limits depend on the service; some services scale without a policy you
  write. For example, an EC2 Auto Scaling group has minimum, desired, and
  maximum capacities; a scaling policy changes the desired number within
  those limits.[^aws-autoscaling-groups] More copies also require an
  application that can handle them.
- **Region** means a provider's geographic area. Azure, for example,
  describes an **availability zone** as a separate datacenter group within
  a region, with its own power, cooling, and network. Not every region or
  service supports the same zone options. Selecting one region alone is not
  a recovery plan.[^azure-regions-zones]
- **Reliability** means a workload can keep working or recover as expected.
  You achieve it by designing for failures. The provider makes
  platform capabilities available, while you choose the workload's
  architecture, backup, monitoring, and recovery settings. A single copy of
  an application or data store can still fail.[^azure-reliability-responsibility]
- **Measured cost** means use can be tracked in units.[^nist-cloud-definition]
  It does not mean a running resource is free while nobody visits your site.
  For example, an Amazon EC2 On-Demand instance incurs compute charges while
  it is running, including idle time.[^aws-ec2-on-demand]

## Visual: the invented photo site

```mermaid
flowchart TD
    visitor[Visitor's browser] --> endpoint[Public address for the photo site]
    endpoint --> app[Application copies in a chosen region]
    app --> data[Photo storage]
    owner[Your team: code, access, scaling, recovery choices] -. configures .-> endpoint
    owner -. configures .-> app
    owner -. configures .-> data
    provider[Provider: facilities and service platform] -. supports .-> platform[Underlying cloud services]
    platform -. supports .-> app
    platform -. supports .-> data
```

**Text alternative:** A visitor reaches the photo site's public address,
which sends the request to application copies. Those copies read or write
photo storage. The provider operates the facilities and platform beneath
those services. Your team configures the application, access rules, scaling,
and data protection. Use the diagram to identify which settings your team
must decide before launch. The exact network path and ownership details vary
by service.

## Example: a small photo-sharing site

Suppose an invented community site has quiet weekdays and a busy weekend
event. Its team follows this sequence:

1. **Start:** Choose a region, a service for running the application, and
   storage for photos. Keep photos outside short-lived application copies;
   decide who may write to storage.
2. **Prepare:** Check how this chosen service scales, set a limit for the
   expected event, and confirm that several application copies can safely
   serve the same users. Decide whether a zone failure needs a redundant
   deployment and a tested recovery path.
3. **During the event:** Watch requests, errors, and running capacity. If
   the configured limit is reached, more visitor traffic does not create
   unlimited capacity.
4. **After the event:** Reduce unneeded running capacity and inspect the
   charges. The end state is an available site with its photos still stored
   and a known bill, not an assumption that idle resources are free.

This example shows choices, not a promise that every cloud service has those
features or that cloud hosting is always cheaper.

## Check your understanding

1. If the provider maintains a physical server, who decides who may read
   your application's data?
2. What must be true before a traffic spike can add useful application
   copies?
3. Why can an application in one region still need a recovery plan?
4. Why might an idle virtual machine appear on the bill?

If you can answer those, compare a specific provider's service model with
this page before adopting its defaults.

## Next steps

- Use the [cloud topic map](index.md) to choose AWS, Azure, Google Cloud, or
  provider-neutral solutions.
- Read [Cost allocation basics](../finops/cost-allocation-basics.md) when a
  team needs to decide who owns cloud spending.
- Read [Stateful vs. stateless on AWS](aws/architecture/stateful-vs-stateless.md)
  to see why adding application copies does not solve data placement.

## Official documentation for deeper study

- [NIST SP 800-145](https://csrc.nist.gov/pubs/sp/800/145/final) defines
  cloud computing and its service models.
- [Microsoft's shared responsibility guide](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)
  shows how customer and provider work changes across IaaS, PaaS, and SaaS.
- [Microsoft's reliability responsibility guide](https://learn.microsoft.com/en-us/azure/reliability/concept-shared-responsibility)
  explains why workload reliability still needs customer decisions.
- [Microsoft's regions and zones guide](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/regions-availability-zones)
  explains Azure's zone boundaries and deployment choices.
- [Amazon EC2 Auto Scaling groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html)
  shows what a configured scaling group can control.
- [Amazon EC2 On-Demand instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html)
  illustrates that running idle compute can still be billed.

## Related links

- [Cloud index](index.md)
- [Start here](../start-here.md)
- [Root knowledge index](../index.md)

[^nist-cloud-definition]: [NIST SP 800-145](https://csrc.nist.gov/pubs/sp/800/145/final), source record `nist-cloud-definition`.
[^azure-shared-responsibility]: [Microsoft Learn - Shared responsibility in the cloud](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility), source record `azure-shared-responsibility`.
[^azure-reliability-responsibility]: [Microsoft Learn - Shared responsibility for reliability](https://learn.microsoft.com/en-us/azure/reliability/concept-shared-responsibility), source record `azure-reliability-responsibility`.
[^azure-regions-zones]: [Microsoft Learn - Regions and availability zones](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/regions-availability-zones), source record `azure-regions-zones`.
[^aws-autoscaling-groups]: [Amazon EC2 Auto Scaling - Auto Scaling groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html), source record `aws-autoscaling-groups`.
[^aws-ec2-on-demand]: [Amazon EC2 - Purchasing On-Demand Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html), source record `aws-ec2-on-demand`.
