---
type: Explanation
title: Secrets Store CSI Driver
description: Mount external-store values as files without embedding provider SDK calls
  in each application.
tags:
- kubernetes
- platform-tooling
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: driver-introduction
  resource: https://secrets-store-csi-driver.sigs.k8s.io/
  title: Driver introduction
- id: rotation
  resource: https://secrets-store-csi-driver.sigs.k8s.io/topics/secret-auto-rotation
  title: Rotation
- id: providers
  resource: https://secrets-store-csi-driver.sigs.k8s.io/providers
  title: Providers
---

# Secrets Store CSI Driver

## Purpose

Mount external-store values as files without embedding provider SDK calls in each application.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## How it works

A node-side driver and provider plugin read a namespaced `SecretProviderClass`, authenticate to an external store, and mount allowed values into a Pod. Optional synchronization also creates Kubernetes Secrets.[^driver-introduction][^rotation][^providers]

This CSI driver delivers secret files. Application-data storage uses different drivers, such as EBS or EFS CSI.

## Pod configuration

Prerequisites: driver/provider installed on eligible nodes, an `app-store` SecretProviderClass in `demo`, and an authenticated service account. The provider must expose a file named `password` for this example.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-reader
  namespace: demo
spec:
  serviceAccountName: app
  containers:
    - name: app
      image: busybox:1.37.0
      command: ["sh", "-c", "test -s /mnt/secrets/password && sleep 3600"]
      volumeMounts:
        - name: secrets
          mountPath: /mnt/secrets
          readOnly: true
  volumes:
    - name: secrets
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: app-store
```

What it does: verifies a non-empty mounted file without printing its contents.

## Rotation and diagnostics

Configure rotation explicitly for the installed release. Applications must reopen files; environment variables and `subPath` mounts do not transparently reload values.

```bash
kubectl describe pod secret-reader -n demo
kubectl get secretproviderclasspodstatus -n demo
kubectl get daemonset -n kube-system
```

What it does: locates mount failures, provider-object status, and node-agent availability. Check credentials, external-secret existence, network access, and node-type compatibility.

## Availability and cleanup

A provider outage can prevent new Pods from starting while existing ones keep running. Include that dependency in node-upgrade planning. Test optional Secret synchronization and deletion behavior. Remove the lab Pod and its dedicated provider configuration; retain shared driver installations.

## Related links

- [Driver introduction](https://secrets-store-csi-driver.sigs.k8s.io/)
- [Rotation](https://secrets-store-csi-driver.sigs.k8s.io/topics/secret-auto-rotation)
- [Providers](https://secrets-store-csi-driver.sigs.k8s.io/providers)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^driver-introduction]: [Driver introduction](https://secrets-store-csi-driver.sigs.k8s.io/).
[^rotation]: [Rotation](https://secrets-store-csi-driver.sigs.k8s.io/topics/secret-auto-rotation).
[^providers]: [Providers](https://secrets-store-csi-driver.sigs.k8s.io/providers).
