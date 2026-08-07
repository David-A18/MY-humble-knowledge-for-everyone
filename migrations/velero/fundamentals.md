# Velero fundamentals

## Purpose

Use this page to understand what Velero is, where it fits, and the limits to account for before using it for Kubernetes migration or recovery.

## Contents

- [What Velero is](#what-velero-is)
- [How Velero works](#how-velero-works)
- [Core components](#core-components)
- [What must be installed and configured](#what-must-be-installed-and-configured)
- [Kubernetes resources versus application data](#kubernetes-resources-versus-application-data)
- [Volume backup paths](#volume-backup-paths)
- [What Velero does not solve](#what-velero-does-not-solve)
- [First commands to know](#first-commands-to-know)

## What Velero is

Velero is a Kubernetes backup, restore, disaster recovery, and migration tool. It captures Kubernetes API objects into backup storage and can also protect persistent volume data through storage snapshots or file-level backup.

Use Velero when you need to recover Kubernetes resources after accidental deletion, rebuild a cluster after failure, rehearse a restore, copy selected namespaces into another environment, or move workload resources during a planned cluster migration.

Do not treat Velero as a complete data migration platform by itself. It is very good at capturing Kubernetes desired objects and some volume data paths, but application-consistent state still depends on the application, database, storage system, and cutover process.

## How Velero works

Velero has two main interfaces:

- A server running inside the cluster, usually in the `velero` namespace.
- A local or automation-runner `velero` CLI that creates and inspects Velero custom resources through the Kubernetes API.

The common backup flow is:

1. An operator runs a `velero backup create` command or a `Schedule` triggers a backup.
2. The Velero CLI creates a `Backup` custom resource in the cluster.
3. The Velero server validates the request, queries the Kubernetes API, applies filters, and writes a backup archive to the configured `BackupStorageLocation`.
4. If volume protection is enabled, Velero also coordinates provider snapshots, CSI snapshots, CSI data movement, or File System Backup.
5. Velero stores logs, warnings, metadata, and backup status so another Velero instance can discover the backup from object storage.

The common restore flow is:

1. A destination cluster runs Velero with access to the same backup storage or a copied backup storage prefix.
2. Velero syncs backup metadata from object storage into the cluster.
3. An operator creates a `Restore` from a selected backup.
4. The restore controller recreates selected Kubernetes resources and restores volume data through the method used during backup.

> [!IMPORTANT]
> A Velero backup is not a single globally atomic transaction. Kubernetes resources and application data can change while a backup is running. For write-heavy state, coordinate quiescing, replication, or application-native backup before relying on the recovery point.

## Core components

| Component | What it is | Why it matters |
| --- | --- | --- |
| Velero CLI | Command-line client used by operators and automation. | Creates and inspects backups, schedules, restores, locations, and plugin behavior. |
| Velero server | Deployment inside the cluster. | Runs controllers that process backup and restore custom resources. |
| Velero CRDs | Kubernetes API types installed by Velero. | Represent `Backup`, `Restore`, `Schedule`, `BackupStorageLocation`, `VolumeSnapshotLocation`, repositories, and volume operations. |
| Provider plugins | Plugin containers loaded into Velero. | Add object storage and provider snapshot integrations for AWS, Azure, Google Cloud, and other platforms. |
| Object storage | Durable backup storage such as S3, Azure Blob, Google Cloud Storage, or S3-compatible storage. | Stores Kubernetes object archives, metadata, logs, warnings, and repository data. |
| Snapshot controller and CSI driver | Kubernetes storage components outside Velero. | Required for CSI volume snapshots and restore from CSI snapshots. |
| Node-agent | Velero DaemonSet on cluster nodes. | Performs File System Backup and built-in data movement work. |
| Backup repository | Repository used by node-agent and Kopia. | Stores file-system or moved volume data in object storage. |

## What must be installed and configured

| Requirement | Needed for | Checks |
| --- | --- | --- |
| Kubernetes cluster access | Installing Velero and creating backup/restore resources. | `kubectl auth can-i create backups.velero.io -n velero` |
| Velero CLI | Operator commands and automation. | `velero version` |
| Velero server and CRDs | Any backup or restore. | `kubectl get pods -n velero` and `kubectl get crd \| grep velero.io` |
| Backup storage location | All Velero backups. | `velero backup-location get` |
| Provider object store plugin | Writing to the selected backup storage. | `kubectl describe deployment velero -n velero` |
| Cloud IAM or storage credentials | Access to buckets, containers, prefixes, snapshots, and repositories. | Cloud IAM policy review plus `velero backup-location get` |
| Volume snapshot location | Provider-native snapshots. | `velero snapshot-location get` |
| CSI snapshot CRDs and controller | CSI snapshots and CSI data movement. | `kubectl get volumesnapshotclass` |
| Node-agent | File System Backup and Velero data mover. | `kubectl get daemonset node-agent -n velero` |
| Matching StorageClasses on restore target | PVC recreation and data restore. | `kubectl get storageclass` |
| Application restore plan | Stateful workload correctness. | Owner sign-off, test restore, and data validation |

### Check basic health

```bash
velero version
velero backup-location get
velero snapshot-location get
kubectl get pods -n velero
```

What it does: confirms the CLI can talk to the server, the server can reach backup storage, snapshot locations are registered when used, and Velero pods are running.

### Inspect the Velero API objects

```bash
kubectl get backups,restores,schedules,backupstoragelocations,volumesnapshotlocations -n velero
```

What it does: reads Velero custom resources directly from Kubernetes so you can see requested and completed operations even when the CLI output is not enough.

## Main use cases

| Use case | How Velero helps | Watch for |
| --- | --- | --- |
| Disaster recovery | Restores resources and volume data from object storage and snapshots. | Recovery depends on backup location durability and tested restore steps. |
| Cluster migration | Uses shared object storage so a destination cluster can discover and restore source backups. | Kubernetes versions, CRDs, storage drivers, and cloud regions must be compatible. |
| Pre-change safety point | Takes a backup before upgrades, controller changes, or risky releases. | Not all live object changes are captured atomically. |
| Environment replication | Restores selected namespaces into dev, test, or staging. | Secrets, external endpoints, DNS, and credentials often need environment-specific changes. |

## Kubernetes resources versus application data

Velero backs up Kubernetes API resources by querying the API server and storing serialized resource data in object storage. It can include or exclude namespaces, resources, labels, and individual objects.

This means Velero can capture objects such as:

- Namespaces.
- Deployments, StatefulSets, DaemonSets, Jobs, CronJobs, Services, Ingresses, ConfigMaps, Secrets, ServiceAccounts, Roles, RoleBindings, PVCs, and custom resources.
- Cluster-scoped resources when the backup includes them, such as CRDs, ClusterRoles, ClusterRoleBindings, StorageClasses, and selected webhook or policy resources.

Velero resource backup is not the same as application-consistent data migration:

| Layer | Velero role | Application owner role |
| --- | --- | --- |
| Kubernetes desired state | Back up and restore API objects. | Ensure manifests are current in GitOps or IaC. |
| PVC file contents | Back up through snapshots, data movement, or File System Backup. | Validate mounted data after restore. |
| Databases | Capture Kubernetes wrapper resources and possibly volume contents. | Use native replication, logical dump, physical backup, PITR, or vendor-supported migration. |
| Queues and streams | Capture Kubernetes resources if self-hosted. | Plan broker-native replication, export/import, offset handling, and producer/consumer cutover. |
| External managed services | Usually only captures Secrets or references. | Migrate service data, endpoints, identities, and client configuration. |

> [!WARNING]
> Backing up a StatefulSet and PVC does not prove the database inside it is transaction-consistent. For databases, use database-native backup or replication as the primary data protection mechanism and use Velero for Kubernetes objects around it.

## Volume backup paths

For persistent volumes, Velero uses one of these methods:

| Method | How it works | Best for | Explicit limitation |
| --- | --- | --- | --- |
| Provider snapshots | A Velero provider plugin calls cloud snapshot APIs, such as EBS snapshots, Azure Managed Disk snapshots, or Google Persistent Disk snapshots. | Same-provider recovery with compatible accounts, regions, drivers, and permissions. | Snapshots are storage-provider objects, not portable Kubernetes backup files. |
| CSI snapshots | Velero creates Kubernetes `VolumeSnapshot` objects and the CSI snapshot controller asks the CSI driver to snapshot the backend volume. | CSI-backed PVCs where source and destination support compatible `VolumeSnapshotClass` and driver names. | The backup contains snapshot metadata; the data remains in the storage backend unless data movement is used. |
| CSI snapshot data movement | Velero snapshots a CSI volume and moves snapshot contents into an object-storage-backed repository. | More portable PVC data movement while still using CSI snapshot semantics. | Requires node-agent, extra restore staging resources, and careful performance testing. |
| File System Backup | Node-agent reads files from mounted pod volumes and stores them with Kopia in object storage. | Volumes without snapshot support, NFS/EFS/AzureFile-style storage, or cross-provider PVC file data migration. | Reads live file systems and can be slower or less consistent for active write-heavy data. |

### Create a resource-only namespace backup

```bash
velero backup create app-prod-resources \
  --include-namespaces app-prod \
  --snapshot-volumes=false \
  --wait
```

What it does: backs up Kubernetes resources in `app-prod` and intentionally skips volume snapshots. Use this when GitOps or another process owns application data migration, or when you want to test resource restore without moving PVC data.

### Create a namespace backup with volume snapshots when configured

```bash
velero backup create app-prod-with-volumes \
  --include-namespaces app-prod \
  --snapshot-volumes=true \
  --wait
```

What it does: backs up Kubernetes resources and asks Velero to snapshot eligible persistent volumes using the configured provider or CSI snapshot path.

### Opt one pod volume into File System Backup

```bash
kubectl -n app-prod annotate pod/app-0 \
  backup.velero.io/backup-volumes=data

velero backup create app-prod-fsb \
  --include-namespaces app-prod \
  --wait
```

What it does: marks the `data` volume on pod `app-0` for File System Backup, then creates a namespace backup. In production, put this annotation on the pod template managed by the workload controller so it survives pod replacement.

### Verify which volume path was used

```bash
velero backup describe app-prod-fsb --details
kubectl get podvolumebackups,datauploads -n velero
```

What it does: shows whether Velero used snapshots, File System Backup, or data movement for protected volumes and lists the volume operation custom resources.

## What Velero does not solve

- It does not make application data automatically transaction-consistent.
- It does not replace database-native backup, replication, or point-in-time recovery.
- It does not migrate cloud-provider snapshots across all providers, regions, or storage systems.
- It does not guarantee that old Kubernetes API versions can be restored into newer or lower-version clusters.
- It does not install missing CRDs, operators, admission controllers, CSI drivers, ingress controllers, or cloud identities on the destination unless those resources are in scope and restore-compatible.
- It does not rewrite application configuration for new DNS names, cloud services, storage classes, identities, or container registries without explicit restore rules or follow-up changes.
- It does not validate application behavior after restore.
- It does not protect backup data from bad retention, weak IAM, missing encryption, or untested runbooks.

> [!WARNING]
> Backups may include Kubernetes Secrets. Treat the backup bucket, repository credentials, logs, and restore workspaces as sensitive infrastructure.

## Capability and limitation checklist

| Capability | Practical expectation |
| --- | --- |
| Namespace restore | Works well when target dependencies, CRDs, storage classes, secrets, and admission policies are compatible. |
| Cluster rebuild | Useful when Velero backup storage survives the cluster and the destination can read it. |
| Cross-cluster migration | Requires version, API, storage, network, identity, and ingress compatibility work. |
| Cross-cloud migration | Usually needs File System Backup, CSI data movement, or application-native data migration because provider snapshots are not portable across clouds. |
| GitOps-managed workloads | Git should redeploy desired state; Velero can recover generated objects, PVC data, and resources not cleanly represented in Git. |
| Stateful systems | Velero helps with Kubernetes wrappers and volume recovery, but application-native mechanisms should own correctness. |
| Secrets | Velero can back them up, but restore may need rotation, environment-specific values, or external secret reconciliation. |
| CRDs and operators | CRDs should usually exist before custom resources are restored. Operators should be installed in a controlled order. |

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

### Inspect backup warnings and errors

```bash
velero backup describe <backup-name> --details
velero backup logs <backup-name>
```

What it does: shows skipped resources, volume backup details, warnings, and errors that decide whether a backup is usable.

## Related links

- [Velero overview](https://velero.io/docs/v1.18/)
- [How Velero works](https://velero.io/docs/v1.18/how-velero-works/)
- [Velero CSI support](https://velero.io/docs/v1.18/csi/)
- [Velero File System Backup](https://velero.io/docs/v1.18/file-system-backup/)
- [Storage and volume backups](storage-and-volume-backups.md)
- [Components and architecture](components-and-architecture.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
