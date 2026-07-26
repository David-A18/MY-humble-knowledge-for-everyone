# Velero storage and volume backups

## Purpose

Use this page to choose how Velero should store backup artifacts and protect Kubernetes persistent volume data.

## Contents

- [Backup storage](#backup-storage)
- [BackupStorageLocation example](#backupstoragelocation-example)
- [Volume backup methods](#volume-backup-methods)
- [Decision flow](#decision-flow)
- [AWS S3 and EBS behavior](#aws-s3-and-ebs-behavior)
- [CSI snapshot requirements](#csi-snapshot-requirements)
- [CSI snapshot data movement](#csi-snapshot-data-movement)
- [File System Backup with Kopia](#file-system-backup-with-kopia)
- [Resource policies for volume decisions](#resource-policies-for-volume-decisions)
- [Decision guide](#decision-guide)

## Backup storage

Velero requires object storage for backup metadata, Kubernetes resource archives, restore logs, warnings, errors, and repository data used by File System Backup or data movement.

| Storage type | Use it for | Notes |
| --- | --- | --- |
| AWS S3 | Standard Velero backup storage on AWS. | Use the AWS plugin and least-privilege IAM. |
| S3-compatible object storage | On-premises or non-AWS object storage. | Test compatibility because S3-compatible providers differ in API behavior. |
| Provider-native object storage plugins | Azure, Google Cloud, and other providers. | Prefer the provider plugin when one is maintained and supported. |

> [!IMPORTANT]
> S3-compatible does not mean fully AWS S3 compatible. Validate upload, download, restore, lifecycle, encryption, retention, and repository maintenance before using a provider for production backups.

## BackupStorageLocation example

```yaml
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: my-velero-backups
    prefix: clusters/prod-eks
  config:
    region: eu-west-1
  accessMode: ReadWrite
```

What it does: tells Velero where to write backup metadata, Kubernetes resource archives, logs, and repository data. The `prefix` keeps one cluster's backups separate from other clusters that may share the bucket.

> [!WARNING]
> Do not reuse one writable bucket prefix across unrelated clusters unless the ownership and retention model is intentional. Shared prefixes can make backup discovery, deletion, and disaster recovery confusing.

## Volume backup methods

| Method | How it works | Best fit | Trade-off |
| --- | --- | --- | --- |
| AWS EBS snapshots | AWS plugin creates EBS snapshots during backup and EBS volumes during restore. | EKS workloads using EBS in the same AWS region/provider boundary. | Fast and storage-native, but less portable across regions or providers. |
| CSI snapshots | Velero creates Kubernetes `VolumeSnapshot` resources through CSI snapshot APIs. | CSI-backed PVCs with a supported snapshot controller and driver. | Requires compatible CSI driver names and snapshot classes. |
| CSI snapshot data movement | Velero snapshots a CSI volume, then moves snapshot data into object storage. | More portable volume backups where snapshot data should leave the storage backend. | Requires node-agent and extra PVC/pod resources. |
| File System Backup | Node-agent reads mounted pod volumes and stores file data using Kopia. | Volumes without snapshot support, EFS/NFS-style storage, or cross-provider moves. | More portable but may be less point-in-time consistent and more resource intensive. |

## Decision flow

| Question | If yes | If no |
| --- | --- | --- |
| Is the workload stateless? | Back up Kubernetes resources or rely on GitOps/IaC. | Continue to data questions. |
| Is the data a database or transactional system? | Use database-native backup or replication, then Velero for Kubernetes objects. | Continue to volume method selection. |
| Is the restore in the same provider, account, region, and compatible storage backend? | Provider or CSI snapshots may be fastest. | Prefer File System Backup, CSI data movement, or application-level migration. |
| Does the CSI driver support snapshots and exist on source and destination? | CSI snapshots may work; test restore. | Use File System Backup or application-native migration. |
| Does the snapshot data need to leave the storage backend? | Use CSI snapshot data movement or File System Backup. | Native snapshots can be acceptable. |
| Is the volume an NFS/EFS/AzureFile-style file share? | File System Backup is usually the Velero path. | Use the storage driver's supported snapshot or backup method. |

> [!IMPORTANT]
> Choose a volume backup method per workload, not per cluster. A cluster may safely use snapshots for one application, File System Backup for another, and database-native replication for a third.

## AWS S3 and EBS behavior

The Velero AWS plugin provides two important integrations:

- An object store plugin that writes Kubernetes backup artifacts to AWS S3.
- A volume snapshotter plugin that creates snapshots from EBS volumes during backup and creates volumes from those snapshots during restore.

For modern EKS clusters, CSI snapshot workflows also require:

- An EBS CSI driver with snapshot support.
- The CSI snapshot controller and snapshot CRDs.
- A `VolumeSnapshotClass` that matches the EBS CSI driver.

## VolumeSnapshotLocation example

```yaml
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  config:
    region: eu-west-1
```

What it does: tells Velero where provider-native snapshots should be created for providers that use `VolumeSnapshotLocation`.

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

### EBS VolumeSnapshotClass example

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: ebs-csi-velero
  labels:
    velero.io/csi-volumesnapshot-class: "true"
driver: ebs.csi.aws.com
deletionPolicy: Delete
```

What it does: creates a Kubernetes snapshot class Velero can select for EBS CSI-backed PVCs. The driver must match the source PVC's CSI driver.

## CSI snapshot data movement

CSI snapshot data movement is useful when the CSI snapshot API can create a point-in-time source, but the data must be copied into Velero backup storage instead of staying only in the storage backend.

The object flow is:

1. Velero starts a backup for PVCs that use a compatible CSI driver.
2. The CSI plugin creates snapshot objects.
3. Velero creates `DataUpload` objects for volume data that should move to backup storage.
4. Node-agent and data mover pods copy data into a backup repository.
5. During restore, Velero creates `DataDownload` objects and data mover pods copy data back into restored volumes.

### Inspect data movement

```bash
kubectl get datauploads,datadownloads -n velero
kubectl describe dataupload <name> -n velero
kubectl describe datadownload <name> -n velero
```

What it does: shows upload and download lifecycle, node placement, data mover progress, and failure details.

> [!NOTE]
> Data movement improves portability but consumes extra object storage, node CPU, network bandwidth, temporary pods, and PVC staging resources. Test throughput before relying on it for large cutover windows.

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

### Opt-in File System Backup example

```bash
kubectl -n app-prod annotate pod/app-0 \
  backup.velero.io/backup-volumes=data

velero backup create app-prod-files \
  --include-namespaces app-prod \
  --snapshot-volumes=false \
  --wait
```

What it does: marks the `data` pod volume for File System Backup and creates a backup that avoids provider snapshots.

### Opt-out File System Backup example

```bash
velero backup create app-prod-all-pod-volumes \
  --include-namespaces app-prod \
  --default-volumes-to-fs-backup \
  --snapshot-volumes=false \
  --wait
```

What it does: tells Velero to use File System Backup for eligible pod volumes in the selected namespace without requiring per-pod annotations.

### Inspect backup repositories

```bash
kubectl get backuprepositories -n velero
kubectl describe backuprepository <repository-name> -n velero
```

What it does: shows Kopia repository readiness for namespaces that use File System Backup or data movement.

## Resource policies for volume decisions

Resource policies let one backup choose different volume actions by condition. Use them when a namespace mixes snapshot-friendly CSI volumes, NFS volumes, and volumes that should be skipped.

```yaml
version: v1
volumePolicies:
- conditions:
    csi:
      driver: ebs.csi.aws.com
  action:
    type: snapshot
- conditions:
    nfs: {}
  action:
    type: fs-backup
- conditions:
    volumeTypes:
    - emptyDir
    - configmap
    - secret
  action:
    type: skip
```

What it does: snapshots EBS CSI volumes, uses File System Backup for NFS volumes, and skips temporary or generated volume types.

```bash
kubectl create configmap app-prod-volume-policy \
  --from-file=resource-policies.yaml \
  -n velero

velero backup create app-prod-policy-backup \
  --include-namespaces app-prod \
  --resource-policies-configmap app-prod-volume-policy \
  --wait
```

What it does: stores the policy in the Velero namespace and references it from a backup.

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
- [Velero CSI snapshot data mover](https://velero.io/docs/v1.18/csi-snapshot-data-movement/)
- [Velero resource filtering](https://velero.io/docs/v1.18/resource-filtering/)
- [Kubernetes volume snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)
- [AWS S3 and EBS installation](aws-s3-ebs-installation.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
