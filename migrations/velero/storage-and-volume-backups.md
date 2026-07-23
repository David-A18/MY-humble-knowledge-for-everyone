# Velero storage and volume backups

## Purpose

Use this page to choose how Velero should store backup artifacts and protect Kubernetes persistent volume data.

## Backup storage

Velero requires object storage for backup metadata, Kubernetes resource archives, restore logs, warnings, errors, and repository data used by File System Backup or data movement.

| Storage type | Use it for | Notes |
| --- | --- | --- |
| AWS S3 | Standard Velero backup storage on AWS. | Use the AWS plugin and least-privilege IAM. |
| S3-compatible object storage | On-premises or non-AWS object storage. | Test compatibility because S3-compatible providers differ in API behavior. |
| Provider-native object storage plugins | Azure, Google Cloud, and other providers. | Prefer the provider plugin when one is maintained and supported. |

> [!IMPORTANT]
> S3-compatible does not mean fully AWS S3 compatible. Validate upload, download, restore, lifecycle, encryption, retention, and repository maintenance before using a provider for production backups.

## Volume backup methods

| Method | How it works | Best fit | Trade-off |
| --- | --- | --- | --- |
| AWS EBS snapshots | AWS plugin creates EBS snapshots during backup and EBS volumes during restore. | EKS workloads using EBS in the same AWS region/provider boundary. | Fast and storage-native, but less portable across regions or providers. |
| CSI snapshots | Velero creates Kubernetes `VolumeSnapshot` resources through CSI snapshot APIs. | CSI-backed PVCs with a supported snapshot controller and driver. | Requires compatible CSI driver names and snapshot classes. |
| CSI snapshot data movement | Velero snapshots a CSI volume, then moves snapshot data into object storage. | More portable volume backups where snapshot data should leave the storage backend. | Requires node-agent and extra PVC/pod resources. |
| File System Backup | Node-agent reads mounted pod volumes and stores file data using Kopia. | Volumes without snapshot support, EFS/NFS-style storage, or cross-provider moves. | More portable but may be less point-in-time consistent and more resource intensive. |

## AWS S3 and EBS behavior

The Velero AWS plugin provides two important integrations:

- An object store plugin that writes Kubernetes backup artifacts to AWS S3.
- A volume snapshotter plugin that creates snapshots from EBS volumes during backup and creates volumes from those snapshots during restore.

For modern EKS clusters, CSI snapshot workflows also require:

- An EBS CSI driver with snapshot support.
- The CSI snapshot controller and snapshot CRDs.
- A `VolumeSnapshotClass` that matches the EBS CSI driver.

## CSI snapshot requirements

Kubernetes volume snapshots use three API objects:

| Object | Meaning |
| --- | --- |
| `VolumeSnapshot` | A user's request for a point-in-time snapshot of a PVC. |
| `VolumeSnapshotContent` | The bound snapshot object representing the real storage snapshot. |
| `VolumeSnapshotClass` | Snapshot behavior and driver settings, similar to `StorageClass` for volumes. |

### Check snapshot support

```bash
kubectl get volumesnapshotclass
kubectl get crd volumesnapshots.snapshot.storage.k8s.io
kubectl get pods -n kube-system | grep -E "snapshot|ebs-csi"
```

What it does: checks whether snapshot classes, snapshot CRDs, and likely EBS snapshot components are present.

## File System Backup with Kopia

File System Backup uses Velero node-agent to read mounted pod volumes from node filesystems and store file data in object storage through a backup repository. Velero v1.18 documents Kopia as the active path and notes that restic is in deprecation.

Use File System Backup when:

- The volume type does not support snapshots.
- You need to migrate volume contents across cloud providers.
- You use NFS, EFS, AzureFile, local volumes, or another volume type without provider snapshots.

Avoid relying only on File System Backup when:

- You need strict point-in-time consistency for a busy database.
- The volume contains very large files that are expensive to scan for deduplication.
- The node-agent cannot safely run with the required host filesystem access.

> [!WARNING]
> File System Backup reads live mounted file systems. For databases and write-heavy applications, use application quiesce hooks, database-native backup, or storage snapshots where consistency matters.

## Decision guide

| Situation | Prefer |
| --- | --- |
| Same EKS cluster or same-region EKS recovery with EBS PVCs | EBS or CSI snapshots. |
| Cross-cluster migration with the same CSI driver and storage backend | CSI snapshots, then test restore on the destination. |
| Cross-provider or cross-region volume migration | File System Backup or CSI snapshot data movement. |
| Stateless workloads only | Kubernetes object backup may be enough. |
| Database with strict recovery needs | Database-native backup plus Velero for manifests and surrounding resources. |

## Related links

- [Velero File System Backup](https://velero.io/docs/v1.18/file-system-backup/)
- [Velero CSI support](https://velero.io/docs/v1.18/csi/)
- [Kubernetes volume snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)
- [AWS S3 and EBS installation](aws-s3-ebs-installation.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
