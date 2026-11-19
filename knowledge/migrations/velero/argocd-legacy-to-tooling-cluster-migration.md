---
type: How-to Guide
title: Migrate an Argo CD-managed legacy cluster into a tooling cluster
description: Move team applications from a legacy cluster into a shared tooling cluster with GitOps for desired state, Velero for resources and file data, and native tools for databases.
tags: [migrations, velero, argo-cd, runbook]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Migrate an Argo CD-managed legacy cluster into a tooling cluster

This runbook moves applications from a legacy Kubernetes cluster into a shared tooling cluster without losing data. It is part of [Velero real use cases and runbooks](real-use-cases-and-runbooks.md).

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

## Related links

- [Velero real use cases and runbooks](real-use-cases-and-runbooks.md)
- [Back to index](index.md)
