# Velero troubleshooting and operations

## Purpose

Use this page to diagnose Velero backup, restore, storage, snapshot, node-agent, and data movement issues.

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

## Inspect Velero resources

```bash
kubectl get backups,restores,schedules,backupstoragelocations,volumesnapshotlocations -n velero
kubectl describe backup <backup-name> -n velero
kubectl describe restore <restore-name> -n velero
```

What it does: inspects Velero custom resources directly through Kubernetes.

## Inspect node-agent and data movement

```bash
kubectl get daemonset node-agent -n velero
kubectl get podvolumebackups,podvolumerestores,datauploads,datadownloads -n velero
kubectl logs -n velero deploy/velero
```

What it does: checks whether node-agent exists, whether volume operations are progressing, and what the Velero server logged.

## Troubleshoot backup storage

Check the configured bucket, prefix, region, and access mode:

```bash
velero backup-location get
kubectl describe backupstoragelocation default -n velero
```

What it does: shows whether the backup location is available, read-only, or failing validation.

If the location is read-only during disaster recovery, backups and deletion may fail by design. Switch to read-write only when the cluster should resume writing backups.

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

## Troubleshoot File System Backup

```bash
kubectl get podvolumebackups -n velero
kubectl describe podvolumebackup <name> -n velero
kubectl get backuprepositories -n velero
```

What it does: checks file-system backup objects and backup repository readiness.

Common fixes:

- Install node-agent with `--use-node-agent`.
- Add the required pod volume annotations or use the default file-system backup setting.
- Verify node-agent can access kubelet pod volume paths.
- Configure resource requests, limits, and cache PVCs for large restores.

> [!WARNING]
> Increasing data movement concurrency can improve throughput but may overload storage, network, or nodes. Change concurrency with measured tests.

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

## Related links

- [Velero troubleshooting](https://velero.io/docs/v1.18/troubleshooting/)
- [Velero File System Backup](https://velero.io/docs/v1.18/file-system-backup/)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
