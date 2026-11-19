---
type: Explanation
title: Choosing S3, EBS, or EFS
description: Pick the right AWS storage service by comparing object storage (S3), block volumes (EBS), and shared file systems (EFS), and plan lifecycle and backups.
tags: [aws, storage, s3, ebs, efs]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: s3-lifecycle
    resource: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
    title: Managing the lifecycle of objects in Amazon S3
  - id: ebs-volumes
    resource: https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html
    title: Amazon EBS volumes
  - id: efs-intro
    resource: https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html
    title: What is Amazon EFS?
  - id: instance-store
    resource: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-lifetime.html
    title: Instance store data persistence
---

# Choosing S3, EBS, or EFS

AWS has three main ways to store data, and they behave very differently. **S3**
stores whole files as objects that any application can fetch over the network.
**EBS** is a virtual hard disk attached to one server. **EFS** is a shared
network folder that many servers can use at the same time. Picking the right
one depends on who reads the data and how.

## Compare the three

| | Amazon S3 | Amazon EBS | Amazon EFS |
| --- | --- | --- | --- |
| What it is | Object storage, reached over HTTPS | Block volume, like a disk | Shared file system (NFS) |
| Who can use it | Any application with permission | Usually one EC2 instance at a time, in one AZ | Many instances and containers at once |
| Typical uses | Backups, logs, static websites, data lakes, file uploads | Operating system disks, databases on EC2 | Shared content, home directories, container volumes |
| Scope | One Region | One Availability Zone | One Region, across AZs |

A Kubernetes volume backed by EBS, for example, can attach to only one node
in the same AZ, while an EFS volume can be shared by Pods on many nodes.[^ebs-volumes][^efs-intro]

> [!WARNING]
> Some EC2 instance types also have **instance store** disks. Their data is lost
> when the instance stops or fails, so never keep data you need only there.[^instance-store]

## Plan the lifecycle

Data you keep forever keeps costing money. Decide up front how long each kind
of data must be kept:

- **S3 lifecycle rules** move older objects to cheaper storage classes and
  delete them when they expire.[^s3-lifecycle]
- **EBS snapshots** are point-in-time backups of a volume. Delete snapshots
  you no longer need, because they are billed too.
- **EFS lifecycle management** moves files that are rarely read to a cheaper
  storage class.

## Back up and test restores

A backup you have never restored is a guess. Keep backups in a separate account
or Region for important data, and practice restoring them. For Kubernetes
workloads, see [Velero storage and volume backups](../../../migrations/velero/storage-and-volume-backups.md).

## Related links

- [Velero AWS S3 and EBS installation](../../../migrations/velero/aws-s3-ebs-installation.md)
- [AWS storage and network costs](../finops/storage-and-network-costs.md)
- [Back to AWS storage](index.md)

[^s3-lifecycle]: [Managing the lifecycle of objects in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
[^ebs-volumes]: [Amazon EBS volumes](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html)
[^efs-intro]: [What is Amazon EFS?](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html)
[^instance-store]: [Instance store data persistence](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-lifetime.html)
