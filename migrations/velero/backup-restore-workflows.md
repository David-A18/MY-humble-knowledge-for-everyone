# Velero backup and restore workflows

## Purpose

Use this page for the day-to-day Velero commands that create backups, schedules, restores, namespace mappings, and inspection output.

## Contents

- [Create backups](#create-backups)
- [Schedule recurring backups](#schedule-recurring-backups)
- [Filter what Velero backs up](#filter-what-velero-backs-up)
- [Use backup hooks](#use-backup-hooks)
- [Restore backups](#restore-backups)
- [Change resources during restore](#change-resources-during-restore)
- [Cleanup test restores](#cleanup-test-restores)

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

### Back up one namespace with YAML

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: app-prod-manual
  namespace: velero
spec:
  includedNamespaces:
  - app-prod
  ttl: 168h0m0s
  snapshotVolumes: false
```

What it does: declares the same backup as a Kubernetes custom resource. This is useful when backups are created by GitOps or automation instead of an operator shell.

### Inspect backup details

```bash
velero backup describe app-prod-manual --details
velero backup logs app-prod-manual
```

What it does: shows included resources, volume backup details, warnings, errors, and controller logs for the backup.

### Back up by label

```bash
velero backup create web-prod \
  --selector app=web,environment=prod \
  --wait
```

What it does: backs up resources with both labels, regardless of namespace, unless other filters limit the backup.

### Back up selected resource kinds

```bash
velero backup create app-prod-workloads \
  --include-namespaces app-prod \
  --include-resources deployments,statefulsets,services,configmaps,secrets,persistentvolumeclaims \
  --wait
```

What it does: backs up only the listed resource types in `app-prod`. Use this when you want a narrow restore set and have checked that omitted resources are recreated elsewhere.

### Include cluster-scoped dependencies

```bash
velero backup create app-prod-with-crds \
  --include-namespaces app-prod \
  --include-cluster-resources=true \
  --wait
```

What it does: includes cluster-scoped resources along with the namespace backup. Review this carefully because cluster roles, storage classes, webhooks, and CRDs can affect the whole destination cluster.

> [!WARNING]
> Do not restore cluster-scoped resources into a shared cluster without review. Old CRDs, admission webhooks, or RBAC can break unrelated workloads.

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

### Schedule with timezone

```bash
velero schedule create app-prod-daily-madrid \
  --schedule "CRON_TZ=Europe/Madrid 0 3 * * *" \
  --include-namespaces app-prod \
  --ttl 168h
```

What it does: creates a schedule that runs at 03:00 Madrid time instead of relying on the controller's default timezone.

### Schedule with YAML

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: app-prod-daily
  namespace: velero
spec:
  schedule: "0 3 * * *"
  template:
    includedNamespaces:
    - app-prod
    ttl: 168h0m0s
    snapshotVolumes: true
```

What it does: declares a recurring backup template in Kubernetes. Velero creates timestamped `Backup` objects from this schedule.

### Trigger a schedule manually

```bash
velero backup create app-prod-manual-from-schedule \
  --from-schedule app-prod-daily \
  --wait
```

What it does: creates an immediate backup using the schedule template without changing the future schedule.

## Filter what Velero backs up

Velero filtering controls what Kubernetes resources are included in backup or restore. Start narrow when learning, then add cluster-scoped resources only when the dependency is understood.

| Filter | Example | Use |
| --- | --- | --- |
| Namespace include | `--include-namespaces app-prod` | Back up one application boundary. |
| Namespace exclude | `--exclude-namespaces kube-system` | Avoid generated platform namespaces. |
| Resource include | `--include-resources deployments,services` | Back up selected kinds. |
| Resource exclude | `--exclude-resources events,events.events.k8s.io` | Skip noisy or generated resources. |
| Label selector | `--selector app=web` | Select resources across namespaces by labels. |
| Cluster resources | `--include-cluster-resources=true` | Include CRDs, RBAC, StorageClasses, and other cluster-scoped objects. |

## Exclude specific objects

```bash
kubectl label -n app-prod secret/generated-token velero.io/exclude-from-backup=true
```

What it does: labels one object so Velero excludes it even if the namespace or selector matches the backup.

### Use a resource-policy ConfigMap

```yaml
version: v1
includeExcludePolicy:
  includedClusterScopedResources:
  - crd
  excludedClusterScopedResources: []
  includedNamespaceScopedResources:
  - deployment
  - service
  - configmap
  - secret
  - persistentvolumeclaim
  excludedNamespaceScopedResources:
  - event
```

What it does: defines reusable include/exclude rules for backups.

```bash
kubectl create configmap app-prod-resource-policy \
  --from-file=resource-policies.yaml \
  -n velero

velero backup create app-prod-policy-backup \
  --include-namespaces app-prod \
  --resource-policies-configmap app-prod-resource-policy \
  --wait
```

What it does: stores the policy in the Velero namespace and creates a backup that uses it.

## Use backup hooks

Hooks run commands in containers before or after backup. Use them to quiesce an application, flush buffers, or pause writes when the application supports it.

```bash
kubectl annotate pod database-0 -n app-prod \
  pre.hook.backup.velero.io/command='["/bin/sh","-c","sync"]'
```

What it does: adds a simple pre-backup hook to run `sync` in a pod before Velero backs it up.

> [!WARNING]
> Hooks can affect live workloads. Test hook commands in a non-production namespace before adding them to production backups.

### Hook annotation on a workload template

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
  namespace: app-prod
spec:
  template:
    metadata:
      annotations:
        pre.hook.backup.velero.io/container: database
        pre.hook.backup.velero.io/command: '["/bin/sh","-c","sync"]'
        pre.hook.backup.velero.io/timeout: 30s
```

What it does: places the hook on the pod template so replacement pods keep the annotation.

> [!IMPORTANT]
> `sync` is only an illustrative file-system flush. Real database consistency needs a database-specific backup, lock, checkpoint, snapshot, or replication procedure.

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

### Restore with YAML

```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: app-prod-restore-test
  namespace: velero
spec:
  backupName: app-prod-manual
  includedNamespaces:
  - app-prod
  namespaceMapping:
    app-prod: app-restore
```

What it does: declares a restore as a Kubernetes custom resource instead of using only the CLI.

### Restore with existing-resource update policy

```bash
velero restore create app-prod-update \
  --from-backup app-prod-manual \
  --include-namespaces app-prod \
  --existing-resource-policy update \
  --wait
```

What it does: asks Velero to update existing resources where possible instead of skipping every existing object.

> [!WARNING]
> Existing-resource update is best-effort and does not overwrite PVC data. Use it only after reviewing which resources already exist in the target namespace.

### Inspect restore output

```bash
velero restore describe app-prod-restore-test --details
velero restore logs app-prod-restore-test
kubectl get all,pvc -n app-restore
```

What it does: checks restore warnings and errors, then verifies restored application and PVC objects.

## Change resources during restore

Use restore-time changes when source and destination clusters differ. Common examples are namespace mapping, StorageClass mapping, image registry changes, and annotation cleanup.

### Map StorageClasses during restore

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: change-storage-class-config
  namespace: velero
  labels:
    velero.io/plugin-config: ""
    velero.io/change-storage-class: RestoreItemAction
data:
  gp2: gp3
  managed-premium: gp3
```

What it does: maps source StorageClass names to destination StorageClass names during restore.

```bash
kubectl apply -f change-storage-class-config.yaml

velero restore create app-prod-storage-map \
  --from-backup app-prod-manual \
  --namespace-mappings app-prod:app-restore \
  --wait
```

What it does: applies the mapping ConfigMap and starts a restore that can bind PVCs to destination storage classes.

### Use restore resource modifiers

```yaml
version: v1
resourceModifierRules:
- conditions:
    groupResource: deployments.apps
    namespaces:
    - app-prod
  patches:
  - operation: replace
    path: "/spec/template/spec/nodeSelector"
    value:
      kubernetes.io/os: linux
- conditions:
    groupResource: services
    namespaces:
    - app-prod
  patches:
  - operation: remove
    path: "/metadata/annotations/service.beta.kubernetes.io~1azure-load-balancer-internal"
```

What it does: defines restore-time JSON patches for selected resources. This is useful when moving between clusters with different node labels, ingress annotations, or cloud provider annotations.

```bash
kubectl create configmap app-prod-restore-modifiers \
  --from-file=restore-resource-modifiers.yaml \
  -n velero

velero restore create app-prod-modified-restore \
  --from-backup app-prod-manual \
  --resource-modifier-configmap app-prod-restore-modifiers \
  --wait
```

What it does: stores restore modifiers and references them from a restore.

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
- [Velero resource filtering](https://velero.io/docs/v1.18/resource-filtering/)
- [Velero backup hooks](https://velero.io/docs/v1.18/backup-hooks/)
- [Velero restore resource modifiers](https://velero.io/docs/v1.18/restore-resource-modifiers/)
- [Cluster migration and disaster recovery](cluster-migration-and-disaster-recovery.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
