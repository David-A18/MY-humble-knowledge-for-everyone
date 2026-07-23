# Velero backup and restore workflows

## Purpose

Use this page for the day-to-day Velero commands that create backups, schedules, restores, namespace mappings, and inspection output.

## Create backups

| Task | Command pattern | When to use it |
| --- | --- | --- |
| Back up a namespace | `velero backup create <name> --include-namespaces <namespace>` | Protect one application boundary. |
| Back up by label | `velero backup create <name> --selector app=web` | Protect resources across namespaces with consistent labels. |
| Exclude a namespace | `velero backup create <name> --exclude-namespaces kube-system` | Avoid system or generated resources. |
| Wait for completion | `velero backup create <name> --wait` | Useful in runbooks and CI checks. |

### Back up one namespace

```bash
velero backup create app-prod-manual --include-namespaces app-prod --wait
```

What it does: backs up Kubernetes resources in `app-prod` and waits for Velero to finish.

### Inspect backup details

```bash
velero backup describe app-prod-manual --details
velero backup logs app-prod-manual
```

What it does: shows included resources, volume backup details, warnings, errors, and controller logs for the backup.

## Schedule recurring backups

```bash
velero schedule create app-prod-daily \
  --schedule "0 3 * * *" \
  --include-namespaces app-prod \
  --ttl 168h
```

What it does: creates a daily 03:00 backup schedule for `app-prod` and keeps each backup for seven days.

> [!IMPORTANT]
> Align `--ttl`, S3 lifecycle, snapshot retention, and compliance retention. A mismatch can leave stale cost or remove recovery points earlier than expected.

## Exclude specific objects

```bash
kubectl label -n app-prod secret/generated-token velero.io/exclude-from-backup=true
```

What it does: labels one object so Velero excludes it even if the namespace or selector matches the backup.

## Use backup hooks

Hooks run commands in containers before or after backup. Use them to quiesce an application, flush buffers, or pause writes when the application supports it.

```bash
kubectl annotate pod database-0 -n app-prod \
  pre.hook.backup.velero.io/command='["/bin/sh","-c","sync"]'
```

What it does: adds a simple pre-backup hook to run `sync` in a pod before Velero backs it up.

> [!WARNING]
> Hooks can affect live workloads. Test hook commands in a non-production namespace before adding them to production backups.

## Restore backups

### Restore into the original namespace

```bash
velero restore create app-prod-restore --from-backup app-prod-manual --wait
```

What it does: restores resources from `app-prod-manual` into their original namespaces.

> [!WARNING]
> Restoring into an active namespace can collide with existing objects or reintroduce old configuration. Prefer a test namespace first unless this is a deliberate recovery action.

### Restore into a different namespace

```bash
velero restore create app-prod-restore-test \
  --from-backup app-prod-manual \
  --namespace-mappings app-prod:app-restore \
  --wait
```

What it does: restores resources backed up from `app-prod` into `app-restore`.

### Inspect restore output

```bash
velero restore describe app-prod-restore-test --details
velero restore logs app-prod-restore-test
kubectl get all,pvc -n app-restore
```

What it does: checks restore warnings and errors, then verifies restored application and PVC objects.

## Cleanup test restores

```bash
kubectl delete namespace app-restore
velero restore delete app-prod-restore-test
```

What it does: removes the temporary namespace and Velero restore object after validation.

> [!WARNING]
> Deleting a namespace deletes namespaced workloads and PVCs. Confirm you are cleaning up a test namespace before running this command.

## Related links

- [Velero backup reference](https://velero.io/docs/v1.18/backup-reference/)
- [Velero restore reference](https://velero.io/docs/v1.18/restore-reference/)
- [Cluster migration and disaster recovery](cluster-migration-and-disaster-recovery.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
