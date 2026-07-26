# Velero troubleshooting and operations

## Purpose

Use this page to diagnose Velero backup, restore, storage, snapshot, node-agent, and data movement issues.

## Contents

- [First checks](#first-checks)
- [Decision flow](#decision-flow)
- [Symptom guide](#symptom-guide)
- [Inspect Velero resources](#inspect-velero-resources)
- [Inspect node-agent and data movement](#inspect-node-agent-and-data-movement)
- [Troubleshoot backup storage](#troubleshoot-backup-storage)
- [Troubleshoot CSI snapshots](#troubleshoot-csi-snapshots)
- [Troubleshoot File System Backup](#troubleshoot-file-system-backup)
- [Troubleshoot restore collisions and PVCs](#troubleshoot-restore-collisions-and-pvcs)
- [Operational habits](#operational-habits)

## First checks

```bash
kubectl get pods -n velero
velero version
velero backup-location get
velero snapshot-location get
velero backup get
velero restore get
```

What it does: checks component health, version visibility, storage location status, and recent backup or restore outcomes.

## Decision flow

Use this order so you do not chase volume errors when the real problem is storage access or a failed backup.

1. Confirm the Velero server is running.
2. Confirm the backup storage location is `Available`.
3. Confirm the backup or restore phase is not `Failed` or `PartiallyFailed` without review.
4. Inspect operation logs.
5. If Kubernetes resources are missing, inspect filters and restore warnings.
6. If PVCs are missing or pending, inspect storage class, snapshots, and volume restore objects.
7. If file or data movement is stuck, inspect node-agent, repositories, and `DataUpload` or `DataDownload`.
8. If resources already exist, decide whether to restore into a new namespace, delete the test namespace, or use an existing-resource policy.

## Symptom guide

| Symptom | Check | Likely cause |
| --- | --- | --- |
| Backup location unavailable | `velero backup-location get` | S3 endpoint, region, credentials, bucket policy, or network issue. |
| Backup has warnings | `velero backup describe <name> --details` | Skipped resources, hook issues, or volume backup failures. |
| Restore does not create PVC data | `velero restore logs <name>` and `kubectl describe pvc` | Missing snapshot access, missing StorageClass, CSI mismatch, or data mover failure. |
| CSI snapshots are not created | `kubectl get volumesnapshotclass` | Missing snapshot controller, CRDs, driver support, or Velero CSI feature flag. |
| File System Backup does not run | `kubectl get podvolumebackups -n velero` | Missing node-agent, missing pod volume annotation, or unsupported host path layout. |
| Data movement is slow | `kubectl get datauploads,datadownloads -n velero` | Low node-agent concurrency, large data set, resource throttling, or repository/cache limits. |
| Restore objects already exist | `velero restore describe <name> --details` | Restoring into a namespace with existing resources. |

## Inspect Velero server logs

```bash
kubectl logs -n velero deploy/velero
kubectl logs -n velero deploy/velero --previous
kubectl describe deployment velero -n velero
```

What it does: shows current and previous Velero server logs and deployment configuration, including plugin init containers and server arguments.

## Inspect Velero resources

```bash
kubectl get backups,restores,schedules,backupstoragelocations,volumesnapshotlocations -n velero
kubectl describe backup <backup-name> -n velero
kubectl describe restore <restore-name> -n velero
kubectl get backup <backup-name> -n velero -o yaml
```

What it does: inspects Velero custom resources directly through Kubernetes.

## Inspect node-agent and data movement

```bash
kubectl get daemonset node-agent -n velero
kubectl get pods -n velero -l name=node-agent
kubectl get podvolumebackups,podvolumerestores,datauploads,datadownloads -n velero
kubectl logs -n velero daemonset/node-agent
```

What it does: checks whether node-agent exists, whether volume operations are progressing, and what node-agent logged.

## Troubleshoot backup storage

Check the configured bucket, prefix, region, and access mode:

```bash
velero backup-location get
kubectl describe backupstoragelocation default -n velero
kubectl get backupstoragelocation default -n velero -o yaml
```

What it does: shows whether the backup location is available, read-only, or failing validation.

If the location is read-only during disaster recovery, backups and deletion may fail by design. Switch to read-write only when the cluster should resume writing backups.

Common checks:

- Bucket or container name is correct.
- Prefix matches the source cluster or copied backup layout.
- Region and endpoint match the provider.
- Velero pod identity or credentials can list, read, write, and delete the expected objects.
- Network policy, proxy, private endpoint, or firewall allows access.
- Object lifecycle rules have not deleted repository or backup archive data unexpectedly.

## Troubleshoot CSI snapshots

```bash
kubectl get volumesnapshotclass
kubectl get volumesnapshot -A
kubectl get volumesnapshotcontent
kubectl describe volumesnapshot <snapshot-name> -n <namespace>
```

What it does: checks snapshot class selection, snapshot object status, and provider binding details.

Common fixes:

- Install or repair the CSI snapshot controller.
- Install the provider CSI driver with snapshot support.
- Create a `VolumeSnapshotClass` for the correct driver.
- Ensure only one Velero default snapshot class label exists per driver.
- Confirm the destination cluster uses the same CSI driver name for CSI snapshot restore.

### Check snapshot class selection

```bash
kubectl get volumesnapshotclass -o yaml
kubectl get pvc -n <namespace> <claim-name> -o yaml
```

What it does: compares the PVC storage driver and the available `VolumeSnapshotClass` objects. The snapshot class driver must match the PVC's CSI driver.

## Troubleshoot File System Backup

```bash
kubectl get podvolumebackups -n velero
kubectl describe podvolumebackup <name> -n velero
kubectl get backuprepositories -n velero
kubectl describe backuprepository <name> -n velero
```

What it does: checks file-system backup objects and backup repository readiness.

Common fixes:

- Install node-agent with `--use-node-agent`.
- Add the required pod volume annotations or use the default file-system backup setting.
- Verify node-agent can access kubelet pod volume paths.
- Configure resource requests, limits, and cache PVCs for large restores.

> [!WARNING]
> Increasing data movement concurrency can improve throughput but may overload storage, network, or nodes. Change concurrency with measured tests.

### Check pod volume annotations

```bash
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A5 backup.velero.io
kubectl describe backup <backup-name> -n velero
```

What it does: confirms whether the pod volume was selected for File System Backup and whether the backup recorded volume work.

### Troubleshoot data mover slowness

```bash
kubectl get datauploads -n velero -o wide
kubectl get datadownloads -n velero -o wide
kubectl describe dataupload <name> -n velero
kubectl describe datadownload <name> -n velero
kubectl top pods -n velero
kubectl top nodes
```

What it does: checks data movement status, node placement, errors, and resource pressure.

Common causes:

- Large files or many small files.
- Low node-agent concurrency.
- Slow object storage endpoint.
- Throttled node CPU, memory, disk, or network.
- Repository cache pressure or insufficient ephemeral storage.
- Storage backend taking too long to provision temporary volumes.

## Troubleshoot restore collisions and PVCs

```bash
velero restore describe <restore-name> --details
velero restore logs <restore-name>
kubectl get pvc,pv -n <namespace>
kubectl describe pvc <claim-name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

What it does: combines restore details with Kubernetes storage events so you can separate Velero restore problems from scheduler or CSI provisioning problems.

If restore logs say resources already exist:

- Restore into a temporary namespace with `--namespace-mappings`.
- Delete only the failed test namespace and restore again.
- Use `--existing-resource-policy update` only after confirming updates are safe.
- Avoid restoring old GitOps-managed resources over actively reconciled objects unless ownership is clear.

If PVCs stay pending:

- Confirm the destination StorageClass exists.
- Confirm topology and `WaitForFirstConsumer` behavior can schedule the restored pods.
- Use a storage-class mapping ConfigMap when source and destination names differ.
- Confirm snapshots are accessible or File System Backup/data movement restored the data path.

## Verify a restore

```bash
kubectl get all,pvc -n <namespace>
kubectl describe pvc <claim-name> -n <namespace>
kubectl exec -n <namespace> <pod-name> -- ls -la /data
```

What it does: checks restored resources, PVC binding, and whether expected files exist inside a restored workload.

## Operational habits

- Run scheduled restore tests into isolated namespaces.
- Alert on failed and partially failed backups.
- Track backup age against RPO.
- Review S3 lifecycle and EBS snapshot cost regularly.
- Keep Velero, plugins, and Kubernetes versions compatible.
- Document who can restore Secrets and production data.
- Keep restore runbooks with the application, not only with the platform team.
- Review backup storage IAM quarterly and after team changes.
- Test one representative File System Backup and one snapshot restore before declaring a cluster protected.

## Related links

- [Velero troubleshooting](https://velero.io/docs/v1.18/troubleshooting/)
- [Velero File System Backup](https://velero.io/docs/v1.18/file-system-backup/)
- [Velero troubleshoot a restore](https://velero.io/docs/v1.18/troubleshoot-restore/)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
