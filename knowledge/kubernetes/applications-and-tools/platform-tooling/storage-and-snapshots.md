---
type: Explanation
title: Kubernetes storage and snapshots
description: Distinguish application storage, secret delivery, snapshots, and recoverable
  backups.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: persistent-volumes
  resource: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
  title: Persistent volumes
- id: volume-snapshots
  resource: https://kubernetes.io/docs/concepts/storage/volume-snapshots/
  title: Volume snapshots
- id: ebs-csi
  resource: https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html
  title: EBS CSI
---

# Kubernetes storage and snapshots

## Purpose

Distinguish application storage, secret delivery, snapshots, and recoverable backups.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Responsibilities

A PersistentVolumeClaim requests capacity and access semantics through a StorageClass. A CSI controller provisions storage; a node plugin attaches or mounts it. Snapshot APIs coordinate driver-supported point-in-time copies.[^persistent-volumes][^volume-snapshots][^ebs-csi]

| Need | Common choices | Main criteria |
| --- | --- | --- |
| EKS block storage | EBS CSI Driver | Zone affinity, attachment limits, access mode, performance. |
| EKS shared files | EFS CSI Driver | Filesystem semantics, access points, throughput, cost. |
| Distributed storage | Rook/Ceph, Longhorn | Replication, repair, storage-node operations, failure domains. |
| Object storage | S3 or compatible service | SDK access rather than normal POSIX disk semantics. |
| Secret files | Secrets Store CSI Driver | Identity and rotation rather than data persistence. |
| Recovery | Velero and appropriate volume protection | Metadata, data consistency, off-cluster copies, tested restore. |

## Inspect before changing

```bash
kubectl get storageclass
kubectl get pvc,pv -A
kubectl get volumesnapshotclass
kubectl get volumesnapshot -A
```

What it does: inventories provisioners, claims, bindings, and snapshot APIs. Missing CRDs/classes differ from a driver failing to create a snapshot.

## Failure modes

Pending claims can mean no default class, topology restrictions, quota, or a valid `WaitForFirstConsumer` wait for scheduling. Mount failures can involve IAM, filesystem permissions, node limits, or zone placement. Inspect events and CSI controller/node logs before deleting claims.

Snapshots may be crash-consistent. Coordinate database flushing or database-native recovery where required. Copies in the same failure domain may not meet disaster-recovery requirements.

> [!WARNING]
> PVC deletion can delete the underlying volume according to reclaim policy. Validate restoration through application reads/writes and measured RPO/RTO.

## Related links

- [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Volume snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)
- [EBS CSI](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html)
- [Velero volume protection](../../../migrations/velero/storage-and-volume-backups.md)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^persistent-volumes]: [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).
[^volume-snapshots]: [Volume snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/).
[^ebs-csi]: [EBS CSI](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html).
