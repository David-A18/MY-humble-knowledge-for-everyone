# Velero real use cases and runbooks

## Purpose

Use this page to map Velero capabilities to realistic Kubernetes operations.

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
- [Troubleshooting and operations](troubleshooting-and-operations.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
