# Velero components and architecture

## Purpose

Use this page to understand Velero's server, CLI, custom resources, controllers, plugins, and data movement components.

## Component map

| Component | Runs where | Role |
| --- | --- | --- |
| Velero CLI | Operator workstation or automation runner | Creates and inspects Backup, Restore, and Schedule resources. |
| Velero server | Kubernetes cluster | Runs controllers that process Velero custom resources. |
| Velero CRDs | Kubernetes API | Store Velero operations such as backups, restores, schedules, and locations. |
| Backup controller | Velero server | Collects Kubernetes resources and writes backup artifacts to object storage. |
| Restore controller | Velero server | Reads backup artifacts and recreates selected resources and volumes. |
| Plugins | Velero deployment init containers | Add provider-specific object store and volume snapshot behavior. |
| Node-agent | Kubernetes DaemonSet | Hosts file-system backup and data movement controllers on cluster nodes. |
| Data mover pods | Kubernetes workload pods | Move volume data between snapshots, PVCs, and backup repositories. |

## Important custom resources

| Resource | Meaning | Common check |
| --- | --- | --- |
| `Backup` | Requested or completed backup operation. | `velero backup describe <name> --details` |
| `Restore` | Requested or completed restore operation. | `velero restore describe <name> --details` |
| `Schedule` | Cron-style recurring backup definition. | `velero schedule get` |
| `BackupStorageLocation` | Object storage destination for backup metadata and artifacts. | `velero backup-location get` |
| `VolumeSnapshotLocation` | Provider-specific block snapshot location. | `velero snapshot-location get` |
| `BackupRepository` | Repository used by file-system backup or data movement. | `kubectl get backuprepositories -n velero` |
| `PodVolumeBackup` | File-system backup of a pod volume. | `kubectl get podvolumebackups -n velero` |
| `PodVolumeRestore` | File-system restore of a pod volume. | `kubectl get podvolumerestores -n velero` |
| `DataUpload` | Data movement upload operation. | `kubectl get datauploads -n velero` |
| `DataDownload` | Data movement download operation. | `kubectl get datadownloads -n velero` |

## Backup workflow

When you create a backup, the CLI creates a `Backup` object. The Velero server validates it, queries the Kubernetes API for selected resources, writes a backup archive to the configured `BackupStorageLocation`, and optionally triggers persistent volume protection.

### Create a namespace backup

```bash
velero backup create app-prod-$(date +%Y%m%d%H%M%S) --include-namespaces app-prod --wait
```

What it does: creates a backup for one namespace and waits until the operation reaches a terminal state.

> [!NOTE]
> Velero backups are not fully atomic. If resources are created or modified during backup, some object state may not match a single exact instant.

## Restore workflow

When you create a restore, the CLI creates a `Restore` object. The restore controller verifies the source backup, downloads backup content from object storage, filters and sorts resources, recreates Kubernetes objects, and restores persistent volume data according to the backup method used.

### Inspect restore details

```bash
velero restore describe <restore-name> --details
velero restore logs <restore-name>
```

What it does: shows the resources restored, warnings, errors, and log output needed for troubleshooting.

> [!WARNING]
> A restore can recreate or modify objects in live namespaces. Restore into a temporary namespace first when you are validating behavior or recovering a subset of data.

## Storage location architecture

Velero treats object storage as durable backup storage and as the source of truth for backup discovery. If a destination cluster points Velero to the same bucket and prefix, Velero can sync backup metadata from object storage and make those backups available for restore.

Provider snapshots are separate from the backup archive. For AWS, the backup metadata lives in S3, while EBS volume data may live in EBS snapshots unless File System Backup or CSI snapshot data movement copies data into object storage.

## Related links

- [How Velero works](https://velero.io/docs/v1.18/how-velero-works/)
- [Velero API types](https://velero.io/docs/v1.18/api-types/)
- [Backup and restore workflows](backup-restore-workflows.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
