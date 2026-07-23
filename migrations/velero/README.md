# Velero

Velero is a Kubernetes backup, restore, disaster recovery, and cluster migration tool. It stores Kubernetes API objects in object storage and can protect persistent volume data through provider snapshots, CSI snapshots, CSI snapshot data movement, or File System Backup.

## Reader path

| Need | Read |
| --- | --- |
| Learn what Velero does and does not do. | [Fundamentals](fundamentals.md) |
| Understand the moving parts and CRDs. | [Components and architecture](components-and-architecture.md) |
| Choose a persistent volume backup method. | [Storage and volume backups](storage-and-volume-backups.md) |
| Install on EKS with S3 and EBS snapshots. | [AWS S3 and EBS installation](aws-s3-ebs-installation.md) |
| Run backups, schedules, restores, and namespace moves. | [Backup and restore workflows](backup-restore-workflows.md) |
| Plan migration or disaster recovery. | [Cluster migration and disaster recovery](cluster-migration-and-disaster-recovery.md) |
| Map Velero to real operating scenarios. | [Real use cases and runbooks](real-use-cases-and-runbooks.md) |
| Investigate failures and operate Velero safely. | [Troubleshooting and operations](troubleshooting-and-operations.md) |

## What Velero protects

| Layer | How Velero handles it | Notes |
| --- | --- | --- |
| Kubernetes objects | Backs up resource definitions into object storage. | Includes objects returned by the Kubernetes API after filters are applied. |
| Persistent volumes | Uses snapshots or file-system backup depending on configuration. | The best method depends on storage driver, provider, consistency needs, and portability. |
| Schedules | Creates backups from cron expressions. | Use schedules for recurring recovery points. |
| Restores | Recreates resources and volume data from a backup. | Test restores before trusting the backup strategy. |

> [!IMPORTANT]
> Velero is not a substitute for application-aware replication, database backup tooling, or a tested disaster recovery plan. Use it as one part of a recovery design and verify every important restore path.

## Official documentation

- [Velero v1.18 overview](https://velero.io/docs/v1.18/)
- [How Velero works](https://velero.io/docs/v1.18/how-velero-works/)
- [Velero cluster migration](https://velero.io/docs/v1.18/migration-case/)
- [Velero File System Backup](https://velero.io/docs/v1.18/file-system-backup/)
- [Velero AWS plugin](https://github.com/velero-io/velero-plugin-for-aws)
- [Kubernetes volume snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)
- [Amazon EKS CSI snapshot controller](https://docs.aws.amazon.com/eks/latest/userguide/csi-snapshot-controller.html)

[Back to migrations index](../README.md) | [Back to root index](../../README.md)
