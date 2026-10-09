# Velero

Velero is a Kubernetes backup, restore, disaster recovery, and cluster migration tool. It stores Kubernetes API objects in object storage and can protect persistent volume data through provider snapshots, CSI snapshots, CSI snapshot data movement, or File System Backup.

## Reader path

| Need | Read |
| --- | --- |
| Learn the difference between backed-up Kubernetes objects and protected application data. | [Fundamentals](fundamentals.md) |
| Understand the moving parts, CRDs, controllers, and object storage sync. | [Components and architecture](components-and-architecture.md) |
| Find where object and volume copies live, then choose a restoreable data-protection path. | [Where a Velero backup keeps objects and volume data](storage-and-volume-backups.md) |
| Understand the S3, EBS snapshot, and AWS identity paths before an EKS installation. | [How Velero on EKS uses S3 and EBS](aws-s3-ebs-installation.md) |
| Back up one disposable ConfigMap and verify a namespace-mapped restore. | [Back up and restore one ConfigMap with Velero](backup-restore-workflows.md) |
| Understand how a protected workflow requests a Velero operation and where its permissions stop. | [How automation asks Velero to back up or restore](possible-integrations.md) |
| See what a second cluster can restore and what its team must prepare separately. | [How a Velero backup reaches another cluster](cluster-migration-and-disaster-recovery.md) |
| Choose which recovery and migration situations fit Velero and which need separate owners. | [Choose where Velero fits in a recovery plan](real-use-cases-and-runbooks.md) |
| Trace a restore with missing application data through its backup, volume path, target PVC, and workload check. | [Find why a Velero restore has no application data](troubleshooting-and-operations.md) |

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

[Back to migrations index](../index.md) | [Back to knowledge index](../../index.md)
