# Velero fundamentals

## Purpose

Use this page to understand what Velero is, where it fits, and the limits to account for before using it for Kubernetes migration or recovery.

## What Velero is

Velero backs up Kubernetes cluster resources and persistent volume data so you can restore after accidental deletion, failed maintenance, cluster loss, or a planned migration. It can run in cloud or on-premises Kubernetes environments as long as it has a supported object storage backend and, when needed, a compatible volume backup method.

Velero has two main interfaces:

- A server running inside the cluster.
- A local `velero` CLI that creates Backup, Restore, and Schedule resources through the Kubernetes API.

## Main use cases

| Use case | How Velero helps | Watch for |
| --- | --- | --- |
| Disaster recovery | Restores resources and volume data from object storage and snapshots. | Recovery depends on backup location durability and tested restore steps. |
| Cluster migration | Uses shared object storage so a destination cluster can discover and restore source backups. | Kubernetes versions, CRDs, storage drivers, and cloud regions must be compatible. |
| Pre-change safety point | Takes a backup before upgrades, controller changes, or risky releases. | Not all live object changes are captured atomically. |
| Environment replication | Restores selected namespaces into dev, test, or staging. | Secrets, external endpoints, DNS, and credentials often need environment-specific changes. |

## What Velero backs up

Velero backs up Kubernetes API resources by querying the API server and storing serialized resource data in object storage. It can include or exclude namespaces, resources, labels, and individual objects.

For persistent volumes, Velero uses one of these methods:

| Method | Best for | Portability |
| --- | --- | --- |
| Cloud provider snapshots | Same-provider restores where the provider plugin supports block snapshots. | Usually provider and region constrained. |
| CSI snapshots | CSI-backed volumes where the destination has the same CSI driver name and compatible snapshot support. | Portable across clusters with matching storage driver behavior. |
| CSI snapshot data movement | Moving CSI snapshot data into backup storage for stronger portability. | Requires node-agent and extra data movement resources. |
| File System Backup | Volumes without snapshot support or cross-provider moves. | More portable, but less point-in-time consistent than snapshots. |

## What Velero does not solve

- It does not make application data automatically transaction-consistent.
- It does not replace database-native backup, replication, or point-in-time recovery.
- It does not migrate cloud-provider snapshots across all providers, regions, or storage systems.
- It does not guarantee that old Kubernetes API versions can be restored into newer or lower-version clusters.
- It does not protect backup data from bad retention, weak IAM, missing encryption, or untested runbooks.

> [!WARNING]
> Backups may include Kubernetes Secrets. Treat the backup bucket, repository credentials, logs, and restore workspaces as sensitive infrastructure.

## First commands to know

### Check the Velero version

```bash
velero version
```

What it does: shows the client and server versions so you can verify compatibility before creating or restoring backups.

### List backup storage locations

```bash
velero backup-location get
```

What it does: confirms whether Velero can reach the configured object storage location.

### List backups

```bash
velero backup get
```

What it does: shows backup names, status, errors, warnings, creation time, expiration, and storage location.

## Related links

- [Velero overview](https://velero.io/docs/v1.18/)
- [How Velero works](https://velero.io/docs/v1.18/how-velero-works/)
- [Storage and volume backups](storage-and-volume-backups.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
