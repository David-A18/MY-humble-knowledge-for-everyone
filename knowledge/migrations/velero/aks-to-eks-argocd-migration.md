---
type: How-to Guide
title: Migrate Argo CD-managed workloads from Azure AKS to AWS EKS
description: Plan a cross-cloud move from AKS to EKS where disk snapshots are not portable, using Argo CD, Velero file-level backups, and application-native data tools.
tags: [migrations, velero, argo-cd, aks, eks, runbook]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Migrate Argo CD-managed workloads from Azure AKS to AWS EKS

This runbook moves Argo CD-managed applications from Azure Kubernetes Service to Amazon EKS. It is part of [Velero real use cases and runbooks](real-use-cases-and-runbooks.md).

## Runbook: migrate Argo CD-managed workloads from Azure AKS to AWS EKS

Use this scenario for a cross-cloud migration where the source cluster is AKS, the destination cluster is EKS, and applications are managed by Argo CD. The critical rule is that cloud-native volume snapshots are not portable between Azure Managed Disks and Amazon EBS. Velero can help with Kubernetes resources and selected file-level PVC data, but it does not turn Azure snapshots into EBS volumes.

### Cross-cloud requirements

| Area | Requirement |
| --- | --- |
| Source AKS | Healthy API access, Velero installed, Azure plugin or reachable backup storage, node-agent for File System Backup when used. |
| Destination EKS | Compatible Kubernetes version, Velero installed, AWS plugin for S3/EBS where needed, node-agent when restoring file backups or moved data. |
| Object storage | A backup location readable by the destination Velero instance, or a tested copy process that preserves Velero backup layout and repository data. |
| Identity | Azure credentials for source backup storage and AWS IAM for S3, EBS, EKS, and workload identities. |
| Network and DNS | Connectivity to backup storage, container registries, external services, databases, DNS zones, and ingress endpoints. |
| Secrets | External secret stores, sealed secrets, or manual rotation path ready for EKS. |
| Storage | EKS StorageClasses, EBS CSI driver, snapshot controller when using AWS snapshots after migration, and any class-name mapping plan. |
| CRDs and operators | Target versions installed before custom resources are restored or reconciled. |
| Argo CD | Applications updated to point to the EKS cluster, with cloud-specific overlays reviewed. |

### Data-type decision guide

| Data type | Recommended migration method | Why |
| --- | --- | --- |
| PostgreSQL, MySQL, MongoDB, Redis with persistence, or similar databases | Native replication, managed migration service, logical dump/restore, physical backup/restore, or PITR. | Database engines understand transactions, logs, consistency, indexes, and promotion. |
| Generic PVC file data such as uploads or shared documents | Velero File System Backup or CSI snapshot data movement after a rehearsal restore. | File-level data can move across clouds when consistency and restore time are acceptable. |
| Azure Managed Disk snapshots | Do not use directly for EKS/EBS restore. | Snapshot handles and backing storage are Azure-specific. |
| Object storage data | Cloud-native copy, replication, or application-level reconfiguration from Azure Blob to S3. | Kubernetes backup tools do not migrate arbitrary object buckets. |
| Queues and streams | Broker-native replication, mirror, export/import, or controlled drain and replay. | Consumer offsets, ordering, retention, and producer cutover are application concerns. |
| Search indexes and caches | Rebuild from source of truth when possible; otherwise use product-native snapshot/restore. | Many indexes and caches are derived data and should not block cluster migration if rebuild is tested. |
| Stateless services | Reconcile from Git with EKS-specific overlays. | Argo CD should own desired state. |

> [!WARNING]
> Azure volume snapshots are not portable to AWS EBS. If the application data lives only on AKS disks, plan database-native migration, Velero File System Backup, Velero data movement, or another file/block migration method that has been restored successfully on EKS.

### Prepare source and destination

On AKS:

```bash
velero version
velero backup-location get
kubectl get pvc,pv -A
kubectl get volumesnapshotclass
kubectl get applications.argoproj.io -A
```

What it does: checks Velero health, storage, persistent volumes, snapshot capability, and GitOps-managed workloads on the source.

On EKS:

```bash
kubectl get nodes
kubectl get storageclass
kubectl get volumesnapshotclass
velero backup-location get
kubectl get daemonset node-agent -n velero
```

What it does: confirms the destination cluster is ready to provision volumes, use snapshots when appropriate, reach backup storage, and run node-agent volume restore work.

### Back up AKS resources without relying on Azure disk snapshots

```bash
velero backup create aks-apps-resource-final \
  --include-namespaces team-a,team-b \
  --snapshot-volumes=false \
  --wait
```

What it does: captures Kubernetes resources while intentionally avoiding Azure disk snapshots for the cross-cloud path.

