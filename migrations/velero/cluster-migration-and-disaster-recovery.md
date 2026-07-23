# Velero cluster migration and disaster recovery

## Purpose

Use this page to plan Velero-based Kubernetes cluster migration, disaster recovery, and cross-cluster restores.

## Migration model

Velero migration is based on shared backup storage. The source cluster writes backups into an object storage bucket and prefix. The destination cluster runs Velero with access to the same backup storage location. Velero syncs backup metadata from object storage into the destination cluster so restore operations can use backups created elsewhere.

## Before migration

| Check | Why it matters |
| --- | --- |
| Kubernetes version compatibility | Velero does not support restoring into a lower Kubernetes version than the source. |
| API group versions | Removed or changed APIs can block restores of old resources or CRDs. |
| CRDs and operators | Custom resources often need their CRDs and controllers installed before restore. |
| Storage driver names | CSI snapshot restores need compatible driver names on source and destination. |
| Region and provider boundaries | AWS and Azure snapshot plugins do not handle all cross-region or cross-provider data moves. |
| Secrets and endpoints | Restored Secrets, URLs, certificates, and external service references may need environment changes. |

> [!WARNING]
> Do not treat a cluster migration as complete until workloads start, PVC data is verified, ingress and DNS are tested, and application owners confirm expected behavior.

## Same-provider cluster migration

### Back up on the source cluster

```bash
kubectl config use-context source-cluster
velero backup create source-app-prod --include-namespaces app-prod --wait
velero backup describe source-app-prod --details
```

What it does: creates and verifies a source namespace backup before switching to the destination cluster.

### Restore on the destination cluster

```bash
kubectl config use-context destination-cluster
velero backup get
velero restore create app-prod-migration \
  --from-backup source-app-prod \
  --namespace-mappings app-prod:app-prod \
  --wait
```

What it does: confirms the destination sees synced backups and restores the selected backup into the destination cluster.

## Disaster recovery with read-only backup storage

During disaster recovery, set the backup storage location to read-only before restoring. This helps prevent the recovery cluster from creating or deleting backup objects during the restore process.

```bash
kubectl patch backupstoragelocation default \
  --namespace velero \
  --type merge \
  --patch '{"spec":{"accessMode":"ReadOnly"}}'
```

What it does: changes the default backup storage location to read-only mode.

After recovery validation, restore read-write mode only when this cluster should resume creating backups:

```bash
kubectl patch backupstoragelocation default \
  --namespace velero \
  --type merge \
  --patch '{"spec":{"accessMode":"ReadWrite"}}'
```

What it does: allows Velero to write new backups to the storage location again.

## Cross-provider and cross-region migration

Provider snapshots are usually tied to a provider, region, account, storage system, or CSI driver. If you need to move volume data across those boundaries, use one of these approaches:

| Requirement | Recommended path |
| --- | --- |
| Cross-provider volume data migration | File System Backup or application-native export/import. |
| Cross-region migration with unsupported snapshot copy | File System Backup or provider-native snapshot copy plus restore testing. |
| Database migration with low data loss | Database replication, logical dump, or native backup plus Velero for Kubernetes resources. |
| Stateless workload migration | Velero Kubernetes object backup, GitOps redeploy, or both. |

> [!IMPORTANT]
> For cross-provider migrations, Velero can help move manifests and file-level volume contents, but it cannot make every cloud snapshot portable.

## API version planning

When source and destination clusters differ, check removed Kubernetes APIs before backup and restore.

```bash
kubectl api-resources
kubectl get crd
velero backup describe <backup-name> --details
```

What it does: inventories available resource APIs and checks what Velero captured.

## Related links

- [Velero cluster migration](https://velero.io/docs/v1.18/migration-case/)
- [Velero disaster recovery](https://velero.io/docs/v1.18/disaster-case/)
- [Velero API group versions](https://velero.io/docs/v1.18/enable-api-group-versions-feature/)
- [Real use cases and runbooks](real-use-cases-and-runbooks.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
