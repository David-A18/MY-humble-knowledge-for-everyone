# Velero real use cases and runbooks

## Purpose

Use this page to map Velero capabilities to realistic Kubernetes operations.

## Contents

- [Use case matrix](#use-case-matrix)
- [Runbook: recover a deleted namespace](#runbook-recover-a-deleted-namespace)
- [Runbook: clone production to development](#runbook-clone-production-to-development)
- [Runbook: rebuild an EKS cluster](#runbook-rebuild-an-eks-cluster)
- [Runbook: migrate an Argo CD-managed legacy cluster into a tooling cluster](#runbook-migrate-an-argo-cd-managed-legacy-cluster-into-a-tooling-cluster)
- [Runbook: migrate Argo CD-managed workloads from Azure AKS to AWS EKS](#runbook-migrate-argo-cd-managed-workloads-from-azure-aks-to-aws-eks)
- [Runbook: prepare for risky maintenance](#runbook-prepare-for-risky-maintenance)

## Use case matrix

| Scenario | Velero pattern | Extra safeguards |
| --- | --- | --- |
| Production namespace accidentally deleted | Restore latest namespace backup. | Confirm backup age, restore into test namespace if time allows, validate PVC data. |
| Failed cluster upgrade | Restore to rebuilt or rolled-back cluster. | Check Kubernetes API compatibility and CRDs. |
| Production-to-development clone | Restore selected namespaces with namespace mapping. | Replace Secrets, DNS, external endpoints, and credentials. |
| EKS cluster rebuild | Install Velero on new cluster with same S3 location, sync backups, restore. | Ensure EBS snapshot access, CSI driver, and snapshot controller are ready. |
| Stateful app migration | Back up manifests and volume data. | Use snapshots for same-provider moves; use File System Backup or application-native migration across providers. |
| Pre-maintenance rollback point | Create manual backup before risky changes. | Also keep GitOps/IaC rollback path for desired state. |

## Runbook: recover a deleted namespace

1. Stop automated deployers that might recreate partial resources.
2. Find the latest successful backup.
3. Restore into a temporary namespace if recovery time permits.
4. Validate application resources and data.
5. Restore into the original namespace or move traffic to the restored namespace.

### Find a usable backup

```bash
velero backup get
velero backup describe <backup-name> --details
```

What it does: lists available backups and confirms whether the selected backup completed with acceptable warnings.

### Restore the namespace

```bash
velero restore create app-prod-recovery \
  --from-backup <backup-name> \
  --include-namespaces app-prod \
  --wait
```

What it does: restores the deleted namespace resources and any protected persistent volume data from the selected backup.

## Runbook: clone production to development

```bash
velero restore create app-dev-refresh \
  --from-backup app-prod-nightly-20260723030000 \
  --namespace-mappings app-prod:app-dev \
  --wait
```

What it does: restores production resources into a development namespace.

> [!WARNING]
> Production restores into development can expose secrets, customer data, production endpoints, and live credentials. Sanitize data and replace environment-specific Secrets before allowing application traffic.

## Runbook: rebuild an EKS cluster

1. Create or select the destination EKS cluster.
2. Install the EBS CSI driver and snapshot controller.
3. Install Velero with access to the same S3 bucket and snapshot location.
4. Confirm backups sync from object storage.
5. Restore critical namespaces in dependency order.
6. Validate PVC data, Services, Ingress, DNS, workload identity, and external integrations.

### Confirm backup sync

```bash
velero backup-location get
velero backup get
```

What it does: verifies the destination Velero instance can reach backup storage and has discovered backups from object storage.

## Runbook: migrate an Argo CD-managed legacy cluster into a tooling cluster

Use this scenario when a legacy Kubernetes cluster hosts many team applications and the desired target is a tooling cluster that provides shared platform services and team application hosting. The safest plan is data-first: use GitOps for desired state, Velero for Kubernetes resource recovery and PVC file data where appropriate, and application-native tooling for databases and other stateful systems.

### Ownership boundaries

| Area | Primary owner | Migration approach |
| --- | --- | --- |
| Argo CD Applications and Git repositories | Platform or GitOps team | Repoint Argo CD to the target cluster and let Git redeploy desired state. |
| Kubernetes resources not fully represented in Git | Platform team with app owners | Use Velero backup and selective restore after review. |
| PVC file data | Platform team with app owners | Use Velero File System Backup, CSI data movement, or snapshots only when compatible. |
| Databases | Database or application owner | Use native replication, logical dump, physical backup/restore, or managed-service migration. |
| Secrets | Security/platform owner | Prefer external secret systems or reissue secrets; restore only when policy allows it. |
| DNS, ingress, certificates, and traffic | Platform/network owner | Prepare target endpoints before cutover and keep rollback routing ready. |
| Validation | Application owner | Confirm data, workflows, integrations, SLOs, and business acceptance. |

### Discovery and inventory

Start by separating desired state from runtime state. In a GitOps estate, many Deployments, Services, ConfigMaps, NetworkPolicies, and Argo CD `Application` objects should be recreated from Git. Runtime objects, generated Secrets, PVC contents, Jobs, and operator-managed custom resources need separate review.

```bash
kubectl get namespaces
kubectl get applications.argoproj.io -A
kubectl get crd
kubectl get pvc,pv -A
kubectl get ingress,service -A
velero backup get
```

What it does: builds the first inventory of namespaces, Argo CD applications, CRDs, persistent volumes, traffic entry points, and existing recovery points.

If the Argo CD CLI is available, capture the GitOps view as well:

```bash
argocd app list
argocd app get <application-name>
```

What it does: identifies which repository path, revision, destination cluster, namespace, sync policy, and health state Argo CD uses for each application.

### Classify every workload

| Workload type | Preferred migration path | Decision point |
| --- | --- | --- |
| Stateless app fully in Git | Recreate from Git through Argo CD. | Use Velero only for emergency restore or objects outside Git. |
| App with PVC file uploads or local assets | Restore PVC file data with Velero File System Backup or data movement. | Test restore time and consistency before cutover. |
| Database in Kubernetes | Use database-native replication or backup/restore; use Velero for manifests. | Decide acceptable RPO and write-freeze window. |
| Operator-managed platform component | Install operator and CRDs first, then restore or reconcile custom resources. | Confirm version compatibility and conversion webhooks. |
| External managed service dependency | Reconfigure clients and secrets. | Velero does not move external service data. |

### Target prerequisites

Before restoring workloads, prepare the target tooling cluster:

1. Install cluster add-ons such as ingress controllers, certificate managers, external DNS, external secrets, policy engines, metrics, logging agents, CSI drivers, and snapshot controllers.
2. Install CRDs and operators before restoring custom resources that depend on them.
3. Configure StorageClasses and decide whether source storage class names will be preserved or mapped.
4. Install Velero with access to the backup storage and node-agent if File System Backup or data movement is used.
5. Register the target cluster in Argo CD or install the Argo CD control plane that will manage it.
6. Prepare network paths, DNS names, certificates, image pull access, workload identity, and secrets.

### Back up Kubernetes resources and PVC file data

For a GitOps-managed migration, prefer a scoped backup. Do not blindly restore the whole cluster into the target because cluster-scoped resources, admission webhooks, generated objects, and controller-owned resources can conflict with the new platform.

```bash
velero backup create legacy-apps-resources \
  --include-namespaces team-a,team-b,team-c \
  --snapshot-volumes=false \
  --wait
```

What it does: captures selected application Kubernetes resources without trying to snapshot volumes. Use it when Argo CD will recreate most desired state and Velero is a recovery reference.

For PVC file data that is not a database and must move with the workload:

```bash
velero backup create legacy-apps-pvc-data \
  --include-namespaces team-a,team-b,team-c \
  --default-volumes-to-fs-backup \
  --snapshot-volumes=false \
  --wait
```

What it does: backs up selected namespaces and asks Velero to use File System Backup for mounted pod volumes instead of provider snapshots.

> [!WARNING]
> File System Backup reads live mounted volumes. For busy databases, message brokers, and indexes, this is usually not enough for application consistency. Use application-native migration and keep Velero for Kubernetes resources around the service.

### Rehearsal restore

Run at least one restore into a rehearsal namespace or non-production target before the real cutover.

```bash
velero restore create legacy-apps-rehearsal \
  --from-backup legacy-apps-pvc-data \
  --namespace-mappings team-a:team-a-rehearsal,team-b:team-b-rehearsal \
  --wait

velero restore describe legacy-apps-rehearsal --details
velero restore logs legacy-apps-rehearsal
```

What it does: restores selected namespaces under temporary names and shows whether Kubernetes objects, PVCs, and volume operations restored cleanly.

During rehearsal, validate:

- CRDs exist before custom resources are restored.
- Operators reconcile restored custom resources without version errors.
- PVCs bind to the intended StorageClass.
- Applications can start without production traffic.
- Secrets are replaced or reconciled from the target secret source.
- Database recovery is handled by the database runbook, not inferred from pod startup.
- Argo CD does not fight Velero-restored objects because of ownership or drift.

### Final synchronization and cutover

When rehearsal is accepted, schedule a cutover window. The final synchronization should be owned per data type:

| Data type | Final sync pattern |
| --- | --- |
| Git-managed Kubernetes manifests | Freeze merges or pin Argo CD revisions, then sync the target. |
| PVC file data | Stop writers, take a final Velero File System Backup or data movement backup, restore to target, then validate checksums or app-level counts. |
| Databases | Promote replica, restore final backup, or complete native migration according to the database runbook. |
| Secrets | Reconcile from external secret manager or rotate manually before traffic. |
| DNS and ingress | Lower TTL ahead of time, switch records or load balancer targets during cutover, and keep rollback records ready. |

> [!IMPORTANT]
> A write freeze must be explicit. Scaling an application down, pausing a queue consumer, setting maintenance mode, or making a database read-only are different controls with different owners. Record which control is used for each stateful service.

Useful cutover commands:

```bash
kubectl -n team-a scale deployment --all --replicas=0
velero backup create team-a-final \
  --include-namespaces team-a \
  --default-volumes-to-fs-backup \
  --snapshot-volumes=false \
  --wait
velero restore create team-a-final-restore \
  --from-backup team-a-final \
  --wait
```

What it does: stops Deployment-managed writers in one namespace, captures a final file-level backup for mounted volumes, and restores it on the destination. StatefulSets, Jobs, CronJobs, databases, and queue consumers need workload-specific freeze steps.

### Ordering

Restore or reconcile in this order:

1. Target platform foundations: network, identity, storage, ingress, certificate, DNS, policy, observability, and backup tooling.
2. CRDs and operators.
3. Shared namespaces and platform services required by team apps.
4. Secrets and external secret bindings.
5. PVC data or application-native restored data.
6. Workload controllers from GitOps.
7. Ingress and traffic.
8. Monitoring, alerts, dashboards, and runbook sign-off.

### Validation

```bash
velero restore get
kubectl get pods,pvc,ingress -A
kubectl get applications.argoproj.io -A
```

What it does: confirms restore status, workload readiness, PVC binding, ingress creation, and Argo CD application health after migration.

Application owners should also validate domain-specific checks such as login, writes, reads, reports, background jobs, queue lag, database row counts, object counts, and error budgets.

### Legacy-cluster rollback

Keep the legacy cluster and data source intact until the target is accepted. A practical rollback plan includes:

- DNS or traffic routing back to the legacy ingress.
- Argo CD destination or cluster registration still available for the legacy cluster.
- Database replication direction clearly documented before and after cutover.
- A rule for rejecting rollback once target-only writes have started and cannot be replayed safely.
- A backup of any target-side changes made during validation.

### Risks and decision points

| Decision | Risk if ignored |
| --- | --- |
| Restore from Git or from Velero? | Two controllers may fight or old generated objects may override intended state. |
| Restore CRDs before custom resources? | Custom resources may fail to create or lose schema conversion behavior. |
| Use File System Backup for databases? | Restored database files may be crash-consistent at best and logically inconsistent at worst. |
| Preserve or change StorageClass names? | PVCs can stay pending or bind to the wrong storage tier. |
| Keep source writable during final sync? | Final backup may miss committed writes. |

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

## Runbook: prepare for risky maintenance

```bash
velero backup create pre-upgrade-$(date +%Y%m%d%H%M%S) --wait
velero backup get
```

What it does: creates a point-in-time recovery point before maintenance and lists backup status.

> [!IMPORTANT]
> A pre-maintenance Velero backup should complement, not replace, IaC, GitOps, database backup, and rollback plans.

## Related links

- [Backup and restore workflows](backup-restore-workflows.md)
- [Cluster migration and disaster recovery](cluster-migration-and-disaster-recovery.md)
- [Storage and volume backups](storage-and-volume-backups.md)
- [Troubleshooting and operations](troubleshooting-and-operations.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