For portable PVC file data:

```bash
velero backup create aks-apps-filedata-final \
  --include-namespaces team-a,team-b \
  --default-volumes-to-fs-backup \
  --snapshot-volumes=false \
  --wait
```

What it does: captures selected mounted pod volume contents into object-storage-backed repositories instead of Azure Managed Disk snapshots.

### Make backups visible to EKS

Choose one backup storage pattern and test it before cutover:

| Pattern | When to use it | Caveat |
| --- | --- | --- |
| EKS Velero reads the original Azure Blob backup location | Network, credentials, and Azure plugin are acceptable on EKS. | EKS must run the needed plugin and identity path to read the source object store. |
| Copy Velero backup objects and repositories to S3 | You want EKS-native backup storage after migration. | Preserve object layout, prefixes, metadata, and repository data; test restore before trusting the copy. |
| Use an S3-compatible location reachable from both clusters | Both clusters can safely access the same durable store. | Validate compatibility, encryption, retention, and IAM separation. |

After configuring the destination backup location:

```bash
velero backup-location get
velero backup get
velero backup describe aks-apps-filedata-final --details
```

What it does: verifies EKS Velero can read the backup location, has synced backup metadata, and can inspect the selected backup.

### Test restore on EKS

```bash
velero restore create aks-to-eks-rehearsal \
  --from-backup aks-apps-filedata-final \
  --namespace-mappings team-a:team-a-rehearsal \
  --wait

velero restore describe aks-to-eks-rehearsal --details
velero restore logs aks-to-eks-rehearsal
```

What it does: restores one namespace into a rehearsal namespace on EKS and exposes warnings, skipped resources, PVC issues, and volume restore errors.

Validate before final migration:

- CRDs and operators are installed on EKS before custom resources reconcile.
- StorageClass names either match or are transformed deliberately.
- PVCs bind to EBS, EFS, or another target storage backend as designed.
- Ingress objects are compatible with the EKS ingress controller or Gateway API implementation.
- External DNS and certificate controllers do not update production DNS during rehearsal.
- Workload identities use AWS IAM paths, not AKS managed identity assumptions.
- Secrets come from the target secret system or are rotated.
- Argo CD health is green without fighting Velero-restored state.
- Database, queue, object storage, and cache validations use their own owner-approved checks.

### Final migration and cutover

Use the rehearsal result to decide whether Velero restores resources, Argo CD recreates resources, or both are used with strict boundaries. For most Argo CD estates, the final sequence should be:

1. Freeze Git changes or pin revisions for applications in scope.
2. Prepare final database, queue, object storage, and cache synchronization.
3. Stop or drain writers on AKS according to each application runbook.
4. Take the final Velero backup only for the namespaces and PVC file data that need it.
5. Restore PVC file data and any non-Git Kubernetes resources to EKS.
6. Sync Argo CD applications to EKS with target overlays.
7. Validate application behavior and data.
8. Switch ingress, DNS, traffic manager, or load balancer routing.
9. Keep AKS read-only until rollback is no longer required.

Useful final commands:

```bash
velero backup create aks-final-filedata \
  --include-namespaces team-a \
  --default-volumes-to-fs-backup \
  --snapshot-volumes=false \
  --wait

velero restore create eks-final-filedata \
  --from-backup aks-final-filedata \
  --wait
```

What it does: creates and restores a final portable file-level backup for one namespace. It does not migrate Azure disk snapshots, databases, external object buckets, managed identities, DNS records, or queues.

### Cross-cloud rollback

Rollback is only simple before target-side writes begin. Keep these controls ready:

- AKS workloads remain available or can be scaled back up.
- DNS TTL was lowered before cutover and old records can be restored.
- Database migration has a defined reverse path or a clear no-rollback point.
- Producers and consumers can be pointed back to the old queue or stream without duplicate processing surprises.
- Argo CD cluster destinations and sync windows allow returning traffic to AKS.
- EKS changes made during failed cutover are captured or disposable.

### Cross-cloud risks

| Risk | Control |
| --- | --- |
| Assuming Azure snapshots restore into EBS | Use File System Backup, data movement, or application-native migration for data. |
| Restoring AKS-specific annotations into EKS | Review ingress, identity, storage, load balancer, and CSI annotations before sync. |
| Missing CRDs or webhooks | Install platform dependencies before restoring application custom resources. |
| StorageClass mismatch | Preserve class names only when semantics match, otherwise map deliberately. |
| Secret reuse across clouds | Rotate or reconcile from an approved secret manager. |
| Unclear data owner | Assign validation and rollback decisions before cutover starts. |

## Related links

- [Velero real use cases and runbooks](real-use-cases-and-runbooks.md)
- [Back to index](index.md)
