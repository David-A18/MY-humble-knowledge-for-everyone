---
type: Troubleshooting Guide
title: Persistent-volume binding and mount failures
description: Trace a blocked stateful Pod through claim binding, topology, attachment,
  mounting, and application filesystem access.
tags:
- kubernetes
- troubleshooting
- storage
- pvc
- csi
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: persistent-volumes
  title: Persistent Volumes
  resource: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- id: storage-classes
  title: Storage Classes
  resource: https://kubernetes.io/docs/concepts/storage/storage-classes/
---

# Persistent-volume binding and mount failures

Use this guide when a PersistentVolumeClaim (PVC) stays Pending or a Pod cannot use its persistent storage. A PVC requests storage; a PersistentVolume (PV) represents the bound storage asset; a StorageClass selects provisioning behavior. Binding, attachment, filesystem mounting, and application access are separate failure boundaries.

> [!WARNING]
> Preserve the claim, volume identifier, and backup evidence before recovery. Deleting a bound PVC can eventually delete the underlying disk under a `Delete` reclaim policy. Removing finalizers or force-detaching storage can bypass protection and risk data loss.[^persistent-volumes]

## Locate the blocked boundary

Start with namespace-scoped read access. PVs, StorageClasses, nodes, VolumeAttachments, and CSI components generally require additional operator permissions.

```bash
kubectl get pod,pvc -n <namespace>
kubectl describe pvc <claim> -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl get storageclass <class> -o yaml
```

What it does: connects the consumer to its claim and provisioner, then reads binding and kubelet events. If the claim has no StorageClass, first establish whether static binding or a default class was intended.

| Boundary / signal | Inspect next | Safe response |
| --- | --- | --- |
| Pending PVC; no suitable PV | Class, requested size, access modes, volume mode, selectors | Correct the request or provide compatible storage. |
| Waiting for first consumer | Pod scheduling and class binding mode | Diagnose placement before treating the wait as provisioning failure. |
| Provisioning error | CSI controller logs and provider identity/quota | Correct the specific controller/provider failure. |
| Bound PVC; attach or Multi-Attach error | Node, existing attachment, previous consumer, driver limits | Confirm the old writer is stopped before moving exclusive storage. |
| `FailedMount` | CSI node component, filesystem, mount options, referenced Secret availability | Escalate the exact driver event without exposing Secret values. |
| Mounted but application gets permission denied | UID/GID, supported `fsGroup` behavior, path permissions, read-only flags | Use a driver-supported permission model; avoid recursive world-writable changes. |

`WaitForFirstConsumer` delays provisioning/binding so placement can respect the consuming Pod's topology. `Immediate` provisioning can bind storage before the Pod's zone constraints are known. The CSI driver must support the intended mode.[^storage-classes]

## Inspect a bound claim without mutating it

Read the bound PV name from the PVC, then replace `<volume>` below. Do not paste full output into public issue trackers; it may contain infrastructure identifiers.

```bash
kubectl get pv <volume> -o yaml
kubectl get volumeattachments.storage.k8s.io
kubectl get csidrivers.storage.k8s.io
kubectl get pods -n <driver-namespace> -o wide
```

What it does: exposes reclaim policy, CSI volume handle, node affinity, and available attachment/driver information. Some drivers do not use attachment objects; absence alone is not proof of a fault. Inspect the specific failing controller/node container's logs with the storage operator.

`ReadWriteOnce` is a single-node access mode, not a universal single-Pod guarantee. `ReadWriteOncePod` provides stronger single-Pod access for supported CSI volumes. An application needing concurrent writers requires compatible storage and application semantics.[^persistent-volumes]

## Recovery and verification

Resolve provider identity, capacity, topology, or driver health first. Treat replacement claims, restored volumes, and forced detach as separate reviewed recovery procedures with a backup and writer-fencing plan. Do not delete the claim as a generic retry.

Success means the intended PVC is Bound to the expected asset, the Pod starts on a compatible node, and the application can read its expected data. A controlled write/read/restart check belongs only in an approved disposable dataset. Remove temporary consumers after diagnosis while preserving real data claims.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Stateful workload model](../core-objects/stateful-workloads.md).
- [Storage and snapshot tooling](../applications-and-tools/platform-tooling/storage-and-snapshots.md).
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^persistent-volumes]: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
[^storage-classes]: [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
