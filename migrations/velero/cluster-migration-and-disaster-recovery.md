# Velero cluster migration and disaster recovery

## Purpose

Use this page to plan Velero-based Kubernetes cluster migration, disaster recovery, and cross-cluster restores.

## Contents

- [Migration model](#migration-model)
- [Before migration](#before-migration)
- [Source and destination setup](#source-and-destination-setup)
- [Same-provider cluster migration](#same-provider-cluster-migration)
- [Disaster recovery with read-only backup storage](#disaster-recovery-with-read-only-backup-storage)
- [Cross-provider and cross-region migration](#cross-provider-and-cross-region-migration)
- [API version planning](#api-version-planning)
- [Validation and rollback boundaries](#validation-and-rollback-boundaries)

## Migration model

Velero migration is based on shared backup storage. The source cluster writes backups into an object storage bucket and prefix. The destination cluster runs Velero with access to the same backup storage location. Velero syncs backup metadata from object storage into the destination cluster so restore operations can use backups created elsewhere.

The important distinction is:

- Kubernetes resources move through Velero backup archives in object storage.
- Provider snapshots usually remain in the provider storage system.
- File System Backup and CSI data movement place volume data in an object-storage-backed repository.
- Application-consistent databases, queues, and external services need their own migration path.

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

## Source and destination setup

Prepare the source cluster:

1. Confirm Velero can write to backup storage.
2. Confirm volume backup method per workload.
3. Capture CRDs, StorageClasses, ingress classes, workload identities, and external dependencies.
4. Run a test backup and inspect warnings before the cutover window.

```bash
kubectl config use-context source-cluster
velero backup-location get
velero snapshot-location get
kubectl get crd,storageclass,ingressclass
kubectl get pvc,pv -A
```

What it does: verifies backup storage and inventories APIs and storage dependencies that must exist or be mapped on the destination.

Prepare the destination cluster:

1. Install platform dependencies before application restore: CRDs, operators, CSI drivers, snapshot controller, ingress, DNS, certificates, policy, and secret tooling.
2. Install Velero with access to the backup storage.
3. Set the backup location read-only until the destination is intentionally allowed to create backups.
4. Confirm Velero syncs backup metadata from object storage.

```bash
kubectl config use-context destination-cluster
velero backup-location get
velero backup get
kubectl get crd,storageclass,ingressclass
kubectl get daemonset node-agent -n velero
```

What it does: verifies the destination can see backups and has the APIs, storage, and node-agent needed for restore.

## Backup sync check

Velero treats object storage as the source of truth for completed backups. A destination cluster can discover source backups when it points to the same bucket and prefix, or to a copied backup storage layout.

```bash
velero backup get
velero backup describe <source-backup-name> --details
```

What it does: confirms the destination Velero instance has synced backup metadata and can inspect a source-created backup.

> [!IMPORTANT]
> If `velero backup get` is empty on the destination, do not start restoring. Check bucket, prefix, provider plugin, credentials, network path, and backup storage access mode first.

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

### Restore in dependency order

For complex clusters, avoid one large restore until the order is proven. A safer sequence is:

1. CRDs and operator namespaces.
2. Shared platform namespaces.
3. Secrets or external secret bindings.
4. PVC data and workload namespaces.
5. Ingress, DNS, and traffic.

```bash
velero restore create app-prod-crds \
  --from-backup source-app-prod \
  --include-cluster-resources=true \
  --include-resources customresourcedefinitions \
  --wait

velero restore create app-prod-workloads \
  --from-backup source-app-prod \
  --include-namespaces app-prod \
  --wait
```

What it does: shows the idea of restoring API definitions before workload resources. Adjust the split to match how the source backup was created and how the destination platform is managed.

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

### BackupStorageLocation read-only YAML

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
  accessMode: ReadOnly
```

What it does: declares a backup location that can be used for restore discovery without letting the recovery cluster write or delete backup data.

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

### Cross-provider backup pattern

```bash
velero backup create app-prod-portable \
  --include-namespaces app-prod \
  --default-volumes-to-fs-backup \
  --snapshot-volumes=false \
  --wait
```

What it does: avoids provider snapshots and uses File System Backup for eligible mounted pod volumes so PVC file data can be restored on a different provider.

> [!WARNING]
> This pattern is not a database consistency guarantee. Stop writes, use database-native backup, or replicate data before using a file-level backup as a migration input.

## API version planning

When source and destination clusters differ, check removed Kubernetes APIs before backup and restore.

```bash
kubectl api-resources
kubectl get crd
velero backup describe <backup-name> --details
```

What it does: inventories available resource APIs and checks what Velero captured.

## Validation and rollback boundaries

Validate migration at three levels:

| Level | Checks |
| --- | --- |
| Velero operation | `velero backup describe`, `velero restore describe`, logs, warnings, and errors. |
| Kubernetes platform | Pods ready, PVCs bound, Services and Ingress created, CRDs served, operators healthy. |
| Application data | Owner-approved checks such as row counts, file counts, object counts, queue lag, login, writes, and background jobs. |

```bash
velero restore get
velero restore describe <restore-name> --details
kubectl get pods,pvc,ingress -n app-prod
kubectl get events -n app-prod --sort-by=.lastTimestamp
```

What it does: checks restore status and common Kubernetes signals before application owners perform domain-specific validation.

Rollback is only dependable when the source remains usable and the data direction is clear:

- Keep the source cluster and original data source available until acceptance.
- Lower DNS TTL before cutover, not during rollback.
- Define when target writes make rollback unsafe.
- Keep Argo CD or deployment automation from reconciling both source and destination unexpectedly.
- Capture any target-side changes made during validation.

## Related links

- [Velero cluster migration](https://velero.io/docs/v1.18/migration-case/)
- [Velero disaster recovery](https://velero.io/docs/v1.18/disaster-case/)
- [Velero API group versions](https://velero.io/docs/v1.18/enable-api-group-versions-feature/)
- [Real use cases and runbooks](real-use-cases-and-runbooks.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
